# swarmArena — Full Documentation

This is the operator's manual for swarmArena, an autonomous 24/7
perpetual-futures trading agent for **Lighter**, packaged as an agent skill.
Read `SKILL.md` first for the behavior contract; this document goes deeper.
Focused deep-dives live in `references/`.

> Nothing here is financial advice. swarmArena is software; markets are
> hostile. Start in `paper` mode. See the FAQ before funding anything.

---

## 1. Architecture

```
                         cron / systemd / launchd
                                  │
                    scripts/autonomous_runner.py          ← the only scheduler entry
                                  │
        ┌─────────────────────────┼──────────────────────────┐
        │                         │                          │
  validate_config        position_monitor              trade_loop (per symbol)
        │                         │                          │
   halt / CB guard        venue reconcile                market_scan_from_lighter
   daily reset            realized PnL + journal         ├─ lighter_rest_client (reads)
        │                         │                      ├─ compute_features ×3 TF
        │                         │                      ├─ compute_signal
        │                         │                      ├─ compute_confluence
        │                         │                      ├─ recommend_leverage (client-side)
        │                         │                      ├─ size_position
        │                         │                      └─ prepare_order (precision/wire ints)
        │                         │                          │
        │                         │                   risk_checks (hard gates)
        │                         │                          │
        │                         │                   live_execution_adapter (mode guard)
        │                         │                          │
        │                         │                   lighter_signer (SDK writes, live only)
        │                         │                          │
        │                         └──────────────────► journal_trade (trades.json)
        │                                                    │
        └────────────────────── state.json ◄─────────────────┘
                                  │
                trailing_stop → review_trades → update_metrics (bounded learning)
```

Design rules that hold everywhere:

- **One writer per file, atomic rewrites.** `state.json` and `trades.json` are
  written via temp-file + `os.replace`.
- **Everything is a dict.** Scripts take and return plain JSON-able dicts so
  they work as modules and as CLIs (`... | python3 scripts/compute_signal.py`).
- **Paths derive from the config location.** `state.json` and `trades.json`
  live beside `config.json` unless `--state` / `--trades` say otherwise. No
  absolute paths are hardcoded anywhere.
- **Paper mode is stdlib-only.** Only `lighter_signer.py` imports the
  third-party SDK, lazily, with a clear install hint.
- **Credentials are environment-only** and masked to their last 4 characters
  in any output.

## 2. Configuration reference

`config.example.json` ships fully annotated (annotation keys start with `_`
and are ignored). Copy to `config.json` and edit; validate with
`python3 scripts/validate_config.py config.json`.

| Key | Type | Default | Meaning |
|---|---|---|---|
| `mode` | string | `paper` | `paper` \| `approval` \| `live` \| `autonomous_live` |
| `autonomous_live_consent` | bool | `false` | One-way latch; set only by typing `ACCEPT` in onboarding |
| `base_url` | string | *(value in example file)* | Lighter API base URL; env `LIGHTER_BASE_URL` overrides |
| `allowed_symbols` | list | `["ETH","BTC","SOL"]` | Lighter perp symbols; mapped to `market_id` at runtime |
| `base_value_per_trade` | number | `100` | Reference USD trade size (display/context) |
| `risk_pct_per_trade` | number | `0.01` | Fraction of equity risked per trade |
| `min_leverage` | int | `2` | Lowest client-side leverage cap |
| `max_leverage` | int | `10` | Absolute client-side leverage ceiling |
| `max_notional_per_trade` | number | `500` | Hard USD cap per order (scale-down then block) |
| `max_total_exposure` | number | `2000` | Hard USD cap on summed open notional |
| `max_concurrent_positions` | int | `3` | Max simultaneous positions (one per symbol) |
| `max_daily_loss` | number | `100` | USD; new entries blocked once reached; UTC reset |
| `allow_short` | bool | `true` | When false, short signals are journaled as blocked |
| `require_stop_loss` | bool | `true` | Hard rule; cannot be false in live modes |
| `require_take_profit` | bool | `true` | Hard rule; cannot be false in live modes |
| `min_reward_risk` | number | `1.5` | Minimum R:R for a valid setup |
| `cooldown_after_close_sec` | number | `120` | Per-symbol pause after a close |
| `minimum_hold_sec` | number | `60` | Young positions are not trailed/managed |
| `cron.enabled` | bool | `true` | Global switch for scheduled operation |
| `cron.scan_interval_minutes` | int | `2` | Runner cadence (paper suggestion: 5) |
| `cron.review_interval_minutes` | int | `30` | Learning-loop cadence |
| `cron.daily_summary_hour` | int | `0` | UTC hour of the daily digest |
| `sentiment.enabled` / `weight` | bool/number | `false` / `0.1` | Reserved external-sentiment hook |
| `execution.cancel_on_halt` | bool | `true` | `halt.py` cancels open orders by default |
| `execution.flatten_on_emergency_stop` | bool | `false` | Allow `halt.py --flatten` without extra confirm |
| `execution.require_human_approval_for_live_orders` | bool | `false` | In `live`, prompt before each real order |
| `arena.start_equity` | number | `10000` | USD seed for each arena model's account |
| `arena.models[]` | list | — | `{id, provider, model, api_key_env, base_url?, max_tokens?, env?}` |

### Environment variables

| Variable | Required | Purpose |
|---|---|---|
| `LIGHTER_API_PRIVATE_KEY` | live modes | API key private key from the Lighter UI |
| `LIGHTER_API_KEY_INDEX` | live modes | integer, 2–254 |
| `LIGHTER_ACCOUNT_INDEX` | live modes | account index (discoverable from L1 address) |
| `LIGHTER_L1_ADDRESS` | optional | used by onboarding for account discovery |
| `LIGHTER_BASE_URL` | optional | overrides `config.base_url` |
| per-model `api_key_env` (e.g. `ANTHROPIC_API_KEY`) | arena | LLM provider key for that model |
| per-model venue vars (e.g. `LIGHTER_ACCOUNT_INDEX_CLAUDE`) | arena, optional | per-model venue credentials via the model's `env` mapping |

## 2a. Arena pipeline (multi-model competition)

```
                 bot.py (loop)  atau  cron (every ~5 min)
                        │
              scripts/arena_runner.py          ← parallel orchestrator
                        │  ThreadPoolExecutor, one thread per model
        ┌───────────────┼───────────────┐
  model_runner (id=A)  model_runner (id=B)  …  ← never raises; one model's
        │                                     failure never touches others
  filelock on state.<id>.json
        │
  position_monitor (per-model closes, per-model journal)
        │
  features per symbol (5m/1h/4h via lighter_rest_client)
        │
  prompt_builder ──► llm_client (provider API) ──► decision_parser
        │                                              │ garbage → hold
        │                              ┌───────────────┼──────────────┐
        │                          open_long/short     close          hold
        │                              │               │              │
        │                     ATR fallback bracket   signer close   journaled
        │                     size from size_usd     (live) / mark- with
        │                     risk_checks ──► execute to-market     reasoning
        │                              │     (paper)
        └──────────── state.<id>.json ◄┘
                      trades.<id>.json (model, llm_reasoning, exit_plan)
```

Fairness rules: every model receives the **same system prompt** and the same
computed market context; only account numbers differ. Every decision —
including holds and parse failures — is journaled with the model id, its
reasoning, and its exit plan, which is what the public board renders.

The backend serves `/api/arena/models|leaderboard|equity|conversations|
trades|positions|prices`; per-model equity is snapshotted to
`data/balance_arena.jsonl` (throttled to one point per model per minute) for
the equity curves and the Sharpe figures on the leaderboard. The frontend
board is `frontend/arena.html` (5 s polling, no build step).

Scheduling: `bot.py` runs the loop in-process (`--models`, `--endpoint`,
`--interval-min`), or add a cron line alongside the existing ones, e.g.
`*/5 * * * * cd <skill> && /usr/bin/python3 scripts/arena_runner.py config.json >> logs/arena.log 2>&1`.
The prompt contract is documented in `references/arena-prompt.md`.

## 3. Pipeline deep-dives

Each subsection maps to a reference doc with full math and examples.

| Stage | Script | Reference |
|---|---|---|
| Feature engineering | `compute_features.py` | `references/strategy-framework.md` |
| Signal scoring | `compute_signal.py` | `references/strategy-framework.md` |
| Confluence gating | `compute_confluence.py` | `references/confluence-model.md` |
| Leverage recommendation | `recommend_leverage.py` | `references/leverage-policy.md` |
| Position sizing | `size_position.py` | `references/risk-policy.md` |
| Hard risk gates | `risk_checks.py` | `references/risk-policy.md` |
| Order preparation | `prepare_order.py` | `references/execution-playbook.md` |
| Execution boundary | `live_execution_adapter.py` | `references/live-execution-boundary.md` |
| Signing / writes | `lighter_signer.py` | `references/lighter-integration.md` |
| Position lifecycle | `position_monitor.py`, `trailing_stop.py` | `references/execution-playbook.md` |
| Learning loop | `fetch_trade_outcomes.py`, `review_trades.py`, `update_metrics.py` | `references/review-and-learning.md` |
| Emergency control | `halt.py`, `resume.py` | `references/emergency-controls.md` |
| Scheduling | `register_crons.py`, deploy files | `references/cron-automation.md` |
| Setup | `onboarding.py`, `install.sh` | `references/onboarding.md`, `references/deployment.md` |
| Arena | `bot.py`, `decision_parser.py`, `prompt_builder.py`, `llm_client.py`, `model_runner.py`, `arena_runner.py` | section 2a above, `references/arena-prompt.md` |

## 4. Lighter API integration (verified 2026-09)

- **REST client**: `scripts/lighter_rest_client.py`, stdlib `urllib` only.
  Retries 429/5xx with exponential backoff (≤ 3 attempts), honoring
  `Retry-After`. CLI subcommands: `market`, `candles`, `book`, `funding`,
  `account`, `positions`, `trades`, `pnl`, `discover`.
- **Wire precision**: order prices/sizes are integers scaled by the market's
  `price_decimals` / `size_decimals` from `orderBookDetails` (cached 1 hour).
  Helpers: `to_int_price`, `to_int_size`, `from_int_price`, `from_int_size`,
  `floor_to_step`.
- **Signing**: `scripts/lighter_signer.py` wraps the official SDK
  (`pip install lighter-sdk`): auth token minting, entry MARKET/IOC orders,
  STOP_LOSS / TAKE_PROFIT with `trigger_price` + `reduce_only=True`, cancel,
  cancel-all, `place_bracket()`, `close_position()` — all synchronous via
  `asyncio.run()` wrappers.
- **Key differences from Binance-style venues**: no leverage endpoint (leverage
  is a client-side sizing cap), account-level cross margin (exposure caps are
  client-side + mandatory reduce-only brackets), realized PnL derived from
  account trades (no income endpoint), symbol → `market_id` mapping resolved
  dynamically.

Full endpoint table, verified response shapes, and recorded assumptions:
`references/lighter-integration.md`.

## 5. Operational runbook

### Daily

1. `python3 scripts/status.py config.json` — expect `health=OK`, errors=0.
2. Skim `logs/scan.log` tail for cycle errors.
3. Check daily loss vs limit and open positions in the status output.

### Weekly

1. `python3 scripts/review_trades.py config.json` — win rate, streaks, lessons.
2. Review `state.metrics` adaptations; confirm learning stayed within bounds.
3. Rotate/archive `trades.json` if large (keep it append-only per epoch).
4. Rotate credentials if your policy requires it (Lighter UI → new API key
   index → update env → `resume.py`).

### After any config change

```
python3 scripts/validate_config.py config.json && python3 scripts/status.py config.json --json
```

### Upgrading the skill

1. Halt: `python3 scripts/halt.py config.json --reason "upgrade"`.
2. Replace skill files (keep `config.json`, `state.json`, `trades.json`, `logs/`).
3. `bash install.sh` → must pass.
4. Resume: `python3 scripts/resume.py config.json`.

### Incident response

Anything feels wrong → `python3 scripts/halt.py config.json --cancel-orders`.
Then inspect: `status.py`, `logs/`, `trades.json` tail. Resume only after the
cause is understood. `halt.py --flatten` exists for emergencies where open
exposure itself is the problem.

## 6. FAQ

**Does swarmArena guarantee profit?**
No. It is a rules-based agent with strict risk limits. It can and will lose
money; the safety rails bound *how much* per day, per trade, and in total.

**Which venue does it trade on?**
Lighter perpetual futures. The API base URL is a config value (see
`config.example.json`); everything else in the system just says "Lighter".

**Do I need to install anything for paper mode?**
No. Paper mode is pure Python standard library.

**What does "leverage" mean here if the venue has no leverage endpoint?**
A client-side sizing cap: `margin = notional / leverage`. It bounds how much
margin a trade may consume. Nothing is sent to the exchange.

**Can the learning loop make the agent riskier over time?**
No. Adaptations are one-directional toward safety within hard bounds: lower
confidence multiplier (floor 0.70), lower leverage cap (never above
`max_leverage`), higher entry threshold (cap 0.75). It recovers toward neutral
only after profitable reviews.

**How do I stop it instantly?**
`python3 scripts/halt.py config.json --cancel-orders`. This sets `halt` and
`circuit_breaker`, journals the event, and (in live modes) cancels all open
orders.

**Can a script or agent enable autonomous_live?**
No. `autonomous_live_consent` becomes true only when a human types `ACCEPT` at
the onboarding prompt. Every other code path treats it as read-only, and
`resume.py` refuses to switch into `autonomous_live` without it.

**What happens if the venue API is down?**
REST calls retry with backoff; persistent failures count as cycle errors. Five
consecutive errors trip the circuit breaker and trading stops until a human
resumes.

**Where are my credentials stored?**
Nowhere on disk by this skill. They come from environment variables at
runtime and are masked to the last 4 characters in any output.

**Does it support spot markets?**
No. The pipeline filters for Lighter perpetual markets.

**Can I trade symbols beyond ETH/BTC/SOL?**
Yes — add them to `allowed_symbols`. The symbol must exist in Lighter's market
list and pass precision/minimum checks.
