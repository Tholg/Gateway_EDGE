# FROM python:3.6.9
FROM python:3.7.13-slim-buster
WORKDIR /app

COPY ./parameters.py .
COPY ./script.py .
COPY ./requirements.txt .

RUN pip3 install -r ./requirements.txt

CMD ["python3", "-u", "./script.py"]