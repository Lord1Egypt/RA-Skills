# wine-archive

Personal wine archive — tasting history, label storage, and natural-language recall.

Built for OpenClaw but usable as a standalone Node.js CLI. Stores data locally in SQLite.
No cloud required. Label images are archived on disk.

## Features

- Log wines from free text, structured input, or label images
- Normalized schema: stable wine identities + individual tasting/purchase instances
- Natural-language recall: "what pinot noir did I drink last month?"
- Label image archiving with deduplication
- Telegram bot integration via OpenClaw bridge
- Optional LLM intent classification (Anthropic or OpenAI)
- Export/import for data portability

## Requirements

- Node.js >= 22
- macOS (recommended) — image normalization uses `sips`; Linux/Windows work without auto-resizing
- `ANTHROPIC_API_KEY` — only if using LLM intent classification (off by default)
- OpenClaw CLI — only if using the Telegram bridge

## Setup

```bash
git clone <this-repo> wine-archive
cd wine-archive
zsh setup.sh
```

Or manually:

```bash
npm install
npm run wine:init
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY if desired
```

## Quick start

```bash
# Add a wine from text
npm run wine:add -- --text "Had a Broadbent Vinho Verde from Minho. Bought at Nugget for \$14. Rated 4/5."

# Add with explicit fields
npm run wine:add -- \
  --wine_name "Broadbent Vinho Verde" \
  --varietal "Loureiro" \
  --region "Minho" \
  --color "white" \
  --style "vino verde" \
  --price 14 \
  --place_of_purchase "Nugget" \
  --consumed_on 2026-03-29

# Add from label text
npm run wine:add -- \
  --label-text $'Broadbent\nVinho Verde\n2024\nMinho Portugal\nLoureiro' \
  --image data/wine/labels/broadbent.jpg

# List recent entries
npm run wine:list -- --limit 10

# Query by field
npm run wine:query -- --varietal "Pinot Noir"
npm run wine:query -- --consumed_after 2026-03-01 --consumed_before 2026-03-31

# Natural-language recall
npm run wine:recall -- --text "show me wines from last week at Nugget"
npm run wine:recall -- --text "find red wines rated at least 3"

# Chat-style dispatch (intent detection + response)
npm run wine:chat -- --text "What was that vinho verde I had last week?"
npm run wine:chat -- --text "Remember this: had a Meiomi Pinot Noir last night, rated 3.5/5"

# Remove an entry
npm run wine:remove -- --id 42
```

## Export and import

Transfer your archive to another machine:

```bash
# Export (paths only — also copy data/wine/labels/ manually)
npm run wine:export -- --out my-wines.json

# Export with images embedded as base64 (self-contained, larger file)
npm run wine:export -- --out my-wines.json --include-images

# Preview import without writing
npm run wine:import -- --in my-wines.json --dry-run

# Import
npm run wine:import -- --in my-wines.json
```

When importing without `--include-images` on the export, copy `data/wine/labels/` from the
source machine to the same path on the target before running `wine:import`.

## Telegram bridge

Requires OpenClaw with a configured Telegram bot.

```bash
npm run wine:telegram-bridge -- \
  --text "Show me the Vinho Verde label" \
  --chat-id -1001234567890 \
  --thread-id 42 \
  --reply-to 101

# Shell helper
zsh scripts/wine-send-label-telegram.sh <chat_id> <thread_id> <reply_to> Vinho Verde
```

## LLM intent classification (optional)

By default the chat flow uses a fast regex classifier. To enable LLM-based classification:

```bash
# In .env:
WINE_LLM_INTENT_CLASSIFIER=1
WINE_LLM_INTENT_MODEL=claude-haiku-4   # or openai/gpt-4.1-mini
ANTHROPIC_API_KEY=sk-ant-...
```

## Data location

| Path | Contents |
|---|---|
| `data/wine/wine.sqlite3` | Main database |
| `data/wine/labels/` | Archived label images |
| `data/wine/audit.log` | Append-only audit log |

Override the DB path with `WINE_DB_PATH` env var.

## Platform notes

- **macOS**: Full support including automatic image resizing via `sips`.
- **Linux/Windows**: Everything works except automatic image resizing. To add cross-platform
  resizing: install ImageMagick and adapt `normalizeImageInPlace` in `lib/wine-store.js`.

## Using as an OpenClaw skill

If you have OpenClaw installed, drop this directory under your workspace `skills/` folder.
The `SKILL.md` is the AgentSkill definition and will be picked up automatically.

To publish to ClawHub:
1. Fill in your `ownerId` in `_meta.json`
2. Run `clawhub publish` from this directory

## License

MIT
