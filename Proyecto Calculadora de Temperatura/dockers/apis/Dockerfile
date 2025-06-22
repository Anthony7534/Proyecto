#Download base image ubuntu:22.04
FROM ubuntu:22.04

#Information
LABEL maintainer="Ian"
LABEL project="Pruebas_Webs"

# Update the image to the latest packages
RUN apt-get update && \
    apt-get install supervisor -y

# Init Web service
EXPOSE 80

# Configuration supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]
