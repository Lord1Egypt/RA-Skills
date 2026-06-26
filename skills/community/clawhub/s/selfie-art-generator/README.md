# Selfie Art Generator

Generate AI selfie art portraits from text descriptions. Create cinematic portraits, anime-style illustrations, oil paintings, and artistic profile pictures. Returns a direct image URL instantly.

> Powered by the **Neta AI image generation API** (`api.talesofai.com`) — the same service as [neta.art/open](https://www.neta.art/open/).

## Install

```bash
npx skills add yangzhou-chaofan/selfie-art-generator
```

```bash
clawhub install selfie-art-generator
```

## Token Setup

This skill requires a Neta API token (free trial available).

1. Get your free trial token at <https://www.neta.art/open/>
2. Pass it via the `--token` flag:

```bash
export NETA_TOKEN=your_token_here
node selfieartgenerator.js "your prompt" --token "$NETA_TOKEN"
```

## Usage

```bash
# Cinematic portrait
node selfieartgenerator.js "cinematic portrait, golden hour lighting, sharp facial details" --token "$NETA_TOKEN"

# Anime style
node selfieartgenerator.js "anime illustration portrait, soft pastel colors, detailed eyes" --size portrait --style anime --token "$NETA_TOKEN"

# Landscape cinematic shot
node selfieartgenerator.js "cinematic outdoor portrait, dramatic lighting, bokeh background" --size landscape --style cinematic --token "$NETA_TOKEN"

# Oil painting style
node selfieartgenerator.js "classical oil painting portrait, renaissance style, rich warm tones" --size portrait --token "$NETA_TOKEN"
```

## Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--style` | `anime`, `cinematic`, `realistic` | `cinematic` | Art style preset |
| `--token` | string | — | Neta API token (required) |
| `--ref` | picture_uuid | — | Reference image UUID for style inheritance |

### Size Dimensions

| Size | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

## Output

On success, prints the generated image URL to stdout:

```
https://oss.talesofai.cn/.../<image>.webp
```

```bash
# Pipe directly to download
curl -o portrait.jpg "$(node selfieartgenerator.js "cinematic portrait" --token "$NETA_TOKEN")"
```

## Example Output

```bash
node selfieartgenerator.js "artistic portrait photo, vibrant cinematic color grading, sharp facial details, golden hour lighting" --token "$NETA_TOKEN"
```

![Example output](https://oss.talesofai.cn/picture/4df8cb1b-745d-4af7-a80b-60aef36f6637.webp)

> Prompt: *"artistic portrait photo, vibrant cinematic color grading, sharp facial details, golden hour lighting, professional photography style, high resolution"*

---

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
