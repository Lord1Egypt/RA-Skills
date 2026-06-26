---
name: api-integrator
description: API integration and automation skill for connecting services, webhooks, and third-party platforms. Use when integrating APIs, building webhooks, syncing data between services, or creating custom API clients. Supports REST, GraphQL, and authentication flows.
---

# API Integrator

## Overview

Professional API integration skill for OpenClaw. Connect and automate workflows between multiple services, handle authentication, manage rate limits, and build custom API clients.

## Features

- REST API testing
- OAuth 2.0/Bearer/Basic auth support
- API client code generation (Python/JavaScript)
- Rate limit handling
- Auto-retry on 429

## Quick Start

### Test API Endpoint

```bash
python scripts/api_client.py --action test --url "https://api.example.com/users" --method GET --auth bearer --token YOUR_TOKEN
```

### Generate API Client

```bash
python scripts/api_client.py --action create-client --name myapi --base-url "https://api.example.com" --language python
```

## Scripts

### api_client.py

Test APIs and generate client code.

**Actions:**
- `test` - Test API endpoint
- `create-client` - Generate API client code
- `webhook-test` - Test webhook receiver

**Arguments:**
- `--action` - Action to perform
- `--url` - API endpoint URL
- `--method` - HTTP method
- `--auth` - Authentication type (none, bearer, basic, api_key)
- `--token` - Auth token/API key
- `--name` - Client name (for create-client)
- `--base-url` - API base URL
- `--language` - Output language (python, javascript)
- `--output` - Output file path

## Authentication Methods

### API Key

```python
headers = {
    "X-API-Key": "your_api_key"
}
```

### Bearer Token

```python
headers = {
    "Authorization": f"Bearer {access_token}"
}
```

### OAuth 2.0

```python
# Get access token
token_url = "https://auth.example.com/oauth/token"
data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}
response = requests.post(token_url, data=data)
access_token = response.json()["access_token"]
```

### Basic Auth

```python
import base64
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {
    "Authorization": f"Basic {credentials}"
}
```

## Common Integrations

### E-commerce Platforms

| Platform | API Docs | Auth Type |
|----------|----------|-----------|
| Taobao | https://open.taobao.com | OAuth 2.0 |
| Douyin | https://open.douyin.com | OAuth 2.0 |
| Shopify | https://shopify.dev/api | API Key |
| WooCommerce | https://woocommerce.github.io | OAuth 1.0a |

### Payment Processors

| Platform | API Docs | Auth Type |
|----------|----------|-----------|
| Stripe | https://stripe.com/docs/api | Bearer Token |
| PayPal | https://developer.paypal.com | OAuth 2.0 |
| Alipay | https://opendocs.alipay.com | RSA Key |

### Communication

| Platform | API Docs | Auth Type |
|----------|----------|-----------|
| SendGrid | https://docs.sendgrid.com | Bearer Token |
| Twilio | https://www.twilio.com/docs | Basic Auth |
| Slack | https://api.slack.com | Bearer Token |

## Rate Limiting

### Built-in Rate Limit Handling

```bash
python scripts/sync_data.py \
  --source stripe \
  --target shopify \
  --rate-limit 100/minute \
  --retry-on-429 true
```

### Rate Limit Strategies

- **Fixed window**: N requests per minute
- **Sliding window**: Smooth distribution
- **Token bucket**: Burst allowance
- **Exponential backoff**: Retry with increasing delays

## Error Handling

### Common HTTP Errors

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Bad Request | Fix request parameters |
| 401 | Unauthorized | Check authentication |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Verify endpoint/ID |
| 429 | Too Many Requests | Wait and retry |
| 500 | Server Error | Retry with backoff |
| 503 | Service Unavailable | Retry later |

### Retry Logic

```python
import time
from requests.exceptions import RequestException

def api_request_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
```

## Best Practices

1. **Use environment variables** for API keys and secrets
2. **Implement rate limiting** to avoid API bans
3. **Cache responses** when appropriate
4. **Log all API calls** for debugging
5. **Handle errors gracefully** with retries
6. **Validate responses** before processing
7. **Use webhooks** instead of polling when possible

## Security

- Never commit API keys to version control
- Use HTTPS for all API calls
- Rotate keys periodically
- Implement request signing for webhooks
- Validate webhook signatures

## Troubleshooting

- **401 Unauthorized**: Check token expiration, refresh if needed
- **403 Forbidden**: Verify API permissions and scopes
- **429 Rate Limited**: Implement backoff, reduce request frequency
- **Timeout errors**: Increase timeout, add retries
- **Invalid response**: Check API version, validate schema
