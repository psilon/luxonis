# syntax=docker/dockerfile:1
FROM python:3.9.5-slim
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
# CMD ["scrapy","runspider", "srealityscraper/spiders/srealityspider.py"]
CMD ["flask", "run"]
