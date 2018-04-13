
FROM alpine:latest

RUN apk add --no-cache py-pip && pip install redis && pip install docker  && rm -f /var/cache/apk/*

WORKDIR /app

ADD  get_container_stats.py  /app/

CMD ["python","get_container_stats.py"]

