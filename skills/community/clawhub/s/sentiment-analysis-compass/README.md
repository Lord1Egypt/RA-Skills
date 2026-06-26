# Sentiment Compass

AI-powered social media sentiment monitoring and analysis tool for Chinese platforms.

## Features

- **Platform Monitoring**: Xiaohongshu (RED), Douyin, Weibo, WeChat Official Account keyword search
- **AI Sentiment Analysis**: 🟢 Positive / 🟡 Neutral / 🔴 Negative + reason summary
- **Sentiment Reports**: Total mentions, sentiment ratio, trending charts, top posts
- **Auto Alerts**: Feishu/email push when negative sentiment exceeds threshold

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

## Quick Start

```bash
# Add keyword monitoring
python3 scripts/sentiment.py add "brand_name" "xhs,douyin"

# Execute crawl
python3 scripts/sentiment.py crawl "brand_name"

# Analyze sentiment
python3 scripts/sentiment.py analyze-pending "brand_name"

# Generate report
python3 scripts/sentiment.py report "brand_name" 7

# Check alerts
python3 scripts/sentiment.py check-alerts
```

## Configuration

```bash
# GLM-4 API Key (optional, for AI sentiment analysis)
python3 scripts/sentiment.py config-set glm_api_key "your_key"

# Feishu group bot Webhook
python3 scripts/sentiment.py config-set feishu_webhook "https://open.feishu.cn/..."

# Email SMTP
python3 scripts/sentiment.py config-set smtp_config '{"host":"smtp.example.com","port":587,"user":"...","pass":"...","from":"...","to":"..."}'
```

## Pricing

| Tier | Price | Keywords | Platforms | Daily Limit |
|------|-------|:--------:|-----------|:-----------:|
| FREE | ¥0 | 1 | Xiaohongshu | 50 |
| STD | ¥29/mo | 3 | Xiaohongshu + Douyin | 300 |
| PRO | ¥99/mo | 10 | 4 platforms | 1,000 |
| MAX | ¥299/mo | Unlimited | 4 platforms | Unlimited |

> For paid plans, visit [YK-Global.com](https://yk-global.com)
