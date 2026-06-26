---
name: slack-block-kit
description: Send rich Slack Block Kit messages — native tables, structured layouts. Use when formatting tabular data for Slack, sending Block Kit payloads, or when markdown tables render poorly in Slack.
---

# Slack Block Kit

Send native Block Kit payloads to Slack. Primary use case: **tables** (Slack's native `table` block type).

## When to Use

- Tabular data in Slack (financial summaries, comparison grids, status dashboards)
- Markdown tables render poorly or not at all in Slack — use Block Kit tables instead

## Sending Block Kit Tables

### Quick Path: `scripts/table.mjs`

Generate table JSON from headers + rows:

```bash
node <skill_dir>/scripts/table.mjs \
  --headers '["Source","Amount","Status"]' \
  --rows '[["Mochary","$11K","Pending"],["MHC","$13.4K","Invoiced"]]' \
  --align '1:right' \
  --compact --blocks-only
```

Options:
- `--headers '["H1","H2"]'` — first row (bold by default)
- `--rows '[["a","b"],["c","d"]]'` — data rows
- `--json '{"headers":[...],"rows":[...]}'` — single JSON input
- `--stdin` — read JSON from stdin
- `--align '<col>:<left|center|right>,...'` — column alignment (0-indexed)
- `--wrap '<col>,...'` — columns to wrap text
- `--no-bold-headers` — plain text headers
- `--compact` — minified JSON
- `--blocks-only` — output just the blocks array (for API calls)

Empty cells are handled automatically (zero-width space).

### Posting to Slack

The `message` tool does not pass `blocks` through. Use the Slack API directly:

```bash
BLOCKS=$(node <skill_dir>/scripts/table.mjs --compact --blocks-only \
  --headers '["Col A","Col B"]' \
  --rows '[["val1","val2"]]')

curl -s -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg channel "$CHANNEL_ID" \
    --arg thread "$THREAD_TS" \
    --argjson blocks "$BLOCKS" \
    '{channel: $channel, thread_ts: $thread, text: "Fallback text", blocks: $blocks}')"
```

The bot token is in `openclaw.json` at `channels.slack.botToken`. The `text` field is required (accessibility fallback) but won't display when blocks render.

### Table Block Constraints

- **1 table per message** (Slack limit)
- **Max 100 rows**, **max 20 columns**
- Cells: `raw_text` (plain) or `rich_text` (bold, links, mentions)
- Empty text is not allowed — the script uses zero-width spaces automatically

### Combining Text + Table

Post your text message first via `message` tool, then post the table in the same thread via curl. Or include a `section` block before the table in the blocks array.

## Manual Block Kit JSON

For non-table blocks or custom layouts, construct the JSON directly. Reference: https://docs.slack.dev/reference/block-kit/blocks/table-block/

Cell with bold text:
```json
{"type": "rich_text", "elements": [{"type": "rich_text_section", "elements": [{"type": "text", "text": "Bold", "style": {"bold": true}}]}]}
```

Plain text cell:
```json
{"type": "raw_text", "text": "Plain"}
```
