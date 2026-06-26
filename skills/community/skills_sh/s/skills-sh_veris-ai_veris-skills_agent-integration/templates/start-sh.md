# start.sh Templates

## Template 1: Bundled services + single agent process

```bash
#!/bin/bash
set -e

echo "Starting bundled services..."

# Start Redis
redis-server --daemonize yes --maxmemory 128mb --maxmemory-policy allkeys-lru
until redis-cli ping 2>/dev/null | grep -q PONG; do sleep 0.5; done
echo "Redis ready"

# Start agent (foreground — must be last, must use exec)
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
```

## Template 2: Multi-agent gateway + sub-agents

```bash
#!/bin/bash
set -e

echo "Starting sub-agents..."

# Start sub-agents in background
(cd /agent/flight-agent && uvicorn main:app --host 0.0.0.0 --port 8081) &
(cd /agent/hotel-agent && uvicorn main:app --host 0.0.0.0 --port 8082) &

# Wait for sub-agents to be ready
echo "Waiting for sub-agents..."
for port in 8081 8082; do
  for i in $(seq 1 30); do
    if curl -sf http://localhost:$port/health >/dev/null 2>&1; then
      echo "  Port $port ready"
      break
    fi
    sleep 1
  done
done

# Start gateway (foreground — must be last, must use exec)
cd /agent/gateway
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
```

## Template 3: FastAPI + background workers

```bash
#!/bin/bash
set -e

echo "Starting background workers..."

# Start Celery worker (or other background processor)
python -m app.workers.celery_worker \
  --concurrency 2 \
  --loglevel info &

# Start webhook listener (if needed)
python -m app.webhook_listener &

# Start main API server (foreground — must be last, must use exec)
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
```

## Template 4: Peer processes with fail-fast

Use this when the container holds **multiple peer processes that all must be alive for the agent to work**, and no single one of them is naturally "the" foreground process. The canonical case is a [transport bridge](../reference/infrastructure-patterns.md#pattern-9-transport-bridge): an in-container media server, the agent worker (which auto-dispatches into the media server's rooms), and the bridge that accepts the actor's channel connection — none of them can be the lone `exec`'d foreground because all three are equally critical.

```bash
#!/bin/bash
# Multi-process container with fail-fast — if any peer dies, take down
# the rest so Veris restarts the container cleanly instead of leaving a
# partially-working stack serving broken responses.

# Peer 1: in-container service the agent depends on (media server, SIP daemon, etc.)
/usr/local/bin/some-server --bind 0.0.0.0 &
SVC_PID=$!

# Give the server a beat to bind sockets before the worker starts probing it.
sleep 1

# Peer 2: agent worker (registers against the in-container service)
uv run --no-sync python -m app.worker start &
WK_PID=$!

# Peer 3: bridge / API on the actor's port — also a peer, not the "main"
uv run --no-sync uvicorn app.bridge:app \
    --host 0.0.0.0 --port "${PORT:-8080}" &
BR_PID=$!

# Clean shutdown. wait -n returns when the first child exits; cleanup
# kills the rest so the container exits as a unit and Veris restarts
# it instead of half-serving requests. NOTE: we intentionally avoid
# `set -e` here — with `set -e`, a non-zero exit from the first child
# would terminate the shell before the explicit kill block runs,
# leaving orphan peers behind.
cleanup() {
  kill "$SVC_PID" "$WK_PID" "$BR_PID" 2>/dev/null || true
}
trap 'cleanup; exit 143' TERM INT

wait -n
status=$?
echo "[start] a peer process exited (status=$status) — shutting down siblings"
cleanup
wait || true
exit "$status"
```

When to prefer this over Templates 1-3:

- **Use Template 1** when there's one clear foreground process (the agent's HTTP server) and the rest are infrastructure it talks to (Redis, etc.). The agent process is the natural `exec` target; if Redis crashes, the agent's next request will fail loudly enough that you'll notice.
- **Use Template 4** when peer processes are equally critical to the agent's wire contract and a silent crash of any one of them leaves the container *looking* healthy from outside (port still open, /health still returns 200) while actually serving broken responses. The media-server-plus-worker-plus-bridge shape is the prototypical case; bash's `wait -n` is the simplest way to make that container fail loudly.

## Rules

- **Templates 1–3:** the LAST command must use `exec` (replaces shell process, receives signals correctly). Background processes use `&`. A background process failing leaves the container running — that's intentional when the dependency isn't on the response path.
- **Template 4:** the foreground `exec` rule does **not** apply — all peer processes run as backgrounds, and a `trap` + `wait -n` + explicit `cleanup` brings the container down as a unit when any peer dies. Use this only when the silent-crash failure mode of Templates 1-3 is unacceptable.
- Always wait for bundled services to be healthy before starting the agent.
- `set -e` at the top of Templates 1–3 is fine; **do not** combine `set -e` with the Template 4 `wait -n` pattern — a non-zero child exit will kill the shell before cleanup runs, leaving orphan peers.
- Use `${PORT:-8080}` to respect veris port injection.
- Never use supervisord in sandbox — start.sh is simpler and sufficient.
- Veris already starts `start.sh` from `agent.code_path`, so do not add a redundant `cd /agent` at the top.
- If you must launch background work from a subdirectory, use an explicit absolute-path subshell like `(cd /agent/worker && python main.py) &`.
- If the foreground process lives in a subdirectory, `cd` there immediately before the final `exec` (Templates 1–3 only).
