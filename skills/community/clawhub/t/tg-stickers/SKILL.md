---
name: tg-stickers
description: "Collect and send Telegram stickers smartly. Auto-import packs, tag by emotion, select contextually, and respect frequency limits (2-5 messages)."
---

# Telegram Stickers Skill

Intelligently manage and send Telegram stickers with emotional awareness.

## Core Value

**OpenClaw natively supports sending stickers** (`message` tool), but this skill adds:
- ✅ **Collection management** - Import entire sticker packs at once
- ✅ **Emotion tagging** - 100+ emoji → emotion mappings
- ✅ **Smart selection** - Context-based + randomization (avoid repetition)
- ✅ **Frequency control** - 2-5 messages between stickers
- ✅ **Usage analytics** - Track which stickers work best

## Quick Start

### 1. Import Sticker Packs
```bash
./import-sticker-pack.sh <pack_short_name_or_id>
```

### 2. Auto-Tag by Emotion
```bash
./auto-tag-stickers.sh
```

### 3. Send Stickers (in agent code)
```javascript
// ✅ Use OpenClaw's message tool directly
message(action='sticker', target='<chat_id>', stickerId=['<file_id>'])

// No bash script needed - OpenClaw handles sending natively
```

### 4. Smart Selection
```bash
./random-sticker.sh "goodnight"  # Returns random sticker tagged "goodnight"
```

## Tools

| Script | Purpose | Usage |
|--------|---------|-------|
| `import-sticker-pack.sh` | Bulk import Telegram sticker pack | `./import-sticker-pack.sh pa_XXX...` |
| `auto-tag-stickers.sh` | Tag stickers by emoji → emotion | `./auto-tag-stickers.sh` |
| `random-sticker.sh` | Select random sticker by tag | `./random-sticker.sh "happy"` |
| `check-collection.sh` | View collection stats | `./check-collection.sh` |

## Agent Integration

```markdown
## Sticker Usage

When to send:
- Goodnight/morning greetings (always use sticker over text)
- Celebrating success/milestones
- Humorous moments
- Emotional responses (joy, sympathy, encouragement)

How to send:
1. Use random-sticker.sh to pick appropriate sticker by emotion
2. Call message(action=sticker, ...) directly
3. (Optional) Update stickers.json manually to track usage

Frequency: 2-5 messages between stickers (track in agent logic)
```

## Emotion Tags

Auto-tagging maps 100+ emoji to emotions:
- `happy` 😊😄🥳
- `sad` 😢😭😔
- `love` ❤️💕😍
- `laugh` 😂🤣😆
- `thinking` 🤔💭
- `goodnight` 🌙💤😴
- `goodmorning` ☀️🌅
- `warm`, `gentle`, `greeting`, ...

## File Structure

```
tg-stickers/
├── SKILL.md                  # This file
├── README.md                 # Quick start guide
├── stickers.json             # Collection + usage data
├── stickers.json.example     # Empty template
├── import-sticker-pack.sh    # Bulk import
├── auto-tag-stickers.sh      # Emoji → emotion
├── random-sticker.sh         # Context-based selection
└── check-collection.sh       # Stats viewer
```

## stickers.json Structure

```json
{
  "collected": [
    {
      "file_id": "CAACAgEAAxUAAWmq...",
      "emoji": "🌙",
      "set_name": "pa_dKjUP9P2dt4k...",
      "added_at": "2026-03-06T23:31:00Z",
      "tags": ["goodnight", "sleep", "night", "warm", "gentle"],
      "used_count": 3,
      "last_used": "2026-03-07T00:24:00Z"
    }
  ],
  "usage_log": [
    {
      "file_id": "...",
      "sent_at": "2026-03-07T00:24:00Z",
      "context": "User saying goodnight",
      "message_id": "2599"
    }
  ],
  "stats": {
    "total_collected": 124,
    "total_sent": 15,
    "last_sent_at": "2026-03-07T00:24:00Z",
    "messages_since_last_sticker": 0
  },
  "config": {
    "min_messages_between_stickers": 2,
    "max_messages_between_stickers": 5,
    "enabled": true
  }
}
```

## Usage Philosophy

**Like a human:**
- Stickers enhance emotion, don't replace words
- Use sparingly but meaningfully
- Goodnight/morning → always sticker preferred
- Celebrations, humor, empathy → good use cases
- Technical answers, data reports → skip stickers

**Frequency:**
- Default: 2-5 messages between stickers
- Special occasions (greetings) override frequency rules
- Track in `messages_since_last_sticker`

## Example: Goodnight Flow

```bash
# 1. Agent detects "goodnight" intent
# 2. Select random goodnight sticker
FILE_ID=$(bash /path/to/random-sticker.sh "goodnight")

# 3. Send via OpenClaw (from agent code)
message(action=sticker, target=<chat_id>, stickerId=[$FILE_ID])

# 4. (Optional) Track usage manually
jq --arg fid "$FILE_ID" \
   '(.collected[] | select(.file_id == $fid) | .used_count) += 1' \
   stickers.json > stickers.json.tmp && \
   mv stickers.json.tmp stickers.json
```

---

**Philosophy:** Stickers should feel natural, not robotic. Collect user preferences, rotate selections, and respect conversation flow.
