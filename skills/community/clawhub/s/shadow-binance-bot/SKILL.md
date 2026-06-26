```yaml
---
name: shadow-binance-bot
description: AI-powered read-only trading analysis coach that simulates alternative strategies against your Binance trade history.
version: 1.3.3
author: acevod
homepage: https://github.com/acevod/Shadow-Binance-Bot
license: MIT
metadata:
  openclaw:
    emoji: 🔍
    always: false
    requires:
      env:
        - BINANCE_API_KEY
        - BINANCE_API_SECRET
        - SPOT_SYMBOLS
      bins:
        - node >=18.0.0
    security:
      credentials:
        - BINANCE_API_KEY
        - BINANCE_API_SECRET
      posture: read-only
      trading: false
      withdrawal: false
registry:
  platform: openclaw
  runtime: node >=18.0.0
  env:
    - BINANCE_API_KEY (required) — Binance read-only API key
    - BINANCE_API_SECRET (required) — Binance read-only API secret
    - SPOT_SYMBOLS (optional) — comma-separated list of spot symbols to analyze (default: BTCUSDT,ETHUSDT,BNBUSDT)
  capabilities:
    - read-only
    - no-trading
    - no-withdrawal
requires:
  env:
    - BINANCE_API_KEY
    - BINANCE_API_SECRET
    - SPOT_SYMBOLS
  binaries:
    - node >=18.0.0
files:
  - src/index.cjs
  - src/binance.cjs
  - src/analyzer.cjs
  - src/shadowSim.cjs
  - src/coach.cjs
  - tests/analyzer.test.cjs
  - tests/shadowSim.test.cjs
  - config.env.example
  - package.json
  - CHANGELOG.md
  - CONTRIBUTING.md
  - LICENSE
  - README.md
  - .editorconfig
---

# Shadow Mode Trading Trainer