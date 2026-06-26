# -*- coding: utf-8 -*-
"""
文本清洗模块
清理文本中的无关字符，保留核心内容
"""

import re
import unicodedata


class TextCleaner:
    """
    文本清洗器
    去除噪声字符，统一格式
    """
    
    def __init__(self):
        # 中文标点符号映射
        self.punc_map = {
            '，': ',',
            '。': '.',
            '！': '!',
            '？': '?',
            '：': ':',
            '；': ';',
            '"': '"',
            '"': '"',
            ''': "'",
            ''': "'",
            '（': '(',
            '）': ')',
            '【': '[',
            '】': ']',
            '《': '<',
            '》': '>',
            '——': '-',
            '…': '...'
        }
        
    def clean(self, text: str) -> str:
        """
        清洗文本
        
        @param text: 原始文本
        @return: 清洗后的文本
        """
        if not text:
            return ""
            
        # 替换中文标点
        for cn_punc, en_punc in self.punc_map.items():
            text = text.replace(cn_punc, en_punc)
            
        # 去除Unicode控制字符
        text = ''.join(
            c for c in text 
            if not unicodedata.category(c).startswith('C') 
            or c in '\n\t '
        )
        
        # 去除多余空白
        text = re.sub(r'[ \t]+', ' ', text)  # 多个空格变一个
        text = re.sub(r'\n{3,}', '\n\n', text)  # 超过两个换行变两个
        text = re.sub(r'^\s+|\s+$', '', text)  # 去除首尾空白
        
        return text
        
    def normalize(self, text: str) -> str:
        """
        标准化文本用于比对
        
        @param text: 原始文本
        @return: 标准化后的文本
        """
        # 转小写
        text = text.lower()
        
        # 去除数字
        text = re.sub(r'\d+', '', text)
        
        # 去除特殊字符，保留中文、英文、空格
        text = re.sub(r'[^\u4e00-\u9fff\s\w]', '', text)
        
        # 去除多余空格
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
        
    def remove_punctuation(self, text: str) -> str:
        """
        去除所有标点符号
        
        @param text: 原始文本
        @return: 去除标点后的文本
        """
        return re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        
    def split_sentences(self, text: str) -> list:
        """
        将文本分割成句子
        
        @param text: 原始文本
        @return: 句子列表
        """
        # 按照常见句子结束符分割
        sentences = re.split(r'[.!?。！？]+', text)
        return [s.strip() for s in sentences if s.strip()]
