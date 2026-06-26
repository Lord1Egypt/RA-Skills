# Skill Discovery Monitor

Discover and monitor popular skills across multiple platforms with automated daily notifications.

## Features

- 🔍 **Multi-platform Monitoring**: Clawhub, GitHub Actions, npm packages, and more
- 📊 **Skill Analytics**: Popularity metrics, usage statistics, trending scores
- 📝 **Feature Summaries**: Concise descriptions of what each skill does
- 📈 **Usage Flowcharts**: Visual diagrams showing how to use each skill
- 📱 **Multi-channel Notifications**: Telegram, Discord, Email
- ⏰ **Scheduled Updates**: Daily automated skill discovery reports
- 💰 **Pay-per-use**: 0.001 USDT per API call

## API Endpoints

### GET /discover

Fetch popular skills from all monitored platforms.

**Query Parameters:**
- `category` (optional): Filter by category (ai, productivity, developer-tools, etc.)
- `limit` (optional): Number of skills to return (default: 10)

**Example:**
```bash
curl "http://localhost:3000/discover?category=ai&limit=5"
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "awesome-skill",
      "platform": "clawhub",
      "category": "ai",
      "description": "An awesome AI-powered skill",
      "author": "developer",
      "stars": 1234,
      "downloads": 5678,
      "features": ["Feature 1", "Feature 2"],
      "usageFlow": "graph TD; A[Start] --> B[Configure]; B --> C[Run]; C --> D[Results]",
      "url": "https://clawhub.com/skills/awesome-skill"
    }
  ]
}
```

### GET /platform/:platform

Get skills from a specific platform.

**Supported Platforms:**
- `clawhub` - Clawhub skills
- `github` - GitHub Actions
- `npm` - npm packages with CLI tools

**Example:**
```bash
curl "http://localhost:3000/platform/clawhub?limit=10"
```

### POST /notify

Trigger immediate notification with skill discoveries.

**Request:**
```json
{
  "userId": "user123",
  "transactionId": "tx456",
  "channels": {
    "telegram": { "chatId": "123456789" }
  },
  "category": "ai",
  "limit": 5
}
```

### POST /subscribe

Subscribe to daily skill discovery updates.

**Request:**
```json
{
  "userId": "user123",
  "channels": {
    "telegram": { "chatId": "123456789" },
    "email": { "to": "user@example.com" }
  },
  "preferences": {
    "categories": ["ai", "productivity"],
    "platforms": ["clawhub", "github"],
    "schedule": "0 10 * * *"
  }
}
```

## Configuration

Required environment variables:
- `SKILLPAY_API_KEY`: SkillPay API key (required)
- `TELEGRAM_BOT_TOKEN`: Telegram bot token (optional)
- `DISCORD_WEBHOOK_URL`: Discord webhook URL (optional)
- `EMAIL_USER/EMAIL_PASS`: SMTP credentials (optional)
- `CLAWHUB_TOKEN`: Clawhub API token (optional, for higher rate limits)

## Installation

```bash
npm install
npm start
```

## Pricing

- 0.001 USDT per API call
- Automatic settlement via SkillPay.me

## License

MIT
