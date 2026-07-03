# Constraints & Escalation

## Constraints

- Only triggered when primary vision fails (or the current model has no image
  support at all).
- Only one fallback call per image (no retry loop).
- Never log or echo the value of `ARK_API_KEY`.
- **Never substitute this skill with local OCR** (`tesseract`, `ocrmypdf`, …).
  OCR extracts text only; it cannot infer layout, control types, or visual
  hierarchy. If the skill cannot run, stop and ask the user to configure the
  missing prerequisite instead of silently degrading to OCR.

## Escalation

If the fallback output is still insufficient:

- Escalate to a stronger vision model (e.g. GPT-4o / Claude Vision).
- Do NOT loop this skill on the same image.

## Scope

This skill is a low-cost multimodal reasoning fallback layer for:

- UI screenshots
- terminal outputs
- mobile apps
- documents with OCR
- structured visual content
