# Skill Discovery Monitor

Discover trending skills across multiple platforms with automated notifications and visual usage guides.

## Overview

Skill Discovery Monitor helps developers and automation enthusiasts stay updated with the latest and most popular skills across various platforms including Clawhub, GitHub Actions, npm packages, and more.

## Features

- 🔍 **Multi-platform Discovery**: Monitor Clawhub, GitHub, npm, and other skill repositories
- 📊 **Popularity Metrics**: Stars, downloads, trending scores
- 📝 **Feature Summaries**: Clear descriptions of what each skill does
- 📈 **Usage Flowcharts**: Mermaid diagrams showing how to use skills
- 📱 **Multi-channel Notifications**: Telegram, Discord, Email
- ⏰ **Daily Updates**: Automated scheduled reports
- 💰 **SkillPay Integration**: Pay-per-use pricing

## Supported Platforms

### Clawhub
- Latest published skills
- Trending skills by category
- User ratings and downloads

### GitHub
- GitHub Actions marketplace
- Popular automation workflows
- Community-starred repositories

### npm
- CLI tools and packages
- Developer utilities
- Automation scripts

## API Usage

### Discover Skills

```bash
# Get top AI skills
curl "http://localhost:3000/discover?category=ai&limit=5"

# Get all trending skills
curl "http://localhost:3000/discover?limit=20"
```

### Platform-specific Discovery

```bash
# Clawhub skills only
curl "http://localhost:3000/platform/clawhub"

# GitHub Actions only
curl "http://localhost:3000/platform/github"
```

### Subscribe to Updates

```bash
curl -X POST http://localhost:3000/subscribe \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "channels": {
      "telegram": { "chatId": "123456789" }
    },
    "preferences": {
      "categories": ["ai", "productivity"],
      "platforms": ["clawhub", "github"]
    }
  }'
```

## Skill Report Format

Each discovered skill includes:

1. **Basic Info**
   - Name and platform
   - Author/creator
   - Category and tags

2. **Metrics**
   - Stars/likes
   - Downloads/installs
   - Trending score

3. **Feature Summary**
   - Key capabilities
   - Use cases
   - Requirements

4. **Usage Flowchart**
   - Step-by-step visual guide
   - Mermaid diagram format
   - Easy to understand workflow

## Configuration

Create a `.env` file:

```env
# SkillPay API Key (Required)
SKILLPAY_API_KEY=sk_e390b52cb259fc4f4aa1489547a48375d72876acdee75de57101d9e0e833fcb7

# Server Port
PORT=3000

# Telegram Bot (Optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Discord Webhook (Optional)
DISCORD_WEBHOOK_URL=your_discord_webhook_url

# Email SMTP (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

# Clawhub Token (Optional - for higher rate limits)
CLAWHUB_TOKEN=your_clawhub_token

# GitHub Token (Optional - for higher rate limits)
GITHUB_TOKEN=your_github_token

# Schedule (Cron format)
SCHEDULE=0 10 * * *
```

## Installation

```bash
npm install
```

## Running

```bash
npm start
```

## Testing

```bash
npm test
```

## Pricing

- **Per-call**: 0.001 USDT
- **Auto-settlement**: Via SkillPay.me

## Use Cases

- **Developers**: Discover new tools and automation skills
- **Teams**: Stay updated on productivity tools
- **Learners**: Find educational skills and tutorials
- **Creators**: Monitor competition and trends

## Tech Stack

- Node.js + Express
- Cheerio (Web scraping)
- Clawhub API
- GitHub API
- npm Registry API
- Mermaid (Flowchart generation)
- Telegram/Discord/Email notifications
- node-cron (Scheduling)

## License

MIT
