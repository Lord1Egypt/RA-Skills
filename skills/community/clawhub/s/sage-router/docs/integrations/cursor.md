# Use Sage Router with Cursor

Cursor can use Sage Router through OpenAI-compatible or Anthropic-compatible settings, depending on how your Cursor environment is configured.

## OpenAI-compatible endpoint

```bash
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=local-router
```

## Anthropic-compatible endpoint

```bash
export ANTHROPIC_BASE_URL=http://localhost:8790
export ANTHROPIC_API_KEY=local-router
```

## Recommended routing

- Code edits and refactors: coding-strong model with cloud fallback.
- Chat and quick explanations: fast or local-first route.
- Large-file reasoning or risky changes: best route.

Keep Cursor pointed at one endpoint and move provider selection into Sage Router policy instead of changing tool settings for every task.
