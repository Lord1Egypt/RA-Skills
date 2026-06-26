# AI Yearbook Photo Generator

Generate classic ai yearbook photo generator images from a text description using AI. Powered by the Neta talesofai API, this skill returns a direct image URL in seconds — no setup beyond a token required.

---

## Install

**Via npx skills:**
```bash
npx skills add omactiengartelle/yearbook-photo-skill
```

**Via ClawHub:**
```bash
clawhub install yearbook-photo-skill
```

---

## Usage

```bash
# Default prompt (classic 1990s yearbook portrait)
node yearbookphoto.js

# Custom subject/description
node yearbookphoto.js "1990s high school yearbook portrait photo of Emma, soft studio lighting, formal attire"

# With size option
node yearbookphoto.js "senior portrait of a student" --size square

# With a reference image UUID
node yearbookphoto.js "yearbook portrait of Alex" --ref <picture_uuid>

# Pass token directly
node yearbookphoto.js "yearbook photo" --token YOUR_NETA_TOKEN
```

The script prints a single image URL to stdout on success.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--token` | string | — | Neta API token (overrides env/file) |
| `--ref` | picture_uuid | — | Reference image UUID for style inheritance |

### Size dimensions

| Size | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

---

## Token setup

The script resolves your `NETA_TOKEN` in this order:

1. `--token` CLI flag
2. `NETA_TOKEN` environment variable

**Recommended:** add to your shell profile or `.env` file:
```bash
export NETA_TOKEN=your_token_here
```

```
NETA_TOKEN=your_token_here
```

---

## Default prompt

```
1990s high school yearbook portrait photo of {subject}, professional school photography studio, neutral background, soft studio lighting, formal attire, genuine smile, film grain texture, classic yearbook aesthetic
```

## Example Output

![Generated example](https://oss.talesofai.cn/picture/db2a00dc-ad39-4024-bf47-173f9f4f268e.webp)
