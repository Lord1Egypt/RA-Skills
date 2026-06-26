# Purchase Order Field Reference

## Table of Contents
1. [Required Fields](#required-fields)
2. [Vietnamese PO Labels](#vietnamese-po-labels)
3. [Delivery Tracking](#delivery-tracking)
4. [Common Payment Terms](#common-payment-terms)

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `po_number` | string | Unique PO identifier |
| `po_date` | YYYY-MM-DD | Date the PO was issued |
| `vendor_name` | string | Supplier/vendor name |
| `delivery_date` | YYYY-MM-DD | Expected delivery date |
| `items` | array | Line items with description, qty, unit_price, total |
| `total_amount` | number | Total PO value |
| `payment_terms` | string | Payment conditions |

## Vietnamese PO Labels

- **Đơn đặt hàng** / **Đơn mua hàng** → Purchase Order
- **Số PO** / **Số ĐĐH** → PO Number
- **Ngày đặt hàng** → Order Date
- **Nhà cung cấp** / **Đơn vị cung cấp** → Vendor/Supplier
- **Ngày giao hàng** / **Hạn giao** → Delivery Date
- **Tên hàng hóa** → Item Description
- **Số lượng** → Quantity
- **Đơn giá** → Unit Price
- **Thành tiền** → Line Total
- **Tổng cộng** / **Tổng giá trị** → Total Amount
- **Điều khoản thanh toán** → Payment Terms

## Delivery Tracking

| Days Left | Status |
|-----------|--------|
| < 0 | **OVERDUE** — delivery date has passed |
| 0-3 | **URGENT** — delivery imminent |
| 4-7 | **APPROACHING** — delivery coming soon |
| > 7 | **ON_TRACK** — within normal timeline |

## Common Payment Terms

- **COD** — Cash on Delivery
- **Net 30 / Net 60** — Payment due N days after invoice
- **TT** — Telegraphic Transfer (wire)
- **L/C** — Letter of Credit
- **Trả trước** — Prepayment
- **Trả sau** — Deferred payment
