# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:2.7-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install Flask flask_cors

RUN apt-get -y update 
RUN apt-get -y install gdal-bin 
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD ["python","app.py"]

# gcloud builds submit --tag gcr.io/rock-sublime-819/ogrservice