# PDF、Word 与知网文档解析

## 目标

在文献分析前，把不同格式统一转换为 UTF-8 纯文本，并生成 `manifest.json`。原始文件始终保留，不得覆盖。

## 快速使用

处理单个或多个文件：

```bash
python3 scripts/extract_documents.py paper.pdf article.docx export.ris --out-dir extracted
```

处理一个目录：

```bash
python3 scripts/extract_documents.py references/ --out-dir extracted
```

对扫描型 PDF 启用 OCR：

```bash
python3 scripts/extract_documents.py scanned.pdf --out-dir extracted --ocr
```

输出：

```text
extracted/
├── texts/
│   ├── paper.txt
│   └── article.txt
└── manifest.json
```

## 格式路由

### PDF

优先级：

1. `pdftotext -layout`
2. Python 包 `pypdf`
3. Python 包 `pdfplumber`

如果提取内容过短或明显为空，把文件标记为 `warning`。只有用户允许 OCR 或使用 `--ocr` 时，才调用 `pdftoppm` 和 `tesseract`。

扫描型文献的 OCR 文本可能存在字符错误。重要结论、数字、公式、表格和参考文献必须回到原页面核验。

### DOCX

直接读取 OOXML，提取正文、表格、脚注和尾注。不需要安装 `python-docx`。解析结果主要用于内容分析，不代表原始视觉顺序或复杂版式。

下列内容可能需要人工复核：

- 文本框和浮动对象
- 公式
- 图片中的文字
- 修订模式内容
- 复杂多栏布局
- 嵌入对象

### 旧版 DOC

依次尝试：

1. `antiword`
2. `catdoc`
3. LibreOffice/`soffice`

如果这些工具均不存在，标记为失败并提示安装，不要把二进制内容按文本读取。

Ubuntu/WSL 可根据需要安装：

```bash
sudo apt install antiword
```

或：

```bash
sudo apt install libreoffice
```

### 知网 CAJ、NH、KDH

这些是知网全文容器，不等同于普通 PDF。若文件本身实际以 `%PDF-` 开头，则按 PDF 处理；否则需要 `caj2pdf` 先转换为 PDF：

```bash
caj2pdf convert input.caj -o output.pdf
```

转换后再按 PDF 路由提取。转换失败时保留错误信息，并建议用户在知网阅读器中另存或导出为 PDF。

不要声称支持 CAJ 加密绕过，不要尝试破解受保护文件。

### 知网题录导出

支持常见的：

- TXT
- RIS
- EndNote/ENW
- NBIB
- XML

依次尝试 UTF-8、UTF-8 BOM、GB18030、UTF-16。题录文件通常只有元数据和摘要，必须标记为“题录/摘要来源”，不得当作全文阅读。

## 解析清单

`manifest.json` 中每个文件至少记录：

- `source`
- `format`
- `status`
- `method`
- `output`
- `characters`
- `full_text_likelihood`
- `warnings`
- `error`

状态说明：

- `success`：提取到足够的可读文本
- `warning`：有文本，但可能不完整、过短或来自 OCR/题录
- `failed`：无法提取，不得进入全文证据分析
- `unsupported`：格式不在支持范围

## 分析前检查

- 查看 `manifest.json` 中所有失败和警告。
- 随机核对每篇文献的题目、摘要、正文小节和参考文献。
- 对 OCR 文献核对关键数字和专有名词。
- 对题录导出文件明确标记“仅摘要或元数据”。
- 只有通过检查的全文文献才能标记为“全文已读”。

