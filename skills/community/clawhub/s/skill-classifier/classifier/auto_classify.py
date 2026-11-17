# -*- coding: utf-8 -*-
"""
重复技能检测
基于名称模式与描述相似度发现功能重复的技能
"""
from typing import Dict, List, Tuple, Any
from difflib import SequenceMatcher
import logging

logger = logging.getLogger(__name__)


def find_duplicate_skills(skills: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], Dict[str, Any], str]]:
    """
    检测功能重复的技能

    Args:
        skills: 技能列表

    Returns:
        [(skill1, skill2, 原因)]
    """
    duplicates = []
    name_patterns = {
        ('eastmoney', 'mx'): '东方财富 vs 妙想（同功能）',
        ('openai-whisper', 'whisper'): '语音转文本（多实现）',
        ('desearch', 'tavily'): '网络搜索（多引擎）',
        ('playwright', 'browser'): '浏览器自动化（多实现）',
    }

    for i, skill1 in enumerate(skills):
        for j, skill2 in enumerate(skills[i+1:], i+1):
            name1 = skill1['name'].lower()
            name2 = skill2['name'].lower()

            # 检查模式匹配
            for (p1, p2), reason in name_patterns.items():
                if (p1 in name1 and p2 in name2) or (p2 in name1 and p1 in name2):
                    duplicates.append((skill1, skill2, reason))
                    break

            # 检查描述相似度
            desc1 = skill1.get('description', '').lower()
            desc2 = skill2.get('description', '').lower()
            if desc1 and desc2 and len(desc1) >= 20 and len(desc2) >= 20 \
                    and SequenceMatcher(None, desc1, desc2).ratio() >= 0.9:
                duplicates.append((skill1, skill2, "描述高度相似"))

    return duplicates
