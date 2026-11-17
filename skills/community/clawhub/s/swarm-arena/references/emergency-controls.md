# Emergency Controls — references/emergency-controls.md

## Halt (`scripts/halt.py`)

```bash
python3 scripts/halt.py config.json --reason "market shock"
```

Sets **both** `halt=true` and `circuit_breaker=true` in `state.json`. Every
trading path (`autonomous_runner.py`, `trade_loop.py`) refuses to run while
either flag is set. The event is journaled to `trades.json` as a
`halt_event`.

### Options

| Flag | Effect |
|---|---|
| `--reason TEXT` | recorded in the journal entry |
| `--cancel-orders` | live modes: cancel **all** open orders via the signer |
| `--no-cancel` | never cancel (overrides `execution.cancel_on_halt`) |
| `--flatten` | also market-close every known position (reduce-only IOC) |
| `--confirm-flatten` | required with `--flatten` unless `execution.flatten_on_emergency_stop: true` |

Default cancel behavior follows `execution.cancel_on_halt` (default true) —
in live modes, halting cancels open orders unless you say otherwise.

Flattening is intentionally awkward: positions close at market with no price
protection beyond reduce-only. Use it when open exposure itself is the
emergency.

## Resume (`scripts/resume.py`)

```bash
python3 scripts/resume.py config.json                 # clear flags, keep mode
python3 scripts/resume.py config.json --mode paper    # clear + switch mode
python3 scripts/resume.py config.json --run-now       # clear + run a cycle
```

Clears `halt` and `circuit_breaker`, resets `consecutive_errors`, journals a
`resume_event`.

**Consent guard**: `--mode autonomous_live` is refused unless
`autonomous_live_consent` is already true in the config. Resume can check
consent; it can never create it.

## Circuit breaker (automatic)

- Every unhandled cycle error increments `state.consecutive_errors`.
- At **5** consecutive errors the breaker trips: `circuit_breaker=true`.
- Any clean cycle resets the counter to 0.
- The tripped state persists until a human runs `resume.py`.

## Watchdog cron

The halt-check job (every 15 min) runs `status.py --json` and alerts (exit 1)
when any of these hold:

- `halt` or `circuit_breaker` set
- `consecutive_errors ≥ 3`
- `daily_loss ≥ 80%` of `max_daily_loss`

Wire its output to whatever alerts you — email via cron `MAILTO`, a wrapper
script, or your agent supervisor.

## Manual position control

```bash
# Cancel every open order:
python3 scripts/lighter_signer.py cancel-all
# Close one position (reduce-only market):
python3 scripts/lighter_signer.py close <market_index> <side> <size_int> <price_int>
```

Both require live credentials in the environment.
