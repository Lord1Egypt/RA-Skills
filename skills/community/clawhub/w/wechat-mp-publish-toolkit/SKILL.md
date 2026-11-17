---
name: wechat-mp-publisher
description: "WeChat Official Account (微信公众号) draft push and auto-publish toolkit. This skill should be used when the user wants to push article drafts to a WeChat Official Account draft box via API, publish drafts automatically on a schedule, or set up a daily publishing automation. Covers credential setup, IP whitelisting, draft creation, and freepublish/submit publishing. Triggers: push draft, publish to WeChat, auto-publish, 微信发布, 推送草稿, 自动发布, 公众号发布."
agent_created: true
---

# WeChat MP Publisher

## Overview

A generic toolkit for pushing and publishing articles to a WeChat Official Account (公众号) via the WeChat MP API. Supports two core operations:

1. **Push Draft** — Upload article HTML + cover image to the draft box (`draft/add`)
2. **Publish Draft** — Publish a draft from the draft box to all subscribers (`freepublish/submit`)

Plus a daily automation template for scheduled auto-publishing.

## First-Time Setup

### 1. Configure Credentials

Copy `assets/.env.example` to a permanent location and fill in values:

```bash
cp assets/.env.example ~/.wechat-mp.env
```

Edit the file:
```
WECHAT_APPID=wx_your_appid_here
WECHAT_SECRET=your_secret_here
WECHAT_AUTHOR=你的公众号名称
```

**Where to find credentials:**
- Login to https://mp.weixin.qq.com
- Settings & Development → Development → Basic Configuration
- AppID is visible directly; AppSecret click "Reset" to get (save immediately, only shown once)

### 2. IP Whitelist

The server IP calling the API must be whitelisted, otherwise `errcode=40164`.

To get the current server IP:
```bash
curl -s https://api.ipify.org
```

Add this IP at: mp.weixin.qq.com → Development → Basic Configuration → IP Whitelist (IP白名单).

### 3. API Permissions

- `draft/add` (push draft): Available to all verified accounts
- `freepublish/submit` (publish): Requires **verified enterprise/organization account** (已认证的企业/个体工商户主体). Permission activates ~24 hours after verification. If `errcode=48001`, the permission is still syncing — publish manually from the draft box.

## Core Tasks

### Task 1: Push Draft to Draft Box

Use `scripts/push_draft.py` to push an article as a draft.

```bash
python3 scripts/push_draft.py \
  --env ~/.wechat-mp.env \
  --title "文章标题" \
  --digest "文章摘要，不超过120字" \
  --html /path/to/article.html \
  --thumb MEDIA_ID_OR_LEAVE_BLANK
```

**What the script does:**
1. Load credentials from the `--env` file
2. Get `access_token` (handles 40164 IP whitelist error)
3. If `--thumb` not provided and a cover image path is given, upload it to the material library first
4. Push the draft via `draft/add` API
5. Print the resulting `media_id`

**Key constraints:**
- Title: max 64 bytes (~21 Chinese characters)
- Digest (摘要): max 120 characters
- Author: leave empty via API (Chinese names exceed 8-byte limit) — set manually in editor
- Article images must use `mmbiz.qpic.cn` domains (upload to material library first)
- JSON must use `ensure_ascii=False` to avoid garbled Chinese — the script handles this with `curl --data-binary`

### Task 2: Publish a Draft

Use `scripts/publish_draft.py` to publish a draft that's already in the draft box.

```bash
python3 scripts/publish_draft.py \
  --env ~/.wechat-mp.env \
  --media-id MEDIA_ID_FROM_DRAFT
```

**What the script does:**
1. Load credentials from the `--env` file
2. Get `access_token`
3. Call `freepublish/submit` with the `media_id`
4. Report success (`publish_id`) or the specific error code

**Error handling:**
| errcode | Meaning | Action |
|---------|---------|--------|
| 0 | Success | Notify user, provide `publish_id` |
| 48001 | API permission not active | Tell user to publish manually from mp.weixin.qq.com draft box |
| 40007 | media_id invalid (already published or deleted) | Tell user to check the draft box |
| -1 | System error (transient) | Retry 2-3 times; if persistent, manual publish |

**Publishing is irreversible** — once published, the article goes to all subscribers. Always verify the `media_id` is correct.

### Task 3: Set Up Daily Auto-Publish Automation

Refer to `references/automation-template.md` for the complete automation prompt. The recommended setup:

1. **Draft generation automation** — runs daily (e.g., 15:00) to generate article content and push to draft box
2. **Publish automation** — runs daily (e.g., 20:00) to call `freepublish/submit` on the day's draft

Create automations using the `automation_update` tool with:
- `scheduleType: "recurring"`
- `rrule: "FREQ=DAILY;BYHOUR=20;BYMINUTE=0"` (for 20:00 daily)
- The prompt from `references/automation-template.md`

## Quick API Reference (Bash)

For ad-hoc operations, use `scripts/wechat_api.sh`:

```bash
source scripts/wechat_api.sh

# Set credentials
export WECHAT_APPID="wx_your_appid"
export WECHAT_SECRET="your_secret"

# Get access token
TOKEN=$(get_wechat_token)

# Upload cover image (returns media_id)
upload_wechat_image "$TOKEN" /path/to/cover.png

# Create draft from JSON file
create_draft "$TOKEN" /path/to/draft.json

# Publish draft
publish_draft "$TOKEN" "MEDIA_ID_HERE"
```

## Resources

- `scripts/push_draft.py` — Push article HTML to draft box (Python, uses curl for binary-safe JSON)
- `scripts/publish_draft.py` — Publish a draft via freepublish/submit (Python)
- `scripts/wechat_api.sh` — Bash helper functions for all WeChat MP API calls
- `references/api-guide.md` — Detailed API documentation, error codes, encoding gotchas
- `references/automation-template.md` — Ready-to-use automation prompt for daily publishing
- `assets/.env.example` — Credential template file
