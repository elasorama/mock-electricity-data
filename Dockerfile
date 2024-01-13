# Base python image
FROM python:3.11

# Adding the app and the requirements.txt to container
WORKDIR /app
COPY app.py /app
COPY requirements.txt /app

# Installing the requirements
RUN pip install -r requirements.txt

# Exposing the port 8000
EXPOSE 8000

# Running the app
CMD ["python", "app.py"]
