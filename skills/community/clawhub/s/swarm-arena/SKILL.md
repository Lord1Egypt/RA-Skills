---
name: swarm-arena
description: >-
  Autonomous 24/7 perpetual-futures trading agent for the Lighter exchange.
  Runs a full indicator/confluence pipeline (5m/1h/4h), risk-based sizing,
  mandatory reduce-only SL/TP brackets, a bounded self-learning loop, and
  cron-driven operation with hard safety rails: daily loss limit, exposure and
  notional caps, halt + circuit breaker, and a one-way human consent gate for
  fully autonomous live trading. Paper mode works stdlib-only with zero order
  writes. Use when the user wants to run, configure, monitor, or operate the
  swarmArena trading agent on Lighter.
---

# swarmArena

**The predator never sleeps.** swarmArena is an autonomous trading agent for
Lighter perpetual futures. It scans markets on a cron cadence, scores long and
short setups independently, demands multi-timeframe confluence, sizes positions
from risk, protects every trade with a reduce-only stop-loss + take-profit
bracket, learns bounded lessons from its own journal, and stops itself when
things go wrong.

- Skill root: `skills/swarm-arena/` (this file's directory)
- Venue: **Lighter** (API base URL is a config value; see `config.example.json`)
- Scripts: `scripts/` — 27 Python 3.10+ tools, each a module AND a CLI
- Deep docs: `documentation-swarm-arena.md` and `references/*.md`

## Core rules (non-negotiable)

1. **Safety rails beat signals.** Every order passes `risk_checks.py` hard
   gates: daily loss limit, total exposure cap, per-trade notional cap,
   available margin, zero-notional guard, halt, circuit breaker.
2. **Every trade carries a bracket.** Entry MARKET (IOC) + STOP_LOSS
   (reduce-only, trigger price) + TAKE_PROFIT (reduce-only, trigger price).
   `require_stop_loss` / `require_take_profit` cannot be disabled in live modes.
3. **Leverage is client-side only.** Lighter has no leverage endpoint and no
   per-position margin mode. "Leverage" here is a sizing cap
   (`effective_leverage = notional / margin`); nothing is sent to the exchange.
4. **Credentials live in the environment only.** `LIGHTER_API_PRIVATE_KEY`,
   `LIGHTER_API_KEY_INDEX`, `LIGHTER_ACCOUNT_INDEX`, `LIGHTER_L1_ADDRESS`.
   Never written to files; logs mask all but the last 4 characters.
5. **Everything is journaled.** Every cycle decision — including `wait` and
   `blocked` — is appended to `trades.json`.
6. **Learning is bounded.** The review loop can only tighten risk
   (lower confidence multiplier, lower leverage cap, higher threshold). It can
   never loosen beyond config bounds, change modes, remove SL/TP, or stop the
   journal.
7. **Consent is one-way and human-only.** `autonomous_live_consent` becomes
   true only when a human types `ACCEPT` in `onboarding.py`. No script, agent,
   or API call may set it.
8. **Gateway-first (default).** With `gateway.enabled` (the shipped default),
   ALL exchange traffic flows through the swarm-arena-backend: REST reads via
   its `/gw/rest`, and SDK writes (nonce/auth/sendTx) because the signer is
   initialized with the backend URL so its `/api/v1/*` calls are proxied
   verbatim and journaled server-side (`orders.jsonl`). `gateway.required=true`
   fails the cycle when the backend is down (counted by the circuit breaker);
   `false` warns and falls back to direct venue access. The exchange private
   key NEVER leaves this host — signing stays local.

## Modes

| Mode | Real orders | Per-trade approval | Use for |
|---|---|---|---|
| `paper` | no | n/a | Full pipeline simulation on real market data, zero API writes. Default. |
| `approval` | no | yes | Emits `PENDING_APPROVAL` proposals for human/agent review. |
| `live` | yes | gated by `execution.require_human_approval_for_live_orders` | Supervised real trading. |
| `autonomous_live` | yes | none | 24/7 unattended. Requires the onboarding consent latch. |

## Workflow (per cron cycle)

```
autonomous_runner.py config.json
  ├─ validate_config.py            # invalid config -> error counter, no trading
  ├─ halt / circuit_breaker?       # either set -> exit quietly
  ├─ daily reset                   # daily_loss/daily_pnl zero on UTC day change
  ├─ position_monitor.py           # detect closes, realized PnL, journal, cooldown
  ├─ trade_loop.py per symbol      # cooldown -> duplicate guard -> scan ->
  │                                #   learning-adjusted gate -> risk -> execute -> journal
  │   └─ market_scan_from_lighter.py
  │        candles 5m/1h/4h + book + funding + account   (via gateway when enabled)
  │        -> compute_features -> compute_signal -> ATR bracket
  │        -> compute_confluence -> recommend_leverage -> size_position
  │        -> precision -> min-notional -> liquidity -> proposal | wait
  ├─ live_execution_adapter.py     # SDK signs locally; delivery via the backend
  │                                # gateway proxy (gateway mode) or direct sendTx
  ├─ trailing_stop.py              # breakeven at +0.5%, ATR x1.5 trail, never against
  ├─ persist state.json atomically
  └─ every 5 new closed trades     # fetch_trade_outcomes + review_trades + update_metrics
```

Traffic shape (gateway mode, the default):

```
skill scripts ──HTTP──> swarm-arena-backend ──HTTPS──> Lighter API
   reads: POST /gw/rest (agent token)          forwarded verbatim
   writes: SDK /api/v1/* (signer url = backend) proxied verbatim, sendTx journaled
dashboard  ──HTTP──> backend /api/state|trades|orders|performance|pnl (local files)
```

## Onboarding requirements

1. `bash install.sh` — Python ≥ 3.10, scripts compile, config validates,
   credentials visible (warn-only in paper), `lighter-sdk` for live modes.
2. `python3 scripts/onboarding.py` — env-first credentials, **live
   verification** (auth token + account read; failure is fatal), risk
   parameters, consent gate, writes `config.json` (0600), registers crons,
   optional first cycle.
3. Credentials exported in the environment of whatever runs the cron jobs
   (systemd `EnvironmentFile`, launchd wrapper, or shell profile). The SDK is
   required only when real orders are placed.

## Connecting an agent & starting to trade (checklist)

What an agent (or operator) needs before the first live cycle:

| Requirement | Where it comes from |
|---|---|
| `LIGHTER_API_PRIVATE_KEY` | Lighter UI → API keys (index 2–254) |
| `LIGHTER_API_KEY_INDEX` | same |
| `LIGHTER_ACCOUNT_INDEX` | Lighter UI, or discover via `accountsByL1Address` from `LIGHTER_L1_ADDRESS` |
| `MANTIS_AGENT_TOKEN` | shared secret you create; **must be identical** in the agent's env and the backend's env |
| Backend running | `backend/swarm-arena-backend` (gateway + dashboard + order journal) |
| `MANTIS_VIEWER_PASSWORD` (optional) | when set, the dashboard + read API require it (HTTP Basic); unset → loopback-open with a startup warning |
| `lighter-sdk` | `pip install lighter-sdk` — only for live/autonomous_live |
| Consent | type `ACCEPT` at the onboarding gate for `autonomous_live` |

Sequence: `install.sh` → export the env vars above → run the backend →
`onboarding.py` → cron registered → first cycle runs → watch
`http://127.0.0.1:8080/dashboard.html`.

## Signal model (summary — see references/strategy-framework.md)

Long and short scored independently from features on 5m (timing), 1h (signal),
4h (trend): EMA20/50/12/26, RSI14, ATR14, MACD(12,26,9), volume ratio,
trend, momentum, volatility flag, funding passthrough.

| Component | Weight | Long fires when | Short fires when |
|---|---|---|---|
| 4h trend | 2.0 | trend up | trend down |
| 1h trend | 2.0 | trend up | trend down |
| RSI zone (1h) | 1.5 | 45–68 | 32–55 |
| MACD cross (1h) | 1.0 | line > signal | line < signal |
| 5m timing | 0.5 | trend up or price > EMA20 | trend down or price < EMA20 |
| Volume (1h) | 1.0 | ratio ≥ 0.8 | ratio ≥ 0.8 |
| EMA20 position (1h) | 1.0 | price above | price below |
| Funding bias | 0.5 | funding < 0 | funding > 0 |

`confidence = score / 9.5`. Enter at ≥ **0.55** (raised to **0.70** under high
volatility). Otherwise `wait`. Ties resolve to `wait`.

## Confluence model (summary — see references/confluence-model.md)

Nine binary checks; `confidence = passed / 9`; entry needs ≥ 0.55 (0.70 high
volatility): trend_alignment, momentum_confirmation, volume_confirmation
(≥ 0.75), rsi_zone (long 40–70 / short 30–60), macd_alignment, reward_risk_ok
(≥ `min_reward_risk`), exposure_capacity_ok (< 90% of cap after the trade),
position_capacity_ok, timeframe_confluence (5m agrees).

Bracket from ATR: **SL = entry ∓ 1.5×ATR**, **TP = entry ± 2.5×ATR** (natural
R:R ≈ 1.67). Sizing: `risk_usd = equity × risk_pct`, `notional = risk_usd /
stop_distance_pct` (capped at `max_notional_per_trade`), `margin = notional /
leverage`, quantity rounded down to market precision, suppressed below the
market's minimum quote/base amounts.

## Learning loop (summary — see references/review-and-learning.md)

Every 30 minutes (review cron) or every 5 newly closed trades: resolve
outcomes → review (win rate, avg/total PnL, streaks, per-symbol, per-regime,
lesson tags) → bounded adaptations to `state.metrics`:

- `confidence_multiplier` — floor 0.70, recovers +0.05/review toward 1.0
- `effective_leverage_cap` — can only drop and recover; never above `max_leverage`
- `recommended_min_confidence` — 0.55 base, up to 0.75 cap after losing streaks
- `underperforming_symbols` — informational list (per-symbol PnL ≤ −$100)

Learning can never: raise leverage above `max_leverage`, switch to a riskier
mode, remove SL/TP requirements, or suppress journaling.

## Hard safety rules

| Rule | Enforcement |
|---|---|
| Daily loss limit | `risk_checks.py` blocks new entries at `max_daily_loss`; reset at UTC midnight |
| Total exposure cap | block above `max_total_exposure`; confluence demands < 90% |
| Per-trade notional | scale-down to, then block above, `max_notional_per_trade` |
| Leverage ceiling | client-side max; learning can only lower it |
| Mandatory SL/TP | bracket on every trade; SL/TP always `reduce_only` |
| Halt blocks all | `halt=true` stops every trading path |
| Circuit breaker blocks all | trips at 5 consecutive errors; any clean cycle resets the counter |
| Bounded learning | see above; no silent risk expansion anywhere |
| Consent one-way | only onboarding's typed `ACCEPT` can set `autonomous_live_consent` |
| Credentials env-only | masked to last 4 chars in all output |

## Emergency controls

```bash
# Stop everything (sets halt + circuit_breaker, journals halt_event):
python3 scripts/halt.py config.json --reason "market shock"
# Also cancel every open order (live modes):
python3 scripts/halt.py config.json --cancel-orders
# Also flatten all positions (requires the config flag or explicit confirm):
python3 scripts/halt.py config.json --flatten --confirm-flatten
# Resume (consent guard: autonomous_live only with existing consent):
python3 scripts/resume.py config.json --mode paper
python3 scripts/resume.py config.json --run-now
```

## Cron jobs (see references/cron-automation.md)

`register_crons.py` renders `cron-templates.json` into ready-to-paste lines:

| Job | Cadence | Command |
|---|---|---|
| scan | every 2 min (paper: 5 min) | `autonomous_runner.py config.json` |
| review | every 30 min | `fetch_trade_outcomes.py` + `review_trades.py` + `update_metrics.py` |
| daily summary | 00:00 UTC | `status.py` + 24h `review_trades.py` digest |
| halt check | every 15 min | `status.py --json`, alert on halt / CB / ≥3 errors / ≥80% daily loss |

systemd (`deploy.systemd.service` + `.timer`) and launchd
(`deploy.launchd.plist`) equivalents ship alongside; log rotation via
`logrotate.swarm-arena.conf` / `newsyslog.swarm-arena.conf`.

## Status

```bash
python3 scripts/status.py config.json           # human view
python3 scripts/status.py config.json --json    # machine view (watchdog uses this)
```

Shows mode, halt/CB flags, error counter, daily loss vs limit, equity,
available margin, daily PnL, open positions, trade stats (total / executed /
closed / win rate / total PnL), adaptive metrics, lessons, and a config
summary.

## Arena (multi-model competition)

Multiple LLMs trade the same market in parallel, each with its own account,
seeded with `arena.start_equity` USD. Every model gets the same market
context and answers with one JSON decision; garbage output degrades to a hold,
never a crash.

**Fastest start — `bot.py` (ready-to-run loop).** Endpoint and models live in
`config.json`:

```json
"arena": {
  "endpoint": "https://api.openai.com",
  "api_key_env": "OPENAI_API_KEY",
  "start_equity": 10000,
  "models": [{"id": "alpha", "model": "gpt-5"},
             {"id": "beta", "model": "deepseek-chat"}]
}
```

```bash
export OPENAI_API_KEY="..."
python3 scripts/bot.py --config config.json          # loop, Ctrl-C to stop
python3 scripts/bot.py --config config.json --once   # smoke run: one cycle
```

`endpoint` is any OpenAI-compatible base URL (OpenAI, xAI, DeepSeek, Qwen
compatible mode, local proxies). Model entries only need `id` + `model` —
they inherit `endpoint` and `api_key_env`; override per model with
`base_url` / `api_key_env` / `provider` (`anthropic`|`openai`|`gemini`|
`xai`|`deepseek`|`qwen`) to mix providers. Keys NEVER live in the file.
`--interval-min` sets cadence (default 5). CLI flags (`--models`,
`--endpoint`) remain as one-off overrides that rewrite the block.

The prompt every model receives is documented verbatim in
`references/arena-prompt.md` (source of truth: `prompt_builder.py`).

Manual config instead (`config.json` → `arena` block, see `config.example.json`):

```json
"arena": {
  "start_equity": 10000,
  "models": [
    {"id": "claude", "provider": "anthropic", "model": "claude-sonnet-5",
     "api_key_env": "ANTHROPIC_API_KEY"}
  ]
}
```

- Providers: `anthropic`, `openai`, `gemini`, `xai`, `deepseek`, `qwen`.
  API keys come from the env var named by `api_key_env` — never from files.
  Optional per-model venue credentials via an `env` mapping
  (`{"LIGHTER_ACCOUNT_INDEX": "LIGHTER_ACCOUNT_INDEX_CLAUDE"}`).
- Run all models in parallel: `python3 scripts/arena_runner.py config.json`
  (schedule every 5 min for continuous play). One model only:
  `python3 scripts/model_runner.py config.json --model claude`.
- Per-model files beside the config: `state.<id>.json`, `trades.<id>.json`,
  each with its own file lock and circuit breaker. The main `state.json`
  halt / circuit-breaker stops ALL models.
- Journal entries gain `model`, `llm_reasoning`, `exit_plan`.
- Backend board API: `/api/arena/models`, `/leaderboard`, `/equity`,
  `/conversations`, `/trades`, `/positions`, `/prices`; the frontend board is
  `frontend/arena.html`.

Scripts: `bot.py` (ready-to-run loop: models + endpoint -> trading),
`decision_parser.py` (robust JSON extraction → validated decision),
`prompt_builder.py` (identical system prompt + context for every model),
`llm_client.py` (stdlib-only multi-provider chat), `model_runner.py` (one
model cycle), `arena_runner.py` (parallel orchestrator).

## Data files

- `config.json` — the annotated schema in `config.example.json`; validate with
  `validate_config.py`. State/trades paths default to beside the config.
- `state.json` — `halt`, `circuit_breaker`, `consecutive_errors`,
  `daily_loss`, `daily_loss_date`, `last_run`, `account {equity,
  available_margin, daily_pnl}`, `known_open_positions {SYM: {side, quantity,
  entry_price, leverage, stop_loss, take_profit, opened_at, order_indexes
  {entry, sl, tp}}}`, `last_close_ts {SYM: ts}`, `metrics {win_rate, avg_pnl,
  total_pnl, confidence_multiplier, effective_leverage_cap,
  recommended_min_confidence, leverage_reduction_active,
  underperforming_symbols, lessons[]}`.
- `trades.json` — append-only journal array. Entry fields: `ts`, `symbol`,
  `mode`, `decision`, `signal`, `signal_reason`, `confidence`,
  `adjusted_confidence`, `regime`, `confluence {passed, failed, count, total,
  confidence}`, `order {entry_price, stop_loss, take_profit, leverage,
  quantity, notional, side}`, `exec_result`, `status`, `market {last_price,
  mark_price, funding_rate}`, `features_1h {...}`, `outcome`, `realised_pnl`,
  `close_reason`, `closed_at`, `lesson_tags[]`, plus arena fields `model`,
  `llm_reasoning`, `exit_plan`.
- `state.<id>.json` / `trades.<id>.json` — per-model arena accounts and
  journals (same shapes as `state.json` / `trades.json`).

Examples for all three ship as `*.example.json` next to this file.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Cycle exits with code 3 | halt or circuit breaker active | inspect `state.json`; fix the cause; `resume.py` |
| `circuit_breaker=true` after errors | 5 consecutive cycle errors | read `state.last_error.message`; fix; `resume.py` |
| "missing environment variables" | creds not exported in the cron environment | export them, or use systemd `EnvironmentFile` |
| "the 'lighter' SDK is not installed" | live mode without lighter-sdk | `pip install -r requirements.txt` |
| Every signal is `wait` | threshold/RSI zones legitimately unmet, learning raised the bar, or the market is newly listed (`insufficient market data: need at least 30 candles`) | check `metrics.recommended_min_confidence`; read the `signal_reason` in `trades.json`; thin-history markets trade once enough bars exist |
| `sizing suppressed` | notional below market minimum quote amount | raise `base_value_per_trade`/`risk_pct`, or accept skips |
| `risk checks failed: daily_loss_limit` | daily loss cap hit | wait for UTC reset or raise the cap deliberately |
| `unknown symbol 'XYZ'` | symbol not in Lighter's market list | `python3 scripts/lighter_rest_client.py market ETH` to inspect known markets |
| auth errors on private reads | expired/invalid API key index | re-mint token; verify key index 2–254 in the Lighter UI |
| Cron never runs | crontab not installed | `python3 scripts/register_crons.py` and paste its output into `crontab -e` |
| Config rejected | failed validation | `python3 scripts/validate_config.py config.json` lists every error |
| Positions stuck open in paper | price never touched SL/TP | expected; monitor marks closes only on level touches |

## Reference index (`references/`)

| File | Topic |
|---|---|
| `onboarding.md` | Setup wizard, verification, consent gate |
| `strategy-framework.md` | Features, weights, thresholds, regimes |
| `confluence-model.md` | The 9 checks and entry math |
| `leverage-policy.md` | Client-side leverage, learning caps |
| `risk-policy.md` | Hard gates, sizing math, kill rules |
| `execution-playbook.md` | Bracket placement, precision, liquidity |
| `live-execution-boundary.md` | What may/may not touch real money |
| `review-and-learning.md` | Outcomes, stats, bounded adaptations |
| `emergency-controls.md` | Halt, resume, flatten, watchdog |
| `cron-automation.md` | Schedules, systemd/launchd, logs |
| `lighter-integration.md` | Lighter REST/SDK facts + assumptions |
| `deployment.md` | Install, hardening, upgrades |
