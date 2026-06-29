---
name: webhook-relay
description: >-
  Webhook Relay integration, driven by the `relay` CLI and the public bin API.
  Receive webhooks on a stable public HTTPS endpoint and forward them to a
  service on localhost or a private network with no public IP (the relay agent
  performs the last hop), or expose any local/internal HTTP or TCP service to
  the internet over a public tunnel. Capture and inspect incoming webhooks with
  a free, no-signup bin to debug exactly what a provider sends, verify HMAC
  signatures, and mock responses. Also: forward server-side to public URLs (no
  agent), fan out one webhook to many destinations, transform payloads with
  JavaScript functions, and schedule recurring (cron) webhooks. Use when the
  user wants to forward, tunnel, debug, transform, or schedule webhooks with
  Webhook Relay.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🪝"
    homepage: https://webhookrelay.com
    requires:
      anyBins: [relay, curl]
---

# Webhook Relay

[Webhook Relay](https://webhookrelay.com) moves HTTP traffic across network
boundaries. It gives you stable public endpoints and a lightweight agent so you
can receive provider webhooks anywhere, expose private services to the internet,
and see exactly what is being sent — without opening firewall ports or owning a
public IP.

This skill covers three primary jobs and a few supporting ones:

1. **Forward webhooks to a private / internal destination** — a provider POSTs
   to a public URL; Webhook Relay streams it down the agent's outbound
   connection to `localhost`, a LAN host, or a Kubernetes service.
2. **Expose a local/internal service to the internet** — publish a stable public
   HTTPS (or TCP) hostname that proxies all inbound traffic to a service only
   your machine can reach (ngrok-style tunnel).
3. **Debug webhooks** — capture and inspect requests in a free, no-signup bin to
   see the exact method, headers, query and body a provider sends.

Supporting: forward server-side to **public** URLs (no agent), **fan out** to
many destinations, **transform** payloads with JavaScript functions, and
schedule **recurring (cron)** webhooks.

Official docs: https://webhookrelay.com/docs — most pages also render as plain
markdown by appending `.md` to the URL.

## Core concepts

- **Bucket** — a container that groups one or more inputs and outputs.
- **Input** — a public endpoint (`https://my.webhookrelay.com/v1/webhooks/<id>`)
  that receives requests. This is the URL you hand to a provider.
- **Output** — a destination a received request is delivered to. `internal`
  outputs (localhost / private network) require the **agent to be running**;
  `public` outputs are delivered server-side with **no agent**.
- **Tunnel** — a public hostname that reverse-proxies *all* inbound HTTP/TCP
  traffic to a destination, for dev servers, demos, APIs, and TCP services.
- **Bin** — a throwaway public endpoint that records every request for
  inspection. No account, key, or CLI required.
- **Function** — server-side JavaScript (or Lua) attached to an input/output
  that rewrites the request, sets the response, or drops it.
- **Cron** — a schedule that fires a webhook automatically.

## Install the CLI and authenticate

The bin (debugging) needs **no install** — it's plain `curl`. Everything else
uses the `relay` CLI.

```bash
# Install — see https://webhookrelay.com/docs/installation/cli
# macOS/Linux quick install, or download a binary from the docs page.

relay login                 # interactive; or set RELAY_KEY / RELAY_SECRET
relay bucket ls             # confirm you're authenticated
```

For CI/servers, set the `RELAY_KEY` and `RELAY_SECRET` environment variables
instead of `relay login`.

---

## 1. Forward webhooks to a private / internal destination

A provider needs to reach code running on `localhost`, a private LAN host, or a
Kubernetes service that has no public IP. Webhook Relay gives you a public input
URL; the agent holds an outbound connection and performs the final hop to your
private destination. Nothing inbound is opened on your firewall.

```
Provider ──POST──▶ https://my.webhookrelay.com/v1/webhooks/<id>  (input, public)
                              │  (streamed down the agent's outbound connection)
                              ▼
                   relay agent on your machine
                              │
                              ▼
                   http://localhost:8080/webhook   (output, internal)
```

> An **internal** output requires the agent to be **running** — it is the agent
> that delivers to the private destination.

### Fastest path: `relay forward`

Creates a bucket + public input + internal output, starts the agent, and
subscribes to the stream — all in one command. Ideal for local development.

```bash
relay forward --bucket my-app http://localhost:8080/webhook
```

- A bucket `my-app` is created if it doesn't exist.
- A public input URL is printed (e.g.
  `https://my.webhookrelay.com/v1/webhooks/2a1b…`) — **give this to the
  provider** (Stripe dashboard, GitHub webhook settings, etc.), never
  `localhost`.
- The agent stays in the foreground; each received webhook is forwarded to your
  local server and logged. Ctrl-C to stop; re-run the same command to resume.

`--type internal` is the default. Re-attach to an existing bucket and relay all
its configured outputs with `relay forward --bucket my-app` (no destination).

Useful flags: `--bucket/-b`, `--function/-f <name|id>` (attach a transform),
`--no-agent` (configure only), and `--max-retries` / `--retry-wait-min` /
`--retry-wait-max` (retry when the destination returns `>= 500`).

### Persistent / explicit setup (servers, config-as-code)

```bash
relay bucket create my-app
relay input  create --bucket my-app "default public endpoint"   # prints the URL
relay output create local-app --bucket my-app \
  --destination http://localhost:8080/webhook                   # internal (default)
relay forward -b my-app                                         # foreground agent
# …or run the agent as a background OS service:
relay service install && relay service start
```

> **Name every output** — the name is the first positional argument
> (`local-app` above). Omitting it creates an empty-named output, and adding a
> second un-named output to the same bucket fails with
> `output with name '' already exists` (which also breaks fan-out).

Inspect / clean up:

```bash
relay bucket ls
relay bucket inspect my-app
relay input ls            # shows the public endpoint URLs
relay output ls
relay bucket rm my-app -f # -f also removes the bucket's inputs/outputs
```

For Kubernetes ingress (exposing in-cluster services), see `relay ingress`.

---

## 2. Expose a local / internal service to the internet (tunnel)

A **tunnel** publishes a public hostname (e.g. `https://myapp.webrelay.io`) and
routes *all* traffic hitting it to a destination your machine can reach. The
agent keeps an outbound connection open, so no inbound ports or public IP are
required. Unlike webhook forwarding, a tunnel proxies any inbound HTTP or TCP
traffic — ideal for dev servers, demos, local APIs, and TCP services (SSH,
databases).

```
Internet ──▶ https://myapp.webrelay.io  (public tunnel host)
                       │  (over the agent's outbound connection)
                       ▼
              relay agent  ──▶  http://localhost:3000  (your service)
```

### Fastest path: `relay connect`

```bash
# Expose a local web app; a public *.webrelay.io host is assigned and printed.
relay connect http://localhost:3000

# Pin a friendly subdomain and enable HTTPS at the edge:
relay connect --name myapp --subdomain myapp --crypto flexible \
  http://localhost:3000
# → https://myapp.webrelay.io  (reuse the same --name to keep the same host)
```

The agent runs in the foreground and logs each request. Ctrl-C to stop; re-run
the **full** `relay connect … <destination>` command to bring it back on the
same hostname (running `relay connect --name myapp` alone falls back to
`http://127.0.0.1:80` and you'll get 502s).

Common flags:

- `--name/-n` — stable identity; reuse to keep the same host.
- `--subdomain/-s` / `--host/-H` — preferred subdomain or full custom host.
- `--crypto/-c` — TLS mode: `flexible` (HTTPS at the edge, HTTP to your service
  — most common), `full`, `full-strict`, `tls-pass-through`.
- `--region/-r` — pick a region (e.g. `eu`, `us-west`) to lower latency.
- `--username/-u` / `--password/-p` — protect the tunnel with HTTP basic auth.
- `--rewrite-host-header` — set the Host header sent to your service (needed by
  many vhost-based apps and dev servers, e.g. `--rewrite-host-header localhost`).
- `--protocol` — `http` (default) or `tcp` (expose SSH, databases, etc.).
- `--group/-g` — group tunnels so one agent serves several at once.
- `--no-agent` — create the configuration only, don't start the agent.

### Recipes

```bash
# Share a Vite dev server with the right Host header
relay connect -n dev -s dev -c flexible --rewrite-host-header localhost \
  http://localhost:5173

# Password-protect a demo
relay connect -n demo -s demo -c flexible -u alice -p s3cret http://localhost:8080

# Expose a private LAN host (run the agent on a machine that can reach it)
relay connect -n grafana -s grafana -c flexible http://10.0.0.5:3000

# TCP tunnel (e.g. SSH)
relay tunnel create ssh-box --protocol tcp --destination tcp://localhost:22
relay connect --name ssh-box --protocol tcp tcp://localhost:22
```

Explicit, persistent setup mirrors forwarding:

```bash
relay tunnel create myapp --destination http://localhost:3000 \
  --subdomain myapp --crypto flexible --region eu
relay tunnel ls
relay tunnel inspect myapp
relay connect --name myapp --crypto flexible http://localhost:3000
relay tunnel rm myapp
```

---

## 3. Debug webhooks with a bin (no install, no signup)

A **bin** is a throwaway public endpoint that captures every HTTP request sent
to it, so you can see exactly what a provider sends, reproduce a payload, or mock
an endpoint's response while building the real handler.

- **API base:** `https://bin.webhookrelay.com` — no auth, CORS enabled.
- **Public & temporary** — anyone with the bin ID can read it; bins auto-expire
  after ~48 hours. **Never send secrets or PII to a bin.**

```bash
B=https://bin.webhookrelay.com

# 1. Create a bin, capture its ID
BIN=$(curl -s -X POST $B/v1/bins | jq -r .id)

# 2. The public receiver URL — give it to any sender (accepts ANY method):
echo "$B/v1/webhooks/$BIN"

# 3. Send a test request
curl -s -X POST "$B/v1/webhooks/$BIN" -H 'Content-Type: application/json' -d '{"hello":"world"}'

# 4. Read back every captured request as JSON
curl -s "$B/v1/bins/$BIN" | jq '.requests'
```

Open the same bin in a browser UI:
`https://webhookrelay.com/webhook-bin?bin=<BIN_ID>`

Each captured request has `id` (sortable ULID), `receivedAt` (Unix seconds),
`method`, `header` (map of `name → { key, values[] }`), `query` (raw string),
`body` (raw string), `ip`, and `responseStatus`.

```bash
# Most recent request's body
curl -s "$B/v1/bins/$BIN" | jq -r '.requests | sort_by(.receivedAt) | last | .body'

# Block until exactly one request arrives, then print it (live SSE stream)
curl -sN "$B/v1/events?stream=$BIN" | grep -m1 '^data:' | sed 's/^data: //' | jq .
```

### Mock the response the bin returns

`PUT /v1/bins/{id}` configures the reply — custom status/body/headers, latency,
and probabilistic failures (test a sender's retry logic):

```bash
curl -s -X PUT "$B/v1/bins/$BIN" -H 'Content-Type: application/json' -d '{
  "id": "'"$BIN"'",
  "response": {
    "status": 201,
    "body": "{\"ok\":true}",
    "delay": 250,
    "header": { "Content-Type": { "key": "Content-Type", "values": ["application/json"] } },
    "failures": [ { "percentage": 10, "status": 500, "body": "simulated failure" } ]
  }
}'
```

### Verify an HMAC signature

`POST /v1/hmac` with `{ algorithm, secret, body }` where `body` is **base64**
encoded (algorithms: `md5`, `sha1`, `sha256`, `sha512`). Returns
`{ "signature": "<hex>" }`. Prefix as the provider expects (GitHub:
`sha256=<hex>`; Stripe builds `t=…,v1=<hex>` over `"{t}.{body}"`).

```bash
RAW=$(curl -s "$B/v1/bins/$BIN" | jq -r '.requests | sort_by(.receivedAt) | last | .body')
# Pipe base64 through `tr -d '\n'` — GNU base64 wraps at 76 cols and would
# embed newlines in the body, producing a wrong signature.
SIG=$(curl -s -X POST "$B/v1/hmac" -H 'Content-Type: application/json' -d "$(jq -nc \
  --arg s "$WEBHOOK_SECRET" --arg b "$(printf %s "$RAW" | base64 | tr -d '\n')" \
  '{algorithm:"sha256", secret:$s, body:$b}')" | jq -r .signature)
echo "expected: sha256=$SIG"
```

Bin endpoint reference: `POST /v1/bins` (create), `GET /v1/bins/{id}` (read +
requests), `PUT /v1/bins/{id}` (configure response), `DELETE /v1/bins/{id}`,
`(any) /v1/webhooks/{id}` (receiver), `GET /v1/events?stream={id}` (SSE),
`POST /v1/hmac`. Bodies are capped at 500 KB; the service is rate limited (429
when flooded).

---

## Supporting capabilities

### Forward to a public destination (no agent)

When the destination is already on the internet, use a **public** output. It is
delivered server-side, so no agent runs and it works 24/7.

```bash
relay forward --type public --bucket to-slack \
  https://hooks.slack.com/services/T000/B000/XXXX
```

The CLI configures it and exits. Pair with a function to reshape the payload.

### Fan out one webhook to many destinations

Add several outputs to the same bucket; every received webhook is delivered to
all of them.

```bash
relay output create slack   -b alerts --type public -d https://hooks.slack.com/services/…
relay output create discord -b alerts --type public -d https://discord.com/api/webhooks/…
relay output create ingest  -b alerts --type public -d https://example.com/ingest
```

### Transform webhooks in flight (JavaScript functions)

A **function** runs server-side on each request passing through an input/output.
Your code runs against a global request object `r` (no wrapper function):

```javascript
// Convert a generic JSON webhook into a Slack message.
const data = JSON.parse(r.body)
r.setBody(JSON.stringify({ text: "New event: " + (data.message || "n/a") }))
r.setHeader("Content-Type", "application/json")
```

Read: `r.body`, `r.method`, `r.path`, `r.headers`, `r.query`, `r.formData`.
Mutate the forwarded request: `r.setBody`, `r.setHeader`/`r.deleteHeader`,
`r.setMethod`, `r.setPath`, `r.setRawQuery`. Control the response:
`r.setResponseStatus`, `r.setResponseBody`, `r.setResponseHeader`. Drop a
request with `r.stopForwarding()`. Read secrets with `cfg.get("KEY")`. Always
`JSON.stringify` before `r.setBody`.

```bash
relay function test   -f spec.yaml -v                 # test locally (set driver: js)
relay function create --name to-slack --driver js --source to-slack.js
relay output create   -b to-slack --type public -d https://hooks.slack.com/services/… \
  --function to-slack                                  # attach to an output
```

### Schedule recurring (cron) webhooks

A **cron** fires a webhook on a schedule (5-field cron expression + IANA
timezone). Good for heartbeats, scheduled reports, and timed reminders.

```bash
relay cron create hourly-ping \
  --schedule "0 * * * *" --timezone "Europe/London" \
  --method POST --destination https://example.com/webhook \
  --payload '{"ping":"hourly"}' --header Content-Type=application/json

relay cron ls
relay cron update hourly-ping --enabled=false   # pause without deleting
relay cron rm hourly-ping
```

`payload` is a string (JSON-encode objects). Attach a function with
`--function` to build/sign the payload at send time. Manage in the dashboard at
https://my.webhookrelay.com/cron, or via the REST API with `relay api /v1/crons`.

---

## Verify

- **Forwarding (internal):** start a throwaway server (`python3 -m http.server
  8080`), run `relay forward -b my-app http://localhost:8080`, then
  `curl -X POST https://my.webhookrelay.com/v1/webhooks/<id> -d '{"hi":1}'` and
  watch the agent log + local server receive it.
- **Tunnel:** open the printed `https://<host>` in a browser; requests appear in
  the agent's terminal. Connection errors usually mean the local service is down
  or `--rewrite-host-header` doesn't match what the app expects.
- **Bin:** `BIN=$(curl -s -X POST $B/v1/bins | jq -r .id); curl -s -X POST
  "$B/v1/webhooks/$BIN" -d '{"smoke":1}'; curl -s "$B/v1/bins/$BIN" | jq
  '.requests | length'` should be `>= 1`.

The dashboard at https://my.webhookrelay.com shows buckets, delivery logs, and
lets you replay/retry failed deliveries.

## Best practices

- Give providers the **public input URL**, never `localhost`.
- Choose the output type deliberately: **internal** needs the agent running;
  **public** is delivered server-side with no agent. A single bucket can mix both.
- Reuse a stable `--bucket` / tunnel `--name` to keep the same public URL across
  restarts.
- Keep secrets in function `cfg.get(...)`, not in source; never send secrets to a
  bin (it's public and temporary).
- Use a bin or https://webhook.site to inspect payloads while wiring up a real
  provider, then switch the destination to your real handler.

## References

Plain-markdown docs (append `.md` to most pages to read directly):

- Docs index: https://webhookrelay.com/llms.txt
- Install the CLI: https://webhookrelay.com/docs/installation/cli.md
- Receive webhooks on localhost / private networks:
  https://webhookrelay.com/docs/webhooks/internal/localhost.md
- Forward to a public URL:
  https://webhookrelay.com/docs/webhooks/public/public-destination.md —
  multiple destinations:
  https://webhookrelay.com/docs/webhooks/public/multiple-destination-urls.md
- Tunnels overview: https://webhookrelay.com/tunnels.md — regions:
  https://webhookrelay.com/docs/tunnels/regions.md
- Transformation functions: https://webhookrelay.com/docs/webhooks/functions.md
- Recurring (cron) webhooks:
  https://webhookrelay.com/docs/webhooks/cron/using-cron-webhooks.md
- Webhook bin (debugging) agent guide: https://webhookrelay.com/webhook-bin.md
- Forwarding rules (filter & route):
  https://webhookrelay.com/features/forwarding-rules.md
- Custom subdomains: https://webhookrelay.com/docs/webhooks/custom-subdomains.md
  — custom domains: https://webhookrelay.com/docs/webhooks/custom-domains.md
