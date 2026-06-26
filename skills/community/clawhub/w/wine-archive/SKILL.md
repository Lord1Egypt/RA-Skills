# Wine Archive

Personal wine archive for tasting history, label storage, and natural-language recall.
Stores wines in a local SQLite database with a normalized schema: stable wine identities
plus individual tasting/purchase instances. Integrates with Telegram via the OpenClaw bridge.

## Trigger phrases

Use this skill when the user says things like:
- "remember this wine", "log this bottle", "add a wine", "save this tasting"
- "what wine did I have last week?", "show me my pinot noirs", "recall wines from Nugget"
- "show the [wine name] label", "send me the Vinho Verde photo"
- "show me the [wine name]", "tell me about the Broadbent"
- "export my wine archive", "import wine data"

## Setup (first time)

```bash
cd skills/wine-archive
zsh setup.sh
```

Or manually:

```bash
cd skills/wine-archive
npm install
npm run wine:init
cp .env.example .env   # add ANTHROPIC_API_KEY for LLM features
```

Data is stored in `data/wine/wine.sqlite3` and label images in `data/wine/labels/`.
Override the DB location with `WINE_DB_PATH` env var.

## Core rules

- Personal ratings use a **5-star scale**.
- Prefer **new tasting instances** over overwriting when the user re-tries a wine.
- If it is ambiguous whether to update an existing instance or create a new one, ask.
- Keep deterministic regex parsing as the source of truth; LLM parsing is assistive only.
- Archived label images are durable — never rely on temporary inbound media paths.
- On Telegram, use the bridge path for label recall rather than inline `MEDIA:` text.

## Data model

**Wine** = stable identity
- producer, wine_name, region, country, style, color, varietal
- official_rating / official_rating_source
- label image (default_source_image_path)

**Wine instance** = specific bottle / tasting event
- vintage, price, currency, place_of_purchase
- purchased_on, consumed_on
- subjective_rating (5-star), notes
- source_type (chat | image | manual)

## Commands

Initialize DB:
```bash
npm run wine:init
```

Add from free text:
```bash
npm run wine:add -- --text "Had a Broadbent Vinho Verde from Minho. Bought at Nugget for $14. Rated 4/5."
```

Add structured:
```bash
npm run wine:add -- --wine_name "Broadbent Vinho Verde" --varietal "Loureiro" --region "Minho" \
  --style "vino verde" --color "white" --price 14 --place_of_purchase "Nugget" --consumed_on 2026-03-29
```

Add from label text + image:
```bash
npm run wine:add -- --label-text $'Broadbent\nVinho Verde\n2024\nMinho Portugal\nLoureiro' \
  --image data/wine/labels/broadbent.jpg
```

Parse label without inserting:
```bash
npm run wine:parse-label -- --label-text $'Broadbent\nVinho Verde\n2024\nMinho Portugal'
```

Query:
```bash
npm run wine:query -- --text "vinho verde"
npm run wine:query -- --varietal "Pinot Noir"
npm run wine:query -- --consumed_after 2026-03-24 --consumed_before 2026-03-31
```

Natural-language recall:
```bash
npm run wine:recall -- --text "show me wines from last week at Nugget"
npm run wine:recall -- --text "what pinot noir did I drink last month"
npm run wine:recall -- --text "find red wines rated at least 3"
```

Chat-facing flow (intent detection + dispatch):
```bash
npm run wine:chat -- --text "Remember this wine: Had a vinho verde last week. Rated 4/5."
npm run wine:chat -- --text "What was that vinho verde I had last week?"
npm run wine:chat -- --label-text $'Broadbent\nVinho Verde\n2024\nMinho' --image data/wine/labels/broadbent.jpg
```

List recent entries:
```bash
npm run wine:list -- --limit 10
```

Remove an entry:
```bash
npm run wine:remove -- --id 42
```

Export archive:
```bash
npm run wine:export -- --out my-wines.json              # paths only
npm run wine:export -- --out my-wines.json --include-images  # embed label images as base64
```

Import archive:
```bash
npm run wine:import -- --in my-wines.json --dry-run    # preview only
npm run wine:import -- --in my-wines.json               # import
```

## Telegram bridge (requires OpenClaw)

The bridge script resolves the wine chat request and outputs a structured JSON result.
When `action === "send-media"`, the agent sends the media using the `openclaw` CLI.

```bash
npm run wine:telegram-bridge -- --text "Show me the Vinho Verde label"
```

Example output when a label is found:
```json
{
  "status": "ok",
  "action": "send-media",
  "reply": "Broadbent Vinho Verde label",
  "mediaPath": "./data/wine/labels/broadbent-abc123.jpg",
  "caption": "Vinho Verde label"
}
```

The agent then sends:
```bash
openclaw message send --channel telegram \
  --target <chat_id> --thread-id <thread_id> --reply-to <reply_to> \
  --media <mediaPath> --message <caption>
```

Shell helper (outputs JSON for the agent):
```bash
zsh scripts/wine-send-label-telegram.sh <chat_id> <thread_id> <reply_to> Vinho Verde
```

## Response templates

### Add / save confirmation
```
Added as a new wine instance:
- Broadbent Vinho Verde · 2024
- Nugget, $14.00 · consumed 2026-03-29
- rated 4/5
```

### Update confirmation
```
Updated — rating: 3.5/5, consumed_on: 2026-04-02
```

### Show a wine (canonical entry)
```
Broadbent — Vinho Verde
- region: Minho
- country: Portugal
- style: vino verde
- color: white
- varietal: Loureiro
[label image]
```

### Show wine instances
```
Broadbent — Vinho Verde (2024)
- consumed: 2026-03-29
- rated: 4/5
- notes: crisp, slightly frizzante
```

### Show a list of wines
```
- Vinho Verde
  producer: Broadbent
  year: 2024
  varietal: Loureiro
  style: vino verde
```

### Recall by time window
```
Broadbent — Vinho Verde (2024)
- consumed: 2026-03-29
- rated: 4/5
```

### Label response
Send the archived image with caption: `Vinho Verde label`

### Clarification (ambiguous intent)
```
Do you want me to update the existing instance or create a new tasting instance?
```

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Required when using an Anthropic model for LLM intent classification |
| `OPENAI_API_KEY` | — | Required when using an OpenAI model for LLM intent classification |
| `WINE_DB_PATH` | `data/wine/wine.sqlite3` | Override DB location |
| `WINE_LLM_INTENT_CLASSIFIER` | `0` | Set to `1` to enable LLM intent classification (off by default; skill works fully offline without it) |
| `WINE_LLM_INTENT_MODEL` | `openai/gpt-4.1-mini` | Model for intent classification — use `claude-haiku-4` for Anthropic, `openai/gpt-4.1-mini` for OpenAI |
| `WINE_LLM_INTENT_MIN_CONFIDENCE` | `0.65` | Minimum confidence to use LLM over regex |

## Platform notes

- **macOS**: Full support including image normalization via `sips`.
- **Linux/Windows**: Core features work. Image resizing is skipped (install ImageMagick
  and adapt `lib/wine-store.js` `normalizeImageInPlace` for cross-platform resizing).
- **Node.js >= 22** required (`node:sqlite` built-in used in `shared/interaction-store.js`).
