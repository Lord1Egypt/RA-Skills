# Watercolor Art Generator

Generate stunning watercolor paintings, portraits, and illustrations from text descriptions — instantly, using AI. Describe any scene, subject, or style and receive a high-quality watercolor artwork ready for printing, sharing, or gifting.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add blammectrappora/watercolor-art-generator
```

**Via ClawHub:**
```bash
clawhub install watercolor-art-generator
```

---

## Usage

```bash
node watercolorartgenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

```bash
# Portrait of a woman with soft watercolor washes
node watercolorartgenerator.js "portrait of a woman, soft translucent watercolor washes, luminous pastel hues" --token "$NETA_TOKEN"

# Landscape in watercolor
node watercolorartgenerator.js "misty mountain landscape, wet-on-wet watercolor blending, delicate brushstrokes" --token "$NETA_TOKEN" --size landscape

# Square watercolor illustration
node watercolorartgenerator.js "botanical floral arrangement, fine art watercolor illustration style" --token "$NETA_TOKEN" --size square

# Tall format with style reference
node watercolorartgenerator.js "fairy tale castle at dusk, watercolor painting" --token "$NETA_TOKEN" --size tall --ref abc123-uuid
```

**Output:** Returns a direct image URL.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | *(required)* | Your Neta API token |
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--ref` | UUID string | *(none)* | Reference image UUID for style inheritance |

### Size dimensions

| Size | Width | Height |
|------|-------|--------|
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `square` | 1024 | 1024 |
| `tall` | 704 | 1408 |

---

## Token Setup

This skill requires a Neta API token. Pass it using the `--token` flag:

```bash
node watercolorartgenerator.js "your prompt" --token YOUR_TOKEN
```

You can store your token in a shell variable and expand it:

```bash
export NETA_TOKEN="your_token_here"
node watercolorartgenerator.js "your prompt" --token "$NETA_TOKEN"
```

Get your free token at: https://www.neta.art/open/

