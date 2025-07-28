FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y \
    ghostscript \
    python3-tk \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libpoppler-cpp-dev \
    build-essential \
    libgl1 && \
    pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
