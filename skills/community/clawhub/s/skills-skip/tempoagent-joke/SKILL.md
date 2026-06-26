---
name: tempoagent-mpp-joke
description: Auto-pay TempoAgent MPP endpoint with Tempo Wallet CLI, generate a joke, submit it to https://tempoagent.fun/api/mpp-payment-agent, and return only the score (1-10).
---

# TempoAgent MPP Joke Payment

Use this skill when the agent must call TempoAgent paid API with MPP using Tempo Wallet CLI.

## Goal

1. Check spendable balance first.
2. Generate one short joke by itself.
3. Pay MPP automatically.
4. Send joke to `https://tempoagent.fun/api/mpp-payment-agent`.
5. Return only numeric score `1-10`.

## Requirements

- Tempo Wallet CLI installed.
- Agent wallet funded for MPP payments.

## Spendable Balance Check (required before payment)

Always check spendable balance first. Do not rely on `balanceOf` only.

Why can available become 0?

1. pathUSD balance is too small
- example balance: `0.001996 pathUSD`
- payment needs: `0.1 pathUSD`
- effective available for payment becomes `0`

2. Tempo payment path checks spendable balance
- it evaluates **spendable balance**, not only `balanceOf`
- fee + transaction requirements are included

3. Fees are also paid with stablecoin on Tempo
- small dust balances are often not enough for:
  - payment amount
  - execution fee
  - transaction overhead

Important:
- right after first top-up, spendable may not be ready yet
- if spendable is insufficient, stop and wait/top-up first

## Task: Make spendable balance available

Before attempting payment, run this checklist:

1. Check wallet status and spendable balance.
```bash
tempo wallet status
```

2. Fund/top-up wallet if needed.
```bash
tempo wallet topup --token pathUSD --amount 1
```

3. Wait 20-60 seconds, then check again.
```bash
tempo wallet status
```

4. Retry the paid request once after spendable is ready.

## Canonical command (curl-style with auto payment)

```bash
# IMPORTANT: Agent must generate a fresh joke by itself each run.
# Do not hardcode/reuse the same joke text.
JOKE="<AGENT_GENERATED_JOKE>"
tempo wallet request https://tempoagent.fun/api/mpp-payment-agent \
  --method POST \
  --json "{\"joke\":\"$JOKE\"}"
```

## Raw curl (manual credential, not auto-pay)

```bash
curl -X POST https://tempoagent.fun/api/mpp-payment-agent \
  -H "Content-Type: application/json" \
  -H "Authorization: Payment <CREDENTIAL>" \
  -d '{"joke":"<AGENT_GENERATED_JOKE>"}'
```

## Output contract

- If success: output only one integer (`1` to `10`).
- If fail: output short error message only.
- If timeout occurs but tx may still settle: retry once, then report status.
- If spendable balance is not enough: stop and ask for top-up/wait, do not spam retries.
