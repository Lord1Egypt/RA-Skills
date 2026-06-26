# -*- coding: utf-8 -*-
"""
PDF文件文本提取器
"""

import re
from pathlib import Path
from typing import Optional

try:
    import pdfplumber
except ImportError:
    raise ImportError("pdfplumber >= 0.10.0 is required. Install: pip install pdfplumber")


class PdfExtractor:
    """
    PDF文档文本提取器
    使用pdfplumber进行文本提取
    """
    
    def extract(self, file_path: str) -> str:
        """
        从PDF中提取纯文本
        
        @param file_path: PDF文件路径
        @return: 提取的纯文本
        """
        texts = []
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    texts.append(text)
                    
        return '\n\n'.join(texts)
        
    def extract_with_layout(self, file_path: str) -> dict:
        """
        提取文本并保留布局信息
        
        @param file_path: PDF文件路径
        @return: 包含文本和布局信息的字典
        """
        pages = []
        
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                words = page.extract_words()
                
                pages.append({
                    'page_num': page_num + 1,
                    'text': text,
                    'words': words,
                    'width': page.width,
                    'height': page.height
                })
                
        return {
            'text': '\n\n'.join(p['text'] for p in pages if p['text']),
            'pages': pages,
            'page_count': len(pages),
            'char_count': sum(len(p['text'] or '') for p in pages)
        }
        
    def extract_tables(self, file_path: str) -> list:
        """
        提取PDF中的表格
        
        @param file_path: PDF文件路径
        @return: 表格列表
        """
        tables = []
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)
                    
        return tables
