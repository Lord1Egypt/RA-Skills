# Linux API Reference

> Linux 无 COM 接口、无 AppleScript，全部通过 **Python 纯库** 或 **LibreOffice headless** 处理文件。
> 适用于服务器、Docker 容器、CI/CD 环境。

---

## 核心原则

1. **优先纯 Python 库**（openpyxl / python-docx）— 无需安装 Office
2. **旧格式先转换**（LibreOffice headless）— 再用纯库读取
3. **无头环境设置 Agg 后端**（Matplotlib）— 无显示器时必须
4. **Docker 环境一次配置，到处运行**

---

## Excel / 表格文件

### 现代格式（.xlsx .xlsm .et）— openpyxl

```python
import openpyxl
from pathlib import Path

def read_excel(filepath: str, sheet_name: str = None) -> dict:
    file_mb = Path(filepath).stat().st_size / 1e6
    read_only = file_mb > 50   # 大文件自动只读模式

    wb = openpyxl.load_workbook(filepath, data_only=True, read_only=read_only)
    result = {}
    sheets = [wb[sheet_name]] if sheet_name else wb.worksheets

    for ws in sheets:
        result[ws.title] = [list(row) for row in ws.iter_rows(values_only=True)]

    wb.close()
    return result
```

### 大文件流式处理（>100MB）

```python
import openpyxl

def stream_excel(filepath: str, sheet_name: str = None, chunk_size: int = 1000):
    """逐块生成 Excel 行数据，避免 OOM。"""
    wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
    ws = wb[sheet_name] if sheet_name else wb.worksheets[0]

    chunk = []
    for row in ws.iter_rows(values_only=True):
        chunk.append(list(row))
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

    wb.close()

# 用法
for batch in stream_excel("huge.xlsx", chunk_size=5000):
    df_chunk = pd.DataFrame(batch)
    process(df_chunk)
```

### 旧格式（.xls）— 两种方案

```bash
# 方案 A：LibreOffice 转换（推荐，保留格式）
libreoffice --headless --convert-to xlsx input.xls --outdir /tmp/
```

```python
# 方案 B：xlrd 直接读取（纯 Python，仅支持 .xls）
import xlrd

wb = xlrd.open_workbook(filepath)
for ws in wb.sheets():
    headers = ws.row_values(0)
    rows = [ws.row_values(i) for i in range(1, ws.nrows)]
```

### CSV — pandas

```python
import pandas as pd

# 标准读取（自动检测分隔符）
df = pd.read_csv(filepath, sep=None, engine='python', encoding='utf-8-sig')

# 大文件分块（>100MB）
chunks = []
for chunk in pd.read_csv(filepath, chunksize=50000):
    chunks.append(process(chunk))   # 每块处理后丢弃原始 chunk
result = pd.concat(chunks, ignore_index=True)
```

---

## Word / 文档文件

### 现代格式（.docx）— python-docx

```python
from docx import Document
import pandas as pd

doc = Document(filepath)

# 正文段落
paragraphs = [(p.style.name, p.text) for p in doc.paragraphs if p.text.strip()]

# 表格 → DataFrame（取第一个表格）
if doc.tables:
    table = doc.tables[0]
    headers = [c.text.strip() for c in table.rows[0].cells]
    rows = [[c.text.strip() for c in row.cells] for row in table.rows[1:]]
    df = pd.DataFrame(rows, columns=headers)

# 元数据
core = doc.core_properties
meta = {"author": core.author, "created": core.created, "modified": core.modified}
```

### 旧格式（.doc / .wps）— LibreOffice 转换

```python
import subprocess
from pathlib import Path

def convert_with_libreoffice(filepath: str, target_format: str = 'docx',
                              out_dir: str = '/tmp', timeout: int = 60) -> str:
    """转换旧格式文件，返回输出路径。"""
    result = subprocess.run(
        ['libreoffice', '--headless', '--convert-to', target_format,
         filepath, '--outdir', out_dir],
        capture_output=True, text=True, timeout=timeout
    )
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice 转换失败: {result.stderr}")
    return str(Path(out_dir) / (Path(filepath).stem + f'.{target_format}'))

# 用法
docx_path = convert_with_libreoffice("old.doc")
doc = Document(docx_path)
```

---

## PDF 文件

```python
# 方案 A：pdfplumber（文本 + 表格，适合排版规范的 PDF）
import pdfplumber

with pdfplumber.open(filepath) as pdf:
    all_text = ""
    all_tables = []
    for page in pdf.pages:
        all_text += page.extract_text() or ""
        tables = page.extract_tables()
        all_tables.extend(tables)

# 方案 B：PyMuPDF（速度快，适合大 PDF）
import fitz   # pip install pymupdf

doc = fitz.open(filepath)
text = "\n".join(page.get_text() for page in doc)
doc.close()
```

---

## 文本编码处理

```python
import chardet

def smart_read(filepath: str) -> tuple[str, str]:
    """自动检测编码，返回 (内容, 编码名称)。"""
    with open(filepath, 'rb') as f:
        raw = f.read()
    result   = chardet.detect(raw)
    encoding = result['encoding'] or 'utf-8'
    content  = raw.decode(encoding, errors='replace')
    return content, encoding
```

---

## 可视化环境配置

### 无头服务器（无显示器）

```python
# 必须在任何 pyplot import 之前设置
import matplotlib
matplotlib.use('Agg')     # 使用非交互式后端

import matplotlib.pyplot as plt
```

### Docker / 服务器中文字体

```bash
# Ubuntu / Debian
sudo apt-get install -y fonts-noto-cjk
fc-cache -fv

# CentOS / RHEL
sudo yum install -y google-noto-sans-cjk-fonts
fc-cache -fv
```

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 自动检测并设置可用 CJK 字体
CJK_FONTS = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'SimHei']
available = {f.name for f in fm.fontManager.ttflist}
for font in CJK_FONTS:
    if font in available:
        plt.rcParams['font.sans-serif'] = [font]
        break
plt.rcParams['axes.unicode_minus'] = False
```

---

## Docker 环境（推荐配置）

项目提供完整 Dockerfile，一键构建含 LibreOffice + 中文字体 + Python 依赖的镜像：

```bash
# 构建镜像
docker compose up -d

# 执行文件解析
docker exec -it sdi-app python scripts/doc_parser.py /data/report.xlsx

# 执行分析
docker exec -it sdi-app python scripts/deep_analyzer.py /data/sales.csv date revenue

# 挂载本地数据目录
# docker-compose.yml 已配置：./data:/data  ./outputs:/app/outputs
```

```dockerfile
# Dockerfile 关键配置（已包含）
FROM python:3.11-slim
RUN apt-get install -y libreoffice-nogui fonts-noto-cjk
ENV MPLBACKEND=Agg       # 自动设置无头后端
```

---

## 第三方库安装

```bash
# 基础（requirements.txt 已包含）
pip install openpyxl python-docx pandas chardet

# 按需安装
pip install pdfplumber    # PDF 文本 + 表格提取
pip install pymupdf       # PDF 大文件高性能
pip install xlrd==2.0.1  # .xls 旧格式支持（2.x 仅支持 .xls）

# LibreOffice
sudo apt install libreoffice-nogui   # Ubuntu/Debian（最小化无界面版）
sudo yum install libreoffice-headless  # RHEL/CentOS
```

---

## 常见问题

| 问题 | 解决方案 |
|---|---|
| `openpyxl` 读取公式单元格返回 `None` | 加 `data_only=True` 参数 |
| `xlrd` 读取 `.xlsx` 报错 | xlrd 2.x 只支持 `.xls`，`.xlsx` 改用 `openpyxl` |
| LibreOffice 转换中文乱码 | 安装 `fonts-noto-cjk`，重建字体缓存：`fc-cache -fv` |
| Matplotlib 报 `cannot connect to display` | 在导入前加 `matplotlib.use('Agg')` |
| Matplotlib 中文显示方块 | 安装 CJK 字体并设置 `plt.rcParams['font.sans-serif']` |
| Docker 中 LibreOffice 转换慢 | 首次启动初始化慢属正常，后续会缓存 |
| 大文件内存溢出 | 改用 `read_only=True`（openpyxl）或 `chunksize`（pandas） |
