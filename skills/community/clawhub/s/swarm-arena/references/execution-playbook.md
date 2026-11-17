# Execution Playbook — references/execution-playbook.md

How a proposal becomes a protected position on Lighter.

## The bracket

Every trade is three orders (`lighter_signer.place_bracket`):

| Leg | SDK order type | Time in force | Flags |
|---|---|---|---|
| Entry | `ORDER_TYPE_MARKET` | `IMMEDIATE_OR_CANCEL`, `DEFAULT_IOC_EXPIRY` | `reduce_only=False` |
| Stop-loss | `ORDER_TYPE_STOP_LOSS` | — | `trigger_price` set, `reduce_only=True`, 28-day expiry |
| Take-profit | `ORDER_TYPE_TAKE_PROFIT` | — | `trigger_price` set, `reduce_only=True`, 28-day expiry |

`reduce_only=True` on both exits means a trigger can only shrink the position,
never flip it. The entry is market/IOC so it fills now or not at all; there is
no resting entry order to forget about.

If any bracket leg fails, the execution result reports which legs succeeded —
`position_monitor.py` reconciles on the next cycle either way. Partial-bracket
failures are logged loudly (a position without its stop is the worst state in
the system).

## Precision (`prepare_order.py` + `lighter_rest_client.py`)

Lighter transmits prices and sizes as **integers** scaled by the market's
decimals from `orderBookDetails` (cached 1 hour):

```
price_int = round(price × 10^price_decimals)     # $3100.00 @ 2 dp → 310000
size_int  = round(size  × 10^size_decimals)      # 0.0010 ETH @ 4 dp → 10
```

Quantities are rounded **down** to the size step (never buy more than sized).
Bracket sanity is validated before anything is sent: long requires
`SL < entry < TP`; short mirrors it.

## Liquidity check

Before entering, `market_scan_from_lighter.py` inspects the order book:

1. Both sides non-empty, book not crossed.
2. Best bid/ask spread < **1%** of mid.
3. Depth within **±0.5%** of mid covers **3×** the proposed notional.

Failure → `wait` decision, journaled with the reason.

## Position lifecycle

1. **Open** — entry fill recorded in `state.known_open_positions[symbol]` with
   side, quantity, entry price, leverage, SL/TP levels, and the three order
   indexes.
2. **Manage** — `trailing_stop.py` (breakeven at +0.5%, ATR×1.5 trail, never
   against the position; live modes re-place the SL order *before* canceling
   the old one).
3. **Close** — `position_monitor.py` detects flat positions each cycle
   (paper: price touched SL/TP; live: position gone from the account read),
   derives realized PnL (live: from account trades matched against the
   journaled entry; fallback: price delta), journals outcome + close reason,
   feeds `daily_loss`, sets the cooldown timestamp.

`minimum_hold_sec` (default 60) keeps the manager from acting on fills that
may not have settled into the account read yet.

## Close reasons

`stop_loss` · `take_profit` · `trailing_stop` · `manual_or_external` ·
(`liquidation` is reported by the venue; the bracket is designed to fire long
before it).

## Approval flow

- `approval` mode: `approval_runner.py` emits a `PENDING_APPROVAL` proposal
  (journaled) and executes nothing.
- `live` mode with `execution.require_human_approval_for_live_orders: true`:
  the adapter prints the full order summary and waits for `y` on a TTY;
  anything else rejects the order (journaled `rejected_by_operator`).
- `autonomous_live`: no gate — consent was locked at onboarding.
