# `.tiervibe.json` Authoring Format

The single file the TierListMaker skill produces. The user imports it at
`https://tiervibe.com/t/import`. The TierVibe editor's local reader validates it,
flattens it into its internal load format, and feeds the editor's existing load
pipeline. **No server calls happen at import time** — the file is parsed entirely
client-side; nothing reaches the server until the user clicks 发布 (Publish).

## Full schema

```jsonc
{
  // REQUIRED. The post title. Non-empty, ≤ 200 chars. The publish endpoint
  // rejects an empty title, so set it even if the user plans to tweak it later.
  "title": "AI Coding Models — 从夯到拉",

  // OPTIONAL. Whole-board background brightness. Number 0..100.
  // 0 = near-black (#181818), 100 = white, linear gray in between.
  // There is NO per-tier background — this single value controls the entire board.
  // Default if omitted: 0 (dark).
  "bgBrightness": 0,

  // OPTIONAL. Board layout. "horizontal" (default) or "vertical".
  "layoutMode": "horizontal",

  // REQUIRED. The ranked tiers, top to bottom. 1..15 items.
  "tiers": [
    {
      // REQUIRED. Tier label shown on the title bar. ≤ 100 chars.
      "name": "夯",

      // REQUIRED. Title-bar background color. Hex string, with or without '#'.
      "color": "#FF0000",

      // OPTIONAL. Title font size in px. Default 24. Omit unless the user wants
      // custom sizing (henz uses 72/56/36/48/36).
      "fontSize": 72,

      // OPTIONAL. Cards placed in this tier, left-to-right order.
      "cards": [
        {
          "type": "text",
          "text": "GPT-4",
          "textColor": "#ffffff",
          "bgColor": "#e11d48",
          "detail": "Strong at multi-file refactors; pricey but reliable for hard tasks."
        },
        {
          "type": "image",
          "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg",
          "label": "Claude",
          "detail": "Best long-context reasoning; great for prose and careful code."
        }
      ]
    }
    // ...more tiers...
  ],

  // OPTIONAL. Unranked cards the user will drag into tiers later. The reader
  // round-robins these into the editor's three candidate columns (C1/C2/C3).
  "candidates": [
    { "type": "text", "text": "待定项", "detail": "" }
  ]
}
```

## Card shape

Every card is one of two types:

### Text card
```jsonc
{
  "type": "text",            // REQUIRED, must be "text"
  "text": "GPT-4",           // REQUIRED, non-empty. The visible label.
  "textColor": "#ffffff",    // OPTIONAL. Hex. Font color.
  "bgColor": "#e11d48",      // OPTIONAL. Hex. Card background.
  "detail": "markdown..."    // OPTIONAL. Explanation (see explanations.md).
}
```
- `text` is encoded into the editor's `text:<encoded>` card protocol.
- **Colors come as a pair or not at all**: if you provide `textColor` you must
  also provide `bgColor`, and vice versa. If you provide only one, the reader
  drops both and the editor auto-picks from its palette.
- Skill policy (`SKILL.md` Step 4 rule 3) is to **provide both on every text
  card** — the auto-palette produces a flat, uniform row.
- Keep `text` short (a label, not a paragraph). The card is a small square.

### Image card
```jsonc
{
  "type": "image",            // REQUIRED, must be "image"
    "imageUrl": "https://... or data:image/...",  // REQUIRED. http(s) URL OR data:image/ base64. See below.
  "label": "Claude",          // OPTIONAL, human-readable only; NOT stored on the card.
  "detail": "markdown..."     // OPTIONAL. Explanation.
}
```
- `imageUrl` is stored as-is. External http(s) images remain external. Embedded
  `data:image/...;base64,` images behave like files added with the editor's own local-image button: they display immediately after import, and publish uploads them to the platform CDN.
- `data:image/...;base64,` URLs ARE allowed (reader accepts them; the editor's own "add local image" produces them, and publish uploads them to CDN). Raw `file:` paths are still invalid, but do not tell users to upload local files to a public image host when you can read and embed the files as `data:image/`. `blob:` and non-image `data:` URLs are rejected - use an https URL or a `data:image/` URL, or switch to a text card.

## Validation rules (the reader enforces these)

| Field | Rule |
|---|---|
| `title` | non-empty string, ≤ 200 chars |
| `bgBrightness` | if present, number 0..100 |
| `layoutMode` | if present, `"horizontal"` or `"vertical"` |
| `tiers` | non-empty array, length 1..15 |
| `tiers[].name` | non-empty string, ≤ 100 chars |
| `tiers[].color` | hex color, e.g. `#FF0000` or `FF0000` (3–8 hex digits) |
| `tiers[].fontSize` | if present, positive number |
| `tiers[].cards` | if present, array of cards |
| `candidates` | if present, array of cards |
| text card `text` | non-empty |
| image card `imageUrl` | non-empty, starts with `http://`/`https://` or `data:image/...;base64,` |
| `detail` | trimmed; empty string is dropped (treated as "no explanation") |
| **total cards** | **sum of every `tiers[].cards` plus `candidates` must be ≤ 200** — the reader rejects with `too many cards (N); max 200` |

On any violation the import page shows the error message and stays on the page
(nothing is imported, nothing is sent to the server). Fix the file and re-import.

## Size limits when auto-opening via `#data=`

The import page also accepts the board in the URL hash — `/t/import#data=<base64>` (standard base64 of the UTF-8 JSON, then `encodeURIComponent`; NOT base64url; see `SKILL.md`),
which is how the skill hands off. Two caps apply there:

- The reader rejects the payload past **2,000,000 characters** of the percent-encoded base64.
- Well before that, the **shell's command-line limit** binds. See the table in
  `SKILL.md` → "Emit + auto-open"; the tight one is cmd.exe / Git Bash at 8,191
  characters. Past your shell's ceiling, save the file and let the user drop it
  on the import page instead.

As a rule of thumb the URL runs about **1.4×** the JSON's UTF-8 byte count.

## What is NOT supported (do not emit)

- Per-tier background colors. Only the single global `bgBrightness`.
- More than 15 tiers.
- `blob:` image URLs, and non-image `data:` URLs (`data:image/` IS supported).
- Raw HTML in `detail` (it's escaped, not rendered).
- Nested tiers, sub-tiers, or card ordering beyond array order.
- Draft vs publish flag — the file always opens as a draft in the editor; the
  user chooses 发布 themselves.
