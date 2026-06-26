---
name: product-doc-reader
description: '产品工程图纸结构化提取器 v5.0。pdftotext 优先 + Vision 兜底，支持软连字符清理/跨行关联/数据校验。专为 Farreach 线材产品图纸设计。'
metadata:
  {
    "openclaw": {
      "emoji": "📐",
      "version": "5.0.1",
      "requires": { "anyBins": ["python3", "pdftoppm"] }
    },
  }
---

# Product Doc Reader 📐

**产品工程图纸 → 结构化数据 (v5.0.1 修复版)**

将 PDF 格式的产品图纸自动转换为结构化 JSON 和 Markdown，专为线材/连接器产品图纸设计。

**v5.0.1 最新修复（2026-03-24）：**
- ✅ 软连字符清理（`\xad` 导致产品名断裂）
- ✅ 跨行关联优化（长度值分行问题）
- ✅ 数据校验增强（排除 BJ 编号/电气参数/线材规格）
- ✅ 599-028 修复（右上角客户品名信息栏提取）

---

## 🎯 使用场景

- 客户发来产品图纸 PDF，需要提取 BOM、规格参数
- 批量处理工程图纸，建立产品数据库
- 图纸内容归档到知识库（Obsidian/Markdown）
- 图纸比对（新旧版本 BOM 差异）
- 客户图纸适配（C331 等非福睿标准模板）
- Excel 模具号列自动填充

---

## 🏗️ 架构 (v5.0 混合策略)

```
PDF 图纸
  ├─→ pdftotext（精确文本，保留布局）⭐ 优先
  │     ├─→ 清理软连字符 \xad
  │     ├─→ BOM 物料清单（字体嵌入，100% 准确）
  │     ├─→ 产品规格矩阵（跨行关联）
  │     └─→ 字段规则识别（BJ/599-xxx/ITEM）
  │
  ├─→ pdftoppm（PDF → PNG，300 DPI）
  │     └─→ Vision API（Gemini 2.5 Flash）⭐ 兜底
  │           ├─→ 布局理解
  │           ├─→ 图形/尺寸标注
  │           ├─→ 测试要求结构化表格
  │           └─→ 多页合并
  │
  └─→ 合并策略
        ├─→ 模具号：pdftotext 优先（精确）
        ├─→ 产品名：pdftotext 优先（排除 BOM 词汇）
        ├─→ 包装规范：pdftotext 优先（BJ 精确匹配）
        ├─→ 长度：pdftotext 优先（跨行关联）
        ├─→ 测试要求：Vision 结构化表格
        └─→ 字段校验 + 置信度评分
```

### 字段识别规则

| 规则 | 示例 | 说明 |
|------|------|------|
| `BJ` + 8 位数字 | BJ0599-0002 | 包装规范（福睿内部编码） |
| `599-xxx` | 599-002 | Drawing No. / 物料编码 |
| `ITEM` 栏的值 | 5001-127A | Model No.（客户图纸常见） |
| `CUSTOMER ITEM` | HDACFM | 客人品名 |
| `MODEL NO.` | OP-DP09 | 型号（多产品图纸） |

### 数据校验规则

| 校验项 | 规则 | 示例 |
|--------|------|------|
| 模具号格式 | 必须包含字母 + 数字 | ✅ `5001-130A` ❌ `P` |
| 排除单字符 | 长度 ≤ 2 | ❌ `P`, `1` |
| 排除 BJ 开头 | 包装规范 | ❌ `BJ0599-0002` |
| 排除 599 开头 | Drawing No. | ❌ `599-002` |
| 产品名长度 | > 3 字符 | ❌ `300`, `60H` |
| 排除纯数字 | 长度值 | ❌ `9144`, `10000` |
| 排除电气参数 | 电压/频率 | ❌ `300V`, `60HZ` |
| 排除线材规格 | 导体规格 | ❌ `32BC`, `511BC` |

---

## 🔧 依赖

| 工具 | 用途 | 安装 |
|------|------|------|
| `python3` | 运行脚本 | 系统自带 |
| `pdftoppm` | PDF 转 PNG | `brew install poppler` |
| `tesseract` | OCR 备用（可选） | `brew install tesseract tesseract-lang` |

**不再依赖：** `docling`

---

## 📋 快速使用

### 基本提取（混合模式，推荐）
```bash
cd /Users/wilson/.openclaw/workspace/skills/product-doc-reader
python3 scripts/extract_hybrid.py <图纸.pdf>
# 输出到 ./output/<图纸名>.json 和 .md
```

### 输出到指定目录
```bash
python3 scripts/extract_hybrid.py <图纸.pdf> -o /path/to/output -f both
```

### 输出 JSON 到 stdout（管道使用）
```bash
python3 scripts/extract_hybrid.py <图纸.pdf> --stdout -f json
```

### 纯 Vision 模式（备用）
```bash
python3 scripts/extract_hybrid.py <图纸.pdf> --vision-only
```

### 纯文本模式（快速）
```bash
python3 scripts/extract_hybrid.py <图纸.pdf> --text-only
```

### 参数说明
| 参数 | 说明 | 默认 |
|------|------|------|
| `pdf_path` | PDF 文件路径（必填） | - |
| `-o, --output-dir` | 输出目录 | `./output` |
| `-f, --format` | 输出格式：`json` / `md` / `both` | `both` |
| `--vision-only` | 仅用 Vision API | 关闭 |
| `--text-only` | 仅用 pdftotext | 关闭 |
| `--stdout` | 输出到 stdout | 关闭 |
| `--dpi` | OCR DPI（默认 300） | `300` |

---

## 📊 输出结构

### JSON 字段
```json
{
  "product_name": "HDMI2CABLE4K6030F, HDMI2CABLE4K6010M",
  "model_no": "5001-131A",
  "drawing_no": "599-028",
  "packaging_spec": "BJ0599-0053, BJ0599-0055",
  "material_code": "599-028",
  "length_mm": "9144+50, 10000+50",
  "mold_info": "",
  "mold_number": "",
  "bom": [
    {
      "no": "①",
      "part_name": "CABLE",
      "spec": "HDMI2 4K60 30AWG...",
      "quantity": "M"
    }
  ],
  "tolerances": [
    { "range": "0.5-3.0", "hardware": "±0.05", "plastic": "±0.1" }
  ],
  "test_requirements": {
    "table": [],
    "other_tests": ["100% OPEN SHORT MISS WIRE TEST", "PASS 4K@60HZ"]
  },
  "pin_assignment": {
    "connectors": ["HDMI"],
    "description": ""
  },
  "dimensions": ["11.33±0.3", "20.8±0.3"],
  "notes": ["ROHS compliant"],
  "revision_history": [
    { "revision": "A0", "date": "2026/03/17", "description": "" }
  ],
  "company": "珠海福睿电子 FARREACH",
  "drawing_date": "2026/03/17",
  "drawn_by": "Kenny",
  "checked_by": "X.J.C",
  "approved_by": "Lin.",
  "products": [
    {
      "customer_item": "HDMI2CABLE4K6030F",
      "length_mm": "9144+50",
      "material_code": "599-028",
      "packaging_spec": "BJ0599-0053"
    }
  ],
  "source_file": "599-028.pdf",
  "extraction_method": "hybrid",
  "pages": 1,
  "confidence": 100.0,
  "warnings": []
}
```

---

## ✅ 测试结果（58 份 599 系列图纸）

| 产品类型 | 图纸数量 | 模具号范围 | 成功率 |
|----------|---------|-----------|--------|
| HDMI 转接头 | 7 | AD4001-009 ~ MB-003 | 100% |
| HDMI 线缆 | 20 | 5001-119A ~ OP-HD65 | 100% |
| DP-HDMI 转换器 | 8 | AP-073A / AP-079A | 100% |
| USB-C 转 HDMI | 3 | OP-USB09 / TP-C089B | 100% |
| DP 光纤线缆 (AOC) | 1 | OP-DP09 (7 款) | 100% |
| KVM 线缆 | 5 | DP-033A ~ 5001-127A | 100% |
| USB 转接头 | 3 | AD9017 / USB-3005A-014 | 100% |
| DP 线缆 | 1 | DP-021B | 100% |

**总计：** 58/58 (100%)

---

## ⚠️ 已知限制与优化建议

### 1. Google Drive 搜索分页
**问题：** `gog drive search "599"` 只返回 17 个结果，实际有 58 个。

**解决：** 逐个搜索 `599-001` 到 `599-058`。

### 2. 产品名提取依赖排除列表
**问题：** 需要手动添加新 BOM 词汇。

**解决：** 已添加 50+ 排除词，后续发现新词继续添加。

### 3. 批量处理无断点续传
**问题：** 58 个文件处理到一半失败，需要重来。

**建议：** 记录已处理文件列表，支持从断点继续。

### 4. 特殊模板适配
**问题：** 客户图纸（如 C331 模板）字段位置不同。

**解决：** 已支持跨行关联（上下 5 行搜索）。

### 5. 数据校验需人工审核
**问题：** 置信度 <80% 的结果需要人工检查。

**建议：** 添加自动标记功能，低置信度结果单独输出。

---

## 📁 文件结构

```
product-doc-reader/
├── SKILL.md                      ← 本文件
├── DEVELOPMENT_SUMMARY.md        ← 开发总结（踩坑记录）
├── scripts/
│   ├── extract_hybrid.py         ← v5.0.1 核心提取脚本
│   ├── batch_599_full.py         ← 批量处理脚本
│   └── batch_process_drive.py    ← Drive 批量处理
├── examples/
│   └── hybrid/                   ← 测试输出示例
└── output/                       ← 默认输出目录
```

---

## 🔄 版本历史

| 版本 | 日期 | 改进 |
|------|------|------|
| v5.0.1 | 2026-03-24 | 599-028 修复：软连字符清理/跨行关联/数据校验 |
| v5.0.0 | 2026-03-24 | pdftotext 优先 + 数据校验规则 |
| v4.0.0 | 2026-03-23 | pdftotext + Vision 混合策略 |
| v3.0.0 | 2026-03-23 | 纯 Vision API（Gemini Flash） |
| v2.0.0 | 2026-03-23 | Docling + 区域分割 + Tesseract OCR |

---

## 📞 维护者

**开发：** WILSON  
**测试：** Jaden  
**最后更新：** 2026-03-24 15:00

---

*Product Doc Reader v5.0.1 - 生产就绪 ✅*
