# Token Cost Monitor 💰

[![ClawHub](https://img.shields.io/badge/ClawHub-skill-blue)](https://clawhub.ai)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-green)](https://github.com/openclaw/openclaw)

Monitor OpenClaw API costs in real-time, set budget alerts, and optimize model spending.

## Why This Matters

**Real user stories:**
- One user spent $18.75 overnight on heartbeat checks asking "Is it daytime yet?"
- Federico Viticci spent $3,600 in a single month
- Regular users report $200/day bills from misconfigured automations

## Features

- **Real-time Cost Tracking** - Monitor API spending by session, task, and model
- **Budget Alerts** - Get notified when approaching daily/monthly limits
- **Model Routing** - Automatically route queries to cost-effective models
- **Cost Optimization Tips** - Receive actionable recommendations to reduce spending
- **Historical Analysis** - Track spending trends over time

## Installation

```bash
# Via ClawHub
openclaw skills install token-cost-monitor
```

## Usage

### Check Current Costs

Ask the agent:
```
"What's my OpenClaw spending today?"
```

### Set Budget Alert

Ask the agent:
```
"Alert me if daily spending exceeds $10"
```

### Optimize Model Routing

Ask the agent:
```
"Route simple queries to Haiku, complex tasks to Sonnet"
```

### Generate Cost Report

Ask the agent:
```
"Show me my top 5 most expensive tasks this week"
```

## Cost Optimization Strategies

### Model Pricing (2026)

| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| Claude Haiku | $0.25/1M | $1.25/1M | Simple queries, facts |
| Claude Sonnet | $3/1M | $15/1M | General tasks |
| Claude Opus | $15/1M | $75/1M | Complex analysis |

### Quick Wins

1. **Reduce heartbeat frequency** - From 30min to 6 hours (saves 80%)
2. **Route to cheaper models** - Use Haiku for simple queries (saves 90%)
3. **Clear context regularly** - Prevent context bloat (saves 30-50%)
4. **Batch similar tasks** - Combine multiple checks into one call

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | N/A | All cost tracking is local |

## Security & Privacy

- **No external API calls** - All cost tracking is local
- **No credentials stored** - Reads from OpenClaw session data
- **No data exfiltration** - All analysis happens on-device

## Model Invocation

This skill analyzes OpenClaw session data to provide cost insights. It does not make external API calls.

## Trust Statement

By using this skill, no external data is sent. All cost analysis is performed locally using OpenClaw session metadata. Only install if you trust the skill author.

## Requirements

- OpenClaw v1.0+
- Access to session usage data (`/status`, `/usage` commands)

## Support

- Documentation: https://github.com/openclaw/openclaw
- OpenClaw Discord: https://discord.gg/clawd

## License

MIT License - See LICENSE file in GitHub repository
