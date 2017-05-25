FROM registry2.applifier.info:5005/ads-infra-kontrol-alpine-3.5:1.0

ENV KONTROL_MODE=slave,verbose \
    KONTROL_PAYLOAD=/data/state \
    KAFKA_VERSION=0.10.2.1 \
    SCALA_VERSION=2.12 \
    PIXY_VERSION=0.13.0

ADD resources/ .
RUN set -ex && \
    apk add --no-cache openjdk8-jre-base bash && \
    mkdir -p /opt && \
    mirror=$(curl --stderr /dev/null https://www.apache.org/dyn/closer.cgi\?as_json\=1 | jq -r '.preferred') && \
    curl -sSL "${mirror}kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz" | tar -xzf - -C /opt && \
    curl -L https://github.com/mailgun/kafka-pixy/releases/download/v${PIXY_VERSION}/kafka-pixy-v${PIXY_VERSION}-linux-amd64.tar.gz | tar -xzf - -C /opt && \
    echo 'hosts: files mdns4_minimal [NOTFOUND=return] dns mdns4' >> /etc/nsswitch.conf