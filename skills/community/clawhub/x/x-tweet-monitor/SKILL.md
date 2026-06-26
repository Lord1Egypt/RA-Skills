---
name: x-tweet-monitor  
description: Monitor X/Twitter accounts for new tweets and send notifications to Telegram.
---

# X Tweet Monitor

Monitor X/Twitter accounts and get Telegram notifications for new tweets.

## Setup

配置环境变量:
- TWITTER_USER: 要监控的用户名
- AUTH_TOKEN: Twitter cookie
- CT0: Twitter cookie  
- TELEGRAM_BOT_TOKEN: Telegram机器人token
- TELEGRAM_CHAT_ID: 你的Telegram ID

## Usage

```bash
python3 x_tweet_monitor.py
```
