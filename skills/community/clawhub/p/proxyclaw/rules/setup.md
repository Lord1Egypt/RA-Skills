# ProxyClaw Setup Guide

## Prerequisites

- `curl` installed (comes pre-installed on most systems)
- `IPLOOP_API_KEY` environment variable set

## Getting Your API Key

1. Sign up at [iploop.io/signup](https://iploop.io/signup.html)
2. Copy your API key from the dashboard
3. Use code **`OPENCLAW`** for 20% off any paid plan

```bash
export IPLOOP_API_KEY="your_api_key_here"
```

To make it permanent, add to your shell profile:
```bash
echo 'export IPLOOP_API_KEY="your_api_key"' >> ~/.bashrc
source ~/.bashrc
```

## Verify Connection

```bash
./setup.sh
```

Expected output:
```
✅ IPLOOP_API_KEY is set
✅ Proxy connection successful
✅ ProxyClaw is ready
```

## Markdown Output

For markdown-formatted output, install:
```bash
npm install -g node-html-markdown
```

Then use:
```bash
./fetch.sh https://example.com --format markdown
```

## Proxy Endpoint

All requests route through: `proxy.iploop.io:8880`

Format: `http://iploop:API_KEY[-options]@proxy.iploop.io:8880`

## Troubleshooting

### Connection timeout
- Check if `IPLOOP_API_KEY` is set correctly
- Verify your free tier hasn't been exhausted (0.5 GB limit)
- Try without country targeting first

### 403 / blocked
- Try a different country: `--country US` or `--country DE`
- Some sites require browser automation (Puppeteer/Playwright)

### Invalid country code
- Must be exactly 2 uppercase letters (ISO 3166-1 alpha-2)
- Examples: US, GB, DE, FR, JP, BR, CA, AU

### Rate limit (429)
- Add delays between requests: `sleep 1` between calls
- Upgrade to a higher tier for more req/min

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `IPLOOP_API_KEY` | ✅ Yes | Your IPLoop API key |

## Network Destinations

- `proxy.iploop.io:8880` — HTTP/HTTPS proxy gateway
- `iploop.io` — API and auth endpoints
- User-specified target URLs
