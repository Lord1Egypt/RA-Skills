# File Formats Reference

## Excel 格式家族

| 扩展名 | 格式 | 特点 | 推荐读取方式 |
|---|---|---|---|
| `.xlsx` | Office Open XML | 现代格式，无宏 | openpyxl / win32com / xlwings |
| `.xls` | BIFF8（旧版） | Excel 97-2003 | xlrd（只读）/ win32com |
| `.xlsm` | 含宏的 xlsx | 包含 VBA 宏 | openpyxl（忽略宏）/ win32com |
| `.xlsb` | 二进制格式 | 大文件性能好 | win32com（需安装 Excel）|
| `.et` | WPS 表格 | WPS 原生格式 | KET COM / openpyxl（兼容）|

### openpyxl 关键参数

```python
import openpyxl

# 读取计算值（非公式）
wb = openpyxl.load_workbook(filepath, data_only=True)

# 大文件只读模式（节省内存）
wb = openpyxl.load_workbook(filepath, read_only=True)

# 迭代行（内存友好）
for row in ws.iter_rows(min_row=1, max_row=100, values_only=True):
    print(row)
```

---

## Word / WPS Writer 格式

| 扩展名 | 格式 | 推荐读取方式 |
|---|---|---|
| `.docx` | Office Open XML | python-docx / win32com |
| `.doc` | 旧版 Word | win32com（需安装 Word）|
| `.wps` | WPS 文字原生 | KWPS COM |

### python-docx 快速使用

```python
from docx import Document

doc = Document(filepath)

# 正文段落
for para in doc.paragraphs:
    print(para.style.name, para.text)

# 表格
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)

# 图片提取
for rel in doc.part.rels.values():
    if 'image' in rel.target_ref:
        image_data = rel.target_part.blob
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
      <Name>任务名称</Name>
      <Start>2026-01-01T08:00:00</Start>
      <Finish>2026-01-15T17:00:00</Finish>
      <Duration>PT10D</Duration>
      <PercentComplete>50</PercentComplete>
    </Task>
  </Tasks>
</Project>
```

### 多版本命名空间检测

```python
import xml.etree.ElementTree as ET

tree = ET.parse(filepath)
root = tree.getroot()

# 从根节点提取命名空间
tag = root.tag  # 格式: {namespace}Project
if tag.startswith('{'):
    ns = tag[1:tag.index('}')]
else:
    ns = ''
```

---

## 文本格式

```python
# TXT —— 自动检测编码
import chardet
with open(filepath, 'rb') as f:
    encoding = chardet.detect(f.read())['encoding']
with open(filepath, encoding=encoding) as f:
    text = f.read()

# Markdown —— 提取纯文本
import re
def strip_markdown(md: str) -> str:
    md = re.sub(r'```[\s\S]*?```', '', md)   # 移除代码块
    md = re.sub(r'[#*`_~>|-]', '', md)        # 移除标记符
    return md.strip()

# CSV —— 自动检测分隔符
import pandas as pd
df = pd.read_csv(filepath, sep=None, engine='python', encoding='utf-8-sig')
```

---

## 编码最佳实践

| 场景 | 推荐编码 |
|---|---|
| Windows 生成的 CSV | `utf-8-sig`（处理 BOM）|
| 纯英文文件 | `utf-8` |
| 日文/韩文文件 | `chardet` 自动检测 |
| 老式 GBK 文件 | `gbk` 或 `gb18030` |
