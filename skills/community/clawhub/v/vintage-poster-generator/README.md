# Vintage Poster Generator

Generate stunning vintage-style poster images from text descriptions. Describe any scene, subject, or concept and receive a retro art print in 1950s–1970s aesthetic — complete with aged paper texture, distressed print effects, muted warm color palettes, and classic typography layouts. Great for Etsy sellers, interior designers, and anyone who loves nostalgic wall art.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add blammectrappora/vintage-poster-generator
```

**Via ClawHub:**
```bash
clawhub install vintage-poster-generator
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
node vintagepostergenerator.js "<description>" --token YOUR_TOKEN [--size <size>] [--ref <uuid>]
```

### Examples

```bash
# Classic travel poster
node vintagepostergenerator.js "Paris travel poster, Eiffel Tower at sunset, art deco style" --token YOUR_TOKEN

# Retro music concert poster
node vintagepostergenerator.js "jazz festival poster, 1960s style, bold geometric shapes, trumpet player silhouette" --token YOUR_TOKEN

# Vintage national park poster
node vintagepostergenerator.js "Yellowstone national park vintage poster, old faithful geyser, WPA style illustration" --token YOUR_TOKEN

# Landscape orientation
node vintagepostergenerator.js "Route 66 road trip poster, desert highway, retro americana" --token YOUR_TOKEN --size landscape

# Tall format
node vintagepostergenerator.js "1950s diner advertisement, neon signs, chrome details" --token YOUR_TOKEN --size tall
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

| Size | Dimensions |
|------|-----------|
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `square` | 1024 × 1024 |
| `tall` | 704 × 1408 |

---

## Default Style

When no prompt is provided, the skill generates using this default:

> vintage retro poster design, aged paper texture, distressed print effect, muted warm color palette, classic typography layout, 1950s-1970s aesthetic, high contrast illustration style, collectible art print

