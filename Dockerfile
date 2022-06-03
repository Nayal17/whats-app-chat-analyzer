FROM python:3.9.1-slim

COPY analyzer.py .

COPY main.py .

COPY preprocess.py .

COPY requirements.txt .

RUN pip --install -r requirements.txt

EXPOSE 8051

ENTRYPOINT ["streamlit","run"]

CMD ["./main.py"]
