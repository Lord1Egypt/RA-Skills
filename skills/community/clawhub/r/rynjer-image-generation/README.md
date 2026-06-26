# Rynjer Image Generation for Agents

Reliable image generation for agent workflows.

## TL;DR

Use this skill when an agent needs a usable image quickly and wants a low-friction path from:

**task → prompt → cost → image**

Recommended first run:
1. `rewrite_image_prompt`
2. `estimate_image_cost`
3. `generate_image`

Pricing boundary:
- rewrite: free
- estimate: free
- generate: paid via Rynjer credits or API access

## Real runtime modes

### Mock mode (default)
No credentials required.
Useful for local testing of tool shape and control flow.

### Live mode
Set env vars before running the runtime:

```bash
export RYNJER_USE_LIVE=1
export RYNJER_BASE_URL="https://rynjer.com"
export RYNJER_ACCESS_TOKEN="your_access_token_or_ryn_agent_v1_key"
```

Then run examples like:

```bash
node src/mock-runtime.js estimate_image_cost '{"use_case":"landing","count":1,"resolution":"1K","aspect_ratio":"16:9","quality_mode":"fast"}'
```

```bash
node src/mock-runtime.js generate_image '{"prompt":"A minimal blue geometric logo on white background","use_case":"landing","aspect_ratio":"1:1","resolution":"1K","quality_mode":"fast","count":1,"auto_poll":true,"poll_attempts":4,"poll_interval_ms":2000}'
```

## Live verification status

This package has now been verified against the real Rynjer backend for the agent-first flow:

- `POST /api/v1/agents/register` ✅
- owner bind via UI at `/en/settings/agents/bind` ✅
- `POST /api/v1/agents/keys/create` ✅
- `POST /api/credits/estimate` ✅
- `POST /v1/generate` ✅
- `GET /v1/generate/{request_id}` ✅

Important real-world note:
- the owner-selected scopes in the bind UI constrain what scopes can be requested in `keys/create`
- if the owner only grants `image/video/music`, requesting `credits:read` will correctly fail with `Requested scope not allowed`

## Quickstart

### Canonical happy path

#### 1) Rewrite a vague request

```json
{
  "tool": "rewrite_image_prompt",
  "input": {
    "goal": "Create a hero image for an AI analytics landing page",
    "raw_prompt": "futuristic dashboard hero",
    "use_case": "landing",
    "tone": "premium",
    "audience": "B2B SaaS buyers"
  }
}
```

#### 2) Estimate cost

```json
{
  "tool": "estimate_image_cost",
  "input": {
    "use_case": "landing",
    "count": 1,
    "resolution": "1K",
    "aspect_ratio": "16:9",
    "quality_mode": "fast"
  }
}
```

#### 3) Generate the image

```json
{
  "tool": "generate_image",
  "input": {
    "prompt": "Create a premium landing-page hero image for an AI analytics platform, sleek dashboard hints, dark interface glow, modern enterprise aesthetic, clean composition, high-end commercial lighting.",
    "use_case": "landing",
    "aspect_ratio": "16:9",
    "resolution": "1K",
    "quality_mode": "fast",
    "count": 1,
    "auto_poll": true
  }
}
```

## Real endpoint bindings

### `estimate_image_cost`
Live mode uses:
- `POST /api/credits/estimate`

Observed compatible request shape:

```json
{
  "product": "image",
  "model": "google/nano-banana",
  "units": 1,
  "price_version": "2026-02-02-v1",
  "options": {
    "resolution": "1K"
  }
}
```

Observed live response shape includes:
- `data.estimated_credits`
- `data.price_version`
- `data.breakdown`

### `generate_image`
Live mode uses:
- `POST /v1/generate`

Observed compatible request shape:

```json
{
  "request_id": "skill-...",
  "model": "google/nano-banana",
  "product": "image",
  "prompt": "A minimal blue geometric logo on white background",
  "units": {
    "count": 1,
    "resolution": "1K",
    "aspect_ratio": "1:1"
  },
  "scene": "text-to-image"
}
```

Observed live response shape includes:
- `data.task_id`
- `data.provider_task_id`
- `data.status`
- `data.usage_event_id`

### `poll_image_result`
Live mode uses:
- `GET /v1/generate/{request_id}`

Observed live response shape includes:
- `data.request_id`
- `data.task_id`
- `data.provider_task_id`
- `data.status`
- `data.outputs[]`
- `data.usage_event_id`

The runtime now extracts:
- `status`
- `image_urls`
- `outputs`
- `task_id`
- `provider_task_id`

## When agents should call this

Use this skill when the agent needs a usable image for:
- landing pages
- product pages
- blog/article covers
- social posts
- ads

## When agents should not call this

Do not use this v1 for:
- video generation
- music generation
- complex asset management
- multi-step studio pipelines
- large-scale brand systems

## Tool contracts

### `rewrite_image_prompt`
Rewrite a rough image request into a stronger prompt for reliable generation.

### `estimate_image_cost`
Estimate likely credit cost before running generation.

### `generate_image`
Generate a usable image for a real workflow task.

Optional live inputs:
- `request_id`
- `resolution`
- `scene`
- `auto_poll`
- `poll_attempts`
- `poll_interval_ms`

### `poll_image_result`
Poll a previously submitted Rynjer generation request by `request_id`.

## Live mode error behavior

The runtime now handles these cases explicitly:
- missing access token when live mode is enabled
- owner-granted scope mismatch during API key creation
- non-200 responses
- invalid or unexpected JSON responses
- pending generation after auto-poll attempts

## Routing philosophy

The skill should not force agents to pick raw models first.
Default routing should happen internally based on:
- `use_case`
- `quality_mode`
- `count`
- `aspect_ratio`

Advanced users may optionally override the model, but model choice should not be the primary interface.

## Product position

This skill is agent infrastructure, not a generic marketing design tool.
The key promise is:

> Give agents a reliable, low-friction path to generate usable images with predictable cost.
