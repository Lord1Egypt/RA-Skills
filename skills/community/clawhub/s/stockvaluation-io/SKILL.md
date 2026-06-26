---
name: stockvaluation-io
description: Set up, run, compare, and debug StockValuation.io, a local-first DCF valuation platform, including Docker startup, ticker valuations, LLM provider changes, prompt dumping, and troubleshooting.
version: 1.0.0
homepage: https://github.com/stockvaluation-io/stockvaluation_io
metadata:
  openclaw:
    emoji: "📈"
    homepage: https://github.com/stockvaluation-io/stockvaluation_io
    primaryEnv: CURRENCY_API_KEY
    requires:
      bins:
        - git
      anyBins:
        - docker
        - docker-compose
      env:
        - CURRENCY_API_KEY
        - POSTGRES_PASSWORD
        - DEFAULT_PASSWORD
        - YFINANCE_SECRET_KEY
        - VALUATION_AGENT_SECRET_KEY
        - BULLBEARGPT_SECRET_KEY
        - VALUATION_SERVICE_JWT_SECRET
        - ANTHROPIC_API_KEY
        - OPENAI_API_KEY
        - GROQ_API_KEY
        - GEMINI_API_KEY
        - OPENROUTER_API_KEY
        - TAVILY_API_KEY
        - DUMP_PROMPTS
        - PROMPT_DUMP_DIR
---

# StockValuation.io

Use this skill when the user wants help with StockValuation.io setup, local DCF runs, LLM provider or model experiments, prompt dumps, Docker logs, or valuation API usage.

## Workflow

1. Identify the goal: setup or startup, run a valuation, compare models, debug a failure, or inspect repo internals.
2. If the repo is available, inspect `README.md`, `.env.example`, `docker-compose.local.yml`, and relevant service files before answering.
3. For installation, startup, and basic valuation runs, read `{baseDir}/references/setup-and-run.md`.
4. For provider or model changes, prompt dumping, or controlled comparisons, read `{baseDir}/references/model-and-provider-experiments.md`.
5. For runtime failures, health checks, logs, or recovery steps, read `{baseDir}/references/troubleshooting.md`.
6. Prefer exact commands, explicit service names, and reproducible steps.

## Operating Rules

- Prefer the manual clone plus Docker Compose path by default.
- If the user wants the installer, tell them to download or inspect `install.sh` locally before running it instead of recommending `curl | bash`.
- Never ask the user to paste real API keys into chat. Tell them to set keys in their local environment or `.env`.
- Never print `.env` contents, echo live secrets, or suggest committing local secret files.
- Treat prompt dumping as privacy-sensitive. When `DUMP_PROMPTS=true`, prompt contents are written to `PROMPT_DUMP_DIR` on disk.
- Treat container teardown and volume deletion as destructive. Only suggest `down -v` when the user explicitly asks to reset local state.
- When only LLM settings change, restart `valuation-agent` and `bullbeargpt` unless the user also changed other infrastructure.
- When comparing experiments, keep the ticker, env changes, and output differences explicit so the comparison stays attributable.

## Useful Repo Signals

- Frontend UI: `http://localhost:4200`
- Valuation service: `http://localhost:8081`
- Valuation agent: `http://localhost:5001`
- BullBearGPT: `http://localhost:5002`
- Main flow often starts with `POST /api-s/valuate`
- High-value repo files when present: `README.md`, `.env.example`, `docker-compose.local.yml`, `shared/llm_models.py`, and `scripts/`
