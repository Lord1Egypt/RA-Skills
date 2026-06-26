# 📋 报价单工作流 - 完整版

**更新时间：** 2026-03-14 18:11  
**状态：** ✅ 完全自动化

---

## 📁 一键生成所有文件

```bash
./generate-all.sh farreach_sample.json QT-20260314-001
```

**生成文件：**
```
QT-20260314-001.xlsx          (6.9KB)   Excel 源文件
QT-20260314-001.docx          (37KB)    Word 源文件
QT-20260314-001.html          (15KB)    HTML 源文件
QT-20260314-001-HTML.pdf      (290KB)   PDF（HTML 导出，推荐 ⭐）
QT-20260314-001-Excel.pdf     (161KB)   PDF（Excel 导出，备用）
```

---

## 🎯 推荐发送客户的文件

### 首选：QT-XXX-HTML.pdf ⭐

**特点：**
- ✅ 现代设计，专业美观
- ✅ Total 全宽醒目
- ✅ 颜色丰富，品牌感强
- ✅ Chrome 导出，质量最佳
- ✅ A4 尺寸，优化分页

**适合：**
- 首次报价
- 欧美客户
- 科技公司
- 注重形象的场合

---

### 备用：QT-XXX-Excel.pdf

**特点：**
- ✅ 传统工整
- ✅ 文件较小（161KB）
- ✅ 保守客户接受度高

**适合：**
- 保守行业
- 日韩客户
- 政府/国企
- 要求"简单点"的客户

---

## 🚀 快速使用

### 方式 1：一键生成（推荐）

```bash
cd /Users/wilson/.openclaw/workspace/skills/quotation-workflow

# 生成所有格式
./scripts/generate-all.sh examples/farreach_sample.json QT-20260314-001

# 完成！5 个文件全部生成
```

### 方式 2：单独生成 HTML PDF

```bash
# 生成 HTML
python3 scripts/generate_quotation_html.py \
  --data examples/farreach_sample.json \
  --output examples/QT-001.html

# 导出 PDF
./scripts/html2pdf.sh examples/QT-001.html
```

### 方式 3：单独生成 Excel PDF

```bash
# 生成 Excel
python3 ../excel-xlsx/scripts/generate_quotation_traditional.py \
  --data examples/farreach_sample.json \
  --output examples/QT-001.xlsx

# 导出 PDF
soffice --headless --convert-to pdf examples/QT-001.xlsx
```

---

## 📊 文件对比

| 文件 | 大小 | 质量 | 推荐场景 |
|------|------|------|----------|
| **QT-XXX-HTML.pdf** | 290KB | ⭐⭐⭐⭐⭐ | 首次报价/现代客户 ⭐ |
| **QT-XXX-Excel.pdf** | 161KB | ⭐⭐⭐⭐ | 保守客户/备用 |
| QT-XXX.html | 15KB | N/A | 在线预览 |
| QT-XXX.xlsx | 6.9KB | N/A | 内部编辑 |
| QT-XXX.docx | 37KB | N/A | 备用 |

---

## 🎨 HTML vs Excel PDF 对比

### 视觉

| 维度 | HTML PDF | Excel PDF |
|------|----------|-----------|
| **设计** | 现代时尚 | 传统工整 |
| **颜色** | 丰富（品牌色） | 单调（黑白） |
| **Total** | 全宽醒目 | 标准 |
| **印象** | 专业团队 | 普通供应商 |

### 技术

| 维度 | HTML PDF | Excel PDF |
|------|----------|-----------|
| **页数** | 2 页（优化后） | 2 页 |
| **尺寸** | A4（210×297mm） | A4（210×297mm） |
| **边距** | 10mm（优化） | 7.6mm（默认） |
| **导出** | Chrome（高质量） | LibreOffice |

---

## ✅ 验证清单

生成后检查：

- [ ] HTML PDF 是 2 页（不是 3 页）
- [ ] Excel PDF 是 2 页
- [ ] Total 金额清晰可见
- [ ] 所有产品完整显示
- [ ] 无内容被切断
- [ ] 背景颜色正确
- [ ] 文字清晰

---

## 📧 发送邮件示例

```
Subject: Quotation QT-20260314-001 - Farreach Electronic

Dear [Customer Name],

Thank you for your inquiry.

Please find attached our quotation for your review.

Product Summary:
• HDMI 2.1 Ultra High Speed Cable (8K@60Hz, 48Gbps)
• HDMI 2.1 Fiber Optical Cable (AOC, 10m)
• USB-C to USB-C Cable (USB 4.0, 80Gbps, 100W PD)
• DisplayPort 2.1 Cable (UHBR20, 80Gbps)
• CAT6A Ethernet Cable (10Gbps, 500MHz)

Total: USD $31,690.00 (FOB Shenzhen)

Should you need any clarification, please feel free to contact us.

Best regards,
[Your Name]
Sales Manager
Farreach Electronic Co., Ltd.
📧 sale@farreach-electronic.com
🌐 www.farreach-electronic.com
```

**附件：** `QT-20260314-001-HTML.pdf` ⭐

---

## 🛠️ 脚本位置

| 脚本 | 路径 | 用途 |
|------|------|------|
| **一键生成** | `scripts/generate-all.sh` | Excel+Word+HTML+双 PDF |
| **HTML 生成** | `scripts/generate_quotation_html.py` | 生成 HTML |
| **HTML 转 PDF** | `scripts/html2pdf.sh` | HTML → PDF（Chrome） |
| **Excel 生成** | `../excel-xlsx/scripts/generate_quotation_traditional.py` | 传统 Excel |

---

## 💡 最佳实践

### 默认流程

```bash
# 1. 一键生成
./generate-all.sh data.json QT-001

# 2. 打开 HTML PDF 检查
open QT-001-HTML.pdf

# 3. 发送给客户
# 附件：QT-001-HTML.pdf ✅
```

### 如果客户说"太花哨"

```bash
# 发送 Excel PDF
# 附件：QT-001-Excel.pdf
```

### 如果客户需要编辑

```bash
# 发送 Excel 源文件
# 附件：QT-001.xlsx
# 邮件注明："Excel version for your reference"
```

---

## ⚠️ 注意事项

### PDF 页数问题
- HTML 设计为 2 页
- 如果变成 3 页，检查：
  - 产品数量是否太多
  - 规格文字是否过长
  - Chrome 打印设置是否正确

### 文件大小
- HTML PDF ~290KB（正常）
- Excel PDF ~160KB（正常）
- 邮件附件完全没问题

### 颜色问题
- 如果 PDF 没有背景色：
  - Chrome 导出时已自动优化
  - 如手动打印，需勾选"背景图形"

---

**最后更新：** 2026-03-14 18:11  
**维护者：** WILSON
