# File Formats Reference

> 本文件列出所有支持的文件格式、读取策略及编码处理方法。
> **统一入口：** `from scripts.doc_parser import detect_and_load` — 自动检测格式并降级。

---

## Excel / 表格格式

| 扩展名 | 格式说明 | 推荐读取方式 | 注意事项 |
|---|---|---|---|
| `.xlsx` | Office Open XML（无宏） | openpyxl / win32com / xlwings | 最通用，优先选择 |
| `.xls` | BIFF8（Excel 97-2003） | xlrd / win32com | xlrd 2.x 仅支持 .xls |
| `.xlsm` | 含 VBA 宏的 xlsx | openpyxl（忽略宏）/ win32com | openpyxl 读取时宏不执行 |
| `.xlsb` | 二进制格式 | win32com（需安装 Excel） | 大文件性能好，纯 Python 库不支持 |
| `.et` | WPS 表格原生格式 | KET COM / openpyxl（兼容） | COM 名：`KET.Application` |
| `.csv` | 逗号分隔值 | pandas | 注意编码和分隔符 |

### openpyxl 关键参数

```python
import openpyxl

# 读取计算值（非公式文本）
wb = openpyxl.load_workbook(filepath, data_only=True)

# 大文件只读模式（省内存，不支持写入）
wb = openpyxl.load_workbook(filepath, read_only=True)

# 迭代行（内存友好，适合大表）
for row in ws.iter_rows(min_row=2, values_only=True):   # min_row=2 跳过表头
    process(row)

wb.close()  # read_only 模式下必须手动 close
```

### CSV 读取（自动检测分隔符 + 编码）

```python
import pandas as pd

# 标准读取
df = pd.read_csv(filepath, sep=None, engine='python', encoding='utf-8-sig')

# 大文件分块读取（>100MB）
chunks = []
for chunk in pd.read_csv(filepath, chunksize=10000, encoding='utf-8-sig'):
    chunks.append(chunk)
df = pd.concat(chunks, ignore_index=True)

# 中文乱码备选
df = pd.read_csv(filepath, encoding='gbk', errors='replace')
```

### xlrd 读取旧版 .xls

```python
import xlrd

wb = xlrd.open_workbook(filepath)
ws = wb.sheet_by_index(0)
headers = ws.row_values(0)
data = [ws.row_values(i) for i in range(1, ws.nrows)]
```

---

## Word / WPS 文档格式

| 扩展名 | 格式说明 | 推荐读取方式 |
|---|---|---|
| `.docx` | Office Open XML（现代） | python-docx / win32com |
| `.doc` | 旧版 Word 格式 | win32com（需安装 Word）/ LibreOffice 转换 |
| `.wps` | WPS 文字原生格式 | KWPS COM / LibreOffice 转换 |

### python-docx 快速参考

```python
from docx import Document

doc = Document(filepath)

# 正文段落（含样式）
for para in doc.paragraphs:
    if para.text.strip():
        print(f"[{para.style.name}] {para.text}")

# 表格提取 → DataFrame
import pandas as pd
for table in doc.tables:
    headers = [cell.text for cell in table.rows[0].cells]
    rows = [[cell.text for cell in row.cells] for row in table.rows[1:]]
    df = pd.DataFrame(rows, columns=headers)

# 图片提取
from pathlib import Path
for i, rel in enumerate(doc.part.rels.values()):
    if 'image' in rel.target_ref:
        img_data = rel.target_part.blob
        Path(f"output_img_{i}.png").write_bytes(img_data)

# 文档元数据
core = doc.core_properties
print(core.author, core.created, core.modified)
```

### 旧格式转换（.doc / .wps）

```python
import subprocess
from pathlib import Path

def convert_to_docx(filepath: str, out_dir: str = '/tmp') -> str:
    """将 .doc/.wps 转换为 .docx，返回转换后路径。"""
    result = subprocess.run(
        ['libreoffice', '--headless', '--convert-to', 'docx',
         filepath, '--outdir', out_dir],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        raise RuntimeError(f"转换失败: {result.stderr}")
    return str(Path(out_dir) / (Path(filepath).stem + '.docx'))
```

---

## RTZ 项目文件

RTZ 是基于 XML 的项目管理格式，兼容 RationalPlan / ProjectLibre / Microsoft Project。

```xml
<!-- RTZ 基本结构 -->
<Project xmlns="http://schemas.microsoft.com/project">
  <Tasks>
    <Task>
      <ID>1</ID>
      <Name>需求分析</Name>
      <Start>2026-01-01T08:00:00</Start>
      <Finish>2026-01-15T17:00:00</Finish>
      <Duration>PT10D</Duration>
      <PercentComplete>80</PercentComplete>
      <OutlineLevel>1</OutlineLevel>
    </Task>
  </Tasks>
</Project>
```

### 解析示例（含命名空间处理）

```python
import xml.etree.ElementTree as ET
import pandas as pd

def parse_rtz(filepath: str) -> pd.DataFrame:
    tree = ET.parse(filepath)
    root = tree.getroot()

    # 自动提取命名空间
    tag = root.tag
    ns = tag[1:tag.index('}')] if tag.startswith('{') else ''
    prefix = f'{{{ns}}}' if ns else ''

    def get(el, key):
        return el.findtext(f'{prefix}{key}') or ''

    tasks = []
    for task in root.iter(f'{prefix}Task'):
        if get(task, 'UID') == '0':   # 跳过项目摘要行
            continue
        tasks.append({
            'id':               get(task, 'ID'),
            'name':             get(task, 'Name'),
            'start':            get(task, 'Start'),
            'finish':           get(task, 'Finish'),
            'duration':         get(task, 'Duration'),
            'percent_complete': get(task, 'PercentComplete'),
            'outline_level':    get(task, 'OutlineLevel'),
        })
    return pd.DataFrame(tasks)
```

---

## JSON 格式

```python
import json
import pandas as pd

# 读取 JSON 文件
with open(filepath, encoding='utf-8') as f:
    data = json.load(f)

# 扁平列表 → DataFrame
if isinstance(data, list):
    df = pd.DataFrame(data)

# 嵌套结构展平
df = pd.json_normalize(data, record_path='items', meta=['id', 'name'])

# 写入 JSON
df.to_json('output.json', orient='records', force_ascii=False, indent=2)
```

---

## 文本格式（TXT / Markdown）

```python
import chardet

def smart_read(filepath: str) -> tuple[str, str]:
    """智能读取文本文件，返回 (内容, 编码)。"""
    with open(filepath, 'rb') as f:
        raw = f.read()
    result = chardet.detect(raw)
    encoding = result['encoding'] or 'utf-8'
    content = raw.decode(encoding, errors='replace')
    return content, encoding

# Markdown → 提取纯文本
import re

def strip_markdown(md: str) -> str:
    md = re.sub(r'```[\s\S]*?```', '', md)    # 移除代码块
    md = re.sub(r'`[^`]+`', '', md)           # 移除行内代码
    md = re.sub(r'!\[.*?\]\(.*?\)', '', md)   # 移除图片
    md = re.sub(r'\[([^\]]+)\]\(.*?\)', r'\1', md)  # 链接保留文字
    md = re.sub(r'^#{1,6}\s+', '', md, flags=re.MULTILINE)   # 移除标题符
    md = re.sub(r'[*_~>|]', '', md)
    return md.strip()
```

---

## 编码速查表

| 场景 | 推荐编码 | 说明 |
|---|---|---|
| Windows 生成的 CSV / TXT | `utf-8-sig` | 处理 BOM 头 |
| 纯英文文件 | `utf-8` | 标准 |
| 老式 GBK 文件（简体中文） | `gbk` 或 `gb18030` | gb18030 是 gbk 超集 |
| 繁体中文（台湾/香港） | `big5` | 或 `cp950` |
| 日文 / 韩文 | `chardet` 自动检测 | 不确定时用 chardet |
| 未知编码 | `chardet` → 失败时 `latin-1` | latin-1 永不报错 |

### 通用编码检测工具函数

```python
import chardet
from pathlib import Path

def detect_encoding(filepath: str, sample_size: int = 50000) -> str:
    """检测文件编码，sample_size 越大越准确但越慢。"""
    with open(filepath, 'rb') as f:
        raw = f.read(sample_size)
    result = chardet.detect(raw)
    encoding = result['encoding'] or 'utf-8'
    confidence = result.get('confidence', 0)
    if confidence < 0.7:
        # 置信度低时，对中文文件尝试 gbk
        try:
            raw.decode('gbk')
            return 'gbk'
        except UnicodeDecodeError:
            pass
    return encoding
```

---

## 格式检测与统一加载

```python
from scripts.doc_parser import detect_and_load

# 支持所有格式，自动选最优策略
data = detect_and_load("/path/to/file.xlsx")

# 返回值结构：
# data['type']      → 'spreadsheet' | 'document' | 'text' | 'markdown' | 'json' | 'project'
# data['sheets']    → { sheet_name: [[row], ...] }    # 表格类
# data['content']   → "..."                            # 文本类
# data['data']      → {...} / [...]                    # JSON 类
# data['tasks']     → [...]                            # RTZ 类
# data['_strategy'] → 实际使用的读取策略名
# data['_os']       → 'Windows' | 'Darwin' | 'Linux'
```
