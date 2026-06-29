# Use Sage Router with OpenClaw

Sage Router can sit between OpenClaw and multiple model providers so agents can use one stable endpoint.

```bash
openclaw skill add sage-router --from clawhub
openclaw skill configure sage-router
```

Start Sage Router on port `8790`.

OpenAI-compatible tools:

```bash
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=local-router
```

Anthropic-compatible tools:

```bash
export ANTHROPIC_BASE_URL=http://localhost:8790
export ANTHROPIC_API_KEY=local-router
```

Use provider-qualified names when needed, for example `ollama/qwen2.5-coder:latest`, `openai/gpt-4.1`, `anthropic/claude-sonnet-4-6`, or `nvidia/meta/llama-3.1-405b-instruct`.

## OpenAI Codex via OpenClaw (OAuth passthrough)

OpenClaw's `openai-codex` provider is now wired to `provider=openai, type=oauth` in the auth profile store. The `openai-codex-responses` API type talks **directly** to `https://chatgpt.com/backend-api/codex` using the OAuth bearer token — no more routing through the OpenClaw gateway for authentication.

### Primary token sources (in order)

1. `OPENAI_CODEX_API_KEY` — written by OpenClaw to `~/.openclaw/.env` (this is the **default**).
2. `OPENAI_CODEX_ACCESS_TOKEN` / `OPENAI_CODEX_OAUTH_TOKEN` — explicit env overrides.
3. `~/.openclaw/agents/main/agent/auth-profiles.json` — runtime fallback if no env value is set.
4. `SAGE_ROUTER_OPENAI_CODEX_ACCESS_TOKEN` / `SAGE_ROUTER_OPENAI_CODEX_OAUTH_TOKEN` — Sage Router-prefixed overrides (e.g. hosted Cloud Run).

Both Umbrel and Cyber compose files pass `OPENAI_CODEX_API_KEY` through to the container, so a fresh `openclaw login chatgpt` is enough to make the router serve Codex models.

### If `OPENAI_CODEX_API_KEY` is not set

Sage Router falls back to registering `openai-codex` as an `openclaw-gateway` provider so model discovery still resolves. As soon as OpenClaw writes a token to `auth-profiles.json`, `load_openclaw_providers()` will overwrite the entry with a direct-Codex provider.
