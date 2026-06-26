# Deployment Guide

Production deployment patterns for Teamgram Server.

## Docker Compose (Single Node)

### Quick Start

```yaml
version: '3.8'

services:
  # Dependencies
  mysql:
    image: mysql:8.0
    environment:
      # ⚠️ 生产环境：使用强密码，通过 .env 文件或 secrets 注入
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-changeme}
      MYSQL_DATABASE: teamgram
    volumes:
      - mysql_data:/var/lib/mysql
      - ./data/teamgram.sql:/docker-entrypoint-initdb.d/1.sql
    # ⚠️ 安全警告：生产环境应该注释掉端口映射，或限制只允许应用服务器访问
    # 使用 Docker network 或防火墙限制访问
    ports:
      - "127.0.0.1:3306:3306"  # 仅本地访问，或完全注释掉

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    # ⚠️ 安全警告：生产环境应该限制访问，建议启用密码认证
    # command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "127.0.0.1:6379:6379"  # 仅本地访问

  etcd:
    image: quay.io/coreos/etcd:v3.5.0
    environment:
      ETCD_NAME: etcd
      ETCD_DATA_DIR: /etcd-data
      ETCD_LISTEN_CLIENT_URLS: http://0.0.0.0:2379
      ETCD_ADVERTISE_CLIENT_URLS: http://etcd:2379
    volumes:
      - etcd_data:/etcd-data
    ports:
      - "2379:2379"

  kafka:
    image: confluentinc/cp-kafka:latest
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports:
      - "9092:9092"

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minio
      MINIO_ROOT_PASSWORD: minio123
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"

  # Teamgram Services
  authsession:
    build:
      context: .
      dockerfile: Dockerfile
    command: ./authsession -f /app/etc/authsession.yaml
    volumes:
      - ./app/service/authsession/etc:/app/etc
    depends_on:
      - mysql
      - redis
      - etcd

  biz:
    build:
      context: .
      dockerfile: Dockerfile
    command: ./biz -f /app/etc/biz.yaml
    volumes:
      - ./app/service/biz/etc:/app/etc
    depends_on:
      - mysql
      - redis
      - etcd
      - kafka

  gnetway:
    build:
      context: .
      dockerfile: Dockerfile
    command: ./gnetway -f /app/etc/gnetway.yaml
    ports:
      - "443:443"
    volumes:
      - ./app/interface/gnetway/etc:/app/etc
    depends_on:
      - authsession
      - session

  httpserver:
    build:
      context: .
      dockerfile: Dockerfile
    command: ./httpserver -f /app/etc/httpserver.yaml
    ports:
      - "8080:8080"
    volumes:
      - ./app/interface/httpserver/etc:/app/etc
    depends_on:
      - biz

volumes:
  mysql_data:
  redis_data:
  etcd_data:
  minio_data:
```

## Kubernetes (Production)

### Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: teamgram
```

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: teamgram-config
  namespace: teamgram
data:
  MYSQL_DATA_SOURCE: "user:pass@tcp(mysql:3306)/teamgram"
  REDIS_HOST: "redis:6379"
  ETCD_ENDPOINTS: "etcd:2379"
  KAFKA_BROKERS: "kafka:9092"
```

### MySQL StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
  namespace: teamgram
spec:
  serviceName: mysql
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: root-password
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: data
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
```

### Biz Service Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: teamgram-biz
  namespace: teamgram
spec:
  replicas: 3
  selector:
    matchLabels:
      app: teamgram-biz
  template:
    metadata:
      labels:
        app: teamgram-biz
    spec:
      containers:
      - name: biz
        image: teamgram/biz:latest
        ports:
        - containerPort: 20001
        envFrom:
        - configMapRef:
            name: teamgram-config
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          grpc:
            port: 20001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          grpc:
            port: 20001
          initialDelaySeconds: 5
          periodSeconds: 5
```

### HPA (Horizontal Pod Autoscaler)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: teamgram-biz-hpa
  namespace: teamgram
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: teamgram-biz
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: teamgram-ingress
  namespace: teamgram
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "100m"
spec:
  tls:
  - hosts:
    - api.yourdomain.com
    secretName: teamgram-tls
  rules:
  - host: api.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: teamgram-gnetway
            port:
              number: 443
```

## High Availability Setup

### Database Clustering

**MySQL Group Replication:**
```yaml
# Primary
mysql-0: write + read
# Replicas
mysql-1: read
mysql-2: read
```

**Redis Cluster:**
```yaml
# 3 master + 3 replica
redis-0: master (slots 0-5460)
redis-1: master (slots 5461-10922)
redis-2: master (slots 10923-16383)
```

### Service Mesh (Istio)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: teamgram-biz
  namespace: teamgram
spec:
  hosts:
  - teamgram-biz
  http:
  - route:
    - destination:
        host: teamgram-biz
    timeout: 5s
    retries:
      attempts: 3
      perTryTimeout: 2s
```

## Monitoring Stack

### Prometheus + Grafana

```yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: teamgram-metrics
  namespace: teamgram
spec:
  selector:
    matchLabels:
      app: teamgram
  endpoints:
  - port: metrics
    interval: 15s
```

### Alerting Rules

```yaml
groups:
- name: teamgram
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High error rate detected"

  - alert: ServiceDown
    expr: up{job="teamgram"} == 0
    for: 1m
    labels:
      severity: critical
```

## Backup Strategy

### Database Backup

```bash
#!/bin/bash
# Daily backup
mysqldump -h mysql -u root -p teamgram > backup-$(date +%Y%m%d).sql

# Upload to S3
aws s3 cp backup-*.sql s3://teamgram-backups/mysql/
```

### Kubernetes CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: mysql-backup
  namespace: teamgram
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: mysql:8.0
            command:
            - /bin/sh
            - -c
            - |
              mysqldump -h mysql -u root -p$MYSQL_ROOT_PASSWORD teamgram | \
              gzip > /backup/teamgram-$(date +%Y%m%d).sql.gz
              aws s3 cp /backup/teamgram-*.sql.gz s3://teamgram-backups/
            env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: root-password
          restartPolicy: OnFailure
```

## Security Hardening

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: teamgram-policy
  namespace: teamgram
spec:
  podSelector:
    matchLabels:
      app: teamgram
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 443
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: mysql
    ports:
    - protocol: TCP
      port: 3306
```

### Secrets Management

```bash
# Create secrets
kubectl create secret generic mysql-secret \
  --from-literal=root-password=$(openssl rand -base64 32) \
  -n teamgram

# Vault integration (optional)
vault kv put secret/teamgram/mysql root-password=$(openssl rand -base64 32)
```

## Troubleshooting

### Common Issues

**1. Connection refused:**
```bash
# Check if service is running
kubectl get pods -n teamgram

# Check logs
kubectl logs -f deployment/teamgram-biz -n teamgram

# Check service endpoints
kubectl get endpoints -n teamgram
```

**2. High latency:**
```bash
# Check resource usage
kubectl top pods -n teamgram

# Check for OOM kills
kubectl get events -n teamgram --field-selector reason=OOMKilled
```

**3. Database connection pool exhausted:**
```yaml
# Increase pool size in config
MySQL:
  MaxOpenConns: 100
  MaxIdleConns: 10
```
