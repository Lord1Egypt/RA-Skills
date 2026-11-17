# PDF 读取与分析（OpenClaw 版 · 双平台统一 Python 路线）

> 🌐 语言 / Language：本文档是**内容规范**而非语言约束；默认中文，用户用英文或其他语言提问时就用该语言回答。
> This document is a content spec, not a language mandate — answer in the user's language.

> ⚠️ **使用本文档前请注意**：本文档应在实际处理 PDF 文件之前完整阅读，以选择最合适的工具和方法。不要在未阅读本文档的情况下盲目尝试处理 PDF。

用于从 PDF 文件中提取文本、表格和元数据的方法。

## ⚠️ 读取边界：所有示例都先过 `pathguard`

本技能的承诺是「所有读取都限定在知识库根内，越界（含符号链接）即拒绝」。下面的示例
全部假定你已经用受控助手拿到**真实路径**——不要直接把用户/文档给出的字符串塞进
`open()` / `PdfReader()` / `pdfplumber.open()`：相对路径取决于工作目录，符号链接会把
读取带到库外。

```python
import sys, pathlib
sys.path.insert(0, "<技能目录>/scripts")
import pathguard

KB_ROOT = "<知识库根目录>"

def kb_path(rel: str) -> str:
    """把库内相对路径解析成真实路径；越出知识库根即拒绝（fail closed）。"""
    root = pathguard.real_root(KB_ROOT)
    real = pathguard.real_target(str(pathlib.Path(root) / rel))
    if not pathguard.is_within(root, real):
        raise SystemExit(f"拒绝读取：越出知识库根 {real}")
    return real
```

后文示例里的 `kb_path("document.pdf")` 即由此而来。

## 平台策略（重要）

**PDF 处理统一走 Python 路线**（pdfplumber + pypdf + pypdfium2），Windows 与 macOS 行为完全一致：
- 双平台统一安装：`pip install pdfplumber pypdf pypdfium2`
- ⚠️ 安装前先告知用户「将安装这些包（会修改 Python 环境）」，获确认后再执行（详见 SKILL.md「依赖自安装」）
- 不依赖 poppler/pdftotext 二进制（Windows/macOS 默认都没有，安装路径还不同——避免双平台差异）
- 若系统中恰好已有 `pdftotext`（可选加速），可优先使用；但**默认路径是 Python，且必须输出到文件而非 stdout**

## 快速决策表

| 场景 | 推荐工具 | 原因 | 代码示例 |
|------|----------|------|---------|
| 纯文本提取（最常见） | pdfplumber | 双平台统一，提取质量好 | `page.extract_text()` |
| 需要提取表格 | pdfplumber | 表格识别能力强 | `page.extract_tables()` |
| 需要元数据 | pypdf | 轻量级 | `reader.metadata` |
| 扫描PDF（图片） | pypdfium2 转图片 + OCR | 无其他选择 | `page.render()` |
| 加密 PDF | pypdf | 支持解密 | `reader.decrypt()` |

## 文本提取优先级

**推荐优先级（从高到低）**：
1. **pdfplumber**（双平台统一，文本+表格都强，首选）
2. pypdf（轻量级，简单提取/元数据）
3. pdftotext 命令行（**仅当系统已安装**，可选加速）
4. OCR（仅用于扫描PDF或无法直接提取文本的情况）

## 快速开始：pdfplumber 提取文本（推荐，双平台通用）

> ⚠️ **重要**：必须将提取结果保存到文件，不要直接打印到 stdout，否则会占用大量 token！

本项目已随包提供 `scripts/extract_pdf_text.py`（双平台通用，**请直接使用它，不要另抄一份**，以免绕开边界校验）：

```bash
python scripts/extract_pdf_text.py <input.pdf> <output.txt> [start_page] [end_page]
```

该脚本的安全行为（与其源码一致）：
- 源 PDF 必须是**真实路径**上的普通文件：路径中**任一段含符号链接即拒绝**（`scripts/pathguard.py` 的 `require_real_file`，fail closed）——不做"解开链接再读"，因此不会跟着链接读到知识库之外；被拒时报错会回显真实位置，改用真实路径即可
- 输出 `.txt` 必须与源 PDF 同处一个（真实）目录内，越界即拒绝（`scripts/pathguard.py`，fail closed）
- 只写这一个派生文件，源 PDF 不动；运行前打印写入路径

**使用流程**：
1. `python scripts/extract_pdf_text.py input.pdf output.txt`（生成派生文本文件，与源 PDF 同目录；不占 token）
2. 用 exec（Select-String / grep）对生成的文本文件检索关键词
3. 只读取匹配部分的上下文，而非全文

**提取特定页面**（大 PDF 用，减少处理量）：
- Windows/macOS 通用：`python scripts/extract_pdf_text.py input.pdf output.txt 1 5`（第 1-5 页）

## Python 库

### pypdf - 基本文本提取与元数据

```python
from pypdf import PdfReader

reader = PdfReader(kb_path("document.pdf"))

# 提取全部文本
for page in reader.pages:
    text = page.extract_text()

# 提取元数据
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
```

### pdfplumber - 文本和表格提取（首选）

#### 提取文本

```python
import pdfplumber

with pdfplumber.open(kb_path("document.pdf")) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
```

#### 提取表格

```python
import pdfplumber

with pdfplumber.open(kb_path("document.pdf")) as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### 高级表格提取（转为 DataFrame）

```python
import pandas as pd
import pdfplumber

with pdfplumber.open(kb_path("document.pdf")) as pdf:
    all_tables = []
    for page in pdf.pages:
        for table in page.extract_tables():
            if table:  # 检查表格非空
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    # 检索期只读：表格留在内存里用（筛选/汇总后写进回答）。
    # 需要落盘属于「维护动作」，必须先取得用户确认，且目标必须在知识库根内
    # 并通过真实路径校验（见 SKILL.md「维护脚本」一节），不要用相对路径直接 to_excel。
```

#### 复杂表格的高级设置

```python
import pdfplumber

with pdfplumber.open(kb_path("complex_table.pdf")) as pdf:
    page = pdf.pages[0]
    table_settings = {
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance": 3,
        "intersection_tolerance": 15
    }
    tables = page.extract_tables(table_settings)
```

### pypdfium2 - 快速渲染（扫描件转图片）

> 🛡️ **写盘边界**：下面几段渲染 / OCR 片段为**示意写法**。实际落盘请用随包脚本
> `scripts/convert_pdf_to_images.py`：输出目录必须位于**源 PDF 所在目录树内**，并按真实
> 路径校验（解符号链接后越界即拒绝）；不要把片段改成写到知识库之外的位置。

```python
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument(kb_path("document.pdf"))

# 渲染单页为图片（供 OCR 或人工查看）
page = pdf[0]
bitmap = page.render(scale=2.0)
img = bitmap.to_pil()
# 落盘不要用相对路径：直接用随包脚本（它会逐页校验目标在根内、非链接、非目录）
#   python scripts/convert_pdf_to_images.py --root "<知识库根>" "<pdf>" "<输出目录>"

# 渲染多页（仅用于 OCR / 预览，**不要在这里落盘**）
for i, page in enumerate(pdf):
    bitmap = page.render(scale=1.5)
    img = bitmap.to_pil()
    # 需要保存时，统一交给随包脚本（它逐页校验：在知识库根内、非符号链接、非目录、存在即跳过）
    #   python scripts/convert_pdf_to_images.py --root "<知识库根>" "<pdf>" "<输出目录>"
    _ = img  # 内存中继续处理（例如交给 pytesseract）
```

## OCR 提取（扫描PDF）

> 需要：`pip install pytesseract pdf2image`（双平台通用；macOS 需 `brew install tesseract`，Windows 需安装 Tesseract OCR 并加入 PATH——仅扫描件场景才需要）

```python
import pytesseract
from pdf2image import convert_from_path

# PDF 转图片
images = convert_from_path(kb_path('scanned.pdf'))

# OCR 每一页
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"
```

> ⚠️ OCR 依赖较重（tesseract 二进制），仅在扫描件（无文本层）时启用；常规 PDF 走 pdfplumber 即可。

## 处理加密 PDF

```python
from pypdf import PdfReader

reader = PdfReader(kb_path("encrypted.pdf"))
if reader.is_encrypted:
    reader.decrypt("password")

for page in reader.pages:
    text = page.extract_text()
```

## 批量处理

批量场景**不要自己 glob + 写同名 .txt**：那会跟随符号链接读库外文件，并可能覆盖
既有文件（包括源 PDF 之外的文档）。逐份调用受控助手即可（它校验根、拒绝链接、
原子写入、不覆盖源文件）：

```bash
# 逐个文件处理（root 必须显式给出；库外 PDF / 链接一律拒绝）
python scripts/extract_pdf_text.py --root "$KB_ROOT" "$pdf" "${pdf%.pdf}.txt"
```

要批量遍历，先列出**非链接**的 PDF，再逐份调用：

```bash
find "$KB_ROOT" -type l -prune -o -type f -name '*.pdf' -print | while read -r pdf; do
  python scripts/extract_pdf_text.py --root "$KB_ROOT" "$pdf" "${pdf%.pdf}.txt"
done
```

## 性能优化

1. **文件输出优先**：始终将提取结果保存到文件，然后用 exec 搜索 / read 局部读取，避免占用大量 token
2. **大型PDF**：用 `extract_pdf_text.py` 的 start_page/end_page 参数按页范围提取，避免处理整个文件
3. **文本提取**：pdfplumber 首选；表格用 `extract_tables()`；元数据用 pypdf
4. **内存管理**：逐页或分块处理大文件

## 快速参考

| 任务 | 最佳工具 | 代码 |
|------|----------|------|
| 提取文本 | pdfplumber | `page.extract_text()` |
| 提取表格 | pdfplumber | `page.extract_tables()` |
| 元数据 | pypdf | `reader.metadata` |
| OCR 扫描PDF | pytesseract + pypdfium2 | 先转图片再OCR |
| PDF转图片 | pypdfium2 | `page.render()` |

## 可用包（双平台 pip 安装）

- **pdfplumber** - 文本和表格提取（MIT 许可）⭐ 首选
- **pypdf** - 基本操作 / 元数据 / 加密（BSD 许可）
- **pypdfium2** - 快速渲染转图片（Apache/BSD 许可）
- **pytesseract + pdf2image** - OCR（Apache 许可，仅扫描件）
