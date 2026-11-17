# Image generation and editing

Read this reference for `image` requests. Routing and Key rules remain in `SKILL.md`.

The initial preference is `gemini-3.1-flash-image` (Nano Banana 2), followed by `gpt-image-2` and `gemini-3-pro-image` (Nano Banana Pro) as model-unavailable fallbacks. The saved user choice always takes precedence.

## Model-specific parameters

| Model | Common parameters |
|---|---|
| `gemini-3.1-flash-image` | runtime `n`: 1–10; `image_size`: 0.5K/1K/2K/4K; `aspect_ratio`: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |
| `gemini-3-pro-image` | runtime `n`: 1–10; `image_size`: 1K/2K/4K; the same aspect-ratio set |
| `gpt-image-2` | `n`: 1–10; `size`; `quality`: auto/high/medium/low; `output_format`: png/jpeg/webp; optional background and compression |
| `nano-banana` | `size` |

Only pass parameters supported by the selected model. The runtime filters and validates fields using `data/model-catalog.json`.

## Examples

```bash
python3 scripts/showmeai.py image --prompt "Editorial product photo" --image-size 2K --aspect-ratio 4:5
python3 scripts/showmeai.py image --model gpt-image-2 --prompt "A detailed icon set" --count 4 --quality high --output-format png
python3 scripts/showmeai.py image --prompt "Keep the subject, change the setting to winter" --input subject.png
python3 scripts/showmeai.py image --prompt "Combine these references" --input person.png --input style.png
```

GPT image edits also accept `--mask`. Local inputs are sent as multipart files. Remote/base64 results are always saved locally. A fallback is attempted only for model/capacity unavailability, never for invalid prompts, authentication errors, or parameter errors.

`--count` and the saved image `n` default form a runtime-wide output contract from 1 to 10. Models with a native `n` parameter receive it directly. If a model has no native count parameter, or an upstream response returns fewer items than requested, the runtime uses bounded parallel single-image completion requests. `--concurrency` controls the completion-request cap and defaults to 4. Usage is aggregated, and the result reports both `requested_count` and `request_count`. Each physical request may be billed separately.

An accepted custom `size` is an aspect-ratio request as well as a pixel target. The upstream service may return a different pixel resolution with the same ratio; inspect the downloaded files when exact dimensions are mandatory.

Base64 responses are saved with an extension detected from their media signature. This avoids mislabeled files when an endpoint returns JPEG bytes without an explicit format even though the local fallback extension is PNG.
