# Set the base image to Python 3
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy requirements
COPY ./requirements.txt /app/requirements.txt

# Install the required packages for the Flask app
RUN pip install -r requirements.txt

# Copy the current directory contents into the container
COPY . /app

# Expose port 8000 for the Flask app to run on
EXPOSE 8000

# Set the command to start the WSGI server
CMD ["uwsgi", "--http", "0.0.0.0:8000", "-w", "wsgi:app"]
