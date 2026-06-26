# Platform Details — Portfolio Management Systems

## Table of Contents

1. [Portfolio Management System Architecture](#1-portfolio-management-system-architecture) — core functions, major platform comparison table, IBOR vs. OBOR
2. [Model Portfolio Management](#2-model-portfolio-management) — model specification, types, hierarchy, change governance, marketplaces
3. [Sleeve-Based and UMA Architecture](#3-sleeve-based-and-uma-architecture) — UMA structure, cash management rules, UMA vs. SMA vs. wrap comparison
4. [Drift Monitoring and Rebalancing](#4-drift-monitoring-and-rebalancing) — drift measurement, threshold configurations, rebalancing approaches, tax-aware logic
5. [Held-Away Asset Aggregation](#5-held-away-asset-aggregation) — data sources, data-quality challenges, reporting views
6. [Portfolio Accounting and Reconciliation](#6-portfolio-accounting-and-reconciliation) — IBOR ledger, daily reconciliation, break resolution, corporate actions, cost basis
7. [Trading and Order Management Integration](#7-trading-and-order-management-integration) — pointer to order-management-advisor
8. [Performance Calculation Engine](#8-performance-calculation-engine) — daily vs. monthly calculation, benchmark tracking, performance levels
9. [Billing and Fee Calculation](#9-billing-and-fee-calculation) — pointer to fee-billing
10. [Custodian Integration and Data Feeds](#10-custodian-integration-and-data-feeds) — data flow table, integration methods, feed timing, multi-custodian management

## Core Concepts

### 1. Portfolio Management System Architecture

The portfolio management system is the operational nerve center of an investment advisory
practice. It sits at the intersection of investment management, client servicing, and
compliance, orchestrating the flow of data between custodians, trading platforms, reporting
engines, CRM systems, and financial planning tools.

**Core PMS Functions:**

- **Portfolio construction** — Building and maintaining investment portfolios aligned with
  client objectives and firm models.
- **Model management** — Defining, versioning, and distributing model portfolios across
  the client base.
- **Rebalancing** — Detecting portfolio drift from targets and generating trade proposals
  to restore alignment.
- **Trading** — Producing trade lists, supporting block trading, and routing orders to
  custodians or execution platforms.
- **Performance reporting** — Calculating time-weighted and money-weighted returns at the
  security, account, household, and composite levels.
- **Billing** — Computing advisory fees based on AUM, generating invoices or direct-debit
  instructions, and tracking revenue.

**Major PMS Platforms:**

| Platform | Provider | Typical Firm Size | Key Strengths |
|---|---|---|---|
| Orion Portfolio Solutions | Orion Advisor Solutions | Mid to large RIAs | Deep rebalancing, compliance, and reporting; Eclipse trading engine |
| Black Diamond | SS&C Technologies | Mid-size RIAs | Strong performance reporting and client portal |
| Tamarac | Envestnet | Mid to large RIAs | Rebalancing, CRM integration (via Envestnet ecosystem) |
| Addepar | Addepar | Large RIAs, family offices | Complex asset support, alternatives, data visualization |
| Morningstar Direct | Morningstar | Research-oriented firms | Investment research integration, manager analysis |
| Advent/APX | SS&C Technologies | Large RIAs, institutional | Institutional-grade accounting and multi-currency support |

**Investment Book of Record (IBOR) vs. Official Book of Record:**

The PMS serves as the firm's investment book of record (IBOR), maintaining the advisory
firm's view of positions, transactions, cost basis, and performance. The custodian
maintains the official book of record (OBOR) — the legally authoritative record of client
assets. These two records must be reconciled daily to ensure accuracy. Discrepancies
(breaks) require investigation and resolution before reporting or billing can proceed
with confidence.

**Key reconciliation dimensions:**

- Position reconciliation — Do PMS and custodian agree on shares/units held?
- Transaction reconciliation — Are all trades, dividends, and corporate actions reflected
  in both systems?
- Cash reconciliation — Do cash balances match after accounting for pending settlements?

### 2. Model Portfolio Management

Model portfolios are the foundation of scalable portfolio management. A model defines a
target investment allocation — specifying asset classes, individual securities or funds,
and their target weights — that can be applied consistently across many client accounts.

**Defining a Model Portfolio:**

A model portfolio specification includes:

- **Target asset allocation** — The percentage assigned to each asset class (e.g., 60%
  equity, 35% fixed income, 5% alternatives).
- **Security selection** — The specific ETFs, mutual funds, or individual securities
  used to represent each asset class.
- **Target weights** — The precise weight for each security within the model (e.g.,
  VTI 30%, VXUS 15%, BND 25%, BNDX 10%, VNQ 5%, cash 5%, etc.).
- **Substitution rules** — Tax-efficient alternatives for taxable accounts, ESG
  substitutions, or client-specific restrictions.

**Model Types:**

- **Strategic models (SAA)** — Long-term, policy-driven allocations reflecting the firm's
  capital market assumptions. Changed infrequently (annually or less). Example: a
  "Moderate Growth" model targeting 60/40 equity/fixed income.
- **Tactical models (TAA overlays)** — Short-term tilts applied on top of strategic
  allocations to capitalize on market dislocations or risk management. Example:
  underweighting international equities by 5% during a dollar-strengthening cycle.
- **Specialty models** — Purpose-built allocations for specific objectives: income
  generation, ESG/SRI mandates, tax-managed (municipal bonds, low-turnover equity),
  concentrated stock diversification.

**Model Hierarchy:**

Most firms operate a two-tier model structure:

- **Firm-level models** — Centrally managed by the investment committee or CIO. These
  represent the firm's house view and ensure consistency.
- **Advisor-customized models** — Advisors may create variants of firm models with
  client-specific adjustments (e.g., excluding a sector due to concentrated employer
  stock, adding a charitable giving sleeve). The PMS should track these customizations
  and flag when they deviate materially from the base model.

**Model Changes and Governance:**

When the investment committee changes a model — whether adjusting allocation weights,
substituting a security, or adding a new asset class — the PMS must:

1. Version the model change with an effective date.
2. Identify all accounts assigned to the affected model.
3. Generate rebalancing trade proposals for those accounts.
4. Apply tax-aware logic to minimize the cost of transitioning.
5. Route trades through the trading workflow for review and execution.

**Model Marketplace:**

Major PMS and TAMP platforms offer access to third-party model portfolios from asset
managers such as BlackRock, DFA (Dimensional Fund Advisors), Vanguard, PIMCO, and
JP Morgan. Advisors can adopt these models wholesale or blend them with proprietary
models. This allows smaller firms to leverage institutional-quality investment management
without building in-house research capabilities.

### 3. Sleeve-Based and UMA Architecture

The Unified Managed Account (UMA) structure represents an evolution from single-strategy
managed accounts to multi-strategy, multi-manager portfolios held within a single
brokerage account.

**UMA Structure:**

A UMA divides a single custodial account into multiple virtual sub-accounts called
sleeves. Each sleeve follows its own investment strategy, model, or external manager,
but all sleeves share a single account number, tax ID, and custodial registration.

**Typical UMA Sleeve Examples:**

| Sleeve | Strategy | Manager/Model |
|---|---|---|
| Core U.S. Equity | Large-cap growth + value | Firm proprietary model |
| International Equity | Developed + emerging markets | DFA International Core model |
| Fixed Income | Investment-grade bonds | PIMCO model |
| Alternatives | Real assets, hedge fund replication | Third-party manager |
| Tactical Overlay | Short-term tilts | CIO tactical model |
| Cash/Liquidity | Money market, short-term | Cash management rules |

**Benefits of UMA/Sleeve Architecture:**

- **Tax efficiency** — The overlay manager or PMS can harvest losses in one sleeve and
  avoid realizing gains in another, optimizing the tax outcome at the account level. This
  cross-sleeve tax coordination is impossible when strategies are held in separate accounts.
- **Simplified reporting** — One account statement instead of multiple, with the option
  to show performance by sleeve or for the total account.
- **Reduced account proliferation** — A client who might otherwise need 5-6 separate
  managed accounts can consolidate into a single UMA, reducing operational complexity.
- **Unified cash management** — Cash flows (dividends, interest, withdrawals, deposits)
  can be managed at the account level and allocated across sleeves according to rules.

**Cash Management Across Sleeves:**

The PMS must define how cash is handled across sleeves:

- **Cash waterfall rules** — When a client deposits funds, which sleeves receive
  the cash and in what priority order?
- **Cash raise logic** — When a client requests a withdrawal, which sleeves are
  liquidated and in what order (typically selling the most overweight sleeve first
  or the sleeve with the most harvestable losses)?
- **Income allocation** — Dividends and interest generated within a sleeve may stay
  in that sleeve or flow to a central cash sleeve.

**UMA vs. SMA vs. Mutual Fund Wrap:**

| Feature | UMA | SMA | Mutual Fund Wrap |
|---|---|---|---|
| Number of strategies | Multiple | Single | Multiple (via funds) |
| Account structure | One account, multiple sleeves | One account, one strategy | One account, fund portfolio |
| Security ownership | Direct (individual securities) | Direct | Indirect (fund shares) |
| Tax management | Cross-sleeve optimization | Single-strategy only | Limited (fund-level) |
| Customization | High (per-sleeve and cross-sleeve) | Moderate (single strategy) | Low |
| Typical minimum | $250K-$1M+ | $100K-$250K | $25K-$100K |
| Manager access | Multiple managers, one account | One manager | Multiple managers via funds |

### 4. Drift Monitoring and Rebalancing

Portfolio drift is the divergence of actual portfolio weights from target model weights
caused by differential asset returns, cash flows, and corporate actions over time. The
PMS continuously monitors drift and generates rebalancing recommendations when
thresholds are breached.

**Measuring Drift:**

- **Absolute drift** — The simple difference between actual weight and target weight.
  If U.S. equity target is 40% and actual is 44%, absolute drift is +4 percentage
  points.
- **Relative drift** — The drift as a percentage of the target weight. Using the same
  example, relative drift is 4/40 = 10%.
- **Band-based monitoring** — Each asset class or security has an allowable range
  (band) around the target. Rebalancing triggers only when a holding breaches the
  band boundary. Example: target 40% with a +/-5% band means rebalancing triggers
  below 35% or above 45%.

**Drift Thresholds:**

Common threshold configurations in PMS platforms:

- Conservative: 3% absolute or 15% relative drift.
- Moderate: 5% absolute or 25% relative drift.
- Permissive: 7% absolute or 30% relative drift.

The appropriate threshold depends on tax sensitivity, turnover tolerance, trading costs,
and client preferences.

**Rebalancing Approaches:**

- **Calendar-based** — Rebalancing at fixed intervals (quarterly, semi-annually,
  annually) regardless of drift levels. Simple to implement but may miss significant
  interim drift or trigger unnecessary trades.
- **Threshold-based** — Rebalancing only when drift exceeds defined thresholds.
  More responsive than calendar-based and avoids unnecessary trading, but requires
  continuous monitoring.
- **Opportunistic (cash-flow-directed)** — Using client deposits, withdrawals,
  dividends, and other cash flows as opportunities to move toward targets without
  generating incremental trades. The most tax-efficient approach for accounts with
  regular cash flows.
- **Hybrid** — Combining threshold-based monitoring with opportunistic cash flow
  rebalancing. Thresholds serve as the outer guardrail while cash flows handle
  minor drift continuously.

**Tax-Aware Rebalancing:**

A sophisticated PMS rebalancing engine incorporates tax considerations:

- **Capital gains minimization** — When selling overweight positions, prefer lots
  with losses or long-term gains over short-term gains.
- **Loss harvesting** — Proactively selling positions with unrealized losses to
  generate tax deductions, then replacing with similar (but not substantially
  identical) securities.
- **Wash sale avoidance** — The PMS must track the 30-day wash sale window across
  all accounts for the same tax ID to prevent disallowed losses.
- **Gain budget** — Some firms set a maximum dollar amount of realized gains per
  account per year, and the rebalancing engine respects this constraint.

**Cash-Flow-Directed Rebalancing:**

When a client deposits $50,000 into a portfolio, the PMS calculates the optimal
allocation of that cash to move the portfolio closer to target weights. Rather than
investing proportionally to the current allocation, the deposit is directed to the
most underweight positions. Similarly, withdrawals are funded by selling the most
overweight positions first.

### 5. Held-Away Asset Aggregation

A complete picture of a client's financial situation requires visibility into all assets,
not just those managed by the advisory firm. Held-away assets include employer retirement
plans (401(k), 403(b)), stock options, restricted stock units (RSUs), bank accounts,
annuities, real estate, and accounts at other custodians.

**Data Sources for Held-Away Assets:**

- **Account aggregation services** — Technology platforms that connect to financial
  institutions via screen-scraping or API to retrieve account data. Major providers
  include Plaid, Yodlee (Envestnet), MX, and ByAllAccounts (Morningstar). These
  services pull positions, balances, and sometimes transactions on a scheduled basis.
- **Custodian data feeds** — Some custodians provide direct feeds for accounts
  held at their institution, enabling higher-quality data than aggregation services.
- **Manual entry** — For assets that cannot be electronically aggregated (real estate,
  private equity, collectibles), advisors or clients enter valuations manually. These
  require periodic updates to remain useful.
- **Employer plan integration** — Specialized feeds from retirement plan recordkeepers
  (Fidelity NetBenefits, Empower, Vanguard) that provide participant-level data.

**Challenges with Held-Away Data:**

- **Data freshness** — Aggregated data may be 1-3 days stale, and connections can
  break when institutions change login procedures or add multi-factor authentication.
- **Categorization accuracy** — Aggregation services may misclassify securities or
  asset types, requiring manual correction in the PMS.
- **Stale connections** — Clients must periodically re-authenticate their linked
  accounts. Stale connections produce outdated data that can lead to incorrect
  planning recommendations.
- **Incomplete data** — Some institutions block aggregation, and certain asset types
  (unvested RSUs, stock options) may not transmit full detail (exercise price,
  vesting schedule).

**Use in Financial Planning and Portfolio Management:**

Held-away assets directly affect advisory decisions:

- **Asset allocation assessment** — A client's managed account may appear well
  diversified, but when combined with a 401(k) heavily concentrated in employer
  stock, the total household allocation could be dangerously concentrated.
- **Planning recommendations** — Held-away 401(k) assets affect retirement
  projections, Roth conversion analysis, and Social Security claiming strategies.
- **Tax planning** — Knowing the asset location (tax-deferred, Roth, taxable) across
  all accounts enables better tax-efficient asset placement decisions.

**Reporting Views:**

The PMS should provide two distinct reporting perspectives:

- **Managed-only view** — Shows only assets under the firm's management, used for
  billing, performance reporting, and regulatory filings.
- **Total household view** — Includes held-away assets, used for financial planning
  discussions, asset allocation reviews, and comprehensive client presentations.

### 6. Portfolio Accounting and Reconciliation

Portfolio accounting is the systematic tracking of all investment positions, transactions,
cost basis, cash flows, and accrued income within the PMS. Accuracy in portfolio
accounting is the foundation for reliable performance reporting, tax management, and
client trust.

**PMS as Investment Book of Record (IBOR):**

The PMS maintains a complete transaction history and position ledger for every managed
account:

- **Positions** — Current holdings with quantity, market value, unrealized gain/loss.
- **Transactions** — Buys, sells, exchanges, transfers-in, transfers-out, dividends,
  interest, fees, corporate actions.
- **Cost basis** — Original purchase price and date for each tax lot, adjusted for
  corporate actions (splits, mergers, return of capital).
- **Cash balances** — Settled and pending cash, including accrued income not yet
  received.
- **Accrued income** — Interest accrued on fixed-income holdings between coupon
  payment dates.

**Daily Reconciliation Process:**

Reconciliation compares the PMS investment book of record against the custodian's
official book of record across three dimensions:

1. **Position reconciliation** — Compares shares/units held per security per account.
   Breaks typically result from unprocessed trades, missed corporate actions, or
   data-feed errors.
2. **Transaction reconciliation** — Compares trade activity for the day. Breaks may
   indicate trades executed at the custodian but not reflected in the PMS, or PMS
   trades that failed to execute.
3. **Cash reconciliation** — Compares cash balances accounting for settled and
   unsettled activity. Cash breaks often result from timing differences in
   dividend/interest posting or fee deductions.

**Break Identification and Resolution:**

A break is any discrepancy between PMS and custodian records. Break resolution follows
a standard workflow:

1. Identify break in the daily reconciliation report.
2. Classify the break type (position, transaction, cash, cost basis).
3. Determine root cause (missed corporate action, trade error, feed issue, timing).
4. Apply correction in the appropriate system (PMS adjustment, custodian inquiry).
5. Verify the break is resolved in the next reconciliation cycle.
6. Document the resolution for audit trail purposes.

**Corporate Actions Processing:**

Corporate actions are among the most common sources of reconciliation breaks:

- **Cash dividends** — Record income and increase cash balance.
- **Stock dividends** — Increase share count without cash impact.
- **Stock splits** — Adjust share count and cost basis per share.
- **Reverse splits** — Reduce share count and adjust cost basis.
- **Mergers/acquisitions** — Remove acquired security, add acquiring security,
  adjust cost basis for tax-free reorganizations.
- **Spin-offs** — Add new security, allocate cost basis from parent.
- **Tender offers** — Partial or full redemption at specified price.
- **Return of capital** — Reduce cost basis rather than record income.

**Cost Basis Methods:**

The PMS must support multiple cost basis methods, as the method affects realized
gains and losses:

- **Specific identification** — The investor (or PMS algorithm) selects which tax
  lots to sell, enabling optimal tax management. This is the most common method
  for advisory accounts.
- **FIFO (First In, First Out)** — Sells the oldest lots first. Simple but may
  result in larger gains in rising markets.
- **Average cost** — Uses the average cost of all shares. Permitted only for mutual
  fund shares and certain other securities.

**Tax Lot Management:**

Effective tax lot management enables gain/loss optimization:

- Maintain lot-level detail (purchase date, cost, quantity) for every position.
- Track holding period (short-term vs. long-term) to distinguish gain character.
- Support lot selection strategies (highest cost, lowest cost, loss harvesting,
  gain minimization).
- Track wash sale adjustments across accounts with the same tax ID.

### 7. Trading and Order Management Integration

Trade list generation, PMS-to-OMS handoff, block trading, pre-trade compliance, and
order routing are covered in the **order-management-advisor** skill (advisory-practice
plugin) — load that skill for trading workflow detail.

### 8. Performance Calculation Engine

The PMS serves as the performance calculation engine for the advisory practice,
computing returns at multiple levels and across multiple methodologies. For the
definitions and mathematics of time-weighted (TWR) vs. money-weighted (MWR/IRR)
returns and when each is appropriate, see the wealth-management **performance-metrics**
and **performance-reporting** skills.

**Daily vs. Monthly Performance:**

- **Daily performance** — Returns calculated every day using daily valuations.
  Provides the most precise TWR calculation and enables intra-month reporting.
  Requires daily position and pricing data from custodians.
- **Monthly performance** — Returns calculated at month-end using month-end
  valuations. Less precise for TWR (uses Modified Dietz or similar approximation
  for intra-month cash flows) but requires less infrastructure.

Most modern PMS platforms support daily performance calculation.

**Benchmark Assignment and Tracking:**

Each model, account, or composite is assigned one or more benchmarks:

- **Primary benchmark** — The market index most representative of the portfolio's
  investment strategy (e.g., 60% MSCI ACWI / 40% Bloomberg U.S. Aggregate for
  a 60/40 portfolio).
- **Blended benchmarks** — Weighted combinations of multiple indices matching
  the portfolio's asset allocation.
- **Custom benchmarks** — Firm-constructed benchmarks reflecting specific
  investment policies.

The PMS must track benchmark returns at the same frequency and over the same periods
as portfolio returns to enable meaningful comparison.

**Performance at Multiple Levels:**

A comprehensive PMS calculates performance at every level of the investment hierarchy:

- **Security level** — Return contribution of each holding.
- **Sleeve level** — Performance of each UMA sleeve or sub-strategy.
- **Account level** — Total account performance (TWR and MWR).
- **Household level** — Aggregated performance across all accounts for a client
  or household.
- **Model level** — Theoretical performance of the model itself (useful for
  evaluating model quality separately from implementation).
- **Composite level** — Aggregated performance of all accounts following a
  similar strategy, used for GIPS reporting and marketing.
- **Firm level** — Overall firm AUM-weighted performance.

### 9. Billing and Fee Calculation

Fee schedule structures, billable-AUM determination, billing cycles, fee deduction,
and revenue tracking are covered in the **fee-billing** skill (advisory-practice
plugin) — load that skill for billing detail.

### 10. Custodian Integration and Data Feeds

Custodian integration is the data backbone of the PMS. The quality, completeness,
and timeliness of custodian data feeds directly determine the accuracy of portfolio
accounting, performance reporting, rebalancing, and billing.

**Data Flowing Between PMS and Custodians:**

| Data Type | Direction | Frequency | Purpose |
|---|---|---|---|
| Positions | Custodian to PMS | Daily (EOD) | Reconciliation, reporting |
| Transactions | Custodian to PMS | Daily (EOD) | Accounting, performance |
| Cash balances | Custodian to PMS | Daily (EOD) | Cash management, rebalancing |
| Cost basis | Custodian to PMS | Daily or on-demand | Tax reporting, gain/loss |
| Corporate actions | Custodian to PMS | As-occurs + EOD | Accounting adjustments |
| New accounts | Custodian to PMS | Daily or real-time | Account setup |
| Trade instructions | PMS to custodian | Real-time or batch | Order execution |
| Fee invoices | PMS to custodian | Quarterly/monthly | Fee deduction |

**Integration Methods:**

- **Custodian proprietary data feeds** — Major custodians provide standardized
  data files in proprietary or industry-standard formats. Examples: Schwab
  (Schwab Advisor Center data feeds), Fidelity (Wealthscape data feeds),
  Pershing (NetX360 data feeds). These are typically delivered as batch files
  (CSV, XML, or fixed-width) at end-of-day.
- **FIX protocol** — Financial Information eXchange protocol for real-time trade
  messaging. Used for order routing, execution reporting, and position updates.
  More common for institutional trading than advisory account management.
- **API-based integration** — RESTful APIs provided by custodians for real-time
  data access. Increasingly available but with varying levels of completeness.
  Schwab and Fidelity have expanded API offerings for RIAs.
- **Third-party data aggregators** — Services like Plaid (which absorbed Quovo in 2019), ByAllAccounts
  (Morningstar), or Addepar's data infrastructure that normalize data from
  multiple custodians into a standard format for PMS consumption.

**Feed Timing:**

- **End-of-day (EOD) batch** — The most common feed timing. Custodian generates
  files after market close and settlement processing (typically available by
  early morning of the following business day). EOD feeds provide the settled
  view of positions and transactions.
- **Intraday updates** — Some custodians provide intraday position snapshots and
  real-time trade confirmations. Useful for same-day rebalancing and cash
  management but not universally available.
- **Real-time streaming** — Available for limited data types (trade confirmations,
  price updates) via FIX or websocket connections. Primarily used by firms with
  active trading or time-sensitive operations.

**Multi-Custodian Management:**

Many advisory firms custody client assets at two or more custodians (e.g., Schwab
and Fidelity). The PMS must:

- Ingest and normalize data feeds from each custodian into a unified data model.
- Present a consolidated view of positions, performance, and asset allocation
  across custodians.
- Generate trades appropriate for each custodian's trading platform and rules.
- Reconcile separately against each custodian's records.
- Handle custodian-specific differences in security identifiers, transaction
  types, corporate action processing, and settlement conventions.

**Custodian Transition Management:**

When a firm changes its primary custodian (e.g., transitioning from TD Ameritrade
to Schwab following the 2023-2024 acquisition), the PMS must support:

- Mapping accounts from the old custodian to the new.
- Ingesting the new custodian's data feeds and formats.
- Transferring historical data to maintain performance continuity.
- Managing the transition period when accounts may exist at both custodians
  simultaneously.
- Re-establishing automated trading and fee deduction with the new custodian.
- Communicating changes to clients and managing expectations around
  temporary data gaps.

