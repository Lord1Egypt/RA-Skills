# Worked Examples — Fee Billing

## Table of Contents

1. [Quarterly Fee Calculation for a Household with Tiered Pricing](#example-1-quarterly-fee-calculation-for-a-household-with-tiered-pricing) — five-account household, tier math, pro-rata allocation, rounding allocation, split debit/invoice output
2. [Mid-Quarter Account Events — Transfers, Contributions, and Terminations](#example-2-mid-quarter-account-events--transfers-contributions-and-terminations) — proration math for advance billing with next-cycle adjustments
3. [Billing System Migration from Spreadsheet to Automated Platform](#example-3-billing-system-migration-from-spreadsheet-to-automated-platform) — five-phase migration with parallel run and cutover controls

### Example 1: Quarterly Fee Calculation for a Household with Tiered Pricing

**Scenario:** The Harrison household has five accounts under a tiered fee schedule. The firm bills quarterly in advance based on prior quarter-end values. The fee schedule is:

| Tier | AUM Range | Annual Rate |
|------|-----------|-------------|
| 1 | First $500,000 | 1.00% |
| 2 | Next $500,000 | 0.85% |
| 3 | Next $2,000,000 | 0.65% |
| 4 | Over $3,000,000 | 0.50% |

Account valuations as of the prior quarter-end (December 31):

| Account | Type | Market Value |
|---------|------|-------------|
| Harrison Joint | Taxable | $1,200,000 |
| Harrison IRA (Mr.) | IRA | $650,000 |
| Harrison IRA (Mrs.) | IRA | $480,000 |
| Harrison Trust | Irrevocable Trust | $850,000 |
| Harrison 529 | 529 Plan | $120,000 |

**Design Considerations:**
- The 529 plan is held away at a separate custodian. The advisory agreement specifies it is included in billable AUM for tier determination but fees on the 529 are billed by invoice, not direct debit.
- The household prefers that direct-debit fees come from the taxable joint account, not the IRAs or trust.
- The firm applies rounding to the nearest cent and allocates rounding differences to the largest account.

**Analysis:**

Step 1 — Aggregate household AUM:
$1,200,000 + $650,000 + $480,000 + $850,000 + $120,000 = $3,300,000

Step 2 — Apply tiered schedule:
- Tier 1: $500,000 at 1.00% = $5,000.00
- Tier 2: $500,000 at 0.85% = $4,250.00
- Tier 3: $2,000,000 at 0.65% = $13,000.00
- Tier 4: $300,000 at 0.50% = $1,500.00
- Annual fee: $23,750.00
- Effective rate: $23,750 / $3,300,000 = 0.7197%

Step 3 — Quarterly fee:
$23,750.00 / 4 = $5,937.50

Step 4 — Allocate to accounts pro rata by market value:

| Account | Market Value | Weight | Allocated Fee |
|---------|-------------|--------|---------------|
| Harrison Joint | $1,200,000 | 36.3636% | $2,159.09 |
| Harrison IRA (Mr.) | $650,000 | 19.6970% | $1,170.01 |
| Harrison IRA (Mrs.) | $480,000 | 14.5455% | $863.64 |
| Harrison Trust | $850,000 | 25.7576% | $1,529.36 |
| Harrison 529 | $120,000 | 3.6364% | $215.91 |
| **Total** | **$3,300,000** | **100%** | **$5,938.01** |

The raw allocation sums to $5,938.01 due to rounding, which is $0.51 over the $5,937.50 quarterly fee. The rounding adjustment of -$0.51 is applied to the largest account (Harrison Joint), reducing its fee to $2,158.58.

Final billing output:
- Direct debit from Harrison Joint account: $5,721.59 (covering Joint $2,158.58 + IRA Mr. $1,170.01 + IRA Mrs. $863.64 + Trust $1,529.36)
- Invoice to Harrison for 529 plan: $215.91

Note: Because the household prefers all direct-debit fees to come from the joint account, the custodian debit instruction is a single debit of $5,721.59 from the joint account. However, the billing detail report still shows the per-account allocation for transparency and performance reporting accuracy.

### Example 2: Mid-Quarter Account Events — Transfers, Contributions, and Terminations

**Scenario:** The Martinez household bills quarterly in advance (Q2: April 1 through June 30, 91 days). At the start of Q2, the household has two accounts:

| Account | Market Value (Mar 31) | Allocated Q2 Fee |
|---------|----------------------|-----------------|
| Martinez Taxable | $800,000 | $1,000.00 |
| Martinez IRA | $400,000 | $500.00 |
| **Total** | **$1,200,000** | **$1,500.00** |

During Q2, three events occur:
1. On April 20 (day 20 of 91), a $200,000 contribution is made to the taxable account.
2. On May 15 (day 45 of 91), a new Roth IRA is opened with a $50,000 transfer from the taxable account.
3. On June 10 (day 71 of 91), the IRA is terminated and the balance is rolled over to another firm.

**Design Considerations:**
- The firm's policy is to prorate for contributions over $25,000 and for all account openings and closings.
- Since billing is in advance, the Q2 fee was already debited on April 1. Adjustments will appear on the Q3 billing run.
- Internal transfers (item 2) should be revenue-neutral at the household level.

**Analysis:**

Event 1 — $200,000 contribution on April 20:
Additional billable days: 71 days remaining out of 91 (April 20 through June 30).
Additional annual fee on $200,000 at the household's effective rate (1.00% flat in this case): $2,000.
Additional quarterly fee: $2,000 / 4 = $500.
Prorated additional fee: $500 * (71 / 91) = $390.11.
This will be charged as an adjustment on the Q3 billing run.

Event 2 — Roth IRA opened May 15 via internal transfer:
The $50,000 moves from the taxable account to the new Roth IRA. Since this is an intra-household transfer, the household AUM does not change and no fee adjustment is needed. The per-account allocation will be updated for the new account going forward, but the household-level fee remains the same.

Event 3 — IRA terminated June 10:
The IRA was billed $500 for the full quarter. Days active: 71 out of 91 (April 1 through June 10).
Days unused: 20 out of 91.
Refund: $500 * (20 / 91) = $109.89.
This refund is applied as a credit on the Q3 billing run.

Net Q3 adjustment for the Martinez household:
- Additional charge for contribution: +$390.11
- Refund for early termination: -$109.89
- Net adjustment: +$280.22 added to the Q3 fee

The billing detail report for Q3 will show the standard Q3 fee plus a line item for the Q2 adjustment with a reference to each underlying event.

### Example 3: Billing System Migration from Spreadsheet to Automated Platform

**Scenario:** A 15-advisor RIA managing $2.1 billion across 1,800 households currently calculates fees using a series of Excel workbooks maintained by two operations staff. The firm is migrating to an integrated billing module within their portfolio management system. The spreadsheet system has worked for years but is error-prone, poorly documented, and dependent on key personnel.

**Design Considerations:**
- The firm has 14 distinct fee schedules (including 6 legacy schedules that apply to fewer than 50 households each).
- Approximately 120 households have negotiated rates that differ from the standard schedule.
- The firm bills quarterly in advance, debiting from custodian accounts at Schwab and Fidelity.
- The migration must not disrupt the next quarterly billing cycle.

**Analysis:**

Phase 1 — Data Extraction and Documentation (Weeks 1-3):
- Export all fee schedules from the existing spreadsheets into a structured format (schedule name, tier breakpoints, rates, effective date).
- Document every negotiated rate override with the associated household, effective date, and authorizing advisor.
- Catalog all billing exceptions: waivers, caps, minimum overrides, split-billing arrangements, invoice-billed accounts.
- Extract two years of historical billing data (household, account, AUM, fee charged, period) for parallel-run comparison.

Phase 2 — System Configuration (Weeks 3-6):
- Configure all 14 fee schedules in the new billing module with correct tier structures and effective dates.
- Enter negotiated rate overrides per household.
- Configure billing preferences per household: collection method, billing account designation, proration rules.
- Set up custodian debit file formats for Schwab and Fidelity.
- Configure the approval workflow (preview, review, approve, submit).

Phase 3 — Parallel Run (Weeks 6-9, coinciding with one billing cycle):
- Run the new system in parallel with the spreadsheet process for one full quarterly cycle.
- Compare results at the household level. Accept a tolerance of $0.01 per household for rounding differences.
- Investigate and resolve every variance exceeding the tolerance.
- Common variance sources: different rounding methods, different day-count conventions for proration, fee schedule data entry errors, missing negotiated rate overrides.

Phase 4 — Cutover (Week 10):
- After parallel-run sign-off, the new system becomes the system of record.
- The spreadsheet process is retained as a reference but is no longer used for production billing.
- First live billing cycle is run with enhanced review (every household is spot-checked, not just exceptions).

Phase 5 — Post-Migration Monitoring (Weeks 10-22, two billing cycles):
- Heightened review of billing output for two additional cycles.
- Monitor client inquiries or complaints related to fee amounts.
- Validate that custodian debit files are accepted without error.
- Confirm revenue recognition entries in the accounting system match prior methodology.

Key success metrics:
- Zero missed billing cycles during migration.
- Variance rate below 0.5% of households in the first live cycle.
- Reduction in billing processing time from approximately 40 person-hours per quarter to under 8 person-hours.
- Elimination of single-point-of-failure key-person risk.
