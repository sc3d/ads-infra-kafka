## Apache Kafka/Pixy+Kontrol pod

### Overview

This project is a [**Docker**](https://www.docker.com) image packaging
[**Apache Kafka 0.10.2.1**](https://kafka.apache.org/) together with
[**Pixy**](https://github.com/mailgun/kafka-pixy) and
[**Kontrol**](https://github.com/UnityTech/ads-infra-kontrol). It is meant
to be included in a [**Kubernetes**](https://github.com/GoogleCloudPlatform/kubernetes)
pod.

The container will just run the JVM broker and does not include a control tier: *kontrol* runs
in slave mode which means you need to point to one or more control tiers in the YAML manifest.

### Lifecycle

Turning the JVM on/off is done via a regular supervisor job. If a broker fails
(e.g is not serving requests anymore) the automaton will attempt to re-start it.

The initial state will render the various configuration files including the
[**telegraf**](https://github.com/influxdata/telegraf) one. The broker is configured
to use dynamic id assignment (e.g from the data volume or zookeeper). Both the broker
and its proxy are started immediately.

### Pixy

The pixy proxy is bundled in the image as well and configured against the local broker. It
exposes a gRPC as well as a HTTP API at TCP 19091 and 19092.

### Building the image

Pick a distro and build from the top-level directory. For instance:

```
$ docker build -f alpine-3.5/Dockerfile .
```

### Manifest

It is important to run this pod as a *stateful set* in order to keep volumes properly
assigned. Note that anti-affinity should be used to spread the pods and land the brokers
on separate machines. For instance:

```
apiVersion: apps/v1beta1
kind: StatefulSet
metadata:
  name: kafka
  namespace: test
spec:
  serviceName: kafka
  replicas: 3
  template:
    metadata:
      labels:
        app: kafka
        role: broker
        tier: data
      annotations:
        kontrol.unity3d.com/opentsdb: kairosdb.us-east-1.applifier.info
        kafka.unity3d.com/overrides: |
          default.replication.factor=3
          num.partitions=32
          retention.ms=259200000
    spec:
      nodeSelector:
        unity3d.com/array: data
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values: 
                    - kafka
              topologyKey: "kubernetes.io/hostname"
      containers:
       - image: registry2.applifier.info:5005/ads-infra-kafka-alpine-3.5
         name: kafka
         imagePullPolicy: Always
         volumeMounts:
         - name: data
           mountPath: "/data"
         ports:
         - containerPort: 8000
           protocol: TCP
         - containerPort: 9092
           protocol: TCP
         - containerPort: 19091
           protocol: TCP
         - containerPort: 19092
           protocol: TCP
         env:
          - name: NAMESPACE
            valueFrom:
              fieldRef:
                fieldPath: metadata.namespace
  volumeClaimTemplates:
    - metadata:
        name: data
        namespace: test
        annotations:
          volume.beta.kubernetes.io/storage-class: ebs
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 250Gi
```

### Support

Contact olivierp@unity3d.com for more information about this project.