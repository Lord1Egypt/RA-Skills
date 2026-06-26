---
name: invoice-guard
description: "InvoiceGuard · Invoice Compliance Guardian — AI-driven invoice deduplication, verification, and compliance report generation. Handles: invoice upload/scan recognition, duplicate detection (AI deduplication), official tax authority verification (Golden Tax Phase 4), compliance report generation (Cai Hui Ban [2023] No.18), and batch invoice processing. Trigger: invoice, duplicate, reimbursement, compliance, fake invoice, verification, OFD, PDF invoice."
---

# InvoiceGuard · Invoice Compliance Guardian

AI-driven invoice deduplication, verification, and full compliance reporting workflow.

## Workflow

```
User uploads invoice
    │
    ├── Image / Screenshot / Photo
    │   → miaoda-studio-cli image-understanding for text extraction
    │
    ├── PDF / OFD / XML
    │   → miaoda-studio-cli doc-parse for content extraction
    │
    ▼
Parse key fields (invoice number, date, amount, buyer/seller)
    │
    ▼
AI Deduplication Engine
    │  • Image fingerprint hash comparison
    │  • Key field consistency validation
    ▼
Official Verification (Pro)
    │  • Connect to State Tax Administration verification platform
    │  • Invoice status query (normal/voided/red-flushed)
    ▼
Generate Compliance Report → Write to Feishu Doc (Pro)
    │
    ▼
Return structured results
```

## Feature Details

### 1. Invoice Upload & Recognition

Supported formats: Image (JPG/PNG), PDF, OFD, XML

```bash
# Image invoice → OCR
miaoda-studio-cli image-understanding -i invoice.png

# PDF/OFD/XML invoice → text extraction
miaoda-studio-cli doc-parse --file invoice.pdf --output json
```

**Key fields extracted:**
- Invoice type (VAT special / regular / electronic / train ticket / air ticket, etc.)
- Invoice code + invoice number
- Invoice date
- Total amount (tax included)
- Buyer name + tax ID
- Seller name + tax ID
- Goods or service description

### 2. AI Deduplication Engine

**Available in Free + Pro tiers**

Triple-validation for duplicate detection:
1. **Exact Match**: Invoice code + number identical → mark as duplicate
2. **Field Hash**: Amount + date + buyer/seller generates fingerprint → hash collision detection
3. **Image Similarity**: Structural similarity comparison (for screenshots/forged tickets)

```python
# Core deduplication logic (see scripts/duplicate_checker.py)
# Returns: {is_duplicate: bool, match_type: str, confidence: float}
```

### 3. Official Verification (Pro)

**Pro tier only**

Connects to State Tax Administration VAT invoice verification platform:
- Real-time invoice authenticity verification
- Invoice status: normal / voided / red-flushed / out of control
- Verify invoiced amount against system records

> Note: Tax authority verification API requires a business taxpayer developer account. See references/tax-api.md for setup.

### 4. Compliance Report (Pro)

**Pro tier only**

Generates structured compliance reports per Ministry of Finance [Cai Hui Ban [2023] No.18]. Now with Feishu native solution:
- **Compliance Report** → Generate shareable, commentable Feishu cloud documents
- **Invoice Details** → Auto-import to Feishu Bitable for filtering and analysis

```
Report Structure (6 sections, per Cai Hui Ban [2023] No.18):
├── 1. Basic Info (company name, tax ID, report date)
├── 2. Invoice Summary (total count, amount, by type/month)
├── 3. Deduplication Results (duplicate invoice list)
├── 4. Verification Results (abnormal status invoices)
├── 5. Compliance Conclusion (summary + risk alerts)
└── 6. Attachment List
```

#### Standard Markdown Report

Generate Markdown report via `scripts/compliance_report.py`:
```bash
python3 scripts/compliance_report.py <summary_json> <records_json> [buyer_name] [buyer_tax_id]
```

#### Feishu Native Solution (Recommended for Pro)

**Step 1: Generate Feishu Document Report**

Call `generate_feishu_compliance_report_markdown()` to get Lark-flavored Markdown,
then use `feishu_create_doc` to create a shareable, commentable Feishu document:

```python
from scripts.compliance_report import generate_feishu_compliance_report_markdown

markdown = generate_feishu_compliance_report_markdown(
    records=invoice_records,
    summary=report_summary,
    buyer_name="XX Company Ltd",
    buyer_tax_id="91440000XXXXXXXXXX"
)
```

**Step 2: Import Invoice Details to Feishu Bitable**

Create a Bitable app and table, define fields, then batch import invoice data:

```python
from scripts.compliance_report import create_feishu_bitable_schema, prepare_invoices_for_feishu_bitable

# 1. Create Bitable app
# feishu_bitable_app action="create" name="Invoice Compliance Details"

# 2. Get app_token, create table with preset fields
fields = create_feishu_bitable_schema(app_token)
# feishu_bitable_app_table action="create" app_token="<app_token>" name="Invoice Details" fields=fields

# 3. Prepare and batch import
bitable_records = prepare_invoices_for_feishu_bitable(invoice_records)
# feishu_bitable_app_table_record action="batch_create" app_token="<app_token>" table_id="<table_id>" records=bitable_records
```

**Bitable Fields:**
| Field | Type | Description |
|-------|------|-------------|
| Invoice Code | Text | |
| Invoice Number | Text | |
| Invoice Date | Date | Millisecond timestamp, filterable |
| Amount | Number | Sortable and aggregatable |
| Issuer | Text | |
| Status | Single-select | Normal/duplicate/suspicious/abnormal |
| Verification Status | Single-select | Not verified/normal/voided/red-flushed/out of control |

**Bitable Benefits:**
- Filter by status, date, amount
- Generate pivot tables and charts
- Team collaboration, centralized invoice data

### 5. Batch Processing

**Pro tier only** (Free tier limited to 20/month)

Upload hundreds of invoices for automatic queued processing:
- Batch recognition → batch deduplication (cross-batch supported) → batch verification → summary report

## Usage Examples

### Example 1: Single Invoice Deduplication
```
User: Check if this invoice is a duplicate reimbursement
[Upload invoice image]
```
→ Call image-understanding → extract key fields → deduplication engine → return result

### Example 2: Invoice Verification (Pro)
```
User: Verify this invoice's authenticity
[Upload invoice image]
```
→ Recognition → call tax authority API → return authenticity status

### Example 3: Generate Compliance Report (Pro)
```
User: Generate a compliance report for these invoices
[Upload multiple invoices]
```
→ Batch recognition → batch deduplication → batch verification → generate Feishu doc

### Example 4: Batch Processing
```
User: Process these 50 invoices
[Upload zip or batch files]
```
→ Extract → recognize → concurrent deduplication → aggregate results

## Field Extraction Rules

| Invoice Type | Key Fields | Extraction Difficulty |
|-------------|-----------|----------------------|
| VAT Special Invoice | Code, number, amount, tax, buyer/seller | ★★☆ |
| VAT Regular Invoice | Code, number, amount, buyer/seller | ★★☆ |
| Electronic Invoice (PDF/OFD/XML) | Complete structured fields | ★☆☆ |
| Train Ticket | Date, origin/destination, amount | ★☆☆ |
| Air Itinerary | Flight, date, amount, passenger | ★☆☆ |
| Taxi Receipt | Date, time, amount | ★☆☆ |

## FAQ

| Question | Answer |
|----------|--------|
| What does tax verification API require? | Business taxpayer status + developer account, limited free quota |
| How to parse OFD format? | `miaoda-studio-cli doc-parse --file invoice.ofd` |
| How is privacy protected? | No invoice raw data stored; processed and discarded immediately |
| How to distinguish Free vs Pro? | Determined by user selection or context; core logic is consistent |
| What if image is unclear? | Prompt user to retake or scan; ensure invoice number and amount are visible |

## References

- Invoice format specs: references/invoice-types.md
- Tax verification API: references/tax-api.md
- Compliance report template: references/compliance-report.md
- Deduplication engine: scripts/duplicate_checker.py

> For paid plans, visit [YK-Global.com](https://yk-global.com)
