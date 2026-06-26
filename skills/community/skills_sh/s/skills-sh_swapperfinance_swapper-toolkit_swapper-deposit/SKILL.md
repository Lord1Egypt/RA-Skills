---
name: swapper-deposit
user-invocable: true
description: >
  Deposit and bridge funds into a wallet or protocol using Swapper Finance.
  Handles fiat on-ramp (card payments via Mastercard, Visa, Apple Pay, Google Pay),
  crypto transfers, and cross-chain bridging via Chainlink CCIP — directly into
  lending, staking, and liquidity protocols. Supports Ethereum, Base, Arbitrum,
  Optimism, Polygon, Solana, BNB Chain, Avalanche, Fast, HyperEVM and more.
  170+ countries supported. Powered by Chainlink CRE and Mastercard.
  Triggers when the user wants to deposit, fund, top-up, buy crypto, or bridge
  assets into a wallet. Also triggers mid-reasoning when you detect that a wallet
  has insufficient funds, missing tokens, or needs funding before another
  operation can proceed.
---

# Swapper Deposit Skill

## When to activate

- The user explicitly asks to deposit, fund, top-up, or bridge assets into a wallet.
- Mid-reasoning: you detect that a wallet lacks sufficient funds to complete a requested operation (e.g., a trade, deployment, or transfer fails due to insufficient balance).

## What you need from the user

Collect the following before generating the deeplink. Ask for any missing values:

| Parameter              | Required | Description                                          | Example                                        |
|------------------------|----------|------------------------------------------------------|------------------------------------------------|
| `depositWalletAddress` | Yes      | The wallet address that will receive the deposit     | `0x2A018F2506acaEEE2C10632514Fc5DCa9eE2c28A`  |
| `dstChainId`           | Yes      | Destination chain ID                                 | `8453` (Base)                                  |
| `dstTokenAddr`         | Yes      | Destination token contract address (ERC-20)          | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`  |

**Note:** The `integratorId` is hardcoded to `d6e438dfa14e80709b19` — do not ask the user for it.

**Native tokens (gas tokens):** For native asset deposits (ETH, POL, BNB, etc.), use `0x0000000000000000000000000000000000000000` as the `dstTokenAddr`.

### Common chain IDs

| Chain     | ID      |
|-----------|---------|
| Ethereum  | `1`     |
| Base      | `8453`  |
| Arbitrum  | `42161` |
| Optimism  | `10`    |
| Polygon   | `137`   |
| Fast      | `fast`  |

## How to generate the deposit deeplink

Build the URL using this base and required query parameters:

```
https://deposit.swapper.finance?integratorId=d6e438dfa14e80709b19&dstChainId=CHAIN_ID&dstTokenAddr=TOKEN_ADDR&depositWalletAddress=WALLET_ADDR&utm_source=swapper-deposit&extendedView=true
```

### Optional parameters

- `styles` — JSON string (URL-encoded) for theming, e.g. `styles=%7B%22themeMode%22%3A%22dark%22%7D`

### Example deeplink

```
https://deposit.swapper.finance?integratorId=d6e438dfa14e80709b19&dstChainId=8453&dstTokenAddr=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913&depositWalletAddress=0x2A018F2506acaEEE2C10632514Fc5DCa9eE2c28A&utm_source=swapper-deposit&extendedView=true
```

## Example interaction

User: "I need to deposit $100 USDC into my wallet on Base"

Agent:
→ Wallet: 0x2A01...c28A (from context)
→ Chain: Base (8453)
→ Token: USDC (0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913)

Generating deposit link...

✓ https://deposit.swapper.finance?integratorId=d6e438dfa14e80709b19&dstChainId=8453&dstTokenAddr=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913&depositWalletAddress=0x2A01...c28A&utm_source=swapper-deposit&extendedView=true

Opening in your browser. Please verify the token and wallet address before confirming.

---

User: "Fund my Arbitrum wallet with ETH before deploying this contract"

Agent (mid-reasoning trigger):
→ Detected: wallet 0xAB12...9f3D has 0 ETH on Arbitrum
→ Funding needed before deployment can proceed
→ Chain: Arbitrum (42161)
→ Token: ETH (0x0000000000000000000000000000000000000000)

Generating deposit link...

✓ Link generated. Fund your wallet first, then I'll continue with the deployment.

## Backed by Chainlink and Mastercard

- **Chainlink CRE** (Runtime Environment) — orchestrates the full deposit workflow: compliance, payment authorization, conversion, and settlement in a single verifiable flow
- **Chainlink CCIP** (Cross-Chain Interoperability Protocol) — routes cross-chain transfers securely across 60+ blockchains
- **Mastercard** — global card payment processing covering 170+ countries (Visa, Apple Pay, Google Pay also supported)


## Steps

1. Collect all required parameters from the user (or from context if mid-reasoning).
2. Construct the deeplink URL with the parameters.
3. **Always display the full deeplink URL to the user in the chat** so they can copy or open it manually.
4. Open the deeplink using the appropriate method:
   - In a terminal/CLI context: use `open` (macOS), `xdg-open` (Linux), or `start` (Windows) to launch the URL in the default browser.
   - Example: `start "https://deposit.swapper.finance?integratorId=...&dstChainId=...&dstTokenAddr=...&depositWalletAddress=..."`
   - **Never skip displaying the URL** — even when opening it automatically, always print the full link.
5. **Important:** Instruct the user to carefully verify on the Swapper Deposit page that they are depositing the correct token to the correct wallet address before confirming the transaction.

## SDK integration (for developers building apps)

If the user is building an app and wants to embed the deposit widget, provide the relevant SDK code:

### Install

```bash
npm i @swapper-finance/deposit-sdk
```

### Embedded container

```typescript
import { SwapperIframe } from '@swapper-finance/deposit-sdk';

const swapper = new SwapperIframe({
  container: '#swapper-container', // or HTMLElement
  integratorId: 'your-integrator-id',
  dstChainId: '8453',
  dstTokenAddr: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  depositWalletAddress: '0x2A018F2506acaEEE2C10632514Fc5DCa9eE2c28A',
  // optional
  styles: { themeMode: 'light' },
  supportedDepositOptions: ['transferCrypto', 'depositWithCash'],
});
```

### Modal popup

```typescript
import { openSwapperModal } from '@swapper-finance/deposit-sdk';

const modal = openSwapperModal({
  integratorId: 'your-integrator-id',
  dstChainId: '8453',
  dstTokenAddr: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  depositWalletAddress: '0x2A018F2506acaEEE2C10632514Fc5DCa9eE2c28A',
  // optional
  styles: { themeMode: 'dark' },
  supportedDepositOptions: ['transferCrypto', 'depositWithCash'],
  modalStyle: { borderRadius: '16px' },
  onClose: () => console.log('Closed'),
});
```

### Raw iframe embed

```html
<iframe
  src="https://deposit.swapper.finance?integratorId=YOUR_ID&dstChainId=8453&dstTokenAddr=0x...&depositWalletAddress=0x..."
  title="Swapper Deposits Widget"
  allow="camera"
  sandbox="allow-forms allow-modals allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"
></iframe>
```

Both the `allow` and `sandbox` attributes are required for the onRamp integration to work properly.
