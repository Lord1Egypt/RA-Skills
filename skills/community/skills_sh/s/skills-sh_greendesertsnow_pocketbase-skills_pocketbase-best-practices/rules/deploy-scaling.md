---
title: Tune OS and Runtime for PocketBase Scale
impact: MEDIUM
impactDescription: Prevents file descriptor exhaustion, OOM kills, and exposes secure config for production deployments
tags: production, scaling, ulimit, gomemlimit, docker, encryption, deployment
---

## Tune OS and Runtime for PocketBase Scale

Three low-effort OS/runtime knobs have outsized impact on production stability: open-file limits for realtime connections, Go memory limits for constrained hosts, and settings encryption for shared or externally-backed infrastructure. None of these are set automatically.

**Incorrect (default OS limits, no memory governor, plain-text settings):**

```bash
# Start without raising the file descriptor limit
/root/pb/pocketbase serve yourdomain.com
# → "Too many open files" once concurrent realtime connections exceed ~1024

# Start in a container that has a 512 MB RAM cap without GOMEMLIMIT
docker run -m 512m pocketbase serve ...
# → OOM kill during large file upload because Go GC doesn't respect cgroup limits

# Store SMTP password and S3 secret as plain JSON in pb_data/data.db
pocketbase serve  # no --encryptionEnv
# → Anyone who obtains the database backup can read all credentials
```

**Correct:**

```bash
# 1. Raise the open-file limit before starting (Linux/macOS)
#    Check current limit first:
ulimit -a | grep "open files"
#    Temporarily raise to 4096 for the current session:
ulimit -n 4096
/root/pb/pocketbase serve yourdomain.com

#    Or persist it via systemd (recommended for production):
# /lib/systemd/system/pocketbase.service
# [Service]
# LimitNOFILE = 4096
# ...

# 2. Cap Go's soft memory target on memory-constrained hosts
#    (instructs the GC to be more aggressive before the kernel OOM-kills the process)
GOMEMLIMIT=512MiB /root/pb/pocketbase serve yourdomain.com

# 3. Encrypt application settings at rest
#    Generate a random 32-character key once:
export PB_ENCRYPTION_KEY="z76NX9WWiB05UmQGxw367B6zM39T11fF"
#    Start with the env-var name (not the value) as the flag argument:
pocketbase serve --encryptionEnv=PB_ENCRYPTION_KEY
```

**Docker deployment pattern (v0.36.8):**

```dockerfile
FROM alpine:latest
ARG PB_VERSION=0.36.8

RUN apk add --no-cache unzip ca-certificates

ADD https://github.com/pocketbase/pocketbase/releases/download/v${PB_VERSION}/pocketbase_${PB_VERSION}_linux_amd64.zip /tmp/pb.zip
RUN unzip /tmp/pb.zip -d /pb/

# Uncomment to bundle pre-written migrations or hooks:
# COPY ./pb_migrations /pb/pb_migrations
# COPY ./pb_hooks      /pb/pb_hooks

EXPOSE 8080

# Mount a volume at /pb/pb_data to persist data across container restarts
CMD ["/pb/pocketbase", "serve", "--http=0.0.0.0:8080"]
```

```yaml
# docker-compose.yml
services:
  pocketbase:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - pb_data:/pb/pb_data
    environment:
      GOMEMLIMIT: "512MiB"
      PB_ENCRYPTION_KEY: "${PB_ENCRYPTION_KEY}"
    command: ["/pb/pocketbase", "serve", "--http=0.0.0.0:8080", "--encryptionEnv=PB_ENCRYPTION_KEY"]
volumes:
  pb_data:
```

**Quick-reference checklist:**

| Concern | Fix |
|---------|-----|
| `Too many open files` errors | `ulimit -n 4096` (or `LimitNOFILE=4096` in systemd) |
| OOM kill on constrained host | `GOMEMLIMIT=512MiB` env var |
| Credentials visible in DB backup | `--encryptionEnv=YOUR_VAR` with a 32-char random key |
| Persistent data in Docker | Mount volume at `/pb/pb_data` |

Reference: [Going to production](https://pocketbase.io/docs/going-to-production/)
