# Live Execution Boundary — references/live-execution-boundary.md

Exactly one module may turn an order plan into venue traffic:
`scripts/live_execution_adapter.py`. This document defines that boundary.

## What may touch real money

| Component | Reads | Writes |
|---|---|---|
| `lighter_rest_client.py` | public + private REST | never |
| strategy scripts (`compute_*`, `size_position`, `risk_checks`, `prepare_order`) | nothing (pure functions) | never |
| `position_monitor.py`, `trailing_stop.py` | account, positions, books | SL re-placement, via the signer, live modes only |
| `live_execution_adapter.py` | — | **the only order-entry path** |
| `lighter_signer.py` | auth token minting | create/cancel/cancel-all/close — called *by* the adapter, halt, and trailing stops |
| `halt.py` | — | cancel-all / flatten, operator-invoked only |

Paper and approval modes perform **zero API writes** — guaranteed by the mode
guard, not by convention.

## The mode guard

```
paper            → simulated fill at the plan price, order_indexes all null
approval         → status "pending_approval", nothing sent
live             → human prompt when execution.require_human_approval_for_live_orders
                   else send the bracket
autonomous_live  → send the bracket (consent was locked at onboarding)
```

Unknown modes are blocked. The adapter also refuses plans that lack wire
integers (`price_int`/`size_int`/triggers) — precision conversion is mandatory,
never improvised at the boundary.

## Trust rules

1. **No script sets consent.** `autonomous_live_consent` flips true only at
   the onboarding keyboard (`ACCEPT`). `validate_config.py` rejects
   `mode=autonomous_live` without it; `resume.py` refuses to switch into it.
2. **Mode downgrades are always safe.** Any human may edit `config.json` to a
   less autonomous mode at any time; the runner picks it up next cycle.
3. **SL/TP requirements can't be disabled live.** `validate_config.py` treats
   `require_stop_loss: false` or `require_take_profit: false` in a live mode
   as an error.
4. **The signer never sees floats.** Wire integers are computed from market
   decimals in `prepare_order.py`; the signer asserts integer inputs.
5. **Secrets never cross the boundary into files or logs.** The signer reads
   env vars itself; callers pass no credentials around; masking shows last 4
   characters only.

## Failure semantics at the boundary

| Failure | Behavior |
|---|---|
| SDK missing | clear `pip install lighter-sdk` message, non-zero exit |
| Entry rejected | no SL/TP sent; result `status: error`; journaled |
| SL or TP rejected after entry filled | bracket result names the failed leg; next monitor cycle reconciles; error counter increments |
| Cancel fails after SL re-place | **both stops live** is reported loudly (never silently dropped) |
| Network failure mid-bracket | cycle error → circuit-breaker counter; next cycle reconciles state vs venue |
