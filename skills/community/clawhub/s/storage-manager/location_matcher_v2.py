#!/usr/bin/env python3
"""
改进的智能位置匹配模块
更精确的匹配算法
"""

import os
import sys
import difflib
import re
from typing import List, Dict, Optional, Tuple

class SmartLocationMatcher:
    """智能位置匹配器（改进版）"""
    
    def __init__(self, existing_options: List[str]):
        self.existing_options = existing_options
        self.threshold = 0.7  # 70%相似度阈值
        self.min_length = 2   # 最小匹配长度
        
    def find_best_match(self, new_location: str) -> Tuple[Optional[str], float]:
        """
        查找最佳匹配的位置选项（改进版）
        
        改进点：
        1. 考虑文本长度差异
        2. 使用词级匹配而非字符级
        3. 排除部分匹配过高的干扰
        """
        if not self.existing_options:
            return None, 0.0
        
        # 标准化处理
        normalized_new = self._normalize_location(new_location)
        
        best_match = None
        best_ratio = 0.0
        
        for option in self.existing_options:
            normalized_option = self._normalize_location(option)
            
            # 计算相似度
            ratio = self._calculate_smart_similarity(normalized_new, normalized_option)
            
            # 如果新位置完全包含在选项中，给予更高权重
            if normalized_new in normalized_option:
                ratio = min(1.0, ratio + 0.2)
            
            # 如果选项完全包含在新位置中，也给予更高权重
            if normalized_option in normalized_new:
                ratio = min(1.0, ratio + 0.2)
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = option
                
        if best_ratio >= self.threshold:
            return best_match, best_ratio
        else:
            return None, best_ratio
    
    def _calculate_smart_similarity(self, text1: str, text2: str) -> float:
        """智能相似度计算"""
        # 基本序列匹配
        seq_ratio = difflib.SequenceMatcher(None, text1, text2).ratio()
        
        # 词级匹配
        words1 = set(self._split_words(text1))
        words2 = set(self._split_words(text2))
        
        if not words1 or not words2:
            return seq_ratio
            
        # 计算Jaccard相似度
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            word_ratio = 0.0
        else:
            word_ratio = len(intersection) / len(union)
        
        # 综合两个相似度
        combined_ratio = (seq_ratio * 0.7 + word_ratio * 0.3)
        
        # 惩罚长度差异过大的情况
        length_ratio = min(len(text1), len(text2)) / max(len(text1), len(text2), 1)
        
        return combined_ratio * length_ratio
    
    def _split_words(self, text: str) -> List[str]:
        """智能分词（中文友好）"""
        if not text:
            return []
        
        # 中文常用分隔符
        separators = ['里', '内', '中', '上', '下', '左', '右', '前', '后', '边', '侧', '层']
        
        # 分割文本
        words = []
        current_word = ""
        
        for char in text:
            if char in separators:
                if current_word:
                    words.append(current_word)
                    current_word = ""
                words.append(char)
            else:
                current_word += char
        
        if current_word:
            words.append(current_word)
        
        return [w for w in words if len(w) >= 1]
    
    def _normalize_location(self, location: str) -> str:
        """标准化位置描述"""
        if not location:
            return ""
        
        # 转换为小写
        location = location.lower()
        
        # 移除标点符号
        location = re.sub(r'[，。！？、；：""''()\[\]{}]', '', location)
        
        # 标准化常见词汇
        replacements = {
            '里边': '里',
            '里面': '里',
            '内部': '内',
            '中间': '中',
            '上面': '上',
            '下面': '下',
            '左边': '左',
            '右边': '右',
            '前边': '前',
            '后边': '后',
            '旁边': '旁',
            '侧面': '侧',
            '层间': '层'
        }
        
        for old, new in replacements.items():
            location = location.replace(old, new)
        
        return location.strip()
    
    def get_matching_option(self, new_location: str) -> str:
        """获取匹配的选项"""
        best_match, best_ratio = self.find_best_match(new_location)
        
        if best_match and best_ratio >= self.threshold:
            print(f"[智能匹配] '{new_location}' -> '{best_match}' (相似度: {best_ratio:.1%})")
            return best_match
        else:
            print(f"[智能匹配] 创建新选项: '{new_location}' (最高相似度: {best_ratio:.1%})")
            return new_location

def test_smart_matcher():
    """测试改进的匹配器"""
    existing_options = [
        "1号纸箱里",
        "白色行李箱里", 
        "电视柜左抽屉",
        "办公桌抽屉",
        "双肩包内层",
        "厨房柜子上层"
    ]
    
    matcher = SmartLocationMatcher(existing_options)
    
    test_cases = [
        ("1号纸箱", "1号纸箱里", True),
        ("白色行李箱", "白色行李箱里", True),
        ("电视柜左边抽屉", "电视柜左抽屉", True),
        ("蓝色行李箱", None, False),  # 应该不匹配
        ("2号纸箱", None, False),     # 应该不匹配
        ("办公桌抽屉", "办公桌抽屉", True),
        ("厨房柜子上", "厨房柜子上层", True),
        ("红色行李箱", None, False),  # 应该不匹配
        ("双肩包内", "双肩包内层", True),
    ]
    
    print("测试改进的智能匹配器:")
    print("=" * 60)
    
    for new_loc, expected_match, should_match in test_cases:
        best_match, best_ratio = matcher.find_best_match(new_loc)
        
        match_status = "✅" if (best_match == expected_match) else "❌"
        
        if best_match:
            print(f"{match_status} '{new_loc}' -> '{best_match}' ({best_ratio:.1%})")
        else:
            print(f"{match_status} '{new_loc}' -> 无匹配 ({best_ratio:.1%})")

if __name__ == "__main__":
    test_smart_matcher()