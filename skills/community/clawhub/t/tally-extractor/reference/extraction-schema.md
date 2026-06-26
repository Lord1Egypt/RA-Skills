# Extraction Schema

Canonical JSON emitted by Instance A (`tally-extractor-skill`) and consumed by Instance B via `bridge-service` → `tally-skill`. Mirror of `tally-skill/reference/bridge-input.md` with extraction-specific notes.

## Schema Version

Current: `1.0`

## JSON Schema (informal)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["schema_version", "request_id", "idempotency_key", "company", "voucher"],
  "properties": {
    "schema_version": { "type": "string", "const": "1.0" },
    "request_id": { "type": "string", "format": "uuid" },
    "idempotency_key": {
      "type": "string",
      "pattern": "^[a-z0-9]+-(purchase|sales|receipt|payment|journal|contra|creditnote|debitnote)-[a-z0-9]+-\\d{8}$"
    },
    "company": { "type": "string", "minLength": 1 },
    "voucher": {
      "type": "object",
      "required": ["type", "date", "number", "party", "total"],
      "properties": {
        "type": {
          "enum": ["Purchase", "Sales", "Receipt", "Payment", "Journal", "Contra", "CreditNote", "DebitNote"]
        },
        "date": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" },
        "number": { "type": "string" },
        "is_invoice_mode": { "type": "boolean" },
        "voucher_class": { "type": ["string", "null"] },
        "narration": { "type": "string" },
        "party": {
          "type": "object",
          "required": ["name"],
          "properties": {
            "name": { "type": "string" },
            "gstin": { "type": "string", "pattern": "^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$" },
            "place_of_supply": { "type": "string" },
            "registration_type": {
              "enum": ["Regular", "Composition", "Unregistered", "Consumer"]
            }
          }
        },
        "company_gstin": { "type": "string" },
        "items": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["description", "qty", "rate", "tax_rate", "amount"],
            "properties": {
              "description": { "type": "string" },
              "hsn": { "type": "string", "pattern": "^\\d{4,8}$" },
              "qty": { "type": "number", "exclusiveMinimum": 0 },
              "unit": { "type": "string" },
              "rate": { "type": "number" },
              "tax_rate": { "type": "number" },
              "amount": { "type": "number" }
            }
          }
        },
        "taxes": {
          "type": "object",
          "properties": {
            "cgst": { "type": "number" },
            "sgst": { "type": "number" },
            "igst": { "type": "number" },
            "round_off": { "type": "number" }
          }
        },
        "total": { "type": "number" },
        "ledgers": { "type": "object" },
        "bill_allocations": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "type", "amount"],
            "properties": {
              "name": { "type": "string" },
              "type": { "enum": ["New Ref", "Agst Ref", "Advance"] },
              "amount": { "type": "number" }
            }
          }
        }
      }
    },
    "source": {
      "type": "object",
      "properties": {
        "kind": { "enum": ["pdf", "image"] },
        "filename": { "type": "string" },
        "extracted_at": { "type": "string", "format": "date-time" }
      }
    },
    "confidence": {
      "type": "object",
      "properties": {
        "overall": { "type": "number", "minimum": 0, "maximum": 1 },
        "fields": { "type": "object" }
      }
    }
  }
}
```

## Numeric types

All amounts (`qty`, `rate`, `amount`, `taxes.*`, `total`, `bill_allocations[].amount`) must be JSON **numbers**, not strings. Use two decimal places where the invoice shows paise.

## Idempotency key pattern

```
{companyShort}-{voucherTypeLower}-{invoiceNumber}-{dateYYYYMMDD}
```

Examples:

- `abc-purchase-ril2026-00123-20260115`
- `abc-sales-186-20260518`
- `abc-receipt-chq991-20260518`

`voucherTypeLower`: purchase, sales, receipt, payment, journal, contra, creditnote, debitnote.

## Required fields by voucher type

| Voucher type | Required beyond root |
|---|---|
| Purchase / Sales | `party.gstin`, `party.place_of_supply`, `company_gstin`, `items[]` (≥1), `taxes`, `total` |
| Receipt / Payment | `party.name`, `total`, `ledgers.bank_or_cash` |
| Journal | `date`, `number`, `total`, `narration` recommended |
| Contra | `total`, bank/cash ledgers in `ledgers` |
| CreditNote / DebitNote | `party.name`, `total`, `bill_allocations` recommended |

## State code table (GSTIN → Place of Supply)

| Code | State |
|---|---|
| 01 | Jammu and Kashmir |
| 02 | Himachal Pradesh |
| 03 | Punjab |
| 04 | Chandigarh |
| 05 | Uttarakhand |
| 06 | Haryana |
| 07 | Delhi |
| 08 | Rajasthan |
| 09 | Uttar Pradesh |
| 10 | Bihar |
| 11 | Sikkim |
| 12 | Arunachal Pradesh |
| 13 | Nagaland |
| 14 | Manipur |
| 15 | Mizoram |
| 16 | Tripura |
| 17 | Meghalaya |
| 18 | Assam |
| 19 | West Bengal |
| 20 | Jharkhand |
| 21 | Odisha |
| 22 | Chhattisgarh |
| 23 | Madhya Pradesh |
| 24 | Gujarat |
| 25 | Daman and Diu |
| 26 | Dadra and Nagar Haveli |
| 27 | Maharashtra |
| 28 | Andhra Pradesh (Old) |
| 29 | Karnataka |
| 30 | Goa |
| 31 | Lakshadweep |
| 32 | Kerala |
| 33 | Tamil Nadu |
| 34 | Puducherry |
| 35 | Andaman and Nicobar Islands |
| 36 | Telangana |
| 37 | Andhra Pradesh |
| 38 | Ladakh |

Derive `place_of_supply` from the first two digits of `party.gstin` when not printed on the invoice.

## Worked example 1: Purchase with IGST (inter-state)

```json
{
  "schema_version": "1.0",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "idempotency_key": "abc-purchase-ril2026-00123-20260115",
  "company": "ABC Company",
  "voucher": {
    "type": "Purchase",
    "date": "2026-01-15",
    "number": "00123",
    "is_invoice_mode": true,
    "voucher_class": null,
    "narration": "Against Invoice 00123 from RIL",
    "party": {
      "name": "Reliance Industries Ltd",
      "gstin": "24AABCU9603R1ZM",
      "place_of_supply": "Gujarat",
      "registration_type": "Regular"
    },
    "company_gstin": "27AABCU9603R1ZN",
    "items": [
      {
        "description": "Industrial Chemical Grade A",
        "hsn": "28141000",
        "qty": 500,
        "unit": "Kg",
        "rate": 120.50,
        "tax_rate": 18,
        "amount": 60250.00
      }
    ],
    "taxes": {
      "cgst": 0,
      "sgst": 0,
      "igst": 10845.00,
      "round_off": 0
    },
    "total": 71095.00,
    "bill_allocations": [
      { "name": "00123", "type": "New Ref", "amount": 71095.00 }
    ]
  },
  "source": {
    "kind": "pdf",
    "filename": "ril_purchase_00123.pdf",
    "extracted_at": "2026-01-15T09:00:00Z"
  },
  "confidence": {
    "overall": 0.95,
    "fields": {
      "party.gstin": 1.0,
      "items[0].hsn": 0.85
    }
  }
}
```

Tax check: 60250 × 18% = 10845. Total: 60250 + 10845 = 71095.

## Worked example 2: Sales with CGST + SGST (intra-state)

```json
{
  "schema_version": "1.0",
  "request_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "idempotency_key": "abc-sales-186-20260518",
  "company": "ABC Company",
  "voucher": {
    "type": "Sales",
    "date": "2026-05-18",
    "number": "186",
    "is_invoice_mode": true,
    "voucher_class": "Sales @ 18 %",
    "narration": "Tax Invoice 186",
    "party": {
      "name": "XYZ Traders",
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
      "cgst": 3522.72,
      "sgst": 3522.71,
      "igst": 0,
      "round_off": 0
    },
    "total": 46197.83,
    "bill_allocations": [
      { "name": "186", "type": "New Ref", "amount": 46197.83 }
    ]
  },
  "source": {
    "kind": "image",
    "filename": "invoice_186.jpg",
    "extracted_at": "2026-05-18T10:30:00Z"
  },
  "confidence": {
    "overall": 0.92,
    "fields": {
      "voucher.voucher_class": 0.65
    }
  }
}
```

Both company and party GSTIN start with `27` (Maharashtra) → CGST + SGST, no IGST.

## Worked example 3: Receipt (payment received in bank)

```json
{
  "schema_version": "1.0",
  "request_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "idempotency_key": "abc-receipt-chq991-20260518",
  "company": "ABC Company",
  "voucher": {
    "type": "Receipt",
    "date": "2026-05-18",
    "number": "CHQ-991",
    "is_invoice_mode": false,
    "narration": "Cheque received against Invoice 186",
    "party": {
      "name": "XYZ Traders",
      "gstin": "27AABCU9603R1ZM",
      "place_of_supply": "Maharashtra",
      "registration_type": "Regular"
    },
    "total": 46197.83,
    "ledgers": {
      "bank_or_cash": "HDFC Bank - Current A/c"
    },
    "bill_allocations": [
      { "name": "186", "type": "Agst Ref", "amount": 46197.83 }
    ]
  },
  "source": {
    "kind": "pdf",
    "filename": "cheque_deposit_991.pdf",
    "extracted_at": "2026-05-18T14:00:00Z"
  },
  "confidence": {
    "overall": 0.88,
    "fields": {
      "voucher.ledgers.bank_or_cash": 0.6
    }
  }
}
```

Receipt vouchers typically have no `items[]` or `taxes`. Confirm bank ledger name with user if confidence < 0.7.

## Cross-links

- Instance B mapping rules: `../../tally-skill/reference/bridge-input.md`
- Voucher XML templates: `../../tally-skill/reference/vouchers.md`
- HTTP transport: `bridge.md`
