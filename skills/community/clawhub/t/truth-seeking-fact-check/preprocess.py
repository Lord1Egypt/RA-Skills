#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Truth (求真) v1.3 - 文本预处理模块
功能：分词、分句、文本清洗
"""

import re
from typing import List


class TextPreprocessor:
    """文本预处理"""
    
    def __init__(self):
        # 中文分句正则
        self.sentence_pattern = re.compile(r'[^。！？!?；;\n]+[。！!?？；;\n]?')
    
    def clean_text(self, text: str) -> str:
        """文本清洗：去除多余空格空行"""
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def split_sentences(self, text: str) -> List[str]:
        """分句，处理中文"""
        text = self.clean_text(text)
        sentences = self.sentence_pattern.findall(text)
        # 过滤空句子
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def split_paragraphs(self, text: str) -> List[str]:
        """分段"""
        paragraphs = re.split(r'\n\s*\n', text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return paragraphs
