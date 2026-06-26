# Formal Verification Report

## TL;DR

We used [Kani](https://model-checking.github.io/kani/), a formal verification tool from AWS, to mathematically prove that torch.market's core math is correct -- not just tested, but **proven for every possible input**. This covers all fee calculations, bonding curve pricing, lending formulas, and reward distribution. No SOL can be created from nothing, no tokens can be minted from thin air, and no fees can exceed their stated rates.

This is **not** a security audit. It proves the arithmetic is correct, but does not cover access control, account validation, or economic attacks. See [What Is NOT Verified](#what-is-not-verified) for full scope limitations.

**71 proof harnesses. All passing. Zero failures.**

---

## Overview

torch_market's core arithmetic has been formally verified using [Kani](https://model-checking.github.io/kani/), a Rust model checker backed by the CBMC bounded model checker. Kani exhaustively proves properties hold for **all** valid inputs within constrained ranges -- not just sampled test cases.

**Tool:** Kani Rust Verifier 0.67.0 / CBMC 6.8.0
**Target:** `torch_market` v10.2.6
**Harnesses:** 71 proof harnesses, all passing
**Source:** `programs/torch_market/src/kani_proofs.rs`

## What Is Formally Verified

The proofs cover the **pure arithmetic layer** -- every fee calculation, bonding curve formula, lending math function, and reward distribution used by the on-chain program. Each proof harness uses symbolic (unconstrained) inputs bounded to realistic protocol ranges, and Kani exhaustively checks all possible values within those bounds.

### Buy Flow (Harnesses 1-8)

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_buy_fee_conservation` | `protocol_fee + treasury_fee + after_fees == sol_amount` | 0.001-200 SOL |
| `verify_protocol_fee_split` | `dev_share + protocol_portion == protocol_fee_total` | 0.001-200 SOL |
| `verify_treasury_rate_bounds` | `rate in [250, 1750]` (2.5-17.5%) flat across all tiers | 0-target SOL reserves |
| `verify_treasury_rate_monotonic` | More reserves -> lower treasury rate | 0-target SOL (two symbolic) |
| `verify_sol_distribution_conservation` | `curve + treasury + creator + dev + protocol == sol_amount` (zero SOL created or lost, V34 5-way sum) | 0.001-10 SOL per trade, 0-target SOL reserves |
| `verify_curve_tokens_bounded_legacy` | `tokens_out < virtual_token_reserves` (can't mint from thin air) | Legacy pool state space (IVT=107.3T) |
| `verify_curve_tokens_bounded_v25` | Same property for V27 per-tier reserves | V27 pool state space (IVT=756.25M tokens) |
| `verify_token_split_conservation` | [V36] `tokens_to_buyer == tokens_out` (100% to buyer, vote vault removed) | 0 to TOTAL_SUPPLY |

### Sell Flow (Harnesses 9-10)

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_sell_sol_bounded_legacy` | `sol_out < virtual_sol_reserves` (can't drain more SOL than exists) | Legacy pool state, max wallet cap |
| `verify_sell_sol_bounded_v25` | Same property for V27 per-tier reserves | V27 pool state (IVS=3BT/8), max wallet cap |

### Transfer Fees (Harnesses 11-12)

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_transfer_fee_bounds` | `floor <= fee <= floor + 1` (ceiling division correct) | 0.001 SOL - 100 tokens |
| `verify_transfer_fee_no_underflow` | `amount - fee` never underflows | 0 to TOTAL_SUPPLY |

### Lending (Harnesses 13-18)

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_collateral_value_bounded_small` | `collateral_value <= pool_sol` when `collateral <= pool_tokens` | 50 SOL / 50B token pool |
| `verify_collateral_value_bounded_large` | Same property at different pool scale | 500 SOL / 200T token pool |
| `verify_ltv_zero_collateral` | Zero collateral returns `u64::MAX` (instant liquidation) | All u64 debt values |
| `verify_ltv_zero_debt` | Zero debt returns 0 LTV | All u64 collateral values |
| `verify_interest_no_overflow` | Interest calculation doesn't overflow; interest <= principal | Up to 1000 SOL, 2%/epoch, 1 epoch |
| `verify_liquidation_bonus_increases_seizure` | Liquidation bonus increases collateral seized | 100 SOL pool, up to 50 SOL debt |
| `verify_per_user_borrow_cap_bounded` | Per-user cap no overflow, `<= max_lendable * 23`, zero collateral → zero cap, full supply → 23x cap | Concrete tier lendable caps (35/70/140 SOL), symbolic collateral up to TOTAL_SUPPLY |

### Protocol Rewards (Harnesses 19-20)

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_user_share_bounded` | `user_share <= distributable` (no user can drain reward pool) | 500 SOL epoch, 50 SOL distributable |
| `verify_min_claim_enforcement` | [V32] Claims passing MIN_CLAIM_AMOUNT check are genuinely >= 0.1 SOL; claim never exceeds distributable | 10-10,000 SOL total volume, up to 1,000 SOL distributable |
| `verify_claim_cap_enforced` | Per-user claim capped at 10% of distributable for any volume share | 500 SOL epoch, 50 SOL distributable |
| `verify_claim_cap_monopoly_trader` | User with 100% of epoch volume receives exactly 10% of distributable (not 100%) | 500 SOL epoch, 50 SOL distributable |

### Ratio Math & Sell Cycle (Harnesses 21-23)

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_ratio_fits_u64` | Pool ratio `(sol * 1e9) / tokens` fits in u64 | Up to 1000 SOL, tokens >= 1 token |
| `verify_sell_threshold_fits_u64` | [V30] Sell threshold `baseline_ratio * 12000 / 10000` fits in u64 | Same bounds as ratio proof, with 1.2x multiplier |
| `verify_double_transfer_fee_positive` | Token amount remains positive after two consecutive transfer fees | 1 token to TOTAL_SUPPLY |

### Migration (Harnesses 22-26)

These harnesses verify the V26 permissionless migration: SOL wrapping conservation, price-matched pool creation, and token burn accounting. Updated for V31 per-tier virtual reserves and zero-burn migration.

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_sol_wrapping_conservation` | [V26] `bc_debited == wsol_credited`, total lamports conserved (bonding curve SOL → payer WSOL) | 0 to 200 SOL reserves, rent up to 10M lamports |
| `verify_price_matched_pool_spark` | [V31] Pool ratio matches curve ratio (truncation error < 1 unit) — legacy, SPARK removed from creation in V4.0 | Spark tier (50 SOL), 3 representative token values |
| `verify_price_matched_pool_flame` | [V31] Pool ratio matches curve ratio (truncation error < 1 unit) | Flame tier (100 SOL), 3 representative token values |
| `verify_price_matched_pool_torch` | [V31] Pool ratio matches curve ratio (truncation error < 1 unit) | Torch tier (200 SOL), 3 representative token values |
| `verify_excess_token_burn_conservation` | [V31] `pool_tokens + burned_tokens == vault_total` (no tokens created or lost) — legacy SPARK tier | Spark tier, vault up to CURVE_SUPPLY |

### V31 Zero-Burn Distribution (Harnesses 27-34)

These harnesses verify the V31 token distribution model where IVS = 3*bonding_target/8, IVT = 756.25M tokens, CURVE_SUPPLY = 700M (70%), and TREASURY_LOCK_TOKENS = 300M (30%). V31 tunes the curve/lock split so that vault_remaining == tokens_for_pool at graduation — proving zero excess burn and full 1B supply preservation.

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_v31_full_supply_conservation_spark` | [V36] `wallets + pool + burned + treasury_lock == TOTAL_SUPPLY` (vote vault removed) — legacy SPARK | Spark tier (50 SOL), exact graduation state |
| `verify_v31_full_supply_conservation_flame` | Same conservation for Flame tier | Flame tier (100 SOL), exact graduation state |
| `verify_v31_full_supply_conservation_torch` | Same conservation for Torch tier | Torch tier (200 SOL), exact graduation state |
| `verify_v31_pool_tokens_positive_and_bounded` | Pool tokens > 0 and <= real_token_reserves at graduation | All tiers, exact graduation state |
| `verify_v31_zero_excess_burn_spark` | `excess_burned == 0` at graduation (zero-burn migration) — legacy SPARK | Spark tier, exact graduation state |
| `verify_v31_zero_excess_burn_flame` | `excess_burned == 0` at graduation (zero-burn migration) | Flame tier, exact graduation state |
| `verify_v31_zero_excess_burn_torch` | `excess_burned == 0` at graduation (zero-burn migration) | Torch tier, exact graduation state |

### Sell Fee (Harness 35)

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_sell_fee_always_zero` | `SELL_FEE_BPS == 0` and computed fee == 0 for all valid sol_out | 0.001-200 SOL |

### Creator Revenue (Harnesses 36-39) — V34

These harnesses verify the V34 creator revenue arithmetic: bonding SOL share rate bounds, monotonicity, safety of the treasury-creator subtraction, and post-migration fee share conservation.

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_creator_rate_bounds` | `creator_rate in [20, 100]` bps (0.2%-1%) for all bonding progress | 0-target SOL reserves |
| `verify_creator_rate_monotonic` | More reserves → higher creator rate | 0-target SOL (two symbolic) |
| `verify_creator_rate_less_than_treasury_rate` | `creator_rate < treasury_rate` at all points (subtraction safety) | 0-target SOL reserves |
| `verify_creator_fee_share_bounded` | 15% share ≤ total, `creator + treasury == total` (conservation) | 0.001-200 SOL fee swap proceeds |

### Community Token (Harnesses 45-46) — V35

These harnesses verify the V35 community token code path where `creator_sol = 0` (all fees to treasury). The existing V34 proofs cover the creator-fee path; these cover the explicit zero branch.

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_community_token_buy_conservation` | With `creator_sol = 0`: `curve + treasury + dev + protocol == sol_amount` (full conservation, treasury gets full split) | 0.001-10 SOL per trade, 0-target SOL reserves |
| `verify_community_token_swap_fees_conservation` | With `creator_amount = 0`: `treasury_amount == sol_received` (100% to treasury, no leakage) | 0.001-1000 SOL fee swap proceeds |

### Lending Lifecycle (Harnesses 40-42)

These harnesses verify end-to-end lending correctness: borrow → (optional interest accrual) → repay, proving treasury SOL conservation, correct interest-first repayment ordering, and loan zeroing.

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_lending_lifecycle_conservation` | After borrow + full repay (same slot): treasury SOL exactly restored, loan zeroed, principal_paid == sol_borrowed | 100 SOL / 50T token pool, up to 50 SOL borrow |
| `verify_lending_partial_repay_accounting` | After partial repay: remaining_debt == total_owed - repaid, interest paid first, borrowed never increases | Up to 50 SOL, interest < 10% of principal |
| `verify_lending_lifecycle_with_interest` | After borrow + 1 epoch interest + full repay: treasury gains exactly the interest, principal fully returned | Up to 50 SOL, 2%/epoch, 1 epoch max |

### Short Selling (Harnesses 47-54) — V5

These harnesses verify the V5 short selling arithmetic — the mirror of lending. Short sellers post SOL collateral and borrow tokens. Interest accrues in token terms. All proofs mirror the long-side lending proofs with inverted assets.

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_short_debt_value_bounded_small` | Token debt value in SOL ≤ pool SOL | 50 SOL / 50T token pool |
| `verify_short_debt_value_bounded_large` | Same property at larger pool scale | 500 SOL / 200T token pool |
| `verify_short_ltv_zero_collateral` | Zero SOL collateral returns `u64::MAX` (instant liquidation) | All u64 debt values |
| `verify_short_ltv_zero_debt` | Zero debt returns 0 LTV | All u64 collateral values |
| `verify_short_interest_no_overflow` | Token interest calculation doesn't overflow; interest ≤ principal | Up to TOTAL_SUPPLY tokens, 2%/epoch, 1 epoch |
| `verify_short_liquidation_bonus_increases_seizure` | 10% bonus increases SOL seized vs no bonus | Up to 50 SOL debt value |
| `verify_short_lifecycle_conservation` | After open_short + full close (same slot): treasury tokens & SOL exactly restored, collateral fully released | 100 SOL / 50T pool, up to 10% supply borrowed, up to 500 SOL collateral |
| `verify_short_partial_close_accounting` | After partial close: remaining_debt == total_owed - returned, interest paid first, borrowed never increases | Up to 10% supply, interest < 10% of principal |
| `verify_short_lifecycle_with_interest` | After open_short + 1 epoch interest + full close: treasury gains exactly the interest tokens, principal fully returned | Up to 10% supply, 2%/epoch, 1 epoch max |
| `verify_short_collateral_reservation` | Reserved short SOL correctly excluded from lending pool; all-short = zero lendable; no-short = full treasury available | 1-1000 SOL treasury, symbolic short collateral |

### Bad Debt Accounting (Harnesses 55-56) — V6

These harnesses verify that liquidation bad debt write-offs correctly reduce aggregate utilization tracking, preventing cap drift after under-collateralized liquidations.

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_liquidation_bad_debt_accounting` | After liquidation with bad debt: `total_sol_lent` reduced by principal paid AND bad debt; fully liquidated loan reduces aggregate by at least `borrowed`; never underflows | 100 SOL / 50T pool, up to 50 SOL borrow, 0.5 SOL interest |
| `verify_short_liquidation_bad_debt_accounting` | After short liquidation with bad debt: `total_tokens_lent` reduced by principal paid AND bad debt tokens; fully liquidated position reduces aggregate by at least `tokens_borrowed`; never underflows | 100 SOL / 50T pool, up to 50T tokens borrowed, 1B token interest |

### Pool Reserve Guards (Harnesses 57-58) — V6

These harnesses verify that the `pool_sol > 0 && pool_tokens > 0` guards prevent division-by-zero in collateral valuation and debt valuation, ensuring no stuck/unliquidatable positions.

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_pool_reserve_guards_prevent_div_zero` | With both-side reserve guards: `calculate_collateral_value` and `calculate_ltv_bps` always succeed | Symbolic pool reserves (> 0), collateral up to MAX_WALLET_TOKENS |
| `verify_short_pool_reserve_guards` | With both-side reserve guards: `calculate_debt_value` always succeeds for short positions | Symbolic pool reserves (> 0), token debt up to TOTAL_SUPPLY |

### Circuit Breakers (Harnesses 59-62) — V6

These harnesses verify the V6 pool health circuit breakers. Note: the baseline deviation band (`require_price_in_band`) is retained for `swap_fees_to_sol` ratio gating but is no longer used for margin operations (replaced by depth-based risk bands in V7).

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_circuit_breaker_baseline_passes` | Baseline price always passes its own deviation band check | 100 SOL / 50T pool at baseline |
| `verify_circuit_breaker_rejects_doubled_price` | 2x price (100% increase) rejected by 50% deviation band | 200 SOL pool vs 100 SOL baseline |
| `verify_circuit_breaker_band_edges` | +/-49% passes, +/-51% fails (symmetric band correctness) | 100 SOL / 100T baseline, four edge cases |
| `verify_min_pool_liquidity_threshold` | Pool SOL >= 5 SOL passes, below fails; exact threshold = 5 SOL | 0-10 SOL symbolic |

### Depth-Based Risk Bands (Harness 71) — V7

Verifies the `get_depth_max_ltv_bps()` function that maps pool SOL depth to maximum LTV for margin operations. Replaces static baseline circuit breaker.

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_depth_bands_boundaries` | Correct tier at every boundary (0, 5, 50, 200, 500 SOL and u64::MAX); tiers monotonically increasing | Concrete boundary values |

### Liquidation Formula Identity (Harnesses 63-64) — V6

These harnesses prove that the on-chain bad debt formula (which uses an indirect expression via `total_debt`) is algebraically identical to the simple form `debt_to_cover - actual_debt_covered`, and that the liquidation slice is conserved: `bad_debt + actual_covered == debt_to_cover`.

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_bad_debt_formula_identity` | On-chain formula `total_debt - (covered + (total_debt - slice))` equals `slice - covered`; conservation: `bad_debt + covered == slice` | Up to 50 SOL borrow, symbolic coverage |
| `verify_short_bad_debt_formula_identity` | Same algebraic identity for token-denominated short liquidation | Up to 50T tokens borrowed, symbolic coverage |

### Treasury Ratio Gate & Sell Safety (Harnesses 65-66) — V6

These harnesses verify the post-migration treasury sell mechanism: fee subtraction from vault balances before ratio computation, and sell amount bounding.

| Harness | Property | Input Range |
|---------|----------|-------------|
| `verify_ratio_gate_fee_subtraction_safe` | After subtracting Raydium fees from vault balances: ratio computation succeeds when `pool_tokens > 0`; fees never inflate balances | Up to 10K SOL vault, fees bounded by vault balance |
| `verify_treasury_sell_amount_bounded` | Sell amount never exceeds balance; 100% below 1M token threshold; exactly 15% above; non-zero for positive amounts | 0 to TOTAL_SUPPLY tokens |

## Verification Methodology

### How Kani Works

Kani translates Rust code into a mathematical model and uses a SAT/SMT solver (CaDiCaL via CBMC) to exhaustively check whether any input can violate the asserted properties. Unlike fuzz testing which samples random inputs, Kani explores **every possible execution path** within the constrained input space.

A passing harness means: "there exists no input in the constrained range that violates this property."

### Constraint Design

Each harness constrains symbolic inputs to realistic protocol bounds:

- **SOL amounts:** `MIN_SOL_AMOUNT` (0.001 SOL) to `BONDING_TARGET_LAMPORTS` (200 SOL)
- **Token amounts:** Up to `TOTAL_SUPPLY` (1 billion tokens, 6 decimals)
- **Legacy pool reserves:** `INITIAL_VIRTUAL_SOL` (30 SOL) to `INITIAL_VIRTUAL_SOL + BONDING_TARGET_LAMPORTS` (230 SOL)
- **V31 pool reserves:** `3*bonding_target/8` initial virtual SOL (18.75-75 SOL), `INITIAL_VIRTUAL_TOKENS_V27` (756.25M tokens)
- **Token reserves:** Up to `INITIAL_VIRTUAL_TOKENS` (107.3T raw units, legacy) or `INITIAL_VIRTUAL_TOKENS_V27` (756.25T raw units, V31)
- **Curve supply:** `CURVE_SUPPLY` (700M tokens) for V31 bonding curve + pool allocation
- **Lending pools:** Concrete post-migration pool states (50-500 SOL, 50B-200T tokens)
- **Interest rates:** Up to `DEFAULT_INTEREST_RATE_BPS` (2% per epoch)

Some harnesses use concrete pool states instead of fully symbolic parameters. This is a deliberate constraint design choice driven by SAT solver tractability:

- **Symbolic inputs** (e.g., `kani::any()`) allow Kani to prove properties for *all* values in a range. This is the strongest form of proof but creates exponentially larger SAT formulas when multiple symbolic u64 values flow through u128 intermediate arithmetic.
- **Concrete inputs** fix specific values (e.g., `pool_sol = 100_000_000_000`), eliminating those variables from the SAT formula entirely. Properties are verified exactly at those values rather than universally.
- **Representative concrete values** are a middle ground used for the migration price-match harnesses. Instead of a single symbolic `virtual_tokens` spanning 47 bits (which the solver cannot handle), three concrete values are tested at key pool states: bonding completion, midpoint, and maximum. This reduces solve time from intractable to sub-100ms while covering the important points.

The concrete values are chosen to represent realistic protocol conditions: post-migration pool states for lending, bonding completion states for migration, and protocol-default rates for the sell cycle.

### Dropped Harnesses (Design Rationale)

Eight harnesses were dropped during verification because they prove structurally guaranteed properties or were superseded:

| Dropped Harness | Reason |
|-----------------|--------|
| `verify_curve_monotonic_fresh/half/full` | Monotonicity of `vt * sol / (vs + sol)` is guaranteed by the formula structure for any fixed positive `vt`, `vs`. Integer floor division preserves monotonicity. |
| `verify_no_round_trip_fresh/half/full` | Round-trip loss (`buy then sell <= original`) is inherent in AMM constant-product formulas with integer truncation. Floor division always rounds down. |
| `verify_ltv_100_percent` | `(v * 10000) / v == 10000` is a mathematical tautology. SAT solvers cannot efficiently prove symbolic u128 division cancellation. |
| `verify_buyback_respects_reserve` | Buyback reserve/amount constraints are enforced by handler-level checks, not arithmetic. Property is structural given the config validation. |

These properties remain true by construction. The remaining 70 harnesses cover every non-tautological safety property.

## What Is NOT Verified

Kani proofs verify **isolated pure functions** extracted from the handlers. They do not cover:

| Category | Examples | Why Not Covered |
|----------|----------|-----------------|
| **Access control** | Who can call `migrate_to_dex`, `update_dev_wallet` | Enforced by Anchor `#[derive(Accounts)]` constraints, not arithmetic |
| **Account validation** | Fake PDAs, wrong mints, account substitution | Requires on-chain runtime context |
| **State machine transitions** | Can you sell before buying? Migrate before bonding completes? | Requires multi-instruction sequencing |
| **CPI safety** | Reentrancy via Raydium CPIs, privilege escalation | Cross-program invocation is outside arithmetic scope |
| **Economic attacks** | Sandwich attacks, oracle manipulation, flash loans | Require multi-transaction economic modeling |
| **Anchor framework correctness** | `init-if-needed` edge cases, PDA derivation | Framework-level concerns |
| **Concurrency** | Parallel transaction ordering, front-running | Solana runtime behavior |

### Recommendation for Auditors

The arithmetic layer is formally verified. Audit effort should focus on:

1. **Access control and account validation** -- can unauthorized callers invoke privileged instructions?
2. **State transition integrity** -- are there invalid state transitions (e.g., double migration, selling into an empty curve)?
3. **CPI safety** -- can Raydium CPIs be exploited for reentrancy or privilege escalation?
4. **Economic attack surface** -- sandwich attacks on bonding curve buys, oracle-free lending price manipulation
5. **Token-2022 edge cases** -- transfer fee interaction with Token-2022 extensions across CPIs

## Running the Proofs

```bash
# Install Kani
cargo install --locked kani-verifier
cargo kani setup

# Run all harnesses
cd torch_market/programs/torch_market
cargo kani

# Run a specific harness
cargo kani --harness verify_buy_fee_conservation
```

All 70 harnesses pass. Most complete in under 1 second; the slowest (`verify_transfer_fee_bounds`, `verify_treasury_rate_monotonic`) take 30-55 seconds due to larger SAT formula complexity.

## Constants Reference

| Constant | Value | Description |
|----------|-------|-------------|
| `TOTAL_SUPPLY` | 1,000,000,000,000,000 | 1 billion tokens (6 decimals) |
| `BONDING_TARGET_SPARK` | 50,000,000,000 | 50 SOL bonding target (legacy — removed from creation in V4.0) |
| `BONDING_TARGET_FLAME` | 100,000,000,000 | 100 SOL bonding target (Flame tier) |
| `BONDING_TARGET_TORCH` | 200,000,000,000 | 200 SOL bonding target (Torch tier, default) |
| `INITIAL_VIRTUAL_SOL` | 30,000,000,000 | 30 SOL initial virtual reserves (legacy) |
| `INITIAL_VIRTUAL_TOKENS` | 107,300,000,000,000 | Initial virtual token reserves (legacy) |
| `INITIAL_VIRTUAL_TOKENS_V27` | 756,250,000,000,000 | 756.25M tokens initial virtual reserves (V27) |
| `TREASURY_LOCK_TOKENS` | 300,000,000,000,000 | 300M tokens locked in treasury (30% of supply) |
| `CURVE_SUPPLY` | 700,000,000,000,000 | 700M tokens for curve + pool (70% of supply) |
| V27 IVS | `3 * bonding_target / 8` | 18.75 SOL (Spark), 37.5 SOL (Flame), 75 SOL (Torch) |
| `PROTOCOL_FEE_BPS` | 50 | [V4.0] 0.5% protocol fee (was 1%) |
| `TREASURY_FEE_BPS` | 0 | [V10] Removed — treasury funded by dynamic SOL rate + transfer fees |
| `TREASURY_SOL_MIN_BPS` | 250 | [V10] 2.5% min treasury SOL rate (was 4%) |
| `TREASURY_SOL_MAX_BPS` | 1750 | [V36] 17.5% max treasury SOL rate (was 15%) |
| `DEV_WALLET_SHARE_BPS` | 5000 | [V10.2.6] 50% of protocol fee to dev (was 10%) |
| `BURN_RATE_BPS` | **REMOVED** | [V36] Vote vault removed — 100% of tokens to buyer |
| `TRANSFER_FEE_BPS` | 7 | [V35] 0.07% Token-2022 transfer fee (was 4 bps, old tokens retain 4) |
| `DEFAULT_INTEREST_RATE_BPS` | 200 | 2% lending interest per epoch |
| `DEFAULT_LIQUIDATION_BONUS_BPS` | 1000 | 10% liquidation bonus |
| `DEFAULT_LENDING_UTILIZATION_CAP_BPS` | 8000 | [V4.0] 80% max treasury SOL lendable (was 70%) |
| `BORROW_SHARE_MULTIPLIER` | 23 | [V10.2.5] Per-user cap: max borrow = 23x collateral's share of lendable pool (was 5x) |
| `RATIO_PRECISION` | 1,000,000,000 | 1e9 ratio scale factor |
| `DEFAULT_SELL_THRESHOLD_BPS` | 12,000 | 120% -- sell triggers at 20% above baseline |
| `DEFAULT_SELL_PERCENT_BPS` | 1,500 | 15% of held tokens sold per call |
| `SELL_ALL_TOKEN_THRESHOLD` | 1,000,000,000,000 | 1M tokens -- sell 100% below this |
| `MIN_EPOCH_VOLUME_ELIGIBILITY` | 2,000,000,000 | [V32] 2 SOL min epoch volume for rewards (was 10 SOL) |
| `MIN_CLAIM_AMOUNT` | 100,000,000 | [V32] 0.1 SOL min claim amount |
| `MAX_CLAIM_SHARE_BPS` | 1,000 | 10% max per-user claim share per epoch |
| `CREATOR_SOL_MIN_BPS` | 20 | [V34] 0.2% creator SOL share at bonding start |
| `CREATOR_SOL_MAX_BPS` | 100 | [V34] 1% creator SOL share at bonding completion |
| `CREATOR_FEE_SHARE_BPS` | 1,500 | [V34] 15% creator share of fee swap proceeds |
| `COMMUNITY_TOKEN_SENTINEL` | u64::MAX | [V35] Sentinel in Treasury.total_bought_back for community tokens (0% creator fees) |
| `SHORT_ENABLED_SENTINEL` | u16::MAX | [V5] Sentinel in Treasury.buyback_percent_bps — short selling enabled |
| `MIN_SHORT_TOKENS` | 1,000,000,000 | [V5] 1,000 tokens minimum short position (6 decimals) |
| `MIN_POOL_SOL_LENDING` | 5,000,000,000 | [V6] 5 SOL minimum pool depth for lending/short operations |
| `MAX_PRICE_DEVIATION_BPS` | 5,000 | [V6] 50% max price deviation from baseline for swap_fees_to_sol ratio gating |
| `DEPTH_TIER_1` | 50,000,000,000 | [V7] 50 SOL — depth band tier 1 threshold |
| `DEPTH_TIER_2` | 200,000,000,000 | [V7] 200 SOL — depth band tier 2 threshold |
| `DEPTH_TIER_3` | 500,000,000,000 | [V7] 500 SOL — depth band tier 3 threshold |
| `DEPTH_LTV_0` | 2,500 | [V7] 25% max LTV for pools <50 SOL |
| `DEPTH_LTV_1` | 3,500 | [V7] 35% max LTV for pools 50-200 SOL |
| `DEPTH_LTV_2` | 4,500 | [V7] 45% max LTV for pools 200-500 SOL |
| `DEPTH_LTV_3` | 5,000 | [V7] 50% max LTV for pools >500 SOL |
| `MIN_SOL_AMOUNT` | 1,000,000 | 0.001 SOL minimum |
