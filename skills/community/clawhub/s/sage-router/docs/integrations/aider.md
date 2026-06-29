# Use Sage Router with Aider

Aider can use Sage Router through the OpenAI-compatible endpoint. Sage Router
picks the best model per edit and fails over across your own providers
(OpenAI-compatible, Anthropic, Gemini, NVIDIA NIM, Ollama, Ollama Cloud) so Aider
keeps working when one provider is slow, down, or rate-limited.

## Setup

Start Sage Router:

```bash
python3 router.py --port 8790
```

Point Aider at it:

```bash
export OPENAI_API_BASE=http://127.0.0.1:8790/v1
export OPENAI_API_KEY=local-router
aider --model openai/auto
```

`openai/auto` lets Sage Router select by policy. Pin a provider-qualified model
when you want an explicit route:

```bash
aider --model openai/openai/gpt-4.1
aider --model openai/ollama/qwen2.5-coder:latest
```

## Recommended routing

- Coding-strong local model first (Ollama `qwen2.5-coder`), cloud fallback for
  larger edits or failed local routes.
- `local-first` route mode for cheap background edits.
- `balanced` for normal coding sessions.
- `best` for fragile refactors where quality matters most.

## Failover

If the first-choice provider is unhealthy or rate-limited, Sage Router retries
the next healthy provider in the chain — Aider's edit stream is preserved.

## Compliance

BYOK/BYOS only. No resale, no pooling, no ToS bypass. Credentials stay local.
