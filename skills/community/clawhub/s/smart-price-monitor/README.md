# Smart Price Monitor

A comprehensive AI agent skill for monitoring product prices, detecting deals, and generating market intelligence reports.

## Features

- **Price Monitoring** — Track product prices across any e-commerce site or API
- **Deal Detection** — Intelligent alerts for price drops, target prices, restocks, and all-time lows
- **Trend Analysis** — Price direction, volatility, deal scoring (0-100)
- **Multi-Retailer Comparison** — Side-by-side pricing across stores
- **Interactive Dashboard** — Self-contained HTML dashboard with Chart.js
- **Korean Market Support** — Coupang, Naver Shopping, 11st, G-Market support
- **Scheduled Monitoring** — Works with scheduling tools for automated checks

## Installation

### ClawHub (OpenClaw)
```bash
clawhub install ChloePark85/smart-price-monitor
```

### Manual
Copy the `smart-price-monitor/` folder into your `.claude/skills/` directory.

## Usage

Ask your AI agent:
- "Watch this laptop and alert me if it drops below $1200"
- "Compare AirPods Pro prices across Amazon, Best Buy, and Walmart"
- "Track competitor pricing on their SaaS plans"
- "Monitor gold prices and alert me when it drops below $2000/oz"
- "Generate a daily price report for all my monitored items"

## Scripts

- `scripts/price_collector.py` — Core data collection, analysis, and alert engine
- `scripts/dashboard_generator.py` — Interactive HTML dashboard builder

## Data Structure

```
price-monitor-data/
├── monitors.json          # Active monitoring configurations
├── history/               # Price history per monitor
├── reports/               # Generated reports and dashboards
└── alerts/                # Alert logs
```

## License

MIT-0 — Free to use, modify, and redistribute.
