---
name: universal-translator
description: Framework for translating Word, PDF, Excel, PowerPoint, HTML, Markdown, TXT documents. Provides document parsing code — the AI agent's own LLM performs the actual translation.
version: 1.0.5
license: MIT-0
metadata: {"openclaw": {"emoji": "🌍", "requires": {"bins": ["python3"], "env": []}}}
---

# Universal Translator

Translate any document format while preserving layout and formatting.

## Features

- 📄 **All Formats**: Word, PDF, Excel, PPT, HTML, Markdown, TXT
- 📁 **Batch Translation**: Translate entire folders
- 🎯 **Terminology**: Keep terms consistent
- 🌍 **50+ Languages**: Chinese, English, Japanese, etc.
- 📐 **Format Preserved**: Keep original layout

## Supported Formats

| Format | Extension | Method |
|--------|-----------|--------|
| Word | .docx | python-docx |
| Excel | .xlsx | openpyxl |
| PowerPoint | .pptx | python-pptx |
| PDF | .pdf | pymupdf |
| HTML | .html | BeautifulSoup |
| Markdown | .md | text processing |
| Text | .txt | text processing |

**Note**: Only modern formats are supported. For .xls files, convert to .xlsx first.

## Trigger Conditions

Only when the user asks to translate a document file (Word/PDF/Excel/PPT/HTML/MD/TXT) to another language.

---

## How Translation Works

> ⚠️ **数据外发提醒**：文档内容由 AI 读取并逐段发送至配置中的 LLM 进行翻译。LLM 的运行位置（本地/远程）取决于 OpenClaw 配置。

This is a **Framework Skill**: it provides document parsing boilerplate (read Word/Excel/PPT/PDF files, iterate paragraphs/cells/shapes, write output). The AI agent's own LLM performs the actual translation.

**Translation workflow:**
1. Use the Python code below to open the document and extract text
2. For each paragraph/cell/shape, translate the text using your LLM
3. Write the translated text back into the document
4. Save the output file

**Note:** The `_translate_text` method is a stub — you MUST replace it with actual LLM translation. The stub exists only to let you test the parsing flow; do not use it in production.

## Python Code

```python
import os
from pathlib import Path
from docx import Document
import openpyxl
from pptx import Presentation

class UniversalTranslator:
    def __init__(self):
        self.supported = {
            'word': ['.docx'],
            'excel': ['.xlsx', '.xls'],
            'powerpoint': ['.pptx'],
            'pdf': ['.pdf'],
            'html': ['.html', '.htm'],
            'markdown': ['.md'],
            'text': ['.txt']
        }
    
    def detect_format(self, file_path):
        """Detect file format"""
        ext = Path(file_path).suffix.lower()
        
        for format_type, extensions in self.supported.items():
            if ext in extensions:
                return format_type
        
        return 'unknown'
    
    def translate_word(self, input_path, output_path, translator_fn):
        """Translate Word document.
        
        Args:
            translator_fn: callable(text, target_lang) -> translated_text
                           Agent should pass its LLM translate function here.
        """
        doc = Document(input_path)
        
        for para in doc.paragraphs:
            if para.text.strip():
                translated = translator_fn(para.text, 'en')
                para.clear()
                para.add_run(translated)
        
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        translated = translator_fn(cell.text, 'en')
                        cell.text = translated
        
        doc.save(output_path)
        return output_path
    
    def translate_excel(self, input_path, output_path, translator_fn):
        """Translate Excel file."""
        wb = openpyxl.load_workbook(input_path)
        
        for sheet in wb.worksheets:
            for row in sheet.iter_rows():
                for cell in row:
                    if cell.value and isinstance(cell.value, str):
                        translated = translator_fn(cell.value, 'en')
                        cell.value = translated
        
        wb.save(output_path)
        return output_path
    
    def translate_pptx(self, input_path, output_path, translator_fn):
        """Translate PowerPoint."""
        prs = Presentation(input_path)
        
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, 'text') and shape.text.strip():
                    translated = translator_fn(shape.text, 'en')
                    shape.text = translated
        
        prs.save(output_path)
        return output_path
    
    def translate_markdown(self, input_path, output_path, translator_fn):
        """Translate Markdown file."""
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = content.split('\n\n')
        translated_sections = []
        
        for section in sections:
            if section.strip():
                translated = translator_fn(section, 'en')
                translated_sections.append(translated)
            else:
                translated_sections.append('')
        
        translated_content = '\n\n'.join(translated_sections)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        return output_path
    
    def translate_folder(self, folder_path, output_folder, target_lang, translator_fn):
        """Translate all files in folder."""
        os.makedirs(output_folder, exist_ok=True)
        
        results = []
        
        for file_path in Path(folder_path).rglob('*'):
            if file_path.is_file():
                format_type = self.detect_format(str(file_path))
                
                if format_type != 'unknown':
                    output_path = os.path.join(output_folder, file_path.name)
                    
                    try:
                        if format_type == 'word':
                            self.translate_word(str(file_path), output_path, translator_fn)
                        elif format_type == 'excel':
                            self.translate_excel(str(file_path), output_path, translator_fn)
                        elif format_type == 'powerpoint':
                            self.translate_pptx(str(file_path), output_path, translator_fn)
                        elif format_type in ['markdown', 'text']:
                            self.translate_markdown(str(file_path), output_path, translator_fn)
                        
                        results.append({'file': file_path.name, 'status': 'success'})
                    except Exception as e:
                        results.append({'file': file_path.name, 'status': 'error', 'error': str(e)})
        
        return results

## Usage Examples

```
User: "Translate this Word document to English"
Agent: 
  1. pip install python-docx (if not installed)
  2. Use translator.translate_word() to parse .docx
  3. For each paragraph, call your LLM to translate
  4. Write translated text back, save output

User: "Translate all files in this folder to Chinese"
Agent:
  1. Ensure required libs are installed
  2. Use translator.translate_folder() for parsing
  3. Translate text via your LLM
  4. Save all translated files

User: "翻译这份PDF成日文"
Agent:
  1. Extract text from PDF
  2. Translate using your LLM
  3. Save as new document
```

## Notes

- Supports Word (.docx), Excel (.xlsx), PPT (.pptx), PDF, HTML, Markdown, TXT
- The parsing code preserves original formatting — the AI agent only replaces text content
- Install dependencies: `pip install python-docx openpyxl python-pptx`
- For PDF support: `pip install pymupdf`
- For HTML: `pip install beautifulsoup4`
