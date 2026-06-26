# DeFi & Trading Cookbook

Step-by-step recipes for your trading and DeFi operations.

You have three **built-in trading engines** that handle signing, approval, and execution automatically. For other protocols, use the universal `exec` command with ABI encoding.

## Table of Contents

1. [DEX Swap (0x Aggregator)](#dex-swap)
2. [Hyperliquid Perpetual Futures & Spot](#hyperliquid)
3. [Bridge to Hyperliquid](#bridge-to-hyperliquid) — Deposit USDC from HyperEVM to HL L1 for trading
4. [EOA Transactions on HyperEVM](#eoa-transactions-on-hyperevm) — Direct EOA operations on Hyperliquid's EVM chain
5. [Fund EOA for Polymarket](#fund-eoa-for-polymarket) — Get POL + USDC.e on Polygon for Polymarket trading
6. [Polymarket Prediction Markets](#polymarket)
7. [Custom Contract Interactions](#custom-contracts) — AAVE, Compound, and any other protocol via `exec`
8. [Trading Strategies](#trading-strategies) — Copy trading, Polymarket arbitrage, high-probability bonds, AI probability modeling
8. [Common Patterns & Safety](#tips)

---

## DEX Swap

`tigerpass swap` uses the **0x aggregator** to find the best price across all DEXes — Uniswap V3, SushiSwap, Curve, Balancer, and dozens more. One command does everything: quote, approve, and execute.

**Important**: Native token (ETH) is not supported as the sell token by 0x. Use **WETH** instead. Buying native ETH is supported.

### Basic Swap

```bash
# Swap 100 USDC → WETH on Base (default chain)
tigerpass swap --from USDC --to WETH --amount 100

# Swap on a different chain
tigerpass swap --from USDC --to WETH --amount 100 --chain ETHEREUM

# Use contract address for unlisted tokens
tigerpass swap --from 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --to WETH --amount 100
```

### Controlling Slippage

```bash
# Tight slippage (0.5% = 50 bps)
tigerpass swap --from USDC --to WETH --amount 100 --slippage 50

# Default is 1% (100 bps) — suitable for most pairs
```

### Don't Wait for Confirmation

```bash
# Submit and return immediately (useful for batch workflows)
tigerpass swap --from USDC --to WETH --amount 100 --no-wait
```

### Dry-Run (Preview Quote)

```bash
# Get quote without executing — see expected output, fees, slippage
tigerpass swap --from USDC --to WETH --amount 100 --simulate
```

### Verify Before and After

```bash
# 1. Check input balance
tigerpass balance --token USDC

# 2. Preview the swap
tigerpass swap --from USDC --to WETH --amount 100 --simulate

# 3. Execute swap
tigerpass swap --from USDC --to WETH --amount 100

# 4. Verify output received
tigerpass balance --token WETH
```

### Output Format

```json
{
  "status": "confirmed",
  "from": "USDC",
  "to": "WETH",
  "sellAmount": "100",
  "buyAmount": "0.0333...",
  "sellToken": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "buyToken": "0x4200000000000000000000000000000000000006",
  "chain": "BASE",
  "feeBps": 15,
  "txHash": "0x...",
  "fromAddress": "0x...",
  "explorer": "https://basescan.org/tx/0x..."
}
```

**Key output fields**: `status` is `"confirmed"` or `"submitted"` (if `--no-wait`). `txHash` is the transaction hash. `fromAddress` is your EOA. `feeBps` is 15 (0.15% integrator fee). `error` field appears on failure.

### Swap Limitations

- **Sell token must be ERC-20** — use WETH instead of native ETH
- **0x does not support testnets** — `swap` is unavailable in test environment
- **Not available on HyperEVM** — 0x does not support HyperEVM; swap works on all other EVM chains

---

## Hyperliquid

`tigerpass hl` trades **perpetual futures** and **spot tokens** on Hyperliquid — the highest-volume perp DEX. All signing, encoding, and builder fee attachment are handled automatically. Add `--spot` to any command to switch from perps (default) to spot trading.

### Setup (Once)

Bridge USDC to HyperEVM and deposit to L1 — see [Bridge to Hyperliquid](#bridge-to-hyperliquid). Builder fee is auto-approved on first order; no separate setup needed.

### Trading Workflow

```bash
# 1. Check available balance (L1, NOT HyperEVM!)
tigerpass hl info --type balances

# 2. Check current mid prices
tigerpass hl info --type mids

# 3. Place a limit buy order
tigerpass hl order --coin BTC --side buy --price 95000 --size 0.01

# 4. Check order status
tigerpass hl info --type orders

# 5. Check position
tigerpass hl info --type positions
```

### Spot Trading

Add `--spot` to switch to spot market. Spot trades buy/sell actual tokens (not derivatives).

```bash
# Buy 10 HYPE at $25
tigerpass hl order --spot --coin HYPE --side buy --price 25 --size 10

# Sell 5 HYPE at $30
tigerpass hl order --spot --coin HYPE --side sell --price 30 --size 5

# Check spot balances (total, hold/frozen in orders, entry value)
tigerpass hl info --spot --type balances

# Check open spot orders
tigerpass hl info --spot --type orders

# Cancel all spot orders
tigerpass hl cancel --spot --all

# Cancel spot order for specific coin
tigerpass hl cancel --spot --coin HYPE --oid 12345
```

### Order Types

```bash
# GTC — Good 'til Cancelled (default)
tigerpass hl order --coin BTC --side buy --price 95000 --size 0.01

# IOC — Immediate or Cancel (fill or kill)
tigerpass hl order --coin ETH --side buy --price 3200 --size 1.0 --type ioc

# ALO — Add Liquidity Only (maker only, no taker fills)
tigerpass hl order --coin BTC --side sell --price 100000 --size 0.01 --type alo

# Reduce-only (close position, never open new — perps only)
tigerpass hl order --coin BTC --side sell --price 100000 --size 0.01 --reduce-only
```

### Cancel Orders

```bash
# Cancel a specific order by OID
tigerpass hl cancel --coin BTC --oid 12345

# Cancel all orders for one coin
tigerpass hl cancel --all --coin BTC

# Cancel everything
tigerpass hl cancel --all

# Spot cancel examples
tigerpass hl cancel --spot --coin HYPE --oid 67890
tigerpass hl cancel --spot --all
```

### Account Queries

```bash
# --- Perpetual Futures ---
# Positions — coin, size, entry price, PnL, liquidation price, leverage
tigerpass hl info --type positions

# Open orders — coin, side, price, size, OID
tigerpass hl info --type orders

# Balance — account value, margin used, withdrawable
tigerpass hl info --type balances

# All mid prices — every listed asset
tigerpass hl info --type mids

# --- Spot ---
# Spot token balances (total, hold/frozen, entry value)
tigerpass hl info --spot --type balances

# Open spot orders
tigerpass hl info --spot --type orders
```

### Position Output Example

```json
{
  "positions": [
    {
      "coin": "BTC",
      "szi": "0.01",
      "entryPx": "95000.0",
      "unrealizedPnl": "50.00",
      "liquidationPx": "80000.0",
      "leverage": { "type": "cross", "value": 10 }
    }
  ]
}
```

### Builder Fees

Fees are automatically attached to every order:

| Market | Fee | Rate |
|--------|-----|------|
| Perpetual futures | `hyperliquidBuilderFee` | 5bp (0.05%) |
| Spot | `hyperliquidSpotBuilderFee` | 50bp (0.5%) |

Auto-authorized on first order — no separate setup needed.

---

## Bridge to Hyperliquid

To trade on Hyperliquid (perps or spot), you need USDC deposited into the **Hyperliquid L1 trading layer**. The L1 is separate from HyperEVM — think of it as: HyperEVM is the on-chain EVM, while L1 is the off-chain order book where trading happens.

**Two-step funding**: (1) Bridge USDC to HyperEVM via `tigerpass bridge --to HYPEREVM` (see `references/advanced-commands.md` "Cross-Chain USDC Bridge" section), then (2) deposit from HyperEVM to L1 using the CoreDepositWallet contract below.

The bridge flow deposits USDC from HyperEVM into the L1 trading account via the **CoreDepositWallet** contract.

### Architecture

```
HyperEVM (chain 999)          Hyperliquid L1 (trading)
┌──────────────────┐          ┌──────────────────────┐
│  EOA holds USDC  │──bridge──│  USDC trading balance │
│  + HYPE for gas  │          │  (perps + spot)       │
└──────────────────┘          └──────────────────────┘
      ↑ approve + deposit           ↓ trade
      │ via CoreDepositWallet       │ via tigerpass hl
```

### Contract Addresses

| Contract | Testnet (998) | Mainnet (999) |
|----------|--------------|---------------|
| CoreDepositWallet | `0x0b80659a4076e9e93c7dbe0f10675a16a3e5c206` | `0x6b9e773128f453f5c2c60935ee2de2cbc5390a24` |
| Native USDC | `0x2B3370eE501B4a559b57D449569354196457D8Ab` | `0xb88339CB7199b77E23DB6E890353E22632Ba630f` |

### Deposit Function

```solidity
CoreDepositWallet.deposit(uint256 amount, uint32 destinationDex)
```

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `amount` | USDC in 6 decimals (e.g., `10000000` = 10 USDC) | How much to deposit |
| `destinationDex` | `0` | Deposit to **perps** margin |
| `destinationDex` | `4294967295` (uint32 max) | Deposit to **spot** balance |

### How to Fund Your EOA on HyperEVM

**USDC**: Bridge autonomously from any CCTP chain via `tigerpass bridge --to HYPEREVM --amount <X>`. This mints USDC directly to your EOA on HyperEVM.

**HYPE (gas)**: Cannot be bridged autonomously. The user must fund the EOA externally:

1. **Get the EOA address**: `tigerpass init` — give this address to the user
2. **User sends HYPE** to the EOA address on HyperEVM via:
   - Hyperliquid UI (spot withdraw to HyperEVM)
   - Direct transfer from another HyperEVM wallet

Once the EOA has HYPE (gas) and USDC, you can operate autonomously on HyperEVM.

### Full Bridge Workflow (HyperEVM → HyperCore L1)

**Prerequisites**: EOA must have HYPE (gas) and USDC on HyperEVM. In test environment, the CLI auto-resolves `--chain HYPEREVM` to HyperEVM testnet (chain 998).

```bash
# 1. Get your EOA address
tigerpass init

# 2. Verify you have HYPE for gas and USDC on HyperEVM
tigerpass balance --chain HYPEREVM
tigerpass balance --token USDC --chain HYPEREVM

# 3. Approve USDC for CoreDepositWallet
#    Testnet: 0x0b80659a4076e9e93c7dbe0f10675a16a3e5c206
#    Mainnet: 0x6b9e773128f453f5c2c60935ee2de2cbc5390a24
tigerpass approve \
  --token USDC \
  --spender 0x6b9e773128f453f5c2c60935ee2de2cbc5390a24 \
  --amount 100 \
  --chain HYPEREVM

# 4. Verify approval (approve without --amount queries current allowance)
tigerpass approve \
  --token USDC \
  --spender 0x6b9e773128f453f5c2c60935ee2de2cbc5390a24 \
  --chain HYPEREVM

# 5. Deposit 100 USDC to HyperCore perps margin
#    amount = 100_000_000 (100 USDC × 10^6 decimals)
#    destinationDex = 0 (perps)
tigerpass exec \
  --to 0x6b9e773128f453f5c2c60935ee2de2cbc5390a24 \
  --fn "deposit(uint256,uint32)" \
  --fn-args '["100000000","0"]' \
  --chain HYPEREVM

# 6. Wait ~30s for the deposit to settle on L1, then verify
tigerpass hl info --type balances
```

**Deposit to spot** (for spot trading):

```bash
# destinationDex = 4294967295 (uint32 max → spot balance)
tigerpass exec \
  --to 0x6b9e773128f453f5c2c60935ee2de2cbc5390a24 \
  --fn "deposit(uint256,uint32)" \
  --fn-args '["100000000","4294967295"]' \
  --chain HYPEREVM
```

### Simulate Before Depositing

For large deposits, use `--simulate` to dry-run the transaction before real execution:

```bash
tigerpass exec \
  --to 0x6b9e773128f453f5c2c60935ee2de2cbc5390a24 \
  --fn "deposit(uint256,uint32)" \
  --fn-args '["100000000","0"]' \
  --chain HYPEREVM --simulate
```

Simulation runs `eth_call` and returns `{"simulated": true, "success": true/false, ...}` without signing or paying gas.

### Withdraw (HyperCore L1 → HyperEVM)

Withdrawing USDC from HyperCore back to HyperEVM uses the Hyperliquid exchange API's `spotSend` action — send to the system address `0x2000000000000000000000000000000000000000`. The protocol automatically credits your HyperEVM EOA.

**This is not yet a CLI command.** The user must withdraw via the Hyperliquid UI for now. The `withdrawable` field in `tigerpass hl info --type balances` shows how much can be withdrawn.

### Approve Max (One-Time)

For repeated deposits, approve unlimited USDC once:

```bash
tigerpass approve \
  --token USDC \
  --spender 0x6b9e773128f453f5c2c60935ee2de2cbc5390a24 \
  --amount max \
  --chain HYPEREVM
```

### End-to-End: From Zero to First Hyperliquid Trade

```bash
# === One-time setup ===

# 1. Initialize
tigerpass init

# 2. Tell the user your EOA address — they need to send HYPE (gas) to it on HyperEVM

# 3. Bridge USDC from Base → HyperEVM (autonomous — no user action needed)
tigerpass bridge --to HYPEREVM --amount 100

# 4. Verify funding arrived
tigerpass balance --chain HYPEREVM                   # HYPE for gas (user-provided)
tigerpass balance --token USDC --chain HYPEREVM      # USDC (from bridge)

# 5. Deposit USDC from HyperEVM → HyperCore L1 (perps margin)
tigerpass approve --token USDC --spender 0x6b9e773128f453f5c2c60935ee2de2cbc5390a24 --amount max --chain HYPEREVM
tigerpass exec --to 0x6b9e773128f453f5c2c60935ee2de2cbc5390a24 --fn "deposit(uint256,uint32)" --fn-args '["100000000","0"]' --chain HYPEREVM

# === Ready to trade ===

# 6. Check balance on L1 (NOT HyperEVM balance!)
tigerpass hl info --type balances

# 7. Place your first order (builder fee auto-approved on first order)
tigerpass hl order --coin BTC --side buy --price 95000 --size 0.01
```

### Important Notes

- `deposit(amount, destinationDex)` takes the **exact amount in atomic units** (6 decimals) — `10000000` = 10 USDC
- `destinationDex=0` → perps margin, `destinationDex=4294967295` → spot balance
- Gas on HyperEVM is paid in HYPE — ensure your EOA has HYPE before any HyperEVM transaction
- Deposits typically settle within 30 seconds on L1
- **Do NOT confuse** `tigerpass balance --chain HYPEREVM` (HyperEVM on-chain) with `tigerpass hl info --type balances` (L1 trading) — they are different pools
- Withdraw (L1 → HyperEVM) is not yet a CLI command — use the Hyperliquid UI

---

## EOA Transactions on HyperEVM

HyperEVM is Hyperliquid's native EVM chain (chain ID 999 mainnet, 998 testnet). All TigerPass chains use EOA, but HyperEVM has unique characteristics worth noting.

### HyperEVM Specifics

- **Native token is HYPE** (not ETH) — gas is paid in HYPE
- **No 0x support** — `tigerpass swap` is not available on HyperEVM
- **No 0x DEX aggregator** — use Hyperliquid spot trading instead
- **Batch exec is sequential** — each call is a separate transaction (non-atomic), same as all other chains

### Transfer on HyperEVM

```bash
# Send HYPE (native token)
tigerpass pay --to 0xRecipient --amount 0.1 --token HYPE --chain HYPEREVM

# Send USDC
tigerpass pay --to 0xRecipient --amount 10 --token USDC --chain HYPEREVM
```

### Approve on HyperEVM

```bash
# Approve a spender
tigerpass approve --token USDC --spender 0xContract --amount 100 --chain HYPEREVM

# Unlimited approval
tigerpass approve --token USDC --spender 0xContract --amount max --chain HYPEREVM
```

### Execute Contracts on HyperEVM

```bash
# Single call with ABI encoding
tigerpass exec --to 0xContract \
  --fn "someFunction(address,uint256)" \
  --fn-args '["0xAddr","1000000"]' \
  --chain HYPEREVM

# Single call with raw calldata
tigerpass exec --to 0xContract --data 0xa9059cbb... --chain HYPEREVM

# Simulate before executing (dry-run via eth_call)
tigerpass exec --to 0xContract \
  --fn "riskyFunction(uint256)" \
  --fn-args '["1000"]' \
  --chain HYPEREVM --simulate

# Batch calls (executed sequentially — NOT atomic! Max 10 calls.)
tigerpass exec --calls '[
  {"to":"0xA","value":"0x0","data":"0x..."},
  {"to":"0xB","value":"0x0","data":"0x..."}
]' --chain HYPEREVM
```

**Batch note**: On HyperEVM, batch `exec --calls` is sequential — each call is a separate transaction. If call 2 fails, call 1 has already executed and cannot be rolled back. Output includes `batchTxHashes` array with individual transaction hashes and a `warning` field.

### Read-Only Operations

These work identically to other EVM chains — no gas needed:

```bash
# Balance
tigerpass balance --chain HYPEREVM
tigerpass balance --token USDC --chain HYPEREVM
tigerpass balance --address 0xAny --chain HYPEREVM

# Read contract
tigerpass call --to 0xContract --fn "balanceOf(address)" --fn-args '["0xAddr"]' --chain HYPEREVM

# Token info
tigerpass token-info --token USDC --chain HYPEREVM

```

---

## Fund EOA for Polymarket

Polymarket uses **EOA** on Polygon (`sigType=0`).

EOA on Polygon needs:
- **POL** — gas
- **USDC.e** (`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`) — collateral

| Token | Address | Polymarket |
|-------|---------|------------|
| **USDC.e** (bridged) | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` | YES |
| USDC (native) | `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359` | NO — swap first |

### Option A: Transfer from Your EVM Wallet on Polygon

```bash
# 1. Check your balance on Polygon
tigerpass balance --chain POLYGON

# 2. Send POL for gas (if transferring to a different address)
tigerpass pay --to <recipient> --amount 0.5 --token POL --chain POLYGON

# 3a. If you have USDC.e — send directly
tigerpass pay --to <recipient> --amount 100 --token 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174 --chain POLYGON

# 3b. If you only have native USDC — swap then send
tigerpass swap --from USDC --to 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174 --amount 100 --chain POLYGON
tigerpass pay --to <recipient> --amount 100 --token 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174 --chain POLYGON
```

### Option B: User Funds EOA Externally

`tigerpass init` to get EOA address. User sends POL + USDC.e via CEX / bridge / direct transfer.

### Verify Funding

```bash
tigerpass balance --address <eoaAddr> --chain POLYGON                                                        # POL
tigerpass balance --address <eoaAddr> --token 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174 --chain POLYGON     # USDC.e
```

### End-to-End: Zero to First Polymarket Trade

```bash
# 1. Init
tigerpass init

# 2. Fund EOA on Polygon
tigerpass pay --to <eoaAddr> --amount 0.5 --token POL --chain POLYGON
tigerpass swap --from USDC --to 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174 --amount 100 --chain POLYGON
tigerpass pay --to <eoaAddr> --amount 100 --token 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174 --chain POLYGON

# 3. Approve all 6 Polymarket contracts (one-time, requires POL for gas)
tigerpass pm approve

# 4. Trade
tigerpass pm info --type balances
tigerpass pm order --market <conditionId> --outcome YES --side buy --amount 100 --price 0.55
```

---

## Polymarket

`tigerpass pm` trades prediction market outcome tokens on Polymarket. **EOA-only** (Polygon mainnet), uses **USDC.e** as collateral.

Ensure EOA has POL + USDC.e before trading — see [Fund EOA for Polymarket](#fund-eoa-for-polymarket).

### Setup (Once)

```bash
# Approve all 6 Polymarket contracts (3x ERC-20 USDC.e + 3x ERC-1155 Conditional Tokens)
# Without this: you can buy but CANNOT sell or redeem outcome tokens
# Requires POL in EOA for gas (6 sequential EOA transactions on Polygon)
tigerpass pm approve
tigerpass pm approve --no-wait    # don't wait for confirmation
```

Approvals:
1. USDC.e → CTF Exchange (ERC-20 unlimited)
2. USDC.e → Neg Risk CTF Exchange (ERC-20 unlimited)
3. USDC.e → Neg Risk Adapter (ERC-20 unlimited)
4. Conditional Tokens → CTF Exchange (ERC-1155 setApprovalForAll)
5. Conditional Tokens → Neg Risk CTF Exchange (ERC-1155 setApprovalForAll)
6. Conditional Tokens → Neg Risk Adapter (ERC-1155 setApprovalForAll)

### Trading Workflow

```bash
# 1. Browse available markets
tigerpass pm info --type markets

# 2. Check USDC.e balance on Polymarket
tigerpass pm info --type balances

# 3. Buy YES tokens at 55 cents ($100 worth)
tigerpass pm order --market <conditionId> --outcome YES --side buy --amount 100 --price 0.55

# 4. Check your position
tigerpass pm info --type positions

# 5. Check open orders
tigerpass pm info --type orders
```

### Order Types

```bash
# GTC — Good 'til Cancelled (default)
tigerpass pm order --market <cid> --outcome YES --side buy --amount 100 --price 0.55

# FOK — Fill or Kill (entire amount or nothing)
tigerpass pm order --market <cid> --outcome YES --side buy --amount 100 --price 0.55 --type FOK

# If you already have the token ID (skip market + outcome lookup)
tigerpass pm order --token-id <tokenId> --side buy --amount 100 --price 0.55

# Neg-risk market (multi-outcome events)
tigerpass pm order --market <cid> --outcome YES --side buy --amount 100 --price 0.55 --neg-risk
```

### Cancel Orders

```bash
# Cancel a specific order
tigerpass pm cancel --order-id 0xOrderId...

# Cancel all open orders
tigerpass pm cancel --all
```

### Account Queries

```bash
# Markets — question, conditionId, token prices, active/closed
tigerpass pm info --type markets

# Positions — asset, size, avg price, current price, PnL
tigerpass pm info --type positions

# Balance — USDC available on Polymarket
tigerpass pm info --type balances

# Trade history — id, side, size, price, outcome, status, txHash
tigerpass pm info --type trades

# Open orders — id, side, price, size, matched amount, outcome
tigerpass pm info --type orders
```

---

## Custom Contract Interactions

For any DeFi protocol that doesn't have a built-in command (Uniswap, AAVE, Compound, Curve, etc.), use `tigerpass exec` with ABI encoding. The `--fn` flag is preferred because it's self-documenting and encoding is handled automatically.

### Universal Pattern

Almost every DeFi interaction follows this flow:

```bash
# 1. Check you have the input token
tigerpass balance --token USDC

# 2. Approve the protocol to spend your tokens (skip for native ETH)
tigerpass approve --token USDC --spender <PROTOCOL_ROUTER> --amount max

# 3. Verify approval (approve without --amount queries current allowance)
tigerpass approve --token USDC --spender <PROTOCOL_ROUTER>

# 4. Simulate the operation first (dry-run, no gas spent)
tigerpass exec --to <PROTOCOL_ROUTER> \
  --fn "<function_signature>" \
  --fn-args '[...]' --simulate

# 5. Execute the DeFi operation
tigerpass exec --to <PROTOCOL_ROUTER> \
  --fn "<function_signature>" \
  --fn-args '[...]'

# 6. Verify the result
tigerpass balance --token WETH
```

### Example: AAVE V3 — Supply & Borrow

```bash
# AAVE V3 Pool on Base: 0xA238Dd80C259a72e81d7e4664a9801593F98d1c5

# Supply 1000 USDC
tigerpass approve --token USDC --spender 0xA238Dd80C259a72e81d7e4664a9801593F98d1c5 --amount 1000
tigerpass exec --to 0xA238Dd80C259a72e81d7e4664a9801593F98d1c5 \
  --fn "supply(address,uint256,address,uint16)" \
  --fn-args '["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913","1000000000","<YOUR_ADDRESS>","0"]'

# Borrow 0.1 WETH (variable rate = 2)
tigerpass exec --to 0xA238Dd80C259a72e81d7e4664a9801593F98d1c5 \
  --fn "borrow(address,uint256,uint256,uint16,address)" \
  --fn-args '["0x4200000000000000000000000000000000000006","100000000000000000","2","0","<YOUR_ADDRESS>"]'

# Check health factor
tigerpass call --to 0xA238Dd80C259a72e81d7e4664a9801593F98d1c5 \
  --fn "getUserAccountData(address)" \
  --fn-args '["<YOUR_ADDRESS>"]'
```

### Batch Transactions (Approve + Action)

Batch calls are **sequential** (non-atomic) — each call is a separate transaction. If call 2 fails, call 1 has already executed and cannot be rolled back.

```bash
# Approve + swap in a batch (max 10 calls, executed sequentially)
tigerpass exec --calls '[
  {"to":"0xUSDC","value":"0x0","data":"0x095ea7b3..."},
  {"to":"0xRouter","value":"0x0","data":"0x..."}
]'
```

To generate calldata for batch transactions, use the `--fn` flag in `exec`, or construct raw hex calldata manually.

### Reading Prices

```bash
# Chainlink price feed
tigerpass call --to 0xChainlinkFeed --fn "latestRoundData()"
```

### Key Contract Addresses

**Base (chainId 8453)**
| Contract | Address |
|----------|---------|
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| WETH | `0x4200000000000000000000000000000000000006` |
| AAVE V3 Pool | `0xA238Dd80C259a72e81d7e4664a9801593F98d1c5` |

**Ethereum (chainId 1)**
| Contract | Address |
|----------|---------|
| USDC | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` |
| WETH | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` |
| AAVE V3 Pool | `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2` |

**Polygon (chainId 137)**
| Contract | Address |
|----------|---------|
| **USDC.e** (bridged — Polymarket collateral) | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` |
| USDC (native — NOT for Polymarket) | `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359` |
| Polymarket CTF Exchange | `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E` |
| Polymarket NegRisk Exchange | `0xC5d563A36AE78145C45a50134d48A1215220f80a` |

**Hyperliquid HyperEVM (chainId 999)**
| Contract | Address |
|----------|---------|
| Native USDC | `0xb88339CB7199b77E23DB6E890353E22632Ba630f` |
| USDT | `0x10982ad645D5A112606534d8567418Cf64c14cB5` |
| CoreDepositWallet | `0x6b9e773128f453f5c2c60935ee2de2cbc5390a24` |
| HYPE (native) | `0x2222222222222222222222222222222222222222` (system) |

> Contract addresses change over time. Always verify via official protocol docs before real-money transactions.

---

## Tips

### Amount Conversions

Token amounts in `exec` are always in the smallest unit (atomic):
- ETH: 18 decimals → 1 ETH = 1000000000000000000 (1e18)
- USDC: 6 decimals → 1 USDC = 1000000 (1e6)
- WBTC: 8 decimals → 1 WBTC = 100000000 (1e8)

The `swap`, `pay`, and `hl order` commands handle this automatically (human-readable input). The `exec` command works with raw atomic values. Use `tigerpass token-info --token X` to check decimals.

### Safety Checklist

1. **Check balance first** — `tigerpass balance --token X` before any operation
2. **Check the right pool** — HyperEVM balance ≠ HL L1 balance ≠ EVM wallet balance ≠ Polymarket EOA balance (see SKILL.md balance pools diagram)
3. **Use `--simulate`** for complex `exec` transactions — dry-run before real execution
4. **Verify allowance** — `tigerpass approve --token X --spender 0x...` (omit --amount) to query, before the main transaction
6. **Check tx status** — `tigerpass tx --hash 0x... --wait` for confirmation

### When to Use Which

| Want to... | Use | Chain/Address |
|-----------|-----|--------------|
| Swap tokens on any DEX | `tigerpass swap` (automatic routing, best price) | EVM / evmAddress |
| Trade perpetual futures | `tigerpass hl order` (Hyperliquid) | HL L1 / eoaAddress |
| Trade spot tokens on HL | `tigerpass hl order --spot` (Hyperliquid spot) | HL L1 / eoaAddress |
| Bridge USDC cross-chain | `tigerpass bridge --from X --to Y` (Circle CCTP V2, 5 chains) | EVM / evmAddress |
| Deposit USDC for HL trading | (1) `tigerpass bridge --to HYPEREVM` then (2) `approve` + `exec` on HyperEVM | EVM → HyperEVM / eoaAddress |
| Bet on events/elections | `tigerpass pm order` (Polymarket, Polygon mainnet, EOA + USDC.e) | Polygon / eoaAddress |
| Transfer EVM tokens | `tigerpass pay --to 0x... --amount X` | EVM / evmAddress |
| Transfer on HyperEVM | `tigerpass pay --chain HYPEREVM` (EOA direct) | HyperEVM / eoaAddress |
| Execute on HyperEVM | `tigerpass exec --chain HYPEREVM` (EOA direct) | HyperEVM / eoaAddress |
| Supply/borrow on lending protocols | `tigerpass exec` with AAVE/Compound ABI | EVM / evmAddress |
| Interact with any EVM contract | `tigerpass exec --fn` or `--data` | EVM / evmAddress |
| Read EVM on-chain state (no gas) | `tigerpass call --fn` | EVM |

---

## Trading Strategies

Real-world strategies you can build with TigerPass. These are patterns — adapt them to your risk tolerance and market conditions.

### Copy Trading Strategy (Hyperliquid)

Mirror trades from profitable Hyperliquid wallets. The top 20% of HL traders consistently outperform — following their positions (with proper sizing) is one of the most accessible strategies.

**How it works:**

1. **Identify whales** — use on-chain tools (HyperTracker, CoinGlass, Hyperbot) or Hyperliquid's public API to find wallets with strong PnL track records
2. **Monitor position changes** — detect when a whale opens, increases, or closes a position
3. **Evaluate before executing** — the AI analyzes whether the trade makes sense (market conditions, whale's historical accuracy, current volatility)
4. **Execute with proportional sizing** — never match whale size 1:1

```bash
# === Copy trading workflow ===

# 1. Check your available margin
tigerpass hl info --type balances

# 2. Get current prices for the asset
tigerpass hl info --type mids

# 3. Whale opened 10 BTC long at $95,000 — you follow with 1% of whale size
tigerpass hl order --coin BTC --side buy --price 95100 --size 0.1

# 4. IMMEDIATELY set a reduce-only exit (stop-loss)
tigerpass hl order --coin BTC --side sell --price 92000 --size 0.1 --reduce-only

# 5. Monitor position
tigerpass hl info --type positions

# 6. When whale exits, you exit too
tigerpass hl order --coin BTC --side sell --price 97000 --size 0.1 --reduce-only
```

**Risk management rules:**
- **Position sizing**: never risk more than 2-5% of your trading balance per trade
- **Always set stop-loss**: place a reduce-only order immediately after entry
- **Latency matters**: whale tracking data has delay — the whale may have already moved. Check `tigerpass hl info --type mids` before placing your order
- **Don't stack correlated positions**: if the whale is long BTC, ETH, and SOL, that's one directional bet, not three independent trades
- **Exit discipline**: if the whale exits and you don't detect it in time, set a time-based exit — don't hold orphaned positions

### Polymarket Arbitrage Strategy

Only 7.6% of Polymarket wallets are profitable. Systematic strategies beat gut feelings. Here are the three main approaches:

#### Strategy 1: Single-Market Rebalancing

When YES + NO prices sum to less than $1.00, buy both for a guaranteed profit at resolution.

```bash
# 1. Scan all markets
tigerpass pm info --type markets

# 2. For each market, calculate: YES_price + NO_price
#    If sum < $0.97, there's a potential 3%+ arbitrage (after 2% Polymarket fee)

# 3. Example: YES = $0.45, NO = $0.52, sum = $0.97
#    Buy both:
tigerpass pm order --market <conditionId> --outcome YES --side buy --amount 100 --price 0.45
tigerpass pm order --market <conditionId> --outcome NO --side buy --amount 100 --price 0.52

# 4. At resolution, one side pays $1.00
#    Cost: $0.97 → Payout: $1.00 → Gross profit: 3.1%
#    After 2% fee on winner: net ~1% profit (risk-free)

# 5. Monitor positions
tigerpass pm info --type positions
```

**Reality check**: Simple arb windows in 2026 last ~2.7 seconds on average. This strategy works best on newly listed markets or during high-volatility events when spreads widen.

#### Strategy 2: High-Probability "Bond" Strategy

Over 90% of large Polymarket orders ($10K+) target events priced above $0.95. This is essentially buying a short-term bond — the event is near-certain, and you collect the spread when it resolves.

```bash
# 1. Scan for high-probability events
tigerpass pm info --type markets
# Look for: outcome price $0.95-$0.99, resolves within days/weeks

# 2. Buy $1000 of a 97-cent outcome
tigerpass pm order --market <conditionId> --outcome YES --side buy --amount 1000 --price 0.97

# 3. If event resolves YES:
#    Payout: $1000 / 0.97 = ~1030 shares × $1.00 = $1030
#    Minus 2% fee on profit: ~$1029.40
#    Net profit: ~$29.40 (2.9% in potentially days)

# 4. Key risk: the "near-certain" event doesn't happen
#    Always assess WHY the market prices it at 97% — what's the 3% risk scenario?
```

**Best for**: events with clear, objective resolution criteria (e.g., "Will X happen before date Y?") where the outcome is highly predictable but not yet resolved.

#### Strategy 3: AI Probability Modeling (Information Arbitrage)

This is where AI agents have a genuine edge. You analyze information systematically to estimate probabilities better than the crowd, then bet when the market diverges from your estimate.

```bash
# 1. Scan markets
tigerpass pm info --type markets

# 2. For a market of interest, the AI analyzes:
#    - Recent news articles and press releases
#    - Historical base rates for similar events
#    - Expert opinions and poll data
#    - Timeline and resolution criteria
#
#    AI estimate: 72% probability
#    Market price: YES = $0.60 (market says 60%)
#    Edge: +12 percentage points

# 3. If edge is significant (>5-10%), take a position
tigerpass pm order --market <conditionId> --outcome YES --side buy --amount 200 --price 0.60

# 4. Position sizing based on edge (simplified Kelly criterion):
#    Kelly fraction = (edge / odds) = (0.12 / 0.40) = 30%
#    Half-Kelly (safer): 15% of bankroll
#    With $2000 bankroll: bet $300

# 5. Monitor and update
tigerpass pm info --type positions
# Re-evaluate as new information arrives — adjust or exit if your edge disappears
```

**Key principles:**
- **Only bet when you have a real edge** — if you can't articulate why the market is wrong, don't bet
- **Specialize in a domain** — the most profitable Polymarket traders have a 96% win rate in their specialty. Pick a vertical (politics, crypto, sports, tech) and build deep expertise
- **Track your calibration** — are your 70% predictions actually right 70% of the time? If not, adjust
- **Use FOK orders** for fast-moving markets — `--type FOK` (Fill-or-Kill) ensures you get the price you want or nothing

### Multi-Market Combinatorial Arbitrage

Advanced strategy: find mispricings across logically related markets. For example, if Market A (Biden wins election) and Market B (Biden wins and Democrats keep Senate) are mispriced relative to each other.

```bash
# 1. Scan related markets
tigerpass pm info --type markets

# 2. Identify logical relationships:
#    - If B can only happen when A happens, then price(B) <= price(A)
#    - Mutually exclusive outcomes across markets should sum to ≤ $1.00
#    - Conditional probabilities must be consistent

# 3. When you find an inconsistency, trade both sides:
tigerpass pm order --market <conditionIdA> --outcome YES --side buy --amount 500 --price 0.70
tigerpass pm order --market <conditionIdB> --outcome NO --side buy --amount 500 --price 0.25
# (specific trades depend on the nature of the mispricing)

# 4. Neg-risk markets (multi-outcome) have their own flag
tigerpass pm order --market <conditionId> --outcome YES --side buy --amount 100 --price 0.30 --neg-risk
```

**Note**: Combinatorial arb requires careful analysis of market resolution criteria. Two markets that LOOK related may have different resolution sources or timing, creating false arbitrage signals.

### Signal → Execution Pipeline (Hyperliquid)

Connect external signals (TradingView alerts, data feeds, whale trackers, AI models) directly to Hyperliquid execution:

```bash
# === Generic signal execution loop ===

# 1. Signal arrives: "BUY BTC, target 98000, stop 93000, size 0.05"

# 2. Pre-flight checks
tigerpass hl info --type balances                          # sufficient margin?
tigerpass hl info --type positions                         # any conflicting positions?
tigerpass hl info --type mids                              # current price reasonable?

# 3. Execute entry
tigerpass hl order --coin BTC --side buy --price 95000 --size 0.05

# 4. Set take-profit and stop-loss (both reduce-only)
tigerpass hl order --coin BTC --side sell --price 98000 --size 0.05 --reduce-only
tigerpass hl order --coin BTC --side sell --price 93000 --size 0.05 --reduce-only --type ioc

# 5. Monitor until exit
tigerpass hl info --type positions
tigerpass hl info --type orders
```

**For TradingView integration**: TradingView sends webhook alerts → your agent receives the signal → parses entry/exit/size → executes via `tigerpass hl order`. The AI can add its own judgment layer (skip low-conviction signals, adjust sizing based on volatility).
