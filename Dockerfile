FROM python:3.10.8-slim-buster

EXPOSE 5000

WORKDIR /app      

COPY . .  

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host", "0.0.0.0"]