---
name: pdf
description: 当用户需要对 PDF 文件进行任何操作时，使用本技能。包括：读取或提取 PDF 中的文字/表格、合并多个 PDF、拆分 PDF、旋转页面、添加水印、创建新 PDF、填写 PDF 表单、加密/解密 PDF、提取图片，以及对扫描版 PDF 进行 OCR 识别使其可搜索。只要用户提到 .pdf 文件或希望生成 PDF，即使用本技能。
---

# PDF 处理指南

## 工具速查

| 任务                             | 推荐库     | 说明                                          |
| -------------------------------- | ---------- | --------------------------------------------- |
| 合并 / 拆分 / 旋转 / 水印 / 加密 | pypdf      | 轻量，纯 Python                               |
| 提取文本 / 表格（结构化）        | pdfplumber | 精度高，支持坐标；                            |
| 创建排版 PDF                     | reportlab  | 支持段落、表格、样式                          |
| 扫描版 OCR / 结构化转 Markdown   | pdf-to-md  | 返回图片 + markdown；文字提取失败时的兜底方案 |

---

## pypdf — 基础操作

```python
from pypdf import PdfReader, PdfWriter

# 提取文本
reader = PdfReader("doc.pdf")
text = "".join(page.extract_text() for page in reader.pages)

# 合并
writer = PdfWriter()
for path in ["a.pdf", "b.pdf"]:
    for page in PdfReader(path).pages:
        writer.add_page(page)
with open("merged.pdf", "wb") as f:
    writer.write(f)

# 拆分（每页单独保存）
for i, page in enumerate(reader.pages):
    w = PdfWriter()
    w.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as f:
        w.write(f)

# 旋转 / 水印 / 加密 / 裁剪
page.rotate(90)
page.merge_page(PdfReader("watermark.pdf").pages[0])
writer.encrypt("user_pass", "owner_pass")
page.mediabox.left, page.mediabox.bottom, page.mediabox.right, page.mediabox.top = 50, 50, 550, 750
```

---

## pdfplumber — 文本与表格提取

```python
import pdfplumber, pandas as pd

with pdfplumber.open("doc.pdf") as pdf:
    # 文本
    text = pdf.pages[0].extract_text()
    # 表格 → DataFrame
    for t in pdf.pages[0].extract_tables():
        if t:
            df = pd.DataFrame(t[1:], columns=t[0])
    # 按坐标区域提取（左、上、右、下）
    region_text = pdf.pages[0].within_bbox((100, 100, 400, 200)).extract_text()
```

---

## 注意事项

- **中文字体**：reportlab 默认字体不含中文字形，生成含中文的 PDF 时必须先通过
  `pdfmetrics.registerFont(TTFont(...))` 注册系统中文字体（如 Noto Sans
  CJK、微软雅黑、文泉驿等），并在样式中指定该字体，否则中文会显示为乱码。

## reportlab — 创建 PDF

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("out.pdf", pagesize=letter)
styles = getSampleStyleSheet()
doc.build([
    Paragraph("标题", styles["Title"]),
    Spacer(1, 12),
    Paragraph("正文内容", styles["Normal"]),
])
```

> **下标/上标**：不要用 Unicode 字符（₀¹²），改用 XML 标签：`H<sub>2</sub>O`、`x<super>2</super>`。

---

## OCR 与常见问题

### OCR：PDF → Markdown（含图片）

> **如果用 `pypdf` 或 `pdfplumber` 提取到的文字为空、极少，或出现大量乱码，必须改用此 OCR 方案。** 扫描版 PDF、拍照 PDF、图片型 PDF 均无法通过普通文本提取获得内容，OCR 是唯一可靠手段。

```python
import sys, os
sys.path.insert(0, os.path.join(os.getenv('skill_path'), 'pdf', 'scripts'))
from pdf_to_md import parse

# 结果写入 <输出目录>/content.md，图片写入 <输出目录>/images/
parse('<PDF路径>', '<输出目录>')
```

> 适用场景：扫描版 PDF、图文混排、需要保留图片、中文内容居多。

### 其他常见问题

```python
# 处理加密 PDF
from pypdf import PdfReader
reader = PdfReader("enc.pdf")
if reader.is_encrypted:
    reader.decrypt("password")

# 提取嵌入图片
from PIL import Image
import io
for page in reader.pages:
    for img_obj in page.images:
        Image.open(io.BytesIO(img_obj.data)).save(f"{img_obj.name}.png")

# 宽容模式读取损坏 PDF
reader = PdfReader("damaged.pdf", strict=False)
```

---

# PDF高级处理参考

---

## pypdfium2 — 渲染为图片

基于 Chromium PDFium，无需 poppler 等外部依赖，适合渲染和 OCR 场景。

```python
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("doc.pdf")
for i, page in enumerate(pdf):
    bitmap = page.render(scale=2.0)   # scale=2 ≈ 192 DPI
    bitmap.to_pil().save(f"page_{i+1}.png")

# 提取文本
for i, page in enumerate(pdf):
    print(f"第 {i+1} 页：{len(page.get_text())} 字符")
```

---

## pdfplumber — 精确坐标与复杂表格

```python
import pdfplumber

with pdfplumber.open("doc.pdf") as pdf:
    page = pdf.pages[0]

    # 逐字符提取含坐标信息
    for char in page.chars[:10]:
        print(f"'{char['text']}' x:{char['x0']:.1f} y:{char['y0']:.1f}")

    # 复杂布局自定义策略
    tables = page.extract_tables({
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance": 3,
        "intersection_tolerance": 15,
    })

    # 可视化调试表格检测结果
    page.to_image(resolution=150).save("debug.png")
```

---

## reportlab — 复杂表格与多页报告

```python
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()

data = [
    ["产品", "Q1", "Q2", "Q3", "Q4"],
    ["Widget", "120", "135", "142", "158"],
    ["Gadget", "85",  "92",  "98",  "105"],
]
table = Table(data, colWidths=[120, 60, 60, 60, 60])
table.setStyle(TableStyle([
    ("BACKGROUND",     (0, 0), (-1,  0), colors.HexColor("#4472C4")),
    ("TEXTCOLOR",      (0, 0), (-1,  0), colors.white),
    ("FONTNAME",       (0, 0), (-1,  0), "Helvetica-Bold"),
    ("ALIGN",          (0, 0), (-1, -1), "CENTER"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2FF")]),
    ("GRID",           (0, 0), (-1, -1), 0.5, colors.grey),
    ("BOX",            (0, 0), (-1, -1), 1,   colors.black),
]))

doc.build([
    Paragraph("销售报告", styles["Title"]),
    table,
    PageBreak(),
    Paragraph("第二页内容", styles["Normal"]),
])
```

---

## 批量处理

```python
import glob, logging
from pypdf import PdfReader, PdfWriter

logger = logging.getLogger(__name__)

# 批量合并目录下所有 PDF
writer = PdfWriter()
for pdf_file in sorted(glob.glob("input/*.pdf")):
    try:
        for page in PdfReader(pdf_file).pages:
            writer.add_page(page)
    except Exception as e:
        logger.error(f"跳过 {pdf_file}：{e}")
with open("merged_all.pdf", "wb") as f:
    writer.write(f)
```
