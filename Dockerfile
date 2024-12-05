FROM python:3.13

RUN apt-get update && apt-get install -y dumb-init && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

ADD ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000

ADD krs.py /app
ADD cache.txt /app
ADD krs_aktualny.pdf /app
ADD krs_pelny.pdf /app
ADD krs.html /app

CMD ["python", "krs.py"]
