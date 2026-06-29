# Use Sage Router with Continue

Continue can point at Sage Router as an OpenAI-compatible model provider.

Use this endpoint:

```text
http://localhost:8790/v1
```

Use this API key placeholder:

```text
local-router
```

Recommended model strategy:

- `auto` for Sage Router policy selection.
- Provider-qualified names for hard pins, for example `ollama/qwen2.5-coder:latest` or `openai/gpt-4.1`.
- `local-first` for cheap background edits and `balanced` for normal coding sessions.
