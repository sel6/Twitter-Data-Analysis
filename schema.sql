DROP TABLE IF EXISTS tweet_data;

CREATE TABLE IF NOT EXISTS tweet_data(
id int not null AUTO_INCREMENT,
created_at TEXT NOT NULL,
source VARCHAR(200) NOT NULL,
original_text TEXT DEFAULT NULL,
polarity FLOAT DEFAULT NULL,
subjectivity FLOAT DEFAULT NULL,
lang TEXT DEFAULT NULL,
favorite_count INT DEFAULT NULL,
original_author TEXT DEFAULT NULL,
followers_count INT DEFAULT NULL,
friends_count INT DEFAULT NULL,
possibly_sensitive TEXT DEFAULT NULL,
hashtags TEXT DEFAULT NULL,
user_mentions TEXT DEFAULT NULL,
place TEXT DEFAULT NULL,
place_coordinate VARCHAR(100) DEFAULT NULL, PRIMARY KEY(id));