---
name: redis-commander
slug: redis-commander
version: 1.0.0
description: "Manage the Redis Commander Docker container for local dev environments. Provides a web UI for Redis key inspection at http://localhost:8083. Requires redis-manager and proxy-manager to be running first."
changelog: Initial release.
triggers:
  - "abrir redis commander"
  - "start redis commander"
  - "stop redis commander"
  - "redis commander status"
  - "interface redis"
  - "admin redis"
  - "redis-commander"
metadata: {"clawdbot":{"emoji":"🔴","requires":{"bins":["docker"]},"os":["linux","darwin"]}}
---

# Redis Commander

Manages the Redis Commander Docker container, providing a web UI for Redis key inspection and management.

## Architecture

```
redis-commander/
├── docker-compose.yml   # Redis Commander container
└── run.sh               # lifecycle CLI
```

Connects to the shared `nginx-proxy_net` network and reaches Redis at `codai_redis:6379`. Access is protected by HTTP Basic Auth. No data is persisted — Redis Commander is stateless.

## Commands

```bash
./run.sh start    # start Redis Commander container
./run.sh stop     # stop container
./run.sh status   # show status and URL
./run.sh open     # print access URL
```

## How to Execute Tasks

### Start Redis Commander

Check your session context for the absolute script path, then run:
```bash
<plugin-root>/redis-commander/run.sh start
```
Open `http://localhost:8083` in a browser. Login: `admin` / `admin` (HTTP Basic Auth).

### Check status
```bash
<plugin-root>/redis-commander/run.sh status
```

## Prerequisites

Start in this order:
1. `proxy-manager start` — creates the shared Docker network
2. `redis-manager start` — Redis must be running before Redis Commander connects

## Configuration

| Variable               | Default                   | Purpose                        |
|------------------------|---------------------------|--------------------------------|
| `COMMANDER_CONTAINER`  | `codai_redis_commander`   | Container name                 |
| `COMMANDER_PORT`       | `8083`                    | Host port                      |
| `COMMANDER_USER`       | `admin`                   | HTTP Basic Auth user           |
| `COMMANDER_PASSWORD`   | `admin`                   | HTTP Basic Auth password       |
| `REDIS_CONTAINER`      | `codai_redis`             | Redis hostname on shared net   |
| `REDIS_PASSWORD`       | `redispass`               | Redis AUTH password            |
| `CODAI_NETWORK`        | `nginx-proxy_net`         | Shared Docker network name     |

## Rules

- Start `redis-manager` before this plugin — Redis Commander cannot connect without Redis.
- Port `8083` is bound to `127.0.0.1` — accessible from the host only.
- Change `COMMANDER_PASSWORD` on shared machines (default `admin` is not secure).
- Use `stop` when done; the container uses `restart: unless-stopped` and survives reboots.

## Related Plugins

- `proxy-manager` — creates the shared Docker network (start first)
- `redis-manager` — Redis container that Redis Commander connects to
