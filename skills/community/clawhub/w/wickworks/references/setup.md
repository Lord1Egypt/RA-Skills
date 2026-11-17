# wickworks setup

wickworks is a single stateless HTTP container: no DB, no queues, no external
calls. Stand one up, point `WICKWORKS_URL` at it, done.

## Requirements

- `docker` (to run the image) and `curl` (to call it). A local run from a
  clone of the repository needs only Docker and Make.
- OHLC bars to feed it. wickworks has no market-data feed of its own.

## Security & safety

wickworks ships **auth-less** and **stateless**: bars in, primitives out, no
writes, no destructive ops. But anyone who can reach the port can call it, so:

- **Bind to loopback by default:** `-p 127.0.0.1:8000:8000`. Only expose it
  off-host behind your own reverse proxy / VPN with auth in front.
- It never fetches or transmits your bars anywhere; it only computes on what you
  POST. Still, only run an instance you (or a trusted operator) control.

## Quick Install

### docker run

```bash
docker run --rm -p 127.0.0.1:8000:8000 psyb0t/wickworks:latest
# listens on :8000; GET /health to check
```

### docker compose

```yaml
services:
  wickworks:
    image: psyb0t/wickworks:latest
    restart: unless-stopped
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      LOG_LEVEL: INFO
      MAX_BARS: "5000"
      MIN_BARS: "50"
      WORKERS: "2"
```

### Local (from a clone)

```bash
make run       # builds the dev image, then runs uvicorn on :8000
```

## Point the skill at it

```bash
export WICKWORKS_URL="http://localhost:8000"
curl -s "$WICKWORKS_URL/health"     # {"ok":true,"version":"..."}
```

For the MCP bridge plugin, the same base URL: `WICKWORKS_URL` (the bridge
appends `/mcp/`), plus optional `WICKWORKS_TOKEN` if a reverse proxy in front
requires a bearer.

## Environment Variables

All env-driven; sensible defaults, nothing to tune for a first run.

| Variable    | Default | Description |
| ----------- | ------- | ----------- |
| `LOG_LEVEL` | `INFO`  | Python logging level. |
| `MAX_BARS`  | `5000`  | Reject requests with more bars than this (HTTP 413). |
| `MIN_BARS`  | `50`    | Baseline warm-up floor for SMC outputs / summaries and the fallback for indicators without an explicit requirement. Series indicators (`sma`, `rsi`, `macd`, …) compute their own minimum from params. |
| `WORKERS`   | `2`     | uvicorn worker count. |

wickworks has **no auth env var**. Connection-level access control is the
operator's responsibility (loopback bind + reverse proxy). The MCP transport's
DNS-rebinding Host check is disabled so real-hostname deployments work; gate
access at your proxy, not the app.
