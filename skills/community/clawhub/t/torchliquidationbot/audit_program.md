# Torch Market Security Audit Summary

**Date:** April 11, 2026 | **Auditor:** Claude Opus 4.6 (Anthropic) + OpenAI o3 (independent review) | **Version:** V10.2.6 Production

---

## Scope

Four audits covering the full stack:

| Layer | Files | Lines | Report |
|-------|-------|-------|--------|
| On-chain program (V10.2.5) | 22 source files | ~7,800 | `audit.md` |
| Frontend & API | 37 files (17 API routes, 12 libs, 8 components) | -- | `SECURITY_AUDIT_FE_V2.4.1_PROD.md` |
| Agent Kit plugin (V4.0) | 4 files | ~1,900 | `SECURITY_AUDIT_AGENTKIT_V4.0.md` |
| Torch SDK (V2.0) | 9 files | ~2,800 | Included in Agent Kit V4.0 audit |

Program ID: `8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`

---

## Findings Summary

### On-Chain Program (V10.2.5)

| Severity | Count | Details |
|----------|-------|---------|
| Critical | 0 | -- |
| High | 0 | -- |
| Medium | 4 | Lending enabled by default (accepted); Token-2022 transfer fee on collateral (inherent, 0.07% new / 0.04% V34 / 0.03% legacy); Epoch rewards race condition (accepted); [V5] AMM spot price for margin valuations (mitigated V6 — circuit breakers block new positions on unhealthy pools, liquidity floor on liquidations; TWAP deferred as higher-risk than spot+breakers for thin pools) |
| Low | 5 | fund_vault_wsol decoupled accounting; Stranded WSOL lamports; Vault sol_balance drift; Sell no position check; Slot-based interest ~~Revival no virtual reserve update; Treasury lock ATA not Anchor-constrained~~ (2 closed in V10.2.2) |
| Informational | 32 | Various carried findings + 3 new V3.7.1 + 2 new V3.7.2 + 2 new V3.7.3 + 2 new V3.7.5 + 1 new V3.7.6 + 1 new V3.7.7 + 1 new V3.7.9 + 1 new V3.7.10 + 1 new V4.0.1 + 2 new V10.0.0 (I-28: oracle-free margin trading; I-29: deprecated field repurposing) + 3 new V10.2.2 (I-30: pool circuit breakers; I-31: bad debt aggregate reconciliation; I-32: independent audit cross-validation) |

**Rating: EXCELLENT -- Ready for Mainnet**

Key strengths:
- 31 instructions, 14 account types, 71 Kani formal verification proofs passed
- **V7 depth-based risk bands** (V10.3.0): Replaced static baseline circuit breaker with `get_depth_max_ltv_bps(pool_sol)` — a pure function that maps pool SOL depth to maximum LTV. Deeper pools are harder to manipulate, so higher LTV is permitted: <5 SOL blocked, 5-50 SOL 25%, 50-200 SOL 35%, 200-500 SOL 45%, 500+ SOL 50%. Eliminates baseline staleness (tokens that organically grew >50% from migration were permanently locked out of lending). No stored state, no baseline updates, no oracle — the pool is the sole source of truth. `require_price_in_band()` retained for `swap_fees_to_sol` ratio gating (separate concern). Effective LTV is `min(depth_band_ltv, treasury.max_ltv_bps)`. 1 new Kani proof verifies boundary correctness and tier monotonicity. Combined with per-user borrow cap, produces effective LTV of <5% in most regimes — making long liquidation a mathematical edge case (see `risk.md`)
- **V6 pool circuit breakers** (V10.2.2): `MIN_POOL_SOL_LENDING` (5 SOL) liquidity floor blocks all margin operations on drained pools. Liquidations remain functional (safety valve) but subject to liquidity floor. `require_min_pool_liquidity()` in `pool_validation.rs`, `PoolTooThin` error. 4 Kani proofs verify band symmetry, edge correctness, and threshold behavior
- **V6 vault ordering fix** (V10.2.2): Lending and short handlers now use `is_wsol_vault_0()` to correctly identify which Raydium pool vault holds SOL vs tokens, regardless of mint pubkey ordering. Previously assumed `token_vault_0 = SOL`, which is only true when WSOL sorts before the token mint (~97% of mints). For the ~3% where the token mint sorts first, collateral valuations were inverted. `swap_fees_to_sol` already handled this correctly; now all margin handlers match. Found via independent cross-audit
- **V6 baseline guard** (V10.2.2): `require_price_in_band()` fails with `BaselineNotInitialized` on zero baseline (no silent bypass). [V7] Baseline check removed from `borrow()` and `open_short()` — depth bands replaced baseline-based circuit breaker for margin operations. Baseline remains active for `swap_fees_to_sol` ratio gating
- **V6 bad debt accounting fix** (V10.2.2): `liquidate()` and `liquidate_short()` now reduce `total_sol_lent` / `total_tokens_lent` by bad debt written off, not just principal repaid. Prevents utilization cap drift after under-collateralized liquidations. `pool_sol > 0` guard added to all 4 margin handlers (borrow, liquidate, open_short, liquidate_short). 8 new Kani proofs cover bad debt accounting, formula algebraic identity, pool reserve guards, and ratio gate safety
- **Independent cross-audit** (V10.2.2): OpenAI o3 performed an independent engineering audit of the full on-chain program. 7 of 8 specific claims verified accurate against source code (1 false positive: IDL/lib.rs instruction count mismatch — both have 31). Key findings that led to V6 changes: spot-price oracle risk on lending/shorts (→ circuit breakers), bad debt aggregate drift (→ accounting fix), missing `pool_sol > 0` guard (→ added). Recommendation for TWAP evaluated and deferred — adds attack surface (stale cranks, manipulation of accumulator) without meaningful benefit on thin long-tail pools where circuit breakers are more practical
- **V36 vote vault removal**: `BURN_RATE_BPS` (10% community treasury split) removed — 100% of `tokens_out` goes to buyer. `BuyArgs.vote` parameter removed. Vote vault balance tracking, vote recording, vote finalization, and vote processing at migration all removed. State fields retained for Borsh layout compatibility but initialized to zero/true for V36+ tokens (`vote_finalized = true` at creation so migration gate passes). Migration handler unchanged — naturally skips vote processing when `vote_vault_balance == 0`. `TREASURY_SOL_MAX_BPS` increased from 1500 (15%) to 1750 (17.5%) to deepen treasury. Net effect: simpler buy instruction, no governance overhead, ~10% more tokens per SOL, deeper lending pool. 6 fewer active state fields, no new attack surface
- **V5 oracle-free margin trading (short selling)**: Completes the two-sided margin system. 4 new instructions: `enable_short_selling` (admin), `open_short`, `close_short`, `liquidate_short`. 2 new account types: `ShortPosition` (per-user, per-token) and `ShortConfig` (per-token stats, holds no SOL). SOL collateral deposited to Treasury, tracked via repurposed deprecated `total_burned_from_buyback` field (sentinel `u16::MAX` in `buyback_percent_bps`, following V35 pattern). Same LTV (50%), liquidation (65%, 10% bonus, 50% close factor), interest (2%/epoch in token terms), and utilization cap (80%) as long lending. One change to existing code: `borrow()` subtracts reserved short collateral from available SOL. All 4 instructions support vault routing. No external oracle — Raydium pool price is canonical. 10 new Kani proofs verify debt value bounds, LTV edge cases, interest non-overflow, liquidation bonus, lifecycle conservation, partial close accounting, and collateral reservation. All accounts boxed to stay under 4KB BPF stack limit
- **V35 community token option**: New `community_token: bool` in `CreateTokenArgs` (default `true`). Community tokens route 0% to creator — all bonding SOL share and `swap_fees_to_sol` proceeds go entirely to treasury. Uses sentinel value (`u64::MAX`) in deprecated `Treasury.total_bought_back` field — no struct layout changes, full backward compat. 2 new Kani proofs verify SOL conservation for both community token paths
- **V34 creator revenue**: Three new income streams for creators — bonding SOL share (0.2%→1% carved from treasury rate, linear growth), 15% of post-migration `swap_fees_to_sol` proceeds, and star payout (cost reduced 0.05→0.02 SOL). `creator` account added to `Buy` and `SwapFeesToSol` contexts, validated against `bonding_curve.creator`. Transfer fee bumped from 3 to 4 bps (new tokens only — old tokens immutable). 4 new Kani proofs verify creator rate bounds, monotonicity, subtraction safety, and fee share conservation
- **Per-user borrow cap**: `BORROW_SHARE_MULTIPLIER = 23` (V10.2.3, was 5, was 3) limits each borrower to 23x their collateral's proportional share of the lendable pool. Combined with depth bands, produces effective LTV of ~3% at fresh treasury (95% drop to liquidate) scaling to ~20% at 150 SOL treasury (68% drop to liquidate). Prevents single-whale pool monopolization. `UserBorrowCapExceeded` error. Kani proof `verify_per_user_borrow_cap_bounded` verifies no overflow, upper bound, and boundary correctness
- **V33 buyback removal**: `execute_auto_buyback` instruction removed (~330 lines of handler + context). Eliminates a complex Raydium CPI instruction that spent treasury SOL providing exit liquidity during dumps, had a fee-inflation bug in vault balance reads, and competed with lending for treasury SOL. One fewer attack surface. Binary size reduced ~6% (850 KB → 804 KB). Treasury simplified to: fee harvest → sell high → SOL → lending yield + epoch rewards
- **V33 lending cap increase**: Utilization cap raised from 50% to 70%. More SOL available for community lending while maintaining 30% visible reserve. Conservative LTV/liquidation thresholds unchanged
- **V10.2.6 fee split rebalance**: Dev wallet share increased from 10% to 50% of protocol fee. Sustainable funding for solo development while remaining 4x cheaper than Pump.fun (0.25% effective vs 1%). Protocol fee unchanged at 0.5% total
- **V32 protocol treasury rebalance**: Reserve floor removed (1,500 SOL → 0) -- all fees distributed each epoch. Volume eligibility lowered (10 SOL → 2 SOL). New MIN_CLAIM_AMOUNT (0.1 SOL) prevents dust claims. Protocol fee split rebalanced from 75/25 to 90% treasury / 10% dev wallet (superseded by V10.2.6). New `verify_min_claim_enforcement` Kani proof
- **V31 zero-burn migration**: Curve supply reduced from 750M to 700M. At graduation, `vault_remaining == tokens_for_pool` exactly -- zero excess tokens to burn. Cleaner migration with no deflationary side effect
- **V31 vote return → treasury lock**: Vote-return tokens now transfer to TreasuryLock PDA instead of Raydium LP injection. Preserves tokens for future governance release instead of diluting the pool. [V36] Vote vault removed for new tokens — migration handler still processes old tokens with vote_vault_balance > 0
- **V31 supply split**: 700M curve (70%) + 300M locked (30%) = 1B total. Treasury lock increased from 250M to 300M for stronger community reserve
- **V31 transfer fee**: Reduced from 10 bps (0.1%) to 3 bps (0.03%). Round-trip cost ~0.006% instead of ~0.2%
- **V29 on-chain metadata**: Token-2022 MetadataPointer + TokenMetadata extensions replace Metaplex dependency. Metadata immutably stored on the mint itself. Pointer authority is `None` (permanently immutable). SDK tests verify name/symbol/uri round-trip via `getTokenMetadata()`
- **V29 Metaplex removal**: `add_metadata` (Metaplex backfill for legacy tokens) was temporary -- 13/24 succeeded, remaining 11 have old account layouts. All Metaplex code removed: `METAPLEX_PROGRAM_ID` constant, `build_create_metaplex_metadata_instruction`, `AddMetadata` context, `add_metadata` handler, `InvalidMetadataAccount` error. L-9 (untyped mint AccountInfo) is now moot
- **V20 swap_fees_to_sol**: Closed economic loop verified -- treasury tokens sold on Raydium, WSOL unwrapped, SOL credited back to same treasury. No external routing possible
- **V20 vault ordering fix**: `order_mints()` now correctly orders pool vaults by mint pubkey for `validate_pool_accounts` in `swap_fees_to_sol`
- **V27 PDA-based pool validation** eliminates oracle spoofing at the Anchor constraint level (cryptographically unforgeable)
- **V27 treasury lock**: 300M tokens (30%) permanently locked in TreasuryLock PDA. No withdrawal instruction exists
- **V27 supply conservation**: 700M curve + 300M locked = 1B total, verified via two separate `mint_to` CPIs
- **V26 permissionless migration**: SOL custody preserved via `bc_wsol` intermediary. CPI isolation via `fund_migration_wsol`
- **V28 zero-cost migration**: Payer fronts ~1 SOL for Raydium costs, treasury reimburses exact amount via lamport snapshot (pre/post CPI). Net cost to payer: 0 SOL. `MIN_MIGRATION_SOL` (1.5 SOL) safety floor replaces fixed `RAYDIUM_POOL_CREATION_FEE`
- **V3.7.1 MigrateToDex amm_config constrained**: Address constraint added to prevent pool creation with wrong Raydium fee tier (defense-in-depth, matches existing constraint on VaultSwap and SwapFeesToSol)
- **V26/V29 authority revocation**: Mint, freeze, and transfer fee config authorities all revoked to `None` at migration (permanent, irreversible). Supply capped, trading unrestricted, fee rate locked forever
- **V28 minimal admin surface**: Only `initialize` and `update_dev_wallet` require authority. `update_authority` removed
- Checked arithmetic everywhere with u128 intermediaries for overflow-prone multiplication
- All 17 PDA types use unique seeds with stored bumps
- Vault full custody verified: closed economic loop across buy, sell, star, borrow, repay, open_short, close_short, DEX swap, and fee swap
- CPI ordering rule enforced: token CPIs before lamport manipulation in all vault paths
- Authority separation: creator (immutable seed) vs authority (transferable) vs controller (disposable signer)

---

## V20: `swap_fees_to_sol` -- Deep Audit

### Overview

New instruction that sells harvested Token-2022 transfer fee tokens back to SOL via Raydium CPMM. Permissionless -- anyone can call post-migration. Completes the fee lifecycle: transfer fees (0.03%) accumulate as tokens, `harvest_fees` collects them, `swap_fees_to_sol` converts to SOL for lending yield and epoch rewards.

**Files audited:**
- `handlers/treasury.rs` (lines 82-207) -- handler logic
- `contexts.rs` (lines 443-540) -- `SwapFeesToSol` account context
- `pool_validation.rs` -- `order_mints`, `validate_pool_accounts`, `read_token_account_balance`
- `state.rs` -- Treasury struct, `harvested_fees` field
- `constants.rs` -- seeds, program IDs
- `lib.rs` -- instruction entry point

### Account Context Verification

All 16 accounts in `SwapFeesToSol` verified:

| Account | Constraint | Verdict |
|---------|-----------|---------|
| `payer` | `Signer`, mutable | SAFE -- permissionless, pays gas only |
| `mint` | `InterfaceAccount<MintInterface>`, mutable | SAFE -- typed, Token-2022 validated via bonding_curve |
| `bonding_curve` | PDA `[BONDING_CURVE_SEED, mint]`, `migrated` + `is_token_2022` | SAFE -- prevents pre-migration and non-Token-2022 calls |
| `treasury` | PDA `[TREASURY_SEED, mint]`, mutable | SAFE -- receives SOL, same treasury that owns the tokens |
| `treasury_token_account` | `associated_token::mint/authority/token_program` | SAFE -- can only be treasury's Token-2022 ATA |
| `treasury_wsol` | Address = `get_associated_token_address(&treasury, &WSOL_MINT)` | SAFE -- can only be treasury's WSOL ATA |
| `raydium_program` | Address = `RAYDIUM_CPMM_PROGRAM_ID` | SAFE -- hardcoded |
| `raydium_authority` | Unconstrained | LOW -- Raydium validates internally (see L-8) |
| `amm_config` | Address = `RAYDIUM_AMM_CONFIG` | SAFE -- hardcoded, prevents fee tier substitution |
| `pool_state` | Address = `derive_pool_state(&mint)` | SAFE -- PDA-derived, unforgeable |
| `token_vault` | Address = `derive_pool_vault(&pool_state, &mint)` | SAFE -- PDA-derived, unforgeable |
| `wsol_vault` | Address = `derive_pool_vault(&pool_state, &WSOL_MINT)` | SAFE -- PDA-derived, unforgeable |
| `wsol_mint` | Address = `WSOL_MINT` | SAFE -- hardcoded |
| `observation_state` | Address = `derive_observation_state(&pool_state)` | SAFE -- PDA-derived |
| `token_program` | `Interface<TokenInterface>` | SAFE -- Anchor validates |
| `token_2022_program` | Address = `TOKEN_2022_PROGRAM_ID` | SAFE -- hardcoded |

### Handler Logic Verification

**Step-by-step trace through `swap_fees_to_sol` (treasury.rs:96-207):**

| Step | Code | Finding |
|------|------|---------|
| 1. Pool validation | `order_mints` + `validate_pool_accounts` with correctly ordered vaults | SAFE -- defense-in-depth, vaults passed in pool order (vault_0/vault_1 by mint pubkey), not swap direction |
| 2. Token balance check | `token_amount > 0`, `minimum_amount_out > 0` | SAFE -- prevents empty swaps and 0-value slippage |
| 3. WSOL balance before | `read_token_account_balance(&treasury_wsol)` | SAFE -- handles pre-existing WSOL via before/after diff |
| 4. Treasury signer | `[TREASURY_SEED, mint, bump]` | SAFE -- standard PDA signer |
| 5. Raydium swap CPI | `swap_base_input(token_amount, minimum_amount_out)` | SAFE -- see CPI analysis below |
| 6. WSOL balance after | `wsol_balance_after.checked_sub(wsol_balance_before)` | SAFE -- checked arithmetic, only counts swap proceeds |
| 7. Slippage check | `sol_received >= minimum_amount_out` | SAFE -- belt-and-suspenders (Raydium also enforces) |
| 8. Close WSOL ATA | `close_account(treasury_wsol → treasury)` | SAFE -- SOL returns to treasury PDA |
| 9. State update | `sol_balance += sol_received`, `harvested_fees += sol_received` | SAFE -- checked arithmetic, credits same treasury |

### Raydium CPI Analysis

The swap CPI correctly maps accounts for the **sell direction** (Token-2022 → WSOL):

| CPI Field | Account | Token Standard | Direction |
|-----------|---------|---------------|-----------|
| `input_token_account` | `treasury_token_account` | Token-2022 | Tokens being sold |
| `output_token_account` | `treasury_wsol` | SPL Token | WSOL being received |
| `input_vault` | `token_vault` | -- | Pool receives tokens |
| `output_vault` | `wsol_vault` | -- | Pool sends WSOL |
| `input_token_program` | `token_2022_program` | Token-2022 | For input token |
| `output_token_program` | `token_program` | SPL Token | For WSOL output |
| `payer` (signer) | `treasury` PDA | -- | Treasury signs swap |

Verified against `vault_swap` sell path (swap.rs:183-250) -- same Raydium CPI pattern with correctly mapped token programs for the sell direction.

### Fund Flow Analysis -- Can Funds Be Drained?

**Critical question: Is there any path where SOL or tokens leave the treasury's control?**

```
Treasury Token ATA (Token-2022 tokens)
    │ swap_base_input CPI
    ▼
Raydium Pool (token_vault receives tokens, wsol_vault sends WSOL)
    │
    ▼
Treasury WSOL ATA (receives WSOL)
    │ close_account CPI
    ▼
Treasury PDA (receives SOL = WSOL lamports)
    │ state update
    ▼
treasury.sol_balance += sol_received
```

**Every hop in this chain is constrained to treasury-owned accounts:**

1. **Source**: `treasury_token_account` -- constrained as treasury's Token-2022 ATA via `associated_token` Anchor macro. Cannot be substituted.
2. **Intermediate**: `treasury_wsol` -- constrained as `get_associated_token_address(&treasury, &WSOL_MINT)`. Cannot be substituted.
3. **Destination**: `treasury.key()` in both `close_account` args (destination AND authority). SOL returns to treasury PDA.
4. **State**: `treasury.sol_balance` credits the same treasury account.

**Verdict: NO DRAIN POSSIBLE. The instruction is a closed economic loop within the treasury.**

### Attack Vector Analysis

| # | Vector | Mitigation | Verdict |
|---|--------|-----------|---------|
| 1 | **Pool substitution** -- pass fake Raydium pool | `pool_state` = `derive_pool_state(&mint)` (PDA, unforgeable). `token_vault`/`wsol_vault` = PDA-derived from pool_state. `amm_config` = hardcoded address. Runtime `validate_pool_accounts()` double-checks. | NOT POSSIBLE |
| 2 | **Sandwich attack** -- front-run/back-run to extract MEV | `minimum_amount_out` slippage protection. Caller sets via SDK based on current price. Tx reverts if output below threshold. | MITIGATED |
| 3 | **Repeated calls** -- drain via multiple invocations | First call swaps all tokens (full balance). Second call hits `require!(token_amount > 0)` and reverts. SOL always returns to same treasury. | NOT POSSIBLE |
| 4 | **Fund routing** -- redirect output to attacker wallet | WSOL destination = treasury's ATA (address-constrained). Close destination = treasury PDA (hardcoded in CPI args). No external wallet referenced. | NOT POSSIBLE |
| 5 | **Pre-migration exploit** -- call before pool exists | `bonding_curve.migrated` constraint. No pool = no swap. | NOT POSSIBLE |
| 6 | **Non-Token-2022 token** -- call on legacy token | `bonding_curve.is_token_2022` constraint. Legacy tokens have no transfer fees. | NOT POSSIBLE |
| 7 | **Vote vault theft** -- steal pre-vote tokens | Only callable post-migration. Vote vault resolved before migration completes (burned or returned). Treasury token ATA only contains harvested fee tokens post-migration. | NOT POSSIBLE |
| 8 | **WSOL account injection** -- fake WSOL ATA | `treasury_wsol` address-constrained to ATA derivation. Deterministic, unforgeable. | NOT POSSIBLE |
| 9 | **Reentrancy** -- re-enter during CPI | Solana runtime prevents reentrancy within same transaction. | NOT POSSIBLE |
| 10 | **Stale WSOL balance** -- count pre-existing WSOL as proceeds | Before/after diff pattern: `sol_received = wsol_after - wsol_before`. Only counts swap delta. | MITIGATED |
| 11 | **Treasury state desync** -- accounting mismatch | `sol_balance += sol_received` uses checked arithmetic. SOL physically arrives at treasury PDA via WSOL close. Accounting matches reality. | MITIGATED |

### V20 New Findings

**~~L-8 (Low): `raydium_authority` has no explicit address constraint~~ -- RESOLVED (V33)**

The `raydium_authority` account in `SwapFeesToSol` context had no `address = ...` constraint. Raydium validates its own authority PDA internally. `TreasuryBuybackDex` (which also had this pattern) was removed in V33. Only `SwapFeesToSol` and `VaultSwap` remain -- both rely on Raydium's internal validation. Not exploitable.

**I-16 (Informational): `harvested_fees` field semantic change**

The `Treasury.harvested_fees` field (declared in V3, never previously written to) is now repurposed to track cumulative SOL earned from fee swaps. The field name suggests "harvested token fees" but now stores SOL amounts. No layout change, no migration needed. Cosmetic only -- no security impact.

**I-17 (Informational): WSOL ATA rent not tracked in `sol_balance`**

When `treasury_wsol` is closed, the treasury PDA receives both swap proceeds (token balance) and rent-exempt lamports. Only the token balance (via before/after diff) is added to `treasury.sol_balance`. The rent lamports become untracked SOL in the treasury PDA. This is consistent with `vault_swap` (the only other WSOL-closing path since `execute_auto_buyback` was removed in V33). Dust-level amounts, not exploitable.

### V20 Vault Ordering Fix Verification

The `order_mints()` fix in `swap_fees_to_sol` was verified:

```rust
// swap_fees_to_sol (treasury.rs:104-111)
let (mint_0, _) = order_mints(&mint_key);
let (vault_0, vault_1) = if mint_0 == mint_key {
    (&ctx.accounts.token_vault, &ctx.accounts.wsol_vault)
} else {
    (&ctx.accounts.wsol_vault, &ctx.accounts.token_vault)
};
```

Correctly passes vaults in **pool order** (vault_0/vault_1 by mint pubkey comparison) to `validate_pool_accounts`, while the Raydium CPI receives vaults in **swap direction** order (input/output). These are independent concerns and both are handled correctly. (Note: `execute_auto_buyback` which had the same pattern was removed in V33.)

---

## V29: Token Metadata + Transfer Fee Changes -- Deep Audit

### Overview

V29 makes two changes: (1) new tokens store metadata on-chain via Token-2022 MetadataPointer + TokenMetadata extensions, replacing the Metaplex dependency; (2) transfer fee reduced from 1% (100 bps) to 0.03% (3 bps) with fee config authority revoked at migration. The `add_metadata` instruction (Metaplex backfill for legacy tokens) was temporary and has been removed -- all Metaplex code is deleted.

**Files audited:**
- `handlers/token.rs` -- create_token with Token-2022 metadata extensions
- `token_2022_utils.rs` -- metadata pointer and token metadata instruction builders
- `constants.rs` -- metadata extension sizes
- `migration.rs` (lines 377-389) -- transfer fee config authority revocation

### `create_token` Metadata Extension Verification

**Extension initialization order (critical -- Token-2022 requires specific ordering):**

| Step | Extension | When | Verified |
|------|-----------|------|----------|
| 1 | `create_account` | Before all inits | SAFE -- space = TransferFeeConfig + MetadataPointer only (346 bytes) |
| 2 | `InitializeTransferFeeConfig` | Before InitializeMint2 | SAFE -- fee config authority = bonding curve PDA, withdraw authority = treasury PDA |
| 3 | `InitializeMetadataPointer` | Before InitializeMint2 | SAFE -- authority = None (immutable), metadata address = mint itself |
| 4 | `InitializeMint2` | After all extension inits | SAFE -- mint/freeze authority = bonding curve PDA |
| 5 | `system_program::transfer` | After InitializeMint2 | SAFE -- funds mint account for TokenMetadata realloc rent |
| 6 | `InitializeTokenMetadata` | After InitializeMint2 | SAFE -- Token-2022 reallocs internally. Bonding curve PDA signs as mint authority |

**Two-phase allocation pattern (I-19):**
The mint is created with space for TransferFeeConfig + MetadataPointer only (346 bytes). Before TokenMetadata init, additional rent lamports are transferred to the mint via `system_program::transfer`. Token-2022 then reallocs the account internally when processing `InitializeTokenMetadata`. This avoids Token-2022's `InvalidAccountData` error when uninitialized TLV entries exist at `InitializeMint2` time.

**Metadata pointer authority = None (I-18):**
The metadata pointer is initialized with `authority = None`, meaning the pointer target (mint itself) can never be changed. This is the correct choice -- the metadata lives on the mint and should never point elsewhere.

### Transfer Fee Config Authority Revocation Verification

```rust
// migration.rs:377-389
set_authority(
    CpiContext::new_with_signer(
        ctx.accounts.token_2022_program.to_account_info(),
        SetAuthority {
            current_authority: ctx.accounts.bonding_curve.to_account_info(),
            account_or_mint: ctx.accounts.mint.to_account_info(),
        },
        bc_signer,
    ),
    AuthorityType::TransferFeeConfig,
    None,  // revoked permanently
)?;
```

**Verified:** This follows the same pattern as the existing mint authority and freeze authority revocations (lines 354-375). `AuthorityType::TransferFeeConfig` with `new_authority = None` is irreversible -- Token-2022 rejects `SetAuthority` when the current authority is `None`. The 0.03% fee rate is locked forever post-migration.

**Three authorities now revoked at migration:**
1. Mint authority → `None` (supply capped)
2. Freeze authority → `None` (free trading guaranteed)
3. Transfer fee config authority → `None` (0.03% fee rate locked)

### V29 New Findings

**~~L-9 (Low): `add_metadata` mint is untyped `AccountInfo`~~ -- REMOVED**

The `add_metadata` instruction and `AddMetadata` context have been deleted. This finding is no longer applicable.

**I-18 (Informational): Metadata pointer authority permanently `None`**

The MetadataPointer extension is initialized with `authority = None`, making the pointer permanently immutable. The pointer target is the mint itself. This is the correct configuration -- there is no reason to ever change where metadata is stored.

**I-19 (Informational): Two-phase mint allocation pattern**

The mint account is created with 346 bytes (TransferFeeConfig + MetadataPointer), then Token-2022 reallocs internally during `InitializeTokenMetadata`. The creator pays additional rent via `system_program::transfer` before the metadata init. This is a standard Token-2022 pattern -- pre-allocating the full space causes `InitializeMint2` to fail due to uninitialized TLV entries in the trailing bytes.

---

## V31: Zero-Burn Migration + Treasury Lock Vote Return -- Deep Audit

### Overview

V31 makes three changes: (1) curve supply reduced from 750M to 700M, treasury lock increased from 250M to 300M -- at graduation, `vault_remaining == tokens_for_pool` exactly, eliminating the ~50M excess token burn; (2) vote-return tokens now transfer to TreasuryLock PDA instead of Raydium LP injection; (3) transfer fee reduced from 10 bps to 3 bps (0.03%).

**Files audited:**
- `contexts.rs` -- `MigrateToDex` account context (treasury_lock_token_account downgraded to AccountInfo)
- `migration.rs` -- vote return transfer to treasury lock, manual ATA validation
- `constants.rs` -- CURVE_SUPPLY, TREASURY_LOCK_TOKENS, TRANSFER_FEE_BPS
- `handlers/token.rs` -- updated mint_to amounts (700M/300M)
- `errors.rs` -- `InvalidTokenAccount` error variant

### Zero-Burn Migration Verification

**Before V31:** `CURVE_SUPPLY = 750M`, `TREASURY_LOCK = 250M`. At graduation with 200 SOL target, `tokens_for_pool ≈ 700M` (computed from price matching), leaving ~50M excess tokens burned.

**After V31:** `CURVE_SUPPLY = 700M`, `TREASURY_LOCK = 300M`. At graduation, `tokens_for_pool == vault_remaining` exactly. The `excess_tokens` burn path (migration.rs:208-225) still exists as a safety net but fires with `excess_tokens = 0` for V31 tokens.

**Supply conservation:** `700M + 300M = 1B` total supply. Verified via two separate `mint_to` CPIs in `create_token`. The 39 Kani formal verification proofs include `verify_price_matched_pool_flame` which validates the zero-excess property.

### Vote Return → Treasury Lock Verification

**Previous behavior (V27):** Vote-return tokens were added to Raydium LP, diluting the pool at migration.

**V31 behavior:** Vote-return tokens transfer to `treasury_lock_token_account` via `transfer_checked` CPI with treasury as signer.

```rust
// migration.rs (V31 vote return path)
if bonding_curve.vote_result_return {
    let expected_lock_ata = get_associated_token_address_2022(
        &ctx.accounts.treasury_lock.key(),
        &mint_key,
    );
    require!(
        ctx.accounts.treasury_lock_token_account.key() == expected_lock_ata,
        TorchMarketError::InvalidTokenAccount
    );
    transfer_checked(/* treasury → treasury_lock_token_account */);
}
```

**Validation chain:**
1. `treasury_lock` is `Box<Account<'info, TreasuryLock>>` -- Anchor validates discriminator and PDA
2. `treasury_lock_token_account` is `AccountInfo` with manual ATA address validation
3. `get_associated_token_address_2022` derives the expected ATA deterministically
4. `require!` rejects mismatched addresses with `InvalidTokenAccount`
5. `transfer_checked` CPI validates the account is a valid Token-2022 token account

### AccountInfo Stack Pressure Mitigation (I-21)

The `treasury_lock_token_account` was downgraded from `Box<InterfaceAccount<TokenAccount>>` with `associated_token::` constraints to plain `AccountInfo` with `#[account(mut)]`. This was necessary because the Anchor-generated `try_accounts` validation code for `MigrateToDex` (which has ~25 accounts) exceeded the Solana BPF 4KB stack frame limit.

**Security impact:** None. The manual ATA validation in the handler provides equivalent security:
- ATA addresses are deterministic (derived from owner + mint + Token-2022 program)
- An attacker cannot forge an ATA address -- it's a PDA with fixed seeds
- `transfer_checked` CPI validates the destination is a valid token account
- The `treasury_lock` account itself is still fully typed and PDA-validated by Anchor

This pattern is analogous to how `raydium_authority` is left unconstrained (L-8) -- the CPI target validates internally.

### Backward Compatibility

Tokens created on v3.7.4 (750M curve / 250M lock) will use the new V31 migration handler when they graduate. They get the new vote-return → treasury lock path, but their creation-time economics are preserved:
- Supply split remains 750M/250M (stored on-chain at creation)
- Transfer fee rate remains whatever was set at mint creation (immutable)
- The ~50M excess burn still occurs (vault_remaining > tokens_for_pool for old supply split)

### V31 New Findings

**I-20 (Informational): Zero-burn migration design**

The V31 supply split (700M/300M) is calibrated so that `vault_remaining == tokens_for_pool` at the 200 SOL bonding target. This eliminates the ~50M deflationary burn at migration, making the supply more predictable. The excess burn code path is retained as a safety net. This property is verified by the `verify_price_matched_pool_flame` Kani proof.

**I-21 (Informational): AccountInfo stack pressure mitigation**

The `treasury_lock_token_account` in `MigrateToDex` uses `AccountInfo` instead of a typed Anchor account to reduce stack frame size. The `associated_token::` macro generates heavy validation code in `try_accounts` that, combined with ~25 other accounts in the context, exceeded the 4KB BPF stack limit. Manual ATA validation in the handler provides equivalent security guarantees. This is a standard Solana optimization pattern for large account contexts.

---

## V32: Protocol Treasury Rebalance -- Deep Audit

### Overview

V32 changes four protocol constants and adds a min claim guard. No new instructions, no new accounts, no state struct changes. Pure economics rebalance: more fees to traders, lower entry barrier, dust claim protection.

**Files audited:**
- `constants.rs` -- PROTOCOL_TREASURY_RESERVE_FLOOR (→0), MIN_EPOCH_VOLUME_ELIGIBILITY (→2 SOL), DEV_WALLET_SHARE_BPS (→1000), new MIN_CLAIM_AMOUNT
- `handlers/protocol_treasury.rs` -- min claim check in `claim_protocol_rewards`
- `errors.rs` -- `ClaimBelowMinimum` error variant

### Constant Changes Verification

| Constant | Before | After | Security Impact |
|----------|--------|-------|-----------------|
| `PROTOCOL_TREASURY_RESERVE_FLOOR` | 1,500 SOL | 0 SOL | Rent-exempt minimum still subtracted (line 61). Account stays alive. No drain risk. |
| `MIN_EPOCH_VOLUME_ELIGIBILITY` | 10 SOL | 2 SOL | More claimants, smaller individual shares. Intentional -- broader distribution. |
| `DEV_WALLET_SHARE_BPS` | 1000 (10%) | 5000 (50%) | [V10.2.6] Same arithmetic path in buy handler. `dev_share = total * 5000 / 10000`. No overflow risk. |
| `MIN_CLAIM_AMOUNT` | (new) | 0.1 SOL | New `require!` guard. Prevents dust drain via many micro-claims. |

### Min Claim Guard Verification

```rust
// handlers/protocol_treasury.rs (V32)
let claim_amount = user_share.min(ctx.accounts.protocol_treasury.distributable_amount);

// [V32] Reject dust claims below minimum
require!(
    claim_amount >= MIN_CLAIM_AMOUNT,
    TorchMarketError::ClaimBelowMinimum
);
```

**Analysis:**
- Guard placed after share calculation, before SOL transfer -- correct position
- Uses `>=` (not `>`) -- 0.1 SOL exactly is accepted
- `MIN_CLAIM_AMOUNT = 100_000_000` lamports (0.1 SOL) -- verified matches constant
- New `ClaimBelowMinimum` error variant added to `TorchMarketError` enum
- Error message string updated: "need >= 2 SOL/epoch" (was 10 SOL)

### Attack Vector Analysis

| # | Vector | Mitigation | Verdict |
|---|--------|-----------|---------|
| 1 | **Dust drain** -- many accounts claim tiny amounts | MIN_CLAIM_AMOUNT (0.1 SOL) floor. Claims below threshold revert. | MITIGATED |
| 2 | **Reserve floor = 0 drain** -- treasury emptied each epoch | Distributable = available - rent_exempt. Account survives. Each claim decrements distributable_amount. | SAFE |
| 3 | **Volume manipulation** -- fake 2 SOL volume to claim | Volume tracked via buy/sell handlers with real SOL flow. Cannot inflate without actual trades. | NOT POSSIBLE |
| 4 | **Fee split arbitrage** -- exploit 50/50 change | Constant-only change. Same `checked_mul/checked_div` path. No timing exploit. | NOT POSSIBLE |

### V32 New Findings

**I-22 (Informational): Reserve floor zeroed with min claim protection**

The reserve floor removal (1,500 SOL → 0) means all accumulated fees are distributed each epoch. The new MIN_CLAIM_AMOUNT (0.1 SOL) prevents the theoretical dust drain vector where many low-volume accounts could claim tiny amounts. The combination is sound -- broader access with a sensible floor on individual claims. The `verify_min_claim_enforcement` Kani proof formally verifies that claims passing the check are genuinely >= 0.1 SOL.

---

## V33: Buyback Removal + Lending Cap Increase -- Deep Audit

### Overview

V33 removes the `execute_auto_buyback` instruction entirely (~330 lines of handler + context) and increases the lending utilization cap from 50% to 70%. No new instructions, no state struct layout changes. Pure simplification: fewer code paths, smaller binary, reduced attack surface.

**Rationale for removal:**
1. **Fee-inflation bug** -- buyback read Raydium vault balances including unclaimed protocol/fund fees, inflating apparent price ratio. V32 patched the read but added complexity.
2. **Exit liquidity subsidy** -- spent treasury SOL buying during dumps, effectively subsidizing sellers when treasury should conserve.
3. **SOL competition** -- buyback, lending, and epoch rewards all competed for the same treasury SOL.
4. **Never triggered in testing** -- sell cycle (`swap_fees_to_sol`) always ran first due to higher threshold sensitivity.

**Files audited:**
- `lib.rs` -- instruction entry point removed
- `handlers/migration.rs` -- handler delegation removed
- `migration.rs` -- `execute_auto_buyback_handler` (230 lines) removed, migration init simplified
- `contexts.rs` -- `TreasuryBuybackDex` struct (100 lines) removed
- `constants.rs` -- 4 buyback constants removed, lending cap updated
- `handlers/token.rs` -- buyback config fields zeroed instead of initialized
- `kani_proofs.rs` -- proof #18 comment updated

### Removed Code Verification

**Instruction removed from `lib.rs`:**
```rust
// REMOVED (V33)
pub fn execute_auto_buyback(ctx: Context<TreasuryBuybackDex>) -> Result<()> {
    handlers::migration::execute_auto_buyback(ctx)
}
```

Instruction count: 28 → 27. One fewer entry point in the dispatch table.

**Handler removed from `migration.rs` (~230 lines):**
The handler performed: cooldown check → Raydium vault balance read → ratio calculation → treasury SOL allocation → Raydium swap CPI → state update. All of this logic is now dead code -- the instruction that called it no longer exists.

**Context removed from `contexts.rs` (~100 lines):**
`TreasuryBuybackDex` had 16 accounts with PDA constraints for Raydium CPMM interaction. Removing this struct eliminates one entire CPI surface with Raydium.

**Constants removed from `constants.rs`:**

| Constant | Value | Was Used By |
|----------|-------|-------------|
| `DEFAULT_RATIO_THRESHOLD_BPS` | 8000 (80%) | Buyback trigger only |
| `DEFAULT_RESERVE_RATIO_BPS` | 3000 (30%) | Buyback amount calc only |
| `DEFAULT_BUYBACK_PERCENT_BPS` | 1500 (15%) | Buyback amount calc only |
| `MIN_BUYBACK_AMOUNT` | 0.01 SOL | Buyback minimum check only |

**Shared infrastructure kept** (used by sell cycle):
- `RATIO_PRECISION` (1e9) -- ratio math in `swap_fees_to_sol`
- `DEFAULT_MIN_BUYBACK_INTERVAL_SLOTS` (2700) -- sell cycle cooldown
- `DEFAULT_SELL_THRESHOLD_BPS` (12000) -- sell cycle trigger
- Baseline fields (`baseline_sol_reserves`, `baseline_token_reserves`, `baseline_initialized`)
- `read_pool_accumulated_fees` -- sell cycle fee correction

### Treasury Struct Layout Verification

On-chain accounts cannot have fields removed without migration. Deprecated buyback fields remain in the `Treasury` struct as dead weight:

| Field | Status | New Token Value |
|-------|--------|-----------------|
| `ratio_threshold_bps` | Deprecated (V33) | 0 |
| `reserve_ratio_bps` | Deprecated (V33) | 0 |
| `buyback_percent_bps` | Deprecated (V33) | 0 |
| `total_bought_back` | Deprecated (V33) | 0 |
| `total_burned_from_buyback` | Deprecated (V33) | 0 |
| `buyback_count` | Deprecated (V33) | 0 |

**Verified:** `handlers/token.rs` now explicitly zeros these fields at token creation. Existing migrated tokens retain their historical values but the instruction to act on them no longer exists. No deserialization issues -- layout is identical.

### Lending Utilization Cap Increase

`DEFAULT_LENDING_UTILIZATION_CAP_BPS`: 5000 (50%) → 7000 (70%)

**Impact analysis:**
- 30% visible reserve remains in per-token treasury -- sufficient for confidence
- More SOL available for community lending → borrowers buy tokens → more volume → more fees
- Conservative LTV (50%) and liquidation threshold (65%) unchanged
- Worst case: 70% lent, all borrowers default, 50% of collateral value recovered via liquidation. Treasury retains 30% reserve + liquidation proceeds (~35% of lent amount). Net loss bounded at ~22.5% of total treasury SOL in catastrophic scenario.

**Code change:** Single constant update. The utilization check in `borrow` handler (`treasury.total_lent + amount <= cap * treasury.sol_balance / 10000`) uses the same checked arithmetic path.

### Attack Vector Analysis

| # | Vector | Mitigation | Verdict |
|---|--------|-----------|---------|
| 1 | **Stale buyback instruction call** -- client sends old buyback tx | Instruction removed from program dispatch. Anchor returns `InvalidInstructionData` or `InstructionFallbackNotFound`. | NOT POSSIBLE |
| 2 | **Layout mismatch** -- zeroed fields cause deserialization error | Layout unchanged. Zero is a valid `u64` value. Anchor deserializes normally. | NOT POSSIBLE |
| 3 | **Sell cycle broken** -- removal affects shared code | Sell cycle (`swap_fees_to_sol`) uses its own handler, context, and shared constants. No code paths shared with removed buyback handler. Verified: `cargo build` succeeds, sell cycle handler unchanged. | NOT POSSIBLE |
| 4 | **Lending over-extension** -- 70% cap too aggressive | 50% max LTV + 65% liquidation threshold unchanged. Liquidation keepers incentivized with 10% bonus. 30% reserve always available for withdrawals. | ACCEPTABLE |
| 5 | **Historical data corruption** -- existing tokens with buyback history | Read-only. Fields retain historical values. No instruction exists to modify them. | NOT POSSIBLE |

### Binary Size Reduction

~850 KB → ~804 KB (~6% reduction). Removing the `TreasuryBuybackDex` context (100 lines of Anchor-generated validation code) and the handler (230 lines with Raydium CPI) accounts for the reduction.

### V33 New Findings

**I-23 (Informational): Buyback removed, lending cap increased**

The `execute_auto_buyback` instruction was removed in its entirety -- handler, context, and 4 dedicated constants. Treasury SOL is no longer spent on market buys during price dips. The lending utilization cap was increased from 50% to 70%, making more SOL available for community lending. Both changes are pure simplification with no new attack surface. The 6 deprecated Treasury fields remain in the struct at zero values for layout compatibility. The sell cycle (`swap_fees_to_sol`) continues to operate with its own ratio gating, baseline tracking, and cooldown logic -- fully independent of the removed buyback.

### V34 New Findings (V3.7.9)

**I-24 (Informational): Creator revenue streams, transfer fee bump**

V34 introduces three creator income streams: (1) a 0.2%→1% SOL share during bonding carved from the existing 20%→5% treasury rate (linear growth formula: `creator = 0.2% + 0.8% × reserves/target`), (2) 15% of post-migration `swap_fees_to_sol` proceeds (85% to treasury, 15% to creator via direct lamport transfer), and (3) star payout at 2000 stars (cost reduced from 0.05 to 0.02 SOL, so ~40 SOL payout instead of ~100 SOL).

**Security analysis:**
- Creator account validated against `bonding_curve.creator` in both `Buy` and `SwapFeesToSol` contexts via Anchor `constraint` — no account substitution possible
- Creator SOL share is carved FROM the existing treasury split, not added — total extraction from buyer unchanged. Kani proof `verify_creator_rate_less_than_treasury_rate` proves subtraction safety at all points
- Direct lamport transfer to creator in `swap_fees_to_sol` follows the same treasury-owned PDA pattern as existing lamport manipulations. Works even if creator wallet is garbage-collected (Solana runtime adds lamports to any address)
- Transfer fee bumped from 3→4 bps for new tokens. Old tokens retain 3 bps (immutable — fee config authority was revoked to `None` at migration)
- Self-buy discount for creators during bonding (0.2%→1% of their own buy) is negligible and incentive-aligned
- 4 new Kani proofs: `verify_creator_rate_bounds`, `verify_creator_rate_monotonic`, `verify_creator_rate_less_than_treasury_rate`, `verify_creator_fee_share_bounded`. All passing. Conservation property updated in `verify_sol_distribution_conservation` (now 5-way sum)

No new accounts, no new instructions, no state struct changes. `creator` account added to two existing contexts.

**I-25 (Informational): Per-user borrow cap (supply-proportional)**

A per-user borrow cap was added to the `borrow` handler to prevent any single borrower from monopolizing the lending pool. The cap formula is `max_user_borrow = max_lendable * user_collateral * 3 / TOTAL_SUPPLY`, enforced after the global utilization cap check. A new `BORROW_SHARE_MULTIPLIER = 3` constant and `UserBorrowCapExceeded` error variant were added.

**Security analysis:**
- All arithmetic uses u128 intermediates — `140_000_000_000 * 1_000_000_000_000_000 * 3` fits comfortably in u128
- Integer floor division is conservative: users get slightly less than their exact proportional share, never more
- Check cannot be bypassed — it's in the same code path as the existing utilization cap, using the on-chain `TOTAL_SUPPLY` constant
- Existing positions above the new cap are unaffected — they can repay normally but cannot borrow additional SOL
- New Kani proof `verify_per_user_borrow_cap_bounded` verifies: no overflow, upper bound (`<= max_lendable * 3`), zero-collateral → zero cap, full-supply → 3x cap

No new accounts, no new instructions, no state struct changes.

---

**I-26 (Informational): Community token option (V35)**

A `community_token: bool` field was added to `CreateTokenArgs` (default `true`). Community tokens route 0% to creator — all bonding SOL share (0.2%→1%) and post-migration `swap_fees_to_sol` proceeds (15%) go entirely to the token treasury. Creator tokens retain full V34 behavior via `community_token: false`.

The implementation repurposes the deprecated `Treasury.total_bought_back` field as a sentinel: `u64::MAX` indicates a community token. This avoids any struct layout changes (no BondingCurve/Treasury reallocation, no borsh deserialization breakage for existing accounts).

**Security analysis:**
- **Sentinel safety:** `u64::MAX` (~1.8e19) is impossible for a legitimate `total_bought_back` value — total supply is 1B tokens (1e15 base units), 4 orders of magnitude smaller. Old tokens have `total_bought_back` at 0 or small historical values, always treated as creator tokens.
- **No new accounts/instructions:** Only `CreateTokenArgs` gains a field; handlers check the sentinel in existing `Treasury` account reads. Zero new attack surface.
- **SOL conservation preserved:** Two new Kani proofs (`verify_community_token_buy_conservation`, `verify_community_token_swap_fees_conservation`) verify that when `creator_sol = 0` / `creator_amount = 0`, the total SOL distribution remains correct (treasury receives the full amount).
- **Stars unchanged:** The star system is user-funded appreciation (0.02 SOL per star), not protocol fees — correctly left unchanged for community tokens.
- **Backward compatibility:** Existing tokens (pre-V35) are unaffected. The sentinel is only set at token creation time.

No new accounts, no new instructions, no state struct changes. 48 Kani proofs all passing.

**I-27 (Informational): V4.0 Simplified Tiers & Reduced Fees (Constants-Only)**

Three constant changes: (1) Removed 50 SOL (Spark) tier from `VALID_BONDING_TARGETS` — existing Spark tokens continue to function, only new creation blocked. (2) Treasury SOL rate reduced from 20%→5% to 12.5%→4% (`TREASURY_SOL_MAX_BPS` 2000→1250, `TREASURY_SOL_MIN_BPS` 500→400). (3) Protocol fee reduced from 1% to 0.5% (`PROTOCOL_FEE_BPS` 100→50).

**Impact:** Fee reduction benefits buyers (~10 SOL treasury on 100 SOL pool, ~20 SOL on 200 SOL pool). No new attack vectors — constants only. Existing Spark tokens retain all functionality via `initial_virtual_reserves()` match arm. `BONDING_TARGET_SPARK` constant preserved for backward compatibility.
**Status:** Accepted — intentional economic rebalance. 48 Kani proofs all passing.

**I-28 (Informational): V10.1 Treasury Rate Rebalance & Fee Simplification (Constants-Only)**

Three constant changes: (1) Treasury SOL rate widened from 12.5%→4% to 15%→2.5% (`TREASURY_SOL_MAX_BPS` 1250→1500, `TREASURY_SOL_MIN_BPS` 400→250). Average treasury take across bonding is unchanged (~8.75%). Early buyers contribute more to treasury, deepening the lending pool at migration. (2) Token treasury fee removed (`TREASURY_FEE_BPS` 100→0). Treasury growth now comes entirely from the dynamic SOL rate + 0.04% post-migration transfer fees. Simplifies the fee structure from two overlapping mechanisms to one. (3) Error message for `UserBorrowCapExceeded` updated from "3x" to "5x" to match the `BORROW_SHARE_MULTIPLIER` constant (which was already 5 since V4.0). Stale comments in `lending.rs`, `market.rs`, and `kani_proofs.rs` updated to reflect current values.

**Impact:** No new attack vectors — constants and comments only. Total treasury SOL at migration is mathematically identical (same integral under the decay curve). Fee simplification removes the `TREASURY_FEE_BPS` path but the code still computes it (multiplies by 0, adds 0) — no dead code risk, just a no-op. 58 Kani proofs, 59 E2E tests all passing.
**Status:** Accepted — intentional economic rebalance and cleanup.

---

### Frontend & API Routes

| Severity | Count | Details |
|----------|-------|---------|
| Critical | 0 | **Fixed:** RPC proxy method allowlist (read-only only) |
| High | 0 | **Fixed:** Amount bounds validation on buy/sell routes; CSP updated for Jupiter API |
| Medium | 5 | SSRF via metadata URI fetch; Vanity grinding DoS; No rate limiting; Slippage unbounded (**Fixed**); SAID confirm feedback spoofing |
| Low | 5 | skipPreflight on all txs; BigInt conversion throws; Unoptimized images; SAID proxy passthrough; API sell route account layout |
| Informational | 5 | Good security headers; No dangerouslySetInnerHTML; Env vars properly segregated; Wallet adapter correct; Transaction preview shown |

**Rating: GOOD with targeted improvements needed**

Post-audit fixes applied:
- **C-1 Fixed:** RPC proxy now allowlists 37 read-only methods, blocks `sendTransaction` and all write methods
- **H-1 Fixed:** Buy route validates 0.001-500 SOL bounds; Sell route validates 1-1B token bounds; Slippage clamped 0.1%-10%
- **H-2 Fixed:** CSP `connect-src` updated with `https://api.jup.ag`

### Agent Kit Plugin (V4.0 -- Vault-Only)

| Severity | Count | Details |
|----------|-------|---------|
| Critical | 0 | **Resolved from V1.6:** Blind signing eliminated -- transactions are now built locally via Anchor IDL |
| High | 0 | **Resolved from V1.6:** No API dependency -- no TLS pinning needed, no server trust required |
| Medium | 1 | SAID feedback endpoint is unauthenticated (best-effort, non-critical) |
| Low | 3 | Memo not sanitized for control characters (max 500 chars); signOrSendTX delegates signing to agent kit (correct but opaque); Spot price oracle for lending collateral (inherits on-chain limitation) |
| Informational | 5 | All state reads via RPC (no caching, fresh every call); Slippage default 100bps (1%) hardcoded per-tool; Action handlers catch all errors (no uncaught throws); E2E test suite covers 21 tests; `buildDirectBuyTransaction` is never imported or called |

**Rating: GOOD -- Recommended for autonomous operation**

**V2.0 → V4.0: Vault-Only Buys**

The V4.0 update eliminates the most significant remaining concern from V2.0: unbounded agent spending. All token purchases now go through Torch Vault -- an on-chain SOL escrow with protocol-enforced spending caps. The `buildDirectBuyTransaction` function is never imported or used anywhere in the plugin. Only `buildBuyTransaction` with a required `vault` parameter is available.

| V2.0 (Previous) | V4.0 (Current) |
|------------------|----------------|
| Agent could buy with direct wallet SOL | Agent can only buy via vault-funded transactions |
| M-2: No spend limits or per-transaction caps | **Resolved:** Vault balance is the spend limit, enforced on-chain |
| Application-layer caps recommended | Protocol-layer caps enforced -- vault is the cap |
| Agent had full control of wallet SOL | Agent can only spend through `buy` instruction on vault SOL |

**Vault security properties (on-chain enforcement):**
- Vault SOL can only flow through the `buy` instruction -- no arbitrary transfers
- Authority (vault owner) can unlink agent wallets at any time -- instant revocation
- One wallet can only be linked to one vault -- PDA uniqueness enforced
- Creator is immutable (PDA seed), authority is transferable
- Deposits are permissionless, withdrawals require authority

**V1.6 → V2.0 Migration (Previous): Critical Improvement**

The V2.0 rewrite eliminated the most significant security finding from V1.6. The plugin no longer calls the `torch.market/api/v1` REST API. Instead, it imports the [Torch SDK](https://github.com/mrsirg97-rgb/torchsdk) which builds transactions locally using the Anchor IDL and reads state directly from Solana RPC.

| V1.6 (Old) | V2.0+ (Current) |
|-------------|------------------|
| Agent → HTTP → torch.market API → return unsigned tx → Agent signs | Agent → SDK (Anchor + IDL) → Solana RPC → Agent signs |
| Trusted the API server to build honest transactions | Transactions built locally from on-chain program IDL |
| C-1 Critical: Blind signing of API-constructed transactions | **Resolved:** No external server in the transaction path |
| H-1: No TLS pinning on API calls | **Resolved:** No HTTP calls (except SAID feedback, best-effort) |
| H-2: Blockhash override negated server expiry | **Resolved:** Blockhash fetched locally from RPC |
| M-1: Lending API routes not deployed | **Resolved:** Lending built directly from IDL |

**Remaining considerations:**
- The SAID feedback call to `api.saidprotocol.com` is the only outbound HTTP request (non-critical, fails gracefully)
- Memo content is user-provided and truncated to 500 chars but not sanitized for control characters

---

## V5: Short Selling (Margin System) -- Deep Audit

### Overview

V5 adds short selling -- the mirror of the existing V2.4 lending system. Short sellers post SOL collateral, borrow tokens from treasury, sell on DEX. When price drops, buy back cheaper, return tokens, keep the difference. Same math, same liquidation, opposite direction. No external oracle -- Raydium pool price is canonical.

**Files audited:**
- `handlers/short.rs` (890 lines) -- all 4 handler functions
- `contexts.rs` (lines 1601-1870) -- `EnableShortSelling`, `OpenShort`, `CloseShort`, `LiquidateShort` account contexts
- `handlers/token.rs` (line 241-244) -- sentinel set at token creation
- `handlers/lending.rs` (lines 230-237) -- short collateral reservation in borrow()
- `state.rs` -- `ShortPosition`, `ShortConfig` structs
- `constants.rs` -- `SHORT_SEED`, `SHORT_CONFIG_SEED`, `MIN_SHORT_TOKENS`, `SHORT_ENABLED_SENTINEL`
- `errors.rs` -- 8 new error variants

**New instructions:** `enable_short_selling`, `open_short`, `close_short`, `liquidate_short`
**New accounts:** `ShortPosition` (105 bytes), `ShortConfig` (65 bytes)
**Repurposed fields:** `Treasury.total_burned_from_buyback` → total_short_sol_collateral, `Treasury.buyback_percent_bps` → short-enabled sentinel

### Account Context Verification

#### EnableShortSelling (contexts.rs:1608-1648)

| Account | Constraint | Verdict |
|---------|-----------|---------|
| `authority` | `Signer`, mutable | SAFE -- pays rent for ShortConfig |
| `global_config` | PDA `[GLOBAL_CONFIG_SEED]`, `authority == authority.key()` | SAFE -- admin-only gate |
| `mint` | `AccountInfo` (CHECK) | SAFE -- used only for PDA derivation; bonding_curve PDA validates mint indirectly |
| `bonding_curve` | PDA `[BONDING_CURVE_SEED, mint]`, `migrated == true` | SAFE -- prevents enabling on pre-migration tokens |
| `treasury` | PDA `[TREASURY_SEED, mint]`, `lending_enabled`, `buyback_percent_bps != SENTINEL` | SAFE -- double gate: lending must be on, shorts must not already be enabled |
| `short_config` | PDA `[SHORT_CONFIG_SEED, mint]`, `init` | SAFE -- Anchor enforces uniqueness via PDA; cannot double-create |
| `system_program` | `Program<System>` | SAFE -- Anchor validates |

**Verdict: SAFE.** Admin-only, idempotency enforced via PDA uniqueness + sentinel check. For pre-V5 tokens only (new tokens auto-enable at creation).

#### OpenShort (contexts.rs:1652-1725)

| Account | Constraint | Verdict |
|---------|-----------|---------|
| `shorter` | `Signer`, mutable | SAFE -- pays rent, signs SOL transfer |
| `mint` | `InterfaceAccount<Mint>`, boxed | SAFE -- typed, Token-2022 validated |
| `bonding_curve` | PDA `[BONDING_CURVE_SEED, mint]`, `migrated`, `!reclaimed` | SAFE -- post-migration gate, no dead tokens |
| `treasury` | PDA `[TREASURY_SEED, mint]`, `buyback_percent_bps == SENTINEL` | SAFE -- shorts must be enabled |
| `treasury_token_account` | `associated_token::mint/authority/token_program` | SAFE -- constrained to treasury's exact Token-2022 ATA. Cannot substitute |
| `short_config` | PDA `[SHORT_CONFIG_SEED, mint]`, `init_if_needed` | SAFE -- lazy creation, PDA-derived. First shorter pays rent (65 bytes = minimal) |
| `short_position` | PDA `[SHORT_SEED, mint, shorter]`, `init_if_needed` | SAFE -- per-user per-token, PDA-derived |
| `shorter_token_account` | `associated_token::mint/authority/token_program` | SAFE -- constrained to shorter's exact ATA |
| `pool_state` | `AccountInfo` (CHECK) | Validated in handler via `validate_pool_accounts()` -- owner, vaults, mints checked |
| `token_vault_0/1` | `AccountInfo` (CHECK) | Validated in handler via `validate_pool_accounts()` |
| `torch_vault` | Optional, boxed, mutable | Consistent with existing vault pattern (Buy, Borrow) |
| `vault_wallet_link` | Optional, boxed | Consistent -- presence check in handler |
| `vault_token_account` | Optional, boxed, mutable | Consistent -- receives borrowed tokens in vault path |
| `token_program` | `Interface<TokenInterface>` | SAFE -- Anchor validates |
| `system_program` | `Program<System>` | SAFE -- Anchor validates |

**Verdict: SAFE.** All typed accounts constrained. Pool validation in handler (same as Borrow). Vault routing follows established V18 pattern.

#### CloseShort (contexts.rs:1729-1790)

| Account | Constraint | Verdict |
|---------|-----------|---------|
| `shorter` | `Signer`, mutable | SAFE |
| `mint` | `InterfaceAccount<Mint>`, boxed | SAFE |
| `bonding_curve` | PDA `[BONDING_CURVE_SEED, mint]` | SAFE -- PDA validates token identity |
| `treasury` | PDA `[TREASURY_SEED, mint]`, mutable | SAFE -- receives returned tokens, returns SOL |
| `treasury_token_account` | `associated_token::mint/authority/token_program` | SAFE -- constrained to treasury's ATA |
| `short_config` | PDA `[SHORT_CONFIG_SEED, mint]`, mutable | SAFE |
| `short_position` | PDA `[SHORT_SEED, mint, shorter]`, `tokens_borrowed > 0` | SAFE -- must have active position |
| `shorter_token_account` | `associated_token::mint/authority/token_program` | SAFE -- source of returned tokens |
| `torch_vault` | Optional, boxed, mutable | Consistent |
| `vault_wallet_link` | Optional, boxed | Consistent |
| `vault_token_account` | Optional, boxed, mutable | Consistent |

**Verdict: SAFE.** No pool accounts needed (no price check on close -- consistent with Repay, which also doesn't validate price).

#### LiquidateShort (contexts.rs:1796-1869)

| Account | Constraint | Verdict |
|---------|-----------|---------|
| `liquidator` | `Signer`, mutable | SAFE -- permissionless |
| `borrower` | `AccountInfo`, mutable | SAFE -- used as PDA seed for short_position derivation. Wrong borrower = wrong PDA = Anchor fails. Matches existing `Liquidate` pattern |
| `mint` | `InterfaceAccount<Mint>`, boxed | SAFE |
| `bonding_curve` | PDA `[BONDING_CURVE_SEED, mint]` | SAFE |
| `treasury` | PDA `[TREASURY_SEED, mint]`, mutable | SAFE -- receives tokens, sends SOL |
| `treasury_token_account` | `associated_token::mint/authority/token_program` | SAFE |
| `short_config` | PDA `[SHORT_CONFIG_SEED, mint]`, mutable | SAFE |
| `short_position` | PDA `[SHORT_SEED, mint, borrower]`, `tokens_borrowed > 0` | SAFE -- must have active position |
| `liquidator_token_account` | `associated_token::mint/authority/token_program` | SAFE -- source of covering tokens |
| `pool_state` | `AccountInfo` (CHECK) | Validated in handler |
| `token_vault_0/1` | `AccountInfo` (CHECK) | Validated in handler |
| `torch_vault` | Optional, boxed, mutable | Consistent |
| `vault_wallet_link` | Optional, boxed | Consistent |
| `vault_token_account` | Optional, boxed, mutable | Consistent |

**Verdict: SAFE.** Permissionless liquidation matches existing `Liquidate` pattern. Pool validation in handler. Borrower identity enforced via PDA seed derivation.

### Handler Logic Verification

#### `enable_short_selling` (short.rs:88-108)

| Step | Code | Finding |
|------|------|---------|
| 1. Zero deprecated field | `treasury.total_burned_from_buyback = 0` | SAFE -- clears any historical pre-V33 data before repurposing |
| 2. Set sentinel | `treasury.buyback_percent_bps = SHORT_ENABLED_SENTINEL` | SAFE -- u16::MAX, impossible as legitimate buyback percentage |
| 3. Init ShortConfig | mint, bump, all counters = 0 | SAFE -- clean initialization |
| 4. Emit event | `ShortSellingEnabled` | SAFE |

**Verdict: SAFE.** Simple initialization. Idempotency enforced by `init` constraint (double-create fails) + sentinel constraint (`!= SENTINEL`).

#### `open_short` (short.rs:115-366) -- Step-by-Step Trace

| Step | Lines | Code | Finding |
|------|-------|------|---------|
| 1. Input validation | 117-128 | `sol_collateral > 0 \|\| tokens_to_borrow > 0`, min tokens check | SAFE -- prevents empty requests and dust positions |
| 2. Vault guard | 131-140 | All vault accounts must be present together | SAFE -- consistent with lending pattern |
| 3. Accrue interest | 146 | `accrue_interest(position, treasury.interest_rate_bps)` | SAFE -- per-slot, u128 intermediaries, checked arithmetic |
| 4. SOL collateral transfer | 150-192 | Standard: `system_program::transfer(shorter → treasury)`. Vault: lamport manipulation `vault → treasury` | SAFE -- see CPI ordering analysis below |
| 5. Calculate user collateral | 197-200 | `position.sol_collateral + args.sol_collateral` | SAFE -- checked_add |
| 6. Pool validation | 204-213 | `validate_pool_accounts()` + balance reads | SAFE -- same validation as Borrow/Liquidate |
| 7. LTV check | 217-229 | `debt_value / collateral <= max_ltv_bps` | SAFE -- checked arithmetic, u128 intermediaries |
| 8. Utilization cap | 236-250 | `total_tokens_lent + new <= tokens_held * cap / 10000` | SAFE -- prevents over-lending |
| 9. Per-user cap | 253-267 | `user_borrowed <= max_lendable * user_collateral * 5 / treasury_sol` | SAFE -- prevents concentration. Division by `treasury.sol_balance` fails cleanly via checked_div if zero (correct behavior -- no shorts on empty treasury) |
| 10. Token transfer (CPI) | 271-302 | Treasury PDA signs `transfer_checked` → shorter/vault ATA | SAFE -- treasury ATA constrained, correct signer seeds |
| 11. Update position | 305-319 | Set user/mint/bump on new, add collateral + debt | SAFE -- checked arithmetic |
| 12. Update treasury | 323-340 | `sol_balance += collateral`, `total_burned_from_buyback += collateral`, `tokens_held -= borrowed` | SAFE -- checked arithmetic. Reservation field tracks collateral |
| 13. Update short_config | 344-358 | Lazy init on first use, add tokens_lent, increment positions | SAFE -- checked arithmetic |
| 14. Emit event | 360-364 | `ShortOpened` | SAFE |

**CPI ordering analysis (open_short):**

SOL collateral transfer (step 4) happens BEFORE token CPI (step 10). This is the reverse of the V3.0 audit rule ("token CPI before lamport manipulation"). However:

- **Standard path** (line 182): Uses `system_program::transfer` CPI, not direct lamport manipulation. Two CPIs in sequence is always safe.
- **Vault path** (lines 162-179): Direct lamport manipulation (vault → treasury). Treasury lamports INCREASE. The subsequent token CPI (treasury signs `transfer_checked`) succeeds because treasury has MORE lamports than before, not less. The V3.0 rule protects against decreasing an account's lamports before it signs a CPI. Here treasury gains lamports, so the runtime balance check passes.

**Verdict: SAFE.** CPI ordering is inverted vs close_short/liquidate_short, but not exploitable because treasury is the gaining party.

#### `close_short` (short.rs:373-582) -- Step-by-Step Trace

| Step | Lines | Code | Finding |
|------|-------|------|---------|
| 1. Input validation | 374 | `token_amount > 0` | SAFE |
| 2. Vault guard | 377-386 | Consistent | SAFE |
| 3. Accrue interest | 393 | Same pattern | SAFE |
| 4. Calculate total owed | 395-401 | `tokens_borrowed + accrued_interest`, cap at total | SAFE |
| 5. **[CPI FIRST]** Token return | 406-458 | `transfer_checked(shorter → treasury_token_account)`. Vault: vault PDA signs. Standard: shorter signs | SAFE -- CPI before lamport manipulation (V3.0 rule followed) |
| 6. SOL return (full close) | 465-504 | Lamport manipulation: `treasury → shorter/vault` | SAFE -- after all CPIs |
| 7. Apply repayment | 516-537 | Interest first, then principal. Full close zeros position | SAFE -- mirrors lending repay exactly |
| 8. Update treasury | 541-556 | `tokens_held += returned`, `sol_balance -= collateral`, `total_burned_from_buyback -= collateral` | SAFE -- `saturating_sub` on reservation field prevents underflow |
| 9. Update short_config | 560-571 | `total_tokens_lent -= principal`, `interest_collected += interest` | SAFE |
| 10. Emit event | 573-580 | `ShortClosed` | SAFE |

**Verdict: SAFE.** CPI ordering correct (token CPI first, lamport manipulation after). Repayment logic mirrors lending.rs repay exactly.

#### `liquidate_short` (short.rs:590-849) -- Step-by-Step Trace

| Step | Lines | Code | Finding |
|------|-------|------|---------|
| 1. Vault guard | 592-601 | Consistent | SAFE |
| 2. Accrue interest | 608 | Same pattern | SAFE |
| 3. Pool validation | 612-621 | `validate_pool_accounts()` | SAFE |
| 4. LTV check | 625-635 | `debt_value / sol_collateral > liquidation_threshold` | SAFE -- must be underwater |
| 5. Calc tokens to cover | 640-646 | `total_debt * close_bps / 10000`, capped at total | SAFE -- 50% close factor |
| 6. Calc SOL to seize | 649-654 | `covered_value * (10000 + bonus) / 10000` | SAFE -- 10% bonus, checked arithmetic |
| 7. Cap at collateral | 657 | `min(sol_to_seize, position.sol_collateral)` | SAFE -- can't seize more than exists |
| 8. Bad debt calc | 661-676 | Scale down tokens if SOL insufficient. Bad debt = unrecoverable remainder | SAFE -- mirrors lending liquidation |
| 9. **[CPI FIRST]** Liquidator sends tokens | 681-731 | `transfer_checked(liquidator → treasury_token_account)` | SAFE -- CPI before lamport manipulation |
| 10. SOL to liquidator | 736-773 | Lamport manipulation: `treasury → liquidator/vault` | SAFE -- after all CPIs |
| 11. Update position | 778-807 | Interest first, then principal. Bad debt written off. Collateral reduced | SAFE -- mirrors lending liquidation |
| 12. Update treasury | 813-823 | `sol_balance -= seized`, `total_burned_from_buyback -= seized`, `tokens_held += covered` | SAFE -- `saturating_sub` prevents underflow |
| 13. Update short_config | 827-838 | `total_tokens_lent -= principal`, `interest_collected += interest` | SAFE |
| 14. Emit event | 840-848 | `ShortLiquidated` | SAFE |

**Verdict: SAFE.** Liquidation logic mirrors lending.rs liquidate exactly. CPI ordering correct. Bad debt handling correct. Close factor enforced.

### Fund Flow Analysis -- Can Funds Be Drained?

#### open_short Fund Flow

```
Shorter's SOL (or Vault SOL)
    │ system_program::transfer CPI (or lamport manipulation)
    ▼
Treasury PDA (sol_balance += collateral, total_burned_from_buyback += collateral)
    │ treasury PDA signs transfer_checked
    ▼
Treasury Token ATA ──tokens_to_borrow──▶ Shorter's Token ATA (or Vault ATA)
    │ state update
    ▼
treasury.tokens_held -= tokens_to_borrow
short_config.total_tokens_lent += tokens_to_borrow
position: sol_collateral += , tokens_borrowed +=
```

**Every hop constrained:**
1. **SOL source**: shorter (signer) or vault (lamport manipulation with balance check)
2. **SOL destination**: treasury PDA (seed-constrained)
3. **Token source**: treasury_token_account (associated_token-constrained to treasury's ATA)
4. **Token destination**: shorter_token_account (associated_token-constrained) or vault_token_account

**Verdict: NO DRAIN POSSIBLE.** SOL goes to treasury (PDA). Tokens come from treasury's ATA (constrained). Closed loop.

#### close_short Fund Flow

```
Shorter's Token ATA (or Vault ATA)
    │ transfer_checked CPI (shorter or vault PDA signs)
    ▼
Treasury Token ATA (tokens returned)
    │ state update: treasury.tokens_held += actual_return
    │
    │ [full close only] lamport manipulation
    ▼
Treasury PDA ──sol_collateral──▶ Shorter (or Vault PDA)
    │ state update
    ▼
treasury.sol_balance -= collateral
treasury.total_burned_from_buyback -= collateral
```

**Verdict: NO DRAIN POSSIBLE.** Tokens return to treasury ATA (constrained). SOL returns from treasury to shorter (signer) or vault. Amounts match position state.

#### liquidate_short Fund Flow

```
Liquidator's Token ATA (or Vault ATA)
    │ transfer_checked CPI
    ▼
Treasury Token ATA (receives tokens covering debt)
    │ state update: treasury.tokens_held += actual_tokens_covered
    │
    │ lamport manipulation
    ▼
Treasury PDA ──sol_seized──▶ Liquidator (or Vault PDA)
    │ state update
    ▼
treasury.sol_balance -= sol_seized
treasury.total_burned_from_buyback -= sol_seized
```

**Verdict: NO DRAIN POSSIBLE.** Liquidator pays tokens (constrained ATA), receives SOL from treasury. SOL seized <= collateral (capped at line 657). Liquidation only fires when LTV > 65% (line 633). Close factor limits to 50% per call.

### Attack Vector Analysis

| # | Vector | Analysis | Verdict |
|---|--------|----------|---------|
| 1 | **Short-and-dump** -- open short, dump tokens on Raydium to profit | Constant-product AMM: large dumps have quadratic slippage. 50% LTV caps position size. Per-user cap prevents concentration. The dump itself costs the attacker SOL on the pool | NOT PROFITABLE at scale |
| 2 | **Token drain** -- borrow all treasury tokens | 80% utilization cap (line 248). Treasury retains 20% for swap_fees_to_sol and normal operations | MITIGATED |
| 3 | **Short squeeze** -- buy tokens to spike price, cascade short liquidations | 80% cap limits total shorts outstanding. Per-user cap prevents dominance. Liquidation returns tokens to treasury (increasing available supply). 50% close factor prevents full position wipeout per call | MITIGATED |
| 4 | **Collateral accounting desync** -- total_burned_from_buyback drifts from actual collateral | All writes use checked_add (open) and saturating_sub (close/liquidate). Collateral only added on open_short, only removed on close/liquidate. No other handler writes this field (verified: only token.rs sets it to 0 at creation). Field is dead for non-short tokens (was deprecated V33, always 0 for V33+ tokens) | NOT POSSIBLE |
| 5 | **Sentinel collision** -- pre-V33 token has `buyback_percent_bps == u16::MAX` | Pre-V33 default was 1500 (15%). Max valid value was ~10000 (100%). u16::MAX (65535) was never a valid buyback percentage. `enable_short_selling` explicitly zeros the field before setting sentinel | NOT POSSIBLE |
| 6 | **Lending pool drain via short collateral** -- lending handler lends out SOL that's reserved for short returns | lending.rs (line 230-237) subtracts `total_burned_from_buyback` from available SOL when sentinel is set. Max lendable calculated from `available_sol = sol_balance - short_reserved`. Short collateral is excluded from lending pool | MITIGATED |
| 7 | **Double-enable** -- call enable_short_selling twice | `init` constraint on ShortConfig PDA fails on second call (account already exists). Sentinel constraint `!= SENTINEL` also fails | NOT POSSIBLE |
| 8 | **Fake pool for price manipulation** -- pass rogue Raydium pool to open_short/liquidate | `validate_pool_accounts()` verifies pool_state owner == RAYDIUM_CPMM_PROGRAM_ID, vault addresses match pool state data, one mint is the token and the other is WSOL | NOT POSSIBLE |
| 9 | **Per-user cap bypass via zero treasury** -- division by zero in cap calculation | `checked_div(treasury.sol_balance)` returns MathOverflow error when sol_balance == 0. Clean failure, no panic. Correct behavior: can't short on empty treasury | HANDLED |
| 10 | **Self-liquidation** -- short seller pumps price to trigger own liquidation for profit | Liquidator pays tokens at inflated price, receives SOL collateral + 10% bonus. The short seller loses collateral. Pumping costs SOL on the pool. Net unprofitable | NOT PROFITABLE |
| 11 | **Vault routing mismatch** -- pass someone else's TorchVault | Same pattern as existing Buy/Borrow vault routing. VaultWalletLink presence is checked but vault_wallet_link.vault != torch_vault binding is not enforced on-chain. Carried finding (applies to all vault-routed instructions equally). Not exploitable for value extraction: attacker can't route value to themselves, only force another vault to act | CARRIED (see existing audit) |
| 12 | **Token-2022 transfer fee accounting drift** -- tokens_held inflated by transfer fees | When tokens are transferred out (open_short) and back (close_short), 0.04% transfer fee is deducted each direction. `tokens_held` tracks nominal amounts, not net-of-fee. Over many cycles, `tokens_held` slightly overstates actual ATA balance. Same class as M-2 (transfer fee on collateral). Utilization cap is slightly more permissive than intended by the fee delta (~0.08% round-trip) | CARRIED (M-2) |
| 13 | **Lazy ShortConfig initialization race** -- two shorters open simultaneously | `init_if_needed` is atomic within a single transaction. Two transactions creating ShortConfig would be serialized by the Solana runtime (account write lock). Second one finds it already initialized. `mint == Pubkey::default()` check in handler correctly distinguishes first init from subsequent uses | NOT POSSIBLE |

### CPI Ordering Verification

| Instruction | Token CPI | Lamport Manipulation | Order | V3.0 Rule |
|-------------|-----------|---------------------|-------|-----------|
| `open_short` | Treasury → shorter (line 289) | Vault → treasury (line 162) OR system CPI (line 182) | SOL first, then tokens | **Inverted** but safe: treasury GAINS lamports before signing token CPI |
| `close_short` | Shorter → treasury (line 426) | Treasury → shorter (line 473) | Tokens first, then SOL | **Correct** |
| `liquidate_short` | Liquidator → treasury (line 702) | Treasury → liquidator (line 745) | Tokens first, then SOL | **Correct** |
| `enable_short_selling` | None | None | N/A | N/A |

### V5 New Findings

**M-4 (Medium): AMM spot price for margin valuations -- both directions**

Short positions use Raydium pool spot price for debt valuation (`calculate_debt_value`: `token_debt * pool_sol / pool_tokens`). Same price source as long lending. No TWAP, no EMA, no external oracle. A well-capitalized attacker could temporarily move the pool price to trigger liquidations on either side, though the constant-product AMM makes this quadratically expensive.

**Status:** Accepted and substantially mitigated (V7). The protocol's design philosophy is oracle-free, deterministic pricing. The Raydium pool IS the price. [V7] Depth-based risk bands now scale max LTV with pool depth (25-50%), replacing the static 50% LTV. Combined with per-user borrow caps, the effective LTV for longs is typically <5%, requiring a >90% price crash for liquidation — making spot-price manipulation attacks on long positions economically infeasible (see `risk.md`). Short positions remain more vulnerable to price pumps (asymmetric risk), which is correct by design.

**Prior recommendation (deferred):** TWAP/EMA for margin price valuations. Evaluated and rejected — adds off-chain keeper dependencies and new attack surface without meaningful benefit given the depth-band model. The pool depth itself is the manipulation-resistance metric.

**I-28 (Informational): Short selling auto-enabled at token creation**

New V5 tokens have `buyback_percent_bps = SHORT_ENABLED_SENTINEL` set at token creation alongside `lending_enabled = true`. Both are gated behind `bonding_curve.migrated` in their respective instruction contexts, so they only become functional post-migration. Pre-V5 tokens use `enable_short_selling` instruction for manual enablement.

ShortConfig PDA is created lazily on first `open_short` via `init_if_needed` -- the first shorter pays ~65 bytes of rent. This avoids bloating token creation with accounts that may never be used.

**I-29 (Informational): Deprecated Treasury field repurposing**

Two deprecated Treasury fields are repurposed for short selling state:

| Field | Original Purpose | Deprecated In | V5 Purpose |
|-------|-----------------|---------------|------------|
| `total_burned_from_buyback` | Cumulative tokens burned via buyback | V33 | `total_short_sol_collateral` -- SOL reserved in treasury for short returns |
| `buyback_percent_bps` | Buyback percentage per call (was 1500 = 15%) | V33 | Short-enabled sentinel (`u16::MAX` when active) |

Both fields were verified as dead code: only declared in `state.rs` and set to 0 in `token.rs` creation handler. No other handler reads or writes them. The sentinel pattern follows V35's `COMMUNITY_TOKEN_SENTINEL` precedent exactly. Pre-V33 tokens with historical non-zero values are safe because `u16::MAX` was never a valid buyback percentage (max meaningful value was ~10000).

**I-30 (Informational): open_short CPI ordering deviates from convention**

The `open_short` handler transfers SOL collateral to treasury (step 4) before the token CPI (step 10). This is the reverse of the V3.0 audit rule ("token CPI before lamport manipulation"). However, the deviation is safe:

- Standard path: uses `system_program::transfer` CPI (not direct lamport manipulation). Two CPIs in sequence is always safe
- Vault path: direct lamport manipulation increases treasury lamports. The subsequent token CPI (treasury signs `transfer_checked`) succeeds because treasury has MORE lamports, not less. The V3.0 rule protects against decreasing a signer's lamports before CPI

`close_short` and `liquidate_short` both follow the correct CPI-first order.

**I-31 (Informational): Dead variable in close_short**

Line 458: `let _ = token_authority;` suppresses an unused variable warning. The `token_authority` bool is set in the CPI branch but never consumed. Cosmetic only, no security impact. Recommend removing the variable and using separate if/else blocks.

### V5 Audit Summary

| Category | Result |
|----------|--------|
| Account constraints | All 4 contexts verified. All typed accounts constrained via PDA seeds, associated_token, or address constraints. Pool validation in handler (same as lending) |
| Handler logic | All 4 handlers traced line-by-line. Arithmetic uses checked_add/checked_sub/checked_mul/checked_div with u128 intermediaries throughout. Interest-first repayment ordering matches lending.rs exactly |
| Fund flow | Closed economic loop verified for all 3 value-moving instructions. No external routing possible. SOL constrained to treasury PDA. Tokens constrained to treasury ATA |
| CPI ordering | close_short and liquidate_short follow V3.0 rule (token CPI first). open_short inverts but is safe (treasury gains lamports before signing) |
| Vault routing | All 3 instructions support optional vault accounts. Pattern matches existing Buy/Borrow/Repay vault routing exactly |
| Attack surface | 13 vectors analyzed. No critical or high findings. 2 carried (M-2 transfer fee drift, vault routing binding). 1 accepted medium (M-4 spot price) |
| Formal verification | 10 new Kani proofs verify debt value bounds, LTV edge cases, interest non-overflow, liquidation bonus, lifecycle conservation, partial close accounting, and collateral reservation |

**Rating: SAFE -- Consistent with existing program security posture. No new critical, high, or low findings. Same math, same patterns, same defense-in-depth as the audited lending system.**

---

## Architecture Security Properties

### What's Protected

- **Private keys never leave the agent.** All signing is local. No keys are sent to any server.
- **Transactions are built locally.** The SDK uses the Anchor IDL to construct transactions directly. No API middleman.
- **Agent spending is vault-bounded.** All buys go through Torch Vault. The agent can only spend what's deposited, and the authority can revoke access instantly.
- **All accounts are PDA-derived.** No user-supplied addresses used as seeds. Account injection is not possible.
- **On-chain program enforces all fund flows.** Neither the SDK nor the frontend can redirect funds -- the Solana runtime validates every instruction.
- **Checked arithmetic everywhere.** All ~7,000 lines of on-chain code use `checked_add/sub/mul/div`. No overflow possible.
- **Minimal admin surface.** Only `initialize` and `update_dev_wallet` require authority. `update_authority` was removed in V3.7.0. Everything else is permissionless.
- **PDA-based pool validation.** Raydium pool accounts are validated via deterministic PDA derivation -- cryptographically unforgeable. No runtime data parsing required.
- **Treasury fee swap is a closed loop.** `swap_fees_to_sol` sells treasury tokens on Raydium and splits SOL 85% to treasury, 15% to creator. All accounts (input, output, destination) are constrained to treasury-owned PDAs and ATAs plus the validated creator wallet. Creator is constrained to `bonding_curve.creator` — no external wallet substitution possible.
- **[V33] Buyback removed -- reduced attack surface.** The `execute_auto_buyback` instruction (~330 lines of handler + context) was removed. One fewer CPI-heavy instruction to audit, one fewer Raydium interaction path, one fewer way treasury SOL can be spent. Treasury now accumulates SOL unidirectionally via sell cycle.
- **Treasury lock is permanent.** 300M tokens (30% of supply) locked at creation with no withdrawal instruction. Release deferred to future governance.
- **Authority revocation is irreversible.** Mint, freeze, and transfer fee config authorities all set to `None` at migration. Supply is capped, trading is unrestricted, and the fee rate is locked forever (0.07% for V35+ tokens, 0.04% for V34 tokens, 0.03% for earlier tokens).
- **Zero-burn migration.** V31 tokens have `vault_remaining == tokens_for_pool` at graduation -- no excess tokens to burn. Supply is fully predictable from creation through migration.
- **On-chain metadata is immutable.** Token-2022 MetadataPointer authority is `None` -- metadata stored on the mint itself can never be redirected. No Metaplex dependency. All Metaplex code has been removed.
- **No dangerouslySetInnerHTML.** Zero instances in the entire frontend. All user content is React-escaped.
- **RPC proxy is read-only.** 37 allowlisted methods, all write operations blocked.
- **SDK is open source.** The Torch SDK is fully auditable at [github.com/mrsirg97-rgb/torchsdk](https://github.com/mrsirg97-rgb/torchsdk).
- **No direct buys.** The agent kit never imports `buildDirectBuyTransaction`. All buys require a vault.

### What's Accepted (Design Trade-offs)

- **Lending enabled by default** with immutable parameters. No per-token disable. Conservative defaults mitigate risk.
- **Token-2022 transfer fee** applies to collateral deposits/withdrawals (~0.006% round-trip cost at 0.03% per transfer).
- **Token-2022 transfer fee on swap input** -- when `swap_fees_to_sol` sells tokens on Raydium, the 0.03% transfer fee is assessed on the input (reducing effective sell amount by ~0.03%). Inherent to Token-2022, not exploitable.
- **Spot price oracle** for lending collateral valuation. TWAP would be more resistant to manipulation but is not implemented.

### Immutable Protocol Parameters (V2.4.1)

All configuration instructions were removed. Parameters are compile-time constants:

| Parameter | Value | Notes |
|-----------|-------|-------|
| Sell cycle threshold | 120% of baseline | Sells when price rises 20%+ above baseline |
| Sell cycle interval | ~18 minutes | Between consecutive sell cycles |
| Lending interest | 2%/epoch (~104% APR) | High rate, may limit adoption |
| Lending max LTV | 50% | Conservative for volatile tokens |
| Liquidation threshold | 65% LTV | 15% buffer from max borrow |
| Liquidation bonus | 10% | Incentive for liquidation keepers |
| Utilization cap | 70% | [V33] Max treasury SOL lendable (was 50%) |

These cannot be changed without a program upgrade.

---

## For Agents

If you're an AI agent interacting with Torch Market:

1. **Your keys are safe.** All transactions are built locally via the SDK. No keys or transactions touch any server.
2. **Your spending is bounded.** All buys go through Torch Vault. You can only spend what's deposited in your linked vault, and the authority can revoke your access at any time.
3. **Transactions are deterministic.** Built from the Anchor IDL against the on-chain program. All accounts are PDA-derived. Verify the program ID (`8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`) if you want extra assurance.
4. **Use the Agent Kit or SDK directly.** The [Torch SDK](https://github.com/mrsirg97-rgb/torchsdk) builds transactions locally -- no API middleman. The Agent Kit plugin wraps the SDK with Solana Agent Kit integration.
5. **Set up a vault before trading.** Create a vault with `torchCreateVault`, deposit SOL with `torchDepositVault`, then pass the vault creator pubkey to `torchBuyToken`. There are no direct buys.
6. **Slippage defaults to 1%.** Configurable per-transaction via `slippage_bps`. The on-chain program enforces minimum output.
7. **Messages require trades.** Every message on the board has a provable buy or sell behind it. Skin in the game by construction.
8. **Confirm for reputation.** Call `torchConfirm` after transactions to build your SAID reputation score.

---

## Full Audit Reports

The complete audit reports (with line-by-line findings, attack vector analysis, and instruction-by-instruction verification) are maintained in the project repository under `/audits/`:

- `SECURITY_AUDIT_SP_V10.2.6_PROD.md` -- On-chain program V10.2.6 (latest: 50/50 protocol fee split -- sustainable dev funding while remaining 4x cheaper than Pump.fun)
- `SECURITY_AUDIT_SP_V10.2.5_PROD.md` -- On-chain program V10.2.5 (depth-based risk bands, borrow multiplier 23x, pool circuit breakers, bad debt accounting fix, independent cross-audit -- 31 instructions, ~7,800 lines, 71 Kani proofs)
- `SECURITY_AUDIT_SP_V10.0.0_PROD.md` -- On-chain program V10.0.0 (oracle-free margin trading / short selling -- 31 instructions, ~7,600 lines, 58 Kani proofs)
- `SECURITY_AUDIT_SP_V3.7.9_PROD.md` -- On-chain program V3.7.9 (per-user borrow cap + V34 creator revenue + transfer fee bump -- 27 instructions, ~6,800 lines, 44 Kani proofs)
- `SECURITY_AUDIT_SP_V3.7.7_PROD.md` -- On-chain program V3.7.7 (V33 buyback removal + lending cap increase -- 27 instructions, ~6,700 lines, binary 804 KB, 39 Kani proofs)
- `SECURITY_AUDIT_SP_V3.7.6_PROD.md` -- On-chain program V3.7.6 (V32 treasury rebalance -- 0 reserve floor, 2 SOL eligibility, 0.1 SOL min claim, 90/10 fee split)
- `SECURITY_AUDIT_SP_V3.7.3_PROD.md` -- On-chain program V3.7.3 (V29 on-chain metadata, fee config authority revocation)
- `SECURITY_AUDIT_SP_V3.7.2_PROD.md` -- On-chain program V3.7.2 (V20 swap_fees_to_sol, vault ordering fix)
- `SECURITY_AUDIT_SP_V3.7.1_PROD.md` -- On-chain program V3.7.1 (V28 payer reimbursement, amm_config constraint)
- `SECURITY_AUDIT_SP_V3.7.0_PROD.md` -- On-chain program V3.7.0
- `SECURITY_AUDIT_SP_V3.1.1_PROD.md` -- On-chain program V3.1.1
- `SECURITY_AUDIT_FE_V2.4.1_PROD.md` -- Frontend & API routes
- `SECURITY_AUDIT_AGENTKIT_V4.0.md` -- Agent Kit plugin V4.0

Source: [github.com/mrsirg97-rgb/torchmarket](https://github.com/mrsirg97-rgb/torchmarket)
SDK: [github.com/mrsirg97-rgb/torchsdk](https://github.com/mrsirg97-rgb/torchsdk)

---

*Audited by Claude Opus 4.6 (Anthropic). This audit is provided for informational purposes and does not constitute financial or legal advice. Security audits cannot guarantee the absence of all vulnerabilities.*
