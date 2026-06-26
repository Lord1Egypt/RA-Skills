# Buffett Oracle — Coverage Scope

*Last updated: 2026-03-25*

## Core Scope

The current repo is **not** a full history of Buffett/Berkshire investments.

It is a **curated 29-case benchmark set** chosen to stress-test the framework across:

- common-stock wins
- common-stock mistakes
- crisis preferred deals
- private-company acquisitions
- early Berkshire capital-allocation turning points

The purpose of this set is methodological:

- force point-in-time underwriting
- compare BUY vs PASS logic across different deal types
- expose where the framework overfits, hedges, or cheats

## What The 29 Cases Are Not

The benchmark set does **not** claim to include:

- every Berkshire public-equity position
- every addition or trim to an existing position
- every wholly owned acquisition
- every preferred, warrant, arbitrage, or financing deal
- every non-U.S. holding
- every short-lived or small historical position

So `29 / 29` means:

- `29 / 29 benchmark cases completed`

It does **not** mean:

- `29 / 29 of Buffett's real investment history`

## Expansion Tracks

If the project grows beyond the benchmark set, new coverage should be added as separate layers:

1. **Public equity universe**
   Add major Berkshire common-stock positions not yet benchmarked.
   Current file: `universe_expansion.md`

   Working broader name registry:
   `buffett_investment_universe.md`

2. **Wholly owned acquisitions**
   Add major private-company deals with source-backed point-in-time memos.

3. **Structured / special situations**
   Preferreds, warrants, rescue financings, arbitrage, and hybrid deals.

4. **Position management history**
   Adds, trims, exits, and re-entries should be tracked separately from the original buy memo.

## Guardrail

Never present the benchmark set as if it were the total Buffett/Berkshire universe.

If a user asks "how many investments did Buffett make?", the honest answer is:

- far more than 29
- this repo currently audits only a selected benchmark subset
- the broader company/entity registry now starts in `buffett_investment_universe.md`
