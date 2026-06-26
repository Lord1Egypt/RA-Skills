---
name: pdf-ppt-docx-xlsx
description: "文档格式转换工具集，支持 PDF、PPTX、DOCX、XLSX 四种格式之间的互转及衍生操作（转图片、合并、拆分、提取文本/表格、加水印等）。当用户需要转换文档格式、处理 PDF、操作 Office 文件时使用此技能。"
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["python","pip"]},"install":[{"id":"pip","kind":"pip","packages":["PyMuPDF","pdf2docx","python-docx","python-pptx","openpyxl","pandas","Pillow","pdfplumber"],"label":"安装文档处理依赖 (pip)"}]}}
---

# PDF / PPTX / DOCX / XLSX 文档转换工具集

四大办公文档格式的转换、提取、合并、拆分工具。基于 Python 生态，所有操作均可通过 `execute_command` 执行 Python 一行命令或短脚本完成。

## 依赖安装

```bash
pip install PyMuPDF pdf2docx python-docx python-pptx openpyxl pandas Pillow pdfplumber
```

部分操作（DOCX→PDF、PPTX→PDF、XLSX→PDF）需要系统安装 **LibreOffice**：

```bash
# Windows (winget)
winget install LibreOffice.LibreOffice

# macOS
brew install --cask libreoffice

# Ubuntu/Debian
sudo apt install libreoffice
```

PDF 转图片如需高质量渲染，可选装 poppler（`PyMuPDF` 内置渲染已足够，poppler 仅作为备选）。

---

## 快速参考：支持的全部转换

| 源格式 | 目标格式 | 推荐库 | 备注 |
|--------|----------|--------|------|
| PDF | 图片 (PNG/JPG) | PyMuPDF | 逐页渲染，支持 DPI 控制 |
| PDF | DOCX | pdf2docx | 保留布局、表格、图片 |
| PDF | PPTX | PyMuPDF + python-pptx | 每页一张幻灯片 |
| PDF | XLSX | pdfplumber + openpyxl | 提取表格数据 |
| PDF | 文本 (TXT) | PyMuPDF | 提取纯文本 |
| DOCX | PDF | LibreOffice (CLI) | 最佳保真度 |
| DOCX | PPTX | python-docx + python-pptx | 段落→幻灯片 |
| DOCX | HTML | python-docx / mammoth | 保留基本格式 |
| DOCX | 纯文本 | python-docx | 提取所有段落文本 |
| PPTX | PDF | LibreOffice (CLI) | 最佳保真度 |
| PPTX | 图片 (PNG) | PyMuPDF | 每页导出为图片 |
| PPTX | DOCX | python-pptx + python-docx | 提取所有文本 |
| PPTX | 纯文本 | python-pptx | 提取幻灯片文本 |
| XLSX | PDF | LibreOffice (CLI) | 最佳保真度 |
| XLSX | CSV | pandas | 可指定 sheet |
| XLSX | DOCX | openpyxl + python-docx | 表格写入 Word |
| XLSX | JSON | pandas | 结构化数据导出 |
| 图片 | PDF | Pillow + reportlab | 多图合并为 PDF |

---

## 转换命令详解

### 1. PDF → 图片

```bash
python -c "
import fitz, sys, os
pdf_path, out_dir = sys.argv[1], sys.argv[2] if len(sys.argv)>2 else '.'
os.makedirs(out_dir, exist_ok=True)
doc = fitz.open(pdf_path)
dpi = int(sys.argv[3]) if len(sys.argv)>3 else 200
fmt = sys.argv[4] if len(sys.argv)>4 else 'png'
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=dpi)
    out = os.path.join(out_dir, f'page_{i+1:04d}.{fmt}')
    pix.save(out)
    print(f'Saved: {out}')
doc.close()
print(f'Done: {len(doc)} pages -> {out_dir}')
" "input.pdf" "./output_images" 200 png
```

**参数说明：**
- `arg1` — PDF 文件路径
- `arg2` — 输出目录（默认当前目录）
- `arg3` — DPI 分辨率（默认 200，推荐 150~300）
- `arg4` — 图片格式：`png`（默认）或 `jpg`

### 2. PDF → DOCX

```bash
python -c "
from pdf2docx import Converter
import sys
cv = Converter(sys.argv[1])
cv.convert(sys.argv[2] if len(sys.argv)>2 else 'output.docx')
cv.close()
print('Done')
" "input.pdf" "output.docx"
```

**可选参数（通过修改脚本）：**
- `start=0, end=None` — 指定页码范围
- `multi_processing=True` — 多进程加速大文件

### 3. PDF → PPTX（每页一张幻灯片）

```bash
python -c "
import fitz, sys
from pptx import Presentation
from pptx.util import Inches
from pptx.dml.color import RGBColor
import io

pdf_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv)>2 else 'output.pptx'
doc = fitz.open(pdf_path)
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]  # blank
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=200)
    img_data = pix.tobytes('png')
    slide = prs.slides.add_slide(blank_layout)
    slide.shapes.add_picture(io.BytesIO(img_data), Inches(0), Inches(0),
                             width=prs.slide_width, height=prs.slide_height)
    print(f'Page {i+1}/{len(doc)} added')

prs.save(out_path)
doc.close()
print(f'Done: {out_path}')
" "input.pdf" "output.pptx"
```

### 4. PDF → XLSX（提取表格）

```bash
python -c "
import pdfplumber, openpyxl, sys

pdf_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv)>2 else 'output.xlsx'
wb = openpyxl.Workbook()
ws_total = wb.active
ws_total.title = 'All Tables'
row_offset = 0

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for t_idx, table in enumerate(tables):
            if row_offset == 0 and t_idx == 0:
                ws = ws_total
            else:
                ws = wb.create_sheet(title=f'p{page_num+1}_t{t_idx+1}')
            for row in table:
                ws.append(row)
            row_offset += len(table)
            print(f'Page {page_num+1}, Table {t_idx+1}: {len(table)} rows')

if ws_total.max_row == 1 and ws_total.max_column == 1:
    wb.remove(ws_total)

wb.save(out_path)
print(f'Done: {out_path}')
" "input.pdf" "output.xlsx"
```

### 5. PDF → 纯文本

```bash
python -c "
import fitz, sys
doc = fitz.open(sys.argv[1])
out_path = sys.argv[2] if len(sys.argv)>2 else 'output.txt'
with open(out_path, 'w', encoding='utf-8') as f:
    for i, page in enumerate(doc):
        text = page.get_text()
        f.write(f'--- Page {i+1} ---\n{text}\n\n')
print(f'Done: {len(doc)} pages extracted')
doc.close()
" "input.pdf" "output.txt"
```

### 6. DOCX → PDF

```bash
# Windows
python -c "
import subprocess, sys, os
docx_path = os.path.abspath(sys.argv[1])
out_dir = os.path.dirname(docx_path)
subprocess.run([
    r'C:\Program Files\LibreOffice\program\soffice.exe',
    '--headless', '--convert-to', 'pdf',
    '--outdir', out_dir, docx_path
], check=True)
print(f'Done')
" "input.docx"

# macOS / Linux
soffice --headless --convert-to pdf --outdir ./ "input.docx"
```

### 7. DOCX → PPTX

```bash
python -c "
from docx import Document
from pptx import Presentation
from pptx.util import Pt, Inches
import sys

docx_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv)>2 else 'output.pptx'
doc = Document(docx_path)
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

slide = None
bullet_count = 0
max_bullets = 8

for para in doc.paragraphs:
    text = para.text.strip()
    if not text:
        continue
    style = para.style.name.lower()
    is_heading = 'heading' in style or 'title' in style

    if is_heading or bullet_count >= max_bullets:
        slide = prs.slides.add_slide(blank_layout)
        bullet_count = 0
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.5),
                                          Inches(12.333), Inches(6.5))
        tf = txBox.text_frame
        tf.word_wrap = True
        if is_heading:
            p = tf.paragraphs[0]
            p.text = text
            p.font.size = Pt(32)
            p.font.bold = True
            bullet_count = 0
            continue

    if slide is None:
        slide = prs.slides.add_slide(blank_layout)
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.5),
                                          Inches(12.333), Inches(6.5))
        tf = txBox.text_frame
        tf.word_wrap = True

    p = tf.add_paragraph()
    p.text = text
    p.font.size = Pt(20)
    p.level = min(para.style.name.count('Heading') if 'Heading' in para.style.name else 0, 2)
    bullet_count += 1

prs.save(out_path)
print(f'Done: {len(prs.slides)} slides -> {out_path}')
" "input.docx" "output.pptx"
```

### 8. DOCX → HTML

```bash
python -c "
from docx import Document
from docx.oxml.ns import qn
import sys, re

doc = Document(sys.argv[1])
out_path = sys.argv[2] if len(sys.argv)>2 else 'output.html'

def paragraph_to_html(para):
    text = para.text
    style = para.style.name.lower()
    if 'heading 1' in style or 'title' in style:
        return f'<h1>{text}</h1>'
    elif 'heading 2' in style:
        return f'<h2>{text}</h2>'
    elif 'heading 3' in style:
        return f'<h3>{text}</h3>'
    elif 'list' in style:
        return f'<li>{text}</li>'
    else:
        return f'<p>{text}</p>'

html_parts = ['<!DOCTYPE html><html><head><meta charset=\"utf-8\"><style>body{font-family:sans-serif;max-width:800px;margin:2em auto;padding:0 1em;}h1{color:#333;}h2{color:#555;border-bottom:1px solid #eee;}</style></head><body>']
for para in doc.paragraphs:
    if para.text.strip():
        html_parts.append(paragraph_to_html(para))
html_parts.append('</body></html>')

with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_parts))
print(f'Done: {out_path}')
" "input.docx" "output.html"
```

### 9. PPTX → PDF

```bash
# Windows
python -c "
import subprocess, sys, os
pptx_path = os.path.abspath(sys.argv[1])
out_dir = os.path.dirname(pptx_path)
subprocess.run([
    r'C:\Program Files\LibreOffice\program\soffice.exe',
    '--headless', '--convert-to', 'pdf',
    '--outdir', out_dir, pptx_path
], check=True)
print('Done')
" "input.pptx"

# macOS / Linux
soffice --headless --convert-to pdf --outdir ./ "input.pptx"
```

### 10. PPTX → 图片

```bash
python -c "
import fitz, sys, os
pptx_path = sys.argv[1]
out_dir = sys.argv[2] if len(sys.argv)>2 else '.'
os.makedirs(out_dir, exist_ok=True)

# 先用 LibreOffice 转为 PDF，再用 PyMuPDF 渲染
import subprocess, tempfile
tmp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
tmp.close()
subprocess.run([
    r'C:\Program Files\LibreOffice\program\soffice.exe',
    '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(tmp.name),
    pptx_path
], check=True, capture_output=True)
# LibreOffice 输出文件名基于输入文件名
pdf_tmp = os.path.join(os.path.dirname(tmp.name),
                        os.path.splitext(os.path.basename(pptx_path))[0] + '.pdf')

doc = fitz.open(pdf_tmp)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=200)
    out = os.path.join(out_dir, f'slide_{i+1:04d}.png')
    pix.save(out)
    print(f'Saved: {out}')
doc.close()
os.unlink(pdf_tmp)
print(f'Done: {len(doc)} slides')
" "input.pptx" "./slides_output"
```

> **注意**：macOS/Linux 下将 `soffice.exe` 路径替换为 `soffice`。

### 11. PPTX → DOCX（提取文本）

```bash
python -c "
from pptx import Presentation
from docx import Document
from docx.shared import Pt
import sys

pptx_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv)>2 else 'output.docx'
prs = Presentation(pptx_path)
doc = Document()

for i, slide in enumerate(prs.slides):
    doc.add_heading(f'Slide {i+1}', level=1)
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                text = para.text.strip()
                if text:
                    p = doc.add_paragraph(text)
                    p.style.font.size = Pt(11)
        if shape.has_table:
            table = shape.table
            rows = []
            for row in table.rows:
                rows.append([cell.text for cell in row.cells])
            t = doc.add_table(rows=len(rows), cols=len(rows[0]) if rows else 0)
            for r_idx, row_data in enumerate(rows):
                for c_idx, cell_text in enumerate(row_data):
                    t.cell(r_idx, c_idx).text = cell_text
    doc.add_page_break()

doc.save(out_path)
print(f'Done: {len(prs.slides)} slides -> {out_path}')
" "input.pptx" "output.docx"
```

### 12. XLSX → PDF

```bash
# Windows
python -c "
import subprocess, sys, os
xlsx_path = os.path.abspath(sys.argv[1])
out_dir = os.path.dirname(xlsx_path)
subprocess.run([
    r'C:\Program Files\LibreOffice\program\soffice.exe',
    '--headless', '--convert-to', 'pdf',
    '--outdir', out_dir, xlsx_path
], check=True)
print('Done')
" "input.xlsx"

# macOS / Linux
soffice --headless --convert-to pdf --outdir ./ "input.xlsx"
```

### 13. XLSX → CSV

```bash
python -c "
import pandas as pd, sys, os
xlsx_path = sys.argv[1]
out_dir = sys.argv[2] if len(sys.argv)>2 else '.'
os.makedirs(out_dir, exist_ok=True)
xls = pd.ExcelFile(xlsx_path)
for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    out = os.path.join(out_dir, f'{sheet}.csv')
    df.to_csv(out, index=False, encoding='utf-8-sig')
    print(f'Saved: {out} ({len(df)} rows)')
print('Done')
" "input.xlsx" "./csv_output"
```

### 14. XLSX → JSON

```bash
python -c "
import pandas as pd, json, sys, os
xlsx_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv)>2 else 'output.json'
xls = pd.ExcelFile(xlsx_path)
result = {}
for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    result[sheet] = df.to_dict(orient='records')
    print(f'Sheet \"{sheet}\": {len(df)} rows')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)
print(f'Done: {out_path}')
" "input.xlsx" "output.json"
```

### 15. XLSX → DOCX（表格写入 Word）

```bash
python -c "
import openpyxl, sys
from docx import Document
from docx.shared import Inches, Pt

xlsx_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv)>2 else 'output.docx'
wb = openpyxl.load_workbook(xlsx_path)
doc = Document()

for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    doc.add_heading(sheet_name, level=1)
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        continue
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx, c_idx)
            cell.text = str(val) if val is not None else ''
            if r_idx == 0:
                for run in cell.paragraphs[0].runs:
                    run.font.bold = True
                    run.font.size = Pt(10)
    doc.add_page_break()

doc.save(out_path)
print(f'Done: {len(wb.sheetnames)} sheets -> {out_path}')
" "input.xlsx" "output.docx"
```

### 16. 图片 → PDF

```bash
python -c "
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import sys, os, io

img_dir = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv)>2 else 'output.pdf'
files = sorted([f for f in os.listdir(img_dir)
                if f.lower().endswith(('.png','.jpg','.jpeg','.webp','.bmp'))])

c = canvas.Canvas(out_path, pagesize=A4)
w, h = A4

for f in files:
    img = Image.open(os.path.join(img_dir, f))
    iw, ih = img.size
    scale = min(w/iw, h/ih, 1)
    dw, dh = iw*scale, ih*scale
    x, y = (w-dw)/2, (h-dh)/2
    c.drawImage(os.path.join(img_dir, f), x, y, dw, dh)
    c.showPage()
    print(f'Added: {f}')

c.save()
print(f'Done: {len(files)} images -> {out_path}')
" "./images" "output.pdf"
```

---

## PDF 高级操作

### 合并 PDF

```bash
python -c "
import fitz, sys, glob
files = sorted(glob.glob(sys.argv[1]))
out_path = sys.argv[2] if len(sys.argv)>2 else 'merged.pdf'
merged = fitz.open()
for f in files:
    doc = fitz.open(f)
    merged.insert_pdf(doc)
    doc.close()
    print(f'Merged: {f}')
merged.save(out_path)
merged.close()
print(f'Done: {len(files)} files -> {out_path}')
" "./*.pdf" "merged.pdf"
```

### 拆分 PDF

```bash
python -c "
import fitz, sys, os
pdf_path = sys.argv[1]
out_dir = sys.argv[2] if len(sys.argv)>2 else './split'
os.makedirs(out_dir, exist_ok=True)
doc = fitz.open(pdf_path)
for i, page in enumerate(doc):
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=i, to_page=i)
    out = os.path.join(out_dir, f'page_{i+1:04d}.pdf')
    new_doc.save(out)
    new_doc.close()
    print(f'Saved: {out}')
doc.close()
print(f'Done: {len(doc)} pages split')
" "input.pdf" "./split"
```

### 按页码范围拆分

```bash
python -c "
import fitz, sys
pdf_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv)>2 else 'extracted.pdf'
ranges = sys.argv[3]  # e.g. '1-3,5,7-10'

def parse_ranges(s):
    result = []
    for part in s.split(','):
        part = part.strip()
        if '-' in part:
            a, b = part.split('-')
            result.extend(range(int(a)-1, int(b)))
        else:
            result.append(int(part)-1)
    return result

pages = parse_ranges(ranges)
doc = fitz.open(pdf_path)
new_doc = fitz.open()
new_doc.insert_pdf(doc, from_page=min(pages), to_page=max(pages))
# 如果不是连续页码，逐页插入更精确
if pages != list(range(min(pages), max(pages)+1)):
    new_doc = fitz.open()
    for p in sorted(set(pages)):
        new_doc.insert_pdf(doc, from_page=p, to_page=p)
new_doc.save(out_path)
new_doc.close()
doc.close()
print(f'Done: pages {ranges} -> {out_path}')
" "input.pdf" "extracted.pdf" "1-3,5,7-10"
```

### PDF 加水印

```bash
python -c "
import fitz, sys

pdf_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv)>2 else 'watermarked.pdf'
text = sys.argv[3] if len(sys.argv)>3 else 'CONFIDENTIAL'
opacity = float(sys.argv[4]) if len(sys.argv)>4 else 0.3

doc = fitz.open(pdf_path)
for page in doc:
    # 计算页面中心
    rect = page.rect
    x, y = rect.width / 2, rect.height / 2
    # 旋转 -45 度
    rc = fitz.Rect(0, 0, rect.width, rect.height)
    page.insert_textbox(
        fitz.Rect(x - 200, y - 30, x + 200, y + 30),
        text, fontsize=50, color=(0.5, 0.5, 0.5),
        rotate=-45, opacity=opacity,
        fontname='helv', align=1
    )
    print(f'Watermarked page {page.number + 1}')

doc.save(out_path)
doc.close()
print(f'Done: {out_path}')
" "input.pdf" "watermarked.pdf" "机密文件" 0.2
```

### PDF 提取图片

```bash
python -c "
import fitz, sys, os
pdf_path = sys.argv[1]
out_dir = sys.argv[2] if len(sys.argv)>2 else './extracted_images'
os.makedirs(out_dir, exist_ok=True)
doc = fitz.open(pdf_path)
count = 0
for page_num, page in enumerate(doc):
    images = page.get_images(full=True)
    for img_idx, img in enumerate(images):
        xref = img[0]
        base = doc.extract_image(xref)
        ext = base['ext']
        out = os.path.join(out_dir, f'p{page_num+1}_img{img_idx+1}.{ext}')
        with open(out, 'wb') as f:
            f.write(base['image'])
        count += 1
        print(f'Extracted: {out}')
doc.close()
print(f'Done: {count} images extracted')
" "input.pdf" "./extracted_images"
```

---

## DOCX 高级操作

### 合并 DOCX

```bash
python -c "
from docx import Document
from docx.oxml.ns import qn
import sys, glob, os

files = sorted(glob.glob(sys.argv[1]))
out_path = sys.argv[2] if len(sys.argv)>2 else 'merged.docx'

if os.path.exists(out_path):
    merged = Document(out_path)
else:
    merged = Document()

for i, f in enumerate(files):
    if i == 0 and not os.path.exists(out_path):
        continue
    doc = Document(f)
    for element in doc.element.body:
        merged.element.body.append(element)
    print(f'Merged: {f}')

merged.save(out_path)
print(f'Done: {len(files)} files -> {out_path}')
" "./*.docx" "merged.docx"
```

### DOCX 提取图片

```bash
python -c "
from docx import Document
import sys, os, zipfile

docx_path = sys.argv[1]
out_dir = sys.argv[2] if len(sys.argv)>2 else './docx_images'
os.makedirs(out_dir, exist_ok=True)

with zipfile.ZipFile(docx_path, 'r') as z:
    for name in z.namelist():
        if name.startswith('word/media/'):
            out = os.path.join(out_dir, os.path.basename(name))
            with open(out, 'wb') as f:
                f.write(z.read(name))
            print(f'Extracted: {out}')

print('Done')
" "input.docx" "./docx_images"
```

---

## XLSX 高级操作

### 合并 XLSX（按 sheet 名合并）

```bash
python -c "
import pandas as pd, sys, glob

files = sorted(glob.glob(sys.argv[1]))
out_path = sys.argv[2] if len(sys.argv)>2 else 'merged.xlsx'

with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
    for f in files:
        xls = pd.ExcelFile(f)
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            sheet_name = sheet if sheet not in writer.sheets else f'{sheet}_{os.path.basename(f)}'
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f'Added sheet \"{sheet_name}\" from {f}')

print(f'Done: {out_path}')
" "./*.xlsx" "merged.xlsx"
```

### XLSX 筛选导出

```bash
python -c "
import pandas as pd, sys

xlsx_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv)>2 else 'filtered.xlsx'
sheet = sys.argv[3] if len(sys.argv)>3 else 0
filter_expr = sys.argv[4]  # e.g. '金额 > 1000'

df = pd.read_excel(xlsx_path, sheet_name=sheet)
filtered = df.query(filter_expr)
filtered.to_excel(out_path, index=False)
print(f'Done: {len(df)} -> {len(filtered)} rows')
" "input.xlsx" "filtered.xlsx" 0 "金额 > 1000"
```

---

## 错误处理指南

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `ModuleNotFoundError` | 缺少 Python 依赖 | 运行 `pip install <包名>` |
| `FileNotFoundError: soffice` | 未安装 LibreOffice | 安装 LibreOffice 并确认路径 |
| `pdf2docx` 转换布局错乱 | 复杂排版 PDF | 改用 PDF→图片→PPTX 方案 |
| 中文乱码 | 编码问题 | CSV 使用 `utf-8-sig`；确保系统有中文字体 |
| `poppler not found` | pdf2image 需要 poppler | 改用 PyMuPDF（`fitz`），不依赖 poppler |
| 大文件内存不足 | 文件过大 | 使用逐页处理，避免一次性加载 |

## LibreOffice 路径参考

| 系统 | 默认路径 |
|------|----------|
| Windows | `C:\Program Files\LibreOffice\program\soffice.exe` |
| macOS | `/Applications/LibreOffice.app/Contents/MacOS/soffice` |
| Linux | `/usr/bin/soffice` 或 `/usr/bin/libreoffice` |

> **提示**：如果 LibreOffice 不在默认路径，可通过 `where soffice`（Windows）或 `which soffice`（Linux/macOS）查找实际路径，替换脚本中的路径即可。

## 脚本方式（推荐）

除了上面的内联 `python -c` 命令，所有转换操作也提供了独立脚本，位于 `scripts/` 目录。脚本方式更易读、更易调试，适合复杂参数场景。

**脚本根目录：** `workspace/skills/pdf-ppt-docx-xlsx/scripts/`

### 脚本清单

| 脚本 | 功能 | 用法示例 |
|------|------|----------|
| `pdf_to_images.py` | PDF → 图片 | `python scripts/pdf_to_images.py input.pdf ./out 200 png` |
| `pdf_to_docx.py` | PDF → DOCX | `python scripts/pdf_to_docx.py input.pdf output.docx --start 0 --end 5` |
| `pdf_to_pptx.py` | PDF → PPTX | `python scripts/pdf_to_pptx.py input.pdf output.pptx 200` |
| `pdf_to_xlsx.py` | PDF → XLSX (提取表格) | `python scripts/pdf_to_xlsx.py input.pdf output.xlsx` |
| `pdf_to_txt.py` | PDF → 纯文本 | `python scripts/pdf_to_txt.py input.pdf output.txt` |
| `pdf_advanced.py` | PDF 合并/拆分/水印/提取/信息 | `python scripts/pdf_advanced.py merge a.pdf b.pdf out.pdf` |
| `docx_to_pdf.py` | DOCX → PDF | `python scripts/docx_to_pdf.py input.docx` |
| `docx_to_pptx.py` | DOCX → PPTX | `python scripts/docx_to_pptx.py input.docx output.pptx` |
| `docx_to_html.py` | DOCX → HTML | `python scripts/docx_to_html.py input.docx output.html` |
| `docx_advanced.py` | DOCX 合并/提取文本/信息 | `python scripts/docx_advanced.py merge a.docx b.docx out.docx` |
| `pptx_to_pdf.py` | PPTX → PDF | `python scripts/pptx_to_pdf.py input.pptx` |
| `pptx_to_images.py` | PPTX → 图片 | `python scripts/pptx_to_images.py input.pptx ./out 200` |
| `pptx_to_docx.py` | PPTX → DOCX | `python scripts/pptx_to_docx.py input.pptx output.docx` |
| `xlsx_to_pdf.py` | XLSX → PDF | `python scripts/xlsx_to_pdf.py input.xlsx` |
| `xlsx_to_csv.py` | XLSX → CSV | `python scripts/xlsx_to_csv.py input.xlsx ./csv_out` |
| `xlsx_advanced.py` | XLSX 合并/信息/摘要 | `python scripts/xlsx_advanced.py info input.xlsx` |
| `images_to_pdf.py` | 图片 → PDF | `python scripts/images_to_pdf.py a.png b.jpg out.pdf` |

### `pdf_advanced.py` 子命令

```bash
# 合并
python scripts/pdf_advanced.py merge file1.pdf file2.pdf merged.pdf

# 拆分（全部页）
python scripts/pdf_advanced.py split input.pdf ./split_output

# 拆分（指定范围）
python scripts/pdf_advanced.py split input.pdf ./split_output --range 0-5,8-10

# 提取指定页
python scripts/pdf_advanced.py extract input.pdf output.pdf --pages 0,2,5-8

# 加水印
python scripts/pdf_advanced.py watermark input.pdf "机密" watermarked.pdf --opacity 0.2 --size 60 --color #ff0000

# 查看信息
python scripts/pdf_advanced.py info input.pdf
```

### `docx_advanced.py` 子命令

```bash
# 合并
python scripts/docx_advanced.py merge a.docx b.docx merged.docx

# 提取文本
python scripts/docx_advanced.py extract_text input.docx output.txt

# 查看信息
python scripts/docx_advanced.py info input.docx
```

### `xlsx_advanced.py` 子命令

```bash
# 合并
python scripts/xlsx_advanced.py merge a.xlsx b.xlsx merged.xlsx

# 查看信息
python scripts/xlsx_advanced.py info input.xlsx

# 生成摘要（前5行预览）
python scripts/xlsx_advanced.py summary input.xlsx summary.txt
```

---

## 使用原则

1. **优先使用 Python 库方案**（PyMuPDF、pdf2docx 等），不依赖 LibreOffice 的转换更快更可控
2. **Office 格式转 PDF 时使用 LibreOffice**，保真度远优于纯 Python 方案
3. **大文件分页处理**，避免内存溢出
4. **输出路径使用绝对路径或明确的相对路径**，避免歧义
5. **转换前检查文件是否存在**，转换后验证输出文件大小非零
6. **简单场景用内联命令，复杂场景用 scripts/ 脚本**——脚本支持更多参数且更易调试
</task_progress>