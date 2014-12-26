#!/bin/bash
set -e

cd /src

echo "Filling the configuration file..."
config=$(</config.py-docker);
config="$config\n    DEBUG = ${DEBUG:-False}"
config="$config\n    SECRET_KEY = '$SECRET_KEY'"
config="$config\n    KOZMIC_GITHUB_CLIENT_ID = '$GITHUB_CLIENT_ID'"
config="$config\n    KOZMIC_GITHUB_CLIENT_SECRET = '$GITHUB_CLIENT_SECRET'"
config="$config\n    SERVER_NAME = '$SERVER_NAME'"
config="$config\n    SESSION_COOKIE_DOMAIN = '$SERVER_NAME'"
config="$config\n    TAILER_URL_TEMPLATE = 'ws://$SERVER_NAME:8080/{job_id}/'"
config="$config\n    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mysql:@${DB_PORT_3306_TCP_ADDR}/kozmic'"
echo -e "$config" > ./kozmic/config_local.py

echo "Creating database..."
mysql -u mysql -h $DB_PORT_3306_TCP_ADDR -e "CREATE DATABASE IF NOT EXISTS kozmic CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
mysql -u mysql -h $DB_PORT_3306_TCP_ADDR -e "GRANT ALL PRIVILEGES ON kozmic.* TO kozmic@'%';"

echo "Running database migrations..."
KOZMIC_CONFIG=kozmic.config_local.Config ./manage.py db upgrade

KOZMIC_CONFIG=kozmic.config_local.Config \
WORKER_CONCURRENCY=${WORKER_CONCURRENCY:-3} \
supervisord -c /etc/supervisor.conf
