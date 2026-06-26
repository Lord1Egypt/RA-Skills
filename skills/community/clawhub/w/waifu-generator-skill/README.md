# Waifu Generator

> Powered by the **Neta AI image generation API** (`api.talesofai.com`) — the same service as [neta.art](https://www.neta.art/open/).

Generate stunning **waifu generator ai image generator** images from a text prompt using AI. Powered by the Neta talesofai API — returns a direct image URL in seconds.

---

## Install

**Via npx skills:**
```bash
npx skills add TomCarranzaem/waifu-generator-skill
```

**Via ClawHub:**
```bash
clawhub install waifu-generator-skill
```

---

## Usage

```bash
# Basic usage (uses default prompt)
node waifugenerator.js

# Custom prompt
node waifugenerator.js "beautiful anime girl, cherry blossoms, soft lighting"

# Portrait size (default)
node waifugenerator.js "silver hair mage" --size portrait

# Landscape
node waifugenerator.js "ocean sunset scene" --size landscape

# Square
node waifugenerator.js "cute chibi character" --size square

# Tall
node waifugenerator.js "full body character art" --size tall

# Use a reference image (by picture UUID)
node waifugenerator.js "same character, winter outfit" --ref <picture_uuid>

# Pass token directly
node waifugenerator.js "fantasy warrior" --token YOUR_NETA_TOKEN
```

The script prints the final image URL to stdout on success.

---

## Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--token` | string | — | Neta API token (required) |
| `--ref` | picture_uuid | — | Reference image UUID for style inheritance |

### Size dimensions

| Size | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

---

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Examples

```bash
# Anime portrait
node waifugenerator.js "waifu in school uniform, detailed anime art, soft colors"

# Action pose landscape
node waifugenerator.js "anime warrior girl, dynamic pose, glowing sword" --size landscape

# Full body tall
node waifugenerator.js "elf princess, long silver hair, fantasy armor" --size tall
```

## Example Output

![Generated example](https://cdn.talesofai.com/picture/f2a01b8f-05f4-4f80-affb-9c5ff4b3a565.webp)
