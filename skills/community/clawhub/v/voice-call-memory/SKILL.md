---
name: voice-call-memory
description: Memory for voice agents and voice-first workflows — every call transcribed, summarized, and searchable by caller, topic, and outcome. Use when a voice agent must remember callers across conversations. Requires a BlueColumn API key (bc_live_*).
---

# Voice Call Memory — BlueColumn Skill

A voice agent that forgets the last call is a phone tree with extra steps. This skill gives voice agents real continuity: who called, why, what was said, and what was promised — ready before the first "hello".

## Store the call summary

After each call, store a structured summary with the caller, purpose, and outcome.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "VOICE CALL +12065550123 (7/31 14:20): asked about Builder plan pricing; concern about overage fees; agreed to email pricing sheet today; tone friendly but rushed; follow up Friday.", "title": "voice - +12065550123 7/31"}'

## Prepare before answering

Pull the caller's history the moment a call connects.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What do we know about this caller from past calls and open promises?"}'

## Voice workflow

1. **On connect** — recall caller history and open items before speaking.
2. **During** — note the purpose, objections, and emotional cues.
3. **On hang-up** — store the summary immediately, including next steps.
4. **Hand off** — if a human takes over, provide the stored summary so the caller never repeats themselves.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Promise to +12065550123: pricing sheet by Aug 1 EOD. Escalate to human if they call back before Friday.", "tags": ["voice", "handoff"]}'

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
