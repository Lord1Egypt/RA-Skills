# 📚 书籍章节提取技能 (Book Chapter Extractor Skill)

> **创建日期**: 2026-03-22
> **版本**: 2.0
> **用途**: 从Word或PDF文档中提取章节结构并分割内容
> **标签**: #文档处理 #章节提取 #PDF #Word

---

## 🎯 核心职责

从指定路径的Word或PDF文档中读取内容，识别章节边界，将全书内容按章节拆分为结构化数据。

---

## 📋 操作流程

### Step 1: 验证书籍路径

**路径规则**:
```
支持格式：
- Word文档: F:\book\<书名>\<书名>.docx
- PDF文档: F:\book\<书名>\<书名>.pdf

示例:
F:\book\Security Analysis\Security Analysis.docx
F:\book\Security Analysis\Security Analysis.pdf
```

**验证逻辑**:
- 检查文件是否存在
- 验证文件格式为.docx或.pdf
- 返回文件基本信息（大小、修改时间、文件类型）

---

### Step 2: 读取文档内容

**使用Python读取**:
```python
import os
from docx import Document
import PyPDF2

def read_book(book_path):
    """
    读取Word或PDF文档
    Args:
        book_path: 书籍完整路径
    Returns:
        Document对象 (Word) 或 文本列表 (PDF)
    """
    file_ext = os.path.splitext(book_path)[1].lower()

    if file_ext == '.docx':
        doc = Document(book_path)
        return doc, 'docx'
    elif file_ext == '.pdf':
        # 读取PDF文本
        text_blocks = extract_pdf_text(book_path)
        return text_blocks, 'pdf'
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")

def extract_pdf_text(book_path):
    """
    从PDF提取文本，按段落分割
    Returns:
        list: 段落文本列表
    """
    text_blocks = []
    
    with open(book_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
            # 按段落分割文本
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
            text_blocks.extend(paragraphs)
    
    return text_blocks
```

**PDF特殊处理**:
- PyPDF2需要安装: `pip install PyPDF2`
- PDF文本提取可能包含格式噪音，需要清理
- 页眉页脚可能被误识别为段落

---

### Step 3: 识别章节结构

**章节识别规则**:
- 以"CHAPTER"开头的段落（不区分大小写）
- 或以"Chapter"开头后跟数字的段落
- 或使用中文"第X章"格式
- 前N个字符中包含章节标识（[:20]截取判断）

**识别逻辑**:
```python
def extract_chapters(doc, file_type):
    """
    提取章节列表
    Args:
        doc: Document对象 (docx) 或 文本列表 (pdf)
        file_type: 'docx' 或 'pdf'
    Returns:
        [
            {
                "chapter": 1,
                "title": "章节标题",
                "start_paragraph": 5,
                "paragraphs": ["段落1", "段落2", ...]
            },
            ...
        ]
    """
    chapters = []
    current_chapter = None
    chapter_counter = 0

    if file_type == 'docx':
        # Word文档处理
        for idx, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if not text:
                continue

            # 检测章节标题
            is_chapter = detect_chapter_title(text)
            
            if is_chapter:
                chapter_counter += 1
                current_chapter = {
                    "chapter": chapter_counter,
                    "title": text,
                    "start_paragraph": idx,
                    "paragraphs": []
                }
                chapters.append(current_chapter)
            elif current_chapter:
                current_chapter["paragraphs"].append(text)
    
    elif file_type == 'pdf':
        # PDF文档处理
        for idx, text in enumerate(doc):
            if not text:
                continue

            # 检测章节标题
            is_chapter = detect_chapter_title(text)
            
            if is_chapter:
                chapter_counter += 1
                current_chapter = {
                    "chapter": chapter_counter,
                    "title": text,
                    "start_paragraph": idx,
                    "paragraphs": []
                }
                chapters.append(current_chapter)
            elif current_chapter:
                current_chapter["paragraphs"].append(text)

    return chapters

def detect_chapter_title(text):
    """
    检测是否为章节标题
    """
    # 规则1: CHAPTER开头
    if 'CHAPTER' in text.upper()[:20]:
        return True
    
    # 规则2: Chapter X格式
    if text.startswith('Chapter ') and len(text) > 9 and text[8:9].isdigit():
        return True
    
    # 规则3: 第X章格式
    if text.startswith('第') and '章' in text[:10]:
        return True
    
    # 规则4: 全大写且较短（可能为标题）
    if len(text) < 100 and text.isupper() and any(char.isdigit() for char in text):
        return True
    
    return False
```

**PDF文本清理**:
```python
def clean_pdf_text(text):
    """
    清理PDF提取的文本噪音
    """
    # 移除页码
    text = re.sub(r'^\d+\s*$', '', text)
    
    # 移除过短的行（可能是页眉页脚）
    if len(text) < 5:
        return None
    
    return text
```

---

### Step 4: 生成结构化输出

**输出格式**:
```json
{
  "book_info": {
    "title": "书名",
    "path": "F:\\book\\<书名>\\<书名>.pdf",
    "file_type": "pdf",
    "total_chapters": 20,
    "file_size": "2.5MB"
  },
  "chapters": [
    {
      "chapter": 1,
      "title": "Security Analysis: Scope and Limitations",
      "start_paragraph": 5,
      "paragraph_count": 85,
      "content_preview": "本章讲述投资的基本概念...",
      "paragraphs": [
        "段落1内容",
        "段落2内容",
        ...
      ]
    },
    {
      "chapter": 2,
      "title": "The Concept of Intrinsic Value",
      "start_paragraph": 90,
      "paragraph_count": 92,
      "paragraphs": [...]
    }
  ]
}
```

---

## 📊 章节统计

生成章节统计表格:
```markdown
| 章节 | 标题 | 段落数 | 预估字数 |
|------|------|-------|---------|
| Ch 1 | Security Analysis: Scope and Limitations | 85 | ~12KB |
| Ch 2 | The Concept of Intrinsic Value | 92 | ~14KB |
| ... | ... | ... | ... |

**文件类型**: PDF
**总页数**: XX
```

---

## 🔧 错误处理

### 常见错误及处理

| 错误类型 | 检测方式 | 处理方案 |
|---------|---------|---------|
| 文件不存在 | 检查路径 | 返回错误信息，提示正确路径格式 |
| 不支持的格式 | 检查扩展名 | 返回错误，仅支持.docx和.pdf |
| 无法识别章节 | 章节数量为0 | 返回检测到的标题列表供确认 |
| 内容为空 | 段落数量为0 | 提示文档可能损坏或加密 |
| PDF提取失败 | PyPDF2异常 | 尝试备用PDF库或建议转Word |

### PDF特殊错误

| 错误类型 | 原因 | 处理方案 |
|---------|------|---------|
| 加密PDF | PDF有密码保护 | 提示输入密码或使用解密工具 |
| 扫描PDF | 图片格式非文本 | 提示使用OCR工具 |
| 编码问题 | 特殊字符编码错误 | 尝试不同编码选项 |

---

## ✅ 输出标准

**必须包含**:
- ✅ 书籍基本信息（路径、标题、文件类型、总章节数）
- ✅ 每个章节的完整内容（paragraphs数组）
- ✅ 章节统计信息
- ✅ 处理状态（成功/失败及原因）

**禁止包含**:
- ❌ Markdown笔记内容（由note-generator负责）
- ❌ Cypher语句（由neo4j-cypher-generator负责）
- ❌ Neo4j导入操作（由neo4j-importer负责）

---

## 🎓 使用示例

### 示例1: Word文档

**输入**:
```
书籍路径: F:\book\Security Analysis\Security Analysis.docx
```

**输出**:
```json
{
  "book_info": {
    "title": "Security Analysis",
    "path": "F:\\book\\Security Analysis\\Security Analysis.docx",
    "file_type": "docx",
    "total_chapters": 40
  },
  "chapters": [
    {
      "chapter": 1,
      "title": "Security Analysis: Scope and Limitations",
      "paragraphs": [...]
    },
    ...
  ]
}
```

### 示例2: PDF文档

**输入**:
```
书籍路径: F:\book\The Intelligent Investor\The Intelligent Investor.pdf
```

**输出**:
```json
{
  "book_info": {
    "title": "The Intelligent Investor",
    "path": "F:\\book\\The Intelligent Investor\\The Intelligent Investor.pdf",
    "file_type": "pdf",
    "total_pages": 640,
    "total_chapters": 20
  },
  "chapters": [
    {
      "chapter": 1,
      "title": "Investment versus Speculation",
      "start_paragraph": 10,
      "paragraph_count": 120,
      "paragraphs": [...]
    },
    ...
  ]
}
```

---

## 🔄 与其他模块的接口

**下游模块**:
- `note-generator`: 接收单个章节的paragraphs进行笔记生成（兼容docx和pdf提取的段落）
- `book-learning-coordinator`: 接收完整章节列表进行进度管理

---

## 📦 依赖库

**必需库**:
```bash
# Word文档处理
pip install python-docx

# PDF文档处理
pip install PyPDF2
```

**可选库**（增强PDF处理）:
```bash
# PDF OCR支持（扫描版PDF）
pip install pdf2image
pip install pytesseract

# 备用PDF库
pip install pypdf
pip install pdfplumber
```

---

## ⚠️ 注意事项

### PDF处理限制
1. **布局敏感**: PDF段落分割基于换行符，可能不准确
2. **格式丢失**: PDF提取的是纯文本，不保留原始格式
3. **页眉页脚**: 可能被误识别为正文段落，需要手动清理
4. **扫描版PDF**: 需要OCR预处理才能提取文本

### Word文档优势
1. **结构清晰**: 段落边界明确
2. **格式保留**: 可以提取标题样式辅助章节识别
3. **处理稳定**: 错误率低于PDF

---

## 🔍 PDF与Word选择建议

| 场景 | 推荐格式 | 原因 |
|------|---------|------|
| 专业书籍 | Word | 段落结构清晰，章节识别准确 |
| 扫描版书籍 | PDF + OCR | 必须使用PDF |
| 网络下载书籍 | PDF | 网络资源多为PDF格式 |
| 自整理笔记 | Word | 便于编辑和调整结构 |

---

## 🛠️ OpenClaw 脚本配置

**脚本文件**: `book-extractor-script.py`
**脚本类型**: Python
**调用方式**: 外部工具

### 执行命令
```bash
python book-extractor-script.py --book_path "<书籍路径>"
```

### 输入参数
```json
{
  "book_path": "F:\\book\\Security Analysis\\Security Analysis.docx",
  "book_title": "Security Analysis"
}
```

### 输出格式
```json
{
  "success": true,
  "book_info": {
    "title": "Security Analysis",
    "path": "F:\\book\\Security Analysis\\Security Analysis.docx",
    "file_type": "docx",
    "total_chapters": 40,
    "file_size_mb": 2.5
  },
  "chapters": [
    {
      "chapter": 1,
      "title": "Security Analysis: Scope and Limitations",
      "start_paragraph": 5,
      "paragraph_count": 85,
      "paragraphs": ["段落1", "段落2", ...]
    }
  ],
  "summary": [...]
}
```

### OpenClaw 调用逻辑
1. 接收用户书籍路径
2. 验证文件存在且格式正确
3. 执行 `book-extractor-script.py`
4. 解析返回的JSON结果
5. 格式化输出章节列表

### 错误处理
- 文件不存在 → 提示用户检查路径
- 不支持的格式 → 仅支持.docx和.pdf
- 无法识别章节 → 返回检测到的标题列表供确认
- PDF加密 → 提示输入密码或使用解密工具

---

_Book Chapter Extractor v2.0 · 2026-03-22_ 📚
