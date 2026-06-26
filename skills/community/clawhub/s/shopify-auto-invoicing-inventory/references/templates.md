# Templates

## Invoice-ready order object

```json
{
  "order_id": "",
  "order_name": "",
  "created_at": "",
  "financial_status": "paid",
  "customer_name": "",
  "customer_email": "",
  "billing_name": "",
  "billing_address": "",
  "currency": "EUR",
  "line_items": [
    {
      "sku": "",
      "title": "",
      "quantity": 1,
      "unit_price": 0,
      "tax_amount": 0,
      "line_total": 0
    }
  ],
  "subtotal": 0,
  "shipping": 0,
  "tax": 0,
  "total": 0
}
```

## Invoice section template

- Invoice number:
- Invoice date:
- Order reference:
- Merchant:
- Customer:
- Billing address:
- Currency:
- Line items:
- Subtotal:
- Tax:
- Shipping:
- Grand total:
- Payment status:

## Monthly report template

- Period:
- Orders processed:
- Paid orders:
- Pending-payment orders:
- Cancelled orders:
- Invoice-ready orders:
- Invoiced revenue:
- Tax collected:
- Units sold:
- Low-stock SKUs:
- Exceptions:

## Merchant-facing language

### Invoice note

Thank you for your order. This invoice summarizes the products billed for the referenced Shopify order.

### Stock alert note

This product is approaching the low-stock threshold and should be reviewed for replenishment.

### Exception note

This order requires review before invoicing because one or more billing or inventory fields are incomplete.
