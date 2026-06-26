---
name: Redis Manager
slug: redis-manager
version: 1.1.0
description: "Manage a shared Redis Docker container for local dev environments. Handles container lifecycle, key inspection, and selective data flush. Joins the shared Docker network created by proxy-manager."
changelog: "v1.1.0: Fix flush-db to use single redis-cli -n connection (was flushing wrong DB), validate DB number input, warn on default password, bind host port to 127.0.0.1, pin image to redis:7.4-alpine."
triggers:
  - "start redis"
  - "stop redis"
  - "redis status"
  - "flush redis"
  - "limpar redis"
  - "redis keys"
  - "redis-manager"
metadata: {"clawdbot":{"emoji":"🔴","requires":{"bins":["docker"]},"os":["linux","darwin"]}}
---

# Redis Manager

Manages the shared Redis Docker container for local dev environments.

## Architecture

```
redis-manager/
├── docker-compose.yml   # Redis 7 Alpine container
└── run.sh               # lifecycle + data inspection CLI
```

Joins the shared `nginx-proxy_net` network (created by proxy-manager) so all app containers can connect via hostname `codai_redis`. Data is persisted in a named volume.

## Commands

```bash
./run.sh start                # start Redis container
./run.sh stop                 # stop container (data persists in volume)
./run.sh status               # status + key count + memory usage
./run.sh wait                 # block until Redis responds PONG
./run.sh flush                # FLUSHALL — clear all data (interactive confirm)
./run.sh flush-db <n>         # FLUSHDB on database N (interactive confirm)
./run.sh list-keys [<pattern>]# KEYS <pattern> (default: *)
./run.sh cli                  # open redis-cli interactive session
```

## How to Execute Tasks

### Start Redis
```bash
cd redis-manager && ./run.sh start
```

### Check status and memory usage
```bash
./run.sh status
```

### Inspect keys for a specific instance
```bash
./run.sh list-keys "session:*"
./run.sh list-keys "cache:feature*"
```

### Flush session data for testing
```bash
./run.sh flush-db 0    # flush default db only
```

## Startup Order

1. `proxy-manager start` — creates the shared Docker network
2. `mysql-manager start` (or `postgres-manager start`)
3. `redis-manager start`

## Configuration

| Variable          | Default       | Purpose                          |
|-------------------|---------------|----------------------------------|
| `REDIS_CONTAINER` | `codai_redis` | Container name                   |
| `REDIS_PASSWORD`  | `redispass`   | Redis AUTH password              |
| `REDIS_PORT`      | `6380`        | Host port (maps to 6379)         |
| `REDIS_MAXMEMORY` | `256mb`       | Max memory before eviction       |
| `CODAI_NETWORK`   | `nginx-proxy_net` | Shared Docker network name   |

## App Connection

Backend containers connect to Redis at:
- **Host**: `codai_redis` (container name on shared network)
- **Port**: `6379`
- **Password**: `redispass` (or `REDIS_PASSWORD`)

## Rules

- `flush` always prompts for confirmation — it deletes all data in all databases.
- `flush-db <n>` flushes exactly database N using a single `-n` connection; confirm text always matches the database being flushed.
- `stop` preserves data in the Docker volume. Use `docker compose down -v` only when you intentionally want to delete persisted data.
- The container uses `restart: unless-stopped` — it will resume after a Docker daemon restart. Run `./run.sh stop` when done.
- The host port (`REDIS_PORT`) is bound to `127.0.0.1` only. Set a non-default `REDIS_PASSWORD` on shared machines.
- Redis connects to the `nginx-proxy_net` network as `external: true` — proxy-manager must start first.

## Related Plugins

- `proxy-manager` — creates the shared Docker network (start first)
- `mysql-manager` — relational DB companion
- `postgres-manager` — relational DB companion
- `worktree-manager` — app instances that consume Redis
