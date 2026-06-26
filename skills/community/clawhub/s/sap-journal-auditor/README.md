# SAP Journal Auditor

<p align="center">
  <strong>Enterprise-grade SAP FI/CO journal audit automation for controllers, auditors, and finance teams.</strong>
</p>

<p align="center">
  <a href="https://github.com/dda-oo/sap-journal-auditor/actions"><img src="https://github.com/dda-oo/sap-journal-auditor/actions/workflows/test.yml/badge.svg" alt="Tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-CC%20BY%204.0-blue" alt="License"></a>
  <a href="https://github.com/dda-oo/sap-journal-auditor"><img src="https://img.shields.io/badge/open%20source-SAP%20Finance-brightgreen" alt="Open Source"></a>
  <a href="https://radarroster.com"><img src="https://img.shields.io/badge/by-RadarRoster-0f172a" alt="RadarRoster"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#audit-checks">Audit Checks</a> •
  <a href="#contributing">Contributing</a> •
  <a href="https://radarroster.com/#contact">Free Strategy Call</a>
</p>

---

**Author:** Daryoosh Dehestani (GitHub: [`dda-oo`](https://github.com/dda-oo))  
**Business:** [RadarRoster](https://radarroster.com) — AI & Data Intelligence Consulting

---

## Overview

SAP Journal Auditor is an open-source audit automation tool that analyzes SAP FI/CO journal entry exports and automatically flags anomalies, duplicates, approval bypass indicators, and period-end irregularities.

Built with deep knowledge of SAP FI/CO, S/4HANA Universal Journal (ACDOCA), and hands-on controlling experience across DACH enterprise environments.

### Why This Tool?

- **Save hours of manual review** — Automated detection of common audit red flags
- **Enterprise-ready** — Handles German/English SAP exports, European/US number formats
- **Zero-dependency option** — Works without npm install for air-gapped environments
- **Professional output** — Structured audit memo ready for management review
- **Open source** — Extend, customize, and contribute improvements

---

## Open Source Spotlight

This project is open source and maintained on GitHub. If you want to improve the audit checks, add new metrics, or share enhancements, you are invited to contribute and help enrich the tool:

- GitHub repository: https://github.com/dda-oo/sap-journal-auditor
- Contribution guide: [`CONTRIBUTING.md`](CONTRIBUTING.md)

---

## Features

| Check | Description | Risk Levels |
|---|---|---|
| 🔁 **Duplicate Postings** | Same amount + account + cost center within ±2 days | HIGH / MEDIUM |
| 💶 **Round Amount Anomalies** | Round figures on accrual accounts at period-end | HIGH / MEDIUM / LOW |
| 📅 **Period-End Outliers** | Accruals posted in last 3 days of fiscal period | HIGH |
| 🏗️ **Cost Center Mismatch** | Account outside typical range for cost center | MEDIUM |
| 🔓 **Approval Bypass** | Missing documentation, backdated postings | HIGH / MEDIUM |
| 🏢 **Intercompany / GR-IR** | IC postings without reference, open GR/IR > 60 days | HIGH / MEDIUM |
| 👤 **User Pattern Analysis** | High-volume users, unusually large single postings | MEDIUM / LOW |

---

## Supported SAP Export Formats

| SAP Transaction | Description | Format |
|---|---|---|
| `FAGLL03` | General Ledger Line Items | CSV / Excel |
| `FB03` | Document Display | CSV |
| `KSB1` | Cost Center Line Items | CSV / Excel |
| `ACDOCA` extract | Universal Journal (S/4HANA) | CSV / Excel |
| Any FI/CO export | Custom column mapping supported | CSV / Excel |

The parser handles both **English and German SAP column headers** and both **European** (`1.234,56`) and **US** (`1,234.56`) number formats.

---

## Quick Start

### Option 1: Standalone (Recommended)

```bash
git clone https://github.com/dda-oo/sap-journal-auditor.git
cd sap-journal-auditor
node tests/test.js   # Verify all 34 tests pass
```

### Option 2: With npm packages (enhanced Excel support)

```bash
git clone https://github.com/dda-oo/sap-journal-auditor.git
cd sap-journal-auditor
npm install
node tests/test.js
```

### Option 3: OpenClaw Integration

```bash
npm install -g openclaw@latest
openclaw onboard
openclaw skill install github:dda-oo/sap-journal-auditor
```

> **Zero-dependency mode:** The tool runs without `npm install` using built-in CSV and XLSX parsers. Installing npm packages enables full Excel format support.

---

## Usage

### CLI / Node.js

```javascript
const { parseJournalFile } = require('./lib/parser');
const { runAllChecks }     = require('./lib/auditor');
const { generateMemo }     = require('./lib/reporter');
const { exportFlaggedCSV } = require('./lib/exporter');
const fs = require('fs');

// Parse your SAP export
const entries = await parseJournalFile('./your_sap_export.csv', { period: '2025-03' });

// Run all audit checks
const results = runAllChecks(entries, { duplicateThreshold: 1000 });

// Generate professional audit memo
const memo = generateMemo(results, entries, { language: 'en' });
fs.writeFileSync('audit_memo.md', memo);

// Export machine-readable findings
exportFlaggedCSV(results.findings, 'flagged_entries.csv');

console.log(`Found ${results.findings.length} issues. Overall risk: ${results.overallRisk}`);
```

### OpenClaw Messaging (Telegram / Slack / WhatsApp)

```
You:   [upload journal_march_2025.csv]
       Audit this SAP journal export for March

Bot:   ⏳ Running audit checks... please wait.
       ✅ Audit Complete
       📊 Entries analyzed: 32
       🚩 Total findings: 15
       🔴 Critical: 2 | 🟠 High: 6
       📋 Overall risk: CRITICAL
       [audit_memo.md attached]
       [flagged_entries.csv attached]
```

### Configuration Options

| Parameter | Type | Default | Description |
|---|---|---|---|
| `language` | `en` / `de` | `en` | Output language for memo |
| `period` | `YYYY-MM` | all | Filter to specific fiscal period |
| `duplicateThreshold` | number | 1000 | Minimum amount to flag duplicates |

---

## Output

### 1. Audit Memo (`audit_memo.md`)

A professional Markdown document containing:

- **Metadata** — audit date, period, entry count, overall risk level
- **Executive Summary** — 3–5 sentence narrative for management
- **Findings by Category** — summary table with counts per check type
- **Full Finding Table** — ID, risk, type, document numbers, amounts, accounts
- **Detailed Descriptions** — per-finding explanation and recommendation
- **Recommendations** — prioritized action list for HIGH/CRITICAL items

### 2. Flagged Entries CSV (`flagged_entries.csv`)

Machine-readable output for downstream processing:

```
FindingID,RiskLevel,CheckType,DocumentNumbers,Amount,Currency,Account,CostCenter,PostingDate,User,Description,Recommendation
```

---

## Sample Output

```markdown
# SAP FI/CO Journal Entry Audit Report

| | |
|---|---|
| **Audit Date** | 2025-03-06 |
| **Entries Analyzed** | 32 |
| **Total Findings** | 15 |
| **Overall Risk** | 🔴 CRITICAL |

## Executive Summary

A total of 32 journal lines were analyzed. The audit identified 15 findings
(2 critical, 6 high, 5 medium, 2 low). High and critical findings require
immediate attention from the controller or internal audit team.

## Findings

| ID | Risk | Check Type | Document(s) | Amount | Account |
|---|---|---|---|---|---|
| FND-0001 | 🟠 HIGH | Duplicate Posting | 1800000001, 1800000002 | 15.000,00 EUR | 400000 |
| FND-0002 | 🔴 CRITICAL | Backdated Posting | 1800000032 | 18.500,00 EUR | 500000 |
...
```

---

## Audit Checks

### Check 1: Duplicate Postings
- Same amount + same account + same cost center within ±2 days → **HIGH** risk
- Same amount + same vendor/customer within same period → **MEDIUM** risk

### Check 2: Round-Amount Postings
- Round amounts (€10,000, €50,000) above threshold → flag for review
- Especially suspicious if posted late in period (day 28-31)

### Check 3: Period-End Timing Outliers
- Postings in last 3 days of fiscal period to accrual accounts (480000–499999)
- Manual reversals on day 1 of following period

### Check 4: Unusual Cost Center Assignments
- Postings to cost centers outside their typical account range
- Statistical profiling detects outliers automatically

### Check 5: Approval Bypass Indicators
- Documents with no reference and no document text above threshold
- Backdated postings (posting date > 7 days before entry date)
- Large manual postings without vendor/customer link

### Check 6: Intercompany / Clearing Anomalies
- Intercompany postings (180000–199999) without matching reference
- Open GR/IR clearing items older than 60 days

---

## Project Structure

```
sap-journal-auditor/
├── skill.json           # OpenClaw skill metadata
├── instructions.md      # Agent system prompt
├── index.js             # OpenClaw entrypoint
├── package.json
├── lib/
│   ├── parser.js        # CSV/Excel parser with SAP column normalization
│   ├── auditor.js       # All 6 audit check implementations
│   ├── reporter.js      # Markdown memo generator (EN/DE)
│   ├── exporter.js      # CSV findings export
│   ├── csv-parse-lite.js # Zero-dependency CSV parser fallback
│   └── xlsx-lite.js      # Zero-dependency XLSX reader fallback
├── sample-data/
│   ├── journal_march_2025.csv   # Realistic test data (32 SAP-style entries)
│   ├── sample_audit_memo.md     # Sample output memo
│   └── sample_flagged.csv       # Sample flagged entries
└── tests/
    └── test.js          # Full test suite (34 assertions)
```

---

## Running Tests

```bash
node tests/test.js
```

Expected output: **34 tests, all passing ✅**

The test suite validates:
- CSV parsing with SAP-format dates and amounts
- All 6 audit check types against realistic sample data
- English and German memo generation
- CSV export format
- Period filtering

---

## Data Freshness & Sources

| Source | Notes |
|---|---|
| SAP FAGLL03 | Standard G/L line item export |
| SAP FB03 | Document display export |
| SAP KSB1 | Cost center line items |
| S/4HANA ACDOCA | Universal Journal extract |

---

## Use Cases

- **Internal audit** — Automated first-pass review of monthly journal entries
- **Controller review** — Quick anomaly detection before period close
- **External audit prep** — Pre-audit cleanup and documentation
- **Compliance monitoring** — Segregation of duties and approval workflow validation
- **Training** — Teaching audit red flags with realistic sample data

---

## Responsible Use

This tool uses exported SAP data only. It does not access live SAP systems and contains no personal or sensitive information beyond what is in the export files. All flagged items require human review before any corrective action.

---

## Attribution

If you use, fork, or build upon this project, please credit:

- **Daryoosh Dehestani** (GitHub: `dda-oo`)
- **RadarRoster** (https://radarroster.com)

Suggested credit line:

> "Based on SAP Journal Auditor by Daryoosh Dehestani (dda-oo) and RadarRoster."

---

## License

This project is licensed under **CC BY 4.0**. See [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md).

---

## Contributing

PRs are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

If you extend the tool, please keep the attribution and add your changes clearly in the README or release notes.

---

## Roadmap Ideas

- [ ] ACDOCA-native column mapping (direct S/4HANA extract)
- [ ] Profit Center dimension checks
- [ ] Intercompany reconciliation across two company codes
- [ ] HTML report output option
- [ ] Integration with SAP Analytics Cloud export format
- [ ] Web UI for drag-and-drop analysis
- [ ] Multi-company code batch processing

---

## Get Help

- **Issues:** https://github.com/dda-oo/sap-journal-auditor/issues
- **Security:** See [`SECURITY.md`](SECURITY.md)
- **Strategy Call:** https://radarroster.com/#contact

---

<p align="center">
  <strong>Built with SAP FI/CO expertise by <a href="https://radarroster.com">RadarRoster</a></strong><br>
  <em>AI & Data Intelligence Consulting — DACH</em>
</p>
