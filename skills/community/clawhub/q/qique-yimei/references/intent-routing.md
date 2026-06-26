# Intent Routing Notes

## Purpose

This routing protocol converts Chinese natural-language intent into:

1. `route.method`: SDK method name
2. `params`: extracted and normalized parameters
3. `missing_required`: required fields still missing before execution

## Extraction Rules (Key)

1. Phone: `1\d{10}` -> `telnum`
2. Customer ID: `客户id/cusId/...` -> `cusId`
3. Appointment ID: `预约id` -> `id`
4. Order IDs:
   - `订单id/billId` -> `billId`
   - `核销码/useCode` -> `useCode`
5. Wallet semantics:
   - `积分` -> `type=31`
   - `佣金` -> `type=21`
   - `余额` -> `type=22`
   - `加/增/补/充值` -> `action=add`
   - `扣/减/消费/使用` -> `action=use`
6. Date strings: `YYYY-MM-DD` or `YYYY-MM-DD HH:mm:ss`
   - Mapped by method context (wallet/appointment/order)

## Operation Safety

1. Router only resolves method + params; it does not call remote API.
2. Write methods still require explicit user confirmation.
3. Always check `can_execute=true` before presenting final execution plan.

## Example

Intent:

```text
把13800000000的积分加50，备注活动补偿
```

Expected route result:

- method: `changeWallet`
- operation: `write`
- params: `{ "telnum": "13800000000", "type": 31, "action": "add", "changeNum": 50, "remark": "活动补偿" }`
