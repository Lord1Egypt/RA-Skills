#!/usr/bin/env python3
"""
智能位置匹配模块
自动匹配相似位置或创建新选项
"""

import os
import sys
import difflib
from typing import List, Dict, Optional, Tuple

class LocationMatcher:
    """智能位置匹配器"""
    
    def __init__(self, existing_options: List[str]):
        self.existing_options = existing_options
        self.threshold = 0.7  # 70%相似度阈值
        
    def find_best_match(self, new_location: str) -> Tuple[Optional[str], float]:
        """
        查找最佳匹配的位置选项
        
        Args:
            new_location: 新的位置描述
            
        Returns:
            (匹配的选项, 相似度) 或 (None, 0.0)
        """
        if not self.existing_options:
            return None, 0.0
            
        # 标准化处理
        normalized_new = self._normalize_text(new_location)
        normalized_options = [self._normalize_text(opt) for opt in self.existing_options]
        
        # 使用difflib进行模糊匹配
        best_match = None
        best_ratio = 0.0
        
        for i, option in enumerate(normalized_options):
            ratio = difflib.SequenceMatcher(None, normalized_new, option).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = self.existing_options[i]
                
        if best_ratio >= self.threshold:
            return best_match, best_ratio
        else:
            return None, best_ratio
    
    def should_create_new_option(self, new_location: str) -> bool:
        """判断是否需要创建新选项"""
        best_match, best_ratio = self.find_best_match(new_location)
        return best_ratio < self.threshold
    
    def get_matching_option(self, new_location: str) -> str:
        """
        获取匹配的选项，如果没有则返回原值用于创建新选项
        
        Args:
            new_location: 新的位置描述
            
        Returns:
            匹配的选项或原值
        """
        best_match, best_ratio = self.find_best_match(new_location)
        
        if best_match and best_ratio >= self.threshold:
            print(f"[LOCATION] 匹配到相似选项: '{new_location}' -> '{best_match}' (相似度: {best_ratio:.1%})")
            return best_match
        else:
            print(f"[LOCATION] 无合适匹配，创建新选项: '{new_location}' (最高相似度: {best_ratio:.1%})")
            return new_location
    
    def _normalize_text(self, text: str) -> str:
        """标准化文本用于匹配"""
        if not text:
            return ""
        
        # 中文全角转半角
        text = text.replace('，', ',').replace('。', '.').replace('！', '!').replace('？', '?')
        
        # 移除空格和常见符号
        text = text.strip().lower()
        
        # 移除常见后缀
        suffixes = ['里', '内', '中', '上', '下', '左', '右', '前', '后']
        for suffix in suffixes:
            if text.endswith(suffix):
                text = text[:-1]
                break
                
        return text
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """计算两个文本的相似度"""
        return difflib.SequenceMatcher(None, text1, text2).ratio()

def test_location_matcher():
    """测试函数"""
    # 测试数据
    existing_options = [
        "1号纸箱里",
        "白色行李箱里", 
        "电视柜左抽屉",
        "办公桌抽屉",
        "双肩包内层"
    ]
    
    matcher = LocationMatcher(existing_options)
    
    test_cases = [
        ("1号纸箱", True),          # 应该匹配到"1号纸箱里"
        ("白色行李箱", True),        # 应该匹配到"白色行李箱里"
        ("电视柜左边抽屉", True),     # 应该匹配到"电视柜左抽屉"
        ("蓝色行李箱", False),       # 应该创建新选项
        ("2号纸箱里", False),       # 应该创建新选项
        ("办公桌抽屉", True),        # 应该精确匹配
    ]
    
    print("测试智能位置匹配器:")
    print("=" * 50)
    
    for new_loc, should_match in test_cases:
        best_match, best_ratio = matcher.find_best_match(new_loc)
        result = "匹配" if best_ratio >= 0.7 else "新建"
        
        if best_match:
            print(f"'{new_loc}' -> '{best_match}' ({best_ratio:.1%}, {result})")
        else:
            print(f"'{new_loc}' -> 无匹配 ({best_ratio:.1%}, {result})")

if __name__ == "__main__":
    test_location_matcher()