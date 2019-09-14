SET FOREIGN_KEY_CHECKS=0;

-- Table user
INSERT INTO `user` (`id`, `first_name`, `last_name`, `email`, `date_created`) VALUES (1, 'Jens', 'Hohn', 'jens@hohn.de', '2019-09-03T15:55:42');
INSERT INTO `user` (`id`, `first_name`, `last_name`, `email`, `date_created`) VALUES (2, 'Kenny', 'Spenny', 'kenny@spenny.de', '2019-08-27T10:23:02');

-- Table event
INSERT INTO `event` (`id`, `title`, `description`, `date_start`, `date_end`) VALUES (23, 'Title', 'Description', '2018-10-10T16:30:00', '2018-10-10T19:00:00');

SET FOREIGN_KEY_CHECKS=1;
