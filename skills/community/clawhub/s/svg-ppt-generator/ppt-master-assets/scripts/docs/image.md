# Image Tools

Image tools cover prompt-based generation and image inspection.

## `image_gen.py`

Unified image generation entry point.

```bash
python3 scripts/image_gen.py "A modern futuristic workspace"
python3 scripts/image_gen.py "Abstract tech background" --aspect_ratio 16:9 --image_size 4K
python3 scripts/image_gen.py "Concept car" -o projects/demo/images
python3 scripts/image_gen.py "Beautiful landscape" -n "low quality, blurry, watermark"
python3 scripts/image_gen.py --list-backends
```

Support tiers:
- Core: `openai`, `qwen`, `zhipu`, `volcengine`
- Extended: `stability`, `bfl`, `ideogram`
- Experimental: `siliconflow`, `fal`, `replicate`

Backend selection:

```bash
python3 scripts/image_gen.py "A cat" --backend openai
python3 scripts/image_gen.py "A product launch hero image" --backend qwen
python3 scripts/image_gen.py "科技感背景图" --backend zhipu
python3 scripts/image_gen.py "A product KV in cinematic style" --backend volcengine
```

Configuration sources:

1. Current process environment variables
2. Repo-root `.env` as a fallback

The active backend must always be selected explicitly via `IMAGE_BACKEND`.

Example `.env`:

```env
IMAGE_BACKEND=openai
OPENAI_API_KEY=your-api-key
```

Example process environment:

```bash
export IMAGE_BACKEND=openai
export OPENAI_API_KEY=your-api-key
```

Current process environment wins over `.env`.

Use provider-specific keys only, such as `OPENAI_API_KEY`, `QWEN_API_KEY`, `ZHIPU_API_KEY`, `VOLCENGINE_API_KEY`, `FAL_KEY`, or `REPLICATE_API_TOKEN`.

`IMAGE_API_KEY`, `IMAGE_MODEL`, and `IMAGE_BASE_URL` are intentionally unsupported.

If you keep multiple providers in one `.env` or environment, `IMAGE_BACKEND` must explicitly select the active provider.

Recommendation:
- Default to the Core tier for routine PPT work
- Use Extended only when you need a specific model style
- Treat Experimental backends as opt-in

## `analyze_images.py`

Analyze images in a project directory before writing the design spec or composing slide layouts.

```bash
python3 scripts/analyze_images.py <project_path>/images
```

Use this instead of opening image files directly when following the project workflow.

Dependencies:

```bash
pip install Pillow numpy
```
