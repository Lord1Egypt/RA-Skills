# Tattoo Design Generator

Generate custom tattoo concept art, ink illustrations, and tattoo reference sheets from text descriptions. Describe your idea — a Japanese koi fish, a geometric mandala, a fine line floral sleeve — and get back a ready-to-use tattoo design image. Perfect for tattoo artists, studios, and anyone planning their next ink.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add omactiengartelle/tattoo-design-generator
```

**Via ClawHub:**
```bash
clawhub install tattoo-design-generator
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
node tattoodesigngenerator.js "<description>" --token YOUR_TOKEN [--size <size>] [--ref <uuid>]
```

### Examples

```bash
# Fine line botanical sleeve concept
node tattoodesigngenerator.js "fine line botanical sleeve with roses, ferns, and butterflies, delicate linework, black ink" --token "$NETA_TOKEN"

# Traditional Japanese koi
node tattoodesigngenerator.js "traditional Japanese koi fish tattoo, bold outlines, red and black ink, waves" --token "$NETA_TOKEN" --size square

# Minimalist geometric mandala
node tattoodesigngenerator.js "minimalist geometric mandala tattoo, dotwork shading, sacred geometry, black ink" --token "$NETA_TOKEN" --size portrait

# Tribal armband
node tattoodesigngenerator.js "Polynesian tribal armband tattoo, bold black ink, traditional patterns" --token "$NETA_TOKEN" --size landscape
```

### Output

Returns a direct image URL.

---

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | Output image size: `portrait`, `landscape`, `square`, `tall` | `portrait` |
| `--ref` | Reference image UUID for style inheritance | — |

### Size dimensions

| Size | Dimensions |
|------|------------|
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `square` | 1024 × 1024 |
| `tall` | 704 × 1408 |

---

## Default Prompt

If no prompt is provided, the script uses:

```
tattoo design concept art, bold black ink linework, intricate detailed illustration, clean lines, black and white tattoo sketch, fine line tattoo style, ready for skin
```

