# Post-Trade Compliance — Worked Examples

### Example 1: Building a Trade Surveillance Program for a Mid-Size Broker-Dealer

**Scenario:** A broker-dealer with 120 registered representatives, $8 billion in customer assets, and business lines spanning equities, fixed income, and listed options is building a formal trade surveillance program. The firm currently relies on ad hoc supervisory review and basic exception reports (concentration, large trades) but has no systematic surveillance for manipulative trading patterns. FINRA's most recent examination identified the absence of structured surveillance as a deficiency.

**Step 1 — Scope and risk assessment.**

The surveillance program must cover the firm's entire business: equity trading (agency and principal), fixed income (corporate and municipal bonds), and listed options. Begin with a risk assessment mapping each business line to the applicable manipulative trading patterns:

- For equities: front-running, churning, wash trading, marking the close, layering/spoofing, insider trading, coordinated trading
- For fixed income: excessive markups/markdowns, interpositioning, trading ahead of customer orders, best execution deviations
- For options: front-running using options, manipulation of underlying securities to affect options values, and unauthorized options trading beyond approved strategy levels

**Step 2 — Data infrastructure.**

Inventory all data sources: the order management system (order timestamps, account IDs, security IDs, order terms), the execution platform (fill prices, quantities, venues, counterparties), the account master (customer profiles, investment objectives, risk tolerance, account type), market data feeds (prices, volumes, index levels, benchmark rates), and the firm's restricted and watch lists.

Identify gaps: Does the OMS capture order receipt time with sufficient precision for front-running detection? Are account relationships (households, common beneficial owners) mapped for coordinated trading analysis? Are fixed income markup calculations available for post-trade review? Remediate data gaps before deploying surveillance analytics.

**Step 3 — Alert design and calibration.**

For each pattern identified in the risk assessment, design alert logic with quantitative thresholds:

- **Churning:** Flag accounts where the annualized turnover ratio exceeds 4 or the cost-to-equity ratio exceeds 12% on a rolling 6-month window. Set a higher threshold (turnover > 6, cost-to-equity > 20%) for immediate escalation. Exclude accounts with documented active trading mandates.
- **Front-running:** Correlate proprietary and employee account trades with customer block orders received within the preceding 60 minutes. Flag instances where the direction matches, the customer order is large enough to move the market (e.g., greater than 10% of average daily volume), and the employee or proprietary trade precedes the customer execution.
- **Marking the close:** Flag orders entered in the last 10 minutes of the trading session in securities where the firm or its clients hold positions sensitive to the closing price (e.g., options positions, performance-fee calculations, mutual fund NAV determinations). Require that the flagged order exceeds 5% of the final-10-minute volume for the security.
- **Wash trading:** Identify buy-sell pairs in the same security, same account (or related accounts), within a 5-minute window, with no change in net position. Also monitor cross-account wash patterns among accounts sharing a common beneficial owner or adviser.
- **Insider trading:** Correlate trading in securities appearing on the firm's watch list (securities for which the firm may possess MNPI due to investment banking or advisory relationships) with material corporate events occurring within 30 days after the trade. Flag trades by employees, their households, and accounts over which the firm exercises discretion.

**Step 4 — Investigation workflow and staffing.**

Establish a tiered investigation workflow. Assign two full-time surveillance analysts and a senior compliance officer to oversee the program. Define SLAs: high-priority alerts (front-running, insider trading) investigated within 3 business days; medium-priority (churning, marking the close) within 10 business days; low-priority (minor allocation deviations) within 20 business days. Implement a case management system to track each alert from generation through disposition, capturing investigator notes, evidence, and supervisory sign-off.

**Step 5 — Governance and tuning.**

Establish a quarterly surveillance review in which the compliance team presents alert volumes, disposition statistics, false positive rates, and findings to senior management. Use disposition data to tune thresholds — if 95% of churning alerts are false positives, consider tightening the threshold or adding qualifying criteria (e.g., also requiring that the account has a conservative investment objective). Document all tuning decisions and rationale. Annually, engage an independent party (internal audit or outside consultant) to assess the surveillance program's effectiveness, consistent with the expectation of FINRA Rule 3120 (supervisory control system testing).

**Step 6 — Regulatory readiness.**

Maintain examination-ready documentation including: the surveillance policy and procedures manual, the risk assessment, alert calibration methodology and tuning history, sample investigation case files demonstrating thorough analysis, disposition statistics showing timely review, and evidence of senior management oversight. During examinations, FINRA and the SEC will request a walkthrough of the surveillance program, review a sample of closed alerts, and assess whether the firm's surveillance is commensurate with its business risk profile.

### Example 2: Implementing Allocation Fairness Monitoring for an RIA Managing Model Portfolios

**Scenario:** A registered investment adviser manages $2.5 billion across 800 client accounts using a model portfolio approach. The firm executes block trades and allocates fills across accounts using a pro-rata method. A recent compliance review identified that allocation records are maintained in spreadsheets with minimal oversight, and no systematic monitoring exists to verify fairness. The CCO wants to implement a post-trade allocation fairness monitoring system.

**Step 1 — Establish the allocation policy.**

Before monitoring can be effective, the firm must have a clear, written allocation policy. The policy should specify:

- Block trades are allocated pro rata based on each account's target participation at the time the order is placed
- Partial fills are allocated pro rata, with rounding adjustments distributed based on a defined methodology (e.g., largest remainder method)
- De minimis exceptions: allocations that would result in fractional shares or odd lots below a threshold may be adjusted
- IPO and new issue allocations follow FINRA Rules 5130 and 5131 restrictions
- Any deviation from pro-rata allocation must be documented with a rationale and approved by the CCO

**Step 2 — Data infrastructure.**

Build a data pipeline that captures:

- The pre-trade allocation schedule (which accounts are participating and at what target percentage)
- Execution data (fill prices, quantities, timestamps, venues)
- The post-trade allocation record (which accounts received which fills at which prices)
- Account metadata (account type, fee structure, whether the account is a proprietary account, a performance-fee account, or an account of a firm principal or employee)

The pre-trade allocation schedule is critical — without it, the firm cannot verify whether post-trade allocations match the intended pro-rata distribution.

**Step 3 — Pro-rata verification.**

For each block trade, compute the expected allocation for each account (target percentage multiplied by total shares filled) and compare to the actual allocation. Flag deviations exceeding a defined tolerance (e.g., more than 1% relative deviation or more than 100 shares absolute deviation, whichever is smaller). For partial fills, verify that the partial allocation preserves the pro-rata distribution.

Investigate flagged deviations: legitimate reasons include rounding, odd-lot avoidance, account-level restrictions (e.g., an account that cannot hold a particular security due to client guidelines), and minimum lot requirements.

**Step 4 — Dispersion analysis.**

For each block trade allocated across multiple accounts, compute the dispersion of average execution prices across accounts. In a perfectly fair allocation, all accounts receive the same average price (the block's average execution price). Compute the standard deviation of account-level average prices and flag block trades where any account's average price deviates by more than a defined threshold from the block average (e.g., more than 5 basis points).

High dispersion may indicate sequential allocation rather than average-price allocation, timing manipulation, or cherry-picking.

**Step 5 — Systematic favoritism detection.**

On a monthly and quarterly basis, run a longitudinal analysis across all block trades. For each account, compute the average allocation quality (measured as the difference between the account's average execution price and the block benchmark, aggregated across all block trades in the period). Rank accounts by allocation quality and test for patterns:

- Test whether proprietary accounts, performance-fee accounts, or accounts of firm principals consistently receive better-than-average allocations
- Use statistical tests (t-test or Mann-Whitney U test) to determine whether the observed differences are statistically significant
- If the firm manages both wrap-fee and commission-based accounts, test whether allocation quality differs between the two — commission-based accounts generate per-trade revenue and may be disfavored in allocation

**Step 6 — Reporting and governance.**

Produce a monthly allocation fairness report for the CCO summarizing: total block trades, number of flagged deviations, root causes of deviations, and results of the systematic favoritism analysis. The CCO should review and sign off on the report.

On a quarterly basis, present allocation fairness findings to the firm's investment or compliance committee. Annually, the allocation fairness monitoring program should be reviewed for effectiveness, and the statistical thresholds should be recalibrated based on the prior year's data. Maintain all reports, investigation files, and committee minutes as examination-ready documentation.
