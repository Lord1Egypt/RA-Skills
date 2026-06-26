---
name: wechat-desktop-sender
description: Windows WeChat desktop automation for opening chats and sending messages. Use when the user wants to open 微信桌面端, search a contact or group, send a message, send the same message to multiple contacts/groups in serial batch mode, or send personalized messages where each recipient gets different content. Best for direct desktop WeChat messaging workflows like 文件传输助手 testing, one-to-one outreach, 串行群发, and名单驱动个性化发送. Not for browser WeChat,朋友圈 scraping, or reliable historical-message forwarding.
---

# wechat-desktop-sender

Use this skill for **Windows 微信桌面端发消息** workflows.

## What this skill provides

Bundled scripts:

- `scripts/wechat_send.py` — formal single-send command entry
- `scripts/wechat_send_hello.py` — core implementation (open WeChat, search chat, send, verify)
- `scripts/wechat_send_batch.py` — serial batch sender for multiple contacts/groups
- `scripts/wechat_send_campaign.py` — personalized serial sender (different message per contact)
- `scripts/wechat_send_template_campaign.py` — template-variable sender (same template, different row values)

## Quick start

Install dependencies:

```bash
pip install pywinauto pyperclip psutil pywin32 pillow pytesseract
```

> `pytesseract` is optional. Install it only if OCR verification is needed.

## Single send

```bash
python scripts/wechat_send.py --to "文件传输助手" --message "你好"
```

Useful flags:

```bash
python scripts/wechat_send.py --to "李义" --message "我是龙虾Koi，打个招呼。" --verify-title
python scripts/wechat_send.py --to "文件传输助手" --message "OCR测试" --ocr-verify
```

## Serial batch send

```bash
python scripts/wechat_send_batch.py --to "张三,李四,文件传输助手" --message "晚上 8 点开会"
```

Or from file:

```bash
python scripts/wechat_send_batch.py --contacts-file contacts.txt --message "晚上 8 点开会"
```

## Personalized send

```bash
python scripts/wechat_send_campaign.py --csv contacts_messages.csv --verify-title
python scripts/wechat_send_campaign.py --json contacts_messages.json --verify-title
```

## Template-variable send

```bash
python scripts/wechat_send_template_campaign.py --csv template_contacts.csv --template "{name}你好，我是Koi，关于{company}这边和你打个招呼。" --verify-title
```

## Recommended workflow

1. Ensure WeChat desktop is logged in
2. Test on `文件传输助手` first
3. Use single-send for one contact/group
4. Use batch-send for serial outreach
5. Check `wechat_automation_logs/` for logs and summaries

## Verification model

Current verification layers:

1. UI element location succeeded
2. Message was sent through the input box
3. Window text verification checks whether the message text appears in current WeChat window
4. Optional OCR verification if `--ocr-verify` is enabled and OCR deps are installed

Treat this as **practical desktop automation**, not a cryptographic delivery guarantee.

## Boundaries

Do not claim support for these unless separately extended:

- Moments / 朋友圈 scraping
- Reliable historical message forwarding
- Multi-window true parallel sending
- Full desktop social graph extraction

## Files and outputs

By default, scripts create logs under:

```text
wechat_automation_logs/
```

Outputs may include:

- run logs
- failure screenshots
- control-tree dumps
- batch summary JSON files

## OpenClaw workflow usage

Once this skill is installed, the user can express intent conversationally and the agent should route to the correct script:

- “给张三发一句话：今晚 8 点开会” → use single-send
- “给这 20 个人发同一条消息” → use batch-send
- “按这份名单分别发不同文案” → use personalized-send
- “按这份名单套一个模板变量群发” → use template-variable send

Preferred operational pattern:

1. Normalize the recipient list and message payload
2. If one recipient and one message → `scripts/wechat_send.py`
3. If many recipients and same message → `scripts/wechat_send_batch.py`
4. If many recipients and different messages → `scripts/wechat_send_campaign.py`
5. If many recipients share one template with per-row fields → `scripts/wechat_send_template_campaign.py`
6. Report success count, verification count, retry recommendations, and log/summary paths back to the user

## When to read more

For detailed CLI usage and arguments, read:

- `references/single-send.md`
- `references/batch-send.md`
- `references/personalized-send.md`
- `references/template-send.md`
