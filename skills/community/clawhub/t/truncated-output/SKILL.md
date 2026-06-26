---
name: truncated-output
description: The reply ends mid-sentence or mid-code-block because the model hit a token limit or was cut short.
emoji: ✂️
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# truncated-output

The reply the user receives is incomplete — the model ran out of tokens, the stream was cancelled, or a code fence opened without closing.

## Symptoms

- Reply ends without terminal punctuation and reads as if more was coming.
- A fenced code block is open (```` ``` ````) with no matching close.
- Enumerated lists or steps trail off before the final item.
- Provider metadata reports `finish_reason: "length"` or `stop_reason: "max_tokens"`.

## What to do

- Before returning the reply, check for an unmatched code fence. If present, the reply is incomplete — do not ship it.
- Check the provider's finish reason. If it indicates a length cap, regenerate with a higher `max_tokens` budget or summarize the remaining work inline.
- Watch context budget. If the prompt is already close to the context ceiling, the reply has no room — trim context before retrying, don't just raise the cap.
- If truncation happens repeatedly on the same task, break the task into smaller turns instead of asking for one giant reply.
- When truncation cannot be avoided (e.g., streaming to a channel with its own cap), surface the incompleteness to the user explicitly rather than pretending the reply is done.
