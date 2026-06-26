# 📊 报价单模板 V2 对比

**生成时间：** 2026-03-14 17:49  
**版本：** V2（统一结构）

---

## 📁 生成文件

```
examples/
├── QT-20260314-011-ExcelV2.xlsx    (6.8KB)   📗 Excel V2
└── QT-20260314-011-HTMLv2.html      (13KB)    🌐 HTML V2
```

---

## ✅ V2 改进点

### 1. HTML V2 改进

| 项目 | V1 | V2 |
|------|------|------|
| **Total Amount 宽度** | 固定宽度（可能太小） | 全宽占满 ✅ |
| **字体大小** | 正常 | 加大（text-3xl）✅ |
| **视觉层次** | 一般 | 更清晰 ✅ |
| **打印优化** | 基础 | 增强 ✅ |

**关键改动：**
```html
<!-- V1 -->
<div class="w-full md:w-1/2 lg:w-1/3 ...">

<!-- V2 -->
<div class="w-full ...">  <!-- 全宽！ -->
```

---

### 2. Excel V2 改进

| 项目 | V1 | V2 |
|------|------|------|
| **结构** | 杂乱 | 参考 HTML，清晰 ✅ |
| **颜色** | 不统一 | 与 HTML 一致 ✅ |
| **列宽** | 不合理 | 优化后 ✅ |
| **打印设置** | 无 | 完整（A4/边距/适配）✅ |
| **产品规格** | 单行 | 多行列表（易读）✅ |
| **总计区域** | 窄 | 全宽（与 HTML 一致）✅ |

**关键改动：**
- ✅ 统一颜色方案（slate-900, teal-600, slate-50）
- ✅ 优化列宽（Description 50，其他合理）
- ✅ 产品规格用 bullet points（• 项目）
- ✅ 总计区域全宽，视觉突出
- ✅ 添加完整打印设置

---

## 🎨 结构对比

### HTML 结构

```
1. Header（公司信息 + 报价单号）
   └─ 左：公司名/联系信息
   └─ 右：QUOTATION 标题/Quote No/Date/Valid Until

2. 客户信息 + 贸易条款（两列）
   └─ 左：Prepared For（客户信息）
   └─ 右：Trade Terms（Incoterms/Currency/Lead Time）

3. 产品表格
   └─ 表头：深色背景，白色文字
   └─ 数据行：No./Description/Qty/Unit Price/Amount

4. 总计（全宽）
   └─ Subtotal
   └─ Estimated Freight
   └─ Total (FOB) ← 最大最醒目

5. 条款 + 银行信息（两列）
   └─ 左：Terms & Conditions
   └─ 右：Bank Details

6. 签名区域（第二页）
```

### Excel V2 结构

**完全参考 HTML！** ✅

```
Row 1-6:   Header（公司信息 + 报价单号）
Row 8-12:  客户信息 + 贸易条款（两列）
Row 14:    产品表头（深色背景）
Row 15+:   产品数据
Row N:     总计（全宽，A-E 合并）
Row N+3:   条款 + 银行信息（两列）
Row N+6:   签名区域（第二页）
```

---

## 🎯 使用建议

### 发送给客户

**推荐：HTML → PDF**
```bash
# 1. 生成 HTML
python3 generate_quotation_html.py --data data.json -o QT-001.html

# 2. 浏览器打开
open QT-001.html

# 3. 按 Cmd+P → 保存为 PDF
# ✅ 勾选"背景图形"
```

**优点：**
- ⭐ 设计最美观
- ⭐ 结构清晰
- ⭐ Total 全宽醒目
- ⭐ 文件小（13KB）

---

### 内部编辑

**推荐：Excel V2**
```bash
# 1. 生成 Excel
python3 generate_quotation_v2.py --data data.json -o QT-001.xlsx

# 2. 在 Excel 中编辑
open QT-001.xlsx

# 3. 修改价格/数量（公式自动计算）

# 4. 导出 PDF（如需）
soffice --headless --convert-to pdf QT-001.xlsx
```

**优点：**
- ⭐ 可编辑
- ⭐ 公式自动计算
- ⭐ 结构与 HTML 一致
- ⭐ 打印设置完整

---

## 📊 视觉效果对比

### Total Amount 区域

| 版本 | Excel V1 | Excel V2 | HTML V1 | HTML V2 |
|------|----------|----------|---------|---------|
| **宽度** | 窄（2 列） | **全宽（4 列）** | 窄（50%） | **全宽（100%）** ✅ |
| **字体** | 12pt | **16pt** | 2xl | **3xl** ✅ |
| **颜色** | 默认黑 | **Teal 600** | Teal 600 | **Teal 600** ✅ |
| **边框** | 有 | **优化** | 有 | **优化** ✅ |

### 产品规格显示

| 版本 | Excel V1 | Excel V2 | HTML |
|------|----------|----------|------|
| **格式** | 单行逗号 | **多行 Bullet** | **多行 Bullet** ✅ |
| **可读性** | 一般 | **优秀** ✅ | **优秀** ✅ |
| **换行** | 无 | **自动** ✅ | **自动** ✅ |

---

## 🚀 快速生成

### 一键生成（Excel V2 + HTML V2）

```bash
cd /Users/wilson/.openclaw/workspace/skills

# Excel V2
python3 excel-xlsx/scripts/generate_quotation_v2.py \
  --data quotation-workflow/examples/farreach_sample.json \
  --output quotation-workflow/examples/QT-20260314-012.xlsx

# HTML V2
python3 quotation-workflow/scripts/generate_quotation_html.py \
  --data quotation-workflow/examples/farreach_sample.json \
  --output quotation-workflow/examples/QT-20260314-012.html
```

### 导出 PDF

**从 HTML（推荐）：**
```bash
open QT-20260314-012.html
# Cmd+P → 保存为 PDF → ✅ 勾选"背景图形"
```

**从 Excel：**
```bash
soffice --headless --convert-to pdf QT-20260314-012.xlsx
```

---

## 📝 代码位置

| 脚本 | 路径 | 用途 |
|------|------|------|
| **Excel V2** | `excel-xlsx/scripts/generate_quotation_v2.py` | 生成 Excel（参考 HTML 结构） |
| **HTML V2** | `quotation-workflow/scripts/generate_quotation_html.py` | 生成 HTML（Total 全宽） |

---

## ✅ 验收清单

- [x] HTML Total Amount 全宽
- [x] HTML 字体加大（text-3xl）
- [x] Excel 结构参考 HTML
- [x] Excel 颜色统一
- [x] Excel 打印设置完整
- [x] 产品规格多行显示
- [x] 总计区域全宽醒目

---

**测试文件：** `QT-20260314-011-ExcelV2.xlsx` / `QT-20260314-011-HTMLv2.html`  
**最后更新：** 2026-03-14 17:49
