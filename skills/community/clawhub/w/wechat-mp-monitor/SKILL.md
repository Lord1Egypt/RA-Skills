---
name: wechat-mp-monitor
description: Monitor WeChat MP (微信公众号) articles and send notifications. Use when user needs to track public account updates, summarize articles, or receive alerts when new content is published. Supports Feishu/Lark notifications and scheduled monitoring via cron.
---

# WeChat MP Monitor

Monitor WeChat public account articles and deliver notifications.

## Features

- Monitor specific WeChat public accounts for new articles
- Extract and summarize article content
- Send notifications to Feishu/Lark
- Schedule checks via cron

## Quick Start

### Monitor a single article

```bash
scripts/wechat_mp.py summary <article_url>
```

### Add account to watchlist

```bash
scripts/wechat_mp.py watch <account_name> [--feishu-webhook <url>]
```

### Check all watched accounts

```bash
scripts/wechat_mp.py check-all
```

## Setup

### Feishu Webhook (Optional)

To receive Feishu notifications:

1. Create a Feishu group
2. Add a webhook bot
3. Copy the webhook URL
4. Set environment variable:
   ```bash
   export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/..."
   ```

### Cron Schedule

Add to crontab for automatic monitoring:

```bash
# Check every hour
0 * * * * cd /path/to/workspace && python scripts/wechat_mp.py check-all
```

Or use OpenClaw cron:
```bash
openclaw cron add --name "wechat-monitor" --schedule "0 * * * *" --command "python scripts/wechat_mp.py check-all"
```

## Commands

| Command | Description |
|---------|-------------|
| `summary <url>` | Summarize a single article |
| `watch <name>` | Add account to watchlist |
| `unwatch <name>` | Remove from watchlist |
| `list` | Show watched accounts |
| `check-all` | Check all accounts for updates |
| `history` | Show recently processed articles |

## Data Storage

- Watchlist: `~/.wechat_mp_monitor/watchlist.json`
- Article history: `~/.wechat_mp_monitor/history.json`

## Dependencies

- Python 3.6+
- requests
- beautifulsoup4

Install: `pip install requests beautifulsoup4`
