---
name: space-router
description: Route HTTP traffic through Space Router residential IP proxy network.
metadata: {"openclaw": {"requires": {"env": ["SPACE_ROUTER_PROXY_URL"]}, "primaryEnv": "SPACE_ROUTER_PROXY_URL"}}
---

# Space Router — Residential IP Proxy Routing

Route your HTTP requests through residential IP addresses via Space Router's forward proxy.

## Setup

The environment variable `SPACE_ROUTER_PROXY_URL` must contain your full proxy URL including API key credentials:

```
SPACE_ROUTER_PROXY_URL=https://sr_live_YOUR_API_KEY@gateway.spacerouter.org
```

The default gateway is `https://gateway.spacerouter.org` (port 443). For local development the host is typically `localhost:8080`.

## When to Use This Skill

Use Space Router when a task requires any of the following:

- Accessing a website that blocks datacenter IPs or cloud provider IP ranges
- Web scraping where you need residential IP rotation
- The user explicitly asks you to route traffic through a residential proxy
- A previous HTTP request failed with a 403 or CAPTCHA challenge suggesting IP-based blocking
- The user says to use "Space Router", "residential proxy", or "residential IP"

Do NOT route through the proxy when:

- Accessing local services (localhost, 127.0.0.1, internal hostnames)
- Accessing APIs that authenticate by IP allowlist (the residential IP will not be allowlisted)
- The user explicitly says to make a direct request

## How to Route Traffic

### Python SDK (recommended for Python)

```bash
pip install spacerouter
```

```python
from spacerouter import SpaceRouter

with SpaceRouter("sr_live_YOUR_API_KEY") as client:
    resp = client.get("https://example.com")
    print(resp.status_code, resp.request_id)
```

Async usage:

```python
from spacerouter import AsyncSpaceRouter

async with AsyncSpaceRouter("sr_live_YOUR_API_KEY") as client:
    resp = await client.get("https://example.com")
    print(resp.status_code, resp.request_id)
```

### JavaScript/TypeScript SDK (recommended for Node.js)

```bash
npm install @spacenetwork/spacerouter
```

```ts
import { SpaceRouter } from "@spacenetwork/spacerouter";

const client = new SpaceRouter("sr_live_YOUR_API_KEY");
const resp = await client.get("https://example.com");
console.log(resp.status, resp.requestId);
client.close();
```

### CLI (for shell scripts and quick tasks)

```bash
pip install spacerouter-cli
spacerouter config set api-key sr_live_YOUR_API_KEY
spacerouter request get https://example.com
```

Other useful CLI commands:

```bash
spacerouter status                    # Check service health
spacerouter api-key list              # List API keys
spacerouter node list                 # List proxy nodes
spacerouter request get https://httpbin.org/ip --region US
```

### curl / environment variables

Set `HTTP_PROXY` and `HTTPS_PROXY` so all HTTP clients in the shell session use the proxy automatically:

```bash
export HTTP_PROXY="$SPACE_ROUTER_PROXY_URL"
export HTTPS_PROXY="$SPACE_ROUTER_PROXY_URL"
```

Or pass the proxy explicitly to curl:

```bash
curl -x "$SPACE_ROUTER_PROXY_URL" https://httpbin.org/ip
```

## Region Targeting

Route requests through residential IPs in a specific country using ISO 3166-1 alpha-2 codes (e.g. `US`, `KR`, `JP`, `DE`):

**Python:**

```python
client = SpaceRouter("sr_live_xxx", region="US")

# Change region on the fly (returns a new client)
jp_client = client.with_routing(region="JP")
```

**JavaScript:**

```ts
const client = new SpaceRouter("sr_live_xxx", { region: "US" });
const jpClient = client.withRouting({ region: "JP" });
```

**curl:**

```bash
curl -x "$SPACE_ROUTER_PROXY_URL" -H "X-SpaceRouter-Region: US" https://httpbin.org/ip
```

## IP Type Filtering

Filter proxy nodes by IP address type: `residential`, `mobile`, `datacenter`, or `business`.

**Python:**

```python
client = SpaceRouter("sr_live_xxx", ip_type="mobile")
```

**JavaScript:**

```ts
const client = new SpaceRouter("sr_live_xxx", { ipType: "mobile" });
```

## SOCKS5 Support

Both SDKs support SOCKS5 as an alternative proxy protocol (default port 1080):

**Python:**

```python
pip install spacerouter[socks]

client = SpaceRouter("sr_live_xxx", protocol="socks5", gateway_url="socks5://gateway:1080")
```

**JavaScript:**

```ts
const client = new SpaceRouter("sr_live_xxx", {
  protocol: "socks5",
  gatewayUrl: "socks5://gateway:1080",
});
```

## Verifying the Proxy Works

After configuring the proxy, confirm that traffic is routed through a residential IP:

```bash
curl -x "$SPACE_ROUTER_PROXY_URL" https://httpbin.org/ip
```

The returned IP should differ from your machine's public IP. You can also run the verification script:

```bash
bash {baseDir}/scripts/verify-proxy.sh
```

## Error Handling

The SDKs raise typed exceptions for proxy-layer errors:

| Exception | HTTP Status | Meaning | What to Do |
|---|---|---|---|
| `AuthenticationError` | 407 | API key missing or invalid | Check that the API key has prefix `sr_live_` |
| `RateLimitError` | 429 | Rate limit exceeded | Wait `retry_after` seconds and retry |
| `UpstreamError` | 502 | Residential node could not reach target | Retry; the proxy will try a different node |
| `NoNodesAvailableError` | 503 | No residential nodes available | Wait and retry; nodes may be temporarily offline |

**Python example:**

```python
from spacerouter import SpaceRouter, RateLimitError
import time

with SpaceRouter("sr_live_xxx") as client:
    try:
        resp = client.get("https://example.com")
    except RateLimitError as e:
        time.sleep(e.retry_after)
```

**JavaScript example:**

```ts
import { SpaceRouter, RateLimitError } from "@spacenetwork/spacerouter";

const client = new SpaceRouter("sr_live_xxx");
try {
  const resp = await client.get("https://example.com");
} catch (e) {
  if (e instanceof RateLimitError) {
    await new Promise((r) => setTimeout(r, e.retryAfter * 1000));
  }
}
```

## Response Headers

Space Router adds these headers to proxied responses:

| Header | Meaning |
|---|---|
| `X-SpaceRouter-Request-Id` | Unique request ID for debugging |

Routing headers sent on the proxy CONNECT request:

| Header | Meaning |
|---|---|
| `X-SpaceRouter-Region` | Target region (2-letter country code) |
| `X-SpaceRouter-IP-Type` | Target IP type (residential, mobile, etc.) |

## Important Notes

- The default gateway is `https://gateway.spacerouter.org` (HTTPS, port 443). The proxy establishes a CONNECT tunnel for TLS traffic — your end-to-end encryption is preserved.
- When using the `SPACE_ROUTER_PROXY_URL` env var with curl, the URL scheme may be HTTP even for HTTPS targets. The proxy handles TLS tunneling.
- Do not put the proxy URL in `NO_PROXY` or bypass lists.
- API keys have the prefix `sr_live_` and are passed as the username in the proxy URL (password is empty).
- Rate limits are per API key, default 60 requests per minute.
- The Python SDK requires Python >= 3.10. The JS SDK requires Node.js >= 18.
