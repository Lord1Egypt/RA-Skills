# 报价单模板 (Quote Template)

## 标准报价单结构

```
┌─────────────────────────────────────────────────────────────┐
│  [公司Logo]                                                  │
│  YIWU BEST TRADING CO., LTD.                                │
│  Address: Room 123, Building A, Yiwu International Trade   │
│           City, Zhejiang Province, China                    │
│  Tel: +86 579 12345678 | Email: sales@yiwubest.com          │
│  WhatsApp: +86 139 1234 5678                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PROFORMA INVOICE                                          │
│                                                             │
│  Quote No.: QT20240315001           Date: 2024-03-15       │
│  Valid Until: 2024-03-22            Payment: T/T 30%       │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  SOLD TO:                        SHIP TO:                   │
│  ABC Trading LLC                 [Same as sold to]         │
│  Dubai, UAE                                               │
│  Attn: Ahmed Hassan              Tel: +971 50 123 4567    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────┬─────────┬────────────────────────────────┬────────┬────────┬──────────┐
│  │No. │  SKU    │  Description                   │  QTY   │  Unit  │  Amount  │
│  ├────┼─────────┼────────────────────────────────┼────────┼────────┼──────────┤
│  │ 1  │ BB-001  │ Yoga Mat with LED Lights       │ 500 pcs│ USD    │          │
│  │    │         │ 8mm, Anti-slip, USB charging   │        │ 11.20  │ 5,600.00 │
│  ├────┼─────────┼────────────────────────────────┼────────┼────────┼──────────┤
│  │ 2  │ BB-002  │ LED Controller                 │ 500 pcs│ USD    │          │
│  │    │         │ Remote control                 │        │ 2.50   │ 1,250.00 │
│  ├────┼─────────┼────────────────────────────────┼────────┼────────┼──────────┤
│  │    │         │                                │        │        │          │
│  └────┴─────────┴────────────────────────────────┴────────┴────────┴──────────┘
│                                                             │
│  ┌─────────────────────────────────────────┬─────────────────────────────┐
│  │  Subtotal                               │ USD 6,850.00                │
│  │  Inspection Fee                         │ USD 100.00                 │
│  │  ────────────────────────────────────   ├─────────────────────────────┤
│  │  TOTAL AMOUNT (FOB Ningbo)              │ USD 6,950.00               │
│  └─────────────────────────────────────────┴─────────────────────────────┘
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐
│  │  SHIPPING ESTIMATE:                                     │
│  │  20FT Container: 500 pcs                                │
│  │  Estimated Freight (Ningbo-Dubai): USD 450              │
│  │  Customs Duty (UAE, 5%): USD 347.50                    │
│  │  ────────────────────────────────────                   │
│  │  Estimated CIF Dubai: USD 7,747.50                      │
│  └─────────────────────────────────────────────────────────┘
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  TERMS & CONDITIONS:                                       │
│  1. Price valid for 7 days from issue date                  │
│  2. 30% deposit required to start production               │
│  3. Balance payable before shipment                        │
│  4. Lead time: 15-20 days after deposit receipt           │
│  5. Sample available at 1.5x unit price, shipping prepaid  │
│  6. Quality inspection available (fee: USD 100)             │
│  7. Shipping marks: as per buyer's instruction             │
│                                                             │
│  BANK INFORMATION:                                         │
│  Bank Name: Industrial and Commercial Bank of China        │
│  Account Name: YIWU BEST TRADING CO., LTD.                 │
│  Account No.: 6222 1234 5678 9012                         │
│  SWIFT Code: ICBKCNBJZJE                                  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Authorized Signature: _________________                    │
│  John Wang | Sales Manager                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 报价单字段说明

### Header信息
| 字段 | 说明 | 示例 |
|------|------|------|
| Quote No. | 报价单编号，格式：QT+日期+序号 | QT20240315001 |
| Date | 报价日期 | 2024-03-15 |
| Valid Until | 有效期截止日期 | 2024-03-22 |
| Payment | 付款方式 | T/T 30% Deposit |

### 产品行
| 字段 | 说明 | 必填 |
|------|------|------|
| Item No. | 序号 | ✓ |
| SKU | 产品编码 | ✓ |
| Description | 产品描述 | ✓ |
| Specifications | 规格参数 | ○ |
| MOQ | 最小起订量 | ○ |
| Quantity | 订购数量 | ✓ |
| Unit | 单位 | ✓ |
| Unit Price | 单价 | ✓ |
| Amount | 金额小计 | ✓ |

### 价格汇总
| 字段 | 说明 |
|------|------|
| Subtotal | 商品小计 |
| Discount | 折扣金额 |
| Inspection Fee | 验货费 |
| Loading Fee | 装柜费 |
| Insurance | 保险费 |
| Grand Total | 总金额 |

---

## 报价单模板变量

```markdown
## 基本变量
{{quote_number}}       # 报价单编号
{{quote_date}}         # 报价日期
{{valid_until}}        # 有效期截止
{{currency}}          # 货币代码
{{incoterms}}          # 贸易术语

## 供应商信息
{{supplier_name}}      # 公司名称
{{supplier_address}}   # 公司地址
{{supplier_tel}}       # 联系电话
{{supplier_email}}     # 邮箱
{{supplier_whatsapp}}  # WhatsApp

## 客户信息
{{client_company}}     # 客户公司
{{client_contact}}     # 联系人
{{client_country}}     # 国家
{{client_address}}     # 客户地址

## 产品信息
{{products[]}}         # 产品列表
  - sku
  - description
  - specifications
  - quantity
  - unit_price
  - amount

## 价格汇总
{{subtotal}}           # 小计
{{discount}}           # 折扣
{{fees}}               # 附加费用
{{grand_total}}        # 总计

## 银行信息
{{bank_name}}          # 银行名称
{{account_name}}       # 账户名
{{account_number}}     # 账户号码
{{swift_code}}         # SWIFT代码
```

---

## 不同格式模板

### 简洁模板 (Compact)
```
┌─────────────────────────────────────────────────────────┐
│  YIWU BEST TRADING - QUOTATION                         │
├─────────────────────────────────────────────────────────┤
│  To: ABC Trading LLC │ Date: 2024-03-15 │ Ref: QT01   │
├─────────────────────────────────────────────────────────┤
│  Product │ QTY │ Unit │ Price │ Amount                │
│  ─────────────────────────────────────────────────────  │
│  LED Yoga Mat │ 500 pcs │ USD 11.20 │ USD 5,600.00   │
│  LED Controller │ 500 pcs │ USD 2.50 │ USD 1,250.00 │
│  ─────────────────────────────────────────────────────  │
│  TOTAL: USD 6,850.00 FOB Ningbo                         │
│  Lead Time: 15-20 days | Payment: T/T 30%             │
├─────────────────────────────────────────────────────────┤
│  John Wang | sales@yiwubest.com | +86 139 1234 5678   │
└─────────────────────────────────────────────────────────┘
```

### 详细模板 (Detailed)
包含：产品图片、技术参数、认证信息、包装详情、验货标准等
