# ShieldBot OpenClaw Skills

OpenClaw/ClawHub skill for [ShieldBot Security](https://shieldbotsecurity.online) — the autonomous transaction firewall for BNB Chain and EVM networks.

## Install

```bash
npx clawhub@latest install shieldbot-security
```

Or clone and add to your OpenClaw skills directory:

```bash
git clone https://github.com/Ridwannurudeen/shieldbot-openclaw-skills.git ~/.openclaw/skills/shieldbot-security
cd ~/.openclaw/skills/shieldbot-security && pip install -r requirements.txt
```

## Architecture

```
OpenClaw Agent → shieldbot_client.py → ShieldBot API (api.shieldbotsecurity.online)
```

No API key required. All endpoints are public. Rate limit: 30 requests/minute.

## Actions

| Keyword | What it does |
|---------|-------------|
| `scan 0x...` | Scan a contract — risk score, flags, honeypot check |
| `simulate` | Firewall a transaction before signing |
| `deployer 0x...` | Investigate a deployer's history and linked contracts |
| `threats` | Live threat feed — latest detected scams |
| `check <url>` | Phishing URL detection |
| `scammers` | Top active scam deployer campaigns |
| `approvals 0x...` | Scan wallet approvals for risky ones |
| `ask <question>` | Free-form security question to AI advisor |

## Supported Chains

| Chain | ID |
|-------|----|
| BNB Smart Chain | 56 |
| Ethereum | 1 |
| Base | 8453 |
| Arbitrum One | 42161 |
| Polygon | 137 |
| Optimism | 10 |
| opBNB | 204 |

## Configuration

Override the API base URL:

```bash
export SHIELDBOT_API_BASE="https://your-custom-endpoint.com"
```

## Links

- [ShieldBot Website](https://shieldbotsecurity.online)
- [ShieldBot Dashboard](https://shieldbotsecurity.online/dashboard/)
- [GitHub (Product)](https://github.com/Ridwannurudeen/shieldbot)
- [GitHub (Claude Code Skill)](https://github.com/Ridwannurudeen/shieldbot-skills)

## License

MIT
