---
name: telegram-interactive-buttons
description: Create interactive Telegram messages with inline buttons using OpenClaw CLI. Use when you need user interaction in Telegram (selection from a list, confirmation dialogs, workflow menus, quick actions). Handles button formatting, callback handling, and message editing. Critical for UX-friendly Telegram automation.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["openclaw", "bash"], "optional_bins": ["python3"] },
        "credentials": ["telegram_bot_token"],
        "config_required": true
      }
  }
---

# Telegram Interactive Buttons

## Requirements

**📖 First time setup?** See [SETUP.md](SETUP.md) for detailed configuration instructions.

### Required Binaries
- `openclaw` - OpenClaw CLI (install: `npm install -g openclaw`)
- `bash` - Shell for helper scripts

### Optional Binaries
- `python3` - For JSON validation script (recommended)

### Credentials & Configuration

**Telegram Bot Setup Required:**

1. **Create a Telegram bot** via [@BotFather](https://t.me/BotFather)
   - Send `/newbot` to BotFather
   - Follow prompts to get your bot token

2. **Configure OpenClaw with your bot token:**
   
   Edit `~/.openclaw/config.json` (or your workspace `openclaw.json`):
   ```json
   {
     "channels": {
       "telegram": {
         "enabled": true,
         "botToken": "YOUR_BOT_TOKEN_HERE"
       }
     }
   }
   ```

3. **Get your chat ID:**
   - Start a chat with your bot
   - Send any message
   - Run: `openclaw message send --target "telegram:YOUR_CHAT_ID" --message "Test"`
   - Check OpenClaw logs or use Telegram bot API to retrieve your chat ID

**Target Format:** All examples use `telegram:CHAT_ID` format. Replace `CHAT_ID` with your actual Telegram chat ID (numeric).

### Security Notes

**Scripts in this skill:**
- Execute local shell commands via `bash`
- Call `openclaw` CLI with user-provided arguments
- `validate_buttons.py` parses JSON (no external connections)

**Before running:**
1. Review all scripts - they are short and readable
2. Replace placeholder chat IDs in examples
3. Run only in trusted environments
4. Never pass untrusted inputs to scripts without validation
5. Store bot token securely (use environment variables or secure config files)

**Credential Scope:**
- Bot token allows sending messages to chats where bot is added
- Scripts do not modify bot permissions or settings
- No sensitive data is transmitted beyond standard Telegram API calls

## Overview

This skill provides reliable methods for creating interactive Telegram messages with inline buttons using the OpenClaw CLI. After extensive testing across different models (Gemini, Claude), the CLI approach via `exec` tool has proven to be the most stable method for sending buttons.

**Why this skill exists:** The `message` tool's `buttons` parameter can be fragile across different models. The CLI provides consistent, predictable button rendering.

## Quick Start

Basic button message:

```bash
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "Choose an option:" \
  --buttons '[[{"text": "Option 1", "callback_data": "opt1"}, {"text": "Option 2", "callback_data": "opt2"}]]'
```

**Key points:**
- Use single quotes around the entire `--buttons` argument
- Buttons is a JSON array of arrays (rows)
- Each button needs `text` and `callback_data`
- Keep 1-2 buttons per row for mobile UX

## Sending Buttons

### Button Structure

The `--buttons` parameter accepts a JSON array of arrays (rows):

```json
[
  [{"text": "B1", "callback_data": "c1"}, {"text": "B2", "callback_data": "c2"}],
  [{"text": "B3", "callback_data": "c3"}]
]
```

**Layout Limits:**
- **Max buttons per row:** 8 (use this for grids/keypads)
- **Max buttons total:** 100
- **Mobile UX Recommendation:** While 8 are supported, keep 1-3 buttons per row for standard menus to ensure readability on mobile. Use the full 8-button width only for grids (e.g., calculators, calendars, or numeric selectors).

### Button Properties

Each button object supports:

- `text` (required): Display text
- `callback_data` (required): Unique identifier for the callback
- `style` (optional): `primary`, `success`, or `danger`

Example with styles:

```bash
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "Confirm action?" \
  --buttons '[[{"text": "✅ Confirm", "callback_data": "confirm", "style": "success"}, {"text": "❌ Cancel", "callback_data": "cancel", "style": "danger"}]]'
```

### Helper Script

Use the provided helper for cleaner code:

```bash
bash scripts/send_buttons.sh "telegram:CHAT_ID" "Choose:" '[[{"text": "Yes", "callback_data": "yes"}, {"text": "No", "callback_data": "no"}]]'
```

## Handling Callbacks

When a user clicks a button, Telegram sends a callback with the `callback_data` value. Handle it in two steps:

1. **Send confirmation message** - Acknowledge the selection
2. **Edit original message** - Remove buttons to prevent accidental re-clicks

Example flow:

```bash
# User clicked button with callback_data="yes"

# Step 1: Send confirmation
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "✅ You selected: Yes"

# Step 2: Edit original message (remove buttons)
openclaw message edit \
  --target "telegram:CHAT_ID" \
  --message-id "MESSAGE_ID" \
  --message "Choose: [Selection complete]"
```

### Editing Messages

Remove buttons after selection:

```bash
openclaw message edit \
  --target "telegram:CHAT_ID" \
  --message-id "939" \
  --message "Updated message text without buttons"
```

Or use the helper:

```bash
bash scripts/edit_message.sh "telegram:CHAT_ID" "939" "Selection complete"
```

## Common Patterns

### Yes/No Confirmation

```bash
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "Delete this file?" \
  --buttons '[[{"text": "Yes", "callback_data": "delete_yes"}, {"text": "No", "callback_data": "delete_no"}]]'
```

### Workflow Menu

```bash
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "What would you like to do?" \
  --buttons '[[{"text": "🎬 Search", "callback_data": "wf_search"}, {"text": "📊 Metrics", "callback_data": "wf_metrics"}], [{"text": "📅 Calendar", "callback_data": "wf_calendar"}, {"text": "⚙️ Settings", "callback_data": "wf_settings"}]]'
```

### Number Selection

```bash
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "How many results?" \
  --buttons '[[{"text": "5", "callback_data": "count_5"}, {"text": "10", "callback_data": "count_10"}, {"text": "20", "callback_data": "count_20"}]]'
```

## Best Practices

1. **Keep it mobile-friendly** - 1-2 buttons per row maximum
2. **Use descriptive callback_data** - `wf_search` not `btn1`
3. **Always edit after callback** - Remove buttons to prevent confusion
4. **Add visual indicators** - Emojis help distinguish button types (✅ 🎬 📊 ⚙️)
5. **Validate JSON** - Use `scripts/validate_buttons.py` before sending

## Troubleshooting

### Common Errors

**"buttons[0][0] requires text and callback_data"**
- Cause: Escaped quotes in JSON (`\"text\"` instead of `"text"`)
- Fix: Use clean JSON without escaping

**Buttons not appearing**
- Cause: Invalid JSON structure
- Fix: Validate with `python3 scripts/validate_buttons.py 'YOUR_JSON'`

**Multiple buttons per user click**
- Cause: Not editing original message after callback
- Fix: Always edit and remove buttons after handling callback

## Resources

### scripts/
- `send_buttons.sh` - Helper for sending button messages
- `edit_message.sh` - Helper for editing messages
- `validate_buttons.py` - JSON validation before sending

### references/
- `REFERENCE.md` - Complete parameter reference and advanced examples

### assets/examples/
- `basic_yes_no.sh` - Simple confirmation dialog
- `workflows_menu.sh` - Multi-option workflow menu
- `full_flow_example.sh` - Complete callback handling flow
