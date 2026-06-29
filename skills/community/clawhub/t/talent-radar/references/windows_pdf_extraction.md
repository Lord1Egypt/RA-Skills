# Windows PDF 文本提取指南

在 Windows 环境下提取 PDF 文本内容的可靠方法。

## 推荐方案：pypdf

### 安装

```bash
# 使用系统 Python 安装（venv 可能没有 pip）
pip install pypdf
```

### 使用

```python
from pypdf import PdfReader

reader = PdfReader(r"C:\path\to\file.pdf")
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    print(f"=== Page {i+1} ===")
    print(text)
```

### 注意事项

- pypdf 是纯 Python 实现，无需系统依赖
- 对于扫描版 PDF（图片），需要使用 OCR 工具
- 路径使用 raw string（`r"..."`）避免转义问题

## 备选方案

### pdfplumber

```bash
pip install pdfplumber
```

```python
import pdfplumber

with pdfplumber.open(r"C:\path\to\file.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            print(text)
```

**注意**：pdfplumber 依赖较重，安装可能较慢

### PyMuPDF (fitz)

```bash
pip install PyMuPDF
```

```python
import fitz

doc = fitz.open(r"C:\path\to\file.pdf")
for page in doc:
    text = page.get_text()
    print(text)
```

**注意**：PyMuPDF 性能最好，但需要编译安装

## 常见问题

### venv 中没有 pip

Hermes 的 venv 可能没有 pip，使用系统 Python：

```bash
# 查找系统 Python
where python

# 使用系统 Python 安装和运行
/c/Users/<user>/AppData/Local/Programs/Python/Python311/python.exe -c "from pypdf import PdfReader; ..."
```

### 路径中的反斜杠

Windows 路径使用反斜杠，在 Python 字符串中需要转义：

```python
# 方式1：raw string
path = r"C:\Users\wus\file.pdf"

# 方式2：正斜杠
path = "C:/Users/wus/file.pdf"

# 方式3：双反斜杠
path = "C:\\Users\\wus\\file.pdf"
```

### 中文乱码

如果提取的中文乱码，可能是 PDF 使用了特殊编码。尝试：

```python
# pdfplumber 对中文支持更好
import pdfplumber

with pdfplumber.open(path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```
