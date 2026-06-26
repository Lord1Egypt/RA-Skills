# Worked Examples — Client Reporting and Delivery

## Table of Contents

1. [Redesigning a Quarterly Reporting Package](#example-1-redesigning-a-quarterly-reporting-package) — modular tier-based templates, production timeline, portal-first delivery for a 20-advisor RIA
2. [Transitioning from Print to Digital-First Delivery](#example-2-transitioning-from-print-to-digital-first-delivery) — phased rollout, e-delivery consent, adoption metrics for an older client base
3. [Remediating Performance Calculation Errors in Quarterly Reports](#example-3-remediating-performance-calculation-errors-in-quarterly-reports) — root cause analysis, data readiness gates, re-issuance process

### Example 1: Redesigning a Quarterly Reporting Package

**Scenario:**

A 20-advisor RIA firm managing $3.5 billion across 2,400 households is redesigning its quarterly reporting package. The current reports are generic, text-heavy PDF exports from the PMS with no customization by client segment. Advisors report that clients find the reports confusing, and the operations team spends two weeks each quarter manually adjusting reports for key clients. The firm uses Orion as its PMS and has a client portal but only 35% portal adoption. The firm wants a modern, tiered reporting approach with efficient production.

**Design Considerations:**

The report template structure should follow a modular design where sections can be toggled by client tier:

- **Cover page:** Firm-branded, household name, reporting period, headline metrics (portfolio value, quarterly return, year-to-date return, net contributions/withdrawals). Clean visual design with the firm's color palette.
- **Executive summary (1 page):** Firm-level market commentary (written by the CIO or investment committee) with an editable field for advisor personalization. Advisors for top-tier clients write 2-3 sentences specific to the client's situation.
- **Portfolio summary (1-2 pages):** Asset allocation chart (current vs target), allocation table, total portfolio value, cash position. Household-level view as the primary presentation.
- **Performance summary (1-2 pages):** TWR and MWR for the portfolio and each account. Periods: QTD, YTD, 1-year, 3-year, 5-year, since inception. Benchmark comparison with blended benchmark matching the portfolio's target allocation. Chart showing cumulative growth of portfolio vs benchmark since inception.
- **Holdings detail (2-5 pages, toggleable):** Complete position listing by asset class. Security name, ticker, shares, market value, percentage of portfolio, unrealized gain/loss. Included by default for HNW and UHNW tiers; excluded by default for mass affluent (available on request).
- **Transaction summary (1-2 pages, toggleable):** Purchases, sales, dividends, contributions, withdrawals, fees. Included for HNW and above by default.
- **Fee summary (1 page):** Quarterly fee calculation detail: beginning AUM, fee rate, fee amount, payment method. Always included for transparency.
- **Disclosures (1-2 pages):** Standard disclaimers, benchmark descriptions, firm information. Updated quarterly by compliance.

Client tier customization:

- **Mass affluent (under $1M):** Cover page, executive summary, portfolio summary, performance summary, fee summary, disclosures. Total approximately 6-8 pages. Simplified language, fewer metrics.
- **HNW ($1M-$10M):** All sections included. Approximately 12-18 pages. Full detail with benchmark comparison and advisor commentary.
- **UHNW ($10M+) and family office:** All sections plus performance attribution summary, alternative investment detail, multi-entity consolidation, and custom analytics. Approximately 20-30 pages. Advisor writes substantive personalized commentary for each household.

For digital delivery via the client portal: all reports are published to the Orion Connect portal with automated email notification. The email contains a branded message with the client's name and a direct link to the portal (no PDF attachment for security). To boost portal adoption from 35% toward 70%, the firm launches a portal onboarding campaign concurrent with the new report rollout, with advisors demonstrating the portal during quarterly review meetings.

The 10-business-day production workflow from quarter-end:

- T+1 to T+4: Data finalization, custodian reconciliation, corporate action processing.
- T+5 to T+6: Batch report generation for all households, exception report produced.
- T+6 to T+7: Automated QA validation, manual spot-check of a 10% sample plus all UHNW households.
- T+7 to T+8: Compliance review of a 5% sample plus all reports containing advisor-written commentary.
- T+7 to T+9: Advisor review and personalized commentary entry (runs in parallel with compliance review).
- T+9: Final approval by operations manager and compliance officer.
- T+10: Batch publication to portal, email notifications sent, print copies mailed for opt-in clients.

**Analysis:**

The modular template design eliminates manual per-client adjustments by encoding customization rules into the report generation configuration. Tier-based defaults reduce the operations team's workload from two weeks of manual adjustments to exception handling only. The 10-business-day cycle is achievable with disciplined data finalization and parallel compliance/advisor review stages. The portal-first delivery strategy, paired with an adoption campaign, should reduce print volume by 50% or more within two quarters. Key risk: advisor commentary delays can push the timeline past T+10, so the firm should establish a hard T+9 deadline for commentary with an auto-populated default if the advisor does not provide custom text.

### Example 2: Transitioning from Print to Digital-First Delivery

**Scenario:**

A 45-year-old advisory firm with 1,800 clients is transitioning from mailing printed quarterly reports to digital-first delivery. Currently, 100% of clients receive printed reports via USPS mail at a cost of $4.50 per report (printing, assembly, postage), totaling approximately $32,400 per year for quarterly reports alone. The firm has a client portal (Black Diamond Client Experience) but has never used it for report delivery. The client base skews older — 40% of clients are over 65 — and the firm is concerned about resistance to change.

**Design Considerations:**

The transition plan should balance efficiency gains with client experience, executed in phases:

**Phase 1 — Communication and consent (Month 1-2):**

- Send a personalized letter to all clients announcing the transition to digital delivery, emphasizing benefits (faster access, 24/7 availability, historical archive, environmental sustainability).
- Include a response form for delivery preference: digital-only (portal and email notification), digital with print supplement (portal access plus mailed copy), or print-only (opt-in exception, requires written request).
- Advisors call their top 50 clients personally to explain the transition and address concerns.
- E-delivery consent documentation collected and filed per SEC electronic delivery guidance.

**Phase 2 — Portal onboarding (Month 2-3):**

- Dedicated onboarding support: a team member or recorded webinar walks clients through portal registration, login, and report access.
- Simplified registration process: pre-populated registration links sent via email requiring only password creation.
- Mobile-friendly portal experience, since many older clients are comfortable with tablets even if not desktop computers.
- Printed quick-start guide mailed to all clients with step-by-step portal access instructions and support phone number.
- Advisors demonstrate the portal during every client meeting during the transition quarter.

**Phase 3 — Parallel delivery (Quarter 1 of new approach):**

- For the first quarterly cycle, deliver reports through both channels: publish to portal with email notification and mail printed copies. This gives clients a safety net and builds confidence in the digital experience.
- Track portal access: which clients logged in, viewed their report, and downloaded PDFs.
- Follow up with clients who did not access the portal, offering additional onboarding support.

**Phase 4 — Digital-first (Quarter 2 onward):**

- Default delivery switches to digital-only (portal publication with email notification).
- Clients who opted for print supplement or print-only continue receiving mailed copies.
- Quarterly review of print opt-in list: advisors gently encourage digital adoption during meetings.

**Exception handling for print-required clients:**

- Clients over age 80 or with documented technology barriers are automatically enrolled in the print supplement program.
- No client is denied printed reports if they request them.
- Print reports are identical to digital (same PDF), printed in color, and mailed in a firm-branded envelope.
- The firm budgets for 20-30% of clients remaining on print in Year 1, declining to 10-15% by Year 3.

**Compliance review of electronic delivery:**

- E-delivery consent forms reviewed by compliance counsel to ensure they meet SEC guidance requirements (informed consent, evidence of access, opt-out ability).
- Portal security reviewed: encryption in transit and at rest, authentication requirements (multi-factor authentication recommended), session timeout, and access logging.
- Record retention: portal automatically archives all published reports with delivery timestamp, satisfying books-and-records requirements. Emailed notification records are also retained.
- Privacy review: portal access controls ensure each client sees only their own data.

**Adoption metrics tracking:**

- Portal registration rate (target: 85% within 6 months).
- Active portal usage rate (logged in at least once per quarter; target: 65% within 12 months).
- Report access rate (percentage of clients who viewed their report within 14 days of publication).
- Print opt-in rate (track trend quarterly, targeting decline).
- Client satisfaction: survey question on report delivery satisfaction added to annual client survey.
- Cost savings: track printing, postage, and assembly cost reduction quarterly.

**Analysis:**

The phased approach minimizes client disruption while systematically driving digital adoption. The parallel delivery quarter is costly (double delivery) but critical for building client confidence. The 40% over-65 demographic is a legitimate concern, but portal adoption among older adults has increased significantly and the firm's approach of personal outreach, simplified onboarding, tablet-friendly design, and continued print availability mitigates the risk. Expected cost savings are substantial: if 70% of clients move to digital-only, annual printing and mailing costs drop from $32,400 to under $10,000, with additional savings in staff time for assembly and mailing. The compliance framework for e-delivery must be established before the first digital delivery, not after.

### Example 3: Remediating Performance Calculation Errors in Quarterly Reports

**Scenario:**

During a routine internal audit, a mid-size RIA discovers that approximately 5% of quarterly reports (60 out of 1,200 households) delivered in the most recent quarter contained performance calculation errors. The errors originated from late custodian data corrections for accounts holding a specific alternative investment fund that revised its NAV two weeks after the initial quarter-end pricing. The firm's reporting workflow generated reports using the preliminary NAV, and the corrected NAV arrived after reports were already delivered. The differences in reported returns ranged from 5 to 35 basis points, affecting since-inception and trailing-period returns for the affected accounts.

**Design Considerations:**

**Root cause analysis:**

The root cause is a timing mismatch between the report generation schedule and the data finalization timeline for alternative investments. The firm's standard T+7 report generation date assumed all custodian data was final, but the alternative investment fund in question consistently provides corrected NAVs at T+14 to T+18. The PMS ingested the corrected data after reports were generated and delivered, but no process existed to flag that delivered reports contained stale pricing for specific holdings.

Contributing factors: (a) no data readiness checklist identifying securities with known delayed pricing, (b) no automated comparison between report-date pricing and current PMS pricing after corrections, (c) the alternative investment was added to client portfolios 18 months ago without updating the reporting workflow to accommodate its pricing timeline.

**Data validation checks to implement:**

- **Pre-generation data readiness gate:** Before batch report generation, run an automated check confirming that all holdings have final pricing. Maintain a watchlist of securities with known delayed pricing (alternatives, private placements, international funds with delayed NAVs). If any watchlist security has preliminary pricing, delay report generation for affected accounts or flag them for manual review.
- **Post-generation pricing comparison:** After the custodian data correction window closes (T+20), automatically compare the pricing used in delivered reports against current PMS pricing. Flag any account where the pricing difference exceeds a materiality threshold (e.g., 10 basis points of return impact).
- **Alternative investment pricing tracker:** Maintain a log of all alternative investments with their expected pricing finalization dates. Cross-reference against the reporting calendar to identify conflicts.

**QA workflow enhancements:**

- Add a specific QA step for accounts holding alternative investments, private placements, or other securities with delayed pricing.
- Implement a two-tier generation process: generate reports for accounts with all-final pricing on the standard timeline (T+7); hold accounts with pending pricing data for a second generation run (T+18 to T+20) after corrections are received.
- Establish a materiality threshold for pricing changes: differences below 5 basis points may not warrant re-issuance; differences above 5 basis points trigger the re-issuance process.

**Re-issuance process for affected clients:**

1. Generate corrected reports for all 60 affected households using final pricing data.
2. QA review all corrected reports (100% review, not sampling, given the sensitivity).
3. Compliance review of corrected reports and the client communication.
4. Prepare a client communication letter (reviewed by compliance counsel) explaining: (a) a pricing correction for a specific investment affected the performance data in the previously delivered report, (b) the corrected report is enclosed/attached/available on the portal, (c) the actual portfolio holdings and transactions were not affected — only the reported performance calculation, (d) the specific line items that changed and the magnitude of the difference, and (e) an apology for the error and a description of the steps the firm is taking to prevent recurrence.
5. Deliver corrected reports and communication letter through each client's preferred channel. Advisors for top-tier clients call the client before or concurrently with the letter to provide a personal explanation.
6. File the corrected reports and communication in the firm's books and records, noting the original report, the correction, and the reason.

**Ongoing monitoring to prevent recurrence:**

- Quarterly review of the security watchlist for delayed-pricing holdings, updated as new investments are added to client portfolios.
- Monthly reporting operations meeting that includes a review of the data readiness gate results and any exceptions.
- Annual review of the reporting timeline relative to custodian data correction windows, adjusting the production calendar as needed.
- Error rate tracking: monitor the corrected-report rate quarterly with a target of zero re-issuances due to data timing issues.
- If the firm adds additional alternative investments, the onboarding process must include updating the reporting watchlist and confirming the pricing timeline is compatible with the report production schedule.

**Analysis:**

The 5% error rate, while seemingly modest, represents a meaningful compliance and reputational risk. Performance reporting accuracy is a fundamental fiduciary obligation, and delivering incorrect returns — even by a few basis points — erodes client trust. The remediation approach addresses both the immediate issue (corrected reports with transparent client communication) and the systemic cause (inadequate data readiness checking for delayed-pricing securities). The two-tier generation process adds operational complexity but is necessary for firms holding alternatives with delayed pricing. The materiality threshold (5 basis points) provides a practical standard for triggering re-issuance while avoiding excessive corrections for immaterial differences. The firm should also evaluate whether its compliance manual and supervisory procedures need updating to reflect the new QA steps and data readiness requirements.
