# Chinese Invoice Types and Field Specifications

## Invoice Classification System

### 1. VAT Invoices

#### VAT Special Invoice (Deductible)
- **Format**: Paper / Electronic
- **Key fields**: Invoice code (10-digit) + invoice number (8-digit), amount, tax, total (tax included), buyer, seller, taxpayer identification number
- **Usage**: Input tax deductible

#### VAT Regular Invoice (Non-deductible)
- **Format**: Paper / Electronic / Roll
- **Key fields**: Same as special invoice, but non-deductible
- **Special**: Buyer name and taxpayer ID are required fields

#### Electronic Invoice (Digital VAT)
- **Format**: PDF / OFD / XML
- **Characteristics**: Issued via national unified electronic invoice platform, no paper
- **Verification**: Via tax digital account

### 2. Air / Train / Transit Tickets
- **Fields**: Passenger name, flight/train number, date, origin, destination, amount
- **Characteristics**: Not VAT invoices, non-deductible

### 3. Taxi Receipts
- **Fields**: Date, time, pick-up/drop-off locations, amount, invoice code + number

### 4. Generic Printed Invoices
- **Fields**: Issuer, date, item details, amount

---

## Invoice Number Coding Rules

| Invoice Type | Code Digits | Number Digits | Example |
|-------------|------------|---------------|---------|
| VAT Special Invoice | 10-digit | 8-digit | 144031900110 / 12345678 |
| VAT Regular Invoice | 12-digit | 8-digit | 144031900110 / 12345678 |
| Electronic Invoice | 20-digit | — | — |
| Taxi Receipt | 10-digit | — | — |

---

## Key Field Extraction Regex (Post-OCR Text)

```python
# Invoice code extraction
invoice_code_pattern = r'[发票代码|代码][：:\s]*(\d{10,12})'
invoice_no_pattern = r'[发票号码|号码][：:\s]*(\d{8})'

# Amount extraction
amount_pattern = r'[价税合计|合计|金额][：:\s]*[￥¥]?\s*(\d+\.?\d{0,2})'

# Date extraction
date_pattern = r'(\d{4}[年\-/]\d{1,2}[月\-/]\d{1,2}[日]?)'

# Taxpayer ID (buyer/seller)
tax_id_pattern = r'[纳税人识别号|税号][：:\s]*([A-Z0-9]{15,20})'
```
