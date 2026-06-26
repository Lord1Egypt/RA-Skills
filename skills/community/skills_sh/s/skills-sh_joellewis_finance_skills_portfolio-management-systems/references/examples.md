# Worked Examples — Portfolio Management Systems

## Table of Contents

1. [PMS Migration for a Growing RIA](#example-1-pms-migration-for-a-growing-ria) — spreadsheet-to-Orion migration: platform selection, data migration, model setup, feed configuration, parallel go-live
2. [UMA/Sleeve Implementation for HNW Clients](#example-2-umasleeve-implementation-for-hnw-clients) — consolidating SMAs into a five-sleeve UMA with cross-sleeve tax management
3. [Reconciliation Break Investigation and Resolution](#example-3-reconciliation-break-investigation-and-resolution) — diagnosing 48 position breaks by root cause and building preventive controls

### Example 1: PMS Migration for a Growing RIA

**Scenario:**

A $500M RIA with 800 client households has been managing portfolios using Excel
spreadsheets and the custodian's online platform. The firm operates 12 model
portfolios across two custodians (Schwab and Fidelity). As the firm grows, the
spreadsheet approach creates unacceptable operational risk: rebalancing is
inconsistent, performance reporting is delayed by weeks, and the firm recently
discovered it had been billing a client at the wrong fee rate for two quarters.
The firm decides to implement Orion as its portfolio management system.

**Design Considerations:**

**Platform selection criteria:**

- Multi-custodian support (Schwab and Fidelity integration required).
- Rebalancing engine capable of handling 12+ models across 800+ households.
- Tax-aware rebalancing with wash sale tracking.
- Automated billing with tiered fee schedule support.
- Performance reporting with composite construction for marketing materials.
- Integration with the firm's existing CRM (Salesforce).
- Client portal for on-demand performance access.

**Data migration planning:**

- Export current positions and cost basis from both custodians.
- Reconstruct historical transactions from custodian records (typically 3-5
  years for performance history, full history for cost basis).
- Map existing security positions to Orion's security master.
- Import client and account demographic data from CRM.
- Establish the 12 model portfolios in Orion with target allocations and
  security selections.

**Model setup and configuration:**

- Define each of the 12 models with target weights, drift bands, and
  rebalancing rules.
- Assign each client account to the appropriate model.
- Configure substitution rules for taxable vs. tax-deferred accounts.
- Set drift thresholds (the firm selects 5% absolute / 25% relative).
- Configure cash reserve rules (2% minimum cash per account).

**Custodian feed setup:**

- Establish Schwab data feeds: positions, transactions, cash balances,
  cost basis, corporate actions. Test file delivery and parsing.
- Establish Fidelity data feeds: same data categories. Test independently.
- Configure daily reconciliation jobs for both custodians.
- Validate initial reconciliation: resolve any breaks before go-live.

**Go-live workflow:**

- Run parallel operations for 30 days (maintain spreadsheets alongside Orion).
- Compare rebalancing recommendations from both systems.
- Validate performance calculations against custodian-reported returns.
- Validate billing calculations against historical invoices.
- Train advisors and operations staff on the new workflows.
- Decommission spreadsheet processes after successful parallel period.

**Analysis:**

The migration represents a significant operational transformation. The firm should
budget 3-6 months for full implementation, including 1-2 months for data migration
and setup, 1 month for parallel testing, and 1-2 months for staff training and
workflow refinement. Key risks include data quality issues during migration
(especially historical cost basis), disruption to client reporting during the
transition, and staff resistance to new workflows. The firm should designate a
dedicated project manager and plan for temporary increases in operations staffing
during the transition. Post-implementation, the firm should expect significant
efficiency gains: rebalancing that previously took two days per quarter should
complete in hours, billing errors should be eliminated by automated fee calculation,
and performance reports should be available daily rather than weeks after quarter-end.

### Example 2: UMA/Sleeve Implementation for HNW Clients

**Scenario:**

A wealth management firm serving high-net-worth clients ($1M+ investable assets)
currently manages client portfolios using 3-5 separate SMAs per client, each
following a different strategy. This creates operational burden (multiple account
statements, separate rebalancing for each SMA, inability to coordinate tax
management across accounts) and client confusion. The firm decides to transition
its HNW clients to a UMA/sleeve-based structure using its existing PMS (Tamarac).

**Design Considerations:**

**Sleeve structure design:**

The firm designs a five-sleeve UMA architecture:

| Sleeve | Allocation Range | Strategy | Management |
|---|---|---|---|
| Core U.S. Equity | 25-45% | Broad U.S. equity exposure | Firm proprietary model |
| International Equity | 10-25% | Developed and emerging markets | DFA model via Tamarac |
| Fixed Income | 15-35% | Investment-grade and municipal bonds | PIMCO model |
| Alternatives | 5-15% | Real assets, liquid alternatives | Third-party manager |
| Tactical Overlay | 0-10% | Short-term tactical tilts | CIO discretion |

Cash is managed at the total account level rather than within individual sleeves,
with a 2% minimum cash target.

**Model assignment rules:**

- Each client's Investment Policy Statement (IPS) dictates the overall allocation
  across sleeves based on their risk profile.
- Conservative clients: higher fixed income and lower alternatives allocation.
- Aggressive clients: higher equity and alternatives allocation.
- Sleeve-level models operate independently within their assigned allocation.
- The overlay manager (CIO) can make tactical adjustments within the overlay
  sleeve without affecting other sleeves.

**Cross-sleeve tax management:**

- The PMS overlay engine monitors unrealized gains and losses across all sleeves.
- When rebalancing triggers a sell in one sleeve, the overlay engine checks
  whether a loss can be harvested in another sleeve to offset the gain.
- Wash sale rules are monitored across sleeves: if the fixed income sleeve sells
  a bond fund at a loss, the equity sleeve cannot purchase a substantially
  identical fund within 30 days.
- Year-end tax management: the overlay engine runs a cross-sleeve analysis to
  identify harvesting opportunities before December 31.

**Reporting configuration:**

- **Client-facing reports** show total UMA performance alongside per-sleeve
  performance attribution, so clients understand how each strategy contributes.
- **Internal reports** track model-level performance (how well each model
  performed independent of client cash flows) and implementation efficiency
  (how closely client accounts track their assigned models).
- **Billing reports** calculate fees on total UMA AUM (not per-sleeve).
- **Household reports** aggregate across multiple UMAs and non-UMA accounts
  for clients with more than one account.

**Analysis:**

The UMA transition consolidates 3-5 accounts per client into a single account,
reducing custodian fees, simplifying client statements, and enabling cross-strategy
tax optimization that was previously impossible. The firm should expect a 2-3 month
transition per client cohort, as existing SMA positions must be transferred in-kind
to the new UMA account structure. Tax implications of the transition must be
carefully managed — the firm should avoid realizing gains during the restructuring
by transferring positions in-kind wherever possible. The ongoing operational benefit
is substantial: the overlay manager can rebalance all sleeves simultaneously,
dividends and income flow to a single cash pool, and withdrawals can be sourced
from the most tax-efficient sleeve. The firm should track client satisfaction
metrics before and after the transition, anticipating improvement in client
comprehension of their portfolio structure and investment strategy.

### Example 3: Reconciliation Break Investigation and Resolution

**Scenario:**

An advisory practice managing $350M across 600 accounts discovers during its
Monday morning reconciliation review that 48 accounts (8% of the total) show
position discrepancies between the PMS and the custodian (Schwab). The breaks
range from minor share-count differences to entirely missing positions. The
operations team needs to diagnose the causes, resolve the breaks, and implement
controls to prevent recurrence.

**Design Considerations:**

**Break classification and diagnosis:**

The operations team categorizes the 48 breaks into root-cause buckets:

| Category | Count | Typical Cause |
|---|---|---|
| Missed corporate action | 18 | A stock split processed at custodian but not reflected in PMS |
| Trade settlement timing | 12 | Friday trades settled at custodian over the weekend but PMS shows pending |
| Data feed failure | 8 | The Saturday custodian file failed to load due to a format change in one field |
| Dividend reinvestment | 6 | DRIP shares added at custodian but PMS not configured for auto-DRIP on these accounts |
| Genuine error | 4 | Trades executed at custodian but not initiated through PMS (advisor placed directly) |

**Resolution workflow:**

1. **Corporate action breaks (18 accounts):** The PMS operations team identifies
   that a widely-held equity (held in 18 accounts) underwent a 3:1 stock split
   on the prior Thursday. The custodian processed the split automatically, but
   the PMS corporate action module failed to pick it up from the data feed. The
   team manually applies the split in the PMS, adjusting share counts and cost
   basis for all 18 accounts.

2. **Settlement timing breaks (12 accounts):** These breaks are expected and
   will self-resolve when Monday's end-of-day reconciliation runs. The team marks
   them as "expected timing difference" and monitors for resolution.

3. **Data feed failure (8 accounts):** The Saturday batch file from Schwab
   contained a format change in the corporate action field that caused the PMS
   file parser to reject the entire file for 8 accounts. The team contacts the
   PMS vendor to update the parser, manually imports the affected data, and
   re-runs reconciliation for those accounts.

4. **DRIP configuration (6 accounts):** Six accounts are configured for dividend
   reinvestment at the custodian but the PMS does not reflect this setting. When
   dividends reinvest into fractional shares, the PMS records a cash dividend
   instead. The team updates the DRIP flag in the PMS for these accounts and
   adjusts positions to match the custodian.

5. **Unauthorized trades (4 accounts):** An advisor placed 4 trades directly
   through the custodian platform without going through the PMS. The team enters
   the trades into the PMS after the fact and counsels the advisor on the
   requirement to use the PMS for all trade activity.

**Controls to reduce future breaks:**

- **Automated corporate action processing:** Configure the PMS to automatically
  apply mandatory corporate actions (splits, mergers) from the custodian data
  feed, with alerts for actions requiring manual review (tenders, elections).
- **Feed monitoring:** Implement automated alerts when custodian data files
  fail to arrive, arrive with unexpected format changes, or contain fewer
  records than expected.
- **DRIP audit:** Run a quarterly audit comparing DRIP settings in the PMS
  against custodian DRIP elections for all accounts.
- **Trade workflow enforcement:** Configure custodian access so that advisors
  cannot place trades directly; all trades must originate from the PMS.
- **Daily break dashboard:** Implement a dashboard showing break counts by
  category, age, and resolution status, with escalation rules for breaks
  older than 3 business days.

**Analysis:**

An 8% break rate is above the industry target of under 2% for well-run operations.
The immediate resolution of the 48 breaks eliminates the risk of incorrect
performance reports or billing. However, the more important outcome is the
implementation of preventive controls. Automated corporate action processing alone
should eliminate the largest break category (37.5% of all breaks). Feed monitoring
prevents silent data-quality failures that can cascade into reporting and billing
errors. The trade workflow enforcement addresses a compliance concern: trades placed
outside the PMS bypass pre-trade compliance checks and block-trading allocations,
creating best-execution and fair-allocation risks. The firm should target a break
rate below 1% within 90 days of implementing these controls and track the metric
weekly in operations meetings.
