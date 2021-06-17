#!/bin/bash


echo "managing env variables"

env

envsubst '${MIGRANTS_HOSTNAME} ${PA_HOSTNAME} ${NGO_HOSTNAME} ${ANALYTIC_HOSTNAME} ${RASA_HOSTNAME} ${RASA_PRODUCTION_HOST} ${RASA_X_HOST}' < /usr/local/openresty/nginx/conf/nginx.conf.template > /usr/local/openresty/nginx/conf/nginx.conf

cat /usr/local/openresty/nginx/conf/nginx.conf 

echo "starting openresty"

/usr/bin/openresty
