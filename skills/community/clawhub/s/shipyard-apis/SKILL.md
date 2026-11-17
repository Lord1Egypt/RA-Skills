---
name: apis
description: "Add outside services to an app the safe way: one guide and checker for every API key (where to get it, its name, where it lives, a cheap test), web search (Brave, Serper, SerpAPI with fallbacks), voice (Deepgram speech-to-text, ElevenLabs text-to-speech), an AI model router (OpenRouter, Groq, OpenAI, Gemini, NVIDIA) and rate limits with Upstash Redis. Use for \"API key\", \"check my keys\", \"add search\", \"Brave\", \"Serper\", \"SerpAPI\", \"speech to text\", \"text to speech\", \"Deepgram\", \"ElevenLabs\", \"which AI model\", \"OpenRouter\", \"Groq\", \"NVIDIA\", \"Gemini\", \"rate limit\", \"Upstash\", \"Redis\", or \"/shipyard:apis\"."
---

# Shipyard APIs

> Part of the Shipyard plugin. This skill runs Shipyard's own scripts and key guard, so it does not work on its own. If it was installed by itself (for example through skills.sh, ClawHub, Hermes, pi or aiden) and Shipyard's `scripts/` folder is not on this computer, stop and install the full plugin first by following https://github.com/philipposk/shipyard/blob/main/INSTALL.md, then start again.

You add outside services (APIs: other companies' tools an app calls) to a Shipyard app without leaking keys or running up a bill. You run every script. The student only makes accounts, creates keys in the provider's dashboard and pastes them into the keys file.

## Rules (always)

- You do the work. Never hand the student a command you could run.
- Never ask for keys in the chat and never read `~/.shipyard/secrets.env` or `.env*` files. Keys go in with `node "${CLAUDE_PLUGIN_ROOT}/scripts/secrets-init.mjs"`; `secrets-check.mjs` shows names with a tick or a cross, never values.
- Every call to a paid API runs on the server (a route under `src/app/api/`), checks the signed-in user, has a rate limit and an input size limit, and the app still works when the call fails.
- Plain English, one question at a time with your recommended answer.
- Say which parts are proven and which are **new, untested in production** (marked in the references). Do not present the second kind as tested.

## 1. Ask one question

"What should the app do?" Read the matching reference, then follow it:

1. **Add or check a key** -> `references/api-keys.md`
2. **Search the web** -> `references/web-search.md`
3. **Speech to text or a voice** -> `references/voice.md`
4. **AI text features, pick a model** -> `references/ai-router.md` (and new-app's `references/ai-and-keys.md`)
5. **Limit abuse or cache answers** -> `references/rate-limit.md`

## Scripts

- `secrets-check.mjs [--live]` checks every key's format; `--live` makes one cheap call per provider (Brave and Serper use one search credit each; NVIDIA is format-only).
- `app-keys.mjs <appDir> NAME ...` gives one app the keys it needs (Vercel and `.env.local`) without printing them. Then `provision-vercel.mjs` and redeploy.
