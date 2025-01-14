FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY app.py .

# Install Flask
RUN pip install flask

# Set the command to run the application
CMD ["python", "app.py"]
