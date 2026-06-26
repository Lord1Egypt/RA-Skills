# Implementation Notes

This package is no longer only a concept draft.
It now reflects a real verified agent-first flow against the live Rynjer backend.

## Verified flow

The following sequence has been exercised successfully against production:

1. `POST /api/v1/agents/register`
2. owner bind through UI at `/en/settings/agents/bind`
3. `POST /api/v1/agents/keys/create`
4. `POST /api/credits/estimate`
5. `POST /v1/generate`
6. `GET /v1/generate/{request_id}`

## Endpoint mapping

### rewrite_image_prompt
Still local logic inside the skill runtime.
This remains the right choice for v1 because it does not need to block monetization-critical execution.

### estimate_image_cost
Bound to the live endpoint:
- `POST /api/credits/estimate`

Observed working request shape:

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

Observed response shape:

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "estimated_credits": 8,
    "price_version": "2026-02-02-v1",
    "breakdown": {
      "mediaType": "image",
      "options": {},
      "price_rules": null
    }
  }
}
```

Implementation consequence:
- do not assume full `per_unit_cost / total` fields are always present
- parse `estimated_credits` first, keep `breakdown` as opaque passthrough

### generate_image
Bound to the live endpoint:
- `POST /v1/generate`

Observed working request shape:

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

Observed response shape:

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "task_id": "...",
    "provider_task_id": "...",
    "status": "pending",
    "usage_event_id": "..."
  }
}
```

### poll_image_result
Bound to the live endpoint:
- `GET /v1/generate/{request_id}`

Observed terminal success payload:

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "request_id": "openclaw-...",
    "task_id": "...",
    "provider_task_id": "...",
    "status": "success",
    "outputs": [
      {
        "url": "https://...png",
        "type": "image"
      }
    ],
    "usage_event_id": "..."
  }
}
```

Implementation consequence:
- poll results should extract image URLs from `data.outputs[]`
- `status` should be normalized without assuming output presence until terminal success

## Agent auth model

The verified autonomous path is:

1. agent generates Ed25519 keypair
2. agent signs canonical payload and calls `POST /api/v1/agents/register`
3. owner binds registration code through the site UI
4. agent signs canonical payload and calls `POST /api/v1/agents/keys/create`
5. returned `ryn_agent_v1_...` key is then used directly as Bearer auth for generation endpoints

## Scope behavior that matters

This was verified during live testing:
- scopes granted in the owner bind UI constrain later API key creation
- requesting a scope not granted by the owner returns a real 403

Observed failure example:
- requested: `credits:read`
- owner granted only: `image`, `video`, `music`
- response: `Requested scope not allowed`

Implementation consequence:
- keep requested scopes minimal
- do not assume read scopes are available unless explicitly granted

## Current runtime priorities

The current executable runtime should optimize for:
1. first-run success
2. real image generation completion
3. resilient parsing of live responses
4. minimal required auth surface

## Remaining polish opportunities

Not blockers anymore, but worth tightening before or during soft publish:
- add a helper script for autonomous register → key-create flow docs
- add optional support for owner-provided request IDs
- add more explicit scope guidance in publish docs
- add response fixtures from live verification for regression tests
