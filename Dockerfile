FROM python:3

RUN apt-get update

RUN apt install -y python3-dev libpq-dev nano

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-OO", "main.py" ]
