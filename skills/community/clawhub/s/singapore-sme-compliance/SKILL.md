---
name: singapore-sme-compliance
description: >
  Help Singapore SMEs automate compliance tasks: GST calculation, PEPPOL invoice 
  validation, tax report generation, and IRAS filing deadlines. Use when: calculating 
  GST for invoices, checking GST registration requirements, preparing GST F5 returns, 
  validating PEPPOL invoices, tracking compliance deadlines.
homepage: https://github.com/openclaw/openclaw
metadata:
  openclaw:
    requires:
      bins: ["bc"]
    files: ["scripts/*"]
official: false
---

# Singapore SME Compliance Assistant

Help Singapore SMEs automate compliance tasks: GST calculation, PEPPOL invoice validation, tax report generation, and regulatory checklist.

## Quick Start

**Check GST registration requirements:**
```bash
# Check if business needs GST registration (threshold: S$1M annual turnover)
curl -s "https://www.iras.gov.sg/api/gst-threshold-check" -d '{"turnover": 1000000}'
```

**GST calculation:**
```bash
# Calculate GST (9% as of 2024)
curl -s "https://api.gstcalculator.sg/calculate" -d '{"amount": 1000, "rate": 0.09}'
# Returns: {amount: 1000, gst: 90, total: 1090}
```

## Key Features

### 1. GST Registration Checker

Singapore businesses must register for GST if:
- Annual taxable turnover exceeds S$1 million (mandatory)
- You expect turnover to exceed S$1 million in next 12 months (voluntary)

**Usage:**
```bash
# Check registration requirement
echo "Check GST registration for turnover: S$1,200,000"
```

### 2. GST Calculator

Current GST rates:
- 2023: 8%
- 2024 onwards: 9%

**Calculate GST:**
```bash
# For invoice amount
Invoice: S$5,000
GST (9%): S$450
Total: S$5,450
```

### 3. PEPPOL Invoice Validator

Singapore uses PEPPOL (InvoiceNow) for e-invoicing.

**Validate PEPPOL invoice:**
1. Check UEN format (9 or 10 characters)
2. Verify invoice structure (UBL 2.1 format)
3. Validate against IRAS requirements

**Checklist:**
- [ ] Supplier UEN present
- [ ] Buyer UEN present
- [ ] Invoice number unique
- [ ] Tax amount calculated correctly
- [ ] Currency code (SGD)
- [ ] Payment terms specified

### 4. Monthly GST Return (GST F5) Helper

**Required data for GST F5:**
- Box 1: Total value of standard-rated supplies
- Box 2: Total value of zero-rated supplies
- Box 3: Total value of supplies (Box 1 + Box 2)
- Box 4: Output tax due
- Box 5: Input tax claimed
- Box 6: Net GST payable/refundable

**Monthly checklist:**
```
□ Collect all tax invoices (purchases)
□ Collect all tax invoices (sales)
□ Calculate output tax (sales)
□ Calculate input tax (purchases)
□ Reconcile with accounting records
□ File GST F5 by deadline (1 month after period end)
```

### 5. Compliance Calendar

**Key deadlines:**
| Deadline | Requirement |
|----------|-------------|
| Monthly (if on monthly filing) | GST F5 return |
| Quarterly (default) | GST F5 return (within 1 month after quarter end) |
| Annually | Estimated Chargeable Income (ECI) - within 3 months after FYE |
| Annually | Corporate Tax Return (Form C-S/C) - by Nov 30 |

**Reminders:**
- Set up auto-reminders 7 days before deadline
- Prepare documents 3 days before filing
- Keep records for 5 years (IRAS requirement)

## Common Compliance Scenarios

### Scenario 1: New Business Registration

**Steps:**
1. Register business with ACRA
2. Get UEN (Unique Entity Number)
3. Check if GST registration required
4. Set up accounting system
5. Register for CorpPass (for digital services)

### Scenario 2: Importing Goods

**Requirements:**
- Customs import permit
- Pay import GST (7% or 9%)
- Claim input tax (if GST registered)
- Keep import documentation

### Scenario 3: Exporting Goods

**Requirements:**
- Zero-rate exports (0% GST)
- Keep export documentation
- Declare in GST return (Box 2)

## IRAS Resources

- [GST Registration](https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/gst-registration)
- [GST F5 Filing](https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/filing-and-payment)
- [PEPPOL/InvoiceNow](https://www.imda.gov.sg/infocomm-tech-for-business/boost-your-business/productivity-and-technology/invoicenow)
- [CorpPass](https://www.corppass.gov.sg/)

## Penalty Information

**Late GST Filing:**
- First offence: S$200 penalty
- Repeat offence: S$500-S$5,000
- Continued failure: Prosecution possible

**Incorrect Information:**
- Up to 200% of tax undercharged
- Criminal prosecution for fraud

## Automation Workflows

### Monthly GST Preparation (Automated)

**Day 1 of new month:**
1. Fetch all sales invoices from previous month
2. Calculate total output tax
3. Fetch all purchase invoices
4. Calculate total input tax
5. Generate GST F5 draft
6. Send reminder to accountant

**Commands:**
```bash
# Generate monthly GST summary
echo "Generate GST report for $(date -d 'last month' '+%Y-%m')"

# Calculate totals
Output Tax: Sum of GST on all sales invoices
Input Tax: Sum of GST on all purchase invoices
Net GST: Output - Input
```

### Quarterly Compliance Check

**End of each quarter:**
1. Review all transactions
2. Verify GST calculations
3. Check PEPPOL compliance
4. Update compliance calendar
5. Prepare for GST F5 filing

## Integration Examples

### With Accounting Software

**Xero/QuickBooks integration:**
```bash
# Export sales data
curl -s "https://api.xero.com/api/Invoices?status=PAID" \
  -H "Authorization: Bearer TOKEN"

# Export purchase data
curl -s "https://api.xero.com/api/Bills?status=PAID" \
  -H "Authorization: Bearer TOKEN"
```

### With IRAS MyTax Portal

**File GST F5 via API:**
```bash
# Submit GST return (requires CorpPass authentication)
curl -s "https://apiservices.iras.gov.sg/gst/f5" \
  -X POST \
  -H "Authorization: Bearer CORPPASS_TOKEN" \
  -d '{"period": "202403", "box1": 100000, "box4": 9000, ...}'
```

## Error Handling

### Common Errors

**"GST registration required"**
- Turnover exceeded S$1M
- Action: Register within 30 days

**"PEPPOL invoice rejected"**
- Invalid UEN format
- Missing required fields
- Action: Validate against InvoiceNow schema

**"Late filing penalty"**
- File immediately
- Pay penalty
- Set up auto-reminders

## Best Practices

1. **Keep digital records** - IRAS accepts digital records
2. **Reconcile monthly** - Don't wait until quarter end
3. **Use accounting software** - Xero, QuickBooks, SQL Accounting
4. **Set up auto-reminders** - Never miss a deadline
5. **Review input tax claims** - Ensure all claims are valid
6. **Keep export documentation** - For zero-rated supplies
7. **Train staff** - On GST requirements and PEPPOL

## Support Resources

- **IRAS Helpline**: +65 1800 356 8300
- **InvoiceNow (PEPPOL)**: +65 6248 0909
- **ACRA**: +65 6248 6000
- **Enterprise Singapore**: +65 6898 1800

## Updates

- 2026-03-27: Initial release
- GST rate: 9% (2024 onwards)
- PEPPOL mandatory for government suppliers
- B2B PEPPOL expansion expected 2027-2028
