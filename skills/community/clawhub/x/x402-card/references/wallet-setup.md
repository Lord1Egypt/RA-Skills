# Wallet Setup

## Requirements

- An EVM wallet private key
- USDT (BEP-20) on BSC for card purchases
- Small BNB for gas (~$0.01 per tx)

## Step 1: Provide Private Key

```bash
npx @aeon-ai-pay/x402-card setup --private-key 0x...
```

Service URL has a built-in default — no need to configure unless you want to override:

```bash
# Optional: override service URL
npx @aeon-ai-pay/x402-card setup --service-url https://custom-api.example.com
```

Or pass via CLI flags per command:

```bash
npx @aeon-ai-pay/x402-card wallet --private-key 0x...
npx @aeon-ai-pay/x402-card create --amount 0.6 --private-key 0x...
```

**Security:**
- NEVER commit `.env` or private keys to git
- Use a dedicated wallet, not a personal wallet with large holdings

## Step 2: Verify Wallet

```bash
npx @aeon-ai-pay/x402-card wallet
```

Output:
```json
{
  "address": "0x1234...5678",
  "bnb": "0.05",
  "usdt": "100.00",
  "network": "BSC Mainnet (Chain ID: 56)"
}
```

## Step 3: Confirm

- `usdt` > 0: can purchase cards
- `bnb` > 0: can pay gas fees
- Both zero: need deposits to the displayed address

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing private key | Run `setup --private-key 0x...` |
| USDT = 0 | Transfer USDT (BEP-20) to wallet address |
| BNB = 0 | Transfer BNB for gas fees |
| Wrong network | Ensure BSC mainnet, not testnet |
