---
name: gpt-image-2
description: Full OpenAI-compatible GPT Image 2 coverage across images/generations, images/edits, and responses with the image_generation tool. Use when the one-shot image helper is not enough - text-to-image, mask edits, multi-image batches, streaming, partial_images, and mixed text+image Responses flows. Reads .env and respects process environment variables; works with any OpenAI-compatible gateway.
---

# GPT Image 2

A single Python entrypoint that covers every GPT Image 2 route, with strict pre-flight validation of the model's size, aspect, and feature constraints.

## Workflow

1. Open [references/config.md](./references/config.md) to pick environment variables and defaults.
2. Open [references/api-surface.md](./references/api-surface.md) to choose between `generations`, `edits`, and `responses`.
3. Prefer `OPENAI_BASE_URL=https://api.openai.com/v1` unless the user asks for a different OpenAI-compatible endpoint.
4. Use `gpt-image-2` for `generations` and `edits`; use a text-capable Responses model such as `gpt-5.4` for `responses`.
5. Run `scripts/gpt_image.py` with one of the three subcommands.
6. Add `--dry-run` first when the payload shape is the main risk.
7. Add `--save-response <path>` when the raw JSON body or SSE event stream needs to be kept for debugging.

## Commands

Text-to-image through the public Images API:

```powershell
python .\skills\gpt-image-2\scripts\gpt_image.py generations `
  --prompt "A bold product hero image for a developer tool homepage" `
  --output .\out\hero.png `
  --size 1536x1024 `
  --quality high `
  --format png
```

Multi-image batch with a filename pattern:

```powershell
python .\skills\gpt-image-2\scripts\gpt_image.py generations `
  --prompt "A cinematic city skyline at night" `
  --output .\out\skyline-{index}.webp `
  --n 3 `
  --format webp `
  --compression 90
```

Image edits with two inputs plus a mask:

```powershell
python .\skills\gpt-image-2\scripts\gpt_image.py edits `
  --prompt "Blend the two references into one clean marketing illustration" `
  --image .\refs\subject.png `
  --image .\refs\background.png `
  --mask .\refs\mask.png `
  --output .\out\edit-{index}.png `
  --image-field-style brackets `
  --n 2
```

Responses API with streaming and partial previews:

```powershell
python .\skills\gpt-image-2\scripts\gpt_image.py responses `
  --input-text "Generate a poster for an AI developer summit" `
  --model gpt-5.4 `
  --output .\out\poster-{index}.png `
  --stream `
  --partial-images 2 `
  --save-response .\out\poster-events.json
```

Responses API edit with a local image plus a mask:

```powershell
python .\skills\gpt-image-2\scripts\gpt_image.py responses `
  --input-text "Turn this product shot into a clean studio ad" `
  --model gpt-5.4 `
  --input-image .\refs\product.png `
  --mask .\refs\mask.png `
  --output .\out\studio.png `
  --action edit
```

Inspect the built request without sending it:

```powershell
python .\skills\gpt-image-2\scripts\gpt_image.py generations `
  --prompt "A minimal cover image" `
  --output .\out\cover.png `
  --dry-run
```

## Rules

- Use `generations` for public text-to-image calls.
- Use `edits` for multipart image edits and mask uploads.
- Use `responses` for advanced flows: streaming, mixed text + image input, `previous_response_id`, `tool_choice`, `action`, and optional `tool_model`.
- Process environment variables override `.env`; CLI flags override both.
- Never print secrets.
- `--output` takes either a single path or a pattern such as `image-{index}.png` for multi-image or streaming flows.
- `responses` uses a top-level Responses model separate from the image model; default it to `gpt-5.4` unless you need another text-capable model.
- `quality` on Responses tool flows is passed through, but final behavior still depends on the hosted image tool.
- On OpenAI GPT image models, omit `response_format`; image data already comes back as base64.
- Fail fast on unsupported `gpt-image-2` combinations: transparent background, invalid size, `partial_images` outside `0..3`, or `stream=true` with `n>1` on public Images routes.

## Resources

- Script: [scripts/gpt_image.py](./scripts/gpt_image.py)
- Config reference: [references/config.md](./references/config.md)
- API surface reference: [references/api-surface.md](./references/api-surface.md)
