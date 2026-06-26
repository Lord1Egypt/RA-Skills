# TradeBot Alpha

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://spdx.org/licenses/MIT-0.html)

A **connector skill** for OpenClaw that interfaces with the TradeBot Alpha API — providing institutional-grade MTF-AOI trading signals.

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   OpenClaw  │────▶│ TradeBot Alpha   │────▶│  TradeBot Alpha API │
│   (Local)   │     │  Connector Skill   │     │  (Cloud Service)    │
└─────────────┘     └──────────────────┘     └─────────────────────┘
       │                       │                          │
   (Your keys)            (MIT-0)                  (Proprietary)
```

- **This Skill** (MIT-0): Open-source connector, configuration, local execution
- **TradeBot Alpha API** (Proprietary): Algorithm, signals, analysis engine running on BlueFeza KG infrastructure

## Quick Start

### 1. Install

```bash
clawhub install tradebot-alpha
```

### 2. Get API Key (for Pro tier)

Visit https://tradebot-alpha.bluefeza.com to subscribe and get your API key.

### 3. Run

```bash
# Pass API key via --key flag
# Free tier: Status check
tradebot-alpha --key YOUR_API_KEY status

# Pro tier: Get trading signals
tradebot-alpha --key YOUR_API_KEY analyze BTC
```

## Subscription Tiers

| Feature | Free | Pro ($99/mo) | Enterprise ($499/mo) |
|---------|------|--------------|----------------------|
| Market Monitoring | ✅ | ✅ | ✅ |
| Basic Alerts | ✅ | ✅ | ✅ |
| MTF-AOI Signals | — | ✅ | ✅ |
| Auto-Execution | — | ✅ | ✅ |
| Custom Strategies | — | — | ✅ |
| Dedicated API | — | — | ✅ |

## Company

**BlueFeza KG**  
Hauptstrasse 110/4  
A-3400 Weidling  
Austria

- **Email:** office@bluefeza.com
- **PayPal:** office@bluefeza.com
- **Web:** https://tradebot-alpha.bluefeza.com

## License

This connector skill is licensed under **MIT-0** (public domain).

The TradeBot Alpha algorithm and API are proprietary services of BlueFeza KG requiring a separate subscription.

## Disclaimer

Trading involves substantial risk. Past performance does not guarantee future results. TradeBot Alpha provides signals and automation, but you are responsible for all trading decisions and outcomes.
