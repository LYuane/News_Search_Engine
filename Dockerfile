FROM python:3.7

MAINTAINER yuane <tongyz@bupt.edu.cn>

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN TZ=Asia/shanghai 
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y

RUN	pip3 install lxml \
	jieba \
	Flask \
	bs4 \
	sklearn

COPY ./src /var/src/

WORKDIR /var/src/web/

EXPOSE 5000

#CMD ["python3","main.py"]
