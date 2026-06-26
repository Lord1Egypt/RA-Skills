# Infrastructure Patterns — Restructuring Guide

Reference for converting agent infrastructure into the veris-sandbox single-container setup. Covers 7 common architecture patterns.

Use this file for architecture shapes only. For canonical service names, current `veris.yaml` schema, and current env-var flow, rely on:
- `reference/service-mapping.md`
- `reference/veris-yaml-schema.md`
- `reference/env-var-overrides.md`

## Veris-Sandbox Container Model

Everything runs in ONE Docker container. The agent's code is COPY'd to `/agent/` by the Dockerfile.sandbox. The simulation config (`veris.yaml`) is mounted at `/config/veris.yaml` by the CLI at runtime — it is NOT baked into the image. Veris provides mock services, an LLM proxy, an actor simulator, and a simulation engine — all as co-resident processes. The agent starts via a single `entry_point` command defined in `veris.yaml`.

At startup, veris's `entrypoint.sh` does `cd $AGENT_CODE_PATH` (from `agent.code_path` in veris.yaml, typically `/agent`), then runs the entry_point command. This means **all entry_point paths are relative to code_path**.

**Reserved Veris ports (do NOT use for the agent):** 6100-6299, 5432, 443.
**Recommended agent ports:** 8080, 3000, 3001.

---

## Pattern 1: Docker Compose — Single Agent + Infrastructure

**Typical setup:** FastAPI app + Postgres + Redis + Elasticsearch + Celery workers + nginx, all defined in `docker-compose.yml`.

**Characteristics:** One service is the agent (the thing a user talks to). Everything else is infrastructure the agent depends on.

### How to identify the agent service

Look for these signals in `docker-compose.yml`:

- Has the main HTTP port mapping (`ports: "8000:8000"`)
- Has a `command:` like `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- Other services `depends_on` it, or it depends on everything else
- Named something like `api`, `app`, `web`, `server`, `agent`

### Restructuring steps

**1. Copy only the agent's code:**

```dockerfile
# Dockerfile.sandbox
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

COPY requirements.txt /agent/
WORKDIR /agent
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /agent/src/

WORKDIR /app
```

Only copy the directory the agent service mounts or builds from. Do NOT copy Postgres data dirs, nginx configs, etc.

**2. Set the entry point:**

```yaml
# veris.yaml
agent:
  entry_point: uvicorn app.main:app --host 0.0.0.0 --port 8080
  port: 8080
  code_path: /agent
```

Match the `command:` from docker-compose, adjusting the port if needed. Entry point paths are relative to code_path (entrypoint.sh cd's there first).

**3. Replace infrastructure hostnames with localhost:**

Docker compose services communicate by service name (`postgres`, `redis`, `elasticsearch`). In veris, everything is localhost. Override via environment variables:

```yaml
# veris.yaml
agent:
  environment:
    DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/${SIMULATION_ID}"
    REDIS_URL: "redis://localhost:6379"
    ELASTICSEARCH_URL: "http://localhost:9200"
```

**4. Handle Celery workers:**

- If Celery processes tasks triggered during a user conversation (e.g., async tool calls, webhook processing), they are needed. Add them to a `start.sh`:

```bash
#!/bin/bash
# Start Celery worker in background
celery -A app.celery_app worker --loglevel=info &

# Start the agent in foreground
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Note: start.sh runs from code_path (/agent), so no `cd` needed at the top.

- If Celery only runs scheduled/cron tasks (daily reports, batch jobs), it is likely not needed during simulation. Skip it.

**5. Skip nginx:**

Veris has its own nginx for TLS termination. The agent's nginx reverse proxy config is not needed.

**6. Bundle or skip other services:**

| Service | Decision |
|---|---|
| Redis | Bundle if agent uses it for caching/sessions during requests. Install in Dockerfile.sandbox: `apt-get install -y redis-server`, start in start.sh. |
| Elasticsearch | Heavy (~500MB). Use external endpoint if possible. Bundle only if agent queries ES on the critical path. Ask user first|
| MinIO/S3 | Lightweight. Bundle if agent stores/retrieves files during conversation. |
| Monitoring (Prometheus, Grafana) | Skip. Not needed for simulation. |

---

## Pattern 2: Single Container + supervisord / Multi-Process

**Typical setup:** supervisord managing FastAPI + webhook listener + alert poller + log shipper, all in one container.

**Characteristics:** Already single-container. Multiple processes managed by supervisord or a process manager.

### Restructuring steps

**1. Copy the entire app directory:**

```dockerfile
# Dockerfile.sandbox
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

COPY requirements.txt /agent/
WORKDIR /agent
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /agent/app/

WORKDIR /app
```

**2. Replace supervisord with start.sh:**

Supervisord adds unnecessary complexity for simulation. Replace it with a shell script that backgrounds processes.

Given a `supervisord.conf` like:

```ini
[program:api]
command=uvicorn app.main:app --port 8080

[program:webhook_listener]
command=python webhook_listener.py

[program:alert_poller]
command=python alert_poller.py

[program:fluent-bit]
command=/opt/fluent-bit/bin/fluent-bit -c /etc/fluent-bit.conf
```

Create this `start.sh`:

```bash
#!/bin/bash

# Triage: which processes are needed for simulation?

# NEEDED — webhook listener (persona/services send webhooks to agent)
python webhook_listener.py &

# NEEDED — alert poller (triggers agent behavior during simulation)
python alert_poller.py &

# SKIP — fluent-bit is a log shipper sidecar, agent code doesn't import it

# FOREGROUND — main API server (always needed)
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
```

**3. Process triage rules:**

| Process type | Needed? |
|---|---|
| Main API server | Always. Runs in foreground with `exec`. |
| Webhook listener | Yes, if persona or veris services send webhooks to the agent. |
| Poller/scheduler | Yes, if it triggers agent actions during simulation time window. |
| Log shipper (fluent-bit, fluentd) | No, unless agent code directly imports/queries it. |
| Health check sidecar | No. Veris has its own health checks. |
| Metrics exporter | No. Not needed for simulation. |

**4. SQLite:**

If the agent uses SQLite, it works out of the box (file-based, no install needed). Ensure the path is writable — use `/agent/data/` or `/tmp/`.

**5. Entry point:**

```yaml
# veris.yaml
agent:
  entry_point: bash start.sh
  port: 8080
  code_path: /agent
```

Entry point paths are relative to code_path (entrypoint.sh cd's there first).

---

## Pattern 3: Cloud-Specific Services (Azure / AWS / GCP)

**Typical setup:** Azure OpenAI + Azurite + Cosmos DB emulator + Azure FHIR, or AWS services via LocalStack, or GCP BigQuery + Cloud SQL.

**Characteristics:** Heavy use of cloud-native services, sometimes with local emulators in docker-compose for development.

### Restructuring steps

**1. Classify each cloud service:**

| Service | Veris equivalent | Action |
|---|---|---|
| Azure OpenAI, OpenAI, Anthropic | LLM proxy (port 443) | Automatic interception, no config needed |
| Google Calendar API | Veris `google/calendar` service | Use the canonical service name and override the SDK endpoint/env vars as needed |
| Salesforce API | Veris `salesforce` service | Use the canonical service name and override the SDK endpoint/env vars as needed |
| Postgres (RDS, Cloud SQL, Neon) | Veris `postgres` service (5432) | Change `DATABASE_URL` to localhost |
| Azure Blob (via Azurite) | Bundle Azurite or MinIO | Lightweight, works in-container |
| Cosmos DB emulator | External endpoint | Too heavy (~2GB) to bundle |
| LocalStack (full) | Evaluate per-service | ~200MB. Bundle only if agent uses multiple AWS services |
| LocalStack (just S3) | Bundle MinIO instead | MinIO is lighter and S3-compatible |
| FHIR, BigQuery, Snowflake | External endpoint | No veris mock. User provides staging URL + credentials. |

**2. Cloud SDK endpoint overrides:**

Most cloud SDKs read endpoint URLs from environment variables. No code changes needed — just override the env vars:

```yaml
# veris.yaml
agent:
  environment:
    # Azure Blob → local Azurite
    AZURE_STORAGE_CONNECTION_STRING: "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=...;BlobEndpoint=http://localhost:10000/devstoreaccount1"

    # AWS → local LocalStack or MinIO
    AWS_ENDPOINT_URL: "http://localhost:4566"
    AWS_ACCESS_KEY_ID: "test"
    AWS_SECRET_ACCESS_KEY: "test"

    # GCP → emulator
    STORAGE_EMULATOR_HOST: "http://localhost:9023"
```

**3. LLM proxy — automatic interception:**

Veris intercepts calls to `api.openai.com`, `api.anthropic.com`, and Azure OpenAI endpoints via DNS aliasing + TLS termination. The agent's LLM calls are proxied transparently. No environment variable changes needed for LLM endpoints.

**4. Bundle lightweight emulators in Dockerfile.sandbox:**

```dockerfile
# Dockerfile.sandbox
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

# Install Azurite (Azure Blob emulator)
RUN npm install -g azurite

# Agent code
COPY requirements.txt /agent/
WORKDIR /agent
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src /agent/src/

WORKDIR /app
```

Start emulators in `start.sh`:

```bash
#!/bin/bash
# Start Azurite in background
azurite --silent --location /tmp/azurite --debug /tmp/azurite-debug.log &

# Start agent in foreground
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
```

**5. External endpoints for heavy/unmocked services:**

For services without a veris mock or lightweight emulator, the user must provide an external endpoint:

```yaml
# veris.yaml
agent:
  environment:
    COSMOS_DB_ENDPOINT: "https://staging-cosmos.documents.azure.com:443/"
    COSMOS_DB_KEY: "<user-provided-key>"
    BIGQUERY_PROJECT: "staging-project-id"
```

---

## Pattern 4: Serverless / No Docker (Vercel, Railway, Fly.io)

**Typical setup:** Next.js on Vercel + Neon Postgres + Upstash Redis + Pinecone. No Dockerfile exists.

**Characteristics:** Agent has never been containerized. Deployed to a PaaS. Uses managed/serverless databases.

### Restructuring steps

**1. Determine the runtime:**

| Framework | Runtime | Install in Dockerfile.sandbox? |
|---|---|---|
| FastAPI, Flask, Django | Python | No (already in base image) |
| Next.js, Express, Hono | Node.js | No (already in base image) |
| Go (Gin, Echo) | Go | Yes |
| Rust (Actix, Axum) | Rust | Yes |

**2. Install non-base runtimes:**

```dockerfile
# Dockerfile.sandbox — Node.js agent example
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

# Copy agent code and install dependencies
COPY package.json package-lock.json /agent/
WORKDIR /agent
RUN npm ci --production

COPY ./src /agent/src
COPY ./next.config.js /agent/
COPY ./tsconfig.json /agent/

# Build step (Next.js needs this)
RUN cd /agent && npm run build

# Prisma (if used)
COPY ./prisma /agent/prisma
RUN cd /agent && npx prisma generate

WORKDIR /app
```

**3. Map serverless databases to veris mocks:**

| Serverless DB | Veris replacement |
|---|---|
| Neon Postgres | Postgres mock. `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/${SIMULATION_ID}` |
| PlanetScale (MySQL) | No veris mock. Bundle MySQL or use external endpoint. |
| Upstash Redis | Bundle Redis. `REDIS_URL=redis://localhost:6379` |
| Pinecone, Weaviate | No veris mock. Use external endpoint. |
| Supabase | Postgres mock for the DB. Auth/storage need external endpoint. |

**4. Entry point:**

```yaml
# veris.yaml
agent:
  entry_point: npx next start -p 8080
  port: 8080
  code_path: /agent
```

For Python serverless frameworks (FastAPI on Railway):

```yaml
agent:
  entry_point: uvicorn app.main:app --host 0.0.0.0 --port 8080
  port: 8080
  code_path: /agent
```

Entry point paths are relative to code_path (entrypoint.sh cd's there first).

**5. Handle Vercel/Railway-specific config:**

- `vercel.json`: Ignore `cron`, `rewrites`, `regions`, `functions`. The agent runs as a standard server.
- `railway.toml` / `fly.toml`: Extract the `start_command` — that becomes your entry point.
- `Procfile` (Heroku/Railway): The `web:` line is the entry point.

**6. Environment variables:**

- `NEXT_PUBLIC_*` vars must be set at **build time** (in the Dockerfile RUN build step), not just at runtime.
- All other env vars go in `veris.yaml` agent.environment.
- Do NOT copy `.env.local` or `.env.production` into the container. Declare all needed vars explicitly in veris.yaml.

**7. API routes:**

Next.js API routes (`app/api/*/route.ts`) work as-is — they are standard HTTP endpoints when running `next start`. No special handling needed.

---

## Pattern 5: Multi-Agent System with Gateway

**Typical setup:** API gateway + flight-agent + hotel-agent + activity-agent + itinerary-agent + Kafka or NATS for inter-agent messaging.

**Characteristics:** Multiple separate agent services that coordinate to handle requests. A gateway routes to sub-agents.

### Restructuring steps

**1. Copy all agent code:**

```dockerfile
# Dockerfile.sandbox
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

# Install all dependencies from all sub-agents
COPY gateway/requirements.txt /tmp/gateway-req.txt
COPY flight-agent/requirements.txt /tmp/flight-req.txt
COPY hotel-agent/requirements.txt /tmp/hotel-req.txt
COPY itinerary-agent/requirements.txt /tmp/itinerary-req.txt
RUN pip install --no-cache-dir \
    -r /tmp/gateway-req.txt \
    -r /tmp/flight-req.txt \
    -r /tmp/hotel-req.txt \
    -r /tmp/itinerary-req.txt

# Copy each sub-agent
COPY ./gateway /agent/gateway/
COPY ./flight-agent /agent/flight-agent/
COPY ./hotel-agent /agent/hotel-agent/
COPY ./itinerary-agent /agent/itinerary-agent/

WORKDIR /app
```

If sub-agents share a `requirements.txt`, install it once. If they have conflicts, use separate virtualenvs (more complex — try to unify first).

**2. Determine the persona-facing port:**

The gateway is what the persona talks to. Its port goes in veris.yaml:

```yaml
agent:
  entry_point: bash start.sh
  port: 8080
  code_path: /agent
```

**3. Create start.sh with health-check waits:**

```bash
#!/bin/bash

# Start sub-agents in background
(cd /agent/flight-agent && uvicorn main:app --host 0.0.0.0 --port 8081) &
(cd /agent/hotel-agent && uvicorn main:app --host 0.0.0.0 --port 8082) &
(cd /agent/itinerary-agent && uvicorn main:app --host 0.0.0.0 --port 8083) &

# Wait for sub-agents to be ready
for port in 8081 8082 8083; do
  echo "Waiting for service on port $port..."
  until curl -sf http://localhost:$port/health > /dev/null 2>&1; do sleep 1; done
  echo "Service on port $port is ready."
done

# Start gateway in foreground
cd /agent/gateway
exec uvicorn main:app --host 0.0.0.0 --port 8080
```

Veris already launches `start.sh` from `agent.code_path`. If you need to start background work from a subdirectory, use an explicit absolute-path subshell like `(cd /agent/flight-agent && ...) &`. If the foreground process lives in a subdirectory, `cd` there immediately before the final `exec`.

**4. Override inter-agent communication URLs:**

Docker compose hostnames become localhost:

```yaml
# veris.yaml
agent:
  environment:
    FLIGHT_AGENT_URL: "http://localhost:8081"
    HOTEL_AGENT_URL: "http://localhost:8082"
    ITINERARY_AGENT_URL: "http://localhost:8083"
```

**5. Handle message queues (Kafka, NATS, RabbitMQ):**

This is the biggest decision for multi-agent systems:

| Option | When to use |
|---|---|
| **Bundle Kafka** | Only if event streaming is core to agent logic (e.g., agents react to event streams, not just request-response). Very heavy (~500MB+ with Zookeeper). |
| **Bundle RabbitMQ** | If message routing/acknowledgment matters. Lighter than Kafka (~150MB). |
| **Bundle Redis pub/sub** | If the queue is just for async task dispatch. Lightest option. |
| **External endpoint** | If bundling is too heavy. User provides a managed Kafka/NATS URL and points the agent at it via env var. |

If bundling Kafka, add to start.sh:

```bash
# Start Zookeeper and Kafka
/opt/kafka/bin/zookeeper-server-start.sh -daemon /opt/kafka/config/zookeeper.properties
sleep 3
/opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties
sleep 3

# Create required topics
/opt/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic agent-events --partitions 1 --replication-factor 1 2>/dev/null || true
```

**6. gRPC between agents:**

gRPC works on localhost. Just update the target addresses:

```yaml
agent:
  environment:
    FLIGHT_AGENT_GRPC: "localhost:50051"
    HOTEL_AGENT_GRPC: "localhost:50052"
```

---

## Pattern 6: Hybrid Frontend + Backend Workers

**Typical setup:** Next.js frontend + Python workers (content generator, image processor, scheduler) + RabbitMQ or Redis queue.

**Characteristics:** Mixed-language stack. Frontend handles user interaction; backend workers process tasks from a queue.

### Restructuring steps

**1. Identify the persona-facing process:**

The persona interacts with the frontend (HTTP chat endpoint). The frontend port goes in veris.yaml.

**2. Install both runtimes:**

```dockerfile
# Dockerfile.sandbox
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

# Install RabbitMQ (if needed as message broker)
RUN apt-get update && apt-get install -y rabbitmq-server && rm -rf /var/lib/apt/lists/*

# Copy and install frontend
COPY frontend/package.json frontend/package-lock.json /agent/frontend/
RUN cd /agent/frontend && npm ci && npm run build

COPY ./frontend /agent/frontend/

# Copy backend workers
COPY backend/requirements.txt /agent/backend/requirements.txt
RUN pip install --no-cache-dir -r /agent/backend/requirements.txt

COPY ./backend /agent/backend/

WORKDIR /app
```

**3. Create start.sh:**

```bash
#!/bin/bash

# Start message broker
rabbitmq-server -detached
until rabbitmqctl status > /dev/null 2>&1; do sleep 1; done
echo "RabbitMQ is ready."

# Start Python workers in background
(cd /agent/backend/content-worker && python main.py) &
(cd /agent/backend/image-processor && python main.py) &

# Start frontend in foreground
cd /agent/frontend
exec npx next start -p 8080
```

**4. veris.yaml:**

```yaml
agent:
  entry_point: bash start.sh
  port: 8080
  code_path: /agent
```

**5. Queue alternatives:**

If the original stack uses RabbitMQ, it can be bundled (~150MB). For lighter alternatives:

| Original | Lighter alternative | Trade-off |
|---|---|---|
| RabbitMQ | Redis with `rq` or `celery[redis]` | Simpler, less robust routing |
| Kafka | Redis Streams | Only works for simple pub/sub patterns |
| SQS (AWS) | Use real SQS via outbound egress, or keep SQS external with a managed endpoint | Don't patch the agent to swap SDKs — that diverges from how it runs in prod |

**6. Skip monitoring and observability:**

- Prometheus + Grafana: skip unless agent code queries the Prometheus metrics API at runtime.
- Jaeger/Zipkin tracing: skip. Tracing is for debugging, not simulation.
- ELK stack: skip. Logs go to stdout in the container.

**7. Shared state between frontend and workers:**

If frontend and workers share state via Redis or a database, ensure both point to the same instance:

```yaml
agent:
  environment:
    REDIS_URL: "redis://localhost:6379"
    DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/${SIMULATION_ID}"
    RABBITMQ_URL: "amqp://guest:guest@localhost:5672/"
```

---

## Pattern 7: Custom / Doesn't Match Above

When the agent architecture doesn't fit any of the patterns above, use this decision framework.

### Questions to ask the user

1. **Which process handles user/persona interaction?** This is the HTTP endpoint where a user sends a chat message. It becomes the entry point and its port goes in veris.yaml.
2. **What happens when a user sends a message?** Trace the full request path: API server -> queue -> worker -> database -> response. Every service on this path must run in the container.
3. **Which services are on the critical path for responding?** If the agent can't respond without a service, it must be bundled or connected externally.
4. **Are there background processes that MUST run during simulation?** Pollers, schedulers, webhook listeners that trigger agent behavior.

### Decision framework for each dependency

```
Is it a database?
  ├── Postgres → Use veris postgres mock (port 5432)
  ├── SQLite → Works as-is (file-based)
  ├── MongoDB → Bundle (apt-get install -y mongod) or external
  └── Other → Bundle if lightweight, external if heavy

Is it a message queue?
  ├── Redis → Bundle (lightweight, ~50MB)
  ├── RabbitMQ → Bundle (~150MB) or replace with Redis
  ├── Kafka → External endpoint or replace with Redis Streams
  └── NATS → Bundle (single binary, very lightweight)

Is it an API the agent calls?
  ├── OpenAI/Anthropic/Azure OpenAI → Automatic (Veris LLM proxy)
  ├── Google Calendar → Use Veris `google/calendar` when it maps cleanly
  ├── Salesforce → Use Veris `salesforce` when it maps cleanly
  ├── Stripe → Use Veris `stripe` when it maps cleanly
  ├── Jira → Use Veris `jira` when it maps cleanly
  └── Other → External endpoint (user provides URL + credentials)

Is it a runtime/language?
  ├── Python → Already in base image
  ├── Node.js → Already in base image
  ├── Go → Install or compile binary in Dockerfile.sandbox
  └── Other → Install in Dockerfile.sandbox

Is it infrastructure tooling?
  ├── nginx → Skip (veris has its own)
  ├── Monitoring (Prometheus, Grafana) → Skip
  ├── Log shipping (fluent-bit, fluentd) → Skip
  ├── Service mesh (Envoy, Istio) → Skip
  └── Health check sidecar → Skip
```

### General principles

- The entry point process runs in **foreground** (with `exec` in start.sh).
- Supporting processes run in **background** (with `&` in start.sh).
- All inter-process communication uses **localhost**.
- Agent port = the port the persona sends requests to.
- When in doubt, start minimal and add services only when the agent fails without them.

---

## Pattern 8: Platform-Hosted Agent (Framework-as-Runtime)

**Typical setup:** The repo contains configuration files, prompt templates, and tool definitions but not a standalone application. The agent runs on an installed framework CLI or server: LangServe, CrewAI, AutoGen, Dify, n8n, Flowise, or similar.

**Characteristics:** No `main.py` / `index.js` / application entrypoint. The "source code" is YAML/JSON config, prompt files, and possibly a few small Python/JS files that define tools or hooks. The framework is the runtime.

### How to identify

- The repo has no traditional app entrypoint (`app.py`, `main.py`, `server.js`, `index.ts`)
- The primary files are configuration: `crew.yaml`, `agents.yaml`, `flows.json`, `docker-compose.yml` that just runs a framework image
- `pyproject.toml` or `package.json` lists the framework as a dependency but there is no substantial application code
- The README says "install [framework], then run [framework CLI command]"

### Restructuring steps

**1. Install the framework in the Dockerfile:**

The framework is installed from a package manager, not built from source:

```dockerfile
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

# Install the framework
RUN pip install crewai    # or: npm install -g langserve, etc.

# Copy config and tool definitions
COPY . /agent/

WORKDIR /app
```

If the repo has a `pyproject.toml` or `requirements.txt` that lists the framework plus tool dependencies, install from that:

```dockerfile
COPY requirements.txt /agent/
WORKDIR /agent
RUN pip install --no-cache-dir -r requirements.txt

COPY . /agent/
WORKDIR /app
```

**2. Determine the entry point:**

The entry point is the framework's CLI or server command:

```yaml
# veris.yaml
agent:
  entry_point: crewai run         # or: langserve start, etc.
  port: 8080
  code_path: /agent
```

Check the framework's docs or the repo's README for the canonical start command. Common patterns:
- CrewAI: `crewai run` or `python -m crewai run`
- LangServe: `langchain serve --port 8080`
- Dify: container with built-in server
- n8n: `n8n start`

**3. Determine the channel interface:**

Most frameworks expose an HTTP API. Check the framework's docs for:
- The chat/invoke endpoint path
- The request/response JSON shape
- Whether it streams (SSE) or returns a complete response

If the framework does not expose a network API and instead runs as a one-shot CLI, this is a platform gap, not a wrapper opportunity. Surface it to the user — the agent's production deployment model probably involves something driving that CLI (cron, a job runner, a shell script), and we want the simulation to drive it the same way, not via a Python adapter that fakes a callable. Do not create a wrapper Python file to paper over this.

**4. Handle framework-specific config:**

- Environment variables the framework reads (API keys, model names, etc.)
- Config file paths the framework expects (may need to be at a specific location)
- Tool/plugin registrations that reference local files

**5. Watch for source-tree compile errors:**

Platform-hosted repos sometimes have Python files with syntax errors or import failures because the developer only ever ran them through the framework (which may not import all files). If `pip install -e .` or the build fails due to bad source files, install the framework and config from published packages and `COPY` only the config files — do not install the repo as an editable package.

---

## Pattern 9: Transport bridge

**Typical setup:** The agent framework's native transport doesn't match what the actor channel speaks on the wire. The most common case is voice agents whose framework uses WebRTC end-to-end (LiveKit Agents, Daily, anything SFU-based) but where the Veris actor expects raw PCM16 over a WebSocket (the [`voice_ws`](voice-channels.md) channel). It also covers agents wired to SIP/Twilio media streams, agents that speak a custom binary protocol, and any case where the framework's transport layer is fixed and not negotiable.

**Characteristics:** The agent ships, in production, against a transport you cannot bypass. Pointing the actor at the agent directly produces a protocol mismatch — the actor sends bytes the framework can't decode, or vice versa. The right answer is **not** to rewrite the agent's transport layer; it's to run a small bridge process inside the sandbox container that translates between the actor's channel format and whatever the framework already speaks.

### How to identify

- The agent uses a framework with a fixed media transport (WebRTC SFU, SIP media, etc.) that doesn't downgrade to raw audio over WS.
- The actor channel you need is `voice_ws` (or any channel whose wire format the framework can't speak directly).
- The framework's published transport plugins don't include one for the actor's channel format. For voice agents specifically, the quick check is: *can the framework serve a raw PCM16 WebSocket?* If yes (Pipecat with `RawAudioFrameSerializer`, most in-house frameworks), use that transport and skip this pattern — you don't need a bridge. If no (LiveKit Agents, Daily SDK, anything WebRTC-only), continue with this pattern.

### Architecture

```
┌─────────────────┐   actor channel    ┌────────────────────────┐
│  Veris actor    │ ──── voice_ws ───▶ │  bridge process        │
│  (in sandbox)   │ ◀── PCM16 frames ─ │  (in sandbox container)│
└─────────────────┘                    └───────────┬────────────┘
                                                   │
                                       framework's native transport
                                       (WebRTC room / SIP media /
                                        custom envelope / etc.)
                                                   │
                                                   ▼
                                       ┌────────────────────────┐
                                       │  agent framework       │
                                       │  + your agent code     │
                                       │  (in sandbox container)│
                                       └────────────────────────┘
```

The bridge is the thin middle layer. It:

1. Accepts the actor's channel connection (a WebSocket on the port `veris.yaml` advertises).
2. Stands up the framework's native transport on the same host — for a WebRTC framework, that means joining a LiveKit room as a participant; for SIP, opening a media socket; for a custom envelope, opening the framework's WS and wrapping/unwrapping its envelope.
3. Pumps audio (or other media) in both directions, with whatever framing translation the wire formats require.

The agent code itself doesn't change. It participates in the framework's transport exactly the way it does in production — same room, same SDK, same tools, same prompt. The bridge is purely a sandbox-edge translator.

### Restructuring steps

**1. Identify the framework's native transport.** What does the agent actually speak when deployed for real? Browser-to-LiveKit-room? SIP trunk? A proprietary WSS with a specific envelope? That's the transport the bridge has to terminate.

**2. Decide what runs in the sandbox container.** For an in-container WebRTC bridge you typically need three peer processes:

| Process | Purpose |
|---|---|
| Framework's media server (e.g., `livekit-server --dev`) | Provides the rooms the agent and bridge will both join. Single binary, in-container. |
| Agent worker | The framework SDK auto-dispatches into every new room. Talks to LLM, runs tools, etc. |
| Bridge | FastAPI (or equivalent) listening on the actor's port. For each connection: join a fresh room as a participant, pump frames. |

For a SIP-style bridge it's typically two processes (the SIP stack and the agent), but the shape is the same — one in-container service plus a small translation layer.

**3. Write the bridge as a normal piece of the repo, not in `.veris/`.** Treat it as production code. If a future product surface needs to call the same agent over a raw WS (mobile app, kiosk, IVR vendor), the bridge ships with that product too — it's not Veris-specific. Put it next to the agent (`app/bridge.py` or similar), exercise it in your own tests, and keep `.veris/` as pure config plus the multi-process `start.sh` ([template 4](../templates/start-sh.md#template-4-peer-processes-with-fail-fast)).

**4. Wire the entry point.** The bridge listens on the port that `veris.yaml` advertises as `agent.port`. The agent worker and the framework's media server run as background siblings in `start.sh`:

```bash
#!/bin/bash
# .veris/start.sh — three peer processes with fail-fast
# Intentionally no `set -e` here — see Template 4 for the rationale.

wait_for_port() {  # poll a TCP port until it accepts, or give up
  local host="$1" port="$2"
  for _ in $(seq 1 100); do
    (exec 3<>"/dev/tcp/${host}/${port}") 2>/dev/null && { exec 3>&- 3<&-; return 0; }
    sleep 0.2
  done
  return 1
}

# 1. Framework's media server — wait until it actually accepts before continuing.
/usr/local/bin/livekit-server --dev --bind 0.0.0.0 &
LK_PID=$!
wait_for_port localhost 7880 || { echo "livekit-server never came up" >&2; exit 1; }

# 2. Agent worker. It registers with the SFU *asynchronously*; capture its log
#    so we can gate on real registration, and mirror it to stdout for agent.log.
uv run --no-sync python -m app.agent start > /tmp/worker.log 2>&1 &
AG_PID=$!
tail -f /tmp/worker.log & TAIL_PID=$!

# 3. GATE the bridge on the worker registering — NOT a fixed sleep. Auto-dispatch
#    only fires for rooms created *after* the worker registers; under load that
#    can take 10s+. Accept a caller too early and the agent never joins the room
#    (the actor sees callee_no_answer). See "LiveKit dispatch gotchas" below.
for _ in $(seq 1 120); do
  grep -q "registered worker" /tmp/worker.log 2>/dev/null && break
  kill -0 "$AG_PID" 2>/dev/null || break
  sleep 0.5
done

# 4. Bridge — listens on the actor's port.
uv run --no-sync uvicorn app.bridge:app --host 0.0.0.0 --port "${PORT:-8080}" &
BR_PID=$!

cleanup() { kill "$LK_PID" "$AG_PID" "$BR_PID" "$TAIL_PID" 2>/dev/null || true; }
trap 'cleanup; exit 143' TERM INT

# Fail-fast: when any peer dies, take down the rest so Veris restarts cleanly.
wait -n
status=$?
cleanup
wait || true
exit "$status"
```

See [start-sh.md Template 4](../templates/start-sh.md#template-4-peer-processes-with-fail-fast) for the rationale around `wait -n` and why this shape avoids `set -e`.

**5. Pull the framework's binary into the image.** For LiveKit, the cleanest path is a multi-stage Dockerfile that copies the prebuilt static binary from the official image:

```dockerfile
ARG GVISOR_BASE
FROM livekit/livekit-server:latest AS lk-stage
FROM ${GVISOR_BASE}

# Framework media server (Go static binary — works on the gVisor base).
COPY --from=lk-stage /livekit-server /usr/local/bin/livekit-server

# Normal agent install
COPY pyproject.toml /agent/
WORKDIR /agent
RUN uv sync --no-dev

COPY app /agent/app
COPY .veris/start.sh /agent/start.sh
RUN chmod +x /agent/start.sh

WORKDIR /app
```

For SIP or other media stacks, install the daemon from the distribution's package manager in the same `Dockerfile.sandbox` and skip the multi-stage copy.

### Worked example: LiveKit Agents over `voice_ws`

For a LiveKit-based voice agent driven through Veris's `voice_ws` actor:

- The framework's media server is `livekit/livekit-server` in dev mode (`devkey`/`secret`). Self-contained, no external LiveKit Cloud account needed.
- The agent worker uses `livekit-agents` with whatever realtime LLM you want — `openai.realtime.RealtimeModel`, `google.realtime.RealtimeModel`, `aws.realtime.RealtimeModel.with_nova_sonic_2`, or a chained STT/LLM/TTS pipeline. The worker is identical to the production worker; no Veris-specific code path.
- The bridge accepts the `voice_ws` connection, mints a LiveKit access token (using `livekit-api` and the in-container dev creds), joins a fresh room as a participant called `veris-actor`, publishes incoming PCM16 frames via `rtc.AudioSource.capture_frame(AudioFrame(...))`, and subscribes to the agent's audio track via `rtc.AudioStream(track, sample_rate=24000, num_channels=1)`, writing each frame back out as `ws.send_bytes(bytes(frame.data))`.

The agent code (its `Agent` subclass, `@function_tool()` methods, prompt, DB-backed tool dispatch) is untouched. In production it joins a room driven by a browser client or SIP gateway; in Veris it joins a room driven by the bridge. Same agent, same surface.

### LiveKit dispatch gotchas

LiveKit Agents' worker/auto-dispatch model has two failure modes a plain WS server doesn't, and both surface identically: the actor connects, nobody answers, and the sim ends in `callee_no_answer`. They only bite under concurrent cluster load — a single local smoke test passes and the problem appears at scale. Both fixes live in the agent's own code; neither needs a `veris-sandbox` change.

**1. Gate the bridge on worker registration — never a fixed `sleep`.** The worker registers with the SFU *asynchronously*, and the SFU only auto-dispatches into rooms created *after* registration. The bridge creates a room the instant the actor opens `/voice`; if that happens first, the worker is never dispatched into the room and the actor hears silence. A fixed `sleep 5` races — under load registration can take 10s+. Gate on the real signal: tail the worker log and wait for the `registered worker` line (with a ceiling, ~60s) before the bridge starts accepting calls. This is the gate in the `start.sh` above — it replaces the naive `sleep 1` that works locally and fails under load.

**2. Disable the worker's CPU self-throttle.** A `start` (prod-mode) `AgentServer` ships a CPU-based load function with a 0.7 threshold and *refuses dispatch* when the host is busy — the SFU then reports "no workers with sufficient capacity" and, again, the agent never joins. In the sandbox the SFU, worker, bridge, and the realtime session all share one CPU-bound pod, so under concurrent load that threshold trips constantly. This worker handles exactly one call per pod and must never refuse, so pin load to zero:

```python
from livekit.agents import AgentServer

# Never self-throttle: one call per pod, must always accept dispatch.
server = AgentServer(load_fnc=lambda *_: 0.0)
```

(dev mode already defaults the threshold to infinity for this reason; a prod-mode `start` worker does not.)

Symptom for both: intermittent `callee_no_answer` that worsens with concurrency. If a handful of parallel sims pass but a larger batch shows ~half failing to connect, suspect these before anything in the bridge or the audio path. See [troubleshooting.md](../phases/troubleshooting.md#voice-agent-never-answers-under-load-callee_no_answer).

### Hosted-runtime variant: Vapi (outbound bridge, inbound webhook)

When the framework is a hosted cloud runtime rather than an in-container stack, the bridge shape inverts. A Vapi agent needs **no media server and no worker process** — the agent process itself serves `voice_ws` and, per call, creates a Vapi call over the API and opens an outbound WSS to Vapi's cloud, pumping PCM16 both ways. One process in the container; no `start.sh` choreography.

What Vapi adds instead is an **inbound** requirement: tools are delivered as HTTP `tool-calls` webhooks from Vapi's cloud to a public `server.url`, so the pod must be publicly reachable. The two ways to provide that — an in-pod ngrok tunnel (with a hard free-tier concurrency limit: one agent session per authtoken) or a stable shared `PUBLIC_BASE_URL` endpoint — plus Vapi's silent string-result trap are covered in [voice-channels.md → Vapi](voice-channels.md#vapi-hosted-runtime-server-tool-webhooks).

### When *not* to use this pattern

- The framework can already serve the actor's channel directly. Most notably: **Pipecat** can serve `voice_ws` natively by configuring `WebsocketServerTransport` with a `RawAudioFrameSerializer` instead of the default `ProtobufFrameSerializer`. If your framework has a transport plugin that emits/consumes bare PCM16 over WS, configure it and skip the bridge entirely — you keep one process in the container instead of three, and the failure modes are correspondingly simpler. (Pipecat's WS transports have one well-defined failure mode of their own — they don't honor `audio_out_auto_silence` — so you still need a small silence-tail processor on the pipeline; see [voice-channels.md](voice-channels.md#pipecat-ws-transports-need-explicit-end-of-turn-silence) for the recipe.)
- The actor channel matches the framework's production transport. If the agent is a plain HTTP chat API and Veris is driving it over the `http` channel, you're in Pattern 1, not 9. The bridge pattern only applies when the actor channel's wire format and the framework's transport differ.
- You're tempted to "translate" semantic content (rewriting messages, adapting tool calls). That's a wrapper, not a bridge. A bridge translates *transport*, not behavior — the agent gets the same audio bytes it would get in production, just delivered via a different network path. If you find yourself reshaping tool-call JSON or normalizing speech-to-text output, stop; that's exactly the "no wrappers, no shims" rule from [SKILL.md](../SKILL.md).

### Cost

Adding a media-server peer process is real container weight — `livekit-server` is ~67 MB on disk, runs Go's network stack on top of gVisor, and binds a WebSocket plus a UDP/TCP RTC port internally. On a constrained sandbox, that's noticeable. The tradeoff is testing the agent against its production transport exactly as shipped. If the framework's transport can be swapped for a `voice_ws`-compatible one without lying about what production looks like (Pipecat's serializer config is the clean example), prefer that.

---

## Common Rules Across All Patterns

These apply regardless of which pattern the agent matches.

### File placement (inside the container at runtime)

| What | Where | How it gets there |
|---|---|---|
| Agent code | `/agent/` | COPY'd by Dockerfile.sandbox. Matches `code_path: /agent` in veris.yaml |
| veris.yaml | `/config/veris.yaml` | Mounted by CLI at runtime (`-v .veris/veris.yaml:/config/veris.yaml:ro`). Do NOT COPY it. |
| start.sh (if needed) | `/agent/start.sh` | COPY'd by Dockerfile.sandbox. Referenced as `entry_point: bash start.sh` (relative to code_path) |

### Dockerfile.sandbox requirements

Every `Dockerfile.sandbox` must end with:

```dockerfile
WORKDIR /app
```

This is a veris requirement. The entrypoint.sh expects this working directory.

### Port conflicts

Agent ports must NOT conflict with Veris service ports:

| Port range | Used by |
|---|---|
| 443 | Veris nginx (TLS termination, DNS interception) |
| 5432 | Veris Postgres service (native TCP) |
| 6100-6199 | Veris infrastructure services |
| 6200-6299 | Veris mock/application services |

**Safe agent ports:** 8080, 3000, 3001, 4000, 5000, 8008, 9000.

### Hostname translation

Docker compose service names become localhost. Common translations:

```yaml
# docker-compose hostnames → veris environment
postgres:5432     → localhost:5432
redis:6379        → localhost:6379
rabbitmq:5672     → localhost:5672
elasticsearch:9200 → localhost:9200
kafka:9092        → localhost:9092
api-gateway:8080  → localhost:8080
```

### start.sh template

When the agent needs multiple processes:

```bash
#!/bin/bash
set -e

# ---- Background services ----
# Start each supporting process and wait for readiness

some-service --daemon &
until some-health-check; do sleep 1; done

# ---- Background workers ----
(cd /agent/worker && python main.py) &

# ---- Foreground: main agent process ----
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Rules for start.sh:
- Use `exec` for the final (foreground) process so it receives signals correctly.
- Use `&` for background processes.
- Add health-check waits (`until curl ...`) before starting processes that depend on background services.
- Use `set -e` so the script fails fast if a critical setup step fails.
