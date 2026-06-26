# output-rules ref

## User Output

- Default to Simplified Chinese for consumers; keep tool names, MCP fields, and code identifiers in English only when needed.
- Summarize tool results. Do not paste raw JSON, internal IDs, API keys, confirmation flags, `orderKey`, `solutionId`, `passengerIds`, or `segmentIds`.
- Prices default to CNY. Dates/times use China-friendly wording.
- If baggage, policy, status, fee, ticketing, or deadline data is not returned, say it was not returned. Do not invent.
- Copyable fields such as order number, ticket number, and document tail number should stand alone without punctuation stuck to the value.
- Never show `PNR`, `airlinePnr`, or airline PNR in normal user-visible output, including `PNR: 未返回`, `票号 / PNR`, or `票号/PNR`.
- Before sending, delete or rewrite any field, table row, bullet, or sentence that contains `PNR` or `airlinePnr`, including status, ticketing, refund/change, and error explanations.
- If a real ticket number is returned, show it only as `票号`; never merge ticket number and PNR into one field. If ticket number is not returned, omit the ticket-number line instead of writing that it was not returned.

## Flight Numbers

- Show only the complete flight number returned by the tool, such as `CA1728`.
- Do not display "airline name + flight number". Airline codes may be used internally for filtering only.

## Order Template

Use this fixed structure for order creation success, order lookup, and post-payment status checks. Do not change titles, field names, field order, or amount format. Missing fields: `未返回`.

Only unpaid order-creation success starts with `订单已创建，尚未支付。`. For lookup or post-payment checks, describe the actual returned status instead.

Do not add PNR fields outside this template, even if the tool returns them. Do not mention PNR emptiness or absence in prose.

```markdown
订单已创建，尚未支付。

### 订单信息
- 订单号：
- 订单状态：
- 支付状态：
- 最晚支付时间：

### 乘客
- 姓名 / 乘客类型 / 证件尾号（如可展示）

### 航段
| 航段 | 航班号 | 行程 | 时间 |
|---|---|---|---|

### 金额
金额：¥{总价}（票面价 ¥{票面价} + 税价 ¥{税价}）

### 下一步
- 根据订单状态给出支付、等待出票、下载行程单、改退等下一步。
```

## Amounts

- Total = fare + tax. Sum fare and tax across passengers/segments before calculating total.
- Always use: `金额：¥{总价}（票面价 ¥{票面价} + 税价 ¥{税价}）`.
- If only total is returned, use: `金额：¥{总价}（票面价 未返回 + 税价 未返回）`.
- If returned total differs from fare + tax, show fare + tax total and say: `返回总额与票面价加税价不一致，我会重新核查订单金额。`
- If payment/ticketing deadline is missing, write: `最晚支付时间：暂未返回，请尽快完成支付；支付前我会再次核查订单状态。`

## Refund/Change Rule Codes（退改规则编码）

When refund/change policy is returned as encoded time and amount rules, translate it into plain Chinese before showing users:

- `*`: 所有时间段。
- `>n`: `n > 0` 表示起飞前 n 小时前；`n < 0` 表示起飞后 `abs(n)` 小时前。
- `<n`: `n > 0` 表示起飞前 n 小时后；`n < 0` 表示起飞后 `abs(n)` 小时后。
- 金额 `> 0`: 显示对应金额。金额 `0`: 免费。金额 `-1`: 按当前场景显示不可退 / 不可改。
- Do not expose confusing negative-hour wording to users; for example `>-2` means `起飞后 2 小时前`.
- If the rule, time condition, or amount is missing, say it was not returned and do not infer from experience.

## Low Inventory

- Low inventory means any returned `segments[].availability <= 3`.
- In the order template "下一步", if low inventory is known, display the remaining ticket count and remind the user to pay quickly or tickets may sell out.
- Multi-segment: use the lowest returned availability. If availability is not returned, do not mention low inventory or invent a count.

## Passenger Data

- Search stage: never collect ID/passport, phone, email, birthday, or gender.
- After verified price and user says to proceed: collect passenger data through `flight-create-order`.
- Do not guess passenger data. For ID-card passengers, do not split Chinese document names; use the full document name according to `flight-create-order`. For passport passengers, use the provided passport English surname/given names.
- Use natural Chinese bullets, not code blocks, gray form blocks, blank templates, or raw forms.
- Fixed collection templates in `flight-create-order` must keep their fields and order.

## Error Output

- Read tool failure: brief reason plus useful next step.
- Write tool failure: do not blindly retry; check status first when relevant.
- Email errors (`email`, valid email, empty email, missing email): say `供应商要求乘机人邮箱`; ask only for email and do not re-collect other passenger data.
- Name errors (`FirstName`, `LastName`, ID-card name): say `证件姓名格式不符合供应商要求`. For ID-card passengers, ask only to verify or correct the full document name; do not ask for surname/given-name splitting. Do not blame price or inventory.
- Service/config/auth/JSON errors: do not expose stack traces, tokens, signatures, raw errors, or API keys. For API-key/auth issues, use `mcp-connection` guidance; tell users to go to https://www.travelkit.ai/ to apply/configure credentials, and never ask them to paste the key in chat.
- On service/config failure, do not ask users to resend personal data.

## Pre-Tool Check

Before calling TravelKit MCP tools, verify intent, operation type, confirmation for writes, hidden internal fields, natural consumer output, no invented missing data, and correct passenger-data timing.
