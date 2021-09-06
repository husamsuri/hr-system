# hr-system
this repo contains hr system using python, flask and mariaDb

## how to run this project :
1. after you clone this project from github you need to activate python virtual environment by changing the current directory to HRSystem
2. you must have docker engine and should pull a MariaDB image by running `docker run -p 3306:3306 -d --name mariadb -eMARIADB_ROOT_PASSWORD=Password123! mariadb/server:10.4`
3. get inside the cli of that docker image and run `CREATE DATABASE HR;` to create the database that we're going to use
4. create applicants table by running `CREATE TABLE HR.applicants (id INT AUTO_INCREMENT NOT NULL, name VARCHAR(100), DOB DATE, experience_years TINYINT, department VARCHAR(100), created_at DATETIME, PRIMARY KEY (id));`
5. go back to the terminal that runs the python virtual environment and run `python3 app.py`
6. now your server is up and running
7. if you have any further questions you can contact me =)