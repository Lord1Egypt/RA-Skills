---
name: wallet-twin-court
description: Use this skill when the user wants to put a Solana wallet on trial, identify the action most likely to cause regret tomorrow, return a verdict, and only then preview execution.
---

# Wallet Twin Court

Use this skill to run the `后悔药 / Wallet Twin Court` workflow inside OpenClaw. The job is not to produce many ideas. The job is to put one wallet on trial and compress the result into:

- `你的后悔体质`
- `今日被起诉的操作`
- `法庭裁决`
- `执行前审理`
- `判后报告`

This skill is designed for `OpenClaw x OKX OnchainOS`.

Public endpoint:

- Court API: `https://todays-orders.vercel.app/api/todays-orders`

## When to use it

- The user wants a pre-trade judgment for one Solana wallet.
- The user asks what action they are most likely to regret tomorrow.
- The user wants one verdict instead of many trade ideas.
- The user wants one explicit prosecuted action written down.
- The user wants a quote-backed hearing before execution.
- The user wants to execute only after a verdict and then summarize the result with a receipt-backed closing report.

## Core law

Every response must obey this rule:

`Every action must go through court first. High-regret trades do not get clearance.`

## Required capabilities

Use `OKX OnchainOS` as the factual layer:

- `Wallet / Portfolio` for balances, holdings, stablecoin reserve, concentration, idle capital, and historical mistake context
- `Market` for price, 24h move, and whether today is a high-temptation regime
- `Trade` for quote, route comparison, and execution hearing
- `Broadcast / Status` for signature, confirmation, and receipt

Do not invent holdings, quotes, routes, or receipts.

Do not substitute this skill with `miraix-wallet-roast`.
Do not call `https://app.miraix.fun/api/wallet-audit`.
Do not append the wallet roast share card URL.
This skill must use the `todays-orders` court endpoint and return the courtroom structure, not the roast structure.

## Workflow

1. Extract one Solana wallet address. If none is provided, ask for it.
2. Run:

```bash
curl -sS -X POST https://todays-orders.vercel.app/api/todays-orders \
  -H 'Content-Type: application/json' \
  -d '{"walletAddress":"<wallet-address>"}'
```

3. Base the answer on the returned JSON.
4. Read the wallet dossier first:
   - total wallet value
   - top holdings
   - stablecoin reserve
   - concentration
   - idle capital
5. Build the wallet twin's regret profile:
   - what kind of mistake is most likely today
   - whether today is a chase, revenge, over-rotation, or watch-only day
6. Prosecute exactly one action that should not happen today.
7. Return exactly one verdict:
   - `approve`
   - `probation`
   - `size-cap`
   - `reject`
8. If execution is requested and the verdict is not `reject`, use the returned `executionPreview` and `executionPlan` as the hearing record.
9. Only continue toward execution if the client environment can sign and broadcast safely. Otherwise stop at preview and say execution should continue in the wallet-connected web client.
10. Close with a final report based on the actual state:
   - preview report if not executed
   - receipt-backed report if executed

Important returned fields:

- `todayIntel`
- `forbiddenOrder`
- `approvedOrder`
- `executionPreview`
- `nightDebrief`
- `sentenceLadder`
- `verdictCertificate`
- `machineView`
- `executionPlan`

## Fixed output

Always return the result in this order:

1. `你的后悔体质`
   - one-line profile
   - wallet summary
   - 2-3 evidence bullets
2. `今日被起诉的操作`
   - one explicit action the court is prosecuting today
3. `法庭裁决`
   - exactly one verdict, or explicitly say no action is cleared
4. `执行前审理`
   - quote, route, slippage, expected output
   - label clearly as `preview` until executed
5. `判后报告`
   - preview report if not executed
   - receipt-backed report if executed

## Output guidance

- Keep the tone disciplined and procedural.
- The shell can be vivid, but the evidence must come from wallet, market, quote, and receipt data.
- Do not output `评分` unless that field truly exists in the court API output.
- Do not output a roast-style `分享卡片` URL.
- Do not rename the sections into wallet roast headings.
- If no clean setup exists, return `reject` or `watch-only` and explain why.
- Do not treat simulation as execution.
- If the user asks to execute, ask for final approval before broadcast.
