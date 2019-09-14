# Migrate GAE Datastore to SQL using Python

![](https://miro.medium.com/max/928/1*e--cLrtZtPqLOW2NGT2EEQ.png)

### Description
1. Clone https://github.com/wittfabian/datastore-sql-migration
2. Install requirements: `pip install -r requirements.txt`
2. Create google cloud credentials (https://cloud.google.com/docs/authentication/getting-started)
3. Replace `GOOGLE_APPLICATION_CREDENTIALS.json` with our generated credentials
3. Open `main.py` and update the parameters
4. Run `main.py`
5. This is what will you see:
```
SET FOREIGN_KEY_CHECKS=0;

-- Table user
INSERT INTO `user` (`id`, `first_name`, `last_name`, `email`, `date_created`) VALUES (1, 'Jens', 'Hohn', 'jens@Hohn.de', '2019-09-03T15:55:42');
INSERT INTO `user` (`id`, `first_name`, `last_name`, `email`, `date_created`) VALUES (2, 'Kenny', 'Spenny', 'kenny@spenny.de', '2019-08-27T10:23:02');

-- Table event
INSERT INTO `event` (`id`, `description`, `date_start`, `date_end`) VALUES (23, 'Description', '2018-10-10T16:30:00', '2018-10-10T19:00:00');

SET FOREIGN_KEY_CHECKS=1;
```