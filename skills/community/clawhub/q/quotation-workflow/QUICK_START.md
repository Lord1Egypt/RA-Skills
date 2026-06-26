# 🚀 报价单工作流 - 快速开始

**5 分钟生成专业报价单！**

---

## 📋 完整流程

```
准备数据 → 生成 Excel → 生成 Word → 导出 PDF → 发送邮件
```

---

## 1️⃣ 准备报价数据

### 方法 A：使用模板（推荐）

复制示例文件并修改：
```bash
cd /Users/wilson/.openclaw/workspace/skills/quotation-workflow/examples

# 复制示例
cp farreach_sample.json my_quotation.json

# 编辑数据
code my_quotation.json  # 或用你喜欢的编辑器
```

### 方法 B：从零创建

```bash
cat > my_quotation.json << 'EOF'
{
  "customer": {
    "company_name": "客户公司名称",
    "contact": "联系人姓名",
    "email": "customer@example.com"
  },
  "quotation": {
    "quotation_no": "QT-20260314-002",
    "date": "2026-03-14",
    "valid_until": "2026-04-13"
  },
  "products": [
    {
      "description": "产品名称",
      "specification": "规格型号",
      "quantity": 100,
      "unit_price": 10.00
    }
  ],
  "currency": "USD",
  "payment_terms": "T/T 30% deposit, 70% before shipment",
  "lead_time": "15-20 days",
  "freight": 0,
  "tax": 0
}
EOF
```

---

## 2️⃣ 生成 Excel 报价单

```bash
cd /Users/wilson/.openclaw/workspace/skills/excel-xlsx/scripts

python3 generate_quotation.py \
  --data ../../quotation-workflow/examples/my_quotation.json \
  --output ../../quotation-workflow/examples/QT-20260314-002.xlsx
```

✅ 输出：`QT-20260314-002.xlsx`

---

## 3️⃣ 生成 Word 报价单

```bash
cd /Users/wilson/.openclaw/workspace/skills/word-docx/scripts

python3 generate_quotation_docx.py \
  --data ../../quotation-workflow/examples/my_quotation.json \
  --output ../../quotation-workflow/examples/QT-20260314-002.docx
```

✅ 输出：`QT-20260314-002.docx`

---

## 4️⃣ 导出 PDF

```bash
cd /Users/wilson/.openclaw/workspace/skills/quotation-workflow/examples

# 单个文件
soffice --headless --convert-to pdf QT-20260314-002.xlsx --outdir ./

# 或使用脚本批量转换
../scripts/convert-to-pdf.sh QT-20260314-002.xlsx QT-20260314-002.docx
```

✅ 输出：`QT-20260314-002.pdf`

---

## 5️⃣ 查看生成的文件

```bash
# 打开 Excel
open QT-20260314-002.xlsx

# 打开 Word
open QT-20260314-002.docx

# 打开 PDF
open QT-20260314-002.pdf
```

---

## 🎯 完整示例（一键生成所有格式）

```bash
# 设置变量
DATA_FILE="/Users/wilson/.openclaw/workspace/skills/quotation-workflow/examples/my_quotation.json"
OUTPUT_DIR="/Users/wilson/.openclaw/workspace/skills/quotation-workflow/examples"
OUTPUT_NAME="QT-20260314-002"

# 生成 Excel
python3 /Users/wilson/.openclaw/workspace/skills/excel-xlsx/scripts/generate_quotation.py \
  --data "$DATA_FILE" \
  --output "$OUTPUT_DIR/$OUTPUT_NAME.xlsx"

# 生成 Word
python3 /Users/wilson/.openclaw/workspace/skills/word-docx/scripts/generate_quotation_docx.py \
  --data "$DATA_FILE" \
  --output "$OUTPUT_DIR/$OUTPUT_NAME.docx"

# 导出 PDF
cd "$OUTPUT_DIR"
soffice --headless --convert-to pdf "$OUTPUT_NAME.xlsx" --outdir ./
soffice --headless --convert-to pdf "$OUTPUT_NAME.docx" --outdir ./

echo "✅ 完成！生成文件："
ls -lh "$OUTPUT_DIR"/$OUTPUT_NAME.*
```

---

## 📊 数据格式说明

### 客户信息 (customer)
| 字段 | 说明 | 示例 |
|------|------|------|
| company_name | 公司名称 | Best Buy Electronics Inc. |
| contact | 联系人 | Michael Johnson |
| email | 邮箱 | mjohnson@example.com |
| phone | 电话（可选） | +1-612-555-0100 |
| address | 地址（可选） | 7601 Penn Avenue South... |

### 报价单信息 (quotation)
| 字段 | 说明 | 示例 |
|------|------|------|
| quotation_no | 报价单号 | QT-20260314-001 |
| date | 报价日期 | 2026-03-14 |
| valid_until | 有效期至 | 2026-04-13 |

### 产品列表 (products[])
| 字段 | 说明 | 示例 |
|------|------|------|
| description | 产品描述 | HDMI 2.1 Ultra High Speed Cable |
| specification | 规格型号 | 8K@60Hz, 48Gbps, 2m |
| quantity | 数量 | 500 |
| unit_price | 单价（USD） | 8.50 |

### 其他字段
| 字段 | 说明 | 默认值 |
|------|------|--------|
| currency | 币别 | USD |
| payment_terms | 付款条款 | T/T 30% deposit, 70% before shipment |
| lead_time | 交货期 | 15-20 days after deposit |
| freight | 运费 | 0 |
| tax | 税费 | 0 |
| notes | 备注 | 自动填充标准条款 |

---

## 🔧 常用命令

### 查看 Excel 内容
```bash
python3 /Users/wilson/.openclaw/workspace/skills/excel-xlsx/scripts/read_excel.py \
  "QT-20260314-002.xlsx" --format table
```

### 快速测试（使用内置测试数据）
```bash
# Excel
python3 generate_quotation.py --output test.xlsx --quick-test

# Word
python3 generate_quotation_docx.py --output test.docx --quick-test

# 查看内容
python3 read_excel.py test.xlsx --format table
```

---

## 📁 文件位置汇总

| 文件类型 | 路径 |
|---------|------|
| **Excel 生成脚本** | `/Users/wilson/.openclaw/workspace/skills/excel-xlsx/scripts/generate_quotation.py` |
| **Excel 读取脚本** | `/Users/wilson/.openclaw/workspace/skills/excel-xlsx/scripts/read_excel.py` |
| **Word 生成脚本** | `/Users/wilson/.openclaw/workspace/skills/word-docx/scripts/generate_quotation_docx.py` |
| **Word 读取脚本** | `/Users/wilson/.openclaw/workspace/skills/read-docx/read-docx.py` |
| **PDF 转换脚本** | `/Users/wilson/.openclaw/workspace/skills/quotation-workflow/scripts/convert-to-pdf.sh` |
| **示例数据** | `/Users/wilson/.openclaw/workspace/skills/quotation-workflow/examples/` |
| **数据模板** | `/Users/wilson/.openclaw/workspace/skills/quotation-workflow/quotation_data_template.json` |

---

## ❓ 常见问题

### Q: 中文文件名乱码？
A: 使用 glob 通配符，不要直接传中文路径：
```bash
# ✅ 正确
python3 read_excel.py "报价单*.xlsx"

# ❌ 错误（可能失败）
python3 read_excel.py "报价单 20260314.xlsx"
```

### Q: Excel 公式不计算？
A: 打开 Excel 文件时会自动重新计算。也可以用 LibreOffice 强制刷新：
```bash
soffice --headless --convert-to xlsx file.xlsx --outdir ./
```

### Q: 如何修改模板格式？
A: 直接编辑脚本中的样式定义部分（颜色、字体、列宽等）。

### Q: 如何批量生成多个报价单？
A: 准备多个 JSON 文件，用循环：
```bash
for file in quotations/*.json; do
  python3 generate_quotation.py --data "$file" --output "output/$(basename $file .json).xlsx"
done
```

---

**需要帮助？** 查看完整文档：`README.md`
