FROM python:3.12.4

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m textblob.download_corpora

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
