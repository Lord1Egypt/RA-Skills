# -*- coding: utf-8 -*-
"""
自动分类器
基于规则和机器学习自动对新技能进行分类
"""
import os
import json
from typing import Dict, Tuple, List, Any
from collections import Counter
import logging
from classifier.category_map import CATEGORY_MAP, get_category, add_to_category_map
from utils.config import CACHE_DIR

logger = logging.getLogger(__name__)

# 分类学习数据文件
LEARNING_FILE = os.path.join(CACHE_DIR, 'category_learning.json')


def load_learning_data() -> Dict[str, Any]:
    """
    加载历史分类学习数据
    
    Returns:
        学习数据字典
    """
    if os.path.exists(LEARNING_FILE):
        try:
            with open(LEARNING_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"加载分类学习数据失败: {e}")
    
    return {
        'manual_classifications': {},  # 人工确认的分类
        'keyword_stats': {},  # 关键词统计
        'total_classified': 0
    }


def save_learning_data(data: Dict[str, Any]):
    """
    保存分类学习数据
    
    Args:
        data: 学习数据字典
    """
    try:
        with open(LEARNING_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"保存分类学习数据失败: {e}")


def suggest_category(skill_name: str, description: str = "") -> Tuple[Tuple[str, str], float]:
    """
    建议技能的分类
    
    Args:
        skill_name: 技能名称
        description: 技能描述
        
    Returns:
        ((大类, 子类), 置信度)
    """
    # 1. 精确匹配
    if skill_name in CATEGORY_MAP:
        return CATEGORY_MAP[skill_name], 1.0
    
    # 2. 规则匹配
    category = get_category(skill_name)
    if category[0] != "其他":
        return category, 0.8
    
    # 3. 基于描述的关键词匹配
    if description:
        desc_lower = description.lower()
        for keywords, big_cat, sub_cat in []:  # 可以扩展描述关键词
            if any(kw.lower() in desc_lower for kw in keywords):
                return (big_cat, sub_cat), 0.6
    
    # 4. 基于历史统计
    learning_data = load_learning_data()
    if learning_data['total_classified'] > 10:
        # 可以实现更复杂的统计分类
        pass
    
    return ("其他", "其他"), 0.1


def record_manual_classification(skill_name: str, category: Tuple[str, str], description: str = ""):
    """
    记录人工分类结果，用于学习
    
    Args:
        skill_name: 技能名称
        category: (大类, 子类)
        description: 技能描述
    """
    learning_data = load_learning_data()
    learning_data['manual_classifications'][skill_name] = {
        'category': category,
        'description': description
    }
    learning_data['total_classified'] += 1
    
    # 更新分类映射
    add_to_category_map(skill_name, category)
    
    save_learning_data(learning_data)
    logger.info(f"已记录人工分类: {skill_name} -> {category}")


def analyze_skill_patterns() -> Dict[str, Counter]:
    """
    分析技能名称的模式，提取分类关键词
    
    Returns:
        {大类: Counter(关键词)}
    """
    category_keywords: Dict[str, Counter] = {}
    
    for skill_name, (big_cat, sub_cat) in CATEGORY_MAP.items():
        words = skill_name.lower().replace('-', ' ').replace('_', ' ').split()
        if big_cat not in category_keywords:
            category_keywords[big_cat] = Counter()
        category_keywords[big_cat].update(words)
    
    return category_keywords


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
            if desc1 and desc2 and desc1[:20] == desc2[:20]:
                duplicates.append((skill1, skill2, "描述高度相似"))
    
    return duplicates
