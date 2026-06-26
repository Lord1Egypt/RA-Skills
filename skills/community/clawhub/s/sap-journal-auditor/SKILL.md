# SAP Journal Auditor

Audit SAP FI/CO journal entry exports for anomalies, duplicate postings, unusual cost center assignments, period-end outliers, and approval bypass patterns.

## Triggers

- audit journal
- check journal entries  
- SAP audit
- review postings
- flag anomalies
- prüfe buchungen
- journal analyse

## Description

This skill analyzes SAP FI/CO journal exports (CSV or Excel) and identifies potential audit issues:

- **Duplicate Postings** - Same amount, account, reference posted multiple times
- **Round Amount Anomalies** - Large round numbers that may indicate estimates or accruals
- **Cost Center Mismatches** - Expenses booked to unusual cost centers
- **Approval Bypass** - Missing references, manual journal entries
- **Intercompany Issues** - IC postings without proper clearing references
- **User Patterns** - Unusual posting activity by specific users

Supports SAP exports from:
- FB03 (Document Display)
- FAGLL03 (G/L Account Line Items)
- KSB1 (Cost Center Line Items)
- ACDOCA (S/4HANA Universal Journal)

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | file | Yes | CSV or Excel export from SAP FI/CO |
| `language` | string | No | Output language: `en` (English) or `de` (German). Default: `en` |
| `period` | string | No | Fiscal period to focus on, e.g., `2025-03` or `Q1-2025` |

## Outputs

- Structured audit memo with findings categorized by severity (CRITICAL, HIGH, MEDIUM, LOW)
- CSV export of flagged entries for further review
- Summary statistics and risk assessment

## Example

```
Audit the attached journal_march_2025.csv for anomalies
```

```
Prüfe die angehängte Buchungsdatei auf Auffälligkeiten
```

## Author

**Daryoosh Dehestani**  
RadarRoster | [https://radarroster.com](https://radarroster.com)

## License

CC-BY-4.0
