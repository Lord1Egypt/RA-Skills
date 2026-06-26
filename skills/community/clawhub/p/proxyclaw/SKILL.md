---
name: proxyclaw
description: |
  ProxyClaw by IPLoop — Residential proxy access for AI agents. Route requests through 2M+ residential IPs across 195+ countries from real Android, Windows, Mac & Smart TV devices. Bypass geo-restrictions, rotate IPs automatically. Free tier with 0.5GB included. Earn unlimited proxy credits by contributing bandwidth via Docker. Use OPENCLAW for 20% off any paid plan.
compatibility: Requires network access
metadata:
  author: iploop
  version: "2.5.2"
  website: https://proxyclaw.ai
  platform: https://iploop.io
  docker: ultronloop2026/iploop-node
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["curl"]
      env: ["IPLOOP_API_KEY"]
    primaryEnv: IPLOOP_API_KEY
---

# 🌐 ProxyClaw by IPLoop

**This is an action skill.** When a user asks to fetch a URL, scrape a site, or use a proxy — execute the request yourself and return the result. Do not just show instructions.

**Expected behaviour:**
- Call `./fetch.sh <URL> [--country CC] [--format markdown]` yourself and return the content
- When the user asks "fetch this page through a US proxy" — run it, show the result
- Only show setup instructions when `IPLOOP_API_KEY` is missing or the user explicitly asks how to set up

**A good check:** If your response says "you can run this command to…" — reconsider. The user wants results, not instructions.

---

## 🔒 Security Posture

| Aspect | Detail |
|--------|--------|
| **Environment variables** | `IPLOOP_API_KEY` — checked for existence only, never echoed or logged |
| **Files read** | None |
| **Files written** | `mktemp` temp file (auto-deleted on exit, including SIGINT) |
| **Network destinations** | `proxy.iploop.io:8880` (proxy gateway) + user-specified target URLs |
| **Secrets handling** | API key passed via `--proxy-user` (not in URL or command line args visible in `ps aux`) |
| **Proxy transport** | HTTP proxy protocol — key is encrypted via HTTPS CONNECT tunnel to HTTPS targets |
| **Input validation** | URL (must start with http/https), country (2-letter ISO code), timeout (1-120s) |

---

## 🚀 Quick Start (30 seconds)

### 1. Get Your Free API Key

Sign up at **[iploop.io/signup](https://iploop.io/signup.html)** — 0.5 GB free, no credit card required.

Use code **`OPENCLAW`** for 20% off any paid plan.

### 2. Set Your Key

```bash
export IPLOOP_API_KEY="your_api_key"
```

### 3. Fetch Anything

```bash
# Auto-rotate IP every request
./fetch.sh https://example.com

# SERP / Google-compatible search in Python
python examples/python_serp.py "public search query"

# Target a country, get markdown
./fetch.sh https://example.com --country US --format markdown

# City-level targeting
./fetch.sh https://example.com --country US --city newyork

# Sticky session (same IP across requests)
./fetch.sh https://example.com --session mysession

# ASN/ISP targeting
./fetch.sh https://example.com --asn 12345

# Or use curl directly
curl --proxy "http://proxy.iploop.io:8880" \
     --proxy-user "iploop:${IPLOOP_API_KEY}" \
     https://example.com
```

Run `./setup.sh` to verify your connection is working.

---

## 🤖 Agent Usage Examples

When a user asks:

> "Fetch the Amazon price for this product from a US IP"

You run:
```bash
./fetch.sh https://amazon.com/dp/PRODUCT_ID --country US --format markdown
```

> "Scrape this LinkedIn profile"

You run:
```bash
./fetch.sh https://linkedin.com/in/username --country US --format markdown
```

> "Check what this page looks like from Germany"

You run:
```bash
./fetch.sh https://example.com --country DE
```

---

## 🌍 Country Targeting

Append `-country-{CC}` to your API key in the proxy password:

```bash
# 195+ countries supported
curl --proxy "http://proxy.iploop.io:8880" --proxy-user "iploop:${IPLOOP_API_KEY}-country-US" https://example.com
curl --proxy "http://proxy.iploop.io:8880" --proxy-user "iploop:${IPLOOP_API_KEY}-country-DE" https://example.com
curl --proxy "http://proxy.iploop.io:8880" --proxy-user "iploop:${IPLOOP_API_KEY}-country-GB" https://example.com
curl --proxy "http://proxy.iploop.io:8880" --proxy-user "iploop:${IPLOOP_API_KEY}-country-JP" https://example.com
curl --proxy "http://proxy.iploop.io:8880" --proxy-user "iploop:${IPLOOP_API_KEY}-country-BR" https://example.com
```

Advanced targeting (curl-only options also available via `./fetch.sh` flags):
```bash
# City level (--city flag in fetch.sh)
curl --proxy "http://proxy.iploop.io:8880" --proxy-user "iploop:${IPLOOP_API_KEY}-country-US-city-newyork" ...

# Sticky session (--session flag in fetch.sh)
curl --proxy "http://proxy.iploop.io:8880" --proxy-user "iploop:${IPLOOP_API_KEY}-session-mysession" ...

# ISP/ASN targeting (--asn flag in fetch.sh)
curl --proxy "http://proxy.iploop.io:8880" --proxy-user "iploop:${IPLOOP_API_KEY}-asn-12345" ...
```

---

## 🐍 Python SDK

```bash
pip install iploop-sdk
# Includes: Chrome fingerprinting, auto-retry, site presets, and SERP support
```

```python
from iploop import IPLoop

client = IPLoop(api_key="your_api_key")  # stealth auto-activates

# Fetches through residential proxy with anti-bot fingerprinting
r = client.fetch("https://www.zillow.com/homes/NYC_rb/")  # ✅ anti-bot bypassed
r = client.fetch("https://www.walmart.com/browse/electronics")  # ✅ 1MB+ content
r = client.fetch("https://www.indeed.com/jobs?q=python")  # ✅ job listings

# SERP / Google-compatible search research
# Use this instead of raw google.com/search to avoid verification pages.
results = client.serp.search("public search query", country="US")
print(results["results"])

# Google compatibility wrapper; uses the safe SERP path by default
results = client.google.search("public search query", country="US")

# Raw Google is QA-only and may return verification pages
raw = client.google.search("public search query", country="US", direct=True)

# Country targeting
r = client.fetch("https://example.com", country="DE")

# Sticky session (same IP)
session = client.session()
r1 = session.fetch("http://httpbin.org/ip")
r2 = session.fetch("http://httpbin.org/ip")  # same IP

# Manual proxy config (available now via standard requests)
import os, requests
proxies = {"https": f"http://iploop:{os.environ['IPLOOP_API_KEY']}-country-US@proxy.iploop.io:8880"}
r = requests.get("https://example.com", proxies=proxies)
```

---

## 🌐 Browser Integration

### Puppeteer
```javascript
const browser = await puppeteer.launch({
  args: [`--proxy-server=http://proxy.iploop.io:8880`]
});
const page = await browser.newPage();
await page.authenticate({ username: 'iploop', password: `${process.env.IPLOOP_API_KEY}-country-US` });
await page.goto('https://example.com');
```

### Playwright
```python
browser = p.chromium.launch(proxy={
    "server": "http://proxy.iploop.io:8880",
    "username": "user",
    "password": f"{os.environ['IPLOOP_API_KEY']}-country-US"
})
```

### Scrapy
```python
import os
HTTP_PROXY = f'http://iploop:{os.environ["IPLOOP_API_KEY"]}-country-US@proxy.iploop.io:8880'
```

---

## 💰 Pricing

| Plan | Per GB | Rate Limit |
|------|--------|------------|
| **Free** | $0 | 30 req/min (0.5 GB included) |
| **Starter** | $4.50 | 120 req/min |
| **Growth** | $3.50 | 300 req/min |
| **Business** | $2.50 | 600 req/min |
| **Enterprise** | Custom | 1000 req/min |

🎁 Use code **`OPENCLAW`** for **20% off** any paid plan at [iploop.io/signup](https://iploop.io/signup.html)

---

## 🐳 Earn Free Proxy Credits

Share unused bandwidth → earn proxy credits. **1 GB shared = 1 GB of proxy access.**

```bash
docker run -d --name iploop-node --restart=always ultronloop2026/iploop-node:latest
```

Runs on Linux, macOS, Windows, Raspberry Pi. Uses < 50MB RAM.

---

## 📊 Network

- **2M+** residential IPs
- **23,000+** nodes online
- **98,000+** daily unique IPs
- **195+** countries
- **99%+** success rate
- **< 0.5s** avg response

---

## 🔧 Setup & Troubleshooting

See [rules/setup.md](./rules/setup.md) for full setup guide and troubleshooting.

## Links

- **ProxyClaw:** [proxyclaw.ai](https://proxyclaw.ai)
- **Sign Up:** [iploop.io/signup](https://iploop.io/signup.html)
- **Python SDK:** `pip install iploop-sdk` on PyPI — site presets, Chrome fingerprinting, SERP-safe search
- **Docker Hub:** [ultronloop2026/iploop-node](https://hub.docker.com/r/ultronloop2026/iploop-node)
- **Support:** partners@iploop.io
