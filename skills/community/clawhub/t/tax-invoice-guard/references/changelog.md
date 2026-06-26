# InvoiceGuard Changelog

## Upgrade: Compliance Report — Feishu Native Solution (2026-04-19)

**Feature**: Feishu native implementation
- **Compliance Report**: Generate shareable, commentable Feishu cloud documents, compliant with [Cai Hui Ban [2023] No.18] 6-section structure
- **Invoice Details**: Auto-import to Feishu Bitable, supporting filtering, sorting, and chart analysis

**New functions**:
- `generate_feishu_compliance_report_markdown()` - Generate Lark-flavored Markdown for `feishu_create_doc`
- `prepare_invoices_for_feishu_bitable()` - Convert invoice records to Feishu Bitable batch creation format
- `create_feishu_bitable_schema()` - Return field definitions for invoice details table

**Technical upgrades**:
- Use Feishu native callout blocks for risk alerts, clearer visual hierarchy
- Complete Bitable field support: invoice code, number, date, amount, issuer, status, verification status
- Supports filtering, sorting, pivot tables and chart analysis
- Documents shareable and commentable, team collaboration enabled

**Deployment notes**:
- 91Skillhub is independent from 91TokenHub
- Reuses the same payment system as GEO Master
- Deployment server: 124.220.60.10

---

## New: Compliance Report Generator (2026-04-19)

**File**: `scripts/compliance_report.py`

New compliance report generation script, compliant with [Cai Hui Ban [2023] No.18] complete 6-section structure:
1. Basic Info (company name, tax ID, report date)
2. Invoice Summary (by type + by month)
3. Deduplication Results (duplicate/suspicious invoice list)
4. Verification Results (abnormal status invoice list)
5. Compliance Conclusion (summary + risk alerts)
6. Attachment List

**Attachment**: Invoice details table — complete list of all invoices with status flags

**Output**: Markdown format, directly writable to Feishu documents.

---

**Review Date**: 2026-04-19
**Reviewer**: 91Skillhub Team
**Status**: All Critical + Major issues resolved

---

## Critical Issue Fixes

### C-1 · Tamper Detection Dead Code

**File**: `scripts/duplicate_checker.py`

**Problem**: Lines 68-74 returned early on exact match, making lines 83-99 under identical conditions unreachable. Invoices with same number but tampered amount were incorrectly flagged as `exact` (confidence 1.0) instead of `tampered` (confidence 0.99).

**Root cause**:
```python
# Original (BUG)
for existing in existing_records:
    if new_code == exist_code:          # Exact match returns early
        return DuplicateResult(match_type="exact", ...)  # Never reaches below

    # This identical condition is unreachable!
    if new_code == exist_code:          # Dead code
        if abs(new_amount - exist_amount) > 0.01:
            return DuplicateResult(match_type="tampered", ...)
```

**Fix**: Move tamper check before exact match return:
```python
if new_code == exist_code:
    if abs(new_amount_dec - exist_amount_dec) > Decimal("0.01"):
        return DuplicateResult(match_type="tampered", confidence=0.99, ...)
    return DuplicateResult(match_type="exact", confidence=1.0, ...)
```

**Verification**: Same invoice number + different amount → `match_type=tampered`, confidence 0.99

---

### C-2 · Regex Character Class Syntax Error

**File**: `duplicate_checker.py`, `batch_processor.py`

**Problem**: `[纳税人识别号|税号]` is a character class (matches single character), not logical OR.

**Fix**: Use correct non-capturing alternation:
```python
# Wrong
r'[纳税人识别号|税号][：:\s]*([A-Z0-9]{15,20})'

# Correct
r'(?:纳税人识别号|税号)[：:\s]*([A-Z0-9]{15,20})'
```

---

### C-3 · Zero Pro/Free Tier Isolation

**File**: `duplicate_checker.py`, `batch_processor.py`

**Problem**: No tier verification logic in code; any user had unlimited access to batch processing and tax authority API.

**Fix**: Introduce `TierConfig` class for complete permission isolation:

| Feature | Free | Pro |
|---------|:----:|:---:|
| Single deduplication | 20/month | Unlimited |
| Batch processing | Blocked | Unlimited |
| Tax authority API | Blocked | Allowed |
| Cross-batch deduplication | Blocked | Allowed |

---

### C-4 · Thousand-separator Amount Extraction Failure

**File**: `duplicate_checker.py`, `batch_processor.py`

**Problem**: `￥1,234.56` only extracted as `1`.

**Fix**: New `_amount_from_text()` function:
```python
r'[价税合计|价税][：:\s]*[￥¥]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)'
```

---

## Major Issue Fixes

### M-1 · SHA256 Truncation Causing Hash Collision Risk
`fields_hash()` changed from `[:16]` (16 chars) to full 64-char SHA256.

### M-2 · Air Itinerary Misidentified as Electronic Invoice
Detection order adjusted: `航空`/`机票`/`行程单` takes priority over `电子发票`.

### M-3 · Cross-batch Duplicate Detection Impossible
`batch_check_duplicates()` added `historical_records` parameter for cross-batch comparison.

### M-5 · Float Comparison Replaced with `Decimal`
All amount comparisons use `Decimal` to avoid floating-point precision issues.

### M-6 · XML/OFD Parse Support
New `parse_xml_text()` and `parse_ofd_text()` functions for XML/OFD file content parsing.

---

## Modified Files

| File | Changes |
|------|---------|
| `scripts/duplicate_checker.py` | C-1, C-2, C-3, C-4, M-1, M-2, M-5 |
| `scripts/batch_processor.py` | C-2, C-3, C-4, M-1, M-2, M-3, M-5, M-6 |
| `SKILL.md` | Updated Pro tier permission descriptions |
| `references/changelog.md` | This file |
