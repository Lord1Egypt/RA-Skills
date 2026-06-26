#!/usr/bin/env python3
"""
简单问题修复：确保所有含义相同的简单问题都得到简洁回答
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoding_utils import safe_print
from final_proper_grading import ProperGradingWeather

class SimpleQuestionFix(ProperGradingWeather):
    """修复简单问题识别的版本"""
    
    def _is_simple_question(self, question):
        """修复：更准确地识别简单问题"""
        q = question.lower()
        
        # 扩展的简单问题关键词（兼容更多问法）
        simple_keywords = [
            # 天气相关
            '天气', '天气怎么样', '天气如何', '天气情况',
            # 温度相关
            '冷', '冷不冷', '冷吗', '外面冷', '现在冷',
            '热', '热不热', '热吗', '外面热', '现在热',
            '温度', '多少度', '温度多少', '现在温度',
            # 雨伞相关
            '伞', '带伞', '雨伞', '要不要带伞', '需要带伞', '带伞吗',
            # 降水相关
            '雨', '下雨', '有雨', '下雨吗', '有雨吗', '会下雨吗',
            # 风力相关
            '风', '风力', '风大', '风大吗', '风力大吗', '风大不大',
            # 湿度相关
            '湿度', '湿度怎么样', '湿度如何', '湿度情况',
        ]
        
        # 检查是否是简单问题
        for keyword in simple_keywords:
            if keyword in q:
                return True
        
        # 很短的问题通常是简单问题
        if len(q) <= 12:  # 放宽长度限制
            return True
        
        return False
    
    def _get_city(self, question):
        """修复：更好地移除关键词"""
        text = question.lower()
        
        # 要移除的关键词
        remove_words = [
            '现在', '今天', '明天', '外面', '外面', '当前',
            '吗', '？', '?', '呢', '啊', '呀', '怎么样', '如何',
            '情况', '说说', '详细', '完整', '全面', '报告',
        ]
        
        # 按长度排序，先移除长的
        remove_words.sort(key=len, reverse=True)
        
        for word in remove_words:
            text = text.replace(word, '')
        
        text = text.strip()
        
        if text:
            return self.loc_handler.parse_input(text)
        else:
            location = self.loc_handler.parse_input(self.user_city)
            location.source = "memory"
            return location


# 测试修复效果
def test_fix():
    """测试修复效果"""
    weather = SimpleQuestionFix(user_city="beijing")
    
    # 之前有问题的情况
    problem_cases = [
        "风力大吗？",  # 之前返回完整信息，现在应该简洁
        "有雨吗？",    # 测试
        "需要带伞吗？", # 测试
        "外面热不热？", # 测试
        "现在多少度？", # 测试
    ]
    
    safe_print("修复测试：之前有问题的情况")
    safe_print("=" * 50)
    
    for question in problem_cases:
        safe_print(f"\n问题：{question}")
        answer = weather.ask(question)
        safe_print(f"回答：{answer}")
        
        # 检查是否是简洁回答
        lines = answer.split('\n')
        if len(lines) <= 3:
            safe_print("✅ 简洁回答（修复成功）")
        else:
            safe_print("⚠️ 可能还是完整回答")
        
        safe_print("-" * 40)
    
    # 对比测试
    safe_print("\n\n对比测试：含义相同的问题")
    safe_print("=" * 50)
    
    pairs = [
        ("现在外面冷不冷？", "冷不冷？"),
        ("风力大吗？", "风大吗？"),
        ("需要带伞吗？", "要不要带伞？"),
        ("有雨吗？", "下雨吗？"),
        ("外面热不热？", "热不热？"),
    ]
    
    for q1, q2 in pairs:
        safe_print(f"\n对比：")
        safe_print(f"  {q1}")
        answer1 = weather.ask(q1)
        safe_print(f"  → {answer1}")
        
        safe_print(f"  {q2}")
        answer2 = weather.ask(q2)
        safe_print(f"  → {answer2}")
        
        # 检查是否一致
        if len(answer1.split('\n')) <= 3 and len(answer2.split('\n')) <= 3:
            safe_print("  ✅ 都是简洁回答")
        else:
            safe_print("  ⚠️ 回答不一致")

if __name__ == "__main__":
    test_fix()