# Trade Checklist

Use this checklist before and after every order action.

## Pre-Trade Checks
1. Confirm normalized intent:
- `symbol`
- `side` (`buy` or `sell`)
- `order type` (`limit` or `market`)
- `size` and unit semantics (base amount vs quote notional)

2. Confirm constraints:
- Max acceptable slippage or explicit price bound
- Partial fill allowed or not
- Cancel/expire conditions for non-market orders

3. Confirm docs and tools:
- WhiteBIT docs MCP search completed for relevant endpoint fields
- OpenClaw tools required for execution are present

4. Confirm account state:
- Balance is sufficient with fee buffer
- Symbol is tradable and not paused/restricted

5. Confirm user approval:
- Require an explicit final confirmation containing symbol, side, type, size, and price (for limit)

## Execution Checks
1. Capture exact parameters sent.
2. Capture returned order id/client id.
3. Capture immediate status response.

## Post-Trade Checks
1. Query order status or fills.
2. Report:
- Final status (`filled`, `partially_filled`, `open`, `cancelled`, `rejected`)
- Executed quantity
- Average execution price
- Fees

3. If status is ambiguous:
- Do not place a second market order.
- Reconcile status first, then request user direction.
