---
name: send-payment
description: >
  Send cross-chain crypto payments via Rozo API. Handles USDC and USDT
  payouts across EVM chains (Ethereum, Arbitrum, Base, BSC, Polygon), Solana, and
  Stellar. Use when user says "pay", "send", "transfer", "payout" with
  crypto amounts, chain names, or wallet addresses. Also handles QR code
  screenshots containing payment URIs (EIP-681, Solana Pay, Stellar URI).
  Auto-detects wallet type, auto-selects token (USDC preferred), confirms
  details before sending.
metadata:
  author: rozo
  version: 0.1.0
---

# Send Cross-Chain Payment

## Instructions

Process cross-chain crypto payments via the Rozo API. Follow steps sequentially. Do NOT skip confirmation.

### Step 1: Parse Payment Intent

The user may provide payment info as text OR as a QR code screenshot.

**If the user shares a QR code image:**
1. You (the agent) read the QR code from the screenshot and extract the text content
2. Pass the extracted text to the QR parser:
   ```bash
   node scripts/dist/parse-qr.js "<qr_content>"
   ```
3. The parser handles: EIP-681 (`ethereum:...`), Solana Pay (`solana:...`), Stellar URI (`web+stellar:pay?...`), and plain addresses
4. Extract address, chain, token, and amount from the parsed result

**If the user provides text:**
Extract from the user's message:
- **Amount** (required) — numeric value, minimum $0.01, maximum $10,000
- **Destination address** (required) — wallet address
- **Destination chain** — explicit name or detected from address
- **Source wallet/chain** — where the user is paying from

Do NOT ask the user which token. The token is auto-selected based on balance (see Step 4).

**Amount limits:** Minimum $0.01, maximum $10,000 per transaction. If the amount is outside this range, inform the user and stop:
> "Amount must be between $0.01 and $10,000."

### Step 2: Detect Wallet Type from Address

Identify the destination chain from the address format:

| Address Pattern | Detected Chain | Action |
|-----------------|---------------|--------|
| `0x` + 40 hex characters | EVM (ambiguous) | MUST ask which chain |
| Base58 encoded, 32-44 chars, no `0x` prefix | Solana (chain 900) | Auto-detect |
| Starts with `G`, 56 characters, Base32 | Stellar G-wallet (chain 1500) | Auto-detect, check trustline |
| Starts with `C`, 56 characters, Base32 | Stellar C-wallet (chain 1500) | Auto-detect, use contract payment flow |

**CRITICAL rules:**

1. **EVM address detected but chain not specified** — ALWAYS ask:
   > "Which chain should I send to? Supported EVM payout chains: Ethereum, Arbitrum, Base, BSC, Polygon"

2. **Stellar G-wallet** — check asset trustline before proceeding:
   ```bash
   node scripts/dist/check-stellar-trustline.js --address <G_wallet_address>
   node scripts/dist/check-stellar-trustline.js --address <G_wallet_address> --asset EURC
   ```
   Default asset is USDC. Also supports EURC.
   - If trustline exists → proceed normally
   - If trustline is missing → inform user and stop:
     > "This Stellar address does not have a [USDC/EURC] trustline. The recipient must add the trustline before they can receive funds."

3. **Stellar C-wallet** — use `stellar_payin_contracts` intent:
   - The Rozo API will return a unique Soroban contract address (`receiverAddressContract`) and memo (`receiverMemoContract`)
   - Instruct the user to invoke the contract's `pay()` function with the amount and memo
   - The system monitors the contract and triggers cross-chain payout once payment is detected

### Step 3: Determine Source Wallet

The user pays from their own wallet. They may have:
- EVM agent wallet (Base, Ethereum, Polygon, etc.)
- Solana agent wallet
- Stellar wallet (G or C)
- Private key wallets on any supported chain

If the source wallet/chain is not clear, ask:
> "Which wallet are you paying from? (e.g., Base wallet, Solana wallet, Stellar wallet)"

Consult `references/supported-chains.md` for the correct token addresses per chain.

### Step 4: Check Balance & Auto-Select Token

Fetch all USDC and USDT balances for the user's wallet in a single call:

```bash
node scripts/dist/check-balance.js --address <wallet_address>
```

The API auto-detects the chain type from the address and returns all token balances across all supported chains.

**Token selection priority:**
1. If USDC balance on the source chain is sufficient → use USDC
2. If USDC is insufficient but USDT balance on the source chain is sufficient → use USDT
3. If neither is sufficient → inform the user and stop

**Note:** USDT payout is only supported on EVM chains (Ethereum, Arbitrum, Base, BSC, Polygon). If the destination is Solana or Stellar and USDC is insufficient, inform the user that only USDC payouts are supported for that chain.

After fetching, tell the user their balance:
> "Your wallet has [X] USDC and [Y] USDT on [chain]. Using [token] for this payment."

### Step 5: Get Fee & Confirm Payment Details

Before confirming, get the exact fee:

```bash
node scripts/dist/create-payment.js \
  --source-chain <chain_id> \
  --source-token <USDC|USDT> \
  --dest-chain <chain_id> \
  --dest-address <address> \
  --dest-token <USDC|USDT> \
  --dest-amount <amount> \
  --dryrun
```

Then present a confirmation summary including the balance and fee:

```
Your wallet has [balance] [token] on [source_chain].

Payment Summary:
- Sending: [amount] [token]
- To: [destination_address] ([chain_name])
- From: [source_wallet] ([source_chain])
- Fee: [fee] [token] ([feePercentage])
- Total deducted: [amount + fee] [token]

Confirm? (yes/no)
```

Default payment type is `exactOut` — recipient gets the exact amount, fee is added on top. Only proceed if the user confirms.

### Step 6: Create Payment

```bash
node scripts/dist/create-payment.js \
  --source-chain <chain_id> \
  --source-token <USDC|USDT> \
  --dest-chain <chain_id> \
  --dest-address <address> \
  --dest-token <USDC|USDT> \
  --dest-amount <amount> \
  --dest-memo <memo_if_stellar_c_wallet>
```

After success, present: Payment ID, Status, Deposit address, any memo required.

## Examples

### Example 1: Clear text intent
User: "Pay 10 USDC on Base to 0x1234567890abcdef1234567890abcdef12345678"

1. Parsed: 10 USDC, Base, EVM address with chain specified
2. Determine source wallet → check balance → confirm → send

### Example 2: Stellar G-wallet
User: "Send 50 to GC56BXCNEWL6JSGKHD3RJ5HJRNKFEJQ53D3YY3SMD6XK7YPDI75BQ7FD"

1. Detected Stellar G-wallet, amount 50
2. Check USDC trustline → exists
3. Fetch balance → auto-select USDC (Stellar only supports USDC payout)
4. Confirm and send

### Example 3: Ambiguous EVM address
User: "Transfer 100 to 0xABCDEF1234567890ABCDEF1234567890ABCDEF12"

1. Detected EVM address, no chain specified
2. Ask: "Which chain? (Ethereum, Arbitrum, Base, BSC, Polygon)"
3. Proceed after selection

### Example 4: Stellar C-wallet (contract payment)
User: "Pay 25 USDC to CABCDEFGHIJKLMNOPQRSTUVWXYZ234567ABCDEFGHIJKLMNOPQRSTUV"

1. Detected Stellar C-wallet → `stellar_payin_contracts` intent
2. API returns Soroban contract address + memo
3. Instruct user to invoke contract's `pay()` with amount and memo

### Example 5: QR code (EIP-681 ERC-20)
User shares QR image. Decoded: `ethereum:0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913/transfer?address=0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed&uint256=1000000`

1. Parse QR → Base USDC, recipient `0x5aAe...`, 1.00 USDC
2. Check balance → confirm → send

### Example 6: QR code (Solana Pay)
User shares QR image. Decoded: `solana:9wFFmGphb7ys1gxkZUJ3pDQDkF1iVjU8D6S6A9VySbT9?amount=10.25&spl-token=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`

1. Parse QR → Solana USDC, 10.25
2. Check balance → confirm → send

### Example 7: QR code (Stellar URI)
User shares QR image. Decoded: `web+stellar:pay?destination=GC56BX...&amount=100&asset_code=USDC`

1. Parse QR → Stellar G-wallet, 100 USDC
2. Check trustline → check balance → confirm → send

### Example 8: QR code (plain address)
User shares QR containing: `0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6`
User says: "Send 50 to this address"

1. Plain EVM address, no chain → ask which chain
2. Proceed with standard flow

## Troubleshooting

### Error: 409 Conflict
Cause: Duplicate orderId. Solution: Generate a new orderId and retry.

### Error: Payment expired
Cause: Not funded in time. Solution: Create a new payment.

### Error: Payment bounced
Cause: Payout chain/address issue. Solution: Verify destination and retry.
