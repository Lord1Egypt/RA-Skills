# Model reference (SpicyAPI catalog, read 2026-09-27)

Test results below come from the public SpicyAPI leaderboards (https://spicyapi.ai/leaderboards, methodology v2.1, runs 2026-09-14 → 2026-09-27) and the review verdicts on https://spicyapi.ai/reviews. Freedom = weighted pass rate over five explicitness levels; "explicit x/y" = L4 test prompts that rendered as asked.

## Tested verdicts (one line each)

- **Wan 3.0**: Index 76.5, Freedom 96, explicit 9/9. Cheap 30-second takes with sound from text, a still or references; it can go further than the prompt, jobs take ~3.5 min, Ref2V refuses real faces.
- **Wan 3.0 Prime / Pro / Pro Prime**: same capability (76.5), Freedom 78–82; Prime is faster for T2V/Ref2V at +36%.
- **MiniMax H3 LoRA / Singularity LoRA**: Freedom 98.3 / 100; your own weights, three LoRAs per call. Singularity for fast action and distant faces.
- **MiniMax H3 (standard)**: all 14 test clips came back as asked; Freedom 33.3 reflects missing coverage, not refusals. Cheapest uncensored H3.
- **Seedance 2.5 / 2.5 Spicy**: base 2.5 stays on script for long takes (explicit 8/9); the Spicy edition goes further on the hardest levels (Freedom 96.7) but costs more.
- **Seedance 2.0 (standard)**: highest capability (81.5) but softens explicit prompts (1/9); use Seedance 2.0 Spicy (Freedom 93.3) for adult work.
- **Wan 2.7 Spicy**: Freedom 100, audio in one file; no text or reference input, 15 s max.
- **Wan 2.2 Spicy**: cheapest Wan Spicy with a closing frame; the hardest level softens sometimes.
- **LTX 2.3 Spicy**: 3–20 s from an opening frame; top level softens more often than Wan Spicy.
- **Qwen Image 2.1**: Index 73, Freedom 96.3; uncensored T2I and 10-reference editing at $0.024. **Qwen Image 2.1 LoRA** posted the cleaner ladder (Index 80.5).
- **MiniMax H3 Image LoRA**: Freedom 100; your LoRAs on an uncensored still model.
- **Seedream 5.0 Pro / Lite**: photographic finish / multi-photo edits; Freedom 94.3 / 96.
- **Qwen Image 3.0 / 3.0 Pro**: pick for legible lettering; Freedom 96 / 98.
- **Z-Image Spicy / Spicy Pro**: cheap, fast uncensored stills at exact sizes (≤1536 / ≤2560 px); weaker anatomy.
- **Qwen Image Edit Spicy**: fast single-photo edit, no setup; not for multiple references.
- **Grok 4.7 / 4.3**: uncensored fiction and roleplay with no jailbreak (Freedom 100 / 98.9); 4.3 is cheaper with a huge context.
- **DeepSeek V4.1 Flash**: cheap long-context reads; add a system prompt to steady intimate scenes.


Prices are USD and are the listed tier for the resolution shown. The quote returned by `spicy.py quote` / `generate` is always authoritative. Model IDs must be copied exactly.

## Spicy image-to-video (adult-tuned editions)

| Model ID | Duration | Resolution → price per output second | Notable fields |
|---|---|---|---|
| `alibaba/wan-2.2-spicy/image-to-video` | 5 or 8 | 480p $0.019 · 720p $0.038 | `prompt` required, `last_image_url`, `enable_prompt_expansion`, `seed` |
| `alibaba/wan-2.2-spicy-lora/image-to-video` | 5 or 8 | 480p $0.024 · 720p $0.048 | `loras`, `high_noise_loras`, `low_noise_loras` (≤3 each, `{path, scale}`) |
| `alibaba/wan-2.2-spicy-lora/video-extend` | 5 or 8 | 480p $0.038 · 720p $0.076 | `video_url` + `prompt`, same LoRA fields |
| `lightricks/ltx-2.3-spicy/image-to-video` | 3–20 | 480p $0.019 · 720p $0.038 · 1080p $0.057 | `preset` (`tuned`/`original`), prompt optional |
| `lightricks/ltx-2.3-spicy-lora/image-to-video` | 3–20 | 480p $0.0285 · 720p $0.0475 · 1080p $0.0665 | `loras` presets |
| `bytedance/seedance-1.5-pro-spicy/image-to-video` | 4–12 | 480p $0.012 (audio $0.024) · 720p $0.026 · 1080p $0.052 | `camera_fixed`, `aspect_ratio`, `last_image_url` |
| `bytedance/seedance-2.0-mini-spicy/image-to-video` | 4–15 | 480p $0.0387 · 720p $0.0821 | `generate_audio`, `aspect_ratio`, `last_image_url` |
| `bytedance/seedance-2.0-fast-spicy/image-to-video` | 4–15 | 480p $0.081 · 720p $0.1742 | sound included |
| `bytedance/seedance-2.0-spicy/image-to-video` | 4–15 | 480p $0.114 · 720p $0.228 · 1080p $0.57 · 4K $1.14 | `aspect_ratio`, `last_image_url` |
| `bytedance/seedance-2.5-spicy/image-to-video` | 4–30 | 480p $0.216 · 720p $0.432 · 1080p $1.08 · 4K $2.16 | `generate_audio`, `last_image_url` |
| `minimax/h3-spicy/image-to-video` | 3–15 | 480p $0.038 · 540p $0.057 · 768p $0.084 · 1080p $0.152 | prompt optional, `last_image_url` |
| `vidu/q3-spicy/image-to-video` | 1–16 | 540p $0.0665 · 720p $0.1425 · 1080p $0.152 | `movement_amplitude` (`auto/small/medium/large`), `generate_audio` |
| `alibaba/wan-2.6-spicy/image-to-video` | 5, 10 or 15 | 720p $0.095 · 1080p $0.1425 | `shot_type` (`single/multi`), `audio_url`, `negative_prompt` |
| `alibaba/wan-2.7-spicy/image-to-video` | 2–15 | 720p $0.1235 · 1080p $0.19 | `prompt` required, `generate_audio`, `audio_url`, `negative_prompt` |

Seedance `aspect_ratio` accepts `16:9, 9:16, 4:3, 3:4, 1:1, 21:9, adaptive`. Other models follow the first frame's shape.

## Images and edits

| Model ID | Price | Size fields |
|---|---|---|
| `alibaba/qwen-image-2.1/text-to-image` (**recommended**, tier `unrestricted`) | $0.024 at 1k, $0.048 at 1.5k/2k | `aspect_ratio` (15 options), `resolution` `1k/1.5k/2k`; prompt up to 5,000 chars |
| `alibaba/qwen-image-2.1/edit` | $0.036 at 1k | 1–10 reference images + instruction |
| `alibaba/qwen-image-2.1-lora/text-to-image` / `.../edit` | $0.03 / $0.042 at 1k | up to 3 LoRAs |
| `alibaba/z-image-spicy/text-to-image` | $0.01235 (prompt expansion on: $0.0133) | `width`, `height` 256–1536 |
| `alibaba/z-image-spicy-pro/text-to-image` | $0.019 | `width`, `height` 256–2560 |
| `prefect/pony-xl/text-to-image` | $0.015 | `size` one of `1024*1024, 896*1152, 1152*896, 832*1216, 1216*832, 768*1344, 1344*768`; tag-style prompt |
| `alibaba/qwen-image-spicy-edit/edit` | $0.038 | `image_url` + `prompt` (one instruction, no mask) |

## Standard video models with catalog tier `unrestricted`

Use these for text-to-video and reference-to-video, which the Spicy editions don't offer. In catalog order: `bytedance/seedance-2.5/{text-to-video,image-to-video,reference-to-video}` ($0.1234/s), `bytedance/seedance-2.0/...` ($0.07/s), `alibaba/wan-3.0-prime/...` ($0.0612/s), `alibaba/wan-3.0/...` ($0.045/s, 2–30 s), `minimax/h3/...` ($0.025/s), `lightricks/ltx-2.5/...`, `alibaba/wan-3.0-pro/...`, `minimax/h3-lora/...`, `bytedance/seedance-2.0-mini/...`, `bytedance/seedance-2.0-fast/...`. Reference-to-video takes character/scene images referenced as `@Image1`, `@Image2` in the prompt; read the schema first.

## Useful non-Spicy tools

`spicyapi/image-upscaler-v1/upscale` ($0.012/image), `spicyapi/video-upscaler-v1/upscale` ($0.006/s), `spicyapi/image-expander-v1/edit` ($0.024), `spicyapi/lip-sync-v1/lip-sync` ($0.012/s), `spicyapi/foley-v1/video-to-audio` ($0.0012/s), `spicyapi/talking-avatar-v1/talking-avatar` ($0.018/s).

Face/head/character swap models exist (`spicyapi/face-swap-v1/edit`, `spicyapi/character-swap-v1/video-analyze` + `video-edit`), but **never** use them to place a real person into sexual content without documented consent. Video swaps are two separately billed tasks; tell the user before the first one.

## Text (OpenAI-compatible, `https://api.spicyapi.ai/v1/chat/completions`)

Catalog tier `unrestricted` on 2026-09-27 includes `xai/grok-4.7/chat` ($0.0036/1K tokens), `deepseek/v4-pro/chat`, `deepseek/v4.1-flash/chat` ($0.0012), `zai/glm-5.3-flash/chat` ($0.000425), `moonshot/kimi-k3/chat`.

## Choosing quickly

- Drafts and volume: Wan 2.2 Spicy or LTX 2.3 Spicy at 480p.
- Cinemagraph, locked camera: Seedance 1.5 Pro Spicy with `camera_fixed: true`.
- Final quality: Seedance 2.0 Spicy (≤15 s) or Seedance 2.5 Spicy (≤30 s).
- Anime: Prefect Pony XL still → Vidu Q3 Spicy.
- Custom style/character: Wan 2.2 Spicy LoRA; continue with `video-extend`.
- Audio: Seedance 2.x (`generate_audio`), Wan 2.7 Spicy, or Wan 2.6/2.7 with your own `audio_url`.
