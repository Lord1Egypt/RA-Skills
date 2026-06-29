# Use Sage Router with Pi agents

Pi agents can route through Sage Router when they support an OpenAI-compatible base URL or run behind an OpenAI-compatible adapter.

## Environment

```bash
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=local-router
```

## Recommended use

- Local-first for routine background work.
- Balanced routing for coding, documentation, and analysis.
- Best routing for high-value reasoning or tasks where retries are expensive.

## Model names

Use `auto` for policy routing, or provider-qualified names such as:

- `ollama/qwen2.5-coder:latest`
- `openai/gpt-4.1`
- `anthropic/claude-sonnet-4-6`
- `nvidia/meta/llama-3.1-405b-instruct`
