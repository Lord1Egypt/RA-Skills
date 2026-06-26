# Texture Art Generator

Generate stunning satisfying texture art and hyperrealistic material images from text descriptions — glass, crystal, liquid jelly, melted wax, soap bubbles, and iridescent surfaces captured in breathtaking macro detail. Perfect for ASMR content creators, product design backgrounds, Instagram aesthetics, TikTok visual content, and short-form video thumbnails.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/texture-art-generator
```

```bash
clawhub install texture-art-generator
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

```bash
node textureartgenerator.js "prompt describing the texture" --token YOUR_TOKEN [--size SIZE] [--ref UUID]
```

If no prompt is supplied, a built-in default prompt is used:

> hyperrealistic macro photograph of a satisfying texture surface — glass crystal, iridescent liquid jelly, melted wax, soap bubble, or shimmering material — studio lighting, ultra-detailed microscopic surface detail, ASMR aesthetic, clean minimalist background, sharp focus

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `square` | Output image dimensions |
| `--token` | string | — | Neta API token (required) |
| `--ref` | UUID | — | Reference image UUID for style inheritance |

### Size dimensions

| Name | Width × Height |
|------|---------------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

## Examples

**Default satisfying texture (square):**
```bash
node textureartgenerator.js --token "$NETA_TOKEN"
```

**Iridescent soap bubble macro:**
```bash
node textureartgenerator.js "extreme closeup of a soap bubble surface, rainbow iridescent film, bokeh background, ultra-sharp" --token "$NETA_TOKEN"
```

**Melted wax texture, portrait:**
```bash
node textureartgenerator.js "melted candle wax pooling, warm amber tones, macro photography, glossy surface reflections" --token "$NETA_TOKEN" --size portrait
```

**Crystal glass refraction:**
```bash
node textureartgenerator.js "cracked crystal glass surface, light refractions, prismatic spectrum, studio light" --token "$NETA_TOKEN" --size landscape
```

**With style reference:**
```bash
node textureartgenerator.js "liquid mercury ripple surface" --token "$NETA_TOKEN" --ref xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## Output

Returns a direct image URL printed to stdout. Progress messages are written to stderr so you can pipe the URL directly:

```bash
URL=$(node textureartgenerator.js "jelly cube macro" --token "$NETA_TOKEN")
echo "Image ready: $URL"
```

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
