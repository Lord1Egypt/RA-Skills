---
name: think-block-leakage
description: Internal reasoning from <think> blocks leaks into the final user-facing reply instead of being stripped.
emoji: 🧠
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# think-block-leakage

The model's internal reasoning escapes into the reply the user sees. This usually means an unclosed `<think>` / `<thinking>` tag, or a reply that begins with planning prose instead of the answer itself.

## Symptoms

- Reply contains literal `<think>`, `<thinking>`, or similar reasoning tags.
- Reply opens with "Let me think...", "Okay, the user wants...", "First I'll need to...", or other planning preamble.
- Reply is cut off mid-sentence and an opening reasoning tag has no matching close.
- A `</think>` appears with only a few dozen characters of content after it.

## What to do

- Inspect the raw LLM output for unmatched reasoning tags before returning it. Strip or redact any content inside reasoning tags.
- If the provider supports a separate reasoning channel, emit reasoning there and keep it out of the reply body entirely.
- If leakage is detected, regenerate the reply. Do not ship reasoning-as-answer.
- If the reply starts with planning language, trim the preamble. The user should see the answer first.
- For persistent leakage, tighten the system prompt to forbid meta-commentary in the reply body.
