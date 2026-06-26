---
name: socialpost-auto
description: 社交媒体自动化运营助手。自动生成并发布小红书、微博、Twitter 内容，定时发送、互动回复。
version: 1.0.0
---

# SocialPost-Auto - 社交媒体自动化运营助手

## Pricing

| Plan | Price | Accounts | Daily Posts | Platforms |
|------|-------|----------|-------------|-----------|
| Free | $0/mo | 1 | 1 | Twitter |
| Pro | $19/mo | 3 | 5 | Twitter, Weibo, Xiaohongshu |
| Enterprise | $49/mo | 10 | Unlimited | All platforms |

Upgrade: ai.agent.anson@qq.com

## When to Run

- User says "post to Xiaohongshu", "schedule a Weibo post", "auto reply to comments"
- Scheduled tasks via cron (9am/12pm/6pm)
- Batch content generation

## Workflow

1. Parse user's content request (topic, platform, style)
2. Generate platform-optimized content + image suggestions via LLM
3. If scheduled, add to task queue
4. At scheduled time, post via platform API or Agent Browser
5. Optional: monitor comments and auto-reply

## How to Use

**Generate content:**
@openclaw generate a Xiaohongshu post about sunscreen, energetic style

**Schedule a post:**
@openclaw schedule a Weibo post daily at 9am about AI news

**View tasks:**
@openclaw show my scheduled posts

**Enable auto reply:**
@openclaw enable auto reply, when someone comments "how much" reply "DM sent"

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "socialpost-auto": {
      "license_key": "<YOUR_LICENSE_KEY>",
      "plan": "free|pro|enterprise",
      "platforms": {
        "twitter": {"api_key": "<KEY>", "api_secret": "<SECRET>"},
        "xiaohongshu": {"cookie": "<COOKIE>"},
        "weibo": {"access_token": "<TOKEN>"}
      }
    }
  }
}
```
