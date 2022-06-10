FROM python:3.10
LABEL maintainer="Himanshu Nayal"

EXPOSE 8501

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./src ./src

ENTRYPOINT [ "streamlit", "run"]
CMD ["./src/main.py"]