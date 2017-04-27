# README #
This is the Server that the Personal Process Manager app is set up to communicate with. It is very bare bones and is used to just provide back end functionality with practically no security. This server was set up and tested running on an Ubuntu server and I can make no guarantees that it will run on a different operating system.

#Set-up#
1. Make sure that you have some type of database setup as well as Python and PIP installed on your machine. I prefer to use PHPMyAdmin and MySql due to their easy to setup nature.
2. From pip install Flask, SQLAlchemy.
3. Once the dependencies are installed you need to tell Flask which file it should run by typing export FLASK_APP=ppm_webserver.py into the console.
4. Finally start the server with the command flask run --host=0.0.0.0