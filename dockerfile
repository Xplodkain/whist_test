FROM python:latest

WORKDIR /app

COPY app.py  .
COPY requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "app.py" ]

EXPOSE 5000