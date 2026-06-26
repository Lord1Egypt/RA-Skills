---
name: scheduled-webhook-push
description: This skill should be used when users want to set up scheduled or recurring content push to WeChat Work group webhooks. It supports flexible scheduling including daily, weekly, monthly (specific date), and advanced patterns like last Monday of each month. Trigger phrases include webhook推送, 定时推送, 推送到企微, 企微群机器人, scheduled push, periodic webhook, 按天推送, 按周推送, 按月推送.
---

# Scheduled Webhook Push Skill

## Purpose

Provide a complete workflow for setting up scheduled content push to WeChat Work (企业微信) group webhooks. This skill handles webhook configuration, flexible schedule patterns, content formatting, and automation creation.

## When to Use

- User wants to push content to a WeChat Work group webhook on a schedule
- User mentions webhook ID/URL and a push frequency (daily, weekly, monthly, or custom)
- User wants to configure recurring automated messages to 企业微信 groups
- User provides a webhook key or full URL and wants to set up automation

## Workflow

### Step 1: Parse Webhook Configuration

Extract the webhook information from user input. The webhook can be provided in multiple formats:

1. **Full URL**: `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
2. **Key only**: `adeee643-bc8e-4ad1-bb52-83001cd5986e`
3. **From a file**: User may specify a file path containing the webhook key/URL

If provided as key only, construct the full URL:
```
https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={KEY}
```

To validate the webhook, run the validation script:
```bash
python3 {SKILL_DIR}/scripts/validate_webhook.py <webhook_url_or_key>
```

### Step 2: Determine Schedule Pattern

Parse the user's desired schedule into one of the supported patterns. Refer to `references/schedule_patterns.md` for the full mapping of natural language to RRULE + date-guard logic.

**Supported schedule types:**

| Type | Examples | Implementation |
|------|----------|----------------|
| **Daily** | 每天、每日、daily | RRULE: `FREQ=HOURLY;INTERVAL=24` |
| **Weekly** | 每周一、每周五、weekly on Monday | RRULE: `FREQ=WEEKLY;BYDAY=MO;BYHOUR=10;BYMINUTE=0` |
| **Monthly (fixed date)** | 每月1日、每月27号、monthly on the 15th | RRULE: `FREQ=HOURLY;INTERVAL=24` + date guard `day == N` |
| **Monthly (pattern)** | 每月最后一周的周一、first Monday of each month | RRULE: `FREQ=WEEKLY;BYDAY=MO;BYHOUR=10;BYMINUTE=0` + date guard |

**Date guard logic** for monthly patterns (used in automation prompt):

- **Fixed date (e.g. 每月27日)**: Add to prompt: `首先检查今天的日期，如果今天不是每月的 {N} 日，则直接结束，不执行任何操作。`
- **Last Monday of month**: Add to prompt: `首先检查今天的日期，计算本月最后一个周一的日期（本月最后一天往前找到第一个周一），如果今天不是该日期，则直接结束。`
- **First Monday of month**: Add to prompt: `首先检查今天的日期，如果今天的日期不在 1-7 号之间，则直接结束。`
- **Last week of month**: Add to prompt: `首先检查今天的日期，如果今天的日期加 7 后仍在本月内（即不是最后一周），则直接结束。`

### Step 3: Determine Push Content

Ask the user what content to push, or infer from context. Common content types:

1. **GitHub Trending** — Fetch and summarize trending AI/tech repos
2. **Custom message** — User-provided static or template message
3. **Data report** — Query data and format as report
4. **URL content** — Fetch and summarize a web page

### Step 4: Test the Push

Before creating the automation, perform a one-time test push to verify the webhook and content formatting.

Use the push script to send a test message:

```bash
python3 {SKILL_DIR}/scripts/push_to_webhook.py \
  --webhook "<WEBHOOK_URL>" \
  --format markdown \
  --message "<FORMATTED_CONTENT>"
```

Or use curl directly:

```bash
curl -s '<WEBHOOK_URL>' \
  -H 'Content-Type: application/json' \
  -d '{"msgtype":"markdown","markdown":{"content":"<CONTENT>"}}'
```

Verify the response is `{"errcode":0,"errmsg":"ok"}`.

### Step 5: Create the Automation

Use the `automation_update` tool with the following configuration:

```
mode: "suggested create"
name: <descriptive name based on content and schedule>
prompt: <date guard if needed> + <content generation steps> + <push via webhook>
rrule: <computed RRULE from Step 2>
cwds: <current workspace>
status: ACTIVE
```

**Automation prompt template:**

```
{DATE_GUARD_IF_NEEDED}

执行以下步骤：

1. {CONTENT_GENERATION_STEPS}

2. 将整理好的内容通过企业微信群机器人 Webhook 推送，Webhook 地址为：{WEBHOOK_URL}

3. 推送格式使用 {FORMAT}，确保内容格式正确、可读性好。
```

### Step 6: Confirm to User

After creating the automation, summarize the configuration:

- **Task name**: What was created
- **Schedule**: Human-readable description (e.g. "每月 27 日上午 10:00")
- **Webhook**: Target webhook (masked key for security: show first 8 and last 4 chars)
- **Content**: What will be pushed
- **Status**: Active/Paused

## Message Format Reference

WeChat Work webhook supports these message types:

### Markdown (recommended for rich content)
```json
{
  "msgtype": "markdown",
  "markdown": {
    "content": "# Title\n> Quote\n**Bold** <font color=\"warning\">Warning</font>"
  }
}
```

Supported markdown elements:
- Headers: `#`, `##`, `###`
- Bold: `**text**`
- Links: `[text](url)`
- Quotes: `> text`
- Color: `<font color="info|comment|warning">text</font>`
- Line breaks: `\n`

### Text (for simple messages)
```json
{
  "msgtype": "text",
  "text": {
    "content": "Message content",
    "mentioned_list": ["@all"]
  }
}
```

## Important Notes

- WeChat Work webhook has a rate limit of 20 messages per minute per webhook
- Markdown message content has a max length of 4096 bytes
- If content exceeds the limit, split into multiple messages
- Always mask webhook keys in user-facing output for security
- The automation scheduling system only supports HOURLY and WEEKLY RRULE frequencies; for monthly schedules, use a date guard in the prompt
