# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies and the ODBC Driver
RUN apt-get update && apt-get install -y \
    gcc \
    unixodbc-dev \
    curl \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y \
    msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

# Copy the application files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Set the command to run the application
CMD ["python", "app.py"]
