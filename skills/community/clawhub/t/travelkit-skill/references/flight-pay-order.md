# flight-pay-order ref

## Purpose

Use `flight_pay_order` only for an already-created order when the user explicitly wants to pay. Never pay automatically.

## Before Payment

- Restate order number, amount, payment method, and known order status.
- Amount follows `output-rules`: total = fare + tax.
- If payment method is missing, ask the user to choose. Do not default.
- User-facing methods: domestic can show 微信、支付宝、易宝移动支付、信用卡、借记卡; international can also show Airwallex.
- Do not offer balance payment. If the user asks for it, show the supported user payment methods and ask them to choose again.

Internal channel mapping:

| User method | Tool channel |
|---|---|
| Airwallex | `airwallex` |
| 支付宝 | `yeepay-alipay` |
| 微信 | `yeepay-wechat` |
| 易宝移动支付 | `yeepay-mobile` |
| 信用卡 | `yeepay-credit-card` |
| 借记卡 | `yeepay-debit-card` |

Ask:

> 是否确认支付？

- 支付金额：¥xxx
- 订单号：xxxxxx

Call `flight_pay_order` only after explicit confirmation.

## Payment Link

After `flight_pay_order` returns a third-party payment link, use this exact format. Do not expose internal channel names, raw JSON, `returnUrl`, or technical parameters.

```markdown
{支付方式}支付已发起，请打开链接完成付款：

[前往{支付方式}支付]({支付链接})

订单金额：¥{订单金额}
交易手续费：¥{交易手续费}
需支付合计：¥{订单金额 + 交易手续费}

付款完成后告诉我一声，我帮你核查订单和出票状态。
```

- Payment method names: 微信、支付宝、易宝移动支付、信用卡、借记卡、Airwallex.
- If payment link is missing, say: `支付链接暂未返回，我会先核查订单支付状态。`
- Transaction fee must come from the tool. If fee is missing, show `未返回`; then payable total is also `未返回`.
- Use the configured default third-party `returnUrl`; do not explain it to normal users.

## Risk Checks

Before retrying payment, call `flight_order_detail` if amount mismatches, fare + tax conflicts with returned total, order status is unclear, prior payment may be processing, order may be expired, or deadline is unclear.

## After User Says Paid

Goal: check payment status and ticketing status without changing the order.

1. Call read-only `flight_order_detail` immediately.
2. If neither payment nor ticketing has a clear result, poll every 10 seconds（每 10 秒）.
3. Stop after 12 total checks（12 次）, including the first immediate check.
4. Use only `flight_order_detail`; never trigger pay, cancel, refund, or change during polling.
5. Do not message the user on every poll. Reply only on a clear result, query failure, or after all 12 checks.
6. Prefer background/timer/automation polling when available. If only synchronous waiting works, tell the user you are checking every 10 seconds. If the environment cannot wait or schedule, say so and ask the user to request another check later.

Clear results:

- Payment terminal states: paid/success, failed, canceled, expired, or any explicit payment result returned by the tool.
- Ticketing terminal states: ticketed/success, failed, abnormal, or any explicit ticketing result returned by the tool.
- Missing or ambiguous fields are not results; keep polling until the limit.

Final notification must include order number, latest payment status, latest ticketing status, and next step. Use the `output-rules` order template when showing order details.

## Errors

On payment failure, briefly explain the returned reason, check current order status with `flight_order_detail`, then decide whether retry is appropriate. Do not blindly retry.
