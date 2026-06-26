# Token Cockpit 💸

See and slash your OpenClaw / LLM token bill. The cost dashboard OpenClaw doesn't ship with.

Running an agent feels free until the invoice lands. Token Cockpit turns the usage logs you already have into a clear picture of where the money goes — and where it's being wasted. Everything runs locally: no API key, nothing leaves your machine.

## What it does

- **Report** — spend and token volume by model, with a monthly projection.
- **Budget** — compare spend (or projected monthly) against a limit and emit a ready-to-send alert when you're close or over.
- **Route** — find small, cheap-to-serve calls running on premium models and estimate what downgrading them would save.
- **Simulate** — what-if: "how much would I save moving all my Opus traffic to Haiku?"

## Quick start

```bash
python token_cockpit.py report   --logs sample_usage.jsonl
python token_cockpit.py budget    --limit 50 --logs sample_usage.jsonl
python token_cockpit.py route     --logs sample_usage.jsonl
python token_cockpit.py simulate  --from opus --to claude-haiku --logs sample_usage.jsonl
```

A `sample_usage.jsonl` is bundled so you can see real output immediately. For your own data, the log path auto-detects (`~/.openclaw/usage.jsonl` and similar) or pass `--logs`. The loader accepts JSONL or a JSON array and is tolerant of different field names (`input_tokens` / `prompt_tokens` / `tokens_in`, nested `usage` objects, etc.).

## About prices

The built-in price table is **editable defaults** (USD per 1M tokens) and model prices drift over time — treat the dollar figures as estimates. Override with a `pricing.json` and `--pricing pricing.json` for exact numbers. Unknown models are counted as $0 and flagged (⚠) so totals are never silently wrong.

## Pairs well with

A scheduled daily `budget` check that pings you only when you cross 80% of your limit — a spend tripwire you never have to think about.

## Requirements

- Python 3.8+ (standard library only)
