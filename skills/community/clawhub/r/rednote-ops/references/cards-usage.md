# Usage

## Generate SVG + PNG cards

```bash
node skills/xiaohongshu-ops/scripts/generate_xhs_cards.js \
  skills/xiaohongshu-ops/references/cards-input-example.json \
  /tmp/openclaw/uploads/xhs_generated_cards \
  /tmp/openclaw/uploads/xhs_generated_cards/png
```

## Input format

JSON array of pages:
- `title`
- `subtitle` (optional)
- `bullets` (optional, up to 4 recommended)
- `footer` (optional)

## Output

- One SVG file per page
- One PNG file per page
- Portrait card layout for Xiaohongshu image notes

## Next step

Feed the PNG directory into the consolidated `xiaohongshu-ops` publish flow for upload.
