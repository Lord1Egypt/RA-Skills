# 💰 IPLoop Node Rewards

Earn proxy credits just by keeping your node online. No bandwidth metering — pure uptime rewards.

## Reward Tiers

| Tier | Cumulative Uptime | Rate | Daily Earning |
|------|-------------------|------|---------------|
| 🥉 Bronze | 0 – 6 hours | 50 MB/hour | 300 MB |
| 🥈 Silver | 6 – 24 hours | 75 MB/hour | 1.35 GB |
| 🥇 Gold | 24+ hours | 100 MB/hour | 2.4 GB/day |

## Earnings Examples

| Scenario | Monthly Credits |
|----------|----------------|
| 1 node, always on | ~70 GB/month |
| 2 nodes (+20% bonus) | ~168 GB/month |
| 5 nodes (+20% each) | ~490 GB/month |

## How It Works

1. **Install** the node agent (Docker or binary)
2. **Run it** — agent connects to `gateway.iploop.io` automatically
3. **Earn** — credits accumulate based on uptime, updated hourly
4. **Use** — spend credits as proxy bandwidth via `proxy.iploop.io:8880`

### Credit = Bandwidth

- 1 credit = 1 MB of proxy access
- Credits accumulate in real-time
- No expiration on earned credits
- Use credits with any IPLoop proxy feature (geo-targeting, sticky sessions, etc.)

## Rules

- **Minimum uptime:** 5 minutes before earning starts
- **Daily cap:** 10 GB/day per node (anti-abuse)
- **Multi-device bonus:** +20% per additional node
- **Tier progression:** Based on cumulative uptime (resets if offline > 24h)
- **Fair use:** Nodes that route traffic earn faster than idle nodes

## Quick Start

```bash
# Docker
docker run -d --name iploop-node --restart=always ultronloop2026/iploop-node:latest

# Check it's connected
curl -s https://gateway.iploop.io:9443/health | python3 -m json.tool
```

## Use Your Earned Credits

```bash
# Basic proxy request
curl -x "http://iploop:YOUR_API_KEY-country-US@proxy.iploop.io:8880" https://httpbin.org/ip

# Python SDK
pip install iploop[stealth]
```

```python
from iploop import IPLoop
client = IPLoop(api_key="YOUR_KEY", stealth=True)
result = client.fetch("https://www.amazon.com/dp/B0BSHF7WHW", country="US")
```

## Pricing Comparison

Without node rewards, proxy pricing is:
- Starter: $4.50/GB
- Growth: $3.50/GB
- Business: $2.50/GB

**With a single node running 24/7, you get ~70 GB/month FREE.**

That's equivalent to $175–$315/month of proxy bandwidth at zero cost.
