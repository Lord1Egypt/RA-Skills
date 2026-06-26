# x402-x-tweet-fetcher

Buy Xcatcher points via x402 on Solana USDC, obtain an API key, create X crawl tasks, poll status, and download XLSX results.

## Overview

`x402-x-tweet-fetcher` is an OpenClaw skill for paid X data collection through Xcatcher.

It supports the full workflow:

1. request a live x402 quote,
2. pay in Solana USDC,
3. exchange payment proof for an API key,
4. create X crawl tasks,
5. poll task status,
6. download XLSX output.

Website:
- https://xcatcher.top/docs/

Service base:
- https://xcatcher.top
- https://xcatcher.top/api/v1

## Best fit

This skill is intended for:
- OpenClaw users,
- remote agents,
- automation workflows,
- analysts who need structured XLSX exports from X account crawl tasks.

## Capabilities

- x402 quote retrieval
- Solana USDC payment flow
- API key issuance after successful payment
- task creation
- task polling
- authenticated XLSX download

## Requirements

Required binaries:
- `curl`
- `jq`
- `base64`

Recommended:
- `python3`

## Authentication model

You do not need an API key to start the top-up flow.

After a successful `buy_points` request, the service returns an API key.  
Set it like this:

```bash
export XCATCHER_API_KEY="your_api_key"
```

Use that Bearer token for:
- `/api/v1/me`
- `/api/v1/tasks`
- `/api/v1/tasks/{task_id}`
- `/api/v1/tasks/{task_id}/download`

## Pricing

Task pricing:
- `normal`: 1 point per user
- `deep`: 10 points per user

Estimated cost:
- `users_count × 1` for `normal`
- `users_count × 10` for `deep`

> Always trust the live quote response for payment amount. Do not hardcode USDC conversion assumptions.

## Typical flow

### 1. Get quote

```bash
curl -sS "https://xcatcher.top/api/v1/x402/quote?points=1" | jq .
```

### 2. Pay on Solana

Send the required SPL USDC amount to the `accepts.solana.payTo` address returned by the quote.

### 3. Exchange payment proof for API key

Submit:
- `quote_id`
- `PAYMENT-SIGNATURE` header

Receive:
- `api_key`

### 4. Create task

Submit:
- `mode`
- `users`
- `idempotency_key`

Receive:
- `task_id`

### 5. Poll and download result

Poll task status until:
- `download_url` exists, or
- `result_path` exists

Then download the XLSX file with the same Bearer token.

## Error handling

- `401` → token missing or invalid
- `402` → quote expired or payment proof invalid
- `429` → rate limit
- delayed task → poll again with backoff

## Publish to ClawHub

Example:

```bash
clawhub publish ./x402-x-tweet-fetcher \
  --slug x402-x-tweet-fetcher \
  --name "X402 X Tweet Fetcher" \
  --version 1.0.0 \
  --tags latest
```

## License

Proprietary or private distribution, depending on your release policy.
Replace this section if you want an explicit public license.
