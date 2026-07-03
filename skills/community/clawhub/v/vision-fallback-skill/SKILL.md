---
name: vision-fallback
description: Vision/image understanding for agents whose model can't read images (returns "model does not support images", empty/unknown output, low confidence, or user-reported failure). Calls the Volcengine Ark (doubao) vision API, returns structured JSON. Use whenever an image must be understood. Do NOT substitute with local OCR (tesseract) — OCR extracts text only, not layout/visual understanding.
compatibility: bash, curl, jq, file, base64; requires ARK_API_KEY (Volcengine)
---

# vision-fallback

> Calls the Volcengine Ark (doubao) vision API — NOT OpenRouter. Only credential
> needed: `ARK_API_KEY`.

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
OCR extracts text only — it cannot infer layout, control types (switch / radio /
card), or visual hierarchy. If the skill cannot run (see Preflight), **stop and
tell the user** the missing prerequisite (usually `ARK_API_KEY`) instead of
silently degrading to OCR.

## Preflight (run once before the first call)

```bash
./scripts/check.sh
```

Exits 0 only when all prerequisites are present (shell deps + `ARK_API_KEY`
resolved + endpoint reachable). If it fails, read its stderr, fix the reported
prerequisite, and re-run. Do not proceed to `call-api.sh` until `check.sh`
passes — a failed preflight means the API call will fail anyway.

## Input

`image` (required: file path / URL / data URL), `ocr_text`, `failure_reason`,
`primary_model_output` (all optional).

## Workflow

1. Run `./scripts/check.sh`. If non-zero, stop and report to the user (see
   above) — do not fall back to OCR.
2. `./scripts/call-api.sh "$IMAGE" "$OCR_TEXT" "$FAILURE_REASON" "$PRIMARY_OUTPUT"`
   — resolves `ARK_API_KEY` itself, converts the image to a data URL, assembles
   the payload, and POSTs. See [references/configuration.md](references/configuration.md)
   for key-resolution order.
3. Parse `choices[0].message.content` → structured JSON. Schema in
   [references/output-format.md](references/output-format.md).
4. If still insufficient → escalate to a stronger model (GPT-4o / Claude
   Vision); do NOT retry this skill and do NOT fall back to OCR. Full rules in
   [references/constraints.md](references/constraints.md).

API endpoint/body/model note: [references/api-reference.md](references/api-reference.md).

## If the current model has NO image support

This is the most common real-world trigger. In that case this skill is **not a
fallback, it is the vision layer** — use it directly whenever the user provides
an image that must be understood.
