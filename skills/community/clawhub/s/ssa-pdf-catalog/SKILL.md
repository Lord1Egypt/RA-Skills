---
name: pdf-product-catalog
description: 从 PDF 产品目录（模具图纸）中自动提取产品信息，生成结构化知识库和 Excel 填充数据。
---

# PDF 产品目录提取 Skill

> **技能名称：** pdf-product-catalog  
> **版本：** 1.0  
> **日期：** 2026-03-23  
> **作者：** IRON 💪

---

## 📋 技能描述

从 PDF 产品目录（模具图纸）中自动提取产品信息，生成结构化知识库和 Excel 填充数据。

**适用场景：**
- 产品目录 PDF 批量处理
- 模具图纸信息提取
- 产品知识库建立
- Excel 产品数据填充

---

## 🎯 核心功能

1. **PDF 文本提取** — pdftotext（矢量图）+ Docling OCR（图片格式 fallback）
2. **关键信息识别** — 模具号、包装规范、客户品名、长度
3. **错误排除** — 识别并排除包装规范（BJ0599-XXXX）误认为模具号
4. **知识库生成** — Markdown 词条 + JSON 结构化数据
5. **Excel 填充** — 自动填充 SKU→模具号映射

---

## 📁 文件结构

```
pdf-product-catalog/
├── SKILL.md              # 技能说明（本文件）
├── scripts/
│   └── extract.py        # 主提取脚本
├── examples/
│   ├── sample_input.json # 输入示例
│   └── sample_output.md  # 输出示例
└── output/               # 输出目录（运行时生成）
```

---

## 🔧 使用方法

### 1️⃣ 基础用法

```bash
python3 skills/pdf-product-catalog/scripts/extract.py \
  --pdf-dir "/path/to/pdf/files" \
  --output-dir "/path/to/output"
```

### 2️⃣ 完整参数

```bash
python3 scripts/extract.py \
  --pdf-dir "/path/to/pdfs" \
  --output-dir "/path/to/output" \
  --excel-path "/path/to/excel.xlsx" \
  --ocr-threshold 300 \
  --verbose
```

### 3️⃣ 参数说明

| 参数 | 必需 | 说明 | 默认值 |
|------|------|------|--------|
| `--pdf-dir` | ✅ | PDF 文件目录 | - |
| `--output-dir` | ✅ | 输出目录 | - |
| `--excel-path` | ❌ | Excel 文件路径（用于填充） | None |
| `--ocr-threshold` | ❌ | 文本少于多少字符时启用 OCR | 300 |
| `--verbose` | ❌ | 详细输出模式 | False |

---

## 📊 提取流程

### Step 1: PDF 文本提取

```python
# 优先使用 pdftotext（矢量图 PDF 准确快速）
result = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True)

# 如果文本太短（<300 字符），启用 OCR fallback
if len(text) < ocr_threshold:
    # 转图片 + Docling OCR
    subprocess.run(['pdftoppm', '-png', '-r', '300', pdf_path, img_path])
    ocr_result = converter.convert(img_path)
    text = ocr_result.document.export_to_markdown()
```

### Step 2: 关键信息提取

```python
# 1. 模具号 (MODEL NO.) - 优先级最高
model_match = re.search(r'MODEL\s+NO\.?\s*[:\|\s\n]*([A-Z]{2,}-\d+[A-Z]?)', text, re.IGNORECASE)

# 2. 包装规范 (Package No.) - BJ0599-XXXX 格式
pkg_matches = re.findall(r'(BJ0599-\d{4})', text)

# 3. 客户品名 (CUSTOMER ITEM)
ci_match = re.search(r'CUSTOMER ITEM\s*\n([A-Za-z0-9\-]+)', text, re.IGNORECASE)

# 4. 长度 (LENGTH)
length_matches = re.findall(r'(\d{2,4})\s*\+\d*\s*-\d*\s*(mm)?', text)
```

### Step 3: 错误排除规则

```python
# ❌ 排除规则 1: BJ0599-XXXX 是包装规范，不是模具号
if model_no.startswith('BJ0599-'):
    model_no = None  # 重新提取

# ❌ 排除规则 2: 客户品名不是模具号
if customer_item == model_no:
    # 可能模具号在图片中，需要 OCR 重新提取
    model_no = extract_with_ocr()

# ❌ 排除规则 3: 太短的字符串不是模具号
if len(model_no) < 5:
    model_no = None  # 如 "TP" 需要人工确认
```

### Step 4: 知识库生成

```python
# Markdown 词条
product_md = f"""# {pdf_file} 产品类目词条

## 基础信息
- **模具号 (MODEL NO.):** {model_no}
- **包装规范:** {', '.join(package_specs)}
- **客户品名:** {', '.join(customer_items)}
- **长度:** {', '.join(lengths)}

## 产品类目
（详细产品信息...）
"""

# JSON 数据
product_json = {
    'pdf_file': pdf_file,
    'model_no': model_no,
    'package_specs': package_specs,
    'customer_items': customer_items,
    'lengths': lengths,
    'products': [...]
}
```

### Step 5: Excel 填充

```python
# 建立 SKU→模具号映射
sku_to_model = {}
for product in products:
    for item in product['customer_items']:
        sku_to_model[item] = product['model_no']

# 填充 Excel
for row in ws.iter_rows(min_row=4):
    sku = row[3].value
    if sku in sku_to_model:
        row[2].value = sku_to_model[sku]  # Model 列
```

---

## ⚠️ 常见错误与排除

### 错误 1: BJ0599-XXXX 误认为模具号

**现象：** 模具号显示为 BJ0599-0001, BJ0599-0002 等

**原因：** BJ0599-XXXX 是包装规范（Package No.），不是模具号

**排除方法：**
```python
if model_no.startswith('BJ0599-'):
    # 重新提取真正的模具号
    model_no = extract_real_model_no(text)
```

### 错误 2: 客户品名误认为模具号

**现象：** 模具号与客户品名完全相同（如 GCHDMIFF, HDACFM）

**原因：** PDF 的 MODEL NO. 字段在图片中，pdftotext 读不到

**排除方法：**
```python
if model_no == customer_item:
    # 启用 OCR 重新提取
    model_no = extract_with_ocr()
```

### 错误 3: 模具号提取为空

**现象：** 模具号为 None 或空字符串

**原因：** PDF 格式特殊，文本层和 OCR 都提取失败

**排除方法：**
```python
if not model_no:
    # 使用已知映射表 fallback
    model_no = known_mappings.get(pdf_file)
```

---

## 📝 输出示例

### 产品索引.md

```markdown
# 599 客户产品知识库索引

**总计：** 58 个产品

**数据结构：** 模具号 → 客户品名 → 长度 + 包装规范

| 序号 | PDF 文件 | 模具号 | 包装规范 | 客户品名 | 长度 |
|------|----------|--------|----------|----------|------|
| 1 | 599-001.pdf | GCHDMIFF | BJ0599-0001 | GCHDMIFF | N/A |
| 8 | 599-008.pdf | OP-HD31 | BJ0599-0009 | 8K-A-30F-HDMI-CABLE | 9150mm |
```

### 产品详细数据.json

```json
{
  "pdf_file": "599-008.pdf",
  "model_no": "OP-HD31",
  "package_specs": ["BJ0599-0009"],
  "customer_items": ["8K-A-30F-HDMI-CABLE", "8K-A-50F-HDMI-CABLE"],
  "lengths": ["9150mm", "15250mm"],
  "products": [
    {
      "customer_item": "8K-A-30F-HDMI-CABLE",
      "length": "9150mm",
      "package_spec": "BJ0599-0009"
    }
  ]
}
```

---

## 🔍 模具号规律参考

| 系列 | 格式 | 示例 | 数量 |
|------|------|------|------|
| AD 系列 | AD + 4 位数字 + 短横线 + 2-3 位 | AD1002-005, AD1008 | 4 个 |
| 5001 系列 | 5001 + 短横线 + 3 位数字 + 字母 | 5001-125A, 5001-130A | 9 个 |
| 5004 系列 | 5004 + 短横线 + 1-3 位 + 字母 | 5004-6A, 5004-65A | 3 个 |
| OP 系列 | OP + 短横线 + 2 位字母 + 2 位数字 | OP-HD31, OP-USB09 | 4 个 |
| AP 系列 | AP + 短横线 + 3 位数字 + 字母 | AP-073A, AP-079A | 2 个 |
| DP 系列 | DP + 短横线 + 3 位数字 + 字母 | DP-033A, DP-034A | 5 个 |

---

## 📦 依赖安装

```bash
# 系统依赖
brew install poppler  # pdftotext, pdftoppm

# Python 依赖
pip3 install docling openpyxl
```

---

## 🧪 测试命令

```bash
# 测试单个 PDF
python3 scripts/extract.py \
  --pdf-dir "/path/to/599" \
  --output-dir "./output" \
  --verbose

# 验证输出
cat output/产品索引.md
cat output/产品详细数据.json | python3 -m json.tool
```

---

## 📚 相关文档

- [Docling 文档](https://ds4sd.github.io/docling/)
- [pdftotext 手册](https://linux.die.net/man/1/pdftotext)
- [OpenPyXL 文档](https://openpyxl.readthedocs.io/)

---

**版本历史：**
- v1.0 (2026-03-23) — 初始版本，支持 PDF 批量提取、错误排除、知识库生成
