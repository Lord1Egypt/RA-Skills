# Read Word Document Skill

读取 Microsoft Word 文档的 OpenClaw Skill

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 命令行使用
```bash
# 读取文档
python read_word.py "文档.docx"

# 搜索关键词
python read_word.py "文档.docx" -s "关键词1,关键词2"

# 保存为文本
python read_word.py "文档.docx" -o "输出.txt"
```

### 3. Python调用
```python
from read_word import read_word_document, search_in_document

# 读取
paragraphs = read_word_document("文档.docx")

# 搜索
results = search_in_document("文档.docx", ["关键词1", "关键词2"])
```

## 支持的格式
- ✅ .docx (Word 2007+)
- ✅ .doc (Word 97-2003)

## 功能
- 自动识别文件格式
- 完美支持中文
- 关键词搜索
- 导出为UTF-8文本
- 文档信息分析
