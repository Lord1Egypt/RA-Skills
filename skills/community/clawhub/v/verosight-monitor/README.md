# 🔍 Verosight Monitor

**Social Media Intelligence Skill for OpenClaw Agents**

Real-time sentiment analysis, trend detection, influencer tracking, and bot detection powered by [Verosight API](https://verosight.com).

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-2563EB?style=for-the-badge)](https://github.com/openclaw/openclaw)
[![Version](https://img.shields.io/badge/Version-1.0.1-8B5CF6?style=for-the-badge)](https://clawhub.com/skills/verosight-monitor)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

---

## What Is This?

Verosight Monitor is an OpenClaw skill that integrates the [Verosight API](https://verosight.com) for real-time social media intelligence. It enables AI agents to perform sentiment analysis, track trends, identify influencers, and detect bot activity across major social media platforms.

### Supported Platforms

- **X (Twitter)** — Posts, replies, engagement metrics
- **Instagram** — Posts, captions, engagement
- **TikTok** — Videos, descriptions, views
- **YouTube** — Videos, comments, engagement
- **Threads** — Posts, replies, engagement
- **Facebook** — Posts, pages
- **LinkedIn** — Posts, articles
- **News Portals** — Indonesian media articles

## Features

- 📊 **Sentiment Analysis** — Positive/negative/neutral breakdown with engagement-weighted scoring
- 📈 **Trend Detection** — Volume tracking over time with daily breakdowns
- 👤 **Influencer Identification** — Find the most vocal and impactful accounts
- 🤖 **Bot Detection** — Identify coordinated posting patterns and inauthentic behavior
- 📄 **PDF Reports** — Professional reports with tables, charts, and formatted layouts
- 🌐 **Multi-Platform** — Monitor across 8+ platforms simultaneously
- ⚡ **Real-Time** — Live data from social media and news sources

## Quick Start

### Prerequisites

- [OpenClaw](https://github.com/openclaw/openclaw) agent instance
- Verosight API key ([sign up here](https://verosight.com))

### Installation

```bash
# Via ClawHub (recommended)
clawhub install verosight-monitor

# Or clone manually
git clone https://github.com/jrrqd/verosight-monitor.git
cp -r verosight-monitor ~/.openclaw/workspace/skills/
```

### Get Your API Key

1. Sign up at [verosight.com](https://verosight.com)
2. Go to [API Keys](https://verosight.com/dashboard/keys)
3. Generate a new key (starts with `vlt_live_`)

### Authenticate

```bash
# Exchange API key for JWT token (valid 24h)
JWT=$(curl -s -X POST "https://api.verosight.com/v1/auth/token" \
  -H "X-API-Key: vlt_live_YOUR_KEY" | jq -r '.token')
```

### Your First Query

```bash
# Sentiment analysis
curl -s "https://api.verosight.com/v1/analytics/sentiment?query=your_keyword&sources=x,instagram&days=7" \
  -H "Authorization: Bearer $JWT" | jq .
```

## API Reference

### Posts

```bash
# Search posts
GET /v1/posts?query=KEYWORD&sources=x,instagram&limit=10&days=7

# Get single post
GET /v1/posts/:id

# Get comments
GET /v1/posts/:id/comments
```

### Analytics

```bash
# Sentiment analysis
GET /v1/analytics/sentiment?query=KEYWORD&sources=x,instagram&days=7

# Volume over time
GET /v1/analytics/volume?query=KEYWORD&days=7

# Trending posts/profiles
GET /v1/analytics/trending?query=KEYWORD&limit=10
```

### Profiles

```bash
# Search profiles
GET /v1/profiles?query=ACCOUNT&source=instagram

# Profile details
GET /v1/profiles/:source/:account

# Engagement stats
GET /v1/profiles/:source/:account/stats
```

### Account

```bash
# Check balance (free)
GET /v1/account/balance

# Usage history (free)
GET /v1/account/usage
```

## Use Cases

- **Digital Reputation Management** — Monitor brand mentions and sentiment in real-time
- **Crisis Detection** — Early warning for negative viral content
- **Competitor Analysis** — Track competitor mentions and public perception
- **Influencer Marketing** — Identify key voices and opinion leaders
- **Political Monitoring** — Track public opinion on policies and events
- **Bot Detection** — Identify coordinated inauthentic behavior networks

## Project Structure

```
verosight-monitor/
├── SKILL.md                              # OpenClaw skill instructions
├── README.md                             # This file
├── LICENSE                               # MIT License
├── references/
│   ├── sentiment-workflow.md             # Step-by-step sentiment analysis guide
│   └── pdf-template.md                   # PDF report generation with pdfkit
└── scripts/
    ├── verosight-auth.sh                 # Auth helper (API key → JWT)
    └── quick-sentiment.sh                # Quick sentiment check CLI
```

## Credit System

Each API call costs credits based on the endpoint:

- **Posts search** — 2 credits
- **Sentiment analysis** — 5 credits
- **Volume analytics** — 5 credits
- **Trending** — 5 credits
- **Profile search** — 2 credits
- **Account balance** — 0 credits

Free accounts start with **1,000 credits**. Failed requests (4xx/5xx) do not deduct credits.

## Rate Limits

- **Standard** — 60 requests/minute
- **Pro** — 300 requests/minute
- **Enterprise** — Custom

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Links

- [Verosight API](https://verosight.com) — API documentation and dashboard
- [ClawHub](https://clawhub.com) — OpenClaw skill marketplace
- [OpenClaw](https://github.com/openclaw/openclaw) — Open-source AI agent runtime
- [GitHub](https://github.com/jrrqd/verosight-monitor) — Source code

---

Built with 🔍 by **Slameticon Digital Valley**
