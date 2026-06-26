# Bundling Recipes

Step-by-step recipes for installing and starting common infrastructure services inside a veris-sandbox container.

The base image is Debian-based with Python 3.12 and `apt-get` available. When an agent depends on a service that veris does not mock (e.g., Redis, Elasticsearch), install it in `Dockerfile.sandbox` and start it via `start.sh` before the agent process starts.

---

## Redis

**Weight: Light** — ~30 MB memory, ~5 MB image size increase.

**Install (Dockerfile.sandbox):**

```dockerfile
RUN apt-get update && apt-get install -y redis-server && rm -rf /var/lib/apt/lists/*
```

**Start (start.sh):**

```bash
redis-server --daemonize yes --maxmemory 128mb --maxmemory-policy allkeys-lru
```

**Health check:**

```bash
until redis-cli ping 2>/dev/null | grep -q PONG; do sleep 0.5; done
```

**Env var overrides:**

```
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
CELERY_BROKER_URL=redis://localhost:6379/0
```

**Memory:** ~30 MB baseline. Set `--maxmemory` to 128-256 MB.

**Notes:** No password needed in sandbox. If the agent uses Redis as a Celery broker, the same URL works.

---

## Elasticsearch (single-node)

**Weight: Heavy** — ~512 MB memory (256 MB heap minimum), ~500 MB image size increase. Confirm with user before bundling — external endpoint may be preferable.

**Install (Dockerfile.sandbox):**

```dockerfile
RUN curl -fsSL https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.12.0-linux-x86_64.tar.gz | tar xz -C /opt/ && \
    mv /opt/elasticsearch-8.12.0 /opt/elasticsearch && \
    /opt/elasticsearch/bin/elasticsearch-plugin remove x-pack-ml 2>/dev/null || true
```

**Start (start.sh):**

```bash
ES_JAVA_OPTS="-Xms256m -Xmx256m" /opt/elasticsearch/bin/elasticsearch \
  -d -p /tmp/es.pid \
  -Ediscovery.type=single-node \
  -Expack.security.enabled=false \
  -Ecluster.routing.allocation.disk.threshold_enabled=false
```

**Health check:**

```bash
until curl -sf http://localhost:9200/_cluster/health >/dev/null; do sleep 1; done
```

**Env var overrides:**

```
ELASTICSEARCH_URL=http://localhost:9200
ES_HOST=localhost
ES_PORT=9200
```

**Memory:** 256 MB heap minimum, ~512 MB total. Heaviest bundleable service.

**Notes:** Disable security (`xpack.security.enabled=false`) for sandbox. Single-node mode is required. If the agent creates indices at startup, they work against this instance.

---

## RabbitMQ

**Weight: Medium** — ~80 MB memory, ~30 MB image size increase.

**Install (Dockerfile.sandbox):**

```dockerfile
RUN apt-get update && apt-get install -y rabbitmq-server && rm -rf /var/lib/apt/lists/*
```

**Start (start.sh):**

```bash
rabbitmq-server -detached
```

**Health check:**

```bash
until rabbitmqctl status >/dev/null 2>&1; do sleep 1; done
```

**Env var overrides:**

```
AMQP_URL=amqp://guest:guest@localhost:5672
RABBITMQ_URL=amqp://guest:guest@localhost:5672
RABBITMQ_HOST=localhost
```

**Memory:** ~80 MB baseline.

**Notes:** Default guest/guest credentials. Management plugin on port 15672 is optional: `rabbitmq-plugins enable rabbitmq_management`.

---

## MinIO (S3-compatible)

**Weight: Light** — ~50 MB memory, ~90 MB image size increase (single binary).

**Install (Dockerfile.sandbox):**

```dockerfile
RUN curl -fsSL https://dl.min.io/server/minio/release/linux-amd64/minio -o /usr/local/bin/minio && \
    chmod +x /usr/local/bin/minio
```

**Start (start.sh):**

```bash
MINIO_ROOT_USER=minioadmin MINIO_ROOT_PASSWORD=minioadmin minio server /data/minio --console-address ":9001" &
```

**Health check:**

```bash
until curl -sf http://localhost:9000/minio/health/live >/dev/null; do sleep 0.5; done
```

**Env var overrides:**

```
AWS_ENDPOINT_URL=http://localhost:9000
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin
S3_ENDPOINT=http://localhost:9000
MINIO_ENDPOINT=localhost:9000
```

**Memory:** ~50 MB baseline.

**Notes:** Use minioadmin/minioadmin as default credentials. Agents using boto3 or any S3 SDK work with the `AWS_ENDPOINT_URL` override. To create buckets at startup, add to `start.sh` after the health check:

```bash
mc alias set local http://localhost:9000 minioadmin minioadmin && mc mb local/my-bucket
```

---

## SQLite

**Weight: None** — zero overhead, built into Python stdlib.

**Start:** No daemon. File-based.

**Env var overrides:**

```
DB_PATH=/tmp/agent.db
SQLITE_PATH=/tmp/agent.db
```

**Notes:** Simplest option. If the agent uses SQLite, just ensure the file path is writable. Works out of the box.

---

## LocalStack (AWS SDK mock)

**Weight: Heavy** — ~200 MB memory, ~300 MB image size increase. Confirm with user before bundling — for just S3, prefer MinIO (much lighter).

**Install (Dockerfile.sandbox):**

```dockerfile
RUN pip install localstack localstack-client awscli-local
```

**Start (start.sh):**

```bash
localstack start -d
```

**Health check:**

```bash
until curl -sf http://localhost:4566/_localstack/health >/dev/null; do sleep 1; done
```

**Env var overrides:**

```
AWS_ENDPOINT_URL=http://localhost:4566
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_DEFAULT_REGION=us-east-1
```

**Memory:** ~200 MB. Heavy.

**Notes:** Mocks S3, SQS, DynamoDB, Lambda, and many other AWS services. Use if the agent relies on multiple AWS services. For just S3, prefer MinIO (lighter).

---

## Memcached

**Weight: Light** — ~64 MB memory (configurable), ~2 MB image size increase.

**Install (Dockerfile.sandbox):**

```dockerfile
RUN apt-get update && apt-get install -y memcached && rm -rf /var/lib/apt/lists/*
```

**Start (start.sh):**

```bash
memcached -d -m 64 -p 11211 -u root
```

**Health check:**

```bash
echo stats | nc localhost 11211 | grep -q pid
```

**Env var overrides:**

```
MEMCACHED_HOST=localhost
MEMCACHED_PORT=11211
MEMCACHED_URL=localhost:11211
```

**Memory:** 64 MB (configurable via the `-m` flag).

---

## Node.js Version Override (only when the repo needs a different Node.js version)

**Weight: Light** — ~0 MB extra memory (runtime only), ~80 MB image size increase.

**Install (Dockerfile.sandbox):**

```dockerfile
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*
```

**Notes:** The current base image already includes Node.js. Use this only when the repo requires a different Node.js version than the base image ships with. This includes npm. For pnpm: `RUN npm install -g pnpm`. For yarn: `RUN npm install -g yarn`.

---

## General Guidelines

- **Clean apt lists:** Always end `apt-get install` lines with `rm -rf /var/lib/apt/lists/*`.
- **Background services:** Start services in `start.sh` with `&` (background) or daemon flags (`--daemonize`, `-d`, `-detached`).
- **Health checks before agent:** Always add a health-check wait loop in `start.sh` after starting each service and before starting the agent.
- **Memory budget:** All bundled services plus the agent share one container. Keep total memory reasonable.
- **Threshold:** If total bundled service memory exceeds ~1 GB, consider using external endpoints instead of bundling.
