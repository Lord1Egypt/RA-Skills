"""
Read Word Document Skill

读取Word文档的OpenClaw Skill

使用示例:
    from read_word import read_word_document, search_in_document
    
    # 读取文档
    paragraphs = read_word_document("文档.docx")
    
    # 搜索关键词
    results = search_in_document("文档.docx", ["关键词1", "关键词2"])
"""

from .read_word import (
    read_docx,
    read_doc_ole,
    read_word_document,
    search_in_document,
    save_as_text,
    analyze_document
)

__version__ = '1.0.0'
__author__ = '叶文洁'

__all__ = [
    'read_docx',
    'read_doc_ole', 
    'read_word_document',
    'search_in_document',
    'save_as_text',
    'analyze_document'
]
