# ProxyClaw by IPLoop

Residential proxy platform for AI agents, bots & data pipelines — 2M+ residential IPs, 195+ countries, anti-bot bypass.

[![GitHub stars](https://img.shields.io/github/stars/Iploop/proxyclaw?style=social)](https://github.com/Iploop/proxyclaw)
[![npm](https://img.shields.io/npm/v/iploop?label=npm&color=CB3837)](https://npmjs.com/package/iploop)
[![PyPI](https://img.shields.io/pypi/v/iploop-sdk?label=PyPI&color=3775A9)](https://pypi.org/project/iploop-sdk/)
[![LangChain](https://img.shields.io/badge/LangChain-Integration-2DB9A7)](https://pypi.org/project/langchain-proxyclaw/)
[![ClawHub](https://img.shields.io/badge/ClawHub-proxyclaw-7B61FF)](https://clawhub.ai/skills/proxyclaw)
[![Docker](https://img.shields.io/docker/pulls/ultronloop2026/iploop-node?label=Docker)](https://hub.docker.com/r/ultronloop2026/iploop-node)
[![QA](https://img.shields.io/badge/QA-66%2F66%20sites-brightgreen)](scripts/qa_scraper.py)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Install

```bash
# Python SDK
pip install iploop-sdk

# Node.js SDK
npm install iploop

# OpenClaw skill
clawhub install proxyclaw
```

## Get Your API Key (free)

1. **Sign up** at [iploop.io/signup.html](https://iploop.io/signup.html) — takes 30 seconds
2. **Get your key** from [platform.iploop.io](https://platform.iploop.io) → API Keys section  
3. **Set it:**
```bash
export IPLOOP_API_KEY="your_key_here"
```

✨ **New Format:** `iploop_{short}_{secret}` — single copy-paste, no more customer_id needed!

Free tier includes **0.5 GB** — no credit card needed. Or [earn unlimited credits](REWARDS.md) by running a Docker node.

## Quick Start

### Python
```python
from iploop import IPLoop

client = IPLoop(api_key="YOUR_KEY", country="US")

# Anti-bot sites just work
r = client.fetch("https://www.zillow.com/homes/NYC_rb/")      # ✅ 1.3MB
r = client.fetch("https://www.walmart.com/browse/electronics")  # ✅ 2.5MB
r = client.fetch("https://www.bestbuy.com/site/laptops")       # ✅ 847KB

# SERP / Google-compatible search research
# Use this instead of raw google.com/search to avoid verification pages.
serp = client.serp.search("public search query", country="US")
print(serp["results"])

# Compatibility wrapper; safe SERP path by default
serp = client.google.search("public search query", country="US")

# Country targeting
r = client.fetch("https://example.com", country="DE")

# Sticky session
s = client.session()
r1 = s.fetch("https://httpbin.org/ip")
r2 = s.fetch("https://httpbin.org/ip")  # same IP
```

### Node.js
```javascript
const { IPLoop } = require('iploop');
const client = new IPLoop('YOUR_API_KEY');
const result = await client.fetch('https://example.com', { country: 'US' });
```

### curl
```bash
# New format (v2) — single key
curl -x "http://iploop:YOUR_KEY-country-US@proxy.iploop.io:8880" https://httpbin.org/ip

# Example:
# curl -x "http://iploop:iploop_fd80eb86_72dabf65...-country-US@proxy.iploop.io:8880" https://httpbin.org/ip
```

### LangChain (AI Agents)
```bash
pip install langchain-proxyclaw
```

```python
from langchain_proxyclaw import ProxyClawTool, ProxyClawScraperTool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

# Single tool usage
tool = ProxyClawTool(api_key="YOUR_KEY")
result = tool.invoke({
    "url": "https://example.com",
    "country": "US"
})

# Use with an AI agent
scraper = ProxyClawScraperTool(api_key="YOUR_KEY")
agent = initialize_agent(
    [scraper],
    ChatOpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

agent.run("Find pricing from https://competitor.com/pricing")
```

[📚 LangChain Integration Docs](https://python.langchain.com/docs/integrations/tools/proxyclaw) | [PyPI](https://pypi.org/project/langchain-proxyclaw/)

## 67 Site Presets — 100% Success Rate

Core site presets were tested 5× back-to-back; SERP-safe search is included as the 67th preset.

| Category | Sites | Method |
|----------|-------|--------|
| **E-commerce** | Amazon, eBay, Walmart, Target, BestBuy, Costco, Nordstrom, Newegg, Wayfair, Nike, Shopify, Zappos, ASOS, IKEA, Apple, Samsung | Proxy + Stealth |
| **Social** | Reddit, Twitter/X, Instagram, TikTok, Pinterest, LinkedIn, Quora, Medium, Twitch | Stealth Mode |
| **News** | CNN, BBC, NYTimes, Fox News, The Guardian, Yahoo News, Dev.to | Proxy |
| **Tech** | GitHub, StackOverflow, HackerNews, NPM, PyPI, Coursera | Proxy |
| **Real Estate** | Zillow, Airbnb, Booking.com, Craigslist | Stealth Mode |
| **APIs** | YouTube, Stocks, CoinGecko, Spotify, XKCD, SpaceX, Pokemon, Weather, ExchangeRate, RemoteOK | Direct API |
| **Other** | Wikipedia, IMDb, Steam, Goodreads, Trustpilot, Archive.org, HomeDepot, DuckDuckGo, Bing, Hulu, Microsoft | Proxy + Stealth |

### Anti-Bot Bypass

Stealth mode uses advanced browser fingerprinting + residential IPs:

- Bypasses Cloudflare, Akamai, and most anti-bot systems
- 66/66 legacy site presets pass (100%) with stealth mode; SERP-safe search is included separately
- Auto-detects stealth capabilities and activates automatically

## API

### Customer API
Full REST API at `https://api.iploop.io/api/v1/` — see [docs/API.md](docs/API.md)

| Endpoint | Auth | Description |
|----------|------|-------------|
| `POST /auth/register` | No | Create account, get JWT |
| `POST /auth/login` | No | Login, get JWT |
| `GET /usage` | JWT | Plan, bandwidth, stats |
| `GET /billing` | No | Pricing plans |
| `GET /nodes` | JWT | Browse proxy nodes |
| `GET /nodes/stats` | JWT | Network statistics |
| `GET /nodes/countries` | JWT | Available countries |
| `GET /proxy/config` | JWT | Proxy configuration |
| `GET /earn/stats` | JWT | Earning overview |
| `GET /earn/balance` | JWT | Credit balance |
| `GET/POST /earn/devices` | JWT | Manage earning devices |
| `POST /earn/cashout` | JWT | Withdraw earnings (min $10) |
| `GET /dashboard/summary` | JWT | Full dashboard data |

### Proxy Endpoint
```
proxy.iploop.io:8880
```

Auth format (v2): `iploop:APIKEY-country-XX-city-NAME-session-ID@proxy.iploop.io:8880`

**New format:** `iploop:iploop_{short}_{secret}-country-XX@proxy.iploop.io:8880`
- `short` = first 8 chars of your customer ID
- `secret` = 40-char random hex
- Both embedded in one key — just copy and paste!

### Gateway Health
```bash
curl https://gateway.iploop.io:9443/health
# → {"connected_nodes": 23000+, "status": "healthy"}
```

## Earn Free Credits 💰

Share bandwidth → earn proxy credits. No investment needed.

```bash
docker run -d --name iploop-node --restart=always ultronloop2026/iploop-node:latest
```

| Tier | Uptime | Rate | Daily |
|------|--------|------|-------|
| 🥉 Bronze | 0–6h | 50 MB/hr | 300 MB |
| 🥈 Silver | 6–24h | 75 MB/hr | 1.35 GB |
| 🥇 Gold | 24h+ | 100 MB/hr | **2.4 GB/day** |

**→ ~70 GB/month free** with one node running 24/7.

Multi-device: +20% per additional node.

See [REWARDS.md](REWARDS.md) for full details.

## Pricing

| Plan | Price | Included |
|------|-------|----------|
| Free | $0 | 0.5 GB |
| Starter | $4.50/GB | 5 GB |
| Growth | $3.50/GB | 50 GB |
| Business | $2.50/GB | 200 GB |
| Enterprise | Custom | Dedicated support |

Use code **OPENCLAW** for 20% off.

## Network Stats

| Metric | Value |
|--------|-------|
| Residential IP pool | 2,000,000+ |
| Connected nodes | 23,000+ |
| Daily unique IPs | 98,000+ |
| Countries | 195+ |
| Protocols | HTTP, HTTPS, SOCKS5 |
| Device types | Android, Windows, Mac, Smart TV |
| QA success rate | 100% on 66 legacy site presets; SERP package smoke passed |

## Links

- 🌐 [proxyclaw.ai](https://proxyclaw.ai) — Landing page
- 📖 [Docs](https://proxyclaw.ai/docs.html) — API documentation
- 🔎 [SERP preset](docs/SERP.md) — Google-compatible public SERP research
- 🏠 [platform.iploop.io](https://platform.iploop.io) — Platform Dashboard & sign up sign up
- 🐍 [Python SDK](https://github.com/Iploop/iploop-python) — `pip install iploop-sdk`
- 📦 [Node.js SDK](https://github.com/Iploop/iploop-node-sdk) — `npm install iploop`
- 🐳 [Node Agent](https://github.com/Iploop/iploop-node) — Earn credits
- 🐳 [Docker Hub](https://hub.docker.com/r/ultronloop2026/iploop-node)

## License

MIT
