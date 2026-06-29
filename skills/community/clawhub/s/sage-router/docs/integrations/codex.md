# Use Sage Router with Codex CLI

Codex CLI can use Sage Router as an OpenAI-compatible endpoint.

## Setup

Start Sage Router on port `8790`, then add a Codex provider that forwards the
API key from `OPENAI_API_KEY`:

```toml
# ~/.codex/config.toml
[model_providers.sage-router]
name = "Sage Router"
base_url = "http://127.0.0.1:8790/v1/"
env_key = "OPENAI_API_KEY"
wire_api = "responses"
```

Create a Sage Router profile:

```toml
# ~/.codex/sage-router.config.toml
model_provider = "sage-router"
model = "sage-router/frontier"
```

Then export a local router token or generated `sk_sage_*` key and start Codex:

```bash
export OPENAI_API_KEY=local-router
codex --profile sage-router
```

Use a provider-qualified model when you want an explicit route:

```bash
codex --model openai/gpt-4.1
codex --model ollama/qwen2.5-coder:latest
```

Recommended policy:

- Coding/refactor/debugging: coding-strong local model first, cloud fallback second.
- Large reasoning or fragile edits: higher-capability cloud model first.
- Background maintenance: local-first mode.
