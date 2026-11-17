---
name: the-scribble-thing
description: Turn a user-provided PNG or JPEG line-art illustration into a hand-drawn scribe animation. Use when the user wants an illustration, diagram, storyboard, or product concept revealed as an MP4, with optional drawing-order instructions and a drawing hand.
---

# The Scribble Thing

Use the connected The Scribble Thing MCP server when it is available. Its public
endpoint is `https://scribble.boringstuff.club/mcp` and the REST fallback guide
is `https://scribble.boringstuff.club/docs/agent-api`.

## Before creating

- Require one PNG or JPEG image. Line art and simple illustrations work best.
- Ask only for missing choices: drawing order is optional, hand display defaults
  to off, and speed defaults to normal.
- Call `get_scribble_service_info` for current limits, retention, terms, and
  pricing. Do not rely on values remembered from an earlier run.
- Before the first creation, tell the user that uploaded and generated files are
  retained for up to the reported retention period. Obtain explicit confirmation
  that the user accepts the current terms and has the rights needed to use the
  artwork. Do not infer acceptance.

## Create and monitor

1. Call `create_scribe_animation` with the image as raw base64, not a data URL.
   Supply a fresh non-personal idempotency key. Reuse that key only when retrying
   the identical request.
2. Preserve the returned animation ID and capability token as secrets. Never put
   them in ordinary chat text, logs, analytics, filenames, or unrelated tools.
3. Poll `get_scribe_animation` every 3-5 seconds until it reports `completed` or
   `failed`. Do not hold a long-running request open.
4. On completion, give the user the watermarked preview and private management
   link. State that the free preview contains a watermark.
5. If the user wants the clean video, prefer the management link so the user can
   purchase or enter a code privately. Call `redeem_scribe_unlock_code` only when
   the user explicitly supplies a code and asks the agent to redeem it.
6. Use `get_scribe_animation_download` for a short-lived download URL. Do not
   place video bytes into the model context.

If the MCP host cannot send the attached image as base64, follow the REST guide's
multipart upload workflow instead of fetching an arbitrary remote image URL.

## Handoff and cleanup

- Explain failures in plain language and preserve the same idempotency key for a
  safe retry of unchanged inputs.
- Remind the user that the private management URL grants access to one animation
  and should not be shared unintentionally.
- Call `delete_scribe_animation` when the user asks for early deletion. Never
  delete merely because the current conversation is ending.
