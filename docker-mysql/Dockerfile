FROM ubuntu:12.04

RUN dpkg-divert --local --rename --add /sbin/initctl
RUN rm /sbin/initctl
RUN ln -s /bin/true /sbin/initctl

RUN echo "deb http://archive.ubuntu.com/ubuntu/ precise main universe" > /etc/apt/sources.list
RUN echo "deb http://archive.ubuntu.com/ubuntu/ precise-updates main universe" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get -y install mysql-server

RUN sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf

ADD ./startup.sh /opt/startup.sh
RUN chmod +x /opt/startup.sh

EXPOSE 3306

CMD ["/bin/bash", "/opt/startup.sh"]
