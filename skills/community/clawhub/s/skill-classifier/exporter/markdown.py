# -*- coding: utf-8 -*-
"""
Markdown 导出模块
生成分类清晰、带统计、带状态图标的技能列表
"""
import os
from typing import List, Dict, Any
from utils.config import CATEGORY_ORDER, STATUS_ICONS, OUTPUT_DIR
from utils.config import CATEGORY_ORDER
from classifier.category_map import get_category
from utils.translator import translate_description


def generate_category_stats(categories: Dict[tuple, List[Dict[str, Any]]]) -> str:
    """
    生成分类统计摘要
    
    Args:
        categories: 分类后的技能字典
        
    Returns:
        统计摘要 Markdown
    """
    lines = ["## 📈 分类统计", "", "| 分类 | 子类 | 数量 |", "|------|------|------|"]
    
    # 按大类聚合
    big_cat_stats = {}
    for (big_cat, sub_cat), skills in categories.items():
        if big_cat not in big_cat_stats:
            big_cat_stats[big_cat] = {'total': 0, 'sub_cats': {}}
        big_cat_stats[big_cat]['total'] += len(skills)
        big_cat_stats[big_cat]['sub_cats'][sub_cat] = len(skills)
    
    for big_cat in CATEGORY_ORDER:
        if big_cat not in big_cat_stats:
            continue
        stats = big_cat_stats[big_cat]
        first_sub = True
        for sub_cat, count in sorted(stats['sub_cats'].items()):
            if first_sub:
                lines.append(f"| {big_cat} | {sub_cat} | {count} |")
                first_sub = False
            else:
                lines.append(f"| | {sub_cat} | {count} |")
        lines.append(f"| | **小计** | **{stats['total']}** |")
    
    return '\n'.join(lines)


def generate_markdown(skills: List[Dict[str, Any]], title: str, 
                     is_activated: bool = True, include_stats: bool = True) -> str:
    """
    生成 Markdown 格式的技能列表
    
    Args:
        skills: 技能列表
        title: 标题
        is_activated: 是否为已激活技能列表
        include_stats: 是否包含统计摘要
        
    Returns:
        Markdown 字符串
    """
    # 按大类+子类分组
    categories = {}
    for skill in skills:
        cat = get_category(skill['name'])
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(skill)
    
    lines = []
    total = len(skills)
    status_text = "已" if is_activated else "未"
    lines.append(f"# {title}")
    lines.append(f"> 数据来源：openclaw skills list | 共 **{total}** 个{status_text}激活技能")
    lines.append("")
    
    if include_stats and categories:
        lines.append(generate_category_stats(categories))
        lines.append("")
    
    def sort_key(item):
        (big_cat, sub_cat), _ = item
        big_idx = CATEGORY_ORDER.index(big_cat) if big_cat in CATEGORY_ORDER else 999
        return (big_idx, sub_cat)
    
    big_counter = 0
    sub_counter_map = {}
    prev_big = None
    idx = 0
    
    for (big_cat, sub_cat), cat_skills in sorted(categories.items(), key=sort_key):
        if big_cat != prev_big:
            big_counter += 1
            sub_counter_map[big_cat] = 0
            prev_big = big_cat
            lines.append(f"{big_counter}. {big_cat}")
            lines.append("")
        
        sub_counter_map[big_cat] += 1
        sc = sub_counter_map[big_cat]
        lines.append(f"   {big_counter}.{sc} {sub_cat} (共 {len(cat_skills)} 个)")
        lines.append("")
        lines.append("| 序号 | 状态 | 技能名称 | 版本 | 描述 |")
        lines.append("|------|------|----------|------|------|")
        
        for skill in cat_skills:
            idx += 1
            status = skill.get('status', 'unknown')
            icon = STATUS_ICONS.get(status, '❓')
            version = skill.get('version', '')
            desc = translate_description(skill.get('description', ''))
            lines.append(f"| {idx} | {icon} | {skill['name']} | {version} | {desc} |")
        
        lines.append("")
    
    return '\n'.join(lines)


def export_markdown(skills: List[Dict[str, Any]], title: str,
                    is_activated: bool = True, include_stats: bool = True,
                    output_path: str = None) -> str:
    """
    导出 Markdown 文件
    
    Args:
        skills: 技能列表
        title: 标题
        is_activated: 是否为已激活技能
        include_stats: 是否包含统计
        output_path: 输出路径（默认自动生成）
        
    Returns:
        输出文件路径
    """
    content = generate_markdown(skills, title, is_activated, include_stats)
    
    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, f"{title}.md")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path
