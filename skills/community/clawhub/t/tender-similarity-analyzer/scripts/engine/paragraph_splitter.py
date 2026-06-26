# -*- coding: utf-8 -*-
"""
段落分割模块
将文本按段落结构分割，便于逐段查重
"""

import re
from typing import List, Dict, Tuple


class ParagraphSplitter:
    """
    段落分割器
    将文档文本分割成结构化的段落
    """
    
    def __init__(self, min_para_len: int = 10, max_para_len: int = 5000):
        """
        @param min_para_len: 最小段落长度（字符数）
        @param max_para_len: 最大段落长度（字符数）
        """
        self.min_para_len = min_para_len
        self.max_para_len = max_para_len
        
    def split(self, text: str) -> List[Dict]:
        """
        将文本分割成段落
        
        @param text: 原始文本
        @return: 段落列表，每个段落包含索引、文本、位置信息
        """
        if not text:
            return []
            
        raw_paragraphs = text.split('\n\n')
        paragraphs = []
        
        for idx, para_text in enumerate(raw_paragraphs):
            para_text = para_text.strip()
            
            if len(para_text) < self.min_para_len:
                continue
                
            # 如果段落过长，进一步分割
            if len(para_text) > self.max_para_len:
                sub_paras = self._split_long_paragraph(para_text)
                for sub_idx, sub_text in enumerate(sub_paras):
                    paragraphs.append({
                        'index': len(paragraphs),
                        'text': sub_text,
                        'original_index': idx,
                        'sub_index': sub_idx,
                        'char_count': len(sub_text)
                    })
            else:
                paragraphs.append({
                    'index': idx,
                    'text': para_text,
                    'original_index': idx,
                    'sub_index': 0,
                    'char_count': len(para_text)
                })
                
        return paragraphs
        
    def _split_long_paragraph(self, text: str) -> List[str]:
        """
        分割过长的段落
        
        @param text: 长段落文本
        @return: 分割后的子段落列表
        """
        # 尝试按句子分割
        sentences = re.split(r'([.!?。！？]+)', text)
        sub_paras = []
        current = ''
        
        for i in range(0, len(sentences) - 1, 2):
            sent = sentences[i] + sentences[i + 1]
            
            if len(current) + len(sent) <= self.max_para_len:
                current += sent
            else:
                if current:
                    sub_paras.append(current.strip())
                current = sent
                
        if current.strip():
            sub_paras.append(current.strip())
            
        return sub_paras if sub_paras else [text]
        
    def split_by_lines(self, text: str) -> List[Dict]:
        """
        按行分割（保留换行信息）
        
        @param text: 原始文本
        @return: 行列表
        """
        lines = text.split('\n')
        paragraphs = []
        
        current_para = ''
        current_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # 空行表示段落分隔
            if not stripped:
                if current_para:
                    paragraphs.append({
                        'index': len(paragraphs),
                        'text': current_para.strip(),
                        'lines': current_lines,
                        'char_count': len(current_para)
                    })
                    current_para = ''
                    current_lines = []
                continue
                
            current_para += line + '\n'
            current_lines.append(line)
            
        # 处理最后一个段落
        if current_para.strip():
            paragraphs.append({
                'index': len(paragraphs),
                'text': current_para.strip(),
                'lines': current_lines,
                'char_count': len(current_para)
            })
            
        return paragraphs
        
    def merge_short_paragraphs(self, paragraphs: List[Dict], merge_threshold: int = 3) -> List[Dict]:
        """
        合并过短的段落
        
        @param paragraphs: 段落列表
        @param merge_threshold: 合并阈值
        @return: 合并后的段落列表
        """
        if not paragraphs:
            return []
            
        merged = []
        current = paragraphs[0].copy()
        consecutive_short = 0
        
        for i in range(1, len(paragraphs)):
            para = paragraphs[i]
            
            if para['char_count'] < self.min_para_len:
                consecutive_short += 1
            else:
                consecutive_short = 0
                
            if consecutive_short >= merge_threshold:
                # 合并段落
                current['text'] += '\n\n' + para['text']
                current['char_count'] += para['char_count']
                current['end_index'] = para['index']
            else:
                if current not in merged:
                    merged.append(current)
                current = para.copy()
                consecutive_short = 0
                
        if current and current not in merged:
            merged.append(current)
            
        # 重新编号
        for idx, para in enumerate(merged):
            para['index'] = idx
            
        return merged
