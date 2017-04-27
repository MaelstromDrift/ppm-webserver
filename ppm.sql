
CREATE TABLE IF NOT EXISTS ppm_follower (
  _id int(11) NOT NULL AUTO_INCREMENT,
  userId int(11) NOT NULL,
  processId int(11) NOT NULL,
  PRIMARY KEY _id (_id)
);

CREATE TABLE IF NOT EXISTS ppm_process (
  _id int(11) NOT NULL AUTO_INCREMENT,
  title varchar(50) NOT NULL,
  description varchar(500) NOT NULL,
  creatorId int(11) NOT NULL,
  categoryId int(11) NOT NULL
  PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS ppm_process_category (
  categoryId int(11) NOT NULL AUTO_INCREMENT,
  categoryName varchar(30) NOT NULL UNIQUE,
  PRIMARY KEY (categoryId)
);

CREATE TABLE IF NOT EXISTS ppm_task (
  _id int(11) NOT NULL AUTO_INCREMENT,
  title varchar(50) NOT NULL,
  description varchar(500) NOT NULL,
  creatorId int(11) NOT NULL,
  PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS ppm_process_followed_tasks (
	_id int(11) PRIMARY KEY AUTO_INCREMENT,
	processId int(11) NOT NULL,
	taskId int(11) NOT NULL,
	taskOrder int(3) NOT NULL
);

CREATE TABLE IF NOT EXISTS ppm_task_review (
  _id int(11) NOT NULL AUTO_INCREMENT,
  comment varchar(1000) NOT NULL,
  taskRating int(11) NOT NULL,
  isLiked int(11) NOT NULL DEFAULT 0,
  userId int(11) NOT NULL,
  taskId int(11) NOT NULL,
  numberOfLikes int(11) NOT NULL DEFAULT 0,
  numberOfDislikes int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS ppm_user (
  _id int(11) NOT NULL AUTO_INCREMENT,
  username varchar(30) NOT NULL UNIQUE,
  firstname varchar(255) NOT NULL,
  lastname varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  PRIMARY KEY (_id)
);

ALTER TABLE ppm_task
  ADD CONSTRAINT ppm_task_fk_1 FOREIGN KEY (creatorId) REFERENCES ppm_user (_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE ppm_task_review
  ADD CONSTRAINT ppm_task_review_fk_1 FOREIGN KEY (taskId) REFERENCES ppm_task (_id) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT ppm_task_review_fk_2 FOREIGN KEY (userId) REFERENCES ppm_user (_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE ppm_process_followed_tasks
  ADD CONSTRAINT ppm_followed_tasks_fk_1 FOREIGN KEY (processId) REFERENCES ppm_process(_id) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT ppm_followed_tasks_fk_2 FOREIGN KEY (taskId) REFERENCES ppm_task(_id) ON DELETE CASCADE ON UPDATE CASCADE;