# Text & Image Cards

## Text cards

A text card is a small square showing a label. Most reliable — no network, no
CORS, no missing-image risk. **Which mode (text vs image) you use is decided in
Step 0 of the interview** (`SKILL.md`); this file covers the mechanics of each
card type once that choice is made. When text mode is chosen — or when an image
can't be cleanly obtained — use a text card.

### Color protocol
- **Provide `textColor` AND `bgColor` on every text card** — that's the Step 4
  policy in `SKILL.md`. Omitting them is mechanically legal but hands the board to
  the editor's auto-palette, which reads as a flat uniform row.
- Colors are all-or-nothing: if you provide only one, the reader drops **both**
  and falls back to the auto-palette. So: pair, or (reluctantly) neither.
- The reader encodes the pair into the card's stored `imageUrl` as
  `text:<encoded>#<fgHex>#<bgHex>` (hex without `#`).
- Hex colors: 3–8 hex digits, with or without leading `#`.
- Readability is the hard constraint — see `references/tier-config.md` →
  "Color tips for cards".

### Sizing the text

**Hard numbers: ≤6 CJK characters, ≤12 Latin characters.** "Keep it short" is too
vague to act on. Past that the label wraps and the card's auto-fit shrinks it
until it's hard to read — real examples that wrapped on a finished board:
`美式橄榄球 NFL`, `滑雪 / 单板`, `NASCAR 赛车`.

The card auto-fits font size to the text length, so a long label never overflows
— it just goes small. When the full name doesn't fit:

- put the **short form on the card** (`NFL`, `滑雪`, `NASCAR`)
- put the **full name in `detail`**, where there's room for it

If a card needs a description, that's `detail` (the explanation), never `text`.

## Image cards (optional, with a caveat)

```jsonc
{ "type": "image", "imageUrl": "https://... or data:image/...", "label": "Claude", "detail": "..." }
```

- `imageUrl` must be either:
  - a real `http://` or `https://` URL, OR
  - a `data:image/<mime>;base64,...` URL when the agent can read the user's local image file and embed it.
  Raw `file:` paths still cannot work in browser import, and `blob:` is session-only, so both are rejected.
- `label` is human-readable only and is **not stored** on the card. It's there
  so you and the user can keep track of which image is which. The user identifies
  the card in the editor by its image.
- External `https://` image URLs are **placeholder/suggestions**. Do NOT download or upload.
  If the user has local files and you can read them, prefer embedding `data:image/`
  in the JSON instead of telling the user to upload the files to a public image host.
  If a local image is transparent or semi-transparent, preserve alpha: use WebP/PNG
  `data:image/` and never flatten it with `convert("RGB")` or JPEG, because JPEG
  cannot store alpha and creates black/white halos around transparent pixels.
  If you cannot read the files or find a clean URL, switch the card to a text card.

### The cover-canvas caveat (why images are "user's local behavior")
At publish time the editor renders the whole board to a canvas for the cover
thumbnail. If a card image is a cross-origin URL whose host does **not** send
`Access-Control-Allow-Origin`, the canvas is "tainted" and the publish can fail.
The platform's own CDN images are CORS-clean; random external images often are
not. So:

- Treat external image URLs as placeholders the user may swap.
- Embedded `data:image/` URLs from readable local files are first-class local-image cards: the imported image shows immediately, and publish uploads it to the platform CDN.
- The user can replace any image in the editor with their own local file (the
  editor uploads it to the platform CDN → guaranteed clean).
- You do **not** handle any of this — it's the user's local editor action.
  Just supply a reasonable URL or use a text card.

## When to use which
- Label-style items (model names, dish names, book titles) → **text card**.
- Items where the image IS the point (a specific character, a logo, a photo) →
  image card. Prefer `data:image/` for readable local files; use `https://` links
  for public images; use text placeholders + manifest only when you cannot read the local files.
- Not sure → text card. The user can always add images themselves in the editor.
