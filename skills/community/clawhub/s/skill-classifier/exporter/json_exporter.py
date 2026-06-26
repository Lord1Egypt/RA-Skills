# -*- coding: utf-8 -*-
"""
JSON 导出模块
支持结构化 JSON 输出，方便其他脚本调用
"""
import os
import json
from typing import List, Dict, Any
from utils.config import OUTPUT_DIR, CATEGORY_ORDER
from classifier.category_map import get_category


def export_json(skills: List[Dict[str, Any]], title: str,
                is_activated: bool = True, include_stats: bool = True,
                output_path: str = None, pretty: bool = True) -> str:
    """
    导出 JSON 文件
    
    Args:
        skills: 技能列表
        title: 标题
        is_activated: 是否为已激活技能
        include_stats: 是否包含统计信息
        output_path: 输出路径（默认自动生成）
        pretty: 是否格式化输出
        
    Returns:
        输出文件路径
    """
    data = generate_json_data(skills, title, is_activated, include_stats)
    
    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, f"{title}.json")
    
    indent = 2 if pretty else None
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
    
    return output_path


def generate_json_data(skills: List[Dict[str, Any]], title: str,
                       is_activated: bool = True, 
                       include_stats: bool = True) -> Dict[str, Any]:
    """
    生成结构化的 JSON 数据
    
    Args:
        skills: 技能列表
        title: 标题
        is_activated: 是否为已激活技能
        include_stats: 是否包含统计信息
        
    Returns:
        结构化 JSON 数据
    """
    # 按大类+子类分组
    categories = {}
    for skill in skills:
        cat = get_category(skill['name'])
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(skill)
    
    # 构建分类树
    category_tree = {}
    for (big_cat, sub_cat), cat_skills in categories.items():
        if big_cat not in category_tree:
            category_tree[big_cat] = {}
        category_tree[big_cat][sub_cat] = cat_skills
    
    data = {
        'title': title,
        'is_activated': is_activated,
        'total_count': len(skills),
        'skills': skills,
        'categories': category_tree,
    }
    
    if include_stats:
        data['stats'] = generate_stats(categories, skills)
    
    return data


def generate_stats(categories: Dict[tuple, List[Dict[str, Any]]],
                   all_skills: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成统计信息
    
    Args:
        categories: 分类后的技能字典
        all_skills: 所有技能列表
        
    Returns:
        统计信息字典
    """
    # 大类统计
    big_cat_stats = {}
    sub_cat_stats = {}
    
    for (big_cat, sub_cat), skills in categories.items():
        if big_cat not in big_cat_stats:
            big_cat_stats[big_cat] = 0
        big_cat_stats[big_cat] += len(skills)
        
        if big_cat not in sub_cat_stats:
            sub_cat_stats[big_cat] = {}
        sub_cat_stats[big_cat][sub_cat] = len(skills)
    
    # 状态统计
    status_stats = {}
    for skill in all_skills:
        status = skill.get('status', 'unknown')
        status_stats[status] = status_stats.get(status, 0) + 1
    
    return {
        'by_big_category': big_cat_stats,
        'by_sub_category': sub_cat_stats,
        'by_status': status_stats,
        'total': len(all_skills)
    }


def skills_to_dict(skills: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    将技能列表转换为名称到技能的字典
    
    Args:
        skills: 技能列表
        
    Returns:
        {技能名: 技能数据}
    """
    return {skill['name']: skill for skill in skills}
