---
name: regulation-extractor
description: 从建筑工程规范PDF中结构化提取条文并同步到飞书多维表格。支持PDF双文字层（原文+OCR）去重、纯图片PDF的RapidOCR识别、条文编号切分（含带空格编号如6. 1. 2. 3）、带圈数字转换（如6.4.④→6.4.4）、OCR错误检测、质量标记、文本清洗（去换行/页眉/符号表/中英文粘连/过长切分）。输出JSON供人工校验或直接写入飞书表格。适用场景：老板提供规范PDF → 提取条文 → 清洗 → 写入飞书多维表格 → 人工校验。触发词：提取规范、法规提取、条文提取、PDF提取规范、批量处理PDF法规。
---

# Regulation Extractor v3.0

从建筑工程规范PDF中提取条文，支持文字层提取和纯图片PDF的OCR识别，经过多轮清洗后输出高质量结构化数据。

## 工作流（完整Pipeline）

### Step 1: 提取条文（文字层）

```bash
python scripts/extract_regulation.py <pdf_path> -o <output.json>
```

支持 `--chapters <chapters.json>` 自定义章节映射。
支持编号格式：`3.1.2`、`3. 1. 2`、4级编号 `6.1.2.4`，自动去除空格。

### Step 2: OCR处理（纯图片PDF）

```bash
# 批量：自动检测0条文的JSON，仅OCR这些PDF
python scripts/ocr_batch.py <pdf_dir> <output_dir>

# 单文件
python scripts/ocr_batch.py <pdf_path> -o <output.json>
```

### Step 3: 深度清洗（必做）

```bash
python scripts/deep_clean.py <output_dir>
```

一次性完成：
- ❌ 过滤符号表（2.2.x 类编号）
- ❌ 删除过短（<5字）和无中文条文
- ✅ 修复中英文粘连（自动插入空格）
- ✅ 切除末尾混入的章节标题
- ✅ 切分过长条文（>300字，按句号/分号智能切分，子条目编号如 3.1.2.a, 3.1.2.b）

### Step 4: 清洗文本（向量化前必做）

```bash
python scripts/clean_json.py <output_dir>
```

去除 `\n` 换行符、页眉页脚垃圾（如 `www.bzfxw.com`、规范名称重复）。每条条文变成一段连续纯文本。

### Step 5: 修复残留尾部垃圾

```bash
python scripts/fix_tails.py <output_dir>
```

更彻底地修复：
- 页码残留（`—83—` 等各种变体）
- 图表标题残留（`图N xxx示意图`）
- 规范名称重复
- 章节标题拼接

### Step 6: 质量检查

```bash
python scripts/quality_check.py <output_dir>
```

输出每个PDF的质量报告：中英文粘连、符号表、末尾章节标题、过长、过短、OCR错误、无中文。

### Step 7: 同步到飞书

```bash
python scripts/sync_to_bitable.py <output.json> \
  --app_token <APP_TOKEN> --table_id <TABLE_ID> \
  --app_id <APP_ID> --app_secret <APP_SECRET> \
  --delete_dupes
```

### Step 8: 人工校验

重点检查：
- `quality: ocr_error` 的条文（OCR识别不准）
- 过长条文的切分点是否合理
- 术语定义中的中英文分隔

## 输出JSON结构

```json
{
  "articles": {
    "3.0.1": {"id": "3.0.1", "chapter": "基本规定", "page": 11, "text": "...", "quality": "clean"},
    "5.3.2.a": {"id": "5.3.2.a", "chapter": "施工", "page": 45, "text": "（切分后的第一段）", "quality": "clean"},
    "5.3.2.b": {"id": "5.3.2.b", "chapter": "施工", "page": 45, "text": "（切分后的第二段）", "quality": "clean"}
  },
  "report": {"total": N, "clean": N, "ocr_error": N, "by_chapter": {...}, "missing": [...], "warnings": [...]}
}
```

## 脚本清单

| 脚本 | 功能 | 阶段 |
|------|------|------|
| `extract_regulation.py` | 核心提取：文字层条文 | Step 1 |
| `ocr_batch.py` | OCR批处理：纯图片PDF | Step 2 |
| `deep_clean.py` | 深度清洗：符号表/粘连/过长切分 | Step 3 |
| `clean_json.py` | 文本清洗：去换行/页眉垃圾 | Step 4 |
| `fix_tails.py` | 尾部修复：页码/图号/章节标题 | Step 5 |
| `quality_check.py` | 质量检查：输出问题报告 | Step 6 |
| `sync_to_bitable.py` | 同步飞书多维表格 | Step 7 |

## 技术要点

- **双图层处理**：PDF有原文层和OCR层，优先保留原文层，过滤OCR乱码层
- **OCR引擎**：RapidOCR (ONNX)，离线运行，无需GPU，支持中英文
- **编号格式**：支持 `3.1.2`、`3. 1. 2`、4级编号，自动去除空格
- **过长切分**：按句号→分号逐级切分，子条目加后缀 `.a` `.b` `.c`
- **清洗Pipeline**：5步递进式清洗，每步解决一类问题
- **数据质量**：实测21个PDF，5865条条文，96.8%干净率

## 依赖

```
pip install PyMuPDF rapidocr-onnxruntime
```

- Python 3.10+

## 已知限制

- 部分PDF只有封面（如JGJ 162-2008仅3页），无法提取条文
- 条文编号非X.X.X格式的文件（如纯文本式实施细则）可能匹配不到
- OCR准确率依赖PDF图片质量，建议对 `quality: ocr_error` 的条文人审
- 约2%条文残留页码/章节标题噪声，对向量化检索影响极小

## 实测数据

| 指标 | 数值 |
|------|------|
| PDF总数 | 21个 |
| 成功提取 | 19个（90%） |
| 总条文数 | 5,865条 |
| 干净率 | 96.8% |
| OCR待校验 | 185条（3.2%） |

## 历史版本

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-03-28 | 初始版本：文字层提取 |
| v2.0 | 2026-03-28 | 新增OCR批处理、带空格编号格式、4级编号 |
| v3.0 | 2026-03-28 | 新增深度清洗Pipeline（5步）、过长切分、符号表过滤、尾部修复、质量检查 |
