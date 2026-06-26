# Invoice Field Reference

## Table of Contents
1. [Required Fields](#required-fields)
2. [Vietnamese Invoice Format (Hóa đơn GTGT)](#vietnamese-invoice-format)
3. [International Invoice Formats](#international-invoice-formats)
4. [VAT Rules (Vietnam)](#vat-rules-vietnam)

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `invoice_number` | string | Unique invoice identifier |
| `invoice_date` | YYYY-MM-DD | Date of invoice issuance |
| `vendor_name` | string | Name of the seller/vendor |
| `vendor_tax_code` | string | Tax identification number |
| `items` | array | Line items with description, qty, unit_price, total |
| `subtotal` | number | Sum of line item totals (before tax) |
| `vat_rate` | number | VAT percentage (0, 5, 8, or 10) |
| `vat_amount` | number | Calculated VAT amount |
| `total_amount` | number | Final amount including VAT |
| `payment_terms` | string | Payment conditions |

## Vietnamese Invoice Format

Vietnamese VAT invoices (Hóa đơn GTGT) follow Circular 78/2021/TT-BTC:

### Key Labels (Vietnamese → English)
- **Ký hiệu** → Invoice series/symbol
- **Số** → Invoice number
- **Ngày ... tháng ... năm** → Date format (day month year)
- **Đơn vị bán hàng** → Seller/Vendor
- **Mã số thuế** → Tax code
- **Tên hàng hóa, dịch vụ** → Item description
- **Đơn vị tính** → Unit of measure
- **Số lượng** → Quantity
- **Đơn giá** → Unit price
- **Thành tiền** → Amount (line total)
- **Cộng tiền hàng** → Subtotal
- **Thuế suất GTGT** → VAT rate
- **Tiền thuế GTGT** → VAT amount
- **Tổng cộng tiền thanh toán** → Total amount

### E-Invoice Format
Since July 2022, Vietnam requires electronic invoices (hóa đơn điện tử) with QR code, digital signature, and unique lookup code from tax authority.

## International Invoice Formats

Common English labels: Invoice No, Date, Bill To, Subtotal, Tax/VAT/GST, Total, Payment Terms, Due Date.

## VAT Rules (Vietnam)

| Rate | Applies to |
|------|-----------|
| 0% | Exported goods and services |
| 5% | Essential goods (water, medicine, education) |
| 8% | Reduced rate (temporary policy for certain sectors) |
| 10% | Standard rate (most goods and services) |

### Validation Rules
1. `vat_amount = subtotal × vat_rate / 100`
2. `total_amount = subtotal + vat_amount`
3. `subtotal = sum(item.total for each item)`
4. `item.total = item.quantity × item.unit_price`
