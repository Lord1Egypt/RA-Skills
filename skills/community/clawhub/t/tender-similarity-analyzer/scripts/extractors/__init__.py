# -*- coding: utf-8 -*-
"""
文件提取器模块
"""

from .docx_extractor import DocxExtractor
from .pdf_extractor import PdfExtractor
from .txt_extractor import TxtExtractor

__all__ = ['DocxExtractor', 'PdfExtractor', 'TxtExtractor']
