FROM python:3.10-slim
LABEL maintainer="Himanshu Nayal"

EXPOSE 8501

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install streamlit
RUN pip install -r requirements.txt

COPY ./src /examples
ENTRYPOINT [ "streamlit", "run"]
CMD ["/examples/intro.py"]