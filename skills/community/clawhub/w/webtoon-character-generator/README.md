# Webtoon Character Generator

Generate manhwa-style character portraits and webtoon OCs from text descriptions — clean line art, highly expressive large eyes, vibrant saturated colors, and the modern Korean webtoon aesthetic, all powered by AI.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add omactiengartelle/webtoon-character-generator
```

**Via ClawHub:**
```bash
clawhub install webtoon-character-generator
```

---

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

```bash
node webtooncharactergenerator.js "DESCRIPTION" --token YOUR_TOKEN [options]
```

If no description is provided, a default webtoon portrait prompt is used.

### Examples

```bash
# Female protagonist with silver hair and glowing blue eyes
node webtooncharactergenerator.js "female protagonist, silver hair, glowing blue eyes, school uniform, confident expression, webtoon style" --token "$NETA_TOKEN"

# Dark fantasy warrior character
node webtooncharactergenerator.js "dark fantasy male warrior, scar on cheek, black armor, dramatic lighting, webtoon manhwa style" --token "$NETA_TOKEN"

# Landscape orientation
node webtooncharactergenerator.js "cute magical girl, pastel colors, star wand, webtoon style" --token "$NETA_TOKEN" --size landscape

# Tall portrait for a full-body webtoon panel
node webtooncharactergenerator.js "villain character, purple coat, menacing smile, webtoon style" --token "$NETA_TOKEN" --size tall

# Use a reference image UUID for style inheritance
node webtooncharactergenerator.js "same character, summer outfit" --token "$NETA_TOKEN" --ref abc123-uuid-here
```

### Output

Returns a direct image URL.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | — | **(Required)** Your Neta API token |
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--ref` | UUID string | — | Reference image UUID for style inheritance |

### Size Dimensions

| Size | Width | Height |
|------|-------|--------|
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `square` | 1024 | 1024 |
| `tall` | 704 | 1408 |

---

## Tips for Better Results

- Describe hair color, eye color, outfit, and expression for detailed characters.
- Include style keywords like `webtoon style`, `manhwa aesthetic`, or `Korean comic style`.
- Add mood or lighting cues: `dramatic lighting`, `soft glow`, `backlit`.
- Use `--size tall` for full-body shots suited to webtoon panel layouts.
- Use `--ref` with a previously generated character's UUID to maintain visual consistency across images.

