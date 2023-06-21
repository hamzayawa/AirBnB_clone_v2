#!/usr/bin/env bash
#Sets up web servers for deployment of web_static

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
printf "<html>
  <head>
  </head>
  <body>
    Best School
  </body>
</html>" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data/
sed -i '/listen 80 default_server;/a location  /hbnb_static { alias /data/web_static/current; autoindex off; }' /etc/nginx/sites-available/default
service nginx restart
