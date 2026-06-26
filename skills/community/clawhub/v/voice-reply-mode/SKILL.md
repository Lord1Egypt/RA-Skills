---
name: voice-reply-mode
description: Add same-modality conversation behavior to an agent: voice in → voice out, text in → text out. Use when enabling Telegram/Feishu voice-note workflows with Edge TTS, documenting agent voice preferences, and providing gateway config snippets for inbound-only TTS auto replies.
---

# Voice Reply Mode

Use this skill when a user wants an agent to behave like this:
- 用户发语音 → agent 回语音
- 用户发文字 → agent 回文字

## What this skill includes

- Workspace-level behavior rules for `SOUL.md` / `IDENTITY.md` / `TOOLS.md`
- A reusable Edge TTS helper script
- Gateway config snippets for `messages.tts`
- Channel notes for Telegram / Feishu style deployments

## Important boundary

This skill can package **rules, scripts, and config snippets**.

It does **not** automatically change a user's global gateway config unless the user explicitly asks and authorizes it.

## Recommended workflow

1. Read `references/workspace-snippets.md`
2. Read `references/gateway-config.md`
3. Copy the relevant snippets into the target agent workspace
4. If the user explicitly asks, patch gateway config with the snippet from `references/gateway-config.md`
5. Validate with one text message and one voice message

## Minimal success criteria

- Text message receives text reply
- Voice message receives voice reply
- Agent workspace documents the preferred voice

## Files in this skill

- `references/workspace-snippets.md` — snippets for `IDENTITY.md`, `SOUL.md`, `TOOLS.md`
- `references/gateway-config.md` — `messages.tts` examples and caveats
- `references/channel-notes.md` — Telegram / Feishu notes
- `scripts/edge-tts.sh` — helper script for local TTS generation

## Notes

- In many deployments, the decisive switch is gateway-level `messages.tts.auto = "inbound"`.
- Workspace files define behavior expectations, but gateway config determines whether automatic voice replies actually happen.
- If schema rejects `identity.voice`, keep voice preference in workspace docs instead.
