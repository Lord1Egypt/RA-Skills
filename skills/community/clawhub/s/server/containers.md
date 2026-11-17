# Running Services From Containers on One Box

Compose as an operating pattern for a single machine: several stacks, one shared proxy, restart policies that survive a reboot. Image building, Dockerfile authoring, and runtime internals belong to the `docker` skill; orchestration across machines to `k8s`.

**Before adding a stack**, read `## Services` in `~/Clawic/data/server/memory.md` (or `services.md` if `## Boxes` points there) for the ports already taken and the proxy network in use. Two stacks each shipping their own proxy on port 80 is the most common self-inflicted outage on a container box.

**Contents:** [One Stack Per App](#one-stack-per-app) · [The Shared Proxy Network](#the-shared-proxy-network) · [A Complete Stack](#a-complete-stack) · [Restart Policies](#restart-policies) · [Publishing Ports Safely](#publishing-ports-safely) · [Volumes and Permissions](#volumes-and-permissions) · [Depends On Is Not Ready](#depends-on-is-not-ready) · [Resource Limits](#resource-limits) · [Logging](#logging) · [Updating Images](#updating-images) · [Reaching the Host, and the Host Reaching In](#reaching-the-host-and-the-host-reaching-in) · [Compose vs systemd Units](#compose-vs-systemd-units) · [Disk Reclamation](#disk-reclamation) · [Write It Down](#write-it-down)

## One Stack Per App

`/srv/<app>/docker-compose.yml`, one directory per application, each with its own `.env`. Not one giant file for the box.

Why it matters in practice: `docker compose down` in a shared file stops everything on the machine, `up -d` after an unrelated edit recreates unrelated containers, and one bad image tag blocks every deploy. Separate stacks fail separately, and each one can be restarted by a person who does not know what else the box runs.

The shared pieces — the proxy, and a network for it — live in their own stack that starts first.

## The Shared Proxy Network

```yaml
# once, from the proxy stack or by hand
networks:
  edge:
    external: true
```

Every app stack joins `edge` for the container the proxy must reach, and keeps its private containers (database, cache, worker) on the stack's default network. The database is then unreachable from the proxy, from other stacks, and from the host — without a single firewall rule.

```yaml
services:
  app:
    networks: [edge, default]     # reachable by the proxy, and by its own db
  db:
    networks: [default]           # reachable only within this stack
```

Containers on the same network resolve each other by **service name** (`db:5432`); nothing else can. That name resolution is the whole access-control story on a single box, and it is stronger than a published port with a firewall in front.

## A Complete Stack

```yaml
services:
  app:
    image: ghcr.io/acme/app@sha256:9f2c1d...   # digest, not a moving tag
    restart: unless-stopped
    env_file: .env                              # 0600, never committed
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://127.0.0.1:8000/healthz"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 30s
    read_only: true
    tmpfs: [/tmp]
    security_opt: ["no-new-privileges:true"]
    cap_drop: [ALL]
    user: "10001:10001"
    deploy:
      resources:
        limits: {memory: 512M}
    logging:
      driver: json-file
      options: {max-size: "10m", max-file: "3"}
    networks: [edge, default]

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      retries: 5
    networks: [default]

volumes:
  pgdata:

networks:
  edge:
    external: true
```

Every line above earns its place: the digest makes the deploy reproducible, `start_period` stops a slow boot being read as a failure, `read_only` plus `tmpfs` removes most post-compromise persistence, and the log limits stop one container filling the disk.

## Restart Policies

| Policy | Behavior |
|---|---|
| `no` (default with `docker run`) | Gone after a crash, a daemon restart, or a reboot. Almost never what anyone wants |
| `on-failure[:N]` | Restart on non-zero exit only; good for jobs |
| `unless-stopped` | Restart always, **except** if you stopped it deliberately — the right default for services |
| `always` | Restarts even after a deliberate stop when the daemon restarts, which surprises people mid-maintenance |

`unless-stopped` only survives a reboot if the container runtime's own service is enabled at boot. On a systemd host: `systemctl is-enabled docker`. This is the container equivalent of `systemctl enable` and it is skipped just as often (`processes.md`).

## Publishing Ports Safely

- `ports: ["127.0.0.1:8000:8000"]` — reachable by the host's proxy, by nothing else. This is the default form for an app behind a proxy.
- `ports: ["8000:8000"]` — published on every interface, **and the rule is written ahead of ufw**, so the port is public even when the firewall says otherwise (`security.md`). Verify from another machine, never from the box.
- No `ports:` at all — the strongest option when the proxy is a container on the same network: it reaches the app by service name, and the host has nothing to expose.
- `expose:` documents a port for other containers; it publishes nothing. It is not a security control, it is a comment.

## Volumes and Permissions

- **Named volumes** for data the container owns (databases): the runtime manages ownership and it survives recreation.
- **Bind mounts** for data you want to see and back up by path (media, uploads, config).
- **UID mismatch is the number one bind-mount problem**: the container writes as UID 10001, the host directory is owned by 1000, and the container gets permission denied — or worse, creates root-owned files the host user cannot delete. Set `user:` to the host owner's UID:GID, or `chown` the directory to the container's UID. Many self-hosted images accept `PUID`/`PGID` for exactly this.
- `:ro` on anything the container does not need to write, config files above all.
- **Never bind-mount the container socket** (`/var/run/docker.sock`) into a service that does not need it: access to it is root on the host. Proxies with a docker provider do need it — mount it read-only and understand that read-only does not meaningfully reduce that risk.
- A named volume is not a backup. It lives on the same disk, and `down -v` deletes it (`maintenance.md`).

## Depends On Is Not Ready

Plain `depends_on` waits for the container to *start*, not to be usable. `condition: service_healthy` with a real healthcheck on the dependency is what actually waits, and even then the app must survive the database going away later — because it will, during an upgrade, and a container that exits on a lost connection with `restart: unless-stopped` recovers, while one that hangs does not.

`start_period` matters more than people expect: without it, a database that takes 40 seconds to initialize is marked unhealthy at second 30 and the whole stack restart-loops on first boot.

## Resource Limits

Without a memory limit, one container's leak invokes the host OOM killer, which picks a victim by heuristic — frequently the database, not the leaker.

- `deploy.resources.limits.memory` (or `mem_limit` in older files) on everything. A container that exceeds it is killed with exit code 137, which is the tell.
- A JVM or Node runtime must be told about the limit too, or it sizes its heap from the host's memory and gets killed while believing it has room (`workers.md`).
- CPU limits are usually unnecessary on a single-app box, and useful to keep a batch container from starving the web path.

## Logging

Container logs default to unbounded JSON files on most runtimes: one chatty container fills the disk and takes the box down. `max-size` and `max-file` on every service, or set the default in the daemon configuration once so new stacks inherit it (`logs.md`).

`docker compose logs -f app` for a single stack; the host's journal for everything else. Shipping to a collector belongs in the logging decision, not per stack.

## Updating Images

1. `docker compose pull` — download first, so the switch is fast and a registry failure happens before anything stops.
2. `docker compose up -d` — recreates only the changed services.
3. Health-check the result; roll back by putting the previous digest back and running `up -d` again (`deployment.md`).

Pin by digest and record it in the deploy row. A moving tag means the image on this box and the image on the next box are different code, and "roll back to `latest`" is not a sentence with meaning.

Automatic updaters (Watchtower and friends) trade a maintenance chore for unattended production changes at 3am. Reasonable for a media box, not for anything anyone depends on; if used, pin to patch-level tags and exclude the database.

## Reaching the Host, and the Host Reaching In

- Container → host service: `host.docker.internal` on Docker Desktop, and on Linux either the bridge gateway (commonly `172.17.0.1`) or an explicit `extra_hosts: ["host.docker.internal:host-gateway"]`, which is the portable form.
- Host → container: the published port, or the container's IP on the bridge network (not stable across recreation — do not put it in a config file).
- `network_mode: host` removes the network namespace: no port mapping, no name resolution between containers, and every listener is on the host's interfaces directly. Necessary for broadcast/discovery protocols and high-volume UDP (`selfhosted.md`), a bad default everywhere else.

## Compose vs systemd Units

| | Compose stack | systemd unit |
|---|---|---|
| Multi-service app with its own database | Natural fit | Several units and hand-written ordering |
| Single compiled binary | Overhead: an image, a registry, a daemon | Natural fit |
| Boot ordering with host services | Weak — the runtime starts everything at once | Native (`After=`, `Requires=`) |
| Resource limits and sandboxing | Runtime-native, good | systemd-native, more granular (`security.md`) |
| Rollback | Previous digest | Previous release directory |

They mix fine: a `docker-compose@.service` unit gives a Compose stack real boot ordering and lets `systemctl` be the single verb on the box. The consistency is worth more than the elegance of either.

## Disk Reclamation

Images, build cache, stopped containers and orphaned volumes accumulate until the disk is full, and the symptom is unrelated services failing.

- `docker system df` first — it tells you which of the four categories is actually large.
- `docker image prune -a` removes unused images; `docker builder prune` clears build cache, which is often the biggest single item on a box that builds.
- **`docker volume prune` deletes data.** Never as a reflex, never as part of a cleanup script that runs unattended, and never on a box whose volumes you have not confirmed are backed up.
- `docker compose down -v` deletes that stack's volumes. `down` without `-v` does not. One character between a restart and a data loss, which is why it belongs behind a confirmation (SKILL.md Output Gates).

## Write It Down

Every containerized service gets its `## Services` row: name, host, `container`/`compose <stack>` as the supervisor, listen address including the `127.0.0.1:` prefix if published that way, restart policy, and the bind-mount path holding its data (`memory-template.md`). Image digests deployed go in `deploys/<year>.md` as the rollback target. A compose file that took real work — a permission fix, a healthcheck that finally stopped a boot loop, a network layout — goes to `~/Clawic/data/server/artifacts/working-stack-<app>.md` with the reason for each non-obvious line, environment values written as pointers (`env:POSTGRES_PASSWORD`), and its `## Boxes` line added the same turn.
