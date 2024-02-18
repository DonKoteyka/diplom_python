FROM python:3.9


WORKDIR .

COPY . .

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONUNBUFFERED=1


CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000