# API keys: where to get them, names, storage, checks

All keys live in the student's keys file `~/.shipyard/secrets.env` (one `NAME=value` line each, on their computer only). Add a missing one with `secrets-init.mjs` (it adds the empty line with a hint; the student pastes the value), check with `secrets-check.mjs --live`, and give it to an app with `app-keys.mjs <appDir> NAME`. Apps read them from `process.env.NAME` on the server only. Nothing here goes in `NEXT_PUBLIC_*` names, the repo or a chat.

| Service | Env var | Where to get it | Cheap check (`--live`) |
|---|---|---|---|
| OpenRouter | `OPENROUTER_API_KEY` | openrouter.ai > Keys | `GET /api/v1/key` (free) |
| OpenAI | `OPENAI_API_KEY` | platform.openai.com > API keys | `GET /v1/models` (free) |
| Groq | `GROQ_API_KEY` | console.groq.com > API Keys | `GET /openai/v1/models` (free) |
| Deepgram | `DEEPGRAM_API_KEY` | console.deepgram.com > API Keys | `GET /v1/projects` (free) |
| ElevenLabs | `ELEVENLABS_API_KEY` | elevenlabs.io > Developers > API Keys | `GET /v1/user` (free; key needs "User: read") |
| NVIDIA | `NVIDIA_API_KEY` | build.nvidia.com > a model > Get API Key | format only (`nvapi-`) |
| Gemini | `GEMINI_API_KEY` | aistudio.google.com > Get API key (free tier) | `GET /v1beta/models` (free) |
| Brave Search | `BRAVE_API_KEY` | api-dashboard.search.brave.com | one search (`count=1`), uses 1 query |
| Serper | `SERPER_API_KEY` | serper.dev > API Key | one search, uses 1 credit |
| SerpAPI | `SERPAPI_API_KEY` | serpapi.com > Your Account | `GET /account.json` (free) |
| Upstash Redis | `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN` | console.upstash.com > database > REST API | `PING` (1 command) |
| Resend | `RESEND_API_KEY` | resend.com > API Keys (full access, stays on the computer) | `GET /domains` |
| Stripe | `STRIPE_SECRET_KEY` (test), `STRIPE_LIVE_*` | dashboard.stripe.com > Developers > API keys | `GET /v1/balance` |

Rules per key:
- Resend: apps never get this one; `/shipyard:launch` makes each app a sending-only key.
- Stripe live keys: only the go-live step uses them.
- Upstash: give an app both names. The token is only ever sent to an `https://*.upstash.io` URL (the checker refuses otherwise).
- Set a monthly spend limit in each paid dashboard (OpenAI, OpenRouter, ElevenLabs, Serper) before an app goes public.
- A key pasted anywhere public: revoke it in the provider's dashboard first, then make a new one.

`app-keys.mjs` only knows the names above. Groq (`GROQ_API_KEY`, fast models) is not Grok (xAI); Grok is not in Shipyard's list.
