# STP & Automation — Worked Example

## Example 1: Designing an STP Framework for a Broker-Dealer's Trade Processing Operations

**Scenario.** A mid-size broker-dealer processes approximately 15,000 equity trades and 3,000 fixed income trades per day. Currently, the equity STP rate is 72% and the fixed income STP rate is 45%. The operations team of 28 people spends most of their time on manual exception handling. The COO has set a target of 90% equity STP and 70% fixed income STP within 12 months.

**Design Considerations:**
- The firm uses a legacy order management system (OMS) that generates trades in a proprietary format, a middle-office system that handles allocation and confirmation, and a back-office system that handles settlement and booking.
- The three systems communicate via batch files exchanged every 30 minutes during the trading day and hourly overnight.
- The most common equity exceptions are counterparty SSI mismatches (28% of exceptions), allocation discrepancies (22%), and late trade reporting by the trading desk (18%).
- The most common fixed income exceptions are security identifier mismatches (31%), non-standard settlement terms (24%), and manual enrichment requirements for structured products (19%).

**Analysis:**

Phase 1 — Data quality remediation (months 1-3). The highest-impact STP improvement comes from fixing the data, not changing the processing logic.

For equity counterparty SSI mismatches (28% of equity exceptions): audit the SSI database against the top 50 counterparties by volume. These 50 counterparties likely represent 80%+ of SSI-related breaks. Update stale or incorrect SSIs, establish a process for counterparties to confirm SSI changes proactively, and implement automated SSI validation against the DTCC ALERT database.

For fixed income security identifier mismatches (31% of fixed income exceptions): the root cause is typically that the OMS uses one identifier (e.g., CUSIP) while the counterparty uses another (e.g., ISIN). Implement a security master cross-reference service that maps between identifier types. When an incoming message uses an identifier type not stored in the system, the cross-reference service translates it automatically.

For allocation discrepancies (22% of equity exceptions): standardize allocation instructions. Require the trading desk to submit allocation instructions with the block trade rather than after the fact. Implement validation that allocation quantities sum to the block quantity and that all allocation accounts are valid and active.

Expected STP improvement from Phase 1: equity from 72% to 82%, fixed income from 45% to 58%.

Phase 2 — Integration upgrade (months 3-8). Replace the 30-minute batch file exchange between the OMS and middle-office system with a message queue (e.g., Kafka). This delivers several benefits:

- Trades flow to the middle office within seconds of execution rather than waiting up to 30 minutes for the next batch. This eliminates the late-trade-reporting exception category for all trades reported to the OMS in real time.
- Failed messages are retained in the queue and can be retried automatically, eliminating the manual file-reprocessing procedures.
- The message queue supports event-driven processing: when a trade message arrives, it immediately triggers allocation, enrichment, and confirmation workflows rather than waiting for a batch scheduler.

Implement a real-time API integration with the DTCC for trade confirmation matching, replacing the current end-of-day batch matching. This enables same-day confirmation matching and earlier identification of mismatches.

Expected STP improvement from Phase 2: equity from 82% to 88%, fixed income from 58% to 65%.

Phase 3 — Auto-resolution and rule enhancement (months 8-12). With the major data quality and integration issues addressed, the remaining exceptions are lower-volume, more varied, and require more nuanced resolution. Implement auto-resolution rules for the most common remaining exception types:

- For minor SSI field differences (e.g., abbreviated vs. full counterparty name), implement fuzzy matching with a confidence threshold. Matches above 95% confidence auto-resolve; below 95% route to manual review.
- For fixed income non-standard settlement terms: build a settlement convention library that maps security type, market, and counterparty to the expected settlement terms. Automatically apply the correct convention when the trade does not specify terms explicitly.
- For structured product enrichment: pre-load security master data for actively traded structured products so the system does not need manual enrichment when a trade in a known security arrives.

Implement STP rate dashboards with daily reporting to operations management. Establish a weekly exception review meeting where the top 5 exception categories from the prior week are analyzed and remediation actions assigned.

Expected STP improvement from Phase 3: equity from 88% to 91%, fixed income from 65% to 72%.

**Key success metrics for the 12-month program:**
- Equity STP rate: 72% to 91% (target 90% — achieved)
- Fixed income STP rate: 45% to 72% (target 70% — achieved)
- Daily manual exceptions: reduced from approximately 5,600 to approximately 2,000
- Operations headcount redeployed from exception handling to process improvement and controls: 8 of 28 staff

