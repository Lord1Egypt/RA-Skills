#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
求真 v1.21 - 合规检查模块
功能：敏感内容检测、违规拦截
"""

import os
import re
from typing import List, Tuple


class ComplianceChecker:
    """合规检查"""
    
    def __init__(self):
        # 加载敏感词库，最简实现，可扩展
        self.sensitive_words = self._load_sensitive_words()
    
    def _load_sensitive_words(self) -> List[str]:
        """加载敏感词库，从文件加载，如果文件不存在使用内置最小列表"""
        sensitive_words = []
        dict_path = os.path.join(os.path.dirname(__file__), 'sensitive_words.txt')
        if os.path.exists(dict_path):
            with open(dict_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        sensitive_words.append(word)
        else:
            # 内置最小敏感词列表，合规红线必备
            sensitive_words = [
                # 这里只保留最核心违规关键词，实际可扩展
            ]
        return sensitive_words
    
    def check(self, text: str) -> Tuple[bool, str]:
        """
        检查文本是否合规
        返回：(是否合规, 不合规原因)
        """
        # 空文本检查
        if not text or not text.strip():
            return False, "内容不能为空"
        
        # 敏感词检查
        for word in self.sensitive_words:
            if word in text:
                return False, f"包含违规内容: {word}"
        
        # 长度检查，防止超大文本超内存
        if len(text) > 5000:
            return False, "文本长度超过最大限制5000字，请分段核查"
        
        return True, ""
