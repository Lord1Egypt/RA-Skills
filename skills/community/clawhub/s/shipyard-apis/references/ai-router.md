# Pick the AI provider and model per task

new-app's `references/ai-and-keys.md` has the proven default order (OpenRouter, then Groq, then OpenAI). This adds Gemini and NVIDIA and a small router. The router itself is **new, untested in production**.

All five accept the OpenAI chat format (`POST <base>/chat/completions`, header `Authorization: Bearer <key>`), so one function covers them:

| Provider | Env var | Base URL | Good for |
|---|---|---|---|
| OpenRouter | `OPENROUTER_API_KEY` | `https://openrouter.ai/api/v1` | one key, hundreds of models, cheap ones first |
| Groq | `GROQ_API_KEY` | `https://api.groq.com/openai/v1` | very fast, free tier, Whisper speech-to-text |
| OpenAI | `OPENAI_API_KEY` | `https://api.openai.com/v1` | best structured output and tools |
| NVIDIA | `NVIDIA_API_KEY` | `https://integrate.api.nvidia.com/v1` | free hosted open models for trials (rate-limited) |
| Gemini | `GEMINI_API_KEY` | `https://generativelanguage.googleapis.com/v1beta/openai` | free tier, long inputs, images (OpenAI-compatible endpoint) |

Gemini: Google documents an OpenAI-compatible endpoint (`.../v1beta/openai/chat/completions`, Bearer key). The free tier has per-minute and per-day limits and Google may use free-tier prompts to improve its products: do not send users' private data through the free tier. Check current limits at ai.google.dev before relying on it.

## Router shape

- `src/lib/ai.ts` with `chat(task, messages)` where `task` is `"cheap"`, `"fast"`, `"smart"` or `"json"`. A table maps each task to an ordered list of `{ provider, model }`; the first entry whose key is set is used, the next on timeout, 429 or 5xx.
- Suggested start (adjust with the student, write it in `SPEC.md`): `fast` Groq then OpenRouter; `cheap` Gemini (free tier, a Flash model) then OpenRouter (a small model) then NVIDIA; `smart` OpenAI then OpenRouter; `json` OpenAI (structured outputs) then OpenRouter.
- Log provider, model, tokens and duration per call (no prompt text), so cost per feature is visible in the admin logs.
- Never let a user pick an arbitrary model name; only the table's entries.
- Tests fake each provider and the fallback.
