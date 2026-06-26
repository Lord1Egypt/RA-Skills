---
name: seaart-image
version: "2.0.0"
description: Use this skill to generate AI images using the SeaArt platform (seaart.ai). Supports text-to-image generation with multiple models, custom dimensions, LoRA models, and negative prompts. Use this whenever the user wants to "generate an image", "create a picture", or explicitly mentions SeaArt image generation.
tags: ["image", "ai", "seaart", "text-to-image", "generation"]
metadata:
  clawdbot:
    requires:
      env:
        - name: SEAART_TOKEN
          primary: true
          description: SeaArt session token (T cookie value). Treat like a password.
      binaries:
        - name: python3
          primary: true
        - name: pip3
          description: Required to install the requests library if not present.
---

# SeaArt Image Generator

This skill generates AI images via the SeaArt platform. You can create images from text prompts with various models, aspect ratios, LoRA models, and other parameters.

## Prerequisites: SeaArt Token

To use this skill, you need a SeaArt authentication token. This token is the value of the `T` cookie.

### How to get your token:
1. Log into your account on [seaart.ai](https://www.seaart.ai) in your browser.
2. Open Developer Tools (F12 or Right Click -> Inspect).
3. Go to the "Application" tab (or "Storage" in Firefox).
4. Expand "Cookies" and select `https://www.seaart.ai`.
5. Find the cookie named `T`.
6. Copy its value (a long JWT string starting with `eyJhbGci...`).

### How to store your token:
Store it as an environment variable (`SEAART_TOKEN`). Never paste the token into chat.

```
/update-config set SEAART_TOKEN="your_token_value_here"
```

> **Security note:** Never share your token in chat messages or logs. The token will be persisted in your local agent config by `/update-config` — ensure only you have access to that config file.

## Supported Models and Parameters

**Default Model:** SeaArt Infinity (if user doesn't specify, use this one)

#### SeaArt Official Models

| Model Name | CLI Key | `model_no` | `model_ver_no` |
|------------|---------|------------|----------------|
| **SeaArt Infinity** (Default) | `seaart-infinity` | `f8172af6747ec762bcf847bd60fdf7cd` | `2c39fe1f-f5d6-4b50-a273-499677f2f7a9` |
| **SeaArt Film** | `seaart-film` | `26058e019e3a0c026e1ad2bfa69e2b75` | `91b19145-a436-4bbc-ace4-62399e71336b` |
| **SeaArt Film Edit** | `seaart-film-edit` | `a70a84e9d2db46c78661de9bfbbf5bd5` | `1cd2354ece4e4308a1b0896eb35b37bc` |
| **SeaArt Film Edit 2.0** | `seaart-film-edit-2` | `d4ont25e878c7390gip0` | `d39166c9-4d77-4fa3-a81f-d69f144929f0` |
| **SeaArt Film Edit 3.0** | `seaart-film-edit-3` | `d6eqg15e878c73dilcv0` | `a8b3e33e-02b5-4a27-bca8-c331c87b267f` |

#### Seedream Series

| Model Name | CLI Key | `model_no` | `model_ver_no` |
|------------|---------|------------|----------------|
| **Seedream 5.0** | `seedream-5` | `d6eqbble878c73dhco9g` | `1ad9c231-1945-4e50-a24d-d2c7570338ad` |
| **Seedream 4.5** | `seedream-4.5` | `d4pbgg5e878c73fengf0` | `53c0eaf0-7de3-4e9c-a906-9499df061661` |
| **Seedream 4.0** | `seedream-4` | `d534afde878c73drik20` | `60099fa2-8f31-4f42-8e7f-5ea4c2784220` |

#### Nano Banana Series

| Model Name | CLI Key | `model_no` | `model_ver_no` |
|------------|---------|------------|----------------|
| **Nano Banana** | `nano-banana` | `0e21cbf906b5b39c2f9863f4b9ff059edbd0b399` | `e651aa45c8ed746bcd2546d46a3cdf3bf83feb67` |
| **Nano Banana 2** | `nano-banana-2` | `d6ggttle878c739bpf50` | `547ebf19-577f-4614-9ef7-f9ece0aebf80` |
| **Nano Banana Pro Image** | `nano-banana-pro` | `d49btu5e878c73avuqfg` | `49a838b1-0ef7-4442-999d-71e10cb2feab` |

#### Other Models

| Model Name | CLI Key | `model_no` | `model_ver_no` |
|------------|---------|------------|----------------|
| **Grok Imagine Image** | `grok-imagine` | `d6sih8le878c73a7cbtg` | `0e7eaf79-5702-4387-bcaa-ce3b79a36889` |
| **Z Image Turbo** | `z-image-turbo` | `d4kssode878c7387fae0` | `ef24b47a8d618127c9342fd0635aedb9` |
| **WAI-ANI-PONYXL** | `wai-ani-ponyxl` | `24231feb2db47b663ff5b3123f01fab6` | `6e2e976db9a8e83312a0c91b852f876c` |

Users can also specify custom models via `--model-no`/`--model-ver` or `--model-url`.

### Supported Aspect Ratios

The script auto-selects resolution based on the model type:

**HD Models** (SeaArt Official, Seedream, Nano Banana, Grok Imagine, Z Image Turbo — require >= 3,686,400 px):

| Ratio | Width | Height | Alias |
|-------|-------|--------|-------|
| `1:1` | 2048 | 2048 | 方图/Square |
| `2:3` | 1664 | 2432 | 竖图/Portrait |
| `3:2` | 2432 | 1664 | 横图/Landscape |
| `3:4` | 1792 | 2304 | |
| `4:3` | 2304 | 1792 | |
| `9:16` | 1536 | 2688 | 手机竖屏 |
| `16:9` | 2688 | 1536 | 宽屏/Widescreen |

**SD Models** (WAI-ANI-PONYXL — standard ~1MP):

| Ratio | Width | Height |
|-------|-------|--------|
| `1:1` | 1024 | 1024 |
| `2:3` | 832 | 1216 |
| `3:2` | 1216 | 832 |
| `9:16` | 768 | 1344 |
| `16:9` | 1344 | 768 |

If custom dimensions are provided but too small for an HD model, the script auto-scales up while preserving aspect ratio.

### LoRA Support

LoRA models add specific styles or effects. Format: `id:strength:version`

- **strength**: 0.5–1.0 (0.8 recommended)
- **version** (`model_ver_no`): Required for most LoRAs. Extract from the API request payload (not from URL).
- Multiple LoRAs: comma-separated, e.g. `id1:0.8:ver1,id2:1.0:ver2`

To get LoRA parameters: open DevTools Network tab on SeaArt, generate an image, find the `text-to-img` request, and extract `id`, `weight`, and `model_ver_no` from the `lora_models` array in the payload/response.

## How to use this skill

When a user asks to generate an image, follow these steps:

### 1. Check for the Token
Check if the `SEAART_TOKEN` environment variable is set: `echo $SEAART_TOKEN`.
If empty, guide the user to set it as described above. Wait before proceeding.

### 2. Gather Requirements
Ensure you have:
- The prompt (what the image should contain)
- The desired model (default to WAI-ANI-NSFW-PONYXL)
- The desired aspect ratio or dimensions (default to 1:1 / 1024x1024)
- Number of images (default 4, max 8)
- Optional: negative prompt, LoRA models, generation steps

### 3. Generate the Image
Use the included Python script:

```bash
# Basic generation
python3 ~/.claude/skills/seaart/scripts/generate.py \
  --prompt "A cute orange cat sitting by the window, soft lighting, realistic photography"

# With predefined model
python3 ~/.claude/skills/seaart/scripts/generate.py \
  --prompt "Anime girl under cherry blossoms" \
  --model wai-ani-ponyxl \
  --aspect-ratio "2:3"

# With custom model
python3 ~/.claude/skills/seaart/scripts/generate.py \
  --prompt "Futuristic cityscape" \
  --model-no "custom_id" \
  --model-ver "custom_ver" \
  --aspect-ratio "16:9"

# With model URL (auto-extracts model_no and model_ver_no)
python3 ~/.claude/skills/seaart/scripts/generate.py \
  --prompt "Mountain landscape" \
  --model-url "https://www.seaart.ai/create/image?id=xxx&model_ver_no=yyy"

# With LoRA
python3 ~/.claude/skills/seaart/scripts/generate.py \
  --prompt "Detailed anime portrait" \
  --model wai-ani-ponyxl \
  --lora "csor35de878c738f4i3g:0.65:8249602c4886cfd76ddfff3eaea805f4"

# With multiple LoRAs + negative prompt + custom count
python3 ~/.claude/skills/seaart/scripts/generate.py \
  --prompt "Beautiful landscape painting" \
  --lora "lora1_id:0.8:lora1_ver,lora2_id:1.0:lora2_ver" \
  --negative "blurry, low quality, watermark" \
  --n 2
```

The script handles submitting the request, polling for completion, and returning the final image URLs.

## Example Usage

**User:** "帮我生成一张赛博朋克风格的城市横图"

**Assistant:**
1. Checks `$SEAART_TOKEN` — set.
2. Runs:
```bash
python3 ~/.claude/skills/seaart/scripts/generate.py \
  --prompt "Cyberpunk city, neon lights, futuristic architecture, detailed" \
  --aspect-ratio "16:9"
```
3. Presents the image URLs to the user.

**User:** "用 Grok Imagine 生成4张猫咪图片，竖图"

**Assistant:**
1. Runs:
```bash
python3 ~/.claude/skills/seaart/scripts/generate.py \
  --prompt "A cute cat, detailed fur, soft lighting" \
  --model grok-imagine \
  --aspect-ratio "2:3" \
  --n 4
```

---

## External Endpoints

| URL | Method | Data Sent |
|-----|--------|-----------|
| `https://www.seaart.ai/api/v1/task/v2/text-to-img` | POST | Prompt, model ID, dimensions, LoRA params, generation params |
| `https://www.seaart.ai/api/v1/task/batch-progress` | POST | Task ID (for polling status) |

All requests are authenticated via your `SEAART_TOKEN` cookie, which never leaves your machine in plaintext — it is only sent to `*.seaart.ai` as an HTTP cookie header.

---

## Security & Privacy

- **What leaves your machine**: Your text prompt, any LoRA configuration, and your `SEAART_TOKEN` are sent to `seaart.ai` servers as an HTTP cookie header on every API request.
- **Token storage**: `SEAART_TOKEN` is persisted locally in your agent config file by `/update-config`. Ensure only you have access to that config. It is not logged or transmitted by this skill beyond the API calls to seaart.ai listed above.
- **No additional data persistence**: This skill does not write any files to disk. Generated image URLs are returned inline.
- **Input handling**: All inputs are passed as structured JSON fields via the `requests` library — no shell interpolation is used.

---

## Trust Statement

By using this skill, your prompt and generation parameters are sent to [seaart.ai](https://www.seaart.ai). Only install and use this skill if you trust SeaArt with your creative content. This skill is not affiliated with or endorsed by SeaArt.
