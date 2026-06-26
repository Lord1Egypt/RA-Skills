---
name: write-opennote
description: Write, update, and read OpenNote notes through the public API. Use when the user wants to publish notes, upload note images, manage labels, or look up previously written notes.
metadata:
  openclaw:
    requires:
      env:
        - OPENNOTE_API_TOKEN
      bins:
        - curl
    primaryEnv: OPENNOTE_API_TOKEN
---

# Write Note via OpenNote Public API

Write a note to [OpenNote](https://opennote.cc) using the public API at `https://api.opennote.cc/api/v1`.

## Getting Started

### What you need

1. An **OpenNote account** — download the app from the [App Store](https://apps.apple.com/app/opennote-notes-journal/id6450187057)
2. A **Pro subscription** — API access is a Pro feature
3. A **Personal Access Token (PAT)** — generated from the app

### Generating an API token

1. Open the OpenNote app
2. Go to **Profile** → **API Tokens**
3. Tap **Create Token**
4. Choose the scopes you need:
   - `diaries:write` — create and update notes
   - `images:write` — upload images to notes
5. Set an expiration (default: 90 days, max: 365 days, or never)
6. Copy the token immediately — it starts with `milo_pat_v1_` and is **only shown once**

### Setting up the environment variable

Set `OPENNOTE_API_TOKEN` in your OpenClaw environment:

**Option A — OpenClaw config (recommended):**

In your OpenClaw settings, add the environment variable:
```
OPENNOTE_API_TOKEN=milo_pat_v1_your_token_here
```

**Option B — Shell profile (if running locally):**
```bash
export OPENNOTE_API_TOKEN="milo_pat_v1_your_token_here"
```

Add this to your `~/.zshrc` or `~/.bashrc` to persist it across sessions.

**Security:**
- Never commit your token to version control
- The token grants write access to your notes — treat it like a password
- If compromised, revoke it immediately from **Profile** → **API Tokens** in the app

### Token lifecycle

- Tokens expire based on the duration you set (default 90 days)
- You can have up to **5 active tokens** per account
- Revoke unused tokens from the app at any time
- When a token expires or is revoked, generate a new one and update `OPENNOTE_API_TOKEN`
- If you get a `401 INVALID_API_TOKEN` error, your token has expired or been revoked

## Prerequisites

The token is read from the `OPENNOTE_API_TOKEN` environment variable. It must have the `diaries:write` scope. If images will be uploaded, `images:write` is also required.

## Local Cache Files

This skill maintains two local files in the working directory under `.opennote/`:

- **Labels cache**: `.opennote/opennote-labels-cache.json` — cached user labels
- **Note history**: `.opennote/opennote-history.json` — log of all notes written/edited via this skill

Always read these files at the start of every invocation. If they are missing, treat them as empty. If the user asks about previously written notes, consult the history file.

## Instructions

### Step 1: Load labels (fetch or use cache)

Read `.opennote/opennote-labels-cache.json`. If it exists and was fetched less than 24 hours ago, use the cached labels.

Expected cache format:
```json
{
  "fetchedAt": 1741111111111,
  "labels": [
    { "categoryID": 1, "categoryName": "Personal", "categoryColor": 4294198070 },
    { "categoryID": 2, "categoryName": "Work", "categoryColor": 4283215696 }
  ]
}
```

If the cache is missing, empty, or stale (older than 24 hours), fetch labels from the API:

```bash
curl -s "https://api.opennote.cc/api/v1/labels" \
  -H "Authorization: Bearer $OPENNOTE_API_TOKEN"
```

Response:
```json
{
  "labels": [
    { "categoryID": 1, "categoryName": "Personal", "categoryColor": 4294198070, "visibility": true, "coverImageName": null, "lastModified": 1741111111111, "fontFamily": null, "backgroundPreset": null }
  ]
}
```

After fetching, write the result to `.opennote/opennote-labels-cache.json` with the current timestamp as `fetchedAt`.

### Step 2: Choose a label/category

- If the user specified a label by name or ID, use that `categoryID`.
- If the user did NOT specify a label, pick a **random** label from the cached label list.
- If no labels are cached at all, use `category: 0` (no label).

When picking a random label, tell the user which label was selected.

### Step 3: Gather note content from the user

Ask the user what they want to write about. Collect:

- The note text content (required)
- Optional: a title
- Optional: whether they want stickers added
- Optional: whether they want images (user must provide image files)

### Step 4: Generate timestamps and fileName

```js
const now = Date.now(); // Unix milliseconds
const fileName = `${now}.json`;
```

### Step 5: Build the richContent (Quill Delta JSON string)

Build a Quill Delta array of ops, then `JSON.stringify()` it into the `richContent` field.

#### Supported Quill Delta operations

**Plain text:**
```json
{ "insert": "Hello world" }
```

**Newline (required - every Delta must end with at least one):**
```json
{ "insert": "\n" }
```

**Inline styles (on text insert):**
- `bold` (boolean)
- `italic` (boolean)
- `underline` (boolean)
- `strike` (boolean)
- `color` (hex string like `"#2a7fff"`) — use the palette below for best results
- `size` (number, typically 2-99; app default is 17)

```json
{ "insert": "Important", "attributes": { "bold": true, "color": "#ff0000", "size": 20 } }
```

**Available color palette (36 colors):**

Always store the **light-mode hex** — the app remaps it automatically when rendering in dark mode.

| Name | Light-mode hex |
|------|---------------|
| Black | `#000000` |
| Charcoal | `#545454` |
| Dark Grey | `#616161` |
| Warm Slate | `#455a64` |
| Crimson | `#b71c1c` |
| Deep Red | `#c0392b` |
| Brick | `#bf360c` |
| Dark Amber | `#a04000` |
| Mustard | `#9a6e00` |
| Dark Olive | `#558b2f` |
| Forest Green | `#2e7d32` |
| Deep Gold | `#8b6914` |
| Dark Teal | `#00695c` |
| Dark Cyan | `#00838f` |
| Royal Blue | `#1565c0` |
| Blue | `#007aff` |
| Indigo | `#5856d6` |
| Deep Purple | `#6a1b9a` |
| Magenta | `#e91e63` |
| Pink | `#ff2d55` |
| Berry | `#880e4f` |
| Plum | `#6a0572` |
| Dark Violet | `#4a148c` |
| Brown | `#8d6e63` |
| Red | `#ff3b30` |
| Dark Rose | `#ad1457` |
| Terracotta | `#8b3a1f` |
| Sea Green | `#007a63` |
| Midnight | `#1a237e` |
| Deep Sage | `#2e5902` |
| Ochre | `#7a5c00` |
| Steel Grey | `#37474f` |
| Wine | `#8b0000` |
| Mahogany | `#6d2f1f` |
| Deep Sea | `#005b72` |
| Dark Coffee | `#4e342e` |

**Block/line styles (attached to the newline op after the line):**
- `align`: `"left"`, `"center"`, `"right"`
- `indent`: integer
- `list`: `"ordered"`, `"bullet"`, `"checked"`, `"unchecked"`
- `code-block`: `true`
- `blockquote`: `true`

```json
{ "insert": "A bullet point" },
{ "insert": "\n", "attributes": { "list": "bullet" } }
```

**Image embed:**
```json
{ "insert": { "image": "{\"src\":\"my_photo.jpg\",\"w\":1920,\"h\":1080}" } }
```

If dimensions are unknown:
```json
{ "insert": { "image": "my_photo.jpg" } }
```

**Collage embed (multi-image layout):**
```json
{
  "insert": {
    "collage": "{\"layout\":\"twoHorizontal\",\"images\":[\"img1.jpg\",\"img2.jpg\"]}"
  }
}
```

Available collage layouts: `twoHorizontal` (2), `bigLeft2Right` (3), `bigRight2Left` (3), `threeRow` (3), `bigLeft2RectRight` (3), `bigTop2Bottom` (3), `bigLeftTopRect2Bottom` (4), `grid2x2` (4)

**Divider embed:**
```json
{ "insert": { "divider": "split" } }
```

#### Example richContent value

The API field `richContent` must be a **JSON string** (not an object):

```json
"[{\"insert\":\"My Title\\n\",\"attributes\":{\"bold\":true,\"size\":24}},{\"insert\":\"Today was a great day.\\n\"},{\"insert\":{\"image\":\"photo.jpg\"}},{\"insert\":\"\\n\"}]"
```

### Step 6: Build the content field (plain text)

`content` is a plain-text summary used for home screen preview and search. Strip all formatting — just include the text. Do NOT put JSON or markdown here.

### Step 7: Build stickerData (optional)

`stickerData` is a JSON string (not an object) containing an array of sticker overlay objects. Stickers float on top of the note page and are NOT part of `richContent`.

Each sticker object:
```json
{
  "id": "unique_hex_id",
  "assetPath": "assets/stickers/bunny.svg",
  "dx": 150.0,
  "dy": 200.0,
  "normalizedDx": 0.39,
  "normalizedDy": 0.25,
  "scale": 1.0,
  "rotation": 0.0
}
```

Field rules:
- `id`: unique string, format `<hex_timestamp>_<6char_hex_random>`
- `assetPath`: must be an exact match from the bundled sticker list below
- `dx`, `dy`: pixel offsets from top-left of note canvas (typical canvas ~390px wide)
- `normalizedDx`, `normalizedDy`: proportional position (0.0–1.0 for dx; dy can exceed 1.0 for long content)
- `scale`: 0.3 to 4.0 (1.0 = default 70px base size)
- `rotation`: radians

Example `stickerData` field value:
```json
"[{\"id\":\"18f0c9d2_a1b2c3\",\"assetPath\":\"assets/stickers/bunny.svg\",\"dx\":150.0,\"dy\":200.0,\"normalizedDx\":0.39,\"normalizedDy\":0.25,\"scale\":1.0,\"rotation\":0.0}]"
```

#### Available sticker asset paths

**Kawaii:**
```
assets/stickers/backpack.svg       assets/stickers/bird.svg
assets/stickers/book.svg           assets/stickers/bunny.svg
assets/stickers/burger.svg         assets/stickers/cake_slice.svg
assets/stickers/cat.svg            assets/stickers/cheese.svg
assets/stickers/chicken.svg        assets/stickers/clapboard.svg
assets/stickers/crown.svg          assets/stickers/flower_2.svg
assets/stickers/frog.svg           assets/stickers/garland.svg
assets/stickers/gramophone.svg     assets/stickers/hat.svg
assets/stickers/heart_2.svg        assets/stickers/kiwi.svg
assets/stickers/kitten.svg         assets/stickers/little_girl.svg
assets/stickers/little_girl_2.svg  assets/stickers/meals.svg
assets/stickers/muffin.svg         assets/stickers/piggy_bank.svg
assets/stickers/pizza.svg          assets/stickers/plant.svg
assets/stickers/pop_corn.svg       assets/stickers/rabbit.svg
assets/stickers/rabbit_2.svg       assets/stickers/saturn.svg
assets/stickers/shooting_star.svg  assets/stickers/skirt.svg
assets/stickers/soda_can.svg       assets/stickers/strawberry.svg
assets/stickers/symbol.svg         assets/stickers/tea_pot.svg
assets/stickers/ufo.svg            assets/stickers/wallet.svg
assets/stickers/watermelon.svg     assets/stickers/watermelon_2.svg
```

**Animals:** `assets/stickers/animals/001-crocodile.svg` through `040-hippopotamus.svg` (040 total)

**Nature:** `assets/stickers/nature/001-sunflower.svg` through `024-tree.svg` (024 total)

**Characters:** `assets/stickers/characters/girl_001-girl.svg` through `girl_020-girl.svg`, `hippie_001-hippie.svg` through `hippie_020-dj.svg`

**Food:** `assets/stickers/food/misc_001-meat.svg` through `misc_020-dolphin.svg`, `k760_001-cat.svg` through `k760_020-ice_cream.svg`, `k791_001-cat.svg` through `k791_020-book.svg`

**Cute Life:** `assets/stickers/cute_life/k678_001-badge.svg` through `k678_020-vinyl_record.svg`, `k612_001-teddy_bear.svg` through `k612_020-yogurt.svg`, `k155_001-egg_and_bacon.svg` through `k155_020-rainbow.svg`

**Everyday:** `assets/stickers/everyday/k448_001-cake.svg` through `k448_020-violin.svg`, `k450_001-backpack.svg` through `k450_020-turtle.svg`

### Step 8: Upload images (if any)

If the note includes images, upload each one first:

```bash
curl -s -X POST "https://api.opennote.cc/api/v1/images" \
  -H "Authorization: Bearer $OPENNOTE_API_TOKEN" \
  -F "image=@/path/to/photo.jpg"
```

Response:
```json
{ "imageName": "photo.jpg", "sizeInMB": 0.42 }
```

Use the returned `imageName` in `imageList`, `richContent` image embeds, and optionally `diaryCoverImageName`.

Image constraints:
- Supported types: jpg, jpeg, png, gif, webp, heic, heif
- Max size: 15 MB per image
- User storage quota applies

### Step 9: Assemble and send the API request

```bash
curl -s -X POST "https://api.opennote.cc/api/v1/diaries" \
  -H "Authorization: Bearer $OPENNOTE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fileName": "<timestamp>.json",
    "time": <timestamp>,
    "content": "<plain text summary>",
    "richContent": "<JSON string of Quill Delta ops>",
    "stickerData": "<JSON string of sticker array or null>",
    "diaryCoverImageName": null,
    "category": <categoryID>,
    "title": "<optional title>",
    "imageList": [],
    "isDeleted": false,
    "lastModified": <timestamp>,
    "hideTitle": false
  }'
```

If the API returns `409 ALREADY_EXISTS`, retry with PUT:

```bash
curl -s -X PUT "https://api.opennote.cc/api/v1/diaries/<fileName>" \
  -H "Authorization: Bearer $OPENNOTE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "content": "...", "richContent": "...", "lastModified": <now> }'
```

### Step 10: Record to note history

After a successful create or update, append an entry to `.opennote/opennote-history.json`.

Read the existing file first (or start with an empty array `[]` if it doesn't exist), then append and write back.

Each history entry format:
```json
{
  "fileName": "1741111111111.json",
  "action": "created",
  "timestamp": 1741111111111,
  "title": "Morning Walk",
  "contentPreview": "Woke up early and went for a walk in the park...",
  "categoryID": 2,
  "categoryName": "Personal",
  "hasStickers": true,
  "hasImages": false,
  "imageList": []
}
```

Rules for the history:
- `action`: either `"created"` or `"updated"`
- `contentPreview`: first 150 characters of the plain text `content`
- `categoryName`: look up from cached labels, or `"No Label"` if category is 0
- `hasStickers`: true if stickerData was non-null
- `hasImages`: true if imageList is non-empty
- For updates, add a new entry with `action: "updated"` (do not overwrite previous entries)

### Step 11: Confirm to the user

Tell the user:
- The note was created/updated successfully
- The fileName
- Which label was used (and whether it was randomly selected)
- A brief summary of the content

## Reading Notes from the API

When the user asks to read, search, or use an existing note as a template, use the read endpoints (requires `diaries:read` scope on the token).

> **Note:** The `diaries:read` scope may not yet be available when creating tokens from the app. If you get a `403 INSUFFICIENT_SCOPE` error on read endpoints, the token doesn't have this scope. Writing notes and fetching labels will still work.

### List notes

```bash
curl -s "https://api.opennote.cc/api/v1/diaries?category=CATEGORY_ID&search=KEYWORD&limit=50&offset=0" \
  -H "Authorization: Bearer $OPENNOTE_API_TOKEN"
```

Query parameters (all optional):
- `category` — filter by categoryID (integer)
- `search` — search in content and title (partial match)
- `limit` — results per page, 1–200, default 50
- `offset` — pagination offset, default 0

Response:
```json
{
  "diaries": [ { "fileName": "...", "time": ..., "content": "...", "richContent": "...", ... } ],
  "total": 42,
  "limit": 50,
  "offset": 0
}
```

### Get a single note

```bash
curl -s "https://api.opennote.cc/api/v1/diaries/FILENAME.json" \
  -H "Authorization: Bearer $OPENNOTE_API_TOKEN"
```

## Looking Up Previous Notes

When the user asks about notes they've previously written (e.g., "what did I write last time?", "find my note about X"), read `.opennote/opennote-history.json`. You can match by:
- `title` (partial match)
- `contentPreview` (keyword search)
- `categoryName` (label name)
- `timestamp` (date range)
- `fileName` (exact match)

Report matching entries with their title, content preview, date, and label.

## Validation Rules

Before sending, validate:

1. `richContent` must be either JSON `null` or a **JSON string** that parses into an array where every element has an `insert` key.
2. Never put plain text, markdown, `"NULL"`, `"null"`, or empty string `""` into `richContent`.
3. `content` must be plain text (for preview/search), not JSON.
4. `imageList` must contain filename-only entries and include all image filenames from `richContent` embeds.
5. Use Unix **milliseconds** for `time` and `lastModified`.
6. `stickerData` must be either omitted, `null`, or a JSON string parsing to an array of valid sticker objects.
7. Each sticker must use an exact `assetPath` from the bundled sticker list above.
8. Sticker `scale` should be between 0.3 and 4.0.
