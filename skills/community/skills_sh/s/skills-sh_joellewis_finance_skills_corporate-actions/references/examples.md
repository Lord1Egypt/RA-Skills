# Corporate Actions — Worked Examples

## Contents

1. [Example 1: Processing a Cash-and-Stock Merger Across Thousands of Client Accounts](#example-1-processing-a-cash-and-stock-merger-across-thousands-of-client-accounts) — Section 368 boot/basis allocation per tax lot, fractional cash-in-lieu, post-settlement reconciliation
2. [Example 2: Managing a Tender Offer with Oversubscription and Proration](#example-2-managing-a-tender-offer-with-oversubscription-and-proration) — election collection, default handling, odd-lot priority, proration math, realized gain per lot
3. [Example 3: Handling a Spin-Off with Fractional Shares and Cost Basis Allocation](#example-3-handling-a-spin-off-with-fractional-shares-and-cost-basis-allocation) — Form 8937 allocation percentages, per-lot basis split, fractional share gain/loss, firm-wide validation

## Example 1: Processing a Cash-and-Stock Merger Across Thousands of Client Accounts

**Scenario:** Acquirer Corp announces the acquisition of Target Inc. The merger terms are: for each share of Target Inc, shareholders receive $25.00 in cash plus 0.4 shares of Acquirer Corp stock. The merger is expected to close on March 15. Target Inc has CUSIP 876543210. Acquirer Corp has CUSIP 012345678. The firm holds Target Inc across 3,200 client accounts with positions ranging from 10 to 50,000 shares. Total firm-wide position is 4.8 million shares. Acquirer Corp's closing price on March 15 is $80.00.

**Design Considerations:**
- The merger terms are fixed (no election or proration), making this a mandatory action.
- Mixed consideration (cash + stock) means the tax treatment depends on the IRS characterization. Assume the merger qualifies as a reorganization under IRC Section 368, meaning the stock portion is tax-deferred but the cash portion ("boot") is taxable.
- Fractional shares of Acquirer Corp will be paid in cash-in-lieu at the closing price on the effective date.
- The firm must process this across two custodians (Schwab and Fidelity) and a self-clearing platform.

**Analysis:**

Step 1 — Pre-Event Validation:
Verify merger terms across DTCC, Bloomberg, and the issuer's proxy filing. Confirm: consideration per share ($25.00 cash + 0.4 shares), effective date (March 15), fractional share policy (cash-in-lieu at market), CUSIP changes, and tax treatment (Section 368 reorganization). Discrepancy check: Bloomberg initially reported the ratio as 0.40; DTCC reported 0.4000. These are consistent. No discrepancy.

Step 2 — Position Snapshot on Record Date:
Extract all accounts holding Target Inc as of the record date. For mergers, the record date is typically the effective date. Total: 3,200 accounts, 4,800,000 shares. Validate against custodian position files. Two accounts show discrepancies due to pending settlements — flag for manual review after settlement.

Step 3 — Entitlement Calculation (Per Account Example):
Client account holds 1,500 shares of Target Inc with the following tax lots:
- Lot 1: 800 shares, acquired 2019-06-15, cost basis $32.00/share ($25,600 total)
- Lot 2: 700 shares, acquired 2021-11-03, cost basis $38.00/share ($26,600 total)

Cash entitlement: 1,500 shares x $25.00 = $37,500.00.
Stock entitlement: 1,500 shares x 0.4 = 600.0 shares of Acquirer Corp (no fractional shares in this case).

For an account holding 113 shares:
Stock entitlement: 113 x 0.4 = 45.2 shares. Whole shares: 45. Fractional portion: 0.2 shares. Cash-in-lieu: 0.2 x $80.00 = $16.00.

Step 4 — Cost Basis Allocation (Section 368 Reorganization):
Under Section 368, the total cost basis in Target Inc shares carries over to the Acquirer Corp shares and any boot (cash) received. The allocation requires determining the relative fair market values of the stock and cash components.

Total consideration per share: $25.00 cash + 0.4 x $80.00 stock = $25.00 + $32.00 = $57.00.
Cash percentage: $25.00 / $57.00 = 43.86%.
Stock percentage: $32.00 / $57.00 = 56.14%.

For Lot 1 (800 shares, $25,600 total basis):
Basis allocated to cash: $25,600 x 43.86% = $11,228.07. Cash received: 800 x $25.00 = $20,000.00. Taxable gain on cash portion: $20,000.00 - $11,228.07 = $8,771.93.
Basis allocated to stock: $25,600 x 56.14% = $14,371.93. Shares received: 800 x 0.4 = 320 shares. Per-share basis: $14,371.93 / 320 = $44.91.

For Lot 2 (700 shares, $26,600 total basis):
Basis allocated to cash: $26,600 x 43.86% = $11,666.76. Cash received: 700 x $25.00 = $17,500.00. Taxable gain on cash portion: $17,500.00 - $11,666.76 = $5,833.24.
Basis allocated to stock: $26,600 x 56.14% = $14,933.24. Shares received: 700 x 0.4 = 280 shares. Per-share basis: $14,933.24 / 280 = $53.33.

Step 5 — System Processing:
For each of the 3,200 accounts, the processing engine executes atomically:
1. Remove the Target Inc position (all lots).
2. Credit cash for the cash component of the merger consideration.
3. Create new Acquirer Corp position with correctly allocated tax lots, preserving original acquisition dates for holding period purposes.
4. Credit cash-in-lieu for any fractional shares.
5. Record the taxable gain on the cash (boot) component per lot.

Step 6 — Post-Settlement Reconciliation:
Compare expected entitlements (cash and shares) against actual receipts from DTC. For Schwab-custodied accounts, compare the Schwab corporate action confirmation against the firm's calculations. Investigate any discrepancy. Common issues: pending settlements that altered the record-date position, DTC claiming adjustments for trades settling after the record date, and rounding differences on cash-in-lieu calculations.

## Example 2: Managing a Tender Offer with Oversubscription and Proration

**Scenario:** MegaCorp launches a self-tender offer to repurchase up to 10 million shares of its common stock at $50.00 per share (current market price: $46.50). The offer is open for 20 business days. The firm holds MegaCorp across 1,400 client accounts totaling 2.1 million shares. Clients may elect to tender all, some, or none of their shares.

**Design Considerations:**
- This is a voluntary action — clients must affirmatively elect to participate.
- The tender price represents a 7.5% premium to market, which may be attractive but clients must consider their investment thesis for holding MegaCorp.
- If total shares tendered across all holders exceed 10 million, the company will prorate acceptance on a pro-rata basis (with odd-lot priority for holders of fewer than 100 shares).
- The firm's internal election deadline is 3 business days before the DTC deadline to allow for aggregation and submission.
- Tendered shares that are accepted will generate a taxable event (capital gain or loss based on cost basis vs. $50.00 tender price).

**Analysis:**

Step 1 — Client Notification (Day 1-2 After Announcement):
Generate notifications to all 1,400 affected accounts. Each notification includes: tender price ($50.00), premium to market (7.5%), maximum shares the company will accept (10 million), election options (tender all, tender a specified number, or do not tender), the firm's default election (do not tender), internal election deadline, and a reminder that proration may apply if the offer is oversubscribed.

For advisory accounts, the advisor receives the notification and decides on behalf of the client within the scope of the advisory agreement. For self-directed accounts, the client receives the notification directly.

Step 2 — Election Collection (Days 2-17):
Elections trickle in over the offer period. The operations team tracks election status:
- 620 accounts elect to tender all shares (1,050,000 shares)
- 180 accounts elect to tender a portion of their shares (310,000 shares)
- 450 accounts elect not to tender
- 150 accounts have not responded by Day 15

For the 150 non-respondents, the firm sends a reminder notification on Day 15. By the internal deadline (Day 17), an additional 90 accounts respond (60 elect to tender, 30 elect not to tender). The remaining 60 non-respondents receive the default election of "do not tender."

Final election tally:
- Total shares elected to tender: 1,050,000 + 310,000 + 95,000 (from the 60 late responders) = 1,455,000 shares
- Total shares not tendering: remaining position

Step 3 — Election Submission (Day 17-18):
The firm submits its aggregated election of 1,455,000 shares to DTC via the PTOP system. The submission specifies the firm's participant number, the event ID, and the total shares tendered. At the account level, the firm maintains its own records of per-client elections.

Step 4 — Proration (After Expiration, Day 20+):
The tender offer expires. Total shares tendered across all holders: 18 million shares (oversubscribed by 80%). The company will accept 10 million shares, so the proration factor is 10,000,000 / 18,000,000 = 55.56%.

Odd-lot holders (fewer than 100 shares) are accepted in full per the offer terms. The firm identifies 45 odd-lot accounts totaling 2,800 shares — all accepted without proration.

For non-odd-lot accounts, the proration factor of 55.56% is applied:
- Example: Client elected to tender 5,000 shares. Accepted: 5,000 x 55.56% = 2,778 shares. Returned: 2,222 shares.
- Rounding: The agent rounds accepted shares down to the nearest whole share. Fractional shares are not accepted.

Firm-wide proration: 1,455,000 shares elected, less 2,800 odd-lot shares = 1,452,200 non-odd-lot shares. Accepted: 1,452,200 x 55.56% = 806,842 shares (rounded down per account). Returned: 645,358 shares plus the odd-lot difference.

Step 5 — Settlement Processing:
For each account with accepted shares:
1. Remove the tendered and accepted shares from the position.
2. Credit cash: accepted shares x $50.00.
3. Return the un-accepted (prorated) shares to the position.
4. Calculate realized gain or loss per tax lot on the accepted shares.

Example for one account:
- Pre-tender position: 5,000 shares, single tax lot, cost basis $42.00/share.
- Elected to tender: 5,000 shares. Accepted after proration: 2,778 shares. Returned: 2,222 shares.
- Cash received: 2,778 x $50.00 = $138,900.00.
- Cost basis of accepted shares: 2,778 x $42.00 = $116,676.00.
- Realized gain: $138,900.00 - $116,676.00 = $22,224.00.
- Remaining position: 2,222 shares at $42.00/share cost basis (unchanged).

Step 6 — Post-Settlement Activities:
Reconcile DTC settlement against expected entitlements. Verify that prorated quantities match the agent's published proration factor. Communicate final results to clients, including: shares accepted, shares returned, cash received, and realized gain/loss. Update tax lot records and performance systems.

## Example 3: Handling a Spin-Off with Fractional Shares and Cost Basis Allocation

**Scenario:** ParentCo announces it will spin off its technology division as NewTechCo. Distribution ratio: 1 share of NewTechCo for every 5 shares of ParentCo held on the record date of June 10. Fractional shares will be aggregated and sold on the open market, with cash-in-lieu distributed to holders. ParentCo currently trades at $120.00. NewTechCo is expected to begin trading at approximately $30.00. The IRS Form 8937 published by ParentCo allocates 80% of the pre-spin cost basis to ParentCo and 20% to NewTechCo.

The firm holds ParentCo across 2,500 accounts totaling 3.6 million shares.

**Design Considerations:**
- This is a mandatory action — no election is required.
- The 1:5 ratio will generate fractional shares for any position not evenly divisible by 5.
- Cost basis allocation must be applied at the individual tax lot level, not the aggregate position level.
- The spin-off creates a new security (NewTechCo) that must be set up in all systems before the distribution date.
- Performance calculation engines must link the ParentCo and NewTechCo positions to avoid distorting returns on the distribution date.

**Analysis:**

Step 1 — Pre-Event Setup:
Set up NewTechCo as a new security in the master security file: assign or receive the new CUSIP, establish pricing feeds, configure the security in the portfolio accounting system, and set up trading capabilities (the security may trade on a "when-issued" basis before the distribution date).

Step 2 — Position Analysis:
Extract all ParentCo positions as of the record date (June 10).
- Total shares: 3,600,000. Distribution ratio: 1:5. Total NewTechCo shares to distribute: 720,000.
- Accounts with positions evenly divisible by 5: 1,850 accounts (no fractional shares).
- Accounts with fractional share remainders: 650 accounts.

Fractional share example: Account holds 1,237 shares of ParentCo. NewTechCo entitlement: 1,237 / 5 = 247.4 shares. Whole shares: 247. Fractional: 0.4 shares. Total fractional shares across all 650 accounts are aggregated into whole shares, sold on the market, and the cash proceeds are allocated back to each account proportionally.

Step 3 — Cost Basis Allocation:
The issuer's Form 8937 specifies: 80% of pre-spin cost basis remains with ParentCo, 20% is allocated to NewTechCo.

Example for one account with two tax lots:
- Lot 1: 600 shares of ParentCo, acquired 2018-03-20, cost basis $85.00/share ($51,000 total).
- Lot 2: 637 shares of ParentCo, acquired 2022-08-11, cost basis $105.00/share ($66,885 total).

Lot 1 cost basis adjustment:
ParentCo retained basis: $51,000 x 80% = $40,800.00. New per-share basis: $40,800 / 600 = $68.00.
NewTechCo allocated basis: $51,000 x 20% = $10,200.00. NewTechCo shares from Lot 1: 600 / 5 = 120 shares. Per-share basis: $10,200 / 120 = $85.00.
Acquisition date for NewTechCo lot: inherits the original date of 2018-03-20 (holding period tacks).

Lot 2 cost basis adjustment:
ParentCo retained basis: $66,885 x 80% = $53,508.00. New per-share basis: $53,508 / 637 = $84.00.
NewTechCo allocated basis: $66,885 x 20% = $13,377.00. NewTechCo shares from Lot 2: 637 / 5 = 127.4 shares. Whole shares: 127. Fractional: 0.4 shares.

For the fractional 0.4 shares:
Basis of fractional portion: ($13,377.00 / 127.4) x 0.4 = $42.00 (approximately).
Cash-in-lieu received: 0.4 x $30.00 (market price at sale) = $12.00.
Realized loss on fractional share: $12.00 - $42.00 = -$30.00 (loss).

NewTechCo Lot 2 (whole shares only): 127 shares, basis = $13,377.00 - $42.00 = $13,335.00, per-share basis = $105.00. Acquisition date: 2022-08-11 (holding period tacks).

Step 4 — System Processing:
For each of the 2,500 accounts:
1. Reduce ParentCo per-share cost basis to 80% of original (per lot).
2. Create NewTechCo position with allocated tax lots (20% of original basis per lot), preserving original acquisition dates.
3. For accounts with fractional NewTechCo shares, record the cash-in-lieu amount and realized gain/loss on the fractional portion.
4. Verify that the sum of (adjusted ParentCo basis + NewTechCo basis + any fractional share basis used) equals the original pre-spin ParentCo basis for each lot.

Step 5 — Post-Processing Validation:
Run a firm-wide reconciliation:
- Total NewTechCo whole shares distributed should equal the total calculated entitlement minus aggregated fractional shares.
- Total cost basis across ParentCo (adjusted) + NewTechCo + fractional share basis should equal the total pre-spin ParentCo cost basis.
- Verify that no tax lot has a negative cost basis or an unreasonable per-share basis.
- Check that performance reports for the distribution date show a combined value (ParentCo + NewTechCo) approximately equal to the pre-spin ParentCo value, confirming no artificial gain or loss was created by the event.

Step 6 — Ongoing Monitoring:
The issuer's Form 8937 with the final allocation percentages may not be available until several weeks or months after the spin-off. If the firm used preliminary estimates (e.g., based on when-issued trading), the cost basis allocation must be revised when the final Form 8937 is published. This revision may require amended tax lot records and, if tax forms have already been issued, corrected 1099-Bs.

