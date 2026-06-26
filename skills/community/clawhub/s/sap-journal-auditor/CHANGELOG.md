# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-03-06

### Added
- Initial release of SAP Journal Auditor
- 6 audit check types: duplicates, round amounts, cost center mismatch, approval bypass, intercompany, user patterns
- CSV and Excel parser with SAP column normalization
- English and German memo output
- Zero-dependency mode with built-in CSV/XLSX parsers
- OpenClaw skill integration
- 34 automated tests
- Professional documentation (README, CONTRIBUTING, SECURITY, etc.)

### Features
- Handles German and English SAP column headers
- Supports European (1.234,56) and US (1,234.56) number formats
- Period filtering for fiscal period analysis
- Configurable duplicate detection threshold
- Machine-readable CSV export for findings

### Supported SAP Transactions
- FAGLL03 (General Ledger Line Items)
- FB03 (Document Display)
- KSB1 (Cost Center Line Items)
- ACDOCA extract (S/4HANA Universal Journal)

---

## Unreleased

### Planned
- ACDOCA-native column mapping
- Profit Center dimension checks
- Intercompany reconciliation across company codes
- HTML report output
- SAP Analytics Cloud export format support
