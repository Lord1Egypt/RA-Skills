# tg-stickers

Smart Telegram sticker management for OpenClaw agents.

## What This Does

**OpenClaw natively sends stickers**, but this skill adds intelligence:
- 📦 **Bulk import** - Add entire sticker packs at once
- 🏷️ **Auto-tagging** - Map 100+ emoji to emotions (happy, sad, goodnight, etc.)
- 🎲 **Smart selection** - Context-based random picks (avoid repetition)
- 📊 **Analytics** - Track usage patterns

## Quick Start

```bash
# 1. Import a sticker pack
./import-sticker-pack.sh pa_YK0WQxd6HTw52j6bazKo_by_SigStick21Bot

# 2. Auto-tag all stickers
./auto-tag-stickers.sh

# 3. Select a sticker (returns file_id)
./random-sticker.sh "goodnight"

# 4. Send via OpenClaw (in agent code)
message(action=sticker, target=<chat_id>, stickerId=[<file_id>])
```

## Tools

| Script | Purpose |
|--------|---------|
| `import-sticker-pack.sh` | Import entire Telegram sticker pack |
| `auto-tag-stickers.sh` | Tag stickers by emoji → emotion mapping |
| `random-sticker.sh` | Pick random sticker by tag |
| `check-collection.sh` | View collection stats |

## Files

- `stickers.json` - Your collection + usage data
- `stickers.json.example` - Empty template
- `SKILL.md` - Full documentation

## Usage Philosophy

**Use stickers like humans do:**
- Greetings (goodnight/morning) → always prefer sticker over text
- Celebrations, humor, empathy → great use cases
- Technical answers, reports → skip stickers
- Frequency: ~1 per 2-5 messages (track yourself in agent logic)

## Integration

Read `SKILL.md` for full integration guide with OpenClaw agents.

## License

MIT
