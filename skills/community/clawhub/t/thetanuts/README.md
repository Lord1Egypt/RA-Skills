# Thetanuts OpenClaw Skill

OpenClaw skill for trading crypto options on [Thetanuts Finance](https://thetanuts.finance) with integrated wallet management.

## For AI Agents

The agent instruction set lives in the locally installed `SKILL.md` (the file
ClawHub places next to this README). Read it from the install directory — do
not fetch it from the internet, since remote files can change after install
and ClawHub's security review only covers the published artifact.

`SKILL.md` contains the complete agent instruction set: onboarding flows,
trading workflows, strategy recommendation logic, risk-tiered decision trees,
SDK reference, contract addresses, and example conversations. Read it fully
before assisting users.

## Features

- **Wallet Management**: Create and import EVM/Solana wallets using Tether WDK
- **Balance Queries**: Check native (ETH/SOL) and token balances (USDC, WETH, cbBTC)
- **Transaction Execution**: Approve tokens and send transactions directly
- **Options Trading**: Orderbook fills, RFQ lifecycle, MM pricing, multi-strike structures (spreads, butterflies, condors)
- **Position Tracking**: Check user positions, calculate payoffs, portfolio ROI
- **Market Intelligence**: News-informed strategy recommendations with risk-tiered suggestions

## Prerequisites

- [OpenClaw](https://docs.openclaw.ai/) installed and running
- Node.js >= 18.0.0

## Installation

### Option A: Install from ClawHub (recommended)

```bash
clawhub install thetanuts
```

Then skip to Step 2 below.

View on ClawHub: [clawhub.ai/goheesheng/thetanuts](https://clawhub.ai/goheesheng/thetanuts)

### Option B: Clone from GitHub

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/goheesheng/thetanuts-openclaw.git thetanuts
```

### Step 2: Run Onboarding

```bash
cd ~/.openclaw/workspace/skills/thetanuts
bash scripts/onboard.sh
```

This will:
- Check prerequisites (node, npm)
- Create WDK MCP runtime at `~/.openclaw/wdk-mcp`
- Install project dependencies (for wallet scripts like `wallet-create.js`)
- Install WDK MCP runtime dependencies

### Step 3: Create or Import Wallet

```bash
# Create new dedicated wallet
node scripts/wallet-create.js

# Or import existing seed
node scripts/wallet-import.js --seed-file /path/to/seed.txt
```

**⚠️ IMPORTANT**: Use a DEDICATED wallet for this integration. Never reuse your primary wallet seed phrase. Write your seed phrase on paper and store it offline (not in a text file, not in a chat, not in email).

### Step 4: Reload OpenClaw

Start a new session to load the skill:
```
/new
```

The agent will automatically detect your wallet, show your address and balances, and display current ETH/BTC option prices. You're ready to trade.

### Step 5: Fund Your Wallet

Before trading, you need tokens on Base network:

- **ETH** (gas fees) - Bridge via [bridge.base.org](https://bridge.base.org)
- **USDC** (for PUT options) - `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **WETH** (for CALL options) - `0x4200000000000000000000000000000000000006`

Once funded, just tell the agent what you want: "Show me ETH puts" or "Recommend a strategy."

## Updates

Check for and apply skill updates:

```bash
bash scripts/update.sh
```

Optional flags:
- `REFRESH_WDK_DEPS=1` - Refresh dependencies from lockfile
- `UPGRADE_WDK_DEPS=1` - Upgrade dependency versions

**Note**: Updates NEVER modify wallet secrets (`.env`, `WDK_SEED`).

## Usage

Once installed, you can ask questions like:

- "Create a new EVM wallet for me"
- "Check my wallet balance"
- "Show me ETH put options"
- "I want to buy 0.1 ETH 2000 put expiring March 28"
- "Check positions for 0x..."

**Seed handling**: The skill reads your seed only from the `WDK_SEED` value in
`~/.openclaw/wdk-mcp/.env` (written there once by `wallet-create.js` or
`wallet-import.js`). The scripts intentionally refuse to accept a seed phrase
as a command-line argument — argv is visible to other processes via `ps`,
shell history, and terminal logs, so any script that requires the seed loads
it from the environment instead.

## Wallet Management

The skill uses a centralized wallet stored in `~/.openclaw/wdk-mcp/.env`. This enables deterministic wallet operations without passing seed phrases in commands.

### Wallet Scripts

| Script | Description |
|--------|-------------|
| `wallet-discover.js` | Check if wallet is configured, show addresses |
| `wallet-create.js` | Generate new BIP-39 seed and configure |
| `wallet-import.js` | Import existing seed from file or stdin |
| `wallet-select.js` | Set active wallet context (family, chain, index) |
| `wallet-balance.js` | Query balances with chain-specific RPC |

### Discover Wallet

```bash
node scripts/wallet-discover.js
```

### Create Wallet

```bash
node scripts/wallet-create.js
```

### Import Wallet

```bash
# From file
node scripts/wallet-import.js --seed-file /path/to/seed.txt

# From stdin
printf '%s' "$SEED" | node scripts/wallet-import.js --stdin
```

### Select Wallet Context

```bash
node scripts/wallet-select.js --family evm --chain base-mainnet --index 0
```

### Check Balance

```bash
# Native balance
node scripts/wallet-balance.js --chain base-mainnet --index 0

# With token balance
node scripts/wallet-balance.js --chain base-mainnet --index 0 --tokens 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
```

## Supported Chains

| Chain Slug | Family | Symbol | Chain ID |
|------------|--------|--------|----------|
| `ethereum-mainnet` | evm | ETH | 1 |
| `base-mainnet` | evm | ETH | 8453 |
| `bnb-smart-chain` | evm | BNB | 56 |
| `solana-mainnet` | solana | SOL | - |

## Legacy Wallet Scripts

The following TypeScript-based commands are available for backward compatibility:

| Script | Description |
|--------|-------------|
| `create-wallet.ts` | Create new EVM or Solana wallet |
| `import-wallet.ts` | Import existing wallet from seed phrase |
| `get-balance.ts` | Get native and token balances |
| `sign-message.ts` | Sign messages for authentication |
| `approve-token.ts` | Approve ERC20 token spending |
| `send-transaction.ts` | Sign and broadcast transactions |

### Approve Token Spending

Approval scripts read the seed from the `WDK_SEED` environment variable
(loaded from `~/.openclaw/wdk-mcp/.env`). Passing a seed phrase as a CLI
argument is rejected at script entry — see the global seed-handling note
above.

```bash
# Approve an exact USDC amount for Thetanuts (preferred over --max)
npx tsx scripts/approve-token.ts --token 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --spender 0x1aDcD391CF15Fb699Ed29B1D394F4A64106886e5 --amount 100 --wait

# Unlimited approvals require explicit confirmation; the spender must also be
# on the Thetanuts allowlist (override with --i-understand-risk only after
# independently verifying the address).
npx tsx scripts/approve-token.ts --token 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --spender 0x1aDcD391CF15Fb699Ed29B1D394F4A64106886e5 --max --confirm-max --wait
```

### Send Transaction

```bash
npx tsx scripts/send-transaction.ts --to 0x1aDcD391CF15Fb699Ed29B1D394F4A64106886e5 --data 0xb5da63e3... --wait
```

## Trading Scripts

| Script | Description |
|--------|-------------|
| `get-prices.ts` | Get current BTC, ETH prices and protocol stats |
| `get-mm-pricing.ts` | Get MM option pricing with filters |
| `get-positions.ts` | Get user positions by wallet address |
| `build-rfq.ts` | Build RFQ transaction data |
| `fetch-orders.ts` | Fetch orderbook with filters |
| `check-orderbook.ts` | Check orderbook liquidity before trading |
| `fill-order.ts` | Fill an existing orderbook order |
| `check-rfq-fill.ts` | Verify RFQ fill status after submission |
| `calculate-payout.ts` | Calculate option payout at settlement |

### Get Option Pricing

```bash
npx tsx scripts/get-mm-pricing.ts ETH --type PUT
```

### Build RFQ

```bash
npx tsx scripts/build-rfq.ts --underlying ETH --type PUT --strike 2000 --expiry 1774684800 --contracts 0.1 --direction buy
```

## Complete Trading Workflow

1. **Create wallet** (or import existing):
   ```bash
   node scripts/wallet-create.js
   ```

2. **Check balance**:
   ```bash
   node scripts/wallet-balance.js --chain base-mainnet --tokens 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
   ```

3. **Approve USDC** for Thetanuts (one-time per token; prefer an exact amount):
   ```bash
   npx tsx scripts/approve-token.ts --token 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --spender 0x1aDcD391CF15Fb699Ed29B1D394F4A64106886e5 --amount 100 --wait
   ```

4. **Check orderbook first** (always check liquidity before choosing a method):
   ```bash
   npx tsx scripts/check-orderbook.ts --underlying ETH --type PUT --strike 1900 --expiry 1774684800 --direction sell
   ```

5a. **If orderbook has liquidity** - fill directly:
   ```bash
   npx tsx scripts/fill-order.ts --order-index 0 --collateral 10 --execute --wait
   ```

5b. **If no orderbook liquidity** - submit an RFQ:
   ```bash
   npx tsx scripts/build-rfq.ts --underlying ETH --type PUT --strike 1900 --expiry 1774684800 --contracts 0.1 --direction buy
   npx tsx scripts/send-transaction.ts --to <from-build-rfq> --data <from-build-rfq> --wait
   ```

6. **Verify fill** (for RFQ trades):
   ```bash
   npx tsx scripts/check-rfq-fill.ts --address <wallet> --ticker <expected> --since <submission_timestamp>
   ```

## Configuration

```bash
# EVM RPC (default: Base Mainnet)
export THETANUTS_RPC_URL="https://mainnet.base.org"

# Solana RPC (default: Mainnet)
export SOLANA_RPC_URL="https://api.mainnet-beta.solana.com"
```

## Contract Addresses (Base)

| Contract | Address |
|----------|---------|
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| WETH | `0x4200000000000000000000000000000000000006` |
| cbBTC | `0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf` |
| Thetanuts RFQ | `0x1aDcD391CF15Fb699Ed29B1D394F4A64106886e5` |

## Security Considerations

- **SEED PHRASES**: Save securely, never share. Scripts display seed only during creation.
- **KEY DISPOSAL**: Wallet scripts automatically clear keys from memory after use.
- **TRANSACTIONS**: Transactions are IRREVERSIBLE once broadcast. Verify before sending.
- **APPROVALS**: Token approvals allow contracts to spend your tokens. Only approve trusted contracts.
- **GAS**: Ensure wallet has ETH on Base network for gas fees.

## License

MIT

## Links

- [ClawHub: thetanuts](https://clawhub.ai/goheesheng/thetanuts)
- [Thetanuts Finance](https://thetanuts.finance)
- [Thetanuts SDK](https://github.com/Thetanuts-Finance/thetanuts-sdk)
- [Tether WDK](https://docs.wdk.tether.io)
- [OpenClaw Docs](https://docs.openclaw.ai/)
