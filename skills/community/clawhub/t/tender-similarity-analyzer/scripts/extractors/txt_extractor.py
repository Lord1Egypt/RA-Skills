# -*- coding: utf-8 -*-
"""
纯文本和Markdown文件提取器
"""

import re
from pathlib import Path
from typing import Optional


class TxtExtractor:
    """
    纯文本文件提取器
    支持 .txt 和 .md 文件
    """
    
    def extract(self, file_path: str) -> str:
        """
        提取纯文本内容
        
        @param file_path: 文件路径
        @return: 提取的文本
        """
        encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
                
        # 最后尝试二进制读取后解码
        with open(file_path, 'rb') as f:
            return f.read().decode('utf-8', errors='ignore')
            
    def extract_markdown(self, file_path: str) -> str:
        """
        提取Markdown内容（去除格式标记）
        
        @param file_path: Markdown文件路径
        @return: 纯文本内容
        """
        content = self.extract(file_path)
        
        # 去除Markdown格式标记
        lines = []
        
        for line in content.split('\n'):
            # 去除标题标记
            line = re.sub(r'^#{1,6}\s+', '', line)
            
            # 去除加粗、斜体标记
            line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
            line = re.sub(r'\*(.+?)\*', r'\1', line)
            line = re.sub(r'__(.+?)__', r'\1', line)
            line = re.sub(r'_(.+?)_', r'\1', line)
            
            # 去除链接
            line = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', line)
            
            # 去除图片
            line = re.sub(r'!\[.*?\]\(.+?\)', '', line)
            
            # 去除代码块标记
            line = re.sub(r'^```.*$', '', line)
            line = re.sub(r'`(.+?)`', r'\1', line)
            
            # 去除列表标记
            line = re.sub(r'^[\*\-\+]\s+', '- ', line)
            line = re.sub(r'^\d+\.\s+', '', line)
            
            lines.append(line)
            
        return '\n'.join(lines)
        
    def extract_with_metadata(self, file_path: str) -> dict:
        """
        提取文本和元数据
        
        @param file_path: 文件路径
        @return: 包含文本和元数据的字典
        """
        import os
        
        content = self.extract(file_path)
        path = Path(file_path)
        
        # 分割段落
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        return {
            'text': content,
            'paragraphs': paragraphs,
            'paragraph_count': len(paragraphs),
            'char_count': len(content),
            'file_name': path.name,
            'file_size': os.path.getsize(file_path),
            'extension': path.suffix
        }
