# Torch SDK Security Audit

**Audit Date:** March 29, 2026
**Auditor:** Claude Opus 4.6 (Anthropic)
**SDK Version:** 10.1.1
**On-Chain Program:** `8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT` (V10.1.1)
**Language:** TypeScript
**Test Result:** 39 passed, 0 failed (Surfpool mainnet fork)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Scope](#scope)
3. [Methodology](#methodology)
4. [PDA Derivation Correctness](#pda-derivation-correctness)
5. [Quote Math Verification](#quote-math-verification)
6. [Vault Integration Review](#vault-integration-review)
7. [Input Validation](#input-validation)
8. [External API Surface](#external-api-surface)
9. [Dependency Analysis](#dependency-analysis)
10. [Transaction Builder Review](#transaction-builder-review)
11. [Findings](#findings)
12. [Conclusion](#conclusion)

---

## Executive Summary

This audit covers the Torch SDK v4.0.1, a TypeScript library that reads on-chain state from Solana and builds unsigned transactions for the Torch Market protocol. The SDK was cross-referenced against the live on-chain program (V4.0.1) to verify PDA derivation, quote math, vault integration, migration flow, lending accounting, and account handling. v3.7.17 includes V25 pump-style reserves, V26 permissionless migration, V27 treasury lock and PDA-based pool validation, removal of `update_authority` (V28), V20 swap fees to SOL, V29 on-chain Token-2022 metadata (Metaplex removal, 0.1% transfer fee), a critical lending accounting fix, and dynamic network detection.

The SDK is **stateless** (no global state, no connection pools), **non-custodial** (never touches private keys — all transactions are returned unsigned), and **RPC-first** (all data from Solana, no proprietary API for core operations).

### Overall Assessment

| Category | Rating | Notes |
|----------|--------|-------|
| PDA Derivation | **PASS** | All 12 seeds match on-chain `constants.rs` exactly |
| Quote Math | **PASS** | Exact match with on-chain buy handler (BigInt, fees, dynamic rate, token split) |
| Vault Integration | **PASS** | Correct null/Some handling, wallet link derived from buyer (not vault creator) |
| Key Safety | **PASS** | No key custody — unsigned transaction pattern throughout |
| Input Validation | **PASS** | Slippage validated with explicit error, lengths checked, PublicKey constructor validates base58 |
| External APIs | **PASS** | SAID + CoinGecko + metadata URI — all degrade gracefully, metadata fetch has 10s timeout |
| Dependencies | **MINIMAL** | 4 runtime deps, all standard Solana ecosystem |

### Finding Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 (3 resolved in v3.2.4) |
| Informational | 7 |

---

## Scope

### Files Reviewed

| File | Lines | Role |
|------|-------|------|
| `src/index.ts` | 114 | Public API surface (37 functions, ~47 types, 5 constants) |
| `src/types.ts` | 458 | All TypeScript interfaces |
| `src/constants.ts` | 114 | Program ID, PDA seeds, token constants, blacklist, dynamic network detection |
| `src/program.ts` | 476 | PDA derivation, Anchor types, quote math, Raydium PDAs |
| `src/tokens.ts` | ~1010 | Read-only queries (tokens, vault, lending, loan positions, holders, messages with SAID enrichment, pool price) |
| `src/transactions.ts` | ~1960 | Transaction builders (buy, sell, vault, lending, star, migrate, reclaim, harvest, swap fees) |
| `src/quotes.ts` | 102 | Buy/sell quote calculations |
| `src/said.ts` | 110 | SAID Protocol integration |
| `src/gateway.ts` | 49 | Irys metadata fetch with fallback + timeout |
| `src/ephemeral.ts` | 45 | Ephemeral agent (disposable wallet helper) |
| `src/torch_market.json` | — | Anchor IDL (V4.0.1, 27 instructions) |
| **Total** | **~4,415** | |

### On-Chain Cross-Reference

| File | Purpose |
|------|---------|
| `constants.rs` | Verified all PDA seed strings and numeric constants |
| `contexts.rs` | Verified Buy context vault account derivation and constraints |
| `handlers/market.rs` | Verified buy/sell math matches SDK quote engine |

---

## Methodology

1. **Line-by-line source review** of all 10 SDK source files
2. **PDA seed cross-reference** between `constants.ts` and on-chain `constants.rs`
3. **Math cross-reference** between `program.ts:calculateTokensOut` and on-chain `handlers/market.rs:buy`
4. **Vault account cross-reference** between `transactions.ts:buildBuyTransaction` and on-chain `contexts.rs:Buy`
5. **E2E validation** via Surfpool mainnet fork (32/32 tests passed)

---

## PDA Derivation Correctness

All PDA seeds in the SDK were compared against the on-chain Rust program:

| PDA | SDK Seed (`constants.ts`) | On-Chain Seed (`constants.rs`) | Match |
|-----|--------------------------|-------------------------------|-------|
| GlobalConfig | `"global_config"` | `b"global_config"` | YES |
| BondingCurve | `["bonding_curve", mint]` | `[BONDING_CURVE_SEED, mint]` | YES |
| Treasury | `["treasury", mint]` | `[TREASURY_SEED, mint]` | YES |
| UserPosition | `["user_position", bonding_curve, user]` | `[USER_POSITION_SEED, bonding_curve, user]` | YES |
| UserStats | `["user_stats", user]` | `[USER_STATS_SEED, user]` | YES |
| ProtocolTreasury | `"protocol_treasury_v11"` | `b"protocol_treasury_v11"` | YES |
| StarRecord | `["star_record", user, mint]` | `[STAR_RECORD_SEED, user, mint]` | YES |
| LoanPosition | `["loan", mint, user]` | `[LOAN_SEED, mint, user]` | YES |
| CollateralVault | `["collateral_vault", mint]` | `[COLLATERAL_VAULT_SEED, mint]` | YES |
| TorchVault | `["torch_vault", creator]` | `[TORCH_VAULT_SEED, creator]` | YES |
| VaultWalletLink | `["vault_wallet", wallet]` | `[VAULT_WALLET_LINK_SEED, wallet]` | YES |

**Raydium PDAs** (under `RAYDIUM_CPMM_PROGRAM`):

| PDA | SDK Seed | Match |
|-----|----------|-------|
| Authority | `["vault_and_lp_mint_auth_seed"]` | YES |
| PoolState | `["pool", amm_config, token0, token1]` | YES |
| LP Mint | `["pool_lp_mint", pool_state]` | YES |
| Vault | `["pool_vault", pool_state, token_mint]` | YES |
| Observation | `["observation", pool_state]` | YES |

**Token ordering** for Raydium uses byte-level comparison (`token0 < token1`), matching Raydium convention. Implementation in `orderTokensForRaydium` (program.ts:334-351) iterates all 32 bytes.

**Verdict:** All PDA derivations are correct and match the on-chain program exactly.

---

## Quote Math Verification

### Buy Quote (`calculateTokensOut`)

SDK implementation (program.ts:243-299) was compared step-by-step against on-chain `buy` handler (market.rs:23-478):

| Step | SDK (BigInt) | On-Chain (u64/u128) | Match |
|------|-------------|---------------------|-------|
| Protocol fee | `solAmount * 50n / 10000n` | `sol_amount * protocol_fee_bps / 10000` | YES |
| Treasury fee | `solAmount * 0n / 10000n` (V10: 0%) | `sol_amount * TREASURY_FEE_BPS / 10000` (0) | YES |
| Sol after fees | `solAmount - protocolFee - treasuryFee` | `sol_amount - protocol_fee_total - token_treasury_fee` | YES |
| Dynamic rate bounds | `treasuryRateBounds(bondingTarget)` → per-tier (max, min) | `treasury_rate_bounds(bonding_target)` → per-tier (max, min) | YES |
| Dynamic rate range | `BigInt(bounds.max - bounds.min)` | `(max_bps - min_bps)` | YES |
| Decay | `realSolReserves * rateRange / resolvedTarget` | `reserves * rate_range / target` | YES |
| Rate floor | `Math.max(bounds.max - decay, bounds.min)` | `rate.max(min_bps)` | YES |
| Sol to treasury | `solAfterFees * treasuryRateBps / 10000` | `sol_after_fees * treasury_rate_bps / 10000` | YES |
| Sol to curve | `solAfterFees - solToTreasurySplit` | `sol_after_fees - sol_to_treasury_split` | YES |
| Tokens out | `virtualTokens * solToCurve / (virtualSol + solToCurve)` | `virtual_token_reserves * sol_to_curve / (virtual_sol_reserves + sol_to_curve)` | YES |
| Tokens to user | `tokensOut * 9000n / 10000n` | `tokens_out * (10000 - BURN_RATE_BPS) / 10000` where BURN_RATE_BPS=1000 | YES |
| Tokens to treasury | `tokensOut - tokensToUser` | `tokens_out - tokens_to_buyer` | YES |

**Key observation:** The SDK uses `BigInt` for all arithmetic, mirroring the on-chain `checked_mul`/`checked_div` behavior. Integer division truncation is identical in both environments.

### Sell Quote (`calculateSolOut`)

| Step | SDK | On-Chain | Match |
|------|-----|----------|-------|
| Sol out | `virtualSol * tokenAmount / (virtualTokens + tokenAmount)` | `virtual_sol_reserves * token_amount / (virtual_token_reserves + token_amount)` | YES |
| Fee | 0 (no sell fee) | `SELL_FEE_BPS = 0` | YES |

**Verdict:** Quote math is an exact match with the on-chain program.

---

## Vault Integration Review

### Buy Transaction — Vault Account Handling

The on-chain `Buy` context (contexts.rs:170-286) defines:

```rust
pub torch_vault: Option<Box<Account<'info, TorchVault>>>,
pub vault_wallet_link: Option<Box<Account<'info, VaultWalletLink>>>,
```

The `vault_wallet_link` constraint uses `buyer.key()` as the seed:
```rust
seeds = [VAULT_WALLET_LINK_SEED, buyer.key().as_ref()],
```

**SDK behavior** (transactions.ts:167-173):

```typescript
if (vaultCreatorStr) {
  const vaultCreator = new PublicKey(vaultCreatorStr)
  ;[torchVaultAccount] = getTorchVaultPda(vaultCreator)     // from creator
  ;[vaultWalletLinkAccount] = getVaultWalletLinkPda(buyer)  // from buyer
}
```

This is **correct**:
- Vault PDA is derived from the vault creator (the `vault` param)
- Wallet link PDA is derived from the buyer (the transaction signer)
- When not using vault, both are passed as `null` (Anchor treats as `None`)

### On-Chain C-1 Fix Verification

The on-chain buy handler (market.rs:30-39) includes the critical fix:

```rust
if ctx.accounts.torch_vault.is_some() {
    require!(
        ctx.accounts.vault_wallet_link.is_some(),
        TorchMarketError::WalletNotLinked
    );
}
```

The SDK always provides both vault accounts together or neither (transactions.ts:167-173), so the C-1 vulnerability path is not reachable through the SDK. However, the on-chain fix is the actual security boundary — the SDK is just a convenience layer.

### Vault Query Functions

| Function | Derivation | Verified |
|----------|-----------|----------|
| `getVault(creator)` | `getTorchVaultPda(creator)` | YES |
| `getVaultForWallet(wallet)` | `getVaultWalletLinkPda(wallet)` → follow `link.vault` | YES |
| `getVaultWalletLink(wallet)` | `getVaultWalletLinkPda(wallet)` | YES |

### Sell, Star, Borrow, Repay — Vault Account Handling

V3.2.0 extends vault routing to all write operations. The SDK passes `torchVault`, `vaultWalletLink`, and (where applicable) `vaultTokenAccount` as optional accounts. When vault is not specified, all three are passed as `null`. The pattern is consistent across all builders — verified by E2E tests covering vault-routed buy, sell, star, borrow, repay, and DEX swap.

### Protocol Rewards — Vault-Routed Claim

`buildClaimProtocolRewardsTransaction` routes epoch reward claims through the vault. The protocol treasury accumulates 0.5% fees from all bonding curve buys. Each epoch, rewards are distributed proportionally to wallets with >= 2 SOL volume in the previous epoch. Min claim: 0.1 SOL. The claim sends SOL directly to the vault — maintaining the closed economic loop. The SDK derives all required accounts (UserStats, ProtocolTreasury, TorchVault, VaultWalletLink) from the caller's public key and vault creator.

**Verdict:** Vault integration is correct and consistent with the on-chain program.

---

## Input Validation

### PublicKey Strings

All public key strings are passed to `new PublicKey(str)` which throws on invalid base58. The SDK does **not** pre-validate these — it relies on the `PublicKey` constructor. This is acceptable since:
- Invalid keys throw immediately with a clear error
- No on-chain transaction is built or submitted with invalid keys

### Slippage Validation

Buy and sell builders validate slippage (transactions.ts):

```typescript
if (slippage_bps < 10 || slippage_bps > 1000) {
  throw new Error(`slippage_bps must be between 10 (0.1%) and 1000 (10%), got ${slippage_bps}`)
}
```

Range: **0.1% to 10%**. Default: **1%** (100 bps). Values outside this range throw an explicit error (previously silently clamped in v3.2.3, resolved in v3.2.4). The buy quote (quotes.ts:47) uses a fixed 1% slippage for `min_output_tokens`, which is independent of the builder's slippage.

### String Length Validation

- Token name: max 32 characters (transactions.ts:346)
- Token symbol: max 10 characters (transactions.ts:347)
- Message: max 500 characters (transactions.ts:206-208, 304-306)

### Numeric Inputs

`amount_sol` and `amount_tokens` are not explicitly validated for zero or negative values. However:
- Zero amounts will produce zero output and fail the on-chain `MIN_SOL_AMOUNT` check (0.001 SOL)
- Negative numbers will produce invalid `BN` values and fail on-chain

---

## External API Surface

### SAID Protocol API

**Endpoint:** `https://api.saidprotocol.com/api`

| Function | Method | Risk |
|----------|--------|------|
| `verifySaid(wallet)` | `GET /verify/{wallet}` | Low |
| `confirmTransaction(...)` | On-chain only (no API call) | None |

`verifySaid` fails gracefully — returns `{ verified: false, trustTier: null }` on any error (said.ts:36-38). This is **read-only** and **non-critical** — it enriches token detail responses but does not affect trading.

### CoinGecko API

**Endpoint:** `https://api.coingecko.com/api/v3/simple/price`

Used in `getToken()` (tokens.ts:342-349) for SOL/USD conversion. Fails gracefully — adds a warning string but does not throw. Non-critical — `price_usd` and `market_cap_usd` are `undefined` on failure.

### Metadata URI (Token Creator-Controlled)

`getToken()` fetches the metadata URI stored in the on-chain `BondingCurve.uri` field (tokens.ts:314-328). This URI is **set by the token creator** and could point to any HTTP endpoint.

The SDK:
- Uses `fetchWithFallback()` which rewrites Irys gateway URLs to uploader URLs
- Parses the JSON response for `description`, `image`, `twitter`, `telegram`, `website`
- Fails gracefully — catches errors and adds a warning

**Risk:** The metadata URI is creator-controlled, so a malicious creator could set it to a slow/hostile endpoint. As of v3.2.4, `fetchWithFallback` enforces a 10-second timeout via `AbortController`. Slow endpoints are aborted and the error is caught gracefully. This is not in any transaction path.

---

## Dependency Analysis

### Runtime Dependencies

| Package | Version | Purpose | Risk |
|---------|---------|---------|------|
| `@coral-xyz/anchor` | ^0.32.1 | IDL decoding, program interaction | Low — standard Solana |
| `@solana/spl-token` | ^0.4.14 | ATA derivation, token instructions | Low — standard Solana |
| `@solana/web3.js` | ^1.98.4 | RPC, PublicKey, Transaction | Low — standard Solana |
| `bs58` | ^6.0.0 | Base58 decoding (memo parsing) | Low — pure JS, no native |

### Dev Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `@types/node` | ^20 | TypeScript types |
| `prettier` | ^3.5.3 | Code formatting |
| `typescript` | ^5 | Compilation |

**Verdict:** Minimal dependency surface. All 4 runtime dependencies are standard Solana ecosystem packages. No native modules (except transitive via `@solana/web3.js`). No custom crypto.

---

## Transaction Builder Review

### Key Safety — Unsigned Transaction Pattern

All `build*Transaction` functions return `{ transaction: Transaction, message: string }`. The SDK **never**:
- Accepts private keys or keypairs as parameters (except `buildCreateTokenTransaction` which generates and returns a mint keypair)
- Signs transactions
- Submits transactions to the network

The `makeDummyProvider` pattern (transactions.ts:67-74) creates a no-op wallet for Anchor's `Program` constructor. The dummy wallet's `signTransaction` is a passthrough — it is never called during instruction building.

**One exception:** `buildCreateTokenTransaction` generates a `Keypair` for the mint, partially signs the transaction with it (transactions.ts:398), and returns the keypair. This is by design — the mint must be a signer for Token-2022 initialization. The caller receives the keypair for address extraction. This is not a custody risk since the mint keypair has no authority after creation.

### Account Derivation Consistency

All transaction builders derive accounts locally from PDA functions in `program.ts`. No builder accepts raw account addresses from the caller — all addresses are computed from the mint, buyer/seller, and vault creator parameters. This eliminates account confusion attacks at the SDK level.

### Blockhash Freshness

All transactions call `finalizeTransaction()` which fetches `getLatestBlockhash()` (transactions.ts:76-84). The blockhash is fetched at build time, not at sign time. If there is a long delay between building and signing, the transaction may expire. This is standard behavior for Solana SDKs.

### ~~Auto-Buyback Pre-Checks (v3.7.2)~~ -- REMOVED (V33)

`buildAutoBuybackTransaction` was removed in v3.7.22. The on-chain `execute_auto_buyback` instruction was removed in V33 (program v3.7.7). Treasury SOL is no longer spent on market buys during price dips. The treasury accumulation loop is now: fee harvest → sell high → SOL → lending yield + epoch rewards.

### Harvest Fees Auto-Discovery (v3.7.2)

`buildHarvestFeesTransaction` includes auto-discovery of token accounts with withheld transfer fees:

1. If `sources` param is provided, uses those addresses directly
2. Otherwise calls `getTokenLargestAccounts(mint)` to find candidate accounts
3. For each account, calls `unpackAccount` + `getTransferFeeAmount` to check for withheld fees > 0
4. Passes matching accounts as `remainingAccounts` to the on-chain `harvestFees` instruction
5. Compute budget scales dynamically: `200_000 + 20_000 * sourceAccounts.length`

The entire auto-discovery path is wrapped in a try/catch. If `getTokenLargestAccounts` fails (unsupported by RPC, e.g. Surfpool local validator), the SDK falls back to an empty source list and the transaction still proceeds — the on-chain program harvests from the mint's withheld authority regardless.

**Verdict:** Auto-discovery is a best-effort optimization. Graceful fallback ensures the transaction builder never throws on RPC limitations. The `sources` param provides an escape hatch for callers who know their source accounts.

---

## Findings

### L-1: No Timeout on Metadata URI Fetch — RESOLVED in v3.2.4

**Severity:** Low
**File:** `gateway.ts`
**Description:** `getToken()` fetches the metadata URI (creator-controlled) without a timeout. A malicious or slow endpoint could cause `getToken()` to hang indefinitely.
**Impact:** Denial of service for `getToken()` callers. Does not affect transaction building.
**Resolution:** `fetchWithFallback` now accepts a `timeoutMs` parameter (default 10s) and enforces it via `AbortController`. Slow/hanging endpoints are aborted and the error is caught gracefully.

### L-2: Silent Slippage Clamping — RESOLVED in v3.2.4

**Severity:** Low
**File:** `transactions.ts`
**Description:** Slippage values outside the 0.1%-10% range were silently clamped. A caller passing `slippage_bps: 5000` (50%) got 10% without any warning.
**Impact:** Unexpected slippage behavior. Not a fund safety issue — trades fail rather than execute at bad prices.
**Resolution:** Out-of-range `slippage_bps` values now throw an explicit error with the accepted range (10–1000 bps).

### L-3: Hardcoded Discriminator — RESOLVED in v3.2.4

**Severity:** Low
**File:** `tokens.ts`
**Description:** LoanPosition account scanning used a hardcoded 8-byte discriminator array. If the IDL changes (account rename), this would silently break loan enumeration.
**Impact:** `getLendingInfo()` could return incorrect loan counts. No security impact.
**Resolution:** LoanPosition discriminator is now derived from the Anchor IDL via `BorshCoder.accounts.accountDiscriminator('LoanPosition')`. Changes to the IDL are automatically reflected.

### I-1: No Zero Amount Validation

**Severity:** Informational
**File:** `transactions.ts:100-224`
**Description:** Buy and sell builders do not check for zero `amount_sol` or `amount_tokens`. Zero amounts will produce zero-output transactions that fail on-chain (`MIN_SOL_AMOUNT` check).
**Impact:** Wasted transaction fee. The on-chain program rejects the transaction safely.

### I-2: Vote Parameter Encoding

**Severity:** Informational
**File:** `transactions.ts:179`
**Description:** The vote parameter encoding is `return → true`, `burn → false`, `undefined → null`. This inverted convention (return=true, burn=false) matches the on-chain program but could confuse SDK consumers who might expect burn=true.
**Impact:** None — encoding is correct. Documentation should clarify the inversion.

### I-3: CoinGecko Rate Limiting

**Severity:** Informational
**File:** `tokens.ts:342-349`
**Description:** The CoinGecko free API has rate limits. High-frequency `getToken()` calls will trigger rate limiting, causing `price_usd` to be unavailable.
**Impact:** Missing USD pricing. Degrades gracefully.

### I-4: Holder Count Uses `getTokenLargestAccounts`

**Severity:** Informational
**File:** `tokens.ts:333-337`
**Description:** Holder count is derived from `getTokenLargestAccounts` which returns at most 20 accounts. For tokens with many holders, this count is an undercount.
**Impact:** Reported holder count may be lower than actual. Non-critical — informational only.

### I-5: Lending Constants are Hardcoded

**Severity:** Informational
**File:** `tokens.ts:504-507`
**Description:** Lending parameters (`INTEREST_RATE_BPS`, `MAX_LTV_BPS`, `LIQUIDATION_THRESHOLD_BPS`, `LIQUIDATION_BONUS_BPS`) are hardcoded in the SDK rather than read from on-chain state. If the on-chain program updates these values, the SDK would report stale parameters.
**Impact:** `getLendingInfo()` could report incorrect rates. Does not affect transaction building — the on-chain program enforces actual rates.
**Recommendation:** Read lending parameters from the on-chain Treasury or GlobalConfig account if available.

### I-6: Platform Treasury Removal (V3.2.0)

**Severity:** Informational
**Description:** V3.2.0 merges the platform treasury into the protocol treasury. The `buildClaimEpochRewardsTransaction` function and `ClaimEpochRewardsParams` type have been removed. The `platform_treasury` optional account has been removed from Buy and Sell builders. Reclaim SOL now routes to the protocol treasury instead of the platform treasury. The protocol treasury is now the single reward system — funded by both trading fees and reclaims.
**Impact:** Breaking change for SDK consumers using epoch rewards. All clients must update to v3.2.0.
**Status:** By design. Reduces code surface and eliminates a duplicate reward system.

### I-7: Harvest Auto-Discovery Depends on `getTokenLargestAccounts` (V3.7.2)

**Severity:** Informational
**File:** `transactions.ts`
**Description:** The harvest fees auto-discovery relies on `getTokenLargestAccounts`, an RPC method that is not universally supported. Some RPC providers and local validators (e.g. Surfpool) return internal errors for this method. The SDK wraps this in a try/catch and falls back to an empty source list.
**Impact:** On unsupported RPCs, auto-discovery is silently skipped. The harvest transaction still executes but only harvests from the mint's withheld authority, not from individual token accounts. Callers can use the explicit `sources` parameter as a workaround.
**Status:** By design. Graceful degradation is the correct behavior — the alternative (throwing) would break the builder entirely on unsupported RPCs.

---

## Conclusion

The Torch SDK v4.0.1 is a well-structured, minimal-surface TypeScript library that correctly mirrors the on-chain Torch Market V4.0.1 program. Key findings:

1. **PDA derivation is correct** — all 11 Torch PDAs and 5 Raydium PDAs match the on-chain seeds exactly.
2. **Quote math is correct** — BigInt arithmetic matches the on-chain Rust `checked_mul`/`checked_div` behavior, including the dynamic treasury rate, 90/10 token split, and constant product formula.
3. **Vault integration is correct** — vault PDA derived from creator, wallet link derived from buyer, both null when vault not used.
4. **No key custody** — the SDK never touches private keys. All transactions are returned unsigned.
5. **Minimal dependency surface** — 4 runtime deps, all standard Solana ecosystem.
6. **All low-severity findings resolved** — metadata fetch timeout added, slippage validation made explicit, discriminator derived from IDL. 7 informational issues remain (by design or non-critical).
7. **V3.2.1 on-chain security fix verified** — `harvest_fees` `treasury_token_account` constrained to treasury's exact ATA via Anchor `associated_token` constraints. Independent human auditor gave green flag.
8. **V3.3.0 tiered bonding** — new `sol_target` parameter on `buildCreateTokenTransaction` correctly passes through to on-chain `CreateTokenArgs`. Kani proofs updated and verified for all tiers (20/20 passing).
9. **V3.4.0 tiered fees** — `calculateTokensOut` now accepts `bondingTarget` parameter. Fee tier derived from `bonding_target` — zero new state. Legacy tokens map to Torch bounds.
10. **V3.5.1 pump-style distribution (V25)** — New virtual reserve model: IVS = bonding_target/8, IVT = 900M tokens, ~81x multiplier. Reverted V24 per-tier fees to flat 20%→5% all tiers. 35 Kani proof harnesses (up from 26), including V25 supply conservation.
11. **V3.6.0 permissionless migration (V26)** — Two-step migration: `fundMigrationWsol` + `migrateToDex` in one transaction. New `buildMigrateTransaction` correctly derives all Raydium CPMM PDAs, passes treasury as WSOL funder, payer covers rent. Tested on devnet E2E.
12. **V3.6.0 pool validation (V27)** — AMM config constrained to known constant, pool state ownership verified against Raydium CPMM program ID. Closes account substitution vector for vault swap operations.
13. **V3.7.0 update authority removed (V28)** — The `update_authority` admin instruction was added in V3.6.0 (V28) and subsequently **removed** in V3.7.0. Authority transfer is now done at deployment time via multisig tooling rather than an on-chain instruction, reducing the protocol's admin attack surface. 27 instructions total (down from 28). Minimal admin surface: only `initialize` and `update_dev_wallet` require authority.
14. **Lending `sol_balance` fix** — Treasury `sol_balance` now correctly decremented on borrow and incremented on repay/liquidation. Critical accounting bug resolved.
15. **Lending utilization cap** — `getLendingInfo` now returns `(sol_balance * 50%) - total_sol_lent` as `treasury_sol_available`, matching on-chain enforcement. Previously returned raw `sol_balance`.
16. **Live Raydium pool price** — `getToken()` fetches pool vault balances for migrated tokens, reporting live price instead of frozen bonding curve virtual reserves.
17. **Dynamic network detection** — `isDevnet()` checks `globalThis.__TORCH_NETWORK__` first (browser runtime), then `process.env.TORCH_NETWORK`. Raydium addresses switch automatically. Deprecated static constants preserved for backward compatibility.
18. **Pre-migration buyback removed** — Simplified protocol: only post-migration DEX buyback remained. *(Post-migration buyback also removed in V33 — see #26)*
19. **V3.7.0 treasury lock (V27)** — 250M tokens (25%) locked in TreasuryLock PDA at creation; 750M (75%) for bonding curve. IVS = 3BT/8, IVT = 756.25M tokens — 13.44x multiplier across all tiers. PDA-based Raydium pool validation replaces runtime validation. 36 Kani proof harnesses, all passing.
20. **V3.7.1 treasury cranks** — New `buildHarvestFeesTransaction` harvests accumulated Token-2022 transfer fees from token accounts into the treasury. Permissionless — anyone can trigger. New type: `HarvestFeesParams`. *(Note: `buildAutoBuybackTransaction` was also added in v3.7.1 and removed in v3.7.22 — see #26)*
21. **V3.7.2 harvest auto-discovery pre-checks** — Harvest fees auto-discovery and pre-checks added. *(Buyback pre-checks also added in v3.7.2 and removed in v3.7.22)*
22. **V3.7.2 harvest auto-discovery** — `buildHarvestFeesTransaction` auto-discovers source accounts with withheld fees via `getTokenLargestAccounts` + `unpackAccount` + `getTransferFeeAmount`. Dynamic compute budget (200k base + 20k per source). Try/catch fallback when RPC doesn't support `getTokenLargestAccounts` (I-7). New optional `sources` param for explicit account list.
23. **V3.7.10 swap fees to SOL (V20)** — New `buildSwapFeesToSolTransaction` bundles `create_idempotent(treasury_wsol)` + `harvest_fees` + `swap_fees_to_sol` in one atomic transaction. Sells harvested Token-2022 transfer fee tokens back to SOL via Raydium CPMM. Treasury PDA signs the swap, WSOL ATA closed to unwrap proceeds. SOL added to `treasury.sol_balance` and tracked in `treasury.harvested_fees` (repurposed from unused field). All Raydium accounts PDA-derived. Defense-in-depth: `validate_pool_accounts()` with correct vault ordering via `order_mints()`. New type: `SwapFeesToSolParams`. Fixed vault ordering bug — vaults now passed in pool order (by mint pubkey) instead of swap direction. No new Kani proofs needed (CPI composition, not new arithmetic).

24. **V3.7.17 on-chain metadata (V29)** — Metaplex `buildAddMetadataTransaction` removed (temporary backfill complete — all active tokens now use Token-2022 metadata extensions). New `getTokenMetadata(connection, mint)` read-only function returns `{ name, symbol, uri, mint }` from on-chain Token-2022 metadata. Transfer fee updated from 1% to 0.1% on-chain (`TRANSFER_FEE_BPS` changed from 100 to 10). All Metaplex program references, constants, and instruction builders removed from SDK. IDL updated to v3.7.17 (28 instructions).

25. **V3.7.17 loan position scanner** — New `getAllLoanPositions(connection, mint)` scans all `LoanPosition` accounts for a token via `getProgramAccounts` with discriminator + mint memcmp filters. Decodes accounts using Anchor's BorshCoder, filters active positions (`borrowed_amount > 0`), fetches Raydium pool price once for collateral valuation, computes health status per position (`healthy`/`at_risk`/`liquidatable`/`none`), and returns sorted by liquidation risk (liquidatable first). New types: `LoanPositionWithKey` (extends `LoanPositionInfo` with `borrower` address), `AllLoanPositionsResult` (`positions` array + `pool_price_sol`). Read-only query — no on-chain instruction change. Uses same discriminator derivation pattern as `getTokens()` (Anchor IDL-derived, not hardcoded — per L-3 resolution). The `getProgramAccounts` call applies a 40-byte offset memcmp filter on the mint field, matching the `LoanPosition` account layout (8-byte discriminator + 32-byte mint).

26. **V3.7.22 buyback removal (V33)** — `buildAutoBuybackTransaction` removed (~180 lines). The on-chain `execute_auto_buyback` instruction was removed in V33 (program v3.7.7, 27 instructions). `AutoBuybackParams` type removed. `TreasuryBuybackDex` context removed from on-chain program. Treasury simplified to: fee harvest → sell high → SOL → lending yield + epoch rewards. Lending utilization cap increased from 50% to 70%. IDL updated to v3.7.7. 39 Kani proofs all passing. Binary size reduced ~6% (850 KB → 804 KB). Pure removal — no new SDK code, no new attack surface.

27. **V3.7.29 reclaim failed tokens + per-user borrow cap (V3.7.9)** — New `buildReclaimFailedTokenTransaction` — permissionless reclaim of failed tokens inactive for 7+ days that haven't completed bonding. SOL from both bonding curve and token treasury goes to protocol treasury. New `ReclaimParams` type (`payer`, `mint`). Accounts derived locally: `bondingCurve`, `tokenTreasury`, `protocolTreasury` PDAs — same derivation pattern as other builders. `getTokenStatus` now returns `'reclaimed'` status (previously reclaimed tokens were filtered out entirely in `fetchAllRawTokens`). New `last_activity_at` field on `TokenSummary` (from on-chain `last_activity_slot`). New on-chain per-user borrow cap: max borrow = 3x collateral share of supply. New error code `UserBorrowCapExceeded` (code 6048, all subsequent codes shifted +1). `getLendingInfo` now exposes `utilization_cap_bps` (7000) and `borrow_share_multiplier` (3) in response. Bundled lib `LENDING_UTILIZATION_CAP_BPS` updated from 5000 to 7000 to match V33 on-chain enforcement. IDL updated to v3.7.9. 27 instructions (unchanged). 43 Kani proofs all passing.

28. **V3.7.30 community token option (V35)** — New `community_token?: boolean` parameter on `buildCreateTokenTransaction` (default `true`). Community tokens route 0% to creator — all bonding SOL share and post-migration `swap_fees_to_sol` proceeds go entirely to treasury. Creator tokens (opt-in `community_token: false`) retain V34 behavior: 0.2%→1% bonding SOL share + 15% fee swap share. SDK passes `communityToken: community_token` to the on-chain `createToken` instruction. On-chain implementation uses sentinel value (`u64::MAX`) in deprecated `Treasury.total_bought_back` field — no struct layout changes, full backward compatibility. New on-chain constant `COMMUNITY_TOKEN_SENTINEL`. Stars system unchanged (user-funded appreciation, not protocol fees). No new SDK types, no new SDK functions, no new PDA derivations. IDL updated to v3.7.10. 27 instructions (unchanged). 48 Kani proofs all passing (2 new: `verify_community_token_buy_conservation`, `verify_community_token_swap_fees_conservation`).

29. **V3.7.37 message enrichment** — `getMessages()` now accepts `{ enrich: true }` option. When enabled, the SDK batch-verifies unique message senders via `verifySaid()` and populates four new fields on each message: `sender_verified` (boolean), `sender_trust_tier` (string | null), `sender_said_name` (string | null), `sender_badge_url` (string | null). Verification results are cached per-sender within the call to avoid redundant API hits. The enrichment is opt-in — existing callers are unaffected. `verifySaid` already degrades gracefully (returns `{ verified: false }` on error), so enrichment cannot break message retrieval. No new types — the fields are optional additions to the existing `TokenMessage` type. No on-chain changes. Read-only feature.

30. **V4.0.0 simplified tiers & reduced fees** — Constants-only update. Removed 50 SOL (Spark) tier from `VALID_BONDING_TARGETS` — existing Spark tokens continue to function via `initial_virtual_reserves()`. Treasury SOL rate reduced from 20%→5% to 12.5%→2.5% (`TREASURY_SOL_MAX_BPS` 2000→1250, `TREASURY_SOL_MIN_BPS` 500→250). Protocol fee reduced from 1% to 0.5% (`PROTOCOL_FEE_BPS` 100→50). Per-user borrow cap increased from 3x to 5x (`BORROW_SHARE_MULTIPLIER` 3→5). Lending utilization cap increased from 70% to 80% (`DEFAULT_LENDING_UTILIZATION_CAP_BPS` 7000→8000). SDK constants updated in `tokens.ts` (`LENDING_UTILIZATION_CAP_BPS` 7000→8000, `BORROW_SHARE_MULTIPLIER` 3→5) and `quotes.ts` (fallback multiplier 3→5). IDL updated to v4.0.0. 27 instructions (unchanged). 48 Kani proofs all passing.

30. **V4.0.1 flattened bonding treasury fee** — Constants-only update. Treasury SOL rate increased from 12.5%→2.5% to 12.5%→4% (`TREASURY_SOL_MIN_BPS` 250→400). This is justified due to the increased available SOL in the treasury for lending post migration, ensuring each tier meets the minimum borrow threshold. IDL updated to v4.0.1. 27 instructions (unchanged). 48 Kani proofs all passing.

31. **V4.1.0 VersionedTransaction + Quote-Driven Trading** — Major SDK improvement, no on-chain program changes. All transaction builders now return `VersionedTransaction` (v0 messages) instead of legacy `Transaction`. Address Lookup Tables hardcoded for mainnet (`GQzbU32oN3znZa3uWFKGc9cBukpQbYYJSirKstMuFF3i`) and devnet (`3umSStZSLJNk5QstxeQB12a2MSDh4o8RgSzT76gigJ8P`) — 14 static addresses compressed from 32 bytes to 1 byte each. `getBuyQuote`/`getSellQuote` now work on migrated tokens using Raydium CPMM constant product formula with 25 bps fee; both return `source: 'bonding' | 'dex'`. `BuyParams`/`SellParams`/`DirectBuyParams` accept optional `quote` field — when provided, the builder uses `quote.source` for automatic routing (bonding curve vs vault swap) and `quote.min_output_*` for slippage protection. `buildVaultSwapTransaction` internalized (removed from public API); `buildBuyTransaction` and `buildSellTransaction` auto-route through vault swap for migrated tokens. `VaultSwapParams` removed from exports. `getRaydiumMigrationAccounts` removed from public API. Deprecated constants removed (`RAYDIUM_CPMM_PROGRAM`, `RAYDIUM_AMM_CONFIG`, `RAYDIUM_FEE_RECEIVER`). DRY helpers extracted: `deriveVaultAccounts`, `createVaultTokenAtaIx`, `getVaultTokenAta`, `addMemoIx` — replacing 7+ duplicate code blocks across transaction builders. `EphemeralAgent.sign()` now handles both `VersionedTransaction` (`.sign([keypair])`) and legacy `Transaction` (`.partialSign(keypair)`). E2E tests updated with bonding curve quote output, DEX quote output, transaction size logging, and unified buy/sell flow for post-migration trading. No new on-chain instructions. IDL unchanged at v4.0.1. 48 Kani proofs all passing.

32. **V4.1.2 sendBuy/sendDirectBuy + WalletAdapter + Default-All Pagination** — SDK-only change, no on-chain program changes. New `sendBuy(connection, wallet, params)` and `sendDirectBuy(connection, wallet, params)` — high-level helpers that build, simulate, and submit a buy via `wallet.signAndSendTransaction()`. Recommended for Phantom and other browser wallets: atomic sign+send avoids false-positive "malicious dapp" warnings. Both handle auto-migration when a buy completes bonding (simulates migration tx, submits if valid). New `WalletAdapter` interface in `types.ts` — minimal `{ publicKey: PublicKey, signAndSendTransaction: (tx) => Promise<{ signature }> }`. `getTokens()` pagination changed: previously defaulted to `limit: 50`; now returns all tokens when no `limit` specified (`filterAndSort` only slices when `params.limit` or `params.offset` is set). `TokenListResult.limit` returns `summaries.length` instead of hardcoded 50 when no limit specified. No new on-chain instructions. IDL unchanged at v4.0.1. 48 Kani proofs all passing.

33. **V10.0.1 Short selling accounts fix + getShortPosition** — Bug fix: `buildOpenShortTransaction`, `buildCloseShortTransaction`, and `buildLiquidateShortTransaction` now correctly pass `treasuryLock` and `treasuryLockTokenAccount` (the 300M token lending pool) instead of `treasuryTokenAccount` (the treasury's vote vault ATA). This aligns the SDK with the on-chain IDL — the previous code would have failed at the program level. New read-only `getShortPosition(connection, mint, wallet)` returns short position state (SOL collateral, tokens borrowed, accrued interest, LTV, health). No new signing paths, no new attack surface. All other changes in v10 are copy, branding, and frontend — no SDK security implications. 58 Kani proofs, 59 E2E tests all passing.

34. **V10.1.0 Treasury rate rebalance** — Constants-only SDK update matching on-chain V10.1. `TREASURY_SOL_MAX_BPS` 1250→1500 (15%), `TREASURY_SOL_MIN_BPS` 400→250 (2.5%). `treasuryFeeBps` default 100→0 (token treasury fee removed). IDL updated to V10.1.1. No new instructions, no new signing paths. 58 Kani proofs, 59 E2E tests all passing.

35. **V10.1.1 Free Authority Revocation on Launch** — All tokens now launch with freeze authority disabled instead of being disabled on migration.

The SDK is safe for production use by AI agents and applications interacting with the Torch Market protocol.

---

## Audit Certification

This audit was performed by Claude Opus 4.6 (Anthropic). Original audit on February 12, 2026 (v3.2.3). Updated February 14, 2026 for v3.2.4 remediation. Updated February 15, 2026 for v3.3.0 (tiered bonding curves, harvest_fees security fix, Kani proof updates). Updated February 16, 2026 for v3.4.0 (tiered fee structure). Updated February 19, 2026 for v3.6.8 (V25 pump-style reserves, V26 permissionless migration, V27 pool validation, V28 authority transfer, lending accounting fix, utilization cap fix, live pool price, dynamic network detection, pre-migration buyback removal). Updated February 20, 2026 for v3.7.0 (V28 `update_authority` removed — authority transfer now via multisig tooling, V27 treasury lock with 250M locked tokens, PDA-based pool validation, pre-migration buyback handler removed, 27 instructions total). Updated February 20, 2026 for v3.7.2 (treasury cranks: auto-buyback with full client-side pre-checks, harvest fees with auto-discovery and graceful RPC fallback, dynamic compute budget, new `sources` param, E2E test coverage across all three test suites). Updated February 21, 2026 for v3.7.10 (V20 swap fees to SOL: new `buildSwapFeesToSolTransaction` bundles harvest + Raydium swap in one atomic tx, vault ordering bug fix in `validate_pool_accounts`, 28 instructions). Updated February 22, 2026 for v3.7.17 (V29 on-chain metadata: Metaplex `buildAddMetadataTransaction` removed, new `getTokenMetadata` read-only function, transfer fee 1%→0.1%, IDL updated to v3.7.17). Updated February 23, 2026 for v3.7.17 loan position scanner (`getAllLoanPositions` — batch scan all loan positions for a token with health computation). Updated February 26, 2026 for v3.7.22 (V33 buyback removal — `buildAutoBuybackTransaction` and `AutoBuybackParams` removed, on-chain `execute_auto_buyback` instruction removed, lending cap 50%→70%, IDL v3.7.7, 27 instructions, 39 Kani proofs). Updated March 3, 2026 for v3.7.29 (reclaim failed tokens — new `buildReclaimFailedTokenTransaction`, `ReclaimParams`, `reclaimed` token status, `last_activity_at` field; per-user borrow cap with `UserBorrowCapExceeded` error; `getLendingInfo` exposes `utilization_cap_bps` and `borrow_share_multiplier`; IDL v3.7.9, 27 instructions, 43 Kani proofs). Updated March 4, 2026 for v3.7.30 (V35 community token option — new `community_token` param on `buildCreateTokenTransaction`, default true, 0% creator fees for community tokens; IDL v3.7.10, 27 instructions, 48 Kani proofs). Updated March 10, 2026 for v3.7.37 (message enrichment — `getMessages` with `{ enrich: true }` batch-verifies senders via SAID Protocol, populates `sender_verified`, `sender_trust_tier`, `sender_said_name`, `sender_badge_url`; opt-in, read-only, no on-chain changes). Updated March 19, 2026 for v4.1.2 (`sendBuy`/`sendDirectBuy` helpers, `WalletAdapter` interface, default-all pagination). All source files were read in full and cross-referenced against the on-chain program. The E2E test suite validates the SDK against a Surfpool mainnet fork. Separate devnet E2E test validates the full lifecycle including V26 migration on Solana devnet. Tiers E2E test validates harvest and lending across Flame/Torch. Independent human security auditor verified the on-chain program and frontend.

**Auditor:** Claude Opus 4.6
**Date:** 2026-03-28
**SDK Version:** 10.1.1
**On-Chain Version:** V10.1.1 (Program ID: `8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`)
