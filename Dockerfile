# Base Image
FROM python:3.12.7

# Set working directory
WORKDIR /usr/src/app

# Create a directory for local repository
RUN mkdir -p /usr/src/app/packages

# Expose the directory through a web server
RUN pip install flask requests

# Copy the script to serve files
COPY serve.py /usr/src/app/

# Expose port for access
EXPOSE 5000

# Run the Flask server
CMD ["python", "serve.py"]
