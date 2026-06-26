# 📋 报价单工作流 - 标准化流程

**版本：** 2.0.0  
**更新时间：** 2026-03-15  
**状态：** ✅ 完成

---

## 📧 邮件发送规则

**重要：** 邮件附件使用 **HTML 转换的 PDF**

```
邮件附件 = QT-XXXX-HTML.pdf（HTML 转换的 PDF）
          ↓
          ✅ 现代设计、专业美观、适合发送客户

不是：QT-XXXX-Excel.pdf（Excel 转换的 PDF）
          ↓
          ⚠️ 传统风格，仅用于内部存档
```

---

## 🎯 标准工作流

### 方式 1：一键生成（最简单 ⭐）

```bash
cd /Users/wilson/.openclaw/workspace/skills/quotation-workflow

# 一键生成所有格式
./scripts/generate-all.sh examples/farreach_sample.json QT-20260314-001
```

**生成文件：**
- QT-20260314-001.xlsx（Excel）- 内部存档
- QT-20260314-001.docx（Word）- 备用
- QT-20260314-001.html（HTML）- 在线预览
- **QT-20260314-001-HTML.pdf** ⭐ - **邮件附件（推荐）**
- QT-20260314-001-Excel.pdf（Excel 导出 PDF）- 备用

---

### 方式 2：标准流程（带页码）⭐⭐⭐

```bash
# 1. 准备数据
cp examples/farreach_sample.json my_quotation.json

# 2. 生成 HTML
python3 scripts/generate_quotation_html.py \
  --data my_quotation.json \
  --output QT-20260314-001.html

# 3. Chrome 导出 PDF（无页眉页脚）
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=QT-20260314-001.pdf \
  "file://$(pwd)/QT-20260314-001.html"

# 4. 添加页码（底部右侧）
python3 scripts/add-pagenumbers.py \
  QT-20260314-001.pdf \
  QT-20260314-001-Final.pdf
```

**最终文件：** `QT-20260314-001-Final.pdf`

---

### 方式 3：单独生成特定格式

```bash
# Excel（传统工整风格）
python3 ../excel-xlsx/scripts/generate_quotation_traditional.py \
  --data my_quotation.json --output QT-001.xlsx

# Word
python3 ../word-docx/scripts/generate_quotation_docx.py \
  --data my_quotation.json --output QT-001.docx

# HTML（现代设计）
python3 scripts/generate_quotation_html.py \
  --data my_quotation.json --output QT-001.html
```

---

## 📊 数据格式

### 完整示例

```json
{
  "company_name": "Farreach Electronic Co., Ltd.",
  "company_tagline": "Premium Connectivity Solutions",
  "company_address": "No. 123, Technology Road, Zhuhai, Guangdong, China",
  "company_email": "sale@farreach-electronic.com",
  "company_website": "www.farreach-electronic.com",
  "customer": {
    "company_name": "Best Buy Electronics Inc.",
    "contact": "Michael Johnson",
    "address": "7601 Penn Avenue South, Richfield, MN 55423, USA",
    "email": "mjohnson@bestbuy-example.com"
  },
  "quotation": {
    "quotation_no": "QT-20260314-001",
    "date": "2026-03-14",
    "valid_until": "2026-04-13"
  },
  "trade_terms": {
    "incoterms": "FOB Shenzhen"
  },
  "products": [
    {
      "description": "HDMI 2.1 Ultra High Speed Cable",
      "specification": "8K@60Hz, 4K@120Hz, 48Gbps, HDR, eARC, 2m",
      "quantity": 500,
      "unit_price": 8.50
    }
  ],
  "currency": "USD",
  "lead_time": "15-20 days",
  "payment_terms": "T/T 30% deposit, 70% before shipment",
  "freight": 350.00,
  "bank_info": {
    "beneficiary": "Farreach Electronic Co., Ltd.",
    "bank_name": "Standard Chartered Bank",
    "account_no": "1234 5678 9012",
    "swift_code": "SCBLHKHH"
  }
}
```

### 必填字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `customer.company_name` | string | 客户公司名称 |
| `customer.contact` | string | 联系人 |
| `quotation.quotation_no` | string | 报价单号 |
| `products` | array | 产品列表 |
| `products[].description` | string | 产品描述 |
| `products[].quantity` | number | 数量 |
| `products[].unit_price` | number | 单价 |

---

## 🛠️ 脚本位置

| 脚本 | 路径 | 用途 |
|------|------|------|
| **HTML 生成** | `scripts/generate_quotation_html.py` | 生成 HTML 报价单 |
| **Excel 生成** | `../excel-xlsx/scripts/generate_quotation_traditional.py` | 生成 Excel |
| **Word 生成** | `../word-docx/scripts/generate_quotation_docx.py` | 生成 Word |
| **PDF 页码** | `scripts/add-pagenumbers.py` | 添加页码 |
| **一键生成** | `scripts/generate-all.sh` | 一键生成所有格式 |

---

## 📄 PDF 输出规格

### 标准 A4

- **尺寸：** 210 × 297 mm
- **边距：** 上下 10mm，左右 15mm
- **页码：** 底部右侧，"Page X of Y"
- **字体：** Helvetica 9pt，灰色 #64748B

### 打印兼容性

- ✅ 标准 A4 尺寸，任何打印机兼容
- ✅ 无页眉页脚（干净）
- ✅ 可直接发送给客户或打印店

---

## ⚠️ 常见问题

### Q1: PDF 底部有 "Page /" 怎么办？

**A:** 这是 CSS 页码代码的残留，解决方法：

```bash
# 重新生成 HTML（确保没有旧的页码代码）
python3 scripts/generate_quotation_html.py --data data.json -o QT-001.html

# Chrome 导出 PDF
chrome --headless --no-pdf-header-footer \
  --print-to-pdf=QT-001.pdf file://QT-001.html

# 用 reportlab 添加页码
python3 scripts/add-pagenumbers.py QT-001.pdf QT-001-Final.pdf
```

### Q2: 有空白页怎么办？

**A:** CSS 中 `min-height: 297mm` 导致，确保使用：

```css
.a4-container {
    min-height: auto;  /* 让内容决定高度 */
}
```

### Q3: 签名怎么添加？

**A:** 三种方式：

1. **打印后手写**（推荐）
   - 打印 PDF
   - 手写签名
   - 扫描发送

2. **Word 中插入**
   - 生成 Word 版本
   - 插入签名图片
   - 导出 PDF

3. **PDF 后处理**
   - 用 Adobe Acrobat 添加
   - 或用在线工具

### Q4: 页码位置不对？

**A:** 检查 `add-pagenumbers.py` 中的坐标：

```python
c.drawRightString(575, 20, text)  # 距离右边 20pt，底部 20pt
```

---

## 🎯 最佳实践

### 文件命名

```
QT-YYYYMMDD-XXX[-Description].pdf
例：QT-20260314-001-Final.pdf
```

### 产品数量建议

- **1-5 款产品：** 1-2 页
- **6-10 款产品：** 2-3 页
- **10+ 款产品：** 考虑分页或附件

### 发送客户

**推荐格式：** PDF（标准 A4，带页码）

**邮件正文示例：**
```
Dear [Customer],

Please find attached our quotation QT-20260314-001.

Total: USD $31,690.00 (FOB Shenzhen)
Valid until: 2026-04-13

Should you need any clarification, please feel free to contact us.

Best regards,
[Your Name]
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| [QUICK_START.md](QUICK_START.md) | 5 分钟快速上手 |
| [SKILL.md](SKILL.md) | 技能标准文档 |
| [FORMATS.md](FORMATS.md) | 格式对比指南 |
| [PDF_EXPORT.md](PDF_EXPORT.md) | PDF 导出详细指南 |
| [COMPLETE_WORKFLOW.md](COMPLETE_WORKFLOW.md) | 完整工作流 |

---

**最后更新：** 2026-03-14  
**维护者：** WILSON
