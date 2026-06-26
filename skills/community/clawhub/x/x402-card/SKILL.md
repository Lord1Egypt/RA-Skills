---
name: x402-card
description: >
  Use this skill when the user wants to purchase a virtual debit card using crypto,
  create a prepaid card via x402 protocol, check virtual card status, or set up an
  EVM wallet for card payments. Trigger on: "buy a card", "get a virtual card",
  "create card", "card status", "setup wallet for card", or any intent involving
  purchasing virtual Visa/Mastercard with cryptocurrency.
emoji: "💳"
homepage: https://github.com/AEON-Project/x402-card
metadata:
  version: "0.2.0"
  author: AEON-Project
  openclaw:
    requires:
      bins:
        - node
        - npx
    primaryEnv: EVM_PRIVATE_KEY
    user-invocable: true
    disable-model-invocation: false
compatibility: Requires Node.js >= 18 and npm
---

# x402 Virtual Card Skill

Purchase virtual debit cards (Visa/Mastercard) by paying with USDT on BSC via the x402 HTTP payment protocol.

## CLI Tool

All operations use `npx @aeon-ai-pay/x402-card`:

```bash
# First time: provide your EVM wallet private key (service URL has a built-in default)
npx @aeon-ai-pay/x402-card setup --private-key 0x...

# Show current config
npx @aeon-ai-pay/x402-card setup --show

# Create a virtual card ($5 USD, auto-poll status)
npx @aeon-ai-pay/x402-card create --amount 5 --poll

# Check card status
npx @aeon-ai-pay/x402-card status --order-no <orderNo>

# Check wallet balance
npx @aeon-ai-pay/x402-card wallet
```

## Configuration

Config is stored at `~/.x402-card/config.json` (file permission 600). Only `privateKey` is required — service URL has a built-in default.

Priority (high to low):
1. **CLI flags**: `--private-key`, `--service-url`
2. **Environment variables**: `EVM_PRIVATE_KEY`, `X402_CARD_SERVICE_URL`
3. **Config file**: `~/.x402-card/config.json` (set via `setup` command)

## Step 0: Pre-flight Checks

Before ANY operation (create, wallet, status), run these two checks **in parallel**:

### 0a. Auto-upgrade skill (background, non-blocking, once per session)

Run in background (async) only once per session, do NOT wait for result before proceeding:

```bash
npx @aeon-ai-pay/x402-card upgrade --check
```

- `"upToDate": true` → ignore.
- `"upToDate": false` → when result arrives, inform user and run upgrade:
  ```bash
  npx @aeon-ai-pay/x402-card upgrade
  ```
- Network failure → ignore silently.

### 0b. Check config (foreground, blocking)

```bash
npx @aeon-ai-pay/x402-card setup --check
```

- Exit code 0 + `"ready": true` → proceed to user intent. The response includes `amountLimits: { min, max }` — use these when prompting the user for card amount.
- Exit code 1 + `"ready": false` → only `privateKey` is needed (service URL has a built-in default). Ask user:
  > "Please provide your EVM wallet private key (BSC network). It will be stored locally at ~/.x402-card/config.json with restricted file permissions and never transmitted elsewhere."
- Then run:
  ```bash
  npx @aeon-ai-pay/x402-card setup --private-key <key>
  ```
- Do NOT ask for service URL unless the user explicitly wants to change it.

## Decision Tree

After config is verified, determine user intent and route:

### 1. User wants to BUY / CREATE a virtual card
- Read [create-card](references/create-card.md) for the full workflow.
- **Amount limits come from `setup --check` response** (`amountLimits.min` / `amountLimits.max`). Do NOT hardcode, memorize, or guess any limit values — always use the numbers returned by the CLI.
- CLI `create` command validates the amount and returns error JSON with allowed range if invalid.
- CLI will **auto-check** wallet balance before payment. If insufficient, it reports the shortfall.
- **MUST** confirm amount with the user before running the create command. Show the range from `amountLimits` so the user knows the valid range.

### 2. User wants to CHECK card status
- Read [check-status](references/check-status.md) for status query details.
- Requires an `orderNo` from a previous creation.

### 3. User wants to SETUP or UPDATE config
- Read [wallet-setup](references/wallet-setup.md) for configuring the EVM wallet.
- Must be done before any card purchase.
- To update, run `setup` with only the field to change:
  ```bash
  # Update private key
  npx @aeon-ai-pay/x402-card setup --private-key <new-key>
  # Update service URL (optional, only if user explicitly requests)
  npx @aeon-ai-pay/x402-card setup --service-url <new-url>
  ```
- After update, run `setup --show` to confirm (private key is masked).

### 4. User wants to understand the PROTOCOL
- Read [x402-protocol](references/x402-protocol.md) for how x402 works.

## Anti-patterns

- **NEVER** proceed with payment without explicit user confirmation of the amount.
- **NEVER** log or display the full private key. Mask it as `0x...last4`.
- **NEVER** skip the wallet setup check before attempting a purchase.
- **DO NOT** poll status more than 10 times. If still pending, inform the user and stop.

## Insufficient Balance Handling

When create returns `"error": "Insufficient USDT balance"`, present to user:

```
Wallet USDT balance is insufficient.
- Required: {required}
- Available: {available}
- Shortfall: {shortfall}

Please transfer at least {shortfall} USDT (BEP-20) to your wallet:
  {address}

Note: Send USDT on the BSC (BNB Smart Chain) network only. Transfers on other networks (ERC-20, TRC-20, etc.) will result in loss of funds.

After depositing, run the card creation again.
```

Do NOT attempt to transfer funds on behalf of the user. Depositing is the user's responsibility.
