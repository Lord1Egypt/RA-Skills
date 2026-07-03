# 运行环境

## Python 版本

- **最低版本**: Python 3.8+
- **推荐版本**: Python 3.10+

## 必需依赖

| 包名 | 版本要求 | 用途 |
|------|----------|------|
| openpyxl | ≥3.0 | Excel 文件生成与格式化 |

```bash
pip install openpyxl
```

## 可选依赖（用于文档解析）

| 包名 | 版本要求 | 用途 |
|------|----------|------|
| pdfplumber | ≥0.7 | PDF 文档文本提取 |
| PyMuPDF (fitz) | ≥1.20 | PDF 图片提取 |
| python-docx | ≥0.8 | Word 文档解析 |

```bash
# PDF 解析
pip install pdfplumber PyMuPDF

# Word 解析
pip install python-docx

# 安装所有依赖
pip install openpyxl pdfplumber PyMuPDF python-docx
```

## 环境检查

```bash
python -c "import openpyxl; print('openpyxl:', openpyxl.__version__)"
```

## writer.py 运行方式

```bash
# 从文件读取 JSON
python scripts/writer.py input.json

# 从标准输入读取
cat input.json | python scripts/writer.py

# 直接传入 JSON 字符串
echo '{"测试用例":[...]}' | python scripts/writer.py
```
