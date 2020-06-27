FROM python:3.8.3-slim
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . .
RUN chmod 600 /app/*.key

CMD [ "python", "./main.py" ]