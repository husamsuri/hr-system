# hr-system
this repo contains hr system using python, flask and mariaDb


CREATE DATABASE HR;
CREATE TABLE HR.applicants (id INT AUTO_INCREMENT NOT NULL, name VARCHAR(100), DOB DATE, experience_years TINYINT, department VARCHAR(100), created_at DATETIME, PRIMARY KEY (id));
