# SF Residential Build Timelines — Reference

> **Purpose:** Context for report agents evaluating whether any project is on track, stalled, or dead. Use these benchmarks when writing about housing projects in any district. User-specific project watchlists belong in USER.md, not here.

---

## The Phases

| Phase | Typical Duration | Notes |
|-------|-----------------|-------|
| **Entitlement (planning approval)** | 27-34 months (discretionary) / 3-6 months (AB 2011, SB 35) | UCB/HCD CALES study. SF is the slowest city in CA at 523 days avg. |
| **Approval to building permit filing** | 12-36+ months (market-rate) / 6-18 months (affordable) | The dead zone. 35,000+ units entitled but unpermitted citywide (SocketSite, May 2024). Driven by financing, not city process. |
| **Building permit review (DBI)** | 280 days median (all) / 114 days (post-Jan 2024 reforms) | BLA Post-Entitlement Report, March 2026. Pre-reform was 605 days. |
| **Construction** | 18-30 months (mid-rise, 5-10 story) | Wood-frame-over-podium ~22 months. Concrete high-rise longer. |
| **Total: approval to move-in** | 4-5.5 years (streamlined) / 6-8+ years (discretionary) | Brian Goggin analysis: median >6 years for 200+ unit projects. |

## Key Benchmarks for Report Context

**When writing about a project sitting idle post-approval, use these comparisons:**

- 12-18 months post-approval with no building permit → **Normal** for market-rate. The financing gap is systemic.
- 6 months post-approval with $50M+ permit filed → **Fast.** Typical of 100% affordable projects with pre-assembled financing.
- 3+ years post-approval with no permit → **Likely dead or frozen.** Check for cancellation or "on hold" status.
- 7+ years under review → **Zombie project.**

**Don't frame any single project as uniquely stalled unless it's genuinely an outlier.** The approval-to-construction gap affects 35,000+ units citywide. The question is systemic: why does the system have a 1-3 year dead zone between approval and construction for all market-rate projects?

## Why Affordable Projects Move Faster Than Market-Rate

- Pre-assembled financing: MOHCD commits acquisition + predevelopment money early
- Known playbook: MOHCD gap loan + state MHP + LIHTC + tax-exempt bonds
- Public subsidy eliminates the feasibility question (the gap between costs and rents is filled by public money)
- Market-rate projects need construction loans at 7-9% rates, pre-leasing commitments, and developer equity of 25-35%

**The pattern across SF:** 100% affordable projects go from approval to permit in weeks to months. Market-rate projects take 1-3 years. The difference is financing, not process.

---

## Tracking Financing Status

### The "go/no-go" signal: Deed of Trust recording

When a construction loan closes, a **Deed of Trust and Assignment of Rents** is recorded with the SF Assessor-Recorder. This is the strongest public signal that a project will break ground.

**How to check:** Search [recorder.sfgov.org](https://recorder.sfgov.org/) by block/lot number. Filter for document type "Deed of Trust." Block/lot numbers are in the housing pipeline data and the parcels dataset (`acdm-wktn`).

**Limitation:** The recorder portal is a JS-rendered web app with no public API. Automated monitoring would require browser automation.

### Financing data sources

| Source | Dataset ID | What it tells you |
|--------|-----------|------------------|
| MOHCD Affordable Pipeline | `aaxw-2cb8` | Project status, developer, unit counts for affordable projects. No financing amounts. |
| SF Development Pipeline | `6jgi-cpb4` | All projects, all stages. Quarterly update. Status tracking. |
| MOHCD Loan Committee PDFs | `media.api.sf.gov/documents/` | Full sources-and-uses for affordable projects. Richest financing data available. |
| Assessor Secured Roll | `wv5m-vpq2` | Property values, ownership. Annual only. |

### Affordable project financing stack (typical)

Example from a recent D5 affordable project loan evaluation ($101M total):
- MOHCD gap loan: ~6%
- Permanent loan: ~22%
- State HCD MHP loan: ~21%
- LIHTC equity (4% credits): ~46%
- Deferred developer fee: ~3%
- MOHCD acquisition: ~13%

### Market-rate financing (typical)
- Developer equity: 25-35% of total cost
- Construction loan: 65-75% (commercial bank, 7-9% rate in current environment)
- Permanent refinance after lease-up (Fannie/Freddie, CMBS)
- No public subsidy beyond entitlement streamlining

---

## Citywide Context Numbers

Use these when framing any individual project:

- **35,000+ units** entitled but not yet in the permitting process (SocketSite, May 2024)
- **52,000+ units** approved but stalled across SF (The Frisc, 2023)
- **1,735 homes** completed citywide in 2024 — a 12-year low
- **82,000 units** required by the state housing mandate
- **~7,300 units** authorized toward that mandate through Dec 2024 (~9%)
- **80 projects / 7,200+ units** in the streamlined (AB 2011/SB 35) pipeline
- **Only 2% of streamlined projects** have broken ground as of Q1 2026

---

## Sources

- UCB/HCD CALES Report: Examining Local Law, Policy, Planning Practice on Development in SF
- BLA Post-Entitlement Permitting Report, March 2026 (sfbos.org)
- SocketSite: "Builders Slow Their Rolls, Banking Entitlements" (May 2024)
- The Real Deal: "SF Housing Bottleneck" (June 2022)
- Brian Goggin: "How Long Do Housing Developments Take in SF?" (2017)
- KQED: "One of the Slowest US Cities to Build" (March 2026)
- The Frisc: "SF's Fast-Track Housing Era Is Here. Where Are All the Homes?"
- MOHCD Loan Committee evaluations (media.api.sf.gov)
- Senator Wiener: SB 35 results data
- SFist/HCD State Report on SF entitlement timelines (Oct 2023)
