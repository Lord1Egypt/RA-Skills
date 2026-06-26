# Worked Examples — Order Management (Advisor)

### Example 1: Model Change Across 800 Accounts with Multi-Custodian Routing and Restrictions
**Scenario:** An RIA managing $1.2 billion across 800 client accounts decides to replace iShares Russell 1000 Value ETF (IWD) with Vanguard Value ETF (VTV) across its Large-Cap Value model portfolio. The 800 accounts are custodied at three custodians: 500 accounts at Schwab, 200 at Fidelity, and 100 at Pershing. The firm discovers that 50 of the 800 accounts have client-specific restrictions that prevent the trade: 30 accounts have tax restrictions (holding IWD shares with very low cost basis that the client has instructed not to sell), 15 accounts have ESG restrictions that exclude VTV due to its holdings in certain energy companies, and 5 accounts are in estate settlement with a trading freeze.

**Design Considerations:**

The trade workflow proceeds as follows:

The PMS generates 800 sell-IWD orders and 800 buy-VTV orders. For each account, the system calculates the exact share quantity based on the account's current IWD position and the target VTV allocation.

Pre-trade compliance screening flags the 50 restricted accounts: the 30 tax-restricted accounts receive hard blocks on the IWD sell (the client instruction to retain low-basis shares overrides the model change); the 15 ESG-restricted accounts receive hard blocks on the VTV buy (VTV fails the ESG screen); and the 5 estate accounts receive hard blocks on both sides (trading freeze). These 50 accounts are excluded from the trade list, and the portfolio manager is notified to determine alternative treatment — the tax-restricted accounts will retain IWD, the ESG-restricted accounts may receive an alternative ESG-compatible value ETF, and the estate accounts will be addressed after the trading freeze is lifted.

The remaining 750 accounts proceed to block aggregation. The OMS creates three custodian-level sub-blocks for each side of the trade: Schwab block (450 accounts, sell approximately 120,000 shares of IWD and buy approximately 150,000 shares of VTV), Fidelity block (200 accounts, sell approximately 55,000 shares of IWD and buy approximately 68,000 shares of VTV), and Pershing block (100 accounts, sell approximately 28,000 shares of IWD and buy approximately 35,000 shares of VTV).

Tax-lot selection for the IWD sell must be specified at the account level before aggregation. The firm's default method is specific identification with a tax-efficient priority: sell highest-cost-basis lots first, then short-term lots (to minimize the net gain), then long-term lots. For accounts with only low-basis lots and no tax restriction, the lots are sold per the default method. The OMS records the specific lot selection for each account as part of the pre-trade allocation documentation.

Each custodian sub-block is routed via FIX to the respective custodian. The IWD sell blocks are executed first to generate cash for the VTV purchases. Given the aggregate size (approximately 203,000 shares of IWD, representing roughly 2-3% of IWD's average daily volume), the trading desk elects to execute the IWD sells using a VWAP algorithm over two hours to minimize market impact. The VTV buys are executed after the IWD sells are confirmed, also via VWAP.

**Analysis:**

Post-execution, the OMS allocates fills to individual accounts using pro-rata allocation at the average execution price within each custodian sub-block. Each account at Schwab receives the same average price for its IWD sell and the same average price for its VTV buy. Because the three custodian sub-blocks may execute at slightly different average prices (due to timing differences and market movement), accounts at different custodians may receive slightly different prices. This is acceptable — fair allocation requires consistency within each block, not identical pricing across custodians.

The 50 excluded accounts are documented with the reason for exclusion and the alternative treatment plan. The compliance department reviews the exclusion list to confirm that each restriction was properly identified and applied. The portfolio manager signs off on the alternative treatment for each group of restricted accounts.

The entire process — from model change decision to allocation completion — should be documented in the OMS with timestamps, decision records, compliance check results, routing details, execution data, and allocation records. This audit trail satisfies SEC Rule 204-2 and provides the documentation needed for best execution review and supervisory oversight.

### Example 2: Trade Error Discovery and Correction
**Scenario:** On Tuesday afternoon, an operations analyst reviewing the daily trade blotter notices that an advisor entered a sell order for 1,000 shares of Johnson & Johnson (JNJ) in a client account. The account held 1,000 shares of JNJ, and the trade was executed at $158.50 per share (total proceeds: $158,500). However, the advisor intended to sell 1,000 shares of JPMorgan Chase (JPM), which the account also held, to raise cash for a planned withdrawal. The JNJ sale has already settled (the error is discovered on Wednesday, one day after the T+1 settlement). Meanwhile, JNJ has risen to $160.00 and JPM has fallen from $195.00 to $193.00.

**Design Considerations:**

The error correction process follows these steps:

First, the error is documented immediately: the operations analyst records the nature of the error (wrong security — JNJ sold instead of JPM), the account affected, the trade details, the person who entered the order, and the financial impact.

Second, the corrective trades are determined. To restore the client's account to its intended position:
- Buy back 1,000 shares of JNJ to restore the position. Current market price is $160.00, so the repurchase costs approximately $160,000 — a loss of $1,500 versus the $158,500 in sale proceeds ($160,000 - $158,500).
- Sell 1,000 shares of JPM to raise the cash the advisor originally intended. Current price is $193.00, versus $195.00 when the original trade should have been executed — a $2,000 opportunity cost ($195,000 - $193,000).

Third, the corrective trades are executed through the firm's error account. The JNJ repurchase at $160.00 and the JPM sale at $193.00 flow through the error account. The net cost to the firm is: the $1,500 loss on JNJ (bought back higher than sold) plus the $2,000 shortfall on JPM (sold at a lower price than was available when the original trade should have occurred), totaling approximately $3,500. The client's account is made whole — it ends up holding the same securities it would have held if the correct trade had been executed, and the cash raised is $193,000 (the JPM proceeds) rather than the $195,000 that would have been available on Tuesday, but the firm absorbs this difference.

Fourth, the client is notified. The advisor calls the client to explain the error, the correction, and that the client has been made whole. A written confirmation follows.

**Analysis:**

The firm should investigate how the error occurred and what controls could prevent it. Potential OMS enhancements include: (1) security validation that requires the advisor to confirm the security name in addition to the ticker symbol before submission — displaying "Johnson & Johnson (JNJ)" prominently on the order confirmation screen would help catch ticker confusion; (2) a warning when an order would liquidate an entire position, prompting the advisor to confirm intent; (3) a reconciliation check that compares the security being sold against the stated purpose of the trade (if the advisor flagged the trade as "cash raise for withdrawal," the system could verify that the selected security aligns with the cash-raise priority methodology).

The error, correction, and associated costs are logged in the firm's error account records and reported to compliance. If the firm is a dual registrant with a broker-dealer, the error may need to be evaluated under FINRA Rule 4530 for reportability. The error account activity is subject to supervisory review and regulatory examination.

Over time, the firm should analyze error patterns. If wrong-security errors are recurring, it may indicate systemic issues with the OMS interface, training gaps, or workflow problems that need to be addressed.

### Example 3: Multi-Custodian Best Execution Review
**Scenario:** A mid-size RIA custodies client assets at three custodians — Schwab (60% of AUM), Fidelity (30% of AUM), and Pershing (10% of AUM). The firm's compliance committee has tasked the trading desk with conducting the annual best execution review to evaluate execution quality across all three custodians and document findings for the firm's fiduciary records.

**Design Considerations:**

The best execution review should follow a structured methodology:

Data collection: The OMS maintains execution records for all trades at each custodian. The trading desk extracts 12 months of trade data including: security, order type, order size, execution price, National Best Bid and Offer (NBBO) at time of execution, execution venue, fill time (time from order submission to execution), price improvement or disimprovement versus NBBO, and effective spread (the difference between the execution price and the midpoint of the NBBO at the time of order entry). This data is segmented by custodian, security type (equity, ETF, mutual fund, fixed income), order size, and market conditions.

Evaluation criteria: The review evaluates each custodian across multiple dimensions:
- **Price improvement:** What percentage of orders received price improvement (executed at a better price than the NBBO)? What is the average price improvement in cents per share? Schwab, Fidelity, and Pershing each publish their own price improvement statistics, but the firm should independently verify using its own trade data.
- **Effective spread:** The average effective spread (execution price minus midpoint) across all trades. A lower effective spread indicates better execution quality.
- **Fill rate:** What percentage of limit orders were filled? What is the average time to fill?
- **Rejection rate:** What percentage of orders were rejected by the custodian, and what were the reasons?
- **Market impact:** For larger orders, did the execution move the market price? What is the average implementation shortfall (the difference between the decision price and the average execution price)?
- **Execution venue analysis:** Where are orders being routed — to the custodian's internal execution desk, to external market makers, or to exchanges? Are there any concerns about payment for order flow affecting execution quality?

Comparative analysis: The trading desk compares execution quality metrics across the three custodians using standardized measures. For example, if Schwab provides average price improvement of 1.2 cents per share on equity orders while Fidelity provides 0.8 cents and Pershing provides 1.0 cent, this difference is documented. However, best execution is not determined by a single metric — the review must consider the totality of factors including execution speed, reliability, order handling capabilities, and the overall cost of the custodial relationship.

**Analysis:**

The review findings are documented in a written report that includes: the methodology used, the data period and sample size, the metrics evaluated, the results for each custodian, a comparative analysis, and conclusions. If the review identifies material execution quality concerns at any custodian — for example, consistently poor price improvement or high rejection rates — the report should include recommended actions such as engaging the custodian to discuss execution practices, modifying order routing preferences, or in extreme cases considering a custodian change for affected accounts.

The report is presented to the compliance committee and retained as part of the firm's books and records. SEC and FINRA examiners routinely request best execution review documentation. The review should reference the firm's best execution policy, which establishes the frequency of reviews (at least annually), the metrics to be evaluated, the responsible parties, and the escalation process for identified deficiencies.

The OMS facilitates this process by maintaining comprehensive execution data in a structured, queryable format. Firms without adequate OMS reporting capabilities may need to supplement with data from custodian execution quality reports (Rule 605 reports, formerly Rule 11Ac1-5) and Transaction Cost Analysis (TCA) services provided by third-party vendors.
