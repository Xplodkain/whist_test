FROM python:latest

WORKDIR /app

COPY app.py  .
COPY requirements.txt .
RUN pip uninstall mysql-connector
RUN pip uninstall mysql-connector-python
RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "app.py" ]

EXPOSE 5000