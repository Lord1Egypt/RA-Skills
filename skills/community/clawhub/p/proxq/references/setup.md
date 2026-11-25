# proxq setup

## Quick start (docker compose)

```yaml
services:
  proxq:
    image: psyb0t/proxq
    ports:
      - "127.0.0.1:8080:8080"   # bind loopback-only; no built-in auth (see SKILL.md Security & safety)
    environment:
      PROXQ_CONFIG: /etc/proxq/config.yaml
    configs:
      - source: proxq_config
        target: /etc/proxq/config.yaml
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    restart: unless-stopped

configs:
  proxq_config:
    content: |
      listenAddress: "0.0.0.0:8080"
      redis:
        addr: "redis:6379"
      upstreams:
        - prefix: "/"
          url: "http://your-api:3000"
```

```bash
docker compose up -d
curl http://127.0.0.1:8080/__jobs/nonexistent-id   # 404, X-Proxq-Source: proxq → confirms it's up
```

## Docker run (config file mounted from host)

```bash
docker run -d \
  --name proxq \
  -p 127.0.0.1:8080:8080 \
  -e PROXQ_CONFIG=/etc/proxq/config.yaml \
  -v "$(pwd)/config.yaml:/etc/proxq/config.yaml:ro" \
  --link redis \
  psyb0t/proxq
```

Requires a reachable Redis instance (`redis:7-alpine` or any compatible server).

## Config resolution

Config path is resolved in this order: `--config` CLI flag → `PROXQ_CONFIG` env var → `config.yaml` in the current directory. Everything else lives inside the YAML file itself; there is no per-field env var override for the rest of the settings, so mount/generate the YAML.

| Env var / flag | Purpose |
|---|---|
| `--config <path>` | CLI flag, highest priority |
| `PROXQ_CONFIG` | Path to the YAML config file, read if `--config` is unset |

The published image runs the process as a fixed non-root user (`proxq`) baked into the image at build time; there is no `PUID`/`PGID` override.

## Config file reference (YAML)

### Global settings

| Field | Type | Default | Description |
|---|---|---|---|
| `listenAddress` | string | `127.0.0.1:8080` | HTTP server bind address |
| `redis.addr` | string | `127.0.0.1:6379` | Redis server address |
| `redis.username` | string | `""` | Redis ACL username. Empty uses the default user |
| `redis.password` | string | `""` | Redis password |
| `redis.db` | int | `0` | Redis database number |
| `queue` | string | `default` | asynq queue name |
| `concurrency` | int | `10` | Concurrent workers hitting upstream |
| `jobsPath` | string | `/__jobs` | Base path for the jobs API endpoints |
| `taskRetention` | duration | `1h` | How long completed/failed jobs stay in Redis before eviction |

Duration values use Go syntax: `30s`, `5m`, `1h`, `1h30m`.

### Upstreams (`upstreams[]`)

Routed by longest path-prefix match; the matched prefix is stripped before forwarding.

| Field | Type | Default | Description |
|---|---|---|---|
| `prefix` | string | **required** | URL path prefix for routing. Stripped before forwarding. |
| `url` | string | **required** | Upstream server URL. May include a path (e.g. `http://api:3000/v2`). |
| `timeout` | duration | `5m` | Per-upstream request timeout (overridable per-request via `X-Proxq-Timeout`) |
| `maxRetries` | int | `0` | Retry attempts on transport failure. `0` = no retries. |
| `retryDelay` | duration | `0` | Fixed delay between retries. `0` = exponential backoff (`n^4` seconds with `n` = retries already made: no wait, 1s, 16s, 81s, ~4m for retries 1-5). |
| `maxBodySize` | int (bytes) | `10485760` (10 MB) | Max request body buffered into the queue. A longer queued body is silently cut to this size |
| `directProxyThreshold` | int (bytes) | `10485760` (10 MB) | Body size above which requests bypass the queue entirely. `0` or unset means the 10 MB default; a negative value such as `-1` disables the check (always queue regardless of size, up to `maxBodySize`). |
| `directProxyMode` | string | `proxy` | How bypassed requests reach upstream: `proxy` (reverse-proxied, client never sees upstream URL) or `redirect` (`307 Temporary Redirect` to the upstream URL) |
| `cacheKeyExcludeHeaders` | list[string] | `[]` (defaults apply) | Headers excluded from the cache key. Empty list = built-in defaults (`X-Request-ID`, `X-Forwarded-For`, `X-Real-IP`, `X-Forwarded-Proto`). Setting this **replaces** the defaults entirely. Names are matched exactly against Go's canonical header form (`X-Request-Id`, `X-Trace-Id`), so `X-Request-ID` and `X-Real-IP` in the defaults never match. |
| `pathFilter.mode` | string | `blacklist` | `blacklist`: matching paths bypass the queue. `whitelist`: only matching paths get queued. |
| `pathFilter.patterns` | list[string] | `[]` | Regex patterns matched against the request path. |

### Cache (`cache`)

| Field | Type | Default | Description |
|---|---|---|---|
| `cache.mode` | string | `none` | `none`, `memory` (in-process LRU), or `redis` (shared, same Redis instance as the queue) |
| `cache.ttl` | duration | `5m` | Freshness window |
| `cache.maxEntries` | int | `10000` | Max entries for in-memory LRU mode |
| `cache.redisKeyPrefix` | string | `proxq:` | Key prefix for Redis cache mode, avoids colliding with job data |

Cache rules: any HTTP method can be cached (same body → cache hit, different body → miss); only 2xx upstream responses are cached; cache key = `sha256(method + url + headers + body)` with volatile headers excluded per `cacheKeyExcludeHeaders`. Responses carry `X-Cache-Status: HIT` or `MISS`.

### Direct proxy bypass, checked in this order

| Condition | Why |
|---|---|
| WebSocket (`Connection: upgrade` + `Upgrade: websocket`) | Persistent bidirectional, can't queue |
| Chunked transfer (`Transfer-Encoding: chunked`) | Size unknown |
| Body over `directProxyThreshold` | Avoid buffering huge uploads into Redis |
| Path filter match (per-upstream `pathFilter`) | Explicit opt-out |

### Validation (fails startup if violated)

- At least one upstream is required.
- Every upstream needs both `prefix` and `url`.
- Single upstream may use `prefix: "/"` (catch-all). Multiple upstreams may **not** include `prefix: "/"`: too ambiguous.
- No nested prefixes (`/api` and `/api/v2` together is an error).
- No upstream prefix may conflict with `jobsPath` (e.g. an upstream at `/__jobs` when `jobsPath` is `/__jobs`).
- All `pathFilter.patterns` must be valid regexes.

### Example config

```yaml
listenAddress: "0.0.0.0:8080"

redis:
  addr: "redis:6379"
  username: ""
  password: ""
  db: 0

queue: "default"
concurrency: 10
jobsPath: "/__jobs"
taskRetention: "1h"

cache:
  mode: "redis"
  ttl: "10m"
  redisKeyPrefix: "proxq:"

upstreams:
  - prefix: "/api"
    url: "http://api-server:3000"
    timeout: "5m"
    maxRetries: 3
    retryDelay: "10s"
    pathFilter:
      mode: "blacklist"
      patterns:
        - "^/api/auth"
        - "^/api/health"

  - prefix: "/uploads"
    url: "http://file-server:9000/storage"
    timeout: "10m"
    maxBodySize: 1073741824
    directProxyThreshold: -1
    directProxyMode: "redirect"
```

## Headers reference

Set by proxq on responses it generates itself (never on responses proxied verbatim from upstream):

| Header | Value | When |
|---|---|---|
| `X-Proxq-Source` | `proxq` | `202` accepted, `400` bad `X-Proxq-Timeout`, `502` no upstream match, `500` errors on submit, `307` redirects, `404` from job endpoints, reverse-proxy errors. Not on the `200` or `500` answers of the status and cancel endpoints |
| `X-Cache-Status` | `HIT` / `MISS` | On cached responses, when caching is enabled |

Accepted from the client:

| Header | Effect |
|---|---|
| `X-Proxq-Timeout` | Go duration string (e.g. `30s`), overrides the matched upstream's `timeout` for that one submitted request. Invalid value → `400`. |

Forwarded to upstream on every queued request: original headers as-is, plus `X-Forwarded-For`, `X-Real-IP`, `X-Forwarded-Proto`. Direct-proxied requests get none of these three from proxq. Hop-by-hop headers (`Connection`, `Keep-Alive`, `Proxy-Authenticate`, `Proxy-Authorization`, `TE`, `Trailers`, `Transfer-Encoding`, `Upgrade`) are stripped per RFC 7230.

## No built-in auth

proxq has no authentication of its own: no API key, bearer token, or allowlist on any endpoint (job submission, status, content, cancel). Put it behind:
- A reverse proxy doing auth (basic auth, OAuth2 proxy, mTLS) in front of `listenAddress`.
- Network isolation: bind `listenAddress`/the published port to loopback or an internal-only network, never `0.0.0.0` on a publicly routable host without a fronting proxy.

Job IDs are UUIDv4 (unguessable in practice) but there is **no ownership check**: anyone who can reach the instance and knows/guesses a job ID can poll or cancel it.

## Management / development (operator-side, from the repo)

```bash
make dep            # vendor dependencies
make lint           # golangci-lint
make test           # unit + integration tests (race detector on)
make test-coverage  # tests with 90% coverage threshold
make build           # docker build

# e2e tests: spins up Redis + upstream + proxq via testcontainers
cd tests && go test -v -timeout 10m ./...
```
