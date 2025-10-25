# using ubuntu LTS version
FROM ubuntu:22.04 AS builder-image

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-dev python3-venv python3-pip python3-wheel build-essential git && \
   apt-get clean && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# install requirements
RUN pip3 install --no-cache-dir pyserial paho-mqtt

RUN git clone https://github.com/Matze2010/optolink-splitter-docker.git /opt/optolink-splitter/
 
FROM ubuntu:22.04 AS runner-image
RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-venv && \
   apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder-image /opt/venv /opt/venv
COPY --from=builder-image /opt/optolink-splitter /opt/optolink-splitter

ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 65234/tcp

CMD ["python3", "/opt/optolink-splitter/optolinkvs2_switch.py"]