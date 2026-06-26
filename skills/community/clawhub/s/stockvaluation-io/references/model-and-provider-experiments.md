# Model And Provider Experiments

## Main Env Vars

The most useful knobs are:

```text
DEFAULT_LLM_PROVIDER=
AGENT_LLM_PROVIDER=
JUDGE_LLM_PROVIDER=
AGENT_LLM_MODEL=
JUDGE_LLM_MODEL=
TAVILY_API_KEY=
DUMP_PROMPTS=
PROMPT_DUMP_DIR=
```

The exact provider resolution logic lives in `shared/llm_models.py` when the repo is available.
Provider API keys come from `.env.example`: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GROQ_API_KEY`, `GEMINI_API_KEY`, and `OPENROUTER_API_KEY`.

## Common Experiment Patterns

Cheap or fast run:

```text
AGENT_LLM_PROVIDER=anthropic
AGENT_LLM_MODEL=claude-haiku-4-5-20251001
JUDGE_LLM_PROVIDER=anthropic
JUDGE_LLM_MODEL=claude-haiku-4-5-20251001
```

Higher-quality run:

```text
AGENT_LLM_PROVIDER=anthropic
AGENT_LLM_MODEL=claude-opus-4-6
JUDGE_LLM_PROVIDER=anthropic
JUDGE_LLM_MODEL=claude-sonnet-4-5
```

Cross-provider comparison:

```text
AGENT_LLM_PROVIDER=openai
AGENT_LLM_MODEL=gpt-4o
JUDGE_LLM_PROVIDER=anthropic
JUDGE_LLM_MODEL=claude-sonnet-4-5
```

## Prompt Dumping

To inspect prompts:

```text
DUMP_PROMPTS=true
PROMPT_DUMP_DIR=./local_data/prompts
```

After a run, inspect the dump directory and compare prompts across experiments.
This is opt-in and privacy-sensitive: the dump directory can contain full prompt text, ticker context, and retrieved research snippets, so do not enable it for sensitive work and clean it up after comparisons if needed.

## Restart Scope

If only provider or model settings changed, restart:

```bash
docker compose -f docker-compose.local.yml restart valuation-agent bullbeargpt
```

If the user changed deeper service wiring, env secrets, or compose dependencies, restart more broadly:

```bash
docker compose -f docker-compose.local.yml up -d --build
```

## Comparison Workflow

For controlled comparisons:

1. Pick one ticker.
2. Save the baseline output.
3. Change only the model or provider variables.
4. Restart the affected services.
5. Run the same ticker again.
6. Compare valuation deltas, override assumptions, and narrative changes separately.
