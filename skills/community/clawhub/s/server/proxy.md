# The Request Path — Proxying, Headers, Timeouts, Streams

Everything between the client's TCP connection and the app's handler. Directive-level nginx questions belong to the `nginx` skill and Caddyfile syntax to `caddy`; this file is the behavior that has to be right whichever proxy is in front.

**Before editing a route**, read `## Services` in `~/Clawic/data/server/memory.md` (or `services.md` if `## Boxes` points there) for the upstream's real listen address, and `~/Clawic/data/domains/domains.md` for what the hostname is already pointing at. Two vhosts claiming one hostname is a coin flip decided by file order.

**Contents:** [The Minimum Correct Proxy](#the-minimum-correct-proxy) · [Headers That Must Be Right](#headers-that-must-be-right) · [Trusting Forwarded Headers](#trusting-forwarded-headers) · [The Timeout Ladder](#the-timeout-ladder) · [Keepalive, Both Directions](#keepalive-both-directions) · [Path Rewriting](#path-rewriting) · [Buffering](#buffering) · [WebSockets](#websockets) · [Server-Sent Events](#server-sent-events) · [gRPC and HTTP/2](#grpc-and-http2) · [Load Balancing Across Upstreams](#load-balancing-across-upstreams) · [Retries That Duplicate Writes](#retries-that-duplicate-writes) · [Rate Limiting](#rate-limiting) · [Redirect Loops](#redirect-loops) · [Write It Down](#write-it-down)

## The Minimum Correct Proxy

```nginx
server {
    listen 443 ssl;
    http2 on;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host  $host;

        proxy_read_timeout 30s;
        proxy_send_timeout 30s;
    }
}
```

```caddyfile
example.com {
	reverse_proxy 127.0.0.1:8000
}
```

Caddy sets the forwarded headers, uses HTTP/1.1 upstream, and obtains the certificate on its own — the nginx block above is the same behavior written out. Everything else in this file applies to both.

`proxy_http_version 1.1` is not optional in nginx: the default is 1.0, which disables keepalive to the upstream and breaks WebSocket upgrades. Two of the most common "mysterious" proxy problems are one missing line.

## Headers That Must Be Right

| Header | Wrong value causes |
|---|---|
| `Host` | The app generates links with the upstream's address, cookies get the wrong domain, and virtual-host routing on the app side picks the wrong site. `$host`, not `$proxy_host` |
| `X-Forwarded-Proto` | The app believes it is on HTTP, redirects to HTTPS, the proxy forwards the redirect, and the browser loops (below) |
| `X-Forwarded-For` | Every log line and rate limit sees the proxy's IP; abuse becomes invisible and per-IP limits throttle everyone at once |
| `X-Forwarded-Host` / `X-Forwarded-Port` | Absolute URLs in redirects and emails come out with the internal port |
| `Connection` / `Upgrade` | WebSocket and HTTP/2 upgrades fail with a 400 or hang |
| `Accept-Encoding` stripped upstream | The app compresses, the proxy compresses again, or neither does |

`Forwarded:` (RFC 7239) is the standard replacement for the `X-` family; send it *in addition* while any component still reads the old ones, never instead.

## Trusting Forwarded Headers

A forwarded header is a claim by whoever sent it. If the app trusts it unconditionally, any client can set `X-Forwarded-For: 1.2.3.4` and defeat every per-IP control you have.

- **Proxy side**: overwrite, do not append, at the outermost trusted hop. nginx's `realip` module (`set_real_ip_from <proxy CIDR>; real_ip_header X-Forwarded-For;`) rewrites `$remote_addr` to the real client, and only for connections from the listed sources.
- **App side**: every framework has an explicit allowlist — Express `app.set('trust proxy', '127.0.0.1')`, Django `SECURE_PROXY_SSL_HEADER` plus a middleware that knows the hop count, Rails `config.action_dispatch.trusted_proxies`. Setting these to "trust everything" is the same bug one layer down.
- Behind a CDN, the trusted source is the CDN's published IP ranges, and the header carrying the real client is usually the CDN's own (`CF-Connecting-IP` and equivalents), not `X-Forwarded-For`.
- Count the hops. Two proxies in series means `X-Forwarded-For` has two entries and "the client" is the leftmost — unless a hop appended instead of overwriting, in which case the leftmost is whatever the client made up.

## The Timeout Ladder

Shortest on the inside (SKILL.md Rule 3). A working set:

| Hop | Setting | Value |
|---|---|---|
| Database | statement timeout | 5s |
| App | request timeout / worker timeout | 15s |
| Proxy | `proxy_read_timeout` | 30s |
| Client/LB | idle timeout | 60s |

Why the order matters: with the app at 60s and the proxy at 30s, every slow request becomes a 504 with **no application log line** — the app is still working on a request nobody is waiting for, holding a worker, when the proxy has already answered. Invert it and the app logs a timeout with a stack trace pointing at the slow dependency, which is the whole point.

Exceptions get their own location, never a global raise: an export endpoint that legitimately takes two minutes gets `proxy_read_timeout 180s` on `/export` alone. Raising the global read timeout to accommodate one route means every hung request now occupies a connection for three minutes.

`proxy_connect_timeout` is separate and should stay small (2-5s): failing to *establish* a connection to a local upstream in 5 seconds means the upstream is down, and waiting longer only delays the 502.

## Keepalive, Both Directions

- **Client → proxy**: `keepalive_timeout 75s` (nginx default). Longer keeps connections open for repeat visitors; shorter frees worker slots. Rarely worth changing.
- **Proxy → upstream**: must be *declared* in nginx (`upstream { server 127.0.0.1:8000; keepalive 32; }` plus `proxy_http_version 1.1` and `proxy_set_header Connection "";`). Without it, every request is a new TCP handshake and a new ephemeral port (`workers.md`).
- **The upstream's own idle timeout must be longer than the proxy's** (Rule 4). Node defaults to 5s, Gunicorn to 2s — both below any proxy default, both producing intermittent 502s that appear only under load and vanish when you go looking. Set the app's keepalive to the proxy's value plus a few seconds and the class of bug disappears.

## Path Rewriting

The trailing slash in `proxy_pass` decides whether the location prefix is stripped:

```nginx
location /api/ { proxy_pass http://127.0.0.1:8000/; }   # /api/users → /users
location /api/ { proxy_pass http://127.0.0.1:8000;  }   # /api/users → /api/users
```

One character, two different applications. If the app returns 404 for every route behind a prefix, this is the first thing to check; if it returns 200 but every generated link is missing the prefix, the app needs to be told its base path (`SCRIPT_NAME`, `--root-path`, `basePath`) rather than having the proxy lie to it.

Mounting an app at a subpath is genuinely harder than giving it a subdomain: cookies, absolute asset URLs, redirects, and WebSocket paths all have to agree. Prefer a subdomain unless something forces the subpath (`selfhosted.md`).

## Buffering

nginx buffers request and response bodies by default, and that default is usually right:

- **Request buffering on** protects slow-worker runtimes from slow clients — the proxy absorbs a 30-second mobile upload and hands the app a complete request in milliseconds (`workers.md`).
- **Turn response buffering off** (`proxy_buffering off`) for streams: SSE, log tailing, progress endpoints. Otherwise the proxy holds output until a buffer fills and the "live" feed arrives in bursts.
- **Turn request buffering off** (`proxy_request_buffering off`) for very large uploads you want streamed straight through, accepting that a slow client now occupies an app worker for the duration.
- Buffers that overflow spill to `proxy_temp_path` on disk. A full or read-only temp directory truncates responses at a size, not a time — the tell is that small responses work and large ones do not (`static.md`).

## WebSockets

```nginx
location /ws {
    proxy_pass http://127.0.0.1:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade    $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 3600s;
}
```

- Without the two upgrade headers the handshake returns 400 or falls back to long-polling — which looks like it works, until the connection count explodes.
- The read timeout closes *idle* tunnels: a chat app with 60 seconds of silence drops at the default 60s. Raise it on this location only, and send application-level pings (every 30s) so intermediaries and mobile NAT keep the path open.
- Sticky sessions are required if the app keeps per-connection state in memory and there is more than one upstream — or move the state to a shared pub/sub backend, which is the fix that keeps working as you add boxes.

## Server-Sent Events

`proxy_buffering off` and `X-Accel-Buffering: no` from the app, `proxy_read_timeout` above the longest expected gap between events, and a heartbeat comment (`: ping\n\n`) every 15-30s. Compression must be off for the SSE route: a compressor with a flush buffer holds events until it has enough bytes, which is indistinguishable from a hung server.

## gRPC and HTTP/2

- Client → proxy over HTTP/2 is orthogonal to proxy → upstream: nginx speaks HTTP/1.1 upstream unless the location uses `grpc_pass`, and gRPC requires HTTP/2 end to end.
- `grpc_pass grpc://127.0.0.1:50051;` with `grpc_read_timeout` sized for streaming calls; a unary-sized timeout kills long streams.
- HTTP/3 needs UDP 443 open in every firewall on the path and an `Alt-Svc` advertisement; browsers only try it after being told. If HTTP/3 "does not work", the UDP rule is missing far more often than the config is wrong.
- HTTP/2 to the browser removes the reason for domain sharding and asset concatenation; keeping those workarounds now costs cache efficiency (`static.md`).

## Load Balancing Across Upstreams

| Method | Use when |
|---|---|
| Round-robin (default) | Requests are uniform and upstreams identical |
| `least_conn` | Request durations vary — the common real case, and the better default for app servers |
| Hash on a key (`ip_hash`, `hash $cookie_session`) | State lives in the upstream and cannot be moved yet |
| Weighted | Upstreams have genuinely different capacity, e.g. during a migration |

Health checks: passive by default in open-source nginx (`max_fails`, `fail_timeout`) — an upstream is marked down only after real requests fail, so the first users after a crash get the errors. `backup` servers only receive traffic when every primary is down, which makes them useless as spare capacity and excellent as a maintenance page.

Draining a node before a deploy means removing it from the upstream and reloading, waiting out the in-flight requests, then stopping it. Stopping it first is how you turn a deploy into 30 seconds of 502s.

## Retries That Duplicate Writes

`proxy_next_upstream` retries a failed request on the next upstream. By default that includes `error` and `timeout` — and a timeout can mean the upstream *received and processed* the request and was merely slow to answer. Retrying a POST in that state charges the card twice.

Rule: `proxy_next_upstream error timeout http_502 http_503;` for idempotent methods, and `proxy_next_upstream off;` (or `non_idempotent` deliberately excluded) on routes that write. The safe general setting is to let nginx retry only what it retries by default for safe methods, and to make write endpoints idempotent with a client-supplied key.

## Rate Limiting

nginx's `limit_req` is a leaky bucket, not a token bucket: `rate=10r/s` means one request each 100ms, and a legitimate burst of 5 simultaneous requests from one page load is rejected unless `burst=` allows it.

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api/ { limit_req zone=api burst=20 nodelay; }
```

`burst` without `nodelay` queues and delays; with `nodelay` it allows the burst immediately and refills at the rate. A 10 MB zone holds roughly 160,000 IPv4 states. Rate limit on the real client IP — which only exists if forwarded headers are handled correctly (above), otherwise the limit applies to the CDN and takes the whole site down at once.

Return 429 with `limit_req_status 429;`; the default 503 tells clients the server is broken and encourages retries.

## Redirect Loops

The canonical loop: the proxy terminates TLS and forwards plain HTTP; the app sees HTTP, redirects to HTTPS; the browser comes back over HTTPS; the proxy forwards HTTP again. Infinite.

Fix at both ends: send `X-Forwarded-Proto: $scheme` **and** configure the app to trust it (Django `SECURE_PROXY_SSL_HEADER`, Express `trust proxy`, Rails `assume_ssl`). Fixing only one side leaves the loop.

Second most common: two redirect rules (proxy adds `www`, app removes it) fighting. Decide the canonical host once, implement it in exactly one place, and make the other side a no-op.

## Write It Down

A route that took work to get right — a subpath mount, a WebSocket location with a raised timeout, an upstream keepalive that fixed intermittent 502s — goes to `~/Clawic/data/server/artifacts/working-vhost-<service>.md`, with a one-line reason next to each non-default value and its `## Boxes` line in `memory.md` the same turn. The hostname → service mapping goes in `## Services` (vhost column) and in the shared `~/Clawic/data/domains/domains.md` (`memory-template.md`). A timeout ladder you set deliberately belongs in `## Baselines` — the next person to raise one value needs to see the other three.
