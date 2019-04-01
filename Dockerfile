FROM oaklabs/grpcio-tools:python3.7.0-1.15.0

COPY *.proto /protos/

RUN python -m grpc_tools.protoc --proto_path=/protos/ --python_out=/protos/ --grpc_python_out=/protos/ /protos/*.proto

FROM python:3.7.0-alpine

WORKDIR /src/

RUN apk --no-cache add build-base=0.5-r1 python-dev=2.7.15-r1

COPY src/requirements.txt ./
RUN pip install -r requirements.txt

COPY src/ ./

COPY --from=0 /protos/ /protos/

ENV PYTHONUNBUFFERED=yes \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/protos/

CMD python server.py

ENV PORT=9100