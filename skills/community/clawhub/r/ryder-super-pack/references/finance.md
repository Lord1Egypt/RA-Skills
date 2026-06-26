# Finance (OpenClaw Optimized)

This reference defines high-performance financial workflows for AI agents in the OpenClaw environment, merging precise accounting with advanced data analysis.

## 1. Financial Statements & Analysis

### Tool-Driven Reporting
- **Data Source**: Use `read` to ingest CSV/JSON exports from ERP systems.
- **Analysis**: Use `exec` with Python (`pandas`, `numpy`) for:
  - **QoQ/YoY Comparisons**: Automate the calculation of variance and % change.
  - **Ratio Analysis**: Calculate Liquidity, Leverage, and Efficiency ratios.
  - **Waterfall Charts**: Generate a `VARIANCE_REPORT.md` that explains the "why" behind the numbers.

---

## 2. Month-End Close & Reconciliation

### The Autonomous Accountant
- **Bank Recs**: Use `read` on bank statements and GL extracts to flag discrepancies.
- **Accrual Logic**: Automatically generate `JOURNAL_ENTRIES.md` for standard month-end items (Depreciation, Prepaids, Payroll).
- **Close Calendar**: Maintain a `CLOSE_STATUS.md` in the workspace to track tasks and blockers.

---

## 3. Market Data & Investment Research

### Real-Time Financial Intelligence
- **Market Monitoring**: Use `web_search` for the latest market news and `web_fetch` for SEC filings (EDGAR).
- **Thesis Building**:
  1. **Fetch**: `web_fetch` the latest 10-K/10-Q.
  2. **Analyze**: Use `subagent spawn` with a "Senior Equity Analyst" persona to extract risks and catalysts.
  3. **Output**: Generate a `THESIS_[TICKER].md`.

---

## 4. Audit & Compliance

### Audit-Ready Workspace
- **Sample Selection**: Use `exec` with a Python script to select random audit samples from a transaction list.
- **Workpaper Generation**: Create `AUDIT_WORKPAPER_[ID].md` for each control test, including:
  - **Procedure**: What was tested.
  - **Evidence**: Links to files/screenshots in the workspace.
  - **Conclusion**: Pass/Fail with reasoning.

---

## 5. Data Engineering for Finance

### Financial Data Pipelines
- **Automated Extraction**: Use `exec` to run scripts that fetch data from APIs (Stripe, HubSpot, etc.).
- **Transformation**: Use the workspace as a staging area for cleaning and formatting data before loading into `memory/`.

---
*Derived from Perplexity Super-Skills & Claude Code. Optimized for OpenClaw by Ryder.*
