# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy dependencies file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask runs on
EXPOSE 8080

# Start the Flask app with Gunicorn (production ready)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
