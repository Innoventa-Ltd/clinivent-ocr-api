FROM python:3.10-slim

# system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    easyocr \
    numpy \
    pillow \
    opencv-python-headless \
    pdf2image \
    python-multipart \
    torch==2.2.0 \
    torchvision==0.17.0

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]