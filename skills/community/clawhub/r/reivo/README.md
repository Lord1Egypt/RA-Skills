# Reivo — AI Agent Cost Optimizer (OpenClaw Skill)

[![ClawHub](https://img.shields.io/badge/ClawHub-reivo-blue)](https://clawhub.org/skills/reivo)
[![Version](https://img.shields.io/badge/version-0.4.0-green)](https://clawhub.org/skills/reivo)

Track AI agent costs in real-time, set budget limits, and auto-detect runaway loops. Smart routing reduces costs 40-60%.

## Install

```bash
clawhub install reivo
```

## Requirements

- `REIVO_API_KEY` environment variable (get one free at [reivo.dev](https://reivo.dev))
- `curl` (pre-installed on macOS/Linux)

## Commands

| Command | Description |
|---------|-------------|
| `status [days]` | Cost overview for the last N days (default: 7) |
| `budget status` | Show budget usage with progress bar |
| `budget set <amount>` | Set budget limit (e.g. `budget set 50`) |
| `budget clear` | Remove budget limit |
| `defense` | Defense status: loops detected, requests blocked, anomalies |
| `optimize` | Get cost reduction tips with estimated savings |
| `mode <mode>` | Set routing mode: `aggressive`, `balanced`, or `quality` |
| `month` | Monthly report (cost, requests, model/agent breakdown) |
| `slack <webhook-url>` | Configure Slack notifications |
| `share` | Generate a shareable savings summary |
| `on` / `off` | Show proxy enable/disable instructions |

## How It Works

Reivo is a transparent proxy between your agent and the LLM provider:

```
Your Agent → Reivo Proxy → LLM Provider (OpenAI / Anthropic / Google)
                 ↓
          Budget check, loop detection, model routing
```

- **Smart routing**: Analyzes each request and picks the cheapest model that delivers the same quality
- **Budget enforcement**: Blocks requests when spending exceeds the limit
- **Loop detection**: Hash match + TF-IDF cosine similarity detects agents stuck in infinite loops
- **Anomaly detection**: EWMA-based spike detection flags abnormal usage patterns
- **Graceful degradation**: 4-level progressive response as budget pressure increases

## Self-Hosted Guardrails

The guardrail engine is open source:

```bash
pip install reivo-guard    # Python
npm install reivo-guard    # TypeScript
```

[reivo-guard on GitHub](https://github.com/tazsat0512/reivo-guard) — budget enforcement, loop detection, anomaly detection, CUSUM drift detection, and more. MIT licensed.

The managed [Reivo](https://reivo.dev) service adds smart routing, a dashboard, and Slack notifications on top.

## Privacy

Reivo does **not** store prompt or completion content. Only metadata is retained: model name, token counts, cost, latency, timestamp, session/agent IDs, and an irreversible prompt hash.

## Links

- [Reivo Dashboard](https://app.reivo.dev)
- [reivo-guard (OSS)](https://github.com/tazsat0512/reivo-guard)
- [ClawHub Page](https://clawhub.org/skills/reivo)

## License

MIT
