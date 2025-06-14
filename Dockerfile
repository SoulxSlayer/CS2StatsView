# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
# This is done first to leverage Docker's layer caching.
# If requirements.txt doesn't change, this layer won't be rebuilt.
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir reduces image size by not storing the pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (app.py and steam_viewer.html)
# from the current directory on the host to the /app directory in the container
COPY . .

# Make port 5000 available to the world outside this container
# This is the port your Flask app listens on.
EXPOSE 5000

# Define the command to run your application
# This will execute `python app.py` when the container starts.
CMD ["python", "app.py"]