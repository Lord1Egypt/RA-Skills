# Constraints & Escalation

## Constraints

- Only triggered when primary vision fails (or the current model has no image
  support at all).
- Only one fallback call per image (no retry loop).
- Never log or echo the value of any API key (`VISION_API_KEY`, `ARK_API_KEY`,
  `OPENAI_API_KEY`, …).
- **Never substitute this skill with local OCR** (`tesseract`, `ocrmypdf`, …).
  OCR extracts text only; it cannot infer layout, control types, or visual
  hierarchy. If the skill cannot run, stop and ask the user to configure the
  missing prerequisite instead of silently degrading to OCR.

## Escalation

If the fallback output is still insufficient:

- Escalate to a stronger vision model by setting `VISION_MODEL` to a higher-tier
  model (e.g. `gpt-4o`, `doubao-vision-pro`, `claude-3.5-sonnet` via an
  OpenAI-compatible proxy).
- Alternatively, switch provider: `export VISION_PROVIDER=openai` (or `ark`).
- Do NOT loop this skill on the same image.

## Scope

This skill is a low-cost multimodal reasoning fallback layer for:

- UI screenshots
- terminal outputs
- mobile apps
- documents with OCR
- structured visual content
