FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY api.py ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./api.py"]
