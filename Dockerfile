FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ghostscript python3-tk libglib2.0-0 libsm6 libxext6 libxrender-dev libpoppler-cpp-dev build-essential libgl1 && \
    pip install --upgrade pip

# Copy code
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Expose and start
EXPOSE 10000
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]
