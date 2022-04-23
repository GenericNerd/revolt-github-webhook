FROM python:3.10-alpine
WORKDIR /main
COPY . .
RUN pip install -r requirements.txt
CMD ["python3.10", "main.py"]