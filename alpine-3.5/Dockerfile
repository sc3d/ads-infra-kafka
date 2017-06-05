FROM registry2.applifier.info:5005/ads-infra-kontrol-alpine-3.5:1.0.0

ENV KONTROL_MODE=master,slave \
    KONTROL_PAYLOAD=/data/state \
    KONTROL_CALLBACK="python /home/kontrol/callback.py" \
    KAFKA_VERSION=0.10.2.1 \
    SCALA_VERSION=2.12 \
    GLIBC_VERSION=2.23-r3

ADD resources/ .
RUN set -ex && \
    mkdir -p /opt && \
    apk add --no-cache bash libc6-compat openjdk8-jre-base && \
    mirror=$(curl --stderr /dev/null https://www.apache.org/dyn/closer.cgi\?as_json\=1 | jq -r '.preferred') && \
    curl -sSL "${mirror}kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz" | tar -xzf - -C /opt