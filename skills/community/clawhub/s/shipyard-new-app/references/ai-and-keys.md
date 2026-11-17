# AI features, service keys and feature ideas

## Use AI on the server where it helps

When a feature would be better with AI, build it in: summaries, tags and categories picked for the person, search by meaning, drafting text, turning speech into text, pulling fields out of a pasted message or photo. Rules:

- AI calls run on the server only (a route under `src/app/api/`), never in the browser. The key never reaches the page.
- Every AI route checks the signed-in user, has a rate limit (`src/lib/rate-limit.mjs`) and a size limit on input.
- The app must still work when the AI call fails or the key is missing: show the plain version and a short message.
- Write the prompt and the parsing as a small function with a test (fake the provider response in the test).
- Default provider order: OpenRouter (one key, many models, cheap ones first), then Groq (very fast, free tier, also speech-to-text with Whisper), then OpenAI. Speech-to-text: Groq Whisper or Deepgram. Pick the cheapest model that does the job well and say which in `SPEC.md`.

## Give the app its keys (never ask in the chat)

The student's keys live in the Shipyard keys file. To give an app the ones a feature needs:

`node "${CLAUDE_PLUGIN_ROOT}/scripts/app-keys.mjs" <appDir> OPENROUTER_API_KEY GROQ_API_KEY`

It adds the names to the app (so `provision-vercel.mjs` copies them to the live app) and writes them to `.env.local` for local runs, without printing anything. Run it with no names to see what the app uses. If a key is missing, it says where to get it; the student adds it with `secrets-init.mjs`, then you run it again. After adding keys to a live app: `provision-vercel.mjs`, then redeploy. Email keys are not given this way: `/shipyard:launch` makes the app its own sending-only key.

Keys an app can use: `OPENROUTER_API_KEY`, `GROQ_API_KEY`, `DEEPGRAM_API_KEY`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`, `NVIDIA_API_KEY`, `GEMINI_API_KEY`, `BRAVE_API_KEY`, `SERPER_API_KEY`, `SERPAPI_API_KEY`, `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` (guides in `/shipyard:apis`), `STRIPE_*` test keys (via `/shipyard:launch`), `GOOGLE_CLIENT_*`.

## Suggest feature ideas

At the end of the plan (step 2) and again in the hand-off, suggest the 3 best next features for this app: what similar popular apps offer, what would make the main action faster, and where AI would save the person time. One line each with why. Do not build them unless the student says so; add the ones they like to `SPEC.md` under "later".
