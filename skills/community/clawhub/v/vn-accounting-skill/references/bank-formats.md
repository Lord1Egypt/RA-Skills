# Bank Statement Formats

## Table of Contents
1. [Vietnamese Banks](#vietnamese-banks)
2. [Statement Field Labels](#statement-field-labels)
3. [Transaction Table Columns](#transaction-table-columns)
4. [Amount Formats](#amount-formats)

## Vietnamese Banks

| Bank | Abbreviation | Format Notes |
|------|-------------|--------------|
| Vietcombank | VCB | PDF with tables, clear headers |
| Techcombank | TCB | PDF, often merged cells |
| BIDV | BIDV | PDF with standard table layout |
| VietinBank | CTG | PDF with header block |
| MB Bank | MBB | PDF, sometimes image-based |
| VPBank | VPB | PDF with summary section |
| ACB | ACB | PDF with transaction details |
| Sacombank | STB | PDF, mixed formats |
| TPBank | TPB | PDF, clean digital format |
| HDBank | HDB | PDF with account summary |
| Agribank | AGR | PDF, older format styles |

## Statement Field Labels

### Vietnamese → English
- **Sao kê tài khoản** → Account Statement
- **Số tài khoản** / **STK** → Account Number
- **Chủ tài khoản** → Account Holder
- **Kỳ sao kê** / **Từ ngày ... đến ngày** → Statement Period
- **Số dư đầu kỳ** → Opening Balance
- **Số dư cuối kỳ** → Closing Balance
- **Ngày giao dịch** → Transaction Date
- **Diễn giải** / **Nội dung** → Description
- **Số tiền ghi nợ** / **Chi** → Debit Amount
- **Số tiền ghi có** / **Thu** → Credit Amount
- **Số dư** → Balance
- **Mã giao dịch** / **Số tham chiếu** → Reference Number

## Transaction Table Columns

### Standard layout (most banks)
```
| Ngày GD | Ngày HL | Mô tả | Nợ (Debit) | Có (Credit) | Số dư |
```

### Compact layout
```
| Date | Description | Amount | Balance |
```

## Amount Formats

### Vietnamese Dong (VND)
- No decimal places (smallest unit is 1 VND)
- Thousands separator: dot (.) or comma (,)
- Examples: `1.000.000` or `1,000,000` = 1 million VND
- Suffixes: `VND`, `đ`, `VNĐ`
- Negative: parentheses `(500.000)` or minus `-500.000`
