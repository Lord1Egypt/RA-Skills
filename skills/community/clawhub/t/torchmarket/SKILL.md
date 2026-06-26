---
name: torch-market
version: "11.1.0"
description: Every token is its own margin market. Depth-adaptive risk engine, treasury-backed lending, real-token short selling. No oracles. No stored baselines. No keepers. The pool is the source of truth.
license: MIT
disable-model-invocation: true
requires:
  env:
    - name: SOLANA_RPC_URL
      required: true
    - name: SOLANA_PRIVATE_KEY
      required: false
    - name: TORCH_NETWORK
      required: false
metadata:
  clawdbot:
    requires:
      env:
        - name: SOLANA_RPC_URL
          required: true
        - name: SOLANA_PRIVATE_KEY
          required: false
        - name: TORCH_NETWORK
          required: false
    primaryEnv: SOLANA_RPC_URL
  openclaw:
    requires:
      env:
        - name: SOLANA_RPC_URL
          required: true
        - name: SOLANA_PRIVATE_KEY
          required: false
        - name: TORCH_NETWORK
          required: false
    primaryEnv: SOLANA_RPC_URL
    install:
      - id: npm-torchsdk
        kind: npm
        package: torchsdk@^11.1.0
        flags: []
        label: "Install Torch SDK (npm, optional -- SDK is bundled in lib/torchsdk/ on clawhub)"
  author: torch-market
  version: "11.1.0"
  clawhub: https://clawhub.ai/mrsirg97-rgb/torchmarket
  program-source: https://github.com/mrsirg97-rgb/torch_market
  sdk-source: https://github.com/mrsirg97-rgb/torchsdk
  website: https://torch.market
  program-id: 8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT
compatibility: >-
  REQUIRED: SOLANA_RPC_URL (HTTPS Solana RPC endpoint).
  OPTIONAL: SOLANA_PRIVATE_KEY (disposable controller keypair -- fresh key, ~0.01 SOL for gas, NEVER a vault authority key).
  OPTIONAL: TORCH_NETWORK ('devnet' for devnet).
  Without SOLANA_PRIVATE_KEY, operates in read-and-build mode: queries state, returns unsigned transactions.
  SDK bundled in lib/torchsdk/. No API server dependency.
---

# torch.market

Every token launched on torch gets a funded treasury, a 300M token lending reserve, margin lending, short selling, and on-chain pricing — all live from migration.

No external LPs. No oracle feeds. No protocol token. No bootstrapping.

## What Torch Is

A protocol where every token launches with its own margin market.

- **Lending**: borrow SOL against token collateral from the token's own treasury
- **Short selling**: borrow real tokens from the 300M treasury lock, sell on the real market
- **Pricing**: Raydium pool reserves — no external oracle
- **Depth-based risk engine**: max LTV scales with pool SOL depth (25% at <50 SOL, up to 50% at 500+ SOL). Deeper pools are harder to manipulate, so higher leverage is permitted. Combined with per-user borrow caps, the effective LTV for long positions is typically <5% — making liquidation structurally near-impossible. No oracles, no stored baseline, no keepers. The pool itself is the source of truth.
- **Liquidation**: permissionless — anyone can call. Exists primarily as a backstop for shorts and extreme multi-sigma events on longs.
- **Parameters**: immutable on-chain — no admin key changes them

Shorts are not synthetic. Borrowed tokens are real. Selling them moves the real price. Short sellers are market participants contributing to price discovery.

## Token Lifecycle

```
CREATE → BOND → MIGRATE → TRADE → MARGIN
                                     │
                                ┌────┴─────┐
                              LEND     SHORT SELL
                                │          │
                              REPAY    CLOSE
                                │          │
                              LIQUIDATE  LIQUIDATE
```

**Bonding** — constant-product curve. SOL splits: curve (100% of tokens to buyer) + treasury (17.5%→2.5% dynamic SOL rate). 2% max wallet. Completes at 100 or 200 SOL.

**Migration** — permissionless. Creates Raydium pool, burns LP tokens (liquidity locked forever), revokes mint/freeze authority permanently, activates 0.07% transfer fee.

**Trading** — token trades on Raydium. Transfer fees harvest to treasury as SOL. Treasury grows perpetually.

**Margin** — two capital pools, two-sided margin:

| Pool | Asset | Purpose |
|------|-------|---------|
| Token Treasury | SOL | Lending pool — borrow SOL against token collateral |
| Treasury Lock | 300M tokens | Short pool — borrow real tokens against SOL collateral |

## Constants

```
SUPPLY          1,000,000,000 tokens (6 decimals)
CURVE_SUPPLY    700,000,000 (70%)
TREASURY_LOCK   300,000,000 (30%)
MAX_WALLET      2% during bonding
BONDING_TARGET  100 SOL (Flame) / 200 SOL (Torch)
PROTOCOL_FEE    0.5% on buys
TREASURY_RATE   17.5% → 2.5% (dynamic decay)
TRANSFER_FEE    0.07% (post-migration, immutable)
MAX_LTV         25-50% (depth-adaptive: 25% <50 SOL, 35% 50-200, 45% 200-500, 50% 500+)
LIQ_THRESHOLD   65%
INTEREST        2% per epoch (~7 days)
LIQ_BONUS       10%
UTIL_CAP        80%
BORROW_CAP      23x collateral share of supply
MIN_POOL_SOL    5 SOL (below this: all margin ops blocked)
MIN_BORROW      0.1 SOL
PROGRAM_ID      8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT
```

## SDK

```
GET QUOTE → BUILD TX → SIGN & SEND
```

One flow, any token state. The SDK auto-routes bonding curve or Raydium DEX based on the quote's `source` field.

```typescript
import { getBuyQuote, buildBuyTransaction } from "torchsdk";

const quote = await getBuyQuote(connection, mint, 100_000_000); // 0.1 SOL
const { transaction } = await buildBuyTransaction(connection, {
  mint, buyer: wallet, amount_sol: 100_000_000,
  slippage_bps: 500, vault: vaultCreator, quote,
});
// sign and send — VersionedTransaction, ALT-compressed
```

### Queries

| Function | Returns |
|----------|---------|
| `getTokens(connection, params?)` | Token list (filterable, sortable) |
| `getToken(connection, mint)` | Full detail: price, treasury, status |
| `getTokenMetadata(connection, mint)` | On-chain Token-2022 metadata |
| `getHolders(connection, mint)` | Top holders with balance/percentage |
| `getMessages(connection, mint, limit?, opts?)` | On-chain memos. `{ enrich: true }` adds SAID |
| `getLendingInfo(connection, mint)` | Lending parameters and pool state |
| `getLoanPosition(connection, mint, wallet)` | Loan: collateral, debt, LTV, health |
| `getAllLoanPositions(connection, mint)` | All loans sorted by liquidation risk |
| `getShortPosition(connection, mint, wallet)` | Short: collateral, debt, LTV, health |
| `getBuyQuote(connection, mint, sol)` | Tokens out, fees, impact. `source: bonding\|dex` |
| `getSellQuote(connection, mint, tokens)` | SOL out, impact. `source: bonding\|dex` |
| `getBorrowQuote(connection, mint, collateral)` | Max borrow: LTV, pool, per-user caps |
| `getVault(connection, creator)` | Vault state |
| `getVaultForWallet(connection, wallet)` | Reverse vault lookup |
| `getUserStats(connection, wallet)` | Per-user trading volume + rewards-claimed history |
| `getProtocolTreasuryState(connection)` | Protocol treasury: epoch, aggregate volume, distributable amount |
| `getTreasuryState(connection, mint)` | Per-token treasury: SOL balance, tokens held, baseline pool reserves at migration, stars |

### Trading

| Function | Description |
|----------|-------------|
| `buildBuyTransaction` | Buy via vault. Auto-routes bonding/DEX |
| `buildDirectBuyTransaction` | Buy without vault (human wallets) |
| `sendBuy` | Build + simulate + submit vault buy via `signAndSendTransaction` |
| `sendDirectBuy` | Build + simulate + submit direct buy via `signAndSendTransaction` |
| `buildSellTransaction` | Sell via vault. Auto-routes bonding/DEX |
| `buildCreateTokenTransaction` | Launch token + treasury + 300M lock |
| `sendCreateToken` | Build + simulate + submit token creation (Phantom-friendly) |
| `buildStarTransaction` | Star token (0.02 SOL) |
| `buildMigrateTransaction` | Migrate to Raydium (permissionless) |

### Margin (post-migration)

| Function | Description |
|----------|-------------|
| `buildBorrowTransaction` | Borrow SOL against token collateral |
| `buildRepayTransaction` | Repay debt, unlock collateral |
| `buildLiquidateTransaction` | Liquidate loan (>65% LTV) |
| `buildOpenShortTransaction` | Post SOL, borrow tokens from treasury lock |
| `buildCloseShortTransaction` | Return tokens, recover SOL collateral |
| `buildLiquidateShortTransaction` | Liquidate short (>65% LTV) |
| `buildClaimProtocolRewardsTransaction` | Claim epoch trading rewards |

### Vault

| Function | Signer |
|----------|--------|
| `buildCreateVaultTransaction` | creator |
| `buildDepositVaultTransaction` | anyone |
| `buildWithdrawVaultTransaction` | authority |
| `buildWithdrawTokensTransaction` | authority |
| `buildLinkWalletTransaction` | authority |
| `buildUnlinkWalletTransaction` | authority |
| `buildTransferAuthorityTransaction` | authority |

### Treasury Cranks (permissionless)

| Function | Description |
|----------|-------------|
| `buildHarvestFeesTransaction` | Harvest 0.07% transfer fees to treasury |
| `buildSwapFeesToSolTransaction` | Swap harvested tokens to SOL via Raydium |
| `buildAdvanceProtocolEpochTransaction` | Advance protocol epoch so previous-epoch rewards become claimable |
| `buildReclaimFailedTokenTransaction` | Reclaim inactive tokens (7+ days) |

## Vault — Why Funds Are Safe

```
Human (authority)                   Agent (controller, ~0.01 SOL gas)
  ├── createVault()                  ├── buy(vault)       → vault pays
  ├── depositVault(5 SOL)            ├── sell(vault)      → SOL to vault
  ├── linkWallet(agent)              ├── borrow(vault)    → SOL to vault
  ├── withdrawVault()  ← auth only   ├── repay(vault)     → collateral back
  └── unlinkWallet()   ← instant     ├── openShort(vault) → tokens to vault
                                     └── closeShort(vault)→ SOL to vault
```

| Guarantee | Mechanism |
|-----------|-----------|
| Full custody | Vault holds all SOL and tokens. Controller holds nothing. |
| Closed loop | Every operation returns value to vault. No leakage. |
| Authority separation | Creator (immutable) / Authority (transferable) / Controller (disposable) |
| Instant revocation | Authority unlinks controller in one tx |
| No extraction | Controllers cannot withdraw. Period. |
| Isolated positions | One loan per user per token. One short per user per token. No cascading. |
| Immutable parameters | LTV, liquidation, interest — set at deployment. No admin key changes them. |

## Key Safety

If `SOLANA_PRIVATE_KEY` is provided: must be a fresh disposable keypair (~0.01 SOL gas). All capital lives in vault. If compromised: attacker gets dust, authority revokes in one tx. Key never leaves the runtime.

If not provided: read-only mode — queries state, returns unsigned transactions.

**Rules:**
1. Never ask for a private key or seed phrase.
2. Never log, print, store, or transmit key material.
3. Use a secure HTTPS RPC endpoint.

## Risk

Positions can be liquidated. Bad debt is possible in extreme conditions. There is no insurance fund. But:

- Bad debt is isolated — one position going underwater cannot affect any other position
- Per-user caps prevent pool concentration — one user cannot drain the lending pool
- 20% of treasury SOL is always reserved (utilization cap)
- Liquidation is permissionless — no keeper dependency

## Verification

71 Kani proof harnesses. 97 litesvm tests. 62 SDK e2e tests. All passing. Cross-validated by independent audit. Core arithmetic and depth-band boundaries formally verified. See [VERIFICATION.md](https://torch.market/verification.md) and [risk.md](https://torch.market/risk.md).

## Links

- [torch.market](https://torch.market) | [Whitepaper](https://torch.market/whitepaper) | [Risk Model](https://torch.market/risk.md)
- SDK: `lib/torchsdk/` | [npm](https://www.npmjs.com/package/torchsdk) | [source](https://github.com/mrsirg97-rgb/torchsdk)
- Program: `8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`
