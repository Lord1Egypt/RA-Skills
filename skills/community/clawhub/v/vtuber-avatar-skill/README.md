# VTuber Avatar Generator

> Powered by the **Neta AI image generation API** (`api.talesofai.com`) — the same service as [neta.art](https://www.neta.art/open/).

Generate professional VTuber avatar images from text descriptions using AI. Powered by the Neta talesofai API, this skill produces anime-style virtual streamer character art — ready for Live2D rigging and streaming.

---

## Install

**Via npx skills:**
```bash
npx skills add blammectrappora/vtuber-avatar-skill
```

**Via ClawHub:**
```bash
clawhub install vtuber-avatar-skill
```

---

## Usage

**Basic — uses the default VTuber prompt:**
```bash
node vtuberavatar.js
```

**Custom prompt:**
```bash
node vtuberavatar.js "fox girl vtuber, silver hair with blue highlights, golden eyes, shrine maiden outfit, cozy lo-fi aesthetic"
```

**With size option:**
```bash
node vtuberavatar.js "cute bunny vtuber, pastel pink hair, oversized hoodie" --size portrait
```

**With a reference image (for style inheritance):**
```bash
node vtuberavatar.js "same character, winter outfit" --ref <picture_uuid>
```

**Pass token inline:**
```bash
node vtuberavatar.js "dragon vtuber, scales, fierce expression" --token YOUR_TOKEN
```

The script prints a direct image URL to stdout on success.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `square` | Output image dimensions |
| `--token` | string | — | Override token (see Token Setup) |
| `--ref` | picture_uuid | — | Inherit style from an existing image |

### Size dimensions

| Name | Width | Height |
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

## Default Prompt

When no prompt is provided, the skill uses:

> VTuber avatar, anime style, vibrant hair, expressive eyes, live2d ready, clean lines, professional virtual streamer character design, soft pastel background

## Example Output

![Generated example](https://oss.talesofai.cn/picture/9a2f7875-59c9-4d9b-a59e-c3ae9f1deafc.webp)

---

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
