# Stocki — AI Financial Analyst for OpenClaw

OpenClaw skill that brings Stocki's professional AI financial analysis to WeChat via ClawBot.

## Features

- **Instant Mode** — Quick financial Q&A: market prices, news, sector outlooks, company analysis
- **Quant Mode** — Complex quantitative analysis: backtesting, strategy modeling, portfolio review
- **Scheduled Monitoring** — Periodic market updates via cron-triggered tasks
- **Doctor** — Self-diagnostics and auto-repair for setup issues
- **Zero Dependencies** — Python stdlib only, no pip install needed

## Install

```bash
clawhub install stocki --force
```

See [INSTALL.md](INSTALL.md) for all installation methods and configuration.

## Quick Start

**Instant Q&A:**
```bash
stocki instant "What's the outlook for US tech stocks?"
```

**Quant Analysis:**
```bash
stocki quant "Backtest CSI 300 momentum strategy"
stocki status <id>
stocki files <id>
stocki download <id> runs/run_001/report.md
```

**Setup Check:**
```bash
stocki doctor
```

## CLI Commands

| Command | Purpose |
|---------|---------|
| `stocki instant` | Quick financial Q&A |
| `stocki quant` | Submit quantitative analysis |
| `stocki list` | List all quant analyses |
| `stocki status` | Show analysis details and run statuses |
| `stocki files` | List result files |
| `stocki download` | Download report or image |
| `stocki diagnose` | Self-diagnostic to verify installation |
| `stocki doctor` | Check and fix setup issues |

## License

Proprietary. All rights reserved.
