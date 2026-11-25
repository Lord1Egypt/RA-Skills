---
name: proxq
description: Go, Redis-backed async HTTP proxy queue (built on asynq). POST any HTTP request (any method, any path, any body) to a configured upstream, get a job ID back instantly (202), a worker forwards it later, you poll GET /__jobs/{id} for status (queued/running/completed/failed) and GET /__jobs/{id}/content for the replayed upstream response (status/headers/body). DELETE /__jobs/{id} cancels. Path-prefix routing to multiple upstreams, per-upstream timeout/retries/pathFilter, optional response caching (memory or Redis LRU), automatic direct-proxy bypass for WebSocket/chunked/large-body requests. No built-in auth. Use when the user wants to turn a slow/unreliable backend into a fire-and-forget async API, decouple a client from upstream latency, relay webhooks with retries, or queue heavy uploads/processing jobs behind short-timeout reverse proxies.
homepage: https://github.com/psyb0t/docker-proxq
user-invocable: true
metadata:
  { "openclaw": { "emoji": "🦡", "primaryEnv": "PROXQ_URL", "requires": { "bins": ["curl", "docker"] } } }
permissions:
  network: "outbound HTTP to the configured PROXQ_URL (submit/poll/cancel job calls), AND proxq itself makes arbitrary outbound HTTP requests to whatever upstream/URL you submit through it, on your behalf. That's an SSRF surface: only submit requests you intend proxq's configured upstreams to receive."
  shell: "curl + docker/docker-compose invocations shown in setup.md and this file (container lifecycle, request examples); no other host access"
---

# proxq

The honey badger of HTTP proxies. POST a request, get a job ID back instantly, come back later for the goods. "I'll get back to you" as a service: every HTTP request becomes an async job in a Redis-backed queue (via [asynq](https://github.com/hibiken/asynq)).

For installation, configuration, and container setup, see [references/setup.md](references/setup.md).

## Security & safety

- **This is an SSRF surface by design.** proxq's whole job is to make outbound HTTP requests to an upstream on your behalf. That's not a bug, it's the feature. Anyone who can submit a job through proxq gets proxq's network position to reach whatever `upstreams[].url` is configured (and, via `directProxyMode`/prefix stripping, whatever path/query you tack onto it). Never point an upstream at internal/admin services you wouldn't otherwise expose, and never let untrusted callers choose the upstream prefix or URL.
- **No built-in authentication or authorization.** proxq ships with zero auth: no API key, no bearer token, no allowlist. Anyone who can reach `PROXQ_URL` can submit jobs, poll any job ID, and cancel any job ID (job IDs are UUIDv4 but there is no ownership check). Front it with a reverse proxy doing auth (basic auth, mTLS, an API gateway) or bind it to loopback/an internal network only. Do not expose a bare proxq instance to the open internet.
- **Trusted upstreams only.** Configure `upstreams[].url` to point only at backends you control or explicitly trust. proxq forwards the full original request (method, headers, body) plus `X-Forwarded-For`/`X-Real-IP`/`X-Forwarded-Proto`, so treat the upstream config the same way you'd treat a reverse-proxy target list.
- **Consumer-only.** This skill talks to an instance you (or your operator) already run and trust. It never provisions, hardens, or reconfigures the server; that's covered in setup.md as an explicit operator step.
- **Cancelling a job.** `DELETE /__jobs/{id}` best-effort stops an in-flight job and deletes its record (no undo). Per the no-auth point above there's no ownership check, so only cancel a job you submitted or one the user explicitly named. Don't guess IDs or bulk-cancel.

## When To Use

- Put an async facade in front of a slow backend so callers get an instant response instead of hanging on a long-running request.
- Decouple a client from an upstream that occasionally times out: proxq queues the request, retries transport failures automatically, and the client polls at its own pace.
- Sit behind a CDN/reverse-proxy with a short request timeout while your real backend takes minutes.
- Relay webhooks without blocking the sender, with configurable retry/backoff.
- Queue large uploads or long-running processing jobs (video, exports, reports) so the client doesn't hold a connection open.
- Mix sync and async traffic on one gateway: fast paths (auth, health) bypass the queue via `pathFilter`, slow paths get queued.
- Cache idempotent (or even non-idempotent-but-repeatable) responses so duplicate requests don't re-hit the upstream.

## When NOT To Use

- True real-time / streaming responses: the whole model is submit-then-poll; there's no push/webhook-back-to-caller notification built in.
- WebSocket or chunked-transfer traffic that needs the queue semantics: those bypass the queue automatically and just get reverse-proxied straight through (see `directProxyMode` in setup.md), so don't expect a job ID for them.
- As a public-facing endpoint without your own auth layer in front. proxq has none.
- Pointing an upstream at anything you don't fully trust: proxq will happily forward arbitrary methods/bodies/headers to it.

## Usage

Point at a running instance:

```bash
export PROXQ_URL=http://localhost:8080
```

All job-management endpoints live under `jobsPath` (default `/__jobs`). Every response proxq itself generates (not proxied from upstream) carries `X-Proxq-Source: proxq`, except the `200` answers from the status and cancel endpoints and the `500` answers those endpoints give when Redis fails. That's how you distinguish a proxq-origin response (job not ready, no upstream match, proxq error) from a real upstream response replayed verbatim.

### Submit a job

Any request that doesn't hit a job endpoint gets routed by longest-prefix match to a configured upstream and queued (unless it qualifies for direct-proxy bypass, see setup.md).

```bash
curl -s -X POST "$PROXQ_URL/api/heavy-computation" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $UPSTREAM_TOKEN" \
  -d '{"data": "lots of it"}'
# 202 Accepted, X-Proxq-Source: proxq
# {"jobId": "550e8400-e29b-41d4-a716-446655440000"}
```

If no upstream prefix matches the request path: `502 Bad Gateway`, `X-Proxq-Source: proxq`.

Optional per-request override header: `X-Proxq-Timeout: <go-duration>` (e.g. `X-Proxq-Timeout: 30s`) overrides the upstream's configured `timeout` for that one request. Invalid value → `400 Bad Request`.

### Poll job status

```bash
curl -s "$PROXQ_URL/__jobs/550e8400-e29b-41d4-a716-446655440000"
```

```json
{"id": "550e8400-...", "status": "completed", "completedAt": "2025-01-01T00:00:00Z"}
```

Failed job includes `error`:

```json
{"id": "550e8400-...", "status": "failed", "error": "forward request: dial tcp: connection refused"}
```

`status` is one of `queued` (pending/scheduled/aggregating), `running` (active, or waiting on a retry), `completed` (done, response stored, even if upstream returned 4xx/5xx), `failed` (transport broke and retries are exhausted). Unknown job ID → `404 Not Found`, `X-Proxq-Source: proxq`, body `{"code":"NOT_FOUND","message":"Not found"}`.

### Fetch job content (the payoff)

Replays the upstream response exactly (status code, headers, body) as if you'd called upstream directly.

```bash
curl -si "$PROXQ_URL/__jobs/550e8400-e29b-41d4-a716-446655440000/content"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Custom-Header: from-upstream

{"result": "done"}
```

If upstream returned a 404, you get 404 back too, but **without** `X-Proxq-Source` (it's a real upstream response). If the job isn't done yet, or doesn't exist: `404 Not Found` **with** `X-Proxq-Source: proxq`. That header is the whole disambiguation trick: present means "proxq talking", absent means "upstream talking".

### Cancel a job

```bash
curl -s -X DELETE "$PROXQ_URL/__jobs/550e8400-e29b-41d4-a716-446655440000"
# {"status": "cancelled"}
```

Best-effort: attempts to stop in-flight processing, then deletes the task record. A job that is still `running` may return `500` because asynq cannot delete a job a worker holds; check the status and retry the DELETE once it is no longer running. Unknown job ID → `404 Not Found`, `X-Proxq-Source: proxq`. (See [Security & safety](#security--safety): no ownership check, so only cancel jobs you own.)

### Poll loop example

```bash
JOB_ID=$(curl -s -X POST "$PROXQ_URL/api/report" -d '{}' | jq -r .jobId)

while :; do
  STATUS=$(curl -s "$PROXQ_URL/__jobs/$JOB_ID" | jq -r .status)
  case "$STATUS" in
    completed) curl -s "$PROXQ_URL/__jobs/$JOB_ID/content" | jq; break ;;
    failed)    echo "job failed" >&2; break ;;
    *)         sleep 2 ;;
  esac
done
```

For upstream routing rules (prefix matching/stripping), direct-proxy bypass conditions, caching behavior, and the full config reference (env vars, docker run/compose), see [references/setup.md](references/setup.md).
