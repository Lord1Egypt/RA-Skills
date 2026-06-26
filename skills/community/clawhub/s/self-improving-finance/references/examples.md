# Entry Examples

Concrete examples of well-formatted finance entries with all fields. All data is anonymized.

## Learning: Reconciliation Error (FX Conversion Rate)

```markdown
## [LRN-20250415-001] reconciliation_error

**Logged**: 2025-04-15T10:30:00Z
**Priority**: high
**Status**: pending
**Area**: accounting

### Summary
FX conversion using spot rate instead of weighted-average rate for P&L items causes translation variance at consolidation

### Details
Subsidiary Entity B reported P&L in local currency. During consolidation, the translation
used the spot rate at the reporting date for income statement items instead of the
weighted-average rate for the period. Under ASC 830 (and IAS 21), income statement items
should be translated at the average rate for the period unless the rate fluctuated
significantly enough to warrant transaction-date rates. The spot rate approach overstated
revenue by approximately X% and created a CTA (cumulative translation adjustment)
variance of $X.XM that required a top-side adjusting entry.

### Correct Treatment

**Before (incorrect):**
P&L line items translated at month-end spot rate (1 USD = X.XX LCU).
Revenue and expenses distorted by end-of-period rate spike.

**After (correct):**
P&L line items translated at weighted-average rate for the period
(1 USD = X.XX LCU average). Rate table sourced from treasury's
published monthly averages. CTA reflects only balance sheet translation.

### Suggested Action
Add close checklist step: "Verify FX rates for P&L translation use weighted-average
rate per ASC 830-10-45-17. Cross-check against treasury rate table."
Update ERP translation profile for affected entities.

### Metadata
- Source: close_review
- Framework: US_GAAP
- Related Accounts: Revenue accounts (anonymized), CTA equity account
- Tags: fx, translation, consolidation, ASC-830, average-rate
- Pattern-Key: reconciliation.fx_conversion

---
```

## Learning: Control Weakness (JE Approval Bypass)

```markdown
## [LRN-20250416-001] control_weakness

**Logged**: 2025-04-16T09:15:00Z
**Priority**: critical
**Status**: pending
**Area**: audit

### Summary
Journal entries under $10K bypassing approval workflow due to ERP threshold misconfiguration

### Details
During SOX testing of the journal entry approval control (Control ID: JE-001), it was
discovered that the ERP approval workflow had a $10K threshold — entries below this
amount posted directly without requiring a second approver. In Q2, 47 journal entries
totaling $X.XM were posted without any approval stamp. While no individual entry was
material, the aggregate amount and the control design gap represent a significant
deficiency under PCAOB AS 2201.

The root cause was a system configuration change during an ERP upgrade that reset the
approval threshold from $0 to $10K.

### Correct Treatment

**Before (control gap):**
ERP threshold set at $10K — entries below this amount bypass approval.

**After (remediated):**
ERP threshold set to $0 — all journal entries require dual approval.
Added compensating detective control: daily report of entries posted
without approver, reviewed by controller.

### Suggested Action
1. Reset ERP approval threshold to $0 (all entries require approval)
2. Add detective control: daily unapproved JE report
3. Retroactively review and approve the 47 bypassed entries
4. Add to SOX control matrix: "System configuration review after each ERP upgrade"

### Metadata
- Source: control_test
- Framework: SOX
- Related Accounts: Various GL accounts affected by unapproved JEs
- Tags: SOX, journal-entry, approval, ERP, PCAOB, significant-deficiency
- Pattern-Key: control.je_approval_bypass

---
```

## Learning: Regulatory Gap (ASC 842 Embedded Leases)

```markdown
## [LRN-20250417-001] regulatory_gap

**Logged**: 2025-04-17T14:00:00Z
**Priority**: high
**Status**: pending
**Area**: accounting

### Summary
New lease accounting standard ASC 842 not applied to embedded leases in service contracts

### Details
During the annual review of ASC 842 compliance, it was identified that several long-term
service contracts containing embedded lease components had not been assessed for lease
classification. The contracts (with vendors for data center space, dedicated equipment,
and managed fleet services) contain identifiable assets with the right to control use,
meeting the definition of a lease under ASC 842-10-15.

The impact is estimated at $X.XM in unrecognized right-of-use assets and corresponding
lease liabilities. These should have been recognized at the later of the adoption date
or contract commencement.

### Correct Treatment

**Before (gap):**
Service contracts treated entirely as operating expenses.
No embedded lease assessment performed.

**After (correct):**
Each service contract reviewed for embedded lease components per
ASC 842-10-15-2 through 15-42. Identified components separated
and recognized as ROU assets with corresponding lease liabilities.

### Suggested Action
1. Create embedded lease assessment checklist for all service contracts >$X per year
2. Add to annual close calendar: "Q4 — Embedded lease reassessment for new/renewed contracts"
3. Train AP team on embedded lease identification triggers
4. Update contract review process to flag lease-like provisions

### Metadata
- Source: regulatory_update
- Framework: US_GAAP
- Related Accounts: ROU asset, lease liability, operating expense (anonymized)
- Tags: ASC-842, embedded-lease, right-of-use, service-contracts
- Pattern-Key: regulatory.asc842_embedded_lease

---
```

## Finance Issue: Forecast Variance (Revenue Miss)

```markdown
## [FIN-20250418-001] forecast_variance

**Logged**: 2025-04-18T16:00:00Z
**Priority**: medium
**Status**: pending
**Area**: budgeting

### Summary
Q3 revenue forecast 25% above actual due to delayed deal closings not reflected in pipeline weighting

### Issue Details
Q3 revenue came in at $X.XM against a forecast of $X.XM (approximately 25% variance).
The primary driver was $X.XM in deals classified as "likely to close in Q3" that
slipped to Q4 or were lost. The forecast methodology weighted pipeline deals at 80%
probability for "verbal commit" stage, but historical close rates for this stage are
closer to 55%.

### Root Cause
Forecast model used a flat 80% probability for all deals in "verbal commit" stage
without adjusting for deal size, customer segment, or historical close rates by
sales representative. Large enterprise deals have structurally longer closing cycles
that the model did not account for.

### Impact
- Financial statement impact: N/A (forecast, not actuals)
- Operational impact: Hiring and capacity plans built on inflated revenue assumptions
- Cash flow impact: Working capital plan assumed higher collections in Q4

### Remediation
1. Revise pipeline stage probabilities based on trailing 8-quarter close rate data
2. Add deal-size adjustment factor (deals >$X.XM get 15% probability haircut)
3. Implement weekly pipeline scrub meeting with sales leadership
4. Add forecast accuracy KPI to management dashboard

### Context
- Trigger: variance_analysis
- Period: Q3 FY2025
- Entity: Corporate (consolidated)
- System: CRM pipeline report, FP&A forecast model

### Metadata
- Materiality: immaterial (forecast only)
- Related Accounts: Revenue line items (anonymized)
- See Also: FIN-20250118-003 (Q1 similar variance at 18%)

---
```

## Finance Issue: Cash Flow Anomaly (Early Vendor Payment)

```markdown
## [FIN-20250419-001] cash_flow_anomaly

**Logged**: 2025-04-19T11:30:00Z
**Priority**: high
**Status**: pending
**Area**: treasury

### Summary
Unexpected $X.XM cash outflow from early vendor payment outside standard payment terms

### Issue Details
Treasury identified a $X.XM cash outflow on day 15 of the month that was not in the
13-week cash forecast. Investigation revealed an AP payment run that settled invoices
30 days before their due date. The invoices had standard Net-60 terms but were included
in an accelerated payment batch intended only for vendors offering early-payment discounts.

### Root Cause
The AP payment run selection criteria included all invoices from vendors in a "preferred"
tier, regardless of whether those vendors offered early-payment discounts. The ERP
payment proposal logic did not distinguish between discount-eligible and standard-terms
invoices within the same vendor tier.

### Impact
- Financial statement impact: Immaterial (timing only, not amount)
- Operational impact: Cash position dropped below minimum covenant threshold for 2 days
- Cash flow impact: $X.XM timing difference; recovery expected at next regular cycle

### Remediation
1. Update payment proposal logic to require discount flag for early payment
2. Add treasury sign-off for any payment run exceeding $X.XM
3. Implement daily cash position alert when balance approaches covenant minimum
4. Review and correct vendor tier assignments

### Context
- Trigger: reconciliation
- Period: Month 4, FY2025
- Entity: Entity A (operating company)
- System: ERP AP module, treasury management system

### Metadata
- Materiality: immaterial (timing)
- Related Accounts: Cash, AP (anonymized)

---
```

## Feature Request: Automated Three-Way Reconciliation

```markdown
## [FEAT-20250420-001] automated_three_way_recon

**Logged**: 2025-04-20T09:00:00Z
**Priority**: medium
**Status**: pending
**Area**: accounts_payable

### Requested Capability
Automated three-way match reconciliation comparing purchase orders, goods receipts,
and vendor invoices — with tolerance thresholds and exception routing.

### User Context
Current three-way match is performed manually in spreadsheets, taking approximately
40 hours per month across the AP team. Mismatches are identified an average of 15 days
after invoice receipt, delaying vendor payments and incurring late-payment penalties.
Automation would reduce matching time by an estimated 80% and catch exceptions within
24 hours.

### Complexity Estimate
complex

### Suggested Implementation
1. Extract PO, GR, and invoice data from ERP via scheduled API
2. Apply matching rules: quantity within 2% tolerance, price within $X or 1%
3. Route exceptions by type: price variance → procurement, quantity → warehouse, missing GR → receiving
4. Dashboard showing match rate, exception aging, and processing time
5. Auto-approve perfect matches and create payment proposals

### Metadata
- Frequency: recurring
- Related Features: ERP AP module, procurement workflow, receiving system

---
```

## Learning: Promoted to Close Checklist

```markdown
## [LRN-20250410-003] reconciliation_error

**Logged**: 2025-04-10T11:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: close checklist (Month-End Close Procedures v3.2)
**Area**: accounting

### Summary
Intercompany elimination entries must be verified against both entities before consolidation posting

### Details
Found 5 instances over 3 months where intercompany elimination entries were posted
based on only one entity's sub-ledger balance. When the counterparty entity had
timing differences (e.g., goods in transit, service accruals recognized in different
periods), the elimination created an imbalance in the consolidated trial balance.
Correction required manual identification and top-side adjustments, adding 2 days
to the close cycle each time.

### Correct Treatment

**Before (incomplete):**
Post IC elimination based on reporting entity's balance only.

**After (correct):**
Reconcile IC balances between both counterparty entities before posting
eliminations. Resolve timing differences with adjusting entries at entity
level prior to consolidation.

### Suggested Action
Added to close checklist: "☐ Reconcile all intercompany balances between counterparty
entities. Resolve differences >$X before posting elimination entries."

### Metadata
- Source: close_review
- Framework: US_GAAP
- Related Accounts: Intercompany receivable/payable, elimination accounts (anonymized)
- Tags: intercompany, elimination, consolidation, timing-difference
- Pattern-Key: reconciliation.ic_elimination_imbalance
- Recurrence-Count: 5
- First-Seen: 2025-01-31
- Last-Seen: 2025-04-10

---
```

## Learning: Promoted to Skill (Month-End Reconciliation Checklist)

```markdown
## [LRN-20250412-001] reconciliation_error

**Logged**: 2025-04-12T15:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/month-end-reconciliation-checklist
**Area**: accounting

### Summary
Systematic month-end account reconciliation checklist covering bank, intercompany, sub-ledger, and accrual accounts

### Details
Developed a repeatable reconciliation checklist after encountering 8 separate
reconciliation breaks over 4 months across different account types. The root causes
were consistently: missing cutoff procedures, incomplete sub-ledger to GL matching,
and timing differences not resolved before close. The checklist standardizes the
reconciliation sequence, defines tolerance thresholds, and establishes escalation
paths for unresolved items.

### Suggested Action
Follow the month-end reconciliation checklist:
1. Bank reconciliation — match all cleared items, investigate outstanding >5 days
2. Intercompany — reconcile with counterparty, resolve differences before elimination
3. Sub-ledger to GL — tie AR, AP, FA sub-ledgers to GL control accounts
4. Accruals — verify completeness against PO commitments and recurring items
5. Prepaid/deferred — amortize per schedule, verify remaining balance reasonableness

### Metadata
- Source: close_review
- Framework: US_GAAP
- Related Accounts: Multiple (anonymized)
- Tags: reconciliation, month-end, close, checklist, bank, intercompany, sub-ledger
- See Also: LRN-20250410-003, FIN-20250228-001, FIN-20250331-004

---
```
