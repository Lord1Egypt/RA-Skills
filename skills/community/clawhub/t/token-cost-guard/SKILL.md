---
name: token-cost-guard
description: Monitor agent token usage and model cost from the active ecosystem's own records, compare the current run with the previous snapshot, and send an alert report when cost growth exceeds a threshold. In OpenClaw it reads OpenClaw session logs; in Hermes agent it reads Hermes logs/state.db instead of OpenClaw. Use when users ask to track token spend, calculate realtime token cost, detect spending spikes, monitor DeepSeek/Kimi/GPT model usage, or set up cost alerts for OpenClaw or Hermes agents.
---

# Token Cost Guard

Use this skill to compute agent token costs from the current runtime's own usage records and warn in Chinese reports when spend has increased too much since the previous run.

## Quick Start

Run a one-shot check for today:

```bash
python3 skills/token-cost-guard/scripts/token_cost_guard.py --threshold-cny 20
```

Force a source when needed:

```bash
python3 skills/token-cost-guard/scripts/token_cost_guard.py --source hermes --threshold-cny 20
python3 skills/token-cost-guard/scripts/token_cost_guard.py --source openclaw --threshold-cny 20
```

When installed by Hermes and running from the skill directory:

```bash
python3 scripts/token_cost_guard.py --threshold-cny 20
```

Initialize a baseline without alerting:

```bash
python3 skills/token-cost-guard/scripts/token_cost_guard.py --init-only
```

Run every 60 seconds:

```bash
python3 skills/token-cost-guard/scripts/token_cost_guard.py --watch-interval 60 --threshold-cny 20
```

Check the previous hour and stay silent unless the hour exceeds 10 CNY:

```bash
python3 skills/token-cost-guard/scripts/token_cost_guard.py \
  --period previous-hour \
  --alert-mode total \
  --threshold-cny 10 \
  --quiet-ok \
  --alert-exit-zero
```

Send an alert through OpenClaw when the threshold is exceeded:

```bash
python3 skills/token-cost-guard/scripts/token_cost_guard.py \
  --threshold-cny 20 \
  --send-openclaw \
  --channel feishu \
  --target <recipient-or-chat-id>
```

OpenClaw hourly command alert example:

```bash
python3 ~/.openclaw/skills/token-cost-guard/scripts/token_cost_guard.py \
  --source openclaw \
  --period previous-hour \
  --alert-mode total \
  --threshold-cny 10 \
  --quiet-ok \
  --alert-exit-zero \
  --send-openclaw \
  --channel feishu \
  --target <feishu-open-id-or-chat-id>
```

Hermes hourly script alert example:

```bash
~/.hermes/scripts/hermes_hourly_alert.sh
```

## Behavior

- `--source auto` selects Hermes when running under Hermes (`HERMES_*` environment or `~/.hermes/skills` path), otherwise OpenClaw.
- OpenClaw source reads `~/.openclaw/agents/*/sessions/*.jsonl` and prefers native cost fields such as `usage.cost.total`, `usage.costCny`, or `usage.costUsd` before estimating from token prices.
- Hermes source reads `~/.hermes/logs/agent.log*` API-call usage lines and uses Hermes `state.db` session costs (`actual_cost_usd` or `estimated_cost_usd`) when present, allocated across log calls by token share. It falls back to `state.db` session aggregates when logs have no matching records.
- Defaults to today's Asia/Shanghai date.
- Supports `--period day`, `--period current-hour`, and `--period previous-hour`; use `previous-hour` for hourly cron alerts.
- Computes cost by model and by runtime group (`Agents` for OpenClaw, `Hermes Sources` such as `cron`, `weixin`, or `cli` for Hermes).
- Compares current total cost with the previous snapshot in the selected runtime's `token-cost-guard/state.json`.
- Alerts when either condition is true:
  - absolute cost delta is greater than `--threshold-cny`
  - percentage delta is greater than `--threshold-percent`
- With `--alert-mode total`, alerts when the current time window's known cost is greater than `--threshold-cny`; this is the recommended mode for "last hour exceeded budget" cron jobs.
- With `--quiet-ok`, prints nothing when the run is OK; this is useful for Hermes `cron --no-agent --script` delivery.
- With `--alert-exit-zero`, returns exit code 0 even when an alert fires; use it for cron jobs so a successful alert is not marked as a failed run.
- Writes Chinese Markdown reports to the selected runtime's `token-cost-guard/reports/`.

## Hermes Compatibility

The bundled script is stdlib-only and can run under Codex, OpenClaw, Hermes, cron, or a plain shell.

Environment variables:

- `OPENCLAW_STATE_DIR` or `OPENCLAW_HOME`: override the OpenClaw state directory.
- `HERMES_HOME`: override the Hermes home directory; defaults to `~/.hermes`.
- `OPENCLAW_TOKEN_COST_GUARD_STATE_DIR`: override state/report storage.
- `HERMES_STATE_DIR` or `HERMES_DATA_DIR`: when present and source is Hermes, default state/report storage goes under `<that-dir>/token-cost-guard`.
- `OPENCLAW_TOKEN_COST_THRESHOLD_CNY`: default absolute alert threshold.
- `OPENCLAW_TOKEN_COST_THRESHOLD_PERCENT`: default percent alert threshold.
- `TOKEN_COST_GUARD_USD_CNY` or `TOKEN_REPORT_USD_CNY`: USD/CNY conversion for Hermes `state.db` costs and any OpenClaw native USD cost fields.

Hermes tap metadata lives in `skill.json`; ClawHub/OpenClaw marketplace metadata lives in `clawhub.json`.

## Pricing

Cost source priority is: runtime-native billing fields first, then the price table after applying any `--pricing-file` overrides.

The script embeds current DeepSeek official CNY prices per 1M tokens:

- `deepseek-v4-pro`: cache hit 0.025, cache miss 3, output 6
- `deepseek-v4-flash`: cache hit 0.02, cache miss 1, output 2
- `deepseek-chat` and `deepseek-reasoner` are treated as v4-flash compatibility aliases.

Known local CNY estimates are included for Kimi models. Unknown models are listed as unpriced unless OpenClaw or Hermes recorded a usable native cost.

Use `--pricing-file <json>` to override or add prices. JSON shape:

```json
{
  "provider/model-or-model-id": {
    "cache_hit_cny_per_million": 0.02,
    "cache_miss_cny_per_million": 1.0,
    "output_cny_per_million": 2.0
  }
}
```

## Output Contract

When reporting results, include:

- current total known cost
- previous total and delta when available
- alert status and threshold
- top models by cost
- top agents by cost
- unpriced models, if any
