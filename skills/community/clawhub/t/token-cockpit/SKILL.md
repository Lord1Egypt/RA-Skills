---
name: token-cockpit
version: "1.0.0"
description: "See and slash your OpenClaw / LLM token bill. Use this skill whenever the user asks about token usage, model spend, API costs, or wants to save money on their agent, including phrases like 'how much am I spending,' 'what's my token usage,' 'why is my bill so high,' 'break down my costs by model,' 'am I over budget,' 'set a budget alert,' 'how do I cut my costs,' 'which model is costing me the most,' 'should I switch to a cheaper model,' 'how much would I save with Haiku,' 'project my monthly spend,' or 'optimize my model routing.' Reads local usage logs (no API key, nothing leaves the machine), prices them with an editable model-price table, projects monthly spend, raises budget alerts, and finds expensive-model calls that could safely run on a cheaper model. The cost dashboard OpenClaw doesn't ship with."
metadata:
  openclaw:
    emoji: 💸
---

# Token Cockpit

Running an agent feels free until the invoice lands. Token Cockpit turns the local usage logs you already have into a clear picture of where the money goes - and, more usefully, where it's being wasted. Everything is computed locally; no API key, no data leaves the machine.

Four jobs:

1. **Report** - spend and token volume broken down by model, with a monthly projection.
2. **Budget** - compare spend (or projected monthly spend) against a limit and emit a ready-to-send alert when you're close or over.
3. **Route** - find small, cheap-to-serve calls that are running on premium models and estimate the savings from downgrading them.
4. **Simulate** - a what-if: "how much would I save if I moved all my Opus traffic to Haiku?"

## When to use this

Any time cost or usage comes up: "how much am I spending," "why is my bill so high," "break this down by model," "am I over budget," "should I switch to a cheaper model," "how much would Haiku save me," "project my monthly spend." If the user wants to *reduce* spend, lead with `route` and `simulate`; if they want to *understand* it, lead with `report`.

## The tool

```bash
python token_cockpit.py report   --logs PATH [--days N]
python token_cockpit.py budget   --limit 50 [--period month|window] --logs PATH
python token_cockpit.py route    --logs PATH [--small-tokens 2000]
python token_cockpit.py simulate --from claude-opus --to claude-haiku --logs PATH
```

Add `--json` to any command for structured output you can reason over. `--days N` limits any command to the last N days.

### Finding the usage log

The tool auto-detects common locations (`$OPENCLAW_USAGE_LOG`, `~/.openclaw/usage.jsonl`, `~/.openclaw/logs/usage.jsonl`, and the `/data/.openclaw` equivalents). If none exist, ask the user where their usage data lives and pass `--logs`. The loader is tolerant: it accepts JSONL or a JSON array, reads token counts from many field-name variants (`input_tokens`/`prompt_tokens`/`tokens_in`, etc.), and reads usage nested under a `usage` object. A bundled `sample_usage.jsonl` is included so you can demonstrate the output even before the real log is located.

## A note on prices - read this before quoting dollars

The price table in `token_cockpit.py` is a set of **editable defaults** in USD per million tokens, and model prices change over time. Treat the script's dollar figures as estimates. When the user wants exact numbers, confirm current pricing and override with a `pricing.json`:

```json
{
  "claude-opus": {"input": 15.0, "output": 75.0},
  "claude-haiku": {"input": 1.0, "output": 5.0},
  "gpt-4o-mini": {"input": 0.15, "output": 0.60}
}
```

Pass it with `--pricing pricing.json`. Any model with no matching entry is counted as $0 and clearly flagged (⚠) in the report so the totals are never silently wrong.

## How to help

1. **Understand-the-bill requests:** run `report`. Read back the headline (total + monthly projection) and the top one or two models by cost - that's where attention belongs. Don't recite every model.
2. **Save-money requests:** run `route` first. It finds the specific waste (small tasks on premium models) and quantifies it. Then offer `simulate` for the bigger "what if I just switched defaults" question.
3. **Budget setup:** run `budget --limit X`. The output is phrased as an alert message - if the user wants ongoing monitoring, this pairs naturally with a scheduled task that runs `budget` daily and messages them only when the level is WARN or OVER.

## Interpreting the output honestly

- The monthly projection extrapolates from the window's daily rate. Say so - a projection from three days of data is rougher than from thirty.
- Routing and simulation savings assume the cheaper model uses the same token counts and does the job well enough. They're upper-bound estimates. Always pair the number with "verify quality before switching defaults" - a cheaper model that fails the task and forces a retry costs more, not less.
- A clean `route` result ("no obvious wins") is a real and good answer. Don't manufacture savings that aren't there.

## Pairs well with

A scheduled daily `budget` check that only pings when you cross 80% of your limit gives you a spend tripwire without having to think about it.
