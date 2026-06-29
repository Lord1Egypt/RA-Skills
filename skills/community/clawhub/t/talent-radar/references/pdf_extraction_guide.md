# PDF简历提取方法

## Windows环境下的PDF文本提取

### 问题
Hermes的vision_analyze工具不支持PDF文件，需要使用Python库提取文本。

### 解决方案
使用系统Python + pypdf库：

```bash
/c/Users/wus/AppData/Local/Programs/Python/Python311/python.exe -c "
from pypdf import PdfReader

reader = PdfReader(r'C:\path\to\resume.pdf')
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    print(f'=== Page {i+1} ===')
    print(text)
    print()
"
```

### 注意事项
1. **不要使用venv中的Python**：Hermes的venv可能缺少pip
2. **使用系统Python**：路径通常是 `/c/Users/<user>/AppData/Local/Programs/Python/Python311/python.exe`
3. **先安装pypdf**：`pip install pypdf`
4. **处理中文路径**：使用 `r''` 原始字符串

### 替代方案
- 如果pypdf不可用，可尝试 PyMuPDF (fitz)
- 如果需要OCR（扫描件PDF），需要额外安装 pytesseract

### 在execute_code中的注意事项
execute_code工具使用的Python环境可能与系统Python不同，建议直接使用terminal工具调用系统Python。
