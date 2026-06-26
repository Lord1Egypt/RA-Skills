# Bridge Input Schema

This document defines the canonical JSON schema that Instance B receives from the bridge service (`/v1/post-voucher`). All extraction happens on Instance A (`tally-extractor-skill`); this skill only processes validated JSON.

## Schema Version

Current: `1.0`

## Full JSON Schema

```json
{
  "schema_version": "1.0",
  "request_id": "uuid-v4",
  "idempotency_key": "abc-purchase-ril2026-00123-20260115",
  "company": "ABC Company",
  "voucher": {
    "type": "Purchase|Sales|Receipt|Payment|Journal|Contra|CreditNote|DebitNote",
    "date": "YYYY-MM-DD",
    "number": "186",
    "is_invoice_mode": true,
    "voucher_class": "Sales @ 18 %",
    "narration": "Against Invoice 186",
    "party": {
      "name": "XYZ Party",
      "gstin": "27AABCU9603R1ZM",
      "place_of_supply": "Maharashtra",
      "registration_type": "Regular"
    },
    "company_gstin": "27AABCU9603R1ZN",
    "items": [
      {
        "description": "PQR Item 2523",
        "hsn": "25322210",
        "qty": 140,
        "unit": "Bag",
        "rate": 279.66,
        "tax_rate": 18,
        "amount": 39152.40
      }
    ],
    "taxes": {
      "cgst": 0,
      "sgst": 0,
      "igst": 7047.43,
      "round_off": 0
    },
    "total": 46199.83,
    "ledgers": {
      "party": "XYZ Party",
      "purchase_or_sales": "Purchase @ 18 %",
      "cgst": "Input Cgst @ 9 %",
      "sgst": "Input Sgst @ 9 %",
      "igst": "Input IGST @ 18 %",
      "round_off": "Round Off",
      "bank_or_cash": "HDFC Bank"
    },
    "bill_allocations": [
      {
        "name": "186",
        "type": "New Ref",
        "amount": 46199.83
      }
    ]
  },
  "source": {
    "kind": "pdf|image",
    "filename": "invoice_186.pdf",
    "extracted_at": "2026-05-18T10:30:00Z"
  },
  "confidence": {
    "overall": 0.93,
    "fields": {
      "party.gstin": 1.0,
      "items[0].hsn": 0.7
    }
  }
}
```

## Field Definitions

### Root Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | Yes | Schema version (currently `1.0`) |
| `request_id` | string | Yes | UUID v4 for request tracking |
| `idempotency_key` | string | Yes | Maps to Tally `GUID` — must follow pattern: `{companyShort}-{voucherType}-{voucherNumber}-{date}` |
| `company` | string | Yes | Exact TallyPrime company name (case-sensitive) |
| `voucher` | object | Yes | Voucher details |
| `source` | object | No | Extraction source metadata |
| `confidence` | object | No | Extraction confidence scores |

### Voucher Object

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | enum | Yes | One of: `Purchase`, `Sales`, `Receipt`, `Payment`, `Journal`, `Contra`, `CreditNote`, `DebitNote` |
| `date` | string | Yes | Format: `YYYY-MM-DD` (converted to `YYYYMMDD` for Tally) |
| `number` | string | Yes | Invoice/voucher number |
| `is_invoice_mode` | boolean | No | If `true`, use `OBJVIEW="Invoice Voucher View"` and `LEDGERENTRIES.LIST` |
| `voucher_class` | string | Conditional | Required if company uses voucher classes for GST |
| `narration` | string | No | Voucher narration text |
| `party` | object | Yes | Party details |
| `company_gstin` | string | Conditional | Required for GST vouchers |
| `items` | array | Conditional | Required for Purchase/Sales with line items |
| `taxes` | object | Conditional | Required for GST vouchers |
| `total` | number | Yes | Total voucher amount (must balance) |
| `ledgers` | object | No | Pre-mapped ledger names (if not provided, Instance B maps) |
| `bill_allocations` | array | No | Bill-wise allocations for party ledger |

### Party Object

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Party name (exact match or create new) |
| `gstin` | string | Conditional | 15-char GSTIN (required for GST vouchers) |
| `place_of_supply` | string | Conditional | State name (required for GST vouchers) |
| `registration_type` | enum | Conditional | `Regular`, `Composition`, `Unregistered`, `Consumer` |

### Item Object

| Field | Type | Required | Description |
|---|---|---|---|
| `description` | string | Yes | Item description |
| `hsn` | string | No | HSN/SAC code (8 digits) |
| `qty` | number | Yes | Quantity |
| `unit` | string | No | Unit of measure (e.g., `Bag`, `Nos`, `Kg`) |
| `rate` | number | Yes | Rate per unit |
| `tax_rate` | number | Yes | Tax percentage (e.g., `18` for 18%) |
| `amount` | number | Yes | Line item amount (qty × rate) |

### Taxes Object

| Field | Type | Required | Description |
|---|---|---|---|
| `cgst` | number | No | CGST amount (intra-state) |
| `sgst` | number | No | SGST amount (intra-state) |
| `igst` | number | No | IGST amount (inter-state) |
| `round_off` | number | No | Rounding amount |

### Ledgers Object (optional pre-mapping)

| Field | Type | Description |
|---|---|---|
| `party` | string | Party ledger name |
| `purchase_or_sales` | string | Purchase/Sales account ledger |
| `cgst` | string | CGST duty ledger |
| `sgst` | string | SGST duty ledger |
| `igst` | string | IGST duty ledger |
| `round_off` | string | Rounding ledger |
| `bank_or_cash` | string | Bank/Cash ledger (for Payment/Receipt) |

### Bill Allocation Object

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Bill reference name (usually invoice number) |
| `type` | enum | Yes | `New Ref`, `Agst Ref`, `Advance` |
| `amount` | number | Yes | Allocation amount |

## Required Fields by Voucher Type

### Purchase

| Field | Required |
|---|---|
| `company` | Yes |
| `voucher.type` | Yes (`Purchase`) |
| `voucher.date` | Yes |
| `voucher.number` | Yes |
| `voucher.party.name` | Yes |
| `voucher.party.gstin` | Yes (for GST) |
| `voucher.party.place_of_supply` | Yes (for GST) |
| `voucher.company_gstin` | Yes (for GST) |
| `voucher.items[]` | Yes (at least one) |
| `voucher.taxes` | Yes (for GST) |
| `voucher.total` | Yes |
| `voucher.voucher_class` | If class mode |

### Sales

| Field | Required |
|---|---|
| `company` | Yes |
| `voucher.type` | Yes (`Sales`) |
| `voucher.date` | Yes |
| `voucher.number` | Yes |
| `voucher.party.name` | Yes |
| `voucher.party.gstin` | Yes (for GST) |
| `voucher.party.place_of_supply` | Yes (for GST) |
| `voucher.company_gstin` | Yes (for GST) |
| `voucher.items[]` | Yes (at least one) |
| `voucher.taxes` | Yes (for GST) |
| `voucher.total` | Yes |
| `voucher.voucher_class` | If class mode |

### Payment

| Field | Required |
|---|---|
| `company` | Yes |
| `voucher.type` | Yes (`Payment`) |
| `voucher.date` | Yes |
| `voucher.number` | Yes |
| `voucher.party.name` | Yes |
| `voucher.total` | Yes |
| `voucher.ledgers.bank_or_cash` | Yes |
| `voucher.bill_allocations[]` | Recommended |

### Receipt

| Field | Required |
|---|---|
| `company` | Yes |
| `voucher.type` | Yes (`Receipt`) |
| `voucher.date` | Yes |
| `voucher.number` | Yes |
| `voucher.party.name` | Yes |
| `voucher.total` | Yes |
| `voucher.ledgers.bank_or_cash` | Yes |
| `voucher.bill_allocations[]` | Recommended |

### Journal

| Field | Required |
|---|---|
| `company` | Yes |
| `voucher.type` | Yes (`Journal`) |
| `voucher.date` | Yes |
| `voucher.number` | Yes |
| `voucher.total` | Yes |
| `voucher.narration` | Recommended |

### Contra

| Field | Required |
|---|---|
| `company` | Yes |
| `voucher.type` | Yes (`Contra`) |
| `voucher.date` | Yes |
| `voucher.number` | Yes |
| `voucher.total` | Yes |
| `voucher.ledgers.bank_or_cash` | Yes (both from and to) |

### Credit Note / Debit Note

| Field | Required |
|---|---|
| `company` | Yes |
| `voucher.type` | Yes (`CreditNote` or `DebitNote`) |
| `voucher.date` | Yes |
| `voucher.number` | Yes |
| `voucher.party.name` | Yes |
| `voucher.total` | Yes |
| `voucher.narration` | Recommended |
| `voucher.bill_allocations[]` | Recommended (reference original invoice) |

## JSON to XML Mapping Rules

### Date Conversion

```
JSON: "2026-05-18"  →  XML: <DATE>20260518</DATE>
```

Remove dashes from `YYYY-MM-DD` to get `YYYYMMDD`.

### Voucher Type Mapping

| JSON `voucher.type` | XML `VOUCHERTYPENAME` |
|---|---|
| `Purchase` | `Purchase` |
| `Sales` | `Sales` |
| `Payment` | `Payment` |
| `Receipt` | `Receipt` |
| `Journal` | `Journal` |
| `Contra` | `Contra` |
| `CreditNote` | `Credit Note` |
| `DebitNote` | `Debit Note` |

### Invoice Mode

When `voucher.is_invoice_mode = true`:

```xml
<VOUCHER VCHTYPE="Sales" OBJVIEW="Invoice Voucher View">
  <LEDGERENTRIES.LIST>
    <!-- Use LEDGERENTRIES.LIST, not ALLLEDGERENTRIES.LIST -->
  </LEDGERENTRIES.LIST>
</VOUCHER>
```

When `voucher.is_invoice_mode = false` or missing:

```xml
<VOUCHER VCHTYPE="Sales">
  <ISINVOICE>No</ISINVOICE>
  <ALLLEDGERENTRIES.LIST>
    <!-- Use ALLLEDGERENTRIES.LIST -->
  </ALLLEDGERENTRIES.LIST>
</VOUCHER>
```

### Voucher Class

When `voucher.voucher_class` is provided:

```xml
<VOUCHER>
  <CLASSNAME>Sales @ 18 %</CLASSNAME>
  <CMPGSTIN>27AABCU9603R1ZN</CMPGSTIN>
  <PARTYGSTIN>27AABCU9603R1ZM</PARTYGSTIN>
  <GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
  <PLACEOFSUPPLY>Maharashtra</PLACEOFSUPPLY>
</VOUCHER>
```

### GUID / Idempotency Key

```
JSON: "idempotency_key": "abc-purchase-ril2026-00123-20260115"
  →
XML: <GUID>abc-purchase-ril2026-00123-20260115</GUID>
```

The `idempotency_key` becomes the Tally `GUID` directly.

### Bill Allocations

```json
"bill_allocations": [
  { "name": "186", "type": "New Ref", "amount": 46199.83 }
]
```

Becomes:

```xml
<BILLALLOCATIONS.LIST>
  <NAME>186</NAME>
  <BILLTYPE>New Ref</BILLTYPE>
  <AMOUNT>-46199.83</AMOUNT>
</BILLALLOCATIONS.LIST>
```

**Note:** Amount sign depends on debit/credit context.

### Amount Sign Convention

| Voucher Type | Party Entry | Purchase/Sales Entry | Tax Entry |
|---|---|---|---|
| Purchase | Positive (Cr) | Negative (Dr) | Negative (Dr) |
| Sales | Negative (Dr) | Positive (Cr) | Positive (Cr) |
| Payment | Positive (Cr from bank) | N/A | N/A |
| Receipt | Negative (Dr to bank) | N/A | N/A |

## Validation Rules

Before posting, Instance B must validate:

1. **Schema version** matches supported version
2. **idempotency_key** follows GUID pattern
3. **company** is non-empty
4. **voucher.type** is valid enum
5. **voucher.date** is valid `YYYY-MM-DD`
6. **voucher.total** equals sum of items + taxes (within ±1 for rounding)
7. **GSTIN format** if provided: 15 chars, pattern `^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$`
8. **HSN format** if provided: 4-8 digits
9. **Tax math**: taxable amount × tax_rate / 100 = tax amount (within ±0.01)

## Error Response Format

If validation fails or required fields are missing:

```json
{
  "status": "needs_clarification",
  "missing_fields": ["voucher.party.gstin", "voucher.voucher_class"],
  "validation_errors": [
    { "field": "voucher.total", "error": "Total 46000 does not match items + taxes sum 46199.83" }
  ],
  "message": "Please provide the party GSTIN and confirm the voucher class name."
}
```

## Success Response Format

```json
{
  "status": "posted",
  "guid": "abc-purchase-ril2026-00123-20260115",
  "voucher_number": "186",
  "company": "ABC Company",
  "summary": "Purchase voucher posted: XYZ Party, ₹46,199.83 (taxable ₹39,152.40 + IGST ₹7,047.43)",
  "masters_created": ["XYZ Party"]
}
```
