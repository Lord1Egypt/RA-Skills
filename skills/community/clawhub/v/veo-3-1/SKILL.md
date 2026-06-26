---
name: poyo-veo-3-1
description: Use PoYo AI Veo 3.1 for frame-conditioned video generation through the `https://api.poyo.ai/api/generate/submit` endpoint. Use when a user wants fast or quality modes, start-frame and end-frame guidance, up to 4K resolution, reference-image video generation, or PoYo payloads for `veo3.1-fast` and `veo3.1-quality`.
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/video-series/veo-3-1", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---

# PoYo Veo 3.1 Video Generation

Use this skill to submit and track PoYo jobs for the VEO 3.1 family.

## Quick workflow

1. Choose the right model id for the requested output.
2. Build the request body for `POST https://api.poyo.ai/api/generate/submit`.
3. Send Bearer-authenticated JSON with `Authorization: Bearer <POYO_API_KEY>`.
4. Save the returned `task_id`.
5. Poll unified task status or wait for `callback_url` notifications.

## Request rules

- Require top-level `model`.
- Keep prompts concrete and outcome-focused.
- Require `input.prompt` unless the user already supplied a full payload.
- Use `input.image_urls` only when the task needs reference or source images.
- Use `input.duration` when the clip length matters.
- Use `input.aspect_ratio` when the output surface matters.
- Use `input.resolution` when quality/cost tradeoffs matter.

## Model selection

### `veo3.1-fast`

Use for general generation with this model variant.
### `veo3.1-quality`

Use for general generation with this model variant.

## Execution

- Read `references/api.md` for endpoint details, model ids, key fields, example payloads, and polling notes.
- Use `scripts/submit_veo_3_1.sh` to submit a raw JSON payload from the shell.
- If the user only needs a curl example, adapt the example from `references/api.md` instead of rewriting from scratch.
- After submission, report the `task_id` clearly so follow-up polling is easy.

## Output expectations

When helping with this model family, include:
- chosen model id
- final payload or a concise parameter summary
- whether reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook

Notes:

Needs POYO_API_KEY from https://poyo.ai
PoYo.ai - Premium AI API Platform | Image, Video, Music & Chat APIs - 80% Cheaper
