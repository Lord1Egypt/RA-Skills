# Create Virtual Card

## Prerequisites Check

Before creating a card, verify:

1. `EVM_PRIVATE_KEY` is set — if not, guide user to [wallet-setup](wallet-setup.md)
2. Service URL is configured (has built-in default, no action needed unless user wants to override)
3. The `create` command automatically checks wallet balance before proceeding. No need to run `wallet` separately.

## Workflow

### Step 1: Confirm Amount

Ask the user how much they want to load onto the card.

- Amount limits are enforced by the CLI. Do NOT hardcode or state specific min/max numbers.
- Currency: USD (the service handles crypto conversion)

**MUST** get explicit confirmation before proceeding:
> "I'll create a virtual card loaded with $X.XX. This will debit approximately X.XX USDT from your BSC wallet. Proceed?"

### Step 2: Execute

```bash
# Create card and auto-poll status
npx @aeon-ai-pay/x402-card create --amount <amount> --poll
```

The CLI handles the full x402 two-phase protocol automatically:
1. Sends `GET /open/ai/x402/card/create?amount=X` → receives HTTP 402
2. Parses payment requirements, signs with EVM wallet (EIP-712)
3. Retries with `PAYMENT-SIGNATURE` header → receives HTTP 200
4. With `--poll`, auto-polls `/status` every 5s until card is ready

### Step 3: Parse Result

**stdout** outputs JSON (parseable), **stderr** outputs progress logs.

Success output:
```json
{
  "success": true,
  "data": {
    "code": "0",
    "msg": "success",
    "model": { "orderNo": "300217748668047431791" }
  },
  "paymentResponse": {
    "txHash": "0x...",
    "networkId": "eip155:56"
  }
}
```

With `--poll`, additional output when card is ready:
```json
{
  "pollResult": {
    "orderNo": "300217748668047431791",
    "orderStatus": "SUCCESS",
    "channelStatus": "COMPLETED",
    "orderAmount": 0.6,
    "txHash": "0xabc...def",
    "cardLastFour": "4321",
    "cardBin": "485932",
    "cardScheme": "VISA",
    "cardBalance": 0.6,
    "cardStatus": "ACTIVE"
  }
}
```

### Step 4: Present to User

When successful:
```
Virtual Card Created!
- Card: VISA •••• 4321
- Balance: $5.00 USD
- Order: 300217748668047431791
- Tx: 0xabc...def
```

Save the `orderNo` for future status queries.

## Error Handling

| Scenario | Action |
|----------|--------|
| Amount out of range | CLI rejects with error JSON containing allowed range — relay to user |
| Missing env vars | CLI shows which var is missing |
| Insufficient USDT | Run `wallet` command to show balance |
| Network error | Retry once, then report to user |
| Transaction reverted | Show txHash, suggest user check BSCScan |
