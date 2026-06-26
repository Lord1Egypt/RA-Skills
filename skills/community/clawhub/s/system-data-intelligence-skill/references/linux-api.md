# Linux API Reference

## 核心原则

Linux 无 COM 接口、无 AppleScript，一律通过 **Python 纯库** 或 **LibreOffice headless** 处理文件。

---

## Excel / 表格文件

### 现代格式（.xlsx .xlsm .et）—— openpyxl

```python
import openpyxl

# 读取计算值（非公式）
wb = openpyxl.load_workbook(filepath, data_only=True)

# 大文件（>50MB）省内存模式
wb = openpyxl.load_workbook(filepath, read_only=True)

for ws in wb.worksheets:
    for row in ws.iter_rows(values_only=True):
        process(row)

wb.close()
```

### 旧格式（.xls）—— 两种方案

```bash
# 方案A：LibreOffice 转换（推荐）
libreoffice --headless --convert-to xlsx input.xls --outdir /tmp/
# 转换后用 openpyxl 读取 /tmp/input.xlsx
```

```python
# 方案B：xlrd 直接读取（仅支持 .xls，不支持 .xlsx）
import xlrd
wb = xlrd.open_workbook(filepath)
ws = wb.sheet_by_index(0)
for i in range(ws.nrows):
    print(ws.row_values(i))
```

### CSV —— pandas

```python
import pandas as pd

# 自动检测分隔符和编码
df = pd.read_csv(filepath, sep=None, engine='python', encoding='utf-8-sig')

# 如果存在中文乱码第一选 GBK
df = pd.read_csv(filepath, encoding='gbk', errors='replace')
```

---

## Word / 文档文件

### 现代格式（.docx）—— python-docx

```python
from docx import Document

doc = Document(filepath)

# 正文段落
for para in doc.paragraphs:
    print(para.style.name, para.text)

# 表格
for table in doc.tables:
    for row in table.rows:
        cells = [c.text for c in row.cells]
        print(cells)

# 元数据
core = doc.core_properties
print(core.author, core.created)
```

### 旧格式（.doc .wps）—— LibreOffice 转换

```bash
libreoffice --headless --convert-to docx input.doc --outdir /tmp/
# 转换后用 python-docx 读取 /tmp/input.docx
```

```python
import subprocess
from pathlib import Path

def convert_with_libreoffice(filepath: str, target_format: str = 'docx') -> str:
    """返回转换后的文件路径"""
    out_dir = '/tmp'
    result = subprocess.run(
        ['libreoffice', '--headless', '--convert-to', target_format,
         filepath, '--outdir', out_dir],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice 转换失败: {result.stderr}")
    stem = Path(filepath).stem
    return f"{out_dir}/{stem}.{target_format}"
```

---

## PDF 文件

```python
# 方案A：pdfplumber（文本+表格提取）
import pdfplumber

with pdfplumber.open(filepath) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()

# 方案B：PyMuPDF（较快，适合大 PDF）
import fitz  # pymupdf

doc = fitz.open(filepath)
for page in doc:
    text = page.get_text()
doc.close()
```

---

## 文本编码处理

```python
import chardet

def smart_read(filepath: str) -> str:
    """Linux 下文本文件智能读取（自动检测编码）"""
    with open(filepath, 'rb') as f:
        raw = f.read()
    encoding = chardet.detect(raw)['encoding'] or 'utf-8'
    return raw.decode(encoding, errors='replace')
```

---

## 可视化中文字体

Linux 默认缺少中文字体，需要安装：

```bash
# Ubuntu / Debian
sudo apt install fonts-noto-cjk

# CentOS / RHEL
sudo yum install google-noto-sans-cjk-fonts

# 刚装完字体后需重建字体缓存
fc-cache -fv
```

Matplotlib 配置：

```python
import matplotlib.pyplot as plt

# 自动选取可用中文字体
import matplotlib.font_manager as fm
cjk_fonts = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei']
for font in cjk_fonts:
    if any(f.name == font for f in fm.fontManager.ttflist):
        plt.rcParams['font.sans-serif'] = [font]
        break
plt.rcParams['axes.unicode_minus'] = False
```

---

## 第三方库安装

```bash
# 必装
# pip install openpyxl python-docx pandas chardet

# 按需安装
pip install pdfplumber   # PDF 提取
pip install pymupdf      # 大 PDF 高性能
pip install xlrd==1.2.0  # 旧版 .xls 支持

# LibreOffice
sudo apt install libreoffice-nogui   # Ubuntu
sudo yum install libreoffice-headless  # RHEL/CentOS
```

---

## 常见问题

| 问题 | 解决方案 |
|---|---|
| `openpyxl` 读取公式单元格返回 `None` | 加 `data_only=True` 参数 |
| LibreOffice 转换中文乱码 | 安装 `fonts-noto-cjk` 并重启服务 |
| `xlrd` 读取 `.xlsx` 报错 | xlrd 2.x 只支持 `.xls`，改用 `openpyxl` |
| Matplotlib 显示方块 | 增加 `plt.rcParams['axes.unicode_minus'] = False` |
| 无头服务器无显示器 | 在代码开头加 `import matplotlib; matplotlib.use('Agg')` |
