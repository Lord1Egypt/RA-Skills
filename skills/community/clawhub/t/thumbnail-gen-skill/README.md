# YouTube Thumbnail Generator

> Powered by the **Neta AI image generation API** (`api.talesofai.com`) — the same service as [neta.art](https://www.neta.art/open/).

Generate eye-catching, AI-powered YouTube thumbnails from a text description. Returns a direct image URL instantly — no sign-up required beyond your Neta API token.

---

## Install

**Via npx skills:**
```bash
npx skills add SherriHidalgolt/thumbnail-gen-skill
```

**Via ClawHub:**
```bash
clawhub install thumbnail-gen-skill
```

---

## Usage

```bash
# Basic — uses default prompt
node thumbnailgen.js

# Custom prompt
node thumbnailgen.js "gaming channel thumbnail, neon lights, intense action scene"

# Specify size
node thumbnailgen.js "tech review thumbnail" --size landscape

# Use a reference image UUID
node thumbnailgen.js "similar style thumbnail" --ref abc123-uuid-here

# Pass token inline
node thumbnailgen.js "travel vlog thumbnail" --token YOUR_TOKEN_HERE
```

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `landscape` | Output image dimensions |
| `--token` | string | — | Neta API token (required) |
| `--ref` | UUID string | — | Reference image UUID for style inheritance |

### Size dimensions

| Name | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

---

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Examples

```bash
# YouTube gaming thumbnail
node thumbnailgen.js "epic gaming thumbnail, fire and lightning, bold title text area, dark background"

# Cooking channel
node thumbnailgen.js "food thumbnail, delicious pasta closeup, warm lighting, restaurant quality"

# Tech review
node thumbnailgen.js "product review thumbnail, smartphone on desk, clean modern background, professional"
```

Each command prints a direct image URL to stdout on success.

---

## Default prompt

If no prompt is provided, the skill uses:
```
youtube thumbnail, bold colors, eye-catching design, professional
```

## Example Output

![Generated example](https://cdn.talesofai.com/picture/182e7357-7c6f-4b9a-9708-373ea38ccd4a.webp)
