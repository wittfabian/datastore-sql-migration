import os
from converter import DS2SQL

# set GOOGLE_APPLICATION_CREDENTIALS via environment variable
# other methods: https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'GOOGLE_APPLICATION_CREDENTIALS.json'

# set table name mapping
table_name_map = {
    'main_user': 'user',
    'main_event': 'event'
}

# ignores maybe old columns in datastore schema (optional)
ignore_columns_map = {
    'main_event': ['title'],
}

# create DS2SQL instance
agent = DS2SQL(table_list=list(table_name_map.keys()), table_name_map=table_name_map,
               ignore_columns_map=ignore_columns_map)

# run converter
agent.run(print_out=True, disable_pk=True, outfile_path='output.sql')
