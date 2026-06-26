# ReceiptExtract API Notes

## Endpoint

`POST https://www.receiptextract.com/api/receipt/upload`

## Auth

Bearer token in the `Authorization` header.

## Multipart form field

- `file` — one receipt image or PDF

## Example success payload

```json
{
  "success": true,
  "data": {
    "merchant": "Coffee Shop",
    "date": "2026-03-31",
    "items": [
      {
        "description": "Latte",
        "quantity": 1,
        "total_price": 5.25,
        "tax": 0.43
      }
    ],
    "tax": 0.43,
    "total": 5.68,
    "correctnessCheck": true,
    "taxBreakdown": [
      {
        "label": "TAX",
        "amount": 0.43,
        "currency": "USD",
        "confidence": 98.7
      }
    ]
  },
  "creditInfo": {
    "creditsUsed": 1,
    "remainingCredits": 249
  },
  "savedReceiptId": "a1b2c3d4"
}
```

## Example error payload

```json
{
  "success": false,
  "error": "Insufficient credits. Please purchase more credits to continue.",
  "remainingCredits": 0
}
```

## Suggested extracted fields

Receipt-level:
- merchant
- date
- tax
- total
- correctnessCheck
- taxBreakdown
- savedReceiptId

Line-item level:
- description
- quantity
- total_price
- tax
- sku

## Notes

- The API may return useful extraction even when some fields are imperfect.
- Sanity-check currency, tax labels, and item descriptions against the visible receipt when results look suspicious.
- Use raw JSON for debugging; use summary or CSV for downstream workflows.
