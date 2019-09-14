import datetime
from google.cloud import datastore
from datetime import datetime


class DS2SQL:
    def __init__(self, table_list, table_name_map=None, ignore_columns_map=None, client=None):
        self.table_list = table_list
        self.table_name_map = table_name_map or {}
        self.ignore_columns_map = ignore_columns_map or {}

        if client is None:
            client = datastore.Client()

        self.client = client

        self.pk_map = {}
        self.table_schema = {}

    @property
    def base_insert_str(self):
        return 'INSERT INTO `{table_name}` ({keys}) VALUES ({values});'

    def get_or_create_pk_map_value(self, table_name, org_value):
        table_map = self.pk_map.setdefault(table_name, {})
        new_value = table_map.setdefault(org_value, max(list(table_map.values()) + [0]) + 1)
        self.pk_map[table_name] = table_map
        return new_value

    def map_pk_value(self, org_value):
        for table_name, pk_map in self.pk_map.items():
            for pk_key, new_value in pk_map.items():
                if pk_key == org_value:
                    return table_name, new_value
        return None, None

    def convert_value(self, value):
        if isinstance(value, str):
            return '\'{}\''.format(value)

        if isinstance(value, bool):
            return str(value).lower()

        if value is None:
            return 'NULL'

        if isinstance(value, datetime):
            if value.date() == datetime(1970, 1, 1).date():
                return '\'{}\''.format(value.strftime('%H:%M:%S'))

            return '\'{}\''.format(value.strftime('%Y-%m-%dT%H:%M:%S'))

        if isinstance(value, list):
            return '\'{}\''.format(','.join('{}'.format(v) for v in value))

        if isinstance(value, datastore.key.Key):
            return str(self.get_or_create_pk_map_value(value.kind, value.id))

        if isinstance(value, int) and len(str(value)) > 10:
            _, mapped_value = self.map_pk_value(value)
            if mapped_value is not None:
                return str(mapped_value)
            else:
                return 'NULL'

        return str(value)

    def update_pk_map(self, table_name):
        for item in self.client.query(kind=table_name).fetch():
            self.get_or_create_pk_map_value(table_name, item.id)

        return True

    def update_table_schema(self, table_name):
        tmp_table_schema = self.table_schema.get(table_name, set())
        ignore_list = self.ignore_columns_map.get(table_name, set())

        tmp_table_schema.add('id')
        for item in self.client.query(kind=table_name).fetch():
            tmp_table_schema.update([v for v in item.keys() if not v.startswith('_') and v not in ignore_list])

        self.table_schema[table_name] = tmp_table_schema

    def run(self, print_out=True, disable_pk=False, outfile_path=None):
        insert_list = []

        # create/update pk mapping dict for pks in table_name
        for table_name in self.table_list:
            self.update_pk_map(table_name)
            self.update_table_schema(table_name)

        for table_name in self.table_list:
            ignore_list = self.ignore_columns_map.get(table_name, set())
            new_table_name = self.table_name_map.get(table_name, table_name)

            insert_list.append('\n-- Table {}'.format(new_table_name))

            for item in self.client.query(kind=table_name).fetch():
                # set default schema
                insert_dict = dict(('`{}`'.format(k), 'NULL') for k in self.table_schema[table_name])

                key_list = ['id'] + list(item.keys())
                values_list = [item.key] + list(item.values())
                for key, value in zip(key_list, values_list):
                    # ignore datastore index
                    if key.startswith('_') or key in ignore_list:
                        continue

                    insert_dict.update({'`{}`'.format(key): self.convert_value(value)})

                insert_list.append(self.base_insert_str.format(table_name=new_table_name,
                                                               keys=', '.join(insert_dict.keys()),
                                                               values=', '.join(insert_dict.values())))

        if disable_pk is True:
            insert_list = ['\nSET FOREIGN_KEY_CHECKS=0;'] + insert_list + ['\nSET FOREIGN_KEY_CHECKS=1;']

        if print_out is True:
            print(*insert_list, sep="\n")

        if outfile_path is not None:
            with open(outfile_path, 'w') as f:
                for item in insert_list:
                    f.write("%s\n" % item)

        return True
