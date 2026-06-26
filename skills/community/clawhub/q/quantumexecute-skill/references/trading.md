# Trading Reference

## Scope

- Market discovery and API binding checks
- Order create/update/cancel
- Order detail and fills query
- Paired-order execution flow
- Optional completion notification (OpenClaw-oriented)

## Routing

- "List exchange APIs" -> `list_exchange_apis.py`
- "Get market quote" -> `get_market_data.py`
- "Create order" -> `create_master_order.py`
- "Create paired order" -> `create_paired_order.py`
- "Update order" -> `update_master_order.py`
- "Cancel order" -> `cancel_master_order.py`
- "List orders" -> `get_master_orders.py`
- "Get order detail" -> `get_master_order_detail.py`
- "Get fills" -> `get_order_fills.py`

## Mandatory Pre-Check Before Any Order Write (P0)

```bash
python3 scripts/get_market_data.py --symbol <symbol> --type ticker
python3 scripts/list_exchange_apis.py --exchange <exchange> --page 1 --page-size 20
```

## Create Order Parameter Reference

Use `create_master_order.py` for single-order creation. The SDK field names below follow the QuantumExecute Python connector README; the CLI flag column shows the local script parameter to pass.

| CLI flag | SDK field | Required | Type / values | Notes |
| --- | --- | --- | --- | --- |
| `--strategy-type` | `strategyType` | Yes | `TWAP-1`, `POV` | `TWAP_1` is normalized to `TWAP-1` by the local script. |
| `--algorithm` | `algorithm` | Yes | `TWAP`, `VWAP`, `POV` | Execution algorithm. Keep aligned with `strategyType`. |
| `--exchange` | `exchange` | Yes | `Binance`, `OKX`, `LTP`, `Deribit`, `Hyperliquid` | Exchange name. |
| `--symbol` | `symbol` | Yes | string | Trading pair, e.g. `BTCUSDT`. |
| `--market-type` | `marketType` | Yes | `SPOT`, `PERP`, `FUTURES` | Local help says `SPOT` or `PERP`; reference also allows `FUTURES`. |
| `--side` | `side` | Yes | `buy`, `sell` | Order side. |
| `--api-key-id` | `apiKeyId` | Yes | string | Exchange API binding ID from `list_exchange_apis.py`. |
| `--total-quantity` | `totalQuantity` | One of quantity/notional | number | Base-asset quantity. Mutually exclusive with `--order-notional`. |
| `--order-notional` | `orderNotional` | One of quantity/notional | number | Quote-asset notional. Mutually exclusive with `--total-quantity`. |
| `--is-target-position` | `isTargetPosition` | No | boolean flag | Target-position mode. If set, use `--total-quantity` only. |
| `--start-time` | `startTime` | No | ISO 8601 string | Scheduled start time, e.g. `2025-09-03T01:30:00+08:00`. |
| `--execution-duration` | `executionDuration` | No | integer minutes | Max execution duration in minutes. |
| `--execution-duration-seconds` | `executionDurationSeconds` | No | integer seconds | Fine-grained duration for TWAP-1/POV; should be greater than 10. |
| `--must-complete` | `mustComplete` | No | boolean flag | Require completion within the execution duration. |
| `--maker-rate-limit` | `makerRateLimit` | No | number `0`-`1` | Minimum or target maker participation ratio. |
| `--pov-limit` | `povLimit` | No | number/string `0`-`1` | Max market volume participation ratio for POV. |
| `--pov-min-limit` | `povMinLimit` | No | number `0`-`1` | Min market volume participation ratio for POV. |
| `--limit-price` | `limitPrice` | No | number, `-1` for none | Local create script sends `limitPrice`; the SDK README also describes the worst acceptable price concept as `worstPrice`. |
| `--up-tolerance` | `upTolerance` | No | number/string `0`-`1` | Upper price tolerance. |
| `--low-tolerance` | `lowTolerance` | No | number/string `0`-`1` | Lower price tolerance. |
| `--strict-up-bound` | `strictUpBound` | No | boolean flag | Enforce strict upper bound. |
| `--tail-order-protection` / `--no-tail-order-protection` | `tailOrderProtection` | No | boolean | Enable or disable tail order protection. |
| `--reduce-only` | `reduceOnly` | No | boolean flag | Futures/perp reduce-only mode. |
| `--margin-type` | `marginType` | Required for `PERP` | `U`, `C` | `U` for USDT-margined, `C` for coin-margined. |
| `--is-margin` | `isMargin` | No | boolean flag | Use spot margin mode. |
| `--notes` | `notes` | No | string | Free-form order notes. |
| `--enable-make` / `--no-enable-make` | `enableMake` | No | boolean | Allow or disable maker orders. |
| `--client-order-id` | `clientOrderId` | No | string | Custom client order ID supported by the local script. |

### Common Create Order Templates

Use these templates after running the mandatory market-data and account-binding pre-checks. Replace `api-key-id`, `symbol`, side, quantity, and timing values with the user's confirmed values.

High-maker TWAP perp order:

```bash
python3 scripts/create_master_order.py \
  --strategy-type TWAP-1 \
  --algorithm TWAP \
  --exchange Binance \
  --symbol DOGEUSDT \
  --market-type PERP \
  --side buy \
  --api-key-id <api-key-id> \
  --total-quantity 100 \
  --execution-duration 30 \
  --must-complete \
  --tail-order-protection \
  --margin-type U \
  --maker-rate-limit 0.9
```

High-taker TWAP perp order:

```bash
python3 scripts/create_master_order.py \
  --strategy-type TWAP-1 \
  --algorithm TWAP \
  --exchange Binance \
  --symbol DOGEUSDT \
  --market-type PERP \
  --side buy \
  --api-key-id <api-key-id> \
  --total-quantity 100 \
  --must-complete \
  --margin-type U \
  --maker-rate-limit 0 \
  --up-tolerance 1 \
  --low-tolerance 0.6 \
  --execution-duration-seconds 59 \
  --no-tail-order-protection \
  --enable-make
```

Target-position order:

```bash
python3 scripts/create_master_order.py \
  --strategy-type TWAP-1 \
  --algorithm TWAP \
  --exchange Binance \
  --symbol DOGEUSDT \
  --market-type PERP \
  --side sell \
  --api-key-id <api-key-id> \
  --total-quantity 100 \
  --is-target-position \
  --margin-type U
```

Notes:

1. SDK examples may show enum values such as `Algorithm.TWAP`, `Exchange.BINANCE`, `MarketType.PERP`, `OrderSide.BUY`, and `StrategyType.TWAP_1`. For this skill's CLI, pass their string values: `TWAP`, `Binance`, `PERP`, `buy`, and `TWAP-1`.
2. SDK examples may show `marginType` or `MarginType`. For this skill's CLI, use `--margin-type U` or `--margin-type C`.
3. For create orders, `strictUpBound=false` is represented by omitting `--strict-up-bound`. The local create script only sends `strictUpBound=true` when `--strict-up-bound` is present.

### Paired Order CLI Wrapper

Use `create_paired_order.py` only when the user explicitly wants a paired order. It creates two master orders concurrently. If either leg fails, the script attempts to cancel any successfully created leg and exits non-zero. Do not ask the user to choose paired-order tolerance or strict-bound parameters; this wrapper hard-codes them for both legs.

Fixed internal parameters for both legs:

| SDK field | Fixed value | User selectable? | Notes |
| --- | --- | --- | --- |
| `upTolerance` | `"0.05"` | No | Hard-coded in `create_paired_order.py`. |
| `lowTolerance` | `"0.10"` | No | Hard-coded in `create_paired_order.py`. |
| `strictUpBound` | `true` | No | Hard-coded in `create_paired_order.py`. |

| CLI flag | Scope | Required | Notes |
| --- | --- | --- | --- |
| `--strategy-type` | Both legs | No, default `TWAP_1` | Passed as `strategyType` for both orders. |
| `--algorithm` | Both legs | No, default `TWAP` | Passed as `algorithm` for both orders. |
| `--exchange` | Both legs | Yes | Same exchange for both legs. |
| `--api-key-id` | Both legs | Yes | Same exchange API binding ID for both legs. |
| `--execution-duration` | Both legs | No, default `5` | Minutes. |
| `--start-time` | Both legs | No | ISO 8601 string. |
| `--must-complete` | Both legs | No | Boolean flag. |
| `--symbol-1` / `--symbol-2` | Per leg | Yes | Trading pair for each leg. |
| `--market-type-1` / `--market-type-2` | Per leg | Yes | Market type for each leg. |
| `--side-1` / `--side-2` | Per leg | Yes | Side for each leg. |
| `--total-quantity-1` / `--total-quantity-2` | Per leg | One of quantity/notional | Mutually exclusive with the matching `--order-notional-*`. |
| `--order-notional-1` / `--order-notional-2` | Per leg | One of quantity/notional | Mutually exclusive with the matching `--total-quantity-*`. |
| `--margin-type-1` / `--margin-type-2` | Per leg | Required for `PERP` | `U` or `C`. |

### Update and Cancel Parameters

Use `update_master_order.py` and `cancel_master_order.py` only after explicit user confirmation.

| Script | CLI flag | SDK field | Required | Notes |
| --- | --- | --- | --- | --- |
| `update_master_order.py` | `--master-order-id` | `masterOrderId` | Yes | Master order to update. |
| `update_master_order.py` | `--order-notional` | `orderNotional` | No | Updated notional. |
| `update_master_order.py` | `--total-quantity` | `totalQuantity` | No | Updated quantity. |
| `update_master_order.py` | `--up-tolerance` | `upTolerance` | No | Upper tolerance. |
| `update_master_order.py` | `--low-tolerance` | `lowTolerance` | No | Lower tolerance. |
| `update_master_order.py` | `--enable-make` | `enableMake` | No | Pass `true` or `false`. |
| `update_master_order.py` | `--maker-rate-limit` | `makerRateLimit` | No | Number `0`-`1`. |
| `update_master_order.py` | `--strict-up-bound` | `strictUpBound` | No | Pass `true` or `false`. |
| `update_master_order.py` | `--pov-limit` | `povLimit` | No | Number `0`-`1`. |
| `update_master_order.py` | `--pov-min-limit` | `povMinLimit` | No | Number `0`-`1`. |
| `update_master_order.py` | `--worst-price` | `worstPrice` | No | Worst acceptable price, `-1` for no limit. |
| `update_master_order.py` | `--tail-order-protection` | `tailOrderProtection` | No | Pass `true` or `false`. |
| `update_master_order.py` | `--must-complete` | `mustComplete` | No | Pass `true` or `false`. |
| `update_master_order.py` | `--execution-duration-seconds` | `executionDurationSeconds` | No | Mutually exclusive with `--execution-duration`. |
| `update_master_order.py` | `--execution-duration` | `executionDuration` | No | Mutually exclusive with `--execution-duration-seconds`. |
| `cancel_master_order.py` | `--master-order-id` | `masterOrderId` | Yes | Master order to cancel. |
| `cancel_master_order.py` | `--reason` | `reason` | No | Optional cancel reason. |

## Parameter Validation Rules (P0)

1. `--total-quantity` and `--order-notional` are mutually exclusive.
2. If `--is-target-position` is set, use `--total-quantity` only.
3. `PERP` orders must include `--margin-type` (`U` or `C`).
4. Supported enums only:
   - exchange: `Binance` / `OKX` / `LTP` / `Deribit` / `Hyperliquid`
   - market-type: `SPOT` / `PERP` / `FUTURES`
   - side: `buy` / `sell`
5. Time format standards:
   - `get_master_orders.py` and `get_order_fills.py`: ISO 8601
   - `get_tca_analysis.py`: Unix milliseconds

## Risk Check Rules (P0)

### Spot

1. If quantity mode is used, compute notional as `quantity * current_price`.
2. Check quote-asset available balance before submit.
3. If available balance < order notional, mark as insufficient and require explicit reconfirmation.

### Perp/Futures

1. Select account-type-specific scripts from `list_exchange_apis.py` (`isPm`):
   - PM account: `get_pm_positions.py` + `get_pm_margin.py`
   - Normal account: `get_fapi_positions.py` + `get_fapi_margin.py`
2. Read leverage from current position when available.
3. Estimate required margin as `order_notional / leverage`.
4. Compare required margin with available margin before submit.
5. If margin is tight, show clear risk notice and require explicit reconfirmation.

## Paired Order Rules (P0)

1. Use `create_paired_order.py` for paired execution.
2. Do not simulate paired flow by running `create_master_order.py` twice.
3. Return both order IDs explicitly.
4. If one paired leg fails, report the rollback result for any successfully created leg.
5. If rollback cancellation fails or a successful leg result has no `masterOrderId`, stop and require manual review.

## Cancellation Rules (P0)

1. For multiple cancellations, execute sequentially and verify each result.
2. Do not assume cancellation success from command invocation alone.

## Pagination Rules

1. Preserve `total`, `page`, and `pageSize`.
2. If `total > pageSize`, explicitly state current page coverage.

## Notification Note

- `notify_order_complete.py` is optional and OpenClaw-oriented.
- Generic hosted agents should use direct status queries as the default flow.
