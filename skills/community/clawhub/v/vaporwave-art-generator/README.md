# Vaporwave Art Generator

Generate stunning vaporwave, synthwave, and retrowave images from text descriptions using AI. Describe the scene, mood, or aesthetic you want — neon grids, 80s palm tree silhouettes, chrome reflections, pastel skies, glitch effects — and receive a high-quality image URL in seconds.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

**Via npx skills:**
```bash
npx skills add omactiengartelle/vaporwave-art-generator
```

**Via ClawHub:**
```bash
clawhub install vaporwave-art-generator
```

## Usage

```bash
node vaporwaveartgenerator.js "your description here" --token YOUR_TOKEN
```

**Default prompt (no description needed):**
```bash
node vaporwaveartgenerator.js --token YOUR_TOKEN
```

**With size:**
```bash
node vaporwaveartgenerator.js "neon city skyline at dusk, pink gradients" --size portrait --token YOUR_TOKEN
```

**With reference image (style inheritance):**
```bash
node vaporwaveartgenerator.js "retro sunset over the ocean" --ref <picture_uuid> --token YOUR_TOKEN
```

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `landscape`, `portrait`, `square`, `tall` | `landscape` | Output image dimensions |
| `--token` | string | — | Your Neta API token (required) |
| `--ref` | UUID string | — | Reference image UUID for style inheritance |

### Size dimensions

| Size | Dimensions |
|------|-----------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

## Output

Returns a direct image URL printed to stdout. Redirect or pipe it as needed:

```bash
URL=$(node vaporwaveartgenerator.js "glowing grid, retro arcade" --token "$NETA_TOKEN")
echo "Image: $URL"
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Examples

```bash
# Synthwave landscape with neon grid
node vaporwaveartgenerator.js "glowing neon grid floor, retrowave sunset, pink and purple sky" --token "$NETA_TOKEN"

# Lo-fi aesthetic portrait
node vaporwaveartgenerator.js "lo-fi dreamy atmosphere, pastel colors, retro computer, cassette tapes" --size portrait --token "$NETA_TOKEN"

# Album art square
node vaporwaveartgenerator.js "chrome reflective surfaces, palm tree silhouette, 80s aesthetic, glitch effects" --size square --token "$NETA_TOKEN"

# Tall wallpaper
node vaporwaveartgenerator.js "vaporwave city, neon lights, retro arcade signs, rainy streets" --size tall --token "$NETA_TOKEN"
```

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
