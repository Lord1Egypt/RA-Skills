---
name: vision-fallback
description: Vision/image understanding for agents whose model can't read images (returns "model does not support images", empty/unknown output, low confidence, or user-reported failure). Calls an OpenAI-compatible vision API (doubao or any OpenAI-compatible provider), returns structured JSON. Use whenever an image must be understood. Do NOT substitute with local OCR (tesseract) - OCR extracts text only, not layout/visual understanding.
compatibility: bash, curl, jq, file, base64; requires VISION_API_KEY (universal) or ARK_API_KEY / OPENAI_API_KEY
---

# vision-fallback

> Calls an OpenAI-compatible vision API via `/chat/completions`.
> Default provider: Volcengine Ark (doubao). Set `VISION_PROVIDER=openai` to use
> any OpenAI-compatible endpoint (OpenAI, OpenRouter, Azure, vLLM, etc.).
> Only credential needed: `VISION_API_KEY` (universal) or a provider-specific key.

## Trigger

Use when ANY holds:

- the current model **does not support images at all** (e.g. returns
  `model does not support images`, `images are not supported`, or refuses to
  read the attached image)
- vision output empty/null, or says "unknown" / "cannot determine"
- vision confidence < 0.5 (if available)
- OCR text exists but the primary model fails to interpret it
- user says the image is not understood / result is wrong

Otherwise do NOT use this skill.

## ⚠️ No OCR substitution

Do **NOT** fall back to local OCR (`tesseract`, `ocrmypdf`, …) as a substitute.
OCR extracts text only - it cannot infer layout, control types (switch / radio /
card), or visual hierarchy. If the skill cannot run (see Preflight), **stop and
tell the user** the missing prerequisite (usually an API key) instead of
silently degrading to OCR.

## Preflight (run once before the first call)

```bash
./scripts/check.sh
```

Exits 0 only when all prerequisites are present (shell deps + API key resolved +
endpoint reachable). If it fails, read its stderr, fix the reported
prerequisite, and re-run. Do not proceed to `call-api.sh` until `check.sh`
passes - a failed preflight means the API call will fail anyway.

## Input

`image` (required: file path / URL / data URL), `ocr_text`, `failure_reason`,
`primary_model_output` (all optional).

## Workflow

1. Run `./scripts/check.sh`. If non-zero, stop and report to the user (see
   above) - do not fall back to OCR.
2. `./scripts/call-api.sh "$IMAGE" "$OCR_TEXT" "$FAILURE_REASON" "$PRIMARY_OUTPUT"`
   - resolves provider config + API key, converts the image to a data URL,
   assembles the payload, and POSTs. See
   [references/configuration.md](references/configuration.md) for config and
   key-resolution order.
3. Parse `choices[0].message.content` -> structured JSON. Schema in
   [references/output-format.md](references/output-format.md).
4. If still insufficient -> escalate to a stronger model (set `VISION_MODEL`
   or switch `VISION_PROVIDER`); do NOT retry this skill and do NOT fall back
   to OCR. Full rules in [references/constraints.md](references/constraints.md).

API endpoint/body/model note: [references/api-reference.md](references/api-reference.md).

## Provider configuration

| `VISION_PROVIDER` | Backend | Default model | Key env var |
|---|---|---|---|
| `ark` (default) | Volcengine Ark / doubao | `doubao-seed-2.0-lite` | `ARK_API_KEY` |
| `openai` | Any OpenAI-compatible API | `gpt-4o-mini` | `OPENAI_API_KEY` |

`VISION_API_KEY` overrides provider-specific keys and works universally.
Set `VISION_BASE_URL` + `VISION_MODEL` for third-party OpenAI-compatible
providers (OpenRouter, Azure, vLLM, etc.).

## If the current model has NO image support

This is the most common real-world trigger. In that case this skill is **not a
fallback, it is the vision layer** - use it directly whenever the user provides
an image that must be understood.
