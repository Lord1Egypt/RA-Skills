# Xero API Examples Reference

## Line Item JSON Format

When creating invoices, line items must be provided as a JSON array:

```json
[
  {
    "description": "Service description",
    "quantity": 1,
    "unitAmount": 100.00,
    "accountCode": "200",
    "taxType": "OUTPUT"
  }
]
```

### Required Fields
- `description`: Text describing the item/service
- `lineAmount`: Total for the line (OR use quantity + unitAmount)

### Optional Fields
- `quantity`: Number of items (default: 1)
- `unitAmount`: Price per unit
- `accountCode`: Xero account code (e.g., "200" for sales)
- `taxType`: Tax treatment (OUTPUT, INPUT, NONE, etc.)
- `itemCode`: Link to an inventory item

## Common Account Codes

These vary by organization, but typical defaults:

| Code | Name | Type |
|------|------|------|
| 200 | Sales | REVENUE |
| 260 | Other Revenue | REVENUE |
| 300 | Purchases | EXPENSE |
| 400 | Advertising | EXPENSE |
| 404 | Bank Fees | EXPENSE |
| 408 | Cleaning | EXPENSE |
| 412 | Consulting | EXPENSE |
| 420 | Entertainment | EXPENSE |
| 429 | General Expenses | EXPENSE |
| 449 | Office Expenses | EXPENSE |
| 461 | Printing & Stationery | EXPENSE |
| 469 | Rent | EXPENSE |
| 473 | Software | EXPENSE |
| 489 | Telephone & Internet | EXPENSE |
| 493 | Travel | EXPENSE |

Always verify codes with: `xero-cli accounts list --type REVENUE` or `--type EXPENSE`

## Invoice Status Flow

```
DRAFT → SUBMITTED → AUTHORISED → PAID
                  ↘ VOIDED
```

- **DRAFT**: Editable, not sent
- **SUBMITTED**: Awaiting approval (optional workflow)
- **AUTHORISED**: Approved and sent/ready to send
- **PAID**: Fully paid
- **VOIDED**: Cancelled (cannot be deleted once authorised)

## Tax Types

| Code | Description |
|------|-------------|
| OUTPUT | Standard rate on sales |
| INPUT | Standard rate on purchases |
| NONE | No tax / exempt |
| ZERORATEDINPUT | Zero-rated purchases |
| ZERORATEDOUTPUT | Zero-rated sales |
| EXEMPTINPUT | Exempt purchases |
| EXEMPTOUTPUT | Exempt sales |

## Multi-line Invoice Example

```bash
xero-cli invoices create \
  --contact "abc123" \
  --items '[
    {"description":"Consulting - Day Rate","quantity":5,"unitAmount":800,"accountCode":"200"},
    {"description":"Travel Expenses","quantity":1,"unitAmount":250,"accountCode":"200"},
    {"description":"Software License","quantity":1,"unitAmount":99,"accountCode":"200"}
  ]' \
  --reference "PROJECT-001" \
  --due-date "2024-03-01"
```

## Contact Types

Contacts can be:
- **Customer only**: `--customer`
- **Supplier only**: `--supplier`
- **Both**: `--customer --supplier`
- **Neither**: (default) - can be used for either later

## Date Formats

All dates should be in ISO format: `YYYY-MM-DD`

Examples:
- `--date "2024-01-15"`
- `--due-date "2024-02-15"`

## Currency

Invoices inherit the organization's base currency by default. Multi-currency requires additional configuration in Xero.
