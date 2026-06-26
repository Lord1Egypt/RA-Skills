---
name: todays-orders
description: Use this skill when the user wants a single approved onchain order for a Solana wallet, one explicit forbidden order, a quote-backed execution preview, or a receipt-backed daily debrief powered by OKX OnchainOS.
---

# Today's Orders

Use this skill to run the `Today's Orders / 今日军令` workflow inside OpenClaw. The job is not to produce many ideas. The job is to compress one wallet into:

- `今日军情`
- `今日军令`
- `今日禁令`
- `执行推演`
- `夜间战报`

This skill is designed for `OpenClaw x OKX OnchainOS`.

## When to use it

- The user wants a daily onchain plan for one Solana wallet.
- The user asks what to do today with an existing wallet.
- The user wants one approved action instead of many trade ideas.
- The user wants one forbidden action written explicitly.
- The user wants a quote-backed preview before execution.
- The user wants to execute after approval and then summarize the result with a receipt-backed debrief.

## Core law

Every response must obey this rule:

`Approve at most one order for today. Suppress the rest.`

## Required capabilities

Use `OKX OnchainOS` as the factual layer:

- `Wallet / Portfolio` for balances, holdings, stablecoin reserve, concentration, and idle capital
- `Market` for price, 24h move, and token context
- `Trade` for quote, route comparison, and execution preview
- `Broadcast / Status` for signature, confirmation, and receipt

Do not invent holdings, quotes, routes, or receipts.

## Workflow

1. Extract one Solana wallet address. If none is provided, ask for it.
2. Read the wallet posture first:
   - total wallet value
   - top holdings
   - stablecoin reserve
   - concentration
   - idle capital
3. Pull market context only for the few holdings that matter most today.
4. Decide one of four daily stances:
   - `deploy`
   - `defend`
   - `observe`
   - `watch-only`
5. Approve at most one order. Prefer:
   - small deployment from stablecoins into a major asset
   - partial trim from an over-concentrated bag into a stable reserve
   - no action if the setup is not clean
6. Write one forbidden order that is specific to the current wallet posture.
7. If execution is requested, use `Trade` to produce:
   - quote
   - route
   - slippage context
   - expected output
8. Only if the user approves, continue to `Broadcast / Status` and return the receipt.
9. Close with a daily debrief based on the actual state:
   - preview debrief if not executed
   - receipt-backed debrief if executed

## Fixed output

Always return the result in this order:

1. `今日军情`
   - one-line stance
   - wallet summary
   - 2-3 evidence bullets
2. `今日军令`
   - exactly one approved action, or explicitly say no action is approved
3. `今日禁令`
   - one action that should not be taken today
4. `执行推演`
   - quote, route, slippage, expected output
   - label clearly as `preview` until executed
5. `夜间战报`
   - preview debrief if not executed
   - receipt-backed debrief if executed

## Output guidance

- Keep the tone disciplined and procedural.
- Use the military shell only as product language, not as roleplay spam.
- If no clean setup exists, return `watch-only` and explain why.
- Never approve more than one order.
- Do not treat simulation as execution.
- If the user asks to execute, ask for final approval before broadcast.
