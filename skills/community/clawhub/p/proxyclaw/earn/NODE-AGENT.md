# 🌐 IPLoop Node Agent

**Earn proxy credits by sharing your unused bandwidth.**

[![Docker Hub](https://img.shields.io/docker/pulls/ultronloop2026/iploop-node)](https://hub.docker.com/r/ultronloop2026/iploop-node)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Quick Start

### Docker (recommended)

```bash
docker run -d --name iploop-node --restart=always ultronloop2026/iploop-node:latest
```

### Docker Compose

```yaml
version: '3'
services:
  iploop-node:
    image: ultronloop2026/iploop-node:latest
    container_name: iploop-node
    restart: always
```

### Standalone Binary

Download from [Releases](https://github.com/Iploop/iploop-node/releases):

| Platform | Binary |
|----------|--------|
| Linux amd64 | `iploop-node-linux-amd64` |
| Linux arm64 | `iploop-node-linux-arm64` |
| macOS Intel | `iploop-node-darwin-amd64` |
| macOS ARM | `iploop-node-darwin-arm64` |
| Windows x64 | `iploop-node-windows-amd64.exe` |
| Raspberry Pi | `iploop-node-linux-armv7` |

```bash
chmod +x iploop-node-linux-amd64
./iploop-node-linux-amd64
```

## How It Works

1. **Install** — Docker or standalone binary, one command
2. **Connect** — Agent connects to `gateway.iploop.io` via secure WebSocket
3. **Share** — Your idle bandwidth serves proxy requests through real residential IPs
4. **Earn** — Accumulate proxy credits based on uptime (see [REWARDS.md](REWARDS.md))

The agent uses < 50MB RAM and near-zero CPU. Auto-reconnects on network issues.

## Reward Tiers

| Tier | Cumulative Uptime | Rate | Daily Earning |
|------|-------------------|------|---------------|
| 🥉 Bronze | 0 – 6 hours | 50 MB/hour | 300 MB |
| 🥈 Silver | 6 – 24 hours | 75 MB/hour | 1.35 GB |
| 🥇 Gold | 24+ hours | 100 MB/hour | 2.4 GB/day |

**After 24h:** ~2.4 GB/day → **~70 GB/month** of free proxy credits.

Multi-device bonus: +20% per additional node.

Full details: [REWARDS.md](REWARDS.md)

## Use Your Credits

Once you've earned credits, use them as proxy bandwidth:

```bash
# HTTP proxy
curl -x "http://iploop:YOUR_API_KEY-country-US@proxy.iploop.io:8880" https://httpbin.org/ip

# With geo-targeting
curl -x "http://iploop:YOUR_API_KEY-country-DE-city-berlin@proxy.iploop.io:8880" https://example.com

# Sticky session (same IP)
curl -x "http://iploop:YOUR_API_KEY-session-abc123-sesstype-sticky@proxy.iploop.io:8880" https://example.com
```

### Python

```python
from iploop import IPLoop

client = IPLoop(api_key="YOUR_API_KEY", stealth=True)
result = client.fetch("https://example.com", country="US")
```

### Node.js

```javascript
const { IPLoop } = require('iploop');
const client = new IPLoop('YOUR_API_KEY');
const result = await client.fetch('https://example.com', { country: 'US' });
```

## Network Stats

| Metric | Value |
|--------|-------|
| Residential IP pool | 1,000,000+ |
| Connected nodes | 9,600+ |
| Device types | Android (8,100+), Windows (1,500+) |
| Countries | 195+ |
| Proxy endpoint | `proxy.iploop.io:8880` |
| Protocols | HTTP, HTTPS, SOCKS5 |

## Gateway Health

```bash
curl -s https://gateway.iploop.io:9443/health
```

Returns node count, device breakdown, and service status.

## FAQ

**Q: How much bandwidth does it use?**
A: The agent only routes proxy requests through your connection. Typical usage is a few hundred MB/day depending on demand in your region.

**Q: Is it safe?**
A: Yes. The agent only handles HTTP/HTTPS proxy traffic. It does not access your files, passwords, or local network. All traffic is encrypted.

**Q: Can I run multiple nodes?**
A: Yes! Each additional node earns +20% bonus credits.

**Q: What's the minimum uptime to earn?**
A: 5 minutes before earning starts. Gold tier kicks in after 24 cumulative hours.

**Q: Do I need to sign up?**
A: The node agent auto-registers. To use earned credits as proxy, sign up at [iploop.io/signup.html](https://iploop.io/signup.html) to get your API key.

## Ethical & Compliant

- Users **explicitly opt in** to share bandwidth
- Fully **GDPR and CCPA compliant**
- No personal data collected
- Traffic is encrypted end-to-end
- Open source (MIT license)

## Links

- 🌐 [IPLoop Dashboard](https://iploop.io)
- 🐳 [Docker Hub](https://hub.docker.com/r/ultronloop2026/iploop-node)
- 🔧 [ProxyClaw Skill](https://github.com/Iploop/proxyclaw)
- 📦 [Python SDK](https://github.com/Iploop/iploop-python) — `pip install iploop[stealth]`
- 📦 [Node.js SDK](https://github.com/Iploop/iploop-node-sdk) — `npm install iploop`
- 📖 [API Docs](https://proxyclaw.ai/docs.html)

## License

MIT — see [LICENSE](LICENSE)
