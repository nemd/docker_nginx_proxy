FROM alpine:3.4

MAINTAINER michal@reapnet.io

RUN apk --update add nginx wget && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/* 

ENV DOCKERIZE_VERSION v0.2.0

RUN wget --no-check-certificate https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

EXPOSE 80/tcp 443/tcp

COPY nginx.conf.tmpl /tmp
COPY proxy.conf.tmpl /tmp

RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

CMD ["dockerize",\
		"-template", "/tmp/nginx.conf.tmpl:/etc/nginx/nginx.conf", \
		"-template", "/tmp/proxy.conf.tmpl:/etc/nginx/conf.d/proxy.conf", \
		"nginx", "-g", "daemon off;" \
	]
