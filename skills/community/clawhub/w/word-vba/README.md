# Word VBA Skill

基于Microsoft Word VBA/ActiveX的Word文档处理工具包。

## 功能特性

- ✅ 完整的Word文档读写
- ✅ 批量文档处理
- ✅ 文档合并（保留格式）
- ✅ 模板填充（{{placeholder}}语法）
- ✅ 批量文本替换
- ✅ 标题大纲提取
- ✅ 自动生成目录
- ✅ 文档比较

## 快速开始

### 安装依赖

```bash
pip install pywin32
```

### 基本使用

```python
from word_vba import WordWriter, WordReader

# 创建文档
writer = WordWriter()
doc = writer.create_document()
writer.add_paragraph(doc, "Hello World", {'font_name': '宋体', 'font_size': 12})
writer.save_document(doc, "output.docx")
writer.close()

# 读取文档
reader = WordReader()
content = reader.read_document("output.docx")
print(content['paragraphs'][0]['text'])
```

### 高级功能

```python
from word_vba import WordVBAUtils

utils = WordVBAUtils()

# 合并文档
utils.merge_documents(
    ["doc1.docx", "doc2.docx"],
    "merged.docx"
)

# 填充模板
data = {'name': '张三', 'date': '2026-03-04'}
utils.fill_template("template.docx", data, "output.docx")
```

## 运行测试

```bash
python test_word_vba.py
```

## 目录结构

```
word-vba/
├── SKILL.md              # 详细文档
├── README.md             # 本文件
├── requirements.txt      # 依赖
├── __init__.py           # 包初始化
├── word_vba_reader.py    # 读取模块
├── word_vba_writer.py    # 写入模块
├── word_vba_utils.py     # 高级功能
└── test_word_vba.py      # 测试脚本
```

## 许可证

MIT License
