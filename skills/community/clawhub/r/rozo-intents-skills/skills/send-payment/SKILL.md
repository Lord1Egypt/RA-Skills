---
name: send-payment
description: >
  Send cross-chain crypto payments via Rozo API. Handles USDC and USDT
  payouts across EVM chains (Ethereum, Arbitrum, Base, BSC, Polygon), Solana, and
  Stellar (Base and Stellar are USDC-only; Solana receives USDC only but can pay in USDT). Use when user says
  "pay", "send", "transfer", "payout" for crypto/USDC/USDT with crypto
  amounts, chain names, or wallet addresses — NOT for ordinary fiat
  payments or bank transfers. Also handles QR code screenshots containing
  payment URIs (EIP-681, Solana Pay, Stellar URI). Auto-detects wallet
  type, auto-selects token (USDC preferred). Every payment shows full
  details and waits for an explicit yes/no; small-amount auto-execute is
  opt-in and ships disabled (thresholds 0 in version.json).
metadata:
  author: rozo
  version: 0.1.0
---

# Send Cross-Chain Payment

## Runtime

All `node scripts/dist/*.js` commands below MUST run from the **plugin root**
(the directory containing `.claude-plugin/plugin.json`), not from this
skill's directory. When installed as a Claude Code plugin, the plugin root
is `${CLAUDE_PLUGIN_ROOT}`. If that env var isn't set, `cd` to the directory
that contains `scripts/dist/`, `skills/`, and `.claude-plugin/`.

## Irreversibility

**Every transfer this skill creates is irreversible once funded.** Verify
destination address, chain, token, memo and amount with the user before
funding; a mistake is not recoverable by Rozo. (If the
user has deliberately raised the auto-execute thresholds, their standing
opt-in covers amounts below them — correctness checks still run, but the
per-payment restatement is not required there.)

## Confirmation Thresholds

**Auto-execute is OFF by default.** Both thresholds ship as `0`: every
payment, any amount, gets a full summary and an explicit yes/no. A user who
wants small amounts to run unprompted must raise the thresholds in
`version.json` themselves — that is the opt-in.

Read `version.json` at the plugin root for the current thresholds:

- `freeConfirmThresholdUsd` (default `0` = disabled) — at or below: silent auto-execute
- `singleConfirmThresholdUsd` (default `0` = disabled) — at or below: narrated auto-execute

**Auto-execute is OFF by default.** With the shipped `0`/`0` every payment,
any amount, gets the full summary and an explicit yes/no. Raising the
thresholds in `version.json` is the user's deliberate opt-in; never suggest
it, just act on the values found.

**Behavior matrix** (the amount below is `destAmount` in USD):

| Amount               | Confirmation            | Agent narration              | Dryrun fee check            |
|----------------------|-------------------------|------------------------------|-----------------------------|
| `≤ freeConfirm`      | **None** — auto-execute | **Silent** — report only result | **Skip** (fee = 0)       |
| `≤ singleConfirm`    | **None** — auto-execute | **Narrate** steps, no yes/no    | **Skip** (fee = 0)       |
| `> singleConfirm`    | **One** yes/no with full details | Full summary + prompt | **Run** `--dryrun` for exact fee |

**Rozo charges no fee for transactions at or below `singleConfirmThresholdUsd`**
(business rule). For amounts in that range you can skip the `--dryrun` step
entirely and go straight to `create-payment.js` without `--dryrun`.

**Chain ambiguity is NOT a confirmation question.** If the user gives an EVM
address without specifying a chain, you MUST ask which chain regardless of
amount. Wrong chain = lost funds. Only the yes/no confirmation is skipped
for small amounts, never correctness checks (chain selection, trustline
check, insufficient balance).

## Instructions

Process cross-chain crypto payments via the Rozo API. Follow steps sequentially.

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
- **Stellar wallet (G or C)** — preferred source (lowest fees, fastest settlement)
- EVM agent wallet (Base, Ethereum, Polygon, etc.)
- Solana agent wallet
- Private key wallets on any supported chain

**Source chain selection priority:**
1. If the user explicitly names a source chain/wallet, use it.
2. Otherwise ask: "Which wallet are you paying from? I recommend Stellar if
   you have one — it has the lowest fees (zero for ≤ $10) and the fastest
   settlement."
3. **Never go looking for wallet secrets to answer this yourself.** Do not
   probe for `.stellar-secret`, read `.env` files, or enumerate key material
   to infer what the user holds. Secret discovery is how a payment skill
   turns into a credential harvester; the user names the wallet, or you ask.

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

**Note:** USDT payout is only supported on Ethereum, Arbitrum, BSC, and Polygon. Base is USDC-only (no USDT pay-in or pay-out). If the destination is Base, Solana, or Stellar and USDC is insufficient, inform the user that only USDC payouts are supported for that chain.

After fetching, tell the user their balance:
> "Your wallet has [X] USDC and [Y] USDT on [chain]. Using [token] for this payment."

### Step 5: Fee Estimation & Confirmation (amount-dependent)

Read the thresholds from `version.json` (see "Confirmation Thresholds"
above). **They ship as `0`/`0`, so by default NO amount qualifies for the
auto-execute branches below** — every payment takes the confirmation path.
The branches apply only when the user has raised the thresholds themselves.

**If `amount ≤ singleConfirmThresholdUsd`** (only possible after user opt-in):
- **Skip the dryrun step entirely.** Rozo charges no fee at or below $10.
- **Skip the yes/no question.**
- If `amount ≤ freeConfirmThresholdUsd`: stay silent, proceed straight to Step 6.
- If `freeConfirm < amount ≤ singleConfirm`: narrate what you're doing ("Sending 5 USDC on Base to 0x…, no fee, creating payment now…") but do not ask yes/no. Proceed to Step 6.

**If `amount > singleConfirmThresholdUsd`:**

Get the exact fee first via a dryrun:

```bash
node scripts/dist/create-payment.js \
  --source-chain <chain_id_or_name> \
  --source-token <USDC|USDT> \
  --dest-chain <chain_id_or_name> \
  --dest-address <address> \
  --dest-token <USDC|USDT> \
  --dest-amount <amount> \
  --dryrun
```

Then present a full confirmation summary:

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

Only proceed to Step 6 if the user confirms. Default payment type is
`exactOut` — recipient gets the exact amount, fee added on top.

### Step 6: Create Payment

```bash
node scripts/dist/create-payment.js \
  --source-chain <chain_id_or_name> \
  --source-token <USDC|USDT> \
  --dest-chain <chain_id_or_name> \
  --dest-address <address> \
  --dest-token <USDC|USDT> \
  --dest-amount <amount> \
  --dest-memo <memo_if_stellar_c_wallet>
```

`--source-chain` and `--dest-chain` accept either numeric chain IDs (`8453`,
`1500`, `900`) or lowercase chain names (`base`, `stellar`, `solana`,
`ethereum`, `arbitrum`, `bsc`, `polygon`). Use whichever the user gave you.

After success, the API returns a `receiverAddress` and (for Stellar /
Solana) a `receiverMemo`. **The memo is a routing detail — do not mention
it to the user unless they ask.** The user should see a clean summary:

```
Creating payment... done.
Payment ID: <uuid>
```

### Step 7: Fund the Payment

After `create-payment.js` succeeds, Rozo returns a **deposit address**
(`receiverAddress`) and optionally a **memo** (`receiverMemo`). The payment
will NOT proceed until you send the source tokens to that deposit address.
This step actually moves money on-chain.

**How to fund depends on the source chain:**

#### Stellar source (preferred)

If the user has a Stellar wallet, use the **stellar-agent-wallet** plugin's
`send-payment` sub-skill to submit the on-chain payment:

```bash
npx tsx skills/send-payment/run.ts \
  --to <receiverAddress> \
  --chain stellar \
  --amount <source_amount> \
  --yes
```

The `receiverMemo` is handled automatically by the stellar-agent-wallet's
run.ts when it creates the Rozo intent internally. However, if you are
funding an **already-created** intent (from this skill's `create-payment.js`),
you must submit a direct Stellar Classic USDC payment instead:

1. Build a `payment` operation to `receiverAddress` with USDC asset
   (`USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN`)
2. Add `Memo.text(receiverMemo)` — **CRITICAL: without the memo, funds are
   lost.** The deposit address is shared across all Rozo orders; the memo
   routes your payment to your specific order.
3. Sign with the user's Stellar key and submit via Horizon

#### EVM source (Ethereum, Arbitrum, Base, BSC, Polygon)

Instruct the user to send the exact source amount of the specified token
to the deposit address from their EVM wallet. Provide:
- **Deposit address**: `<receiverAddress>`
- **Amount**: `<source.amount>` `<token>`
- **Chain**: must match the `--source-chain` used when creating the intent

#### Solana source

Instruct the user to send the exact source amount to the deposit address.
Include the memo if one was provided in the response.

**IMPORTANT**: Do NOT reference `send-onchain.js` — that script does not
exist in this plugin. Funding is done via the stellar-agent-wallet skill
(for Stellar) or manual user action (for EVM/Solana).

### Step 8: Poll Status Until Complete

Rozo usually confirms end-to-end within 10–15 seconds. Poll with:

```bash
node scripts/dist/get-payment.js --id <payment_id>
```

(You can also use `--payment-id <uuid>`, `--tx-hash <hash>`, or
`--receiver-address <addr> --receiver-memo <memo>` — see the
`payment-status` sub-skill.)

**Do not use `sleep` between polls** — some harnesses block it. Just re-run
the command immediately.

Watch for `status` to reach `payment_payout_completed` or `payment_completed`.
When it does, present a final summary with the destination `txHash` linked
to the appropriate block explorer (Basescan, Stellar Expert, Solscan, etc.).

For amounts `≤ singleConfirmThresholdUsd`, keep the final report to one or
two lines:

```
✓ Sent 0.10 USDC to 0x5772…8897 on Base.
   tx: https://basescan.org/tx/0x621a…75c3
```

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
