# InvoiceGuard · Invoice Compliance Guardian

> AI-driven invoice deduplication, verification, and compliance report generation

---

## Overview

InvoiceGuard automates the full invoice compliance workflow: deduplication, authenticity verification, and structured compliance reporting. Ideal for enterprise finance reimbursement checks, duplicate invoice detection, official tax authority verification (Golden Tax Phase 4), and compliance reporting per Ministry of Finance [Cai Hui Ban [2023] No.18].

**Trigger Words**: invoice, duplicate, reimbursement, compliance, fake invoice, verification, OFD, PDF invoice

---

## Feature Tiers

| Feature | Free | Pro |
|---------|:----:|:---:|
| AI invoice deduplication | 20/month | Unlimited |
| Batch processing (>20) | ❌ | ✅ |
| Cross-batch duplicate detection | ❌ | ✅ |
| Official verification (tax authority) | ❌ | ✅ |
| Compliance report | Markdown only | Markdown + Feishu Doc |
| Invoice details to Feishu Bitable | ❌ | ✅ |

---

## Supported Invoice Types

| Type | Format | Notes |
|------|--------|-------|
| VAT Special Invoice | Paper/Electronic | Input tax deductible |
| VAT Regular Invoice | Paper/Electronic/Roll | Non-deductible |
| Electronic Invoice | PDF / OFD / XML | Issued via national platform |
| Air Itinerary | Paper | Flight info |
| Train Ticket | Paper | Route, date, amount |
| Taxi Receipt | Paper | Time, amount |

---

## Workflow

```
User uploads invoice
    │
    ├── Image (JPG/PNG/Screenshot)
    │   → miaoda-studio-cli image-understanding for text extraction
    │
    ├── PDF / OFD / XML
    │   → miaoda-studio-cli doc-parse for content extraction
    │
    ▼
Parse key fields (invoice number, date, amount, buyer/seller)
    │
    ▼
AI Deduplication Engine (Triple Validation)
    │  • Exact match: code+number identical → mark duplicate
    │  • Field hash: amount+date+buyer/seller → fingerprint collision
    │  • Tamper detection: same number, different amount → mark tampered
    ▼
Official Verification (Pro only)
    │  • Connect to State Tax Administration VAT verification platform
    │  • Status: normal / voided / red-flushed / out of control
    ▼
Generate Compliance Report (Pro)
    │  • Standard Markdown report
    │  • Feishu cloud document (shareable, commentable)
    │  • Invoice details to Feishu Bitable
    ▼
Return structured results
```

---

## Triple Deduplication Logic

1. **Exact Match**: Invoice code + number identical → `exact` (confidence 1.0)
2. **Tamper Detection**: Same code+number, different amount → `tampered` (confidence 0.99)
3. **Field Hash**: Amount + date + buyer/seller → fingerprint collision → `hash_collision`

> Note: Same invoice number with different amounts is flagged as "tampered," not misclassified as normal.

---

## File Structure

```
invoice-guard/
├── SKILL.md                        # Skill definition (trigger words, tool invocation)
├── README.md                       # This file
├── references/
│   ├── changelog.md                # Changelog (issue fix history)
│   ├── invoice-types.md            # Chinese invoice types and field specs
│   ├── tax-api.md                  # Tax authority verification API setup guide
│   └── compliance-report.md        # Compliance report template (Cai Hui Ban [2023] No.18)
└── scripts/
    ├── duplicate_checker.py        # Invoice deduplication engine (triple validation + tier isolation)
    ├── batch_processor.py          # Batch invoice processor
    └── compliance_report.py        # Compliance report generator (Markdown + Feishu native)
```

---

## Core Scripts

### 1. `duplicate_checker.py` — Invoice Deduplication Engine

**Functionality**: Triple-validation deduplication with Pro/Free tier isolation.

**Main classes**:
- `TierConfig`: User tier configuration (is_pro / monthly_count)
- `InvoiceRecord`: Structured invoice data
- `DuplicateResult`: Deduplication result (is_duplicate / match_type / confidence)

**Key functions**:
```python
check_duplicate(new_record: InvoiceRecord, existing_records: List[InvoiceRecord], tier: TierConfig) -> DuplicateResult
batch_check_duplicates(records: List[InvoiceRecord], tier: TierConfig, historical_records: List[InvoiceRecord] = None) -> List[DuplicateResult]
```

**Tier controls**:
- Free: 20 invoices/month, no batch processing
- Pro: Unlimited, cross-batch deduplication supported

---

### 2. `batch_processor.py` — Batch Invoice Processor

**Functionality**: Batch recognition → batch deduplication → batch verification → summary report.

**Main classes**:
- `BatchProcessor`: Batch processor with concurrent deduplication
- `TaxVerificationResult`: Verification result (status / description)

**Key functions**:
```python
BatchProcessor.process_batch(invoices: List[str], tier: TierConfig) -> BatchResult
BatchProcessor.verify_invoice(invoice_record: InvoiceRecord) -> TaxVerificationResult
```

---

### 3. `compliance_report.py` — Compliance Report Generator

**Functionality**: Generates 6-section compliance reports per [Cai Hui Ban [2023] No.18].

**Report structure**:
1. Basic Info (company name, tax ID, report date)
2. Invoice Summary (total + amount, by type + by month)
3. Deduplication Results (duplicate/suspicious invoice list)
4. Verification Results (abnormal status invoice list)
5. Compliance Conclusion (summary + risk alerts)
6. Attachment List

**Output methods**:

| Method | Function | Notes |
|--------|----------|-------|
| Standard Markdown | `generate_compliance_report_markdown()` | Write to local file |
| Feishu Doc (Recommended) | `generate_feishu_compliance_report_markdown()` | Lark-flavored Markdown for `feishu_create_doc` |
| Feishu Bitable | `prepare_invoices_for_feishu_bitable()` | Batch import invoice details to Feishu Bitable |

**Usage**:
```python
from scripts.compliance_report import (
    generate_feishu_compliance_report_markdown,
    create_feishu_bitable_schema,
    prepare_invoices_for_feishu_bitable,
)

# Generate Feishu doc Markdown
markdown = generate_feishu_compliance_report_markdown(
    records=invoice_records,
    summary=report_summary,
    buyer_name="XX Company Ltd",
    buyer_tax_id="91440000XXXXXXXXXX"
)

# Get Bitable field definitions
fields = create_feishu_bitable_schema(app_token)

# Prepare batch import data
bitable_records = prepare_invoices_for_feishu_bitable(invoice_records)
```

---

## Feishu Native Solution (Pro)

### Generate Compliance Report to Feishu Doc

1. Call `generate_feishu_compliance_report_markdown()` to get Lark-flavored Markdown
2. Use `feishu_create_doc` to create Feishu document
3. Document is directly shareable and commentable, compliant with [Cai Hui Ban [2023] No.18]

### Import Invoice Details to Feishu Bitable

1. Call `feishu_bitable_app` to create Bitable app
2. Call `feishu_bitable_app_table` to create table (using fields from `create_feishu_bitable_schema()`)
3. Call `feishu_bitable_app_table_record` batch_create to import invoice details

**Bitable Fields**:

| Field | Type | Description |
|-------|------|-------------|
| Invoice Code | Text | |
| Invoice Number | Text | |
| Invoice Date | Date | Millisecond timestamp, filterable |
| Amount | Number | Sortable and aggregatable |
| Issuer | Text | |
| Status | Single-select | Normal/duplicate/suspicious/abnormal |
| Verification Status | Single-select | Not verified/normal/voided/red-flushed/out of control |

---

## Invoice Status Reference

| Status | Meaning | Reimbursement |
|--------|---------|---------------|
| Normal (00) | Invoice valid | ✅ Acceptable |
| Voided (01) | Self-voided by company | ❌ Not acceptable |
| Red-flushed (02) | Red invoice issued for offset | ❌ Not acceptable |
| Out of control (03) | Flagged by tax authority | ❌ Not acceptable |
| Abnormal (04) | Data inconsistency | ⚠️ Requires verification |

---

## Field Extraction Rules

| Invoice Type | Key Fields | Method |
|-------------|-----------|---------|
| VAT Special Invoice | Code (10-digit) + number (8-digit), amount, tax, buyer/seller, tax ID | Regex |
| VAT Regular Invoice | Code + number + amount + buyer/seller | Regex |
| Electronic PDF/OFD/XML | Complete structured fields | `doc-parse` direct parse |
| Air Itinerary | Flight, date, amount, passenger | Regex |
| Train Ticket | Date, origin/destination, amount | Regex |
| Taxi Receipt | Date, time, amount | Regex |

---

## Privacy & Security

- **No invoice raw data storage**: Processed and discarded immediately
- **Sandbox execution**: Isolated from external systems
- **Pro/Free tier isolation**: Free tier cannot call tax authority API or use batch processing
- **Token-based billing**: Each verification consumes account tokens

---

## FAQ

| Question | Answer |
|----------|--------|
| What does tax verification API require? | Business taxpayer status + developer account (100 calls/day/IP free quota) |
| How to parse OFD format? | `miaoda-studio-cli doc-parse --file invoice.ofd` |
| How to distinguish Free vs Pro? | Determined by user selection or context; permission checks embedded in code |
| What if image is unclear? | Prompt user to retake or scan; ensure invoice number and amount are visible |
| How are tampered invoices detected? | Same invoice code+number but different amount → flagged as `tampered` (confidence 0.99) |

---

## Changelog

See references/changelog.md

---

**Version**: 2.0 (Feishu Native Solution)
**Review Date**: 2026-04-19
**Reviewer**: 91Skillhub Team

> For paid plans, visit [YK-Global.com](https://yk-global.com)
