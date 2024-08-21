FROM python:3.7-stretch

RUN pip install --upgrade pip

ADD requirements.txt /.
RUN pip install -r /requirements.txt

ADD . /code/

WORKDIR /code

CMD ["/code/src/main.py"]
ENTRYPOINT ["python"]
