#!/usr/bin/env python3
"""
需求文档提取工具
从 txt/docx/pdf 文件中提取需求描述
"""

import sys
import os

def extract_from_txt(file_path):
    """从 txt 文件提取内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_from_docx(file_path):
    """从 docx 文件提取内容"""
    try:
        from docx import Document
        doc = Document(file_path)
        content = []
        for para in doc.paragraphs:
            if para.text.strip():
                content.append(para.text)
        return '\n'.join(content)
    except ImportError:
        return "错误：需要安装 python-docx 库 (pip install python-docx)"
    except Exception as e:
        return f"错误：{str(e)}"

def extract_from_pdf(file_path):
    """从 pdf 文件提取内容"""
    try:
        import pdfplumber
        content = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    content.append(text)
        return '\n'.join(content)
    except ImportError:
        return "错误：需要安装 pdfplumber 库 (pip install pdfplumber)"
    except Exception as e:
        return f"错误：{str(e)}"

def extract_requirements(file_path):
    """根据文件类型提取需求内容"""
    if not os.path.exists(file_path):
        return f"错误：文件不存在 - {file_path}"
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.txt':
        return extract_from_txt(file_path)
    elif ext in ['.docx', '.doc']:
        return extract_from_docx(file_path)
    elif ext == '.pdf':
        return extract_from_pdf(file_path)
    else:
        return f"错误：不支持的文件格式 - {ext}\n支持的格式：.txt, .docx, .pdf"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python extract_requirements.py <文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    content = extract_requirements(file_path)
    print(content)
