# Use Python image
FROM public.ecr.aws/docker/library/python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Copy .env file
COPY .env .env

# Expose Restapi port
EXPOSE 8000

# Run Restapi FastAPI service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
