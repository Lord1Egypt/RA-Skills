# -*- coding: utf-8 -*-
"""
Markdown 导出模块
生成分类清晰、带统计、带状态图标的技能列表
"""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from utils.config import CATEGORY_ORDER, STATUS_ICONS, OUTPUT_DIR
from classifier.category_map import get_category
from data.deps import render_mermaid


def _name_cell(skill: Dict) -> str:
    """技能名单元格：带 emoji 与主页链接（如有）"""
    emoji = skill.get('emoji') or ''
    label = f"{emoji} {skill['name']}".strip()
    homepage = skill.get('homepage') or ''
    return f"[{label}]({homepage})" if homepage else label


def _source_cell(skill: Dict) -> str:
    """来源短格式：去掉 openclaw- 前缀"""
    return str(skill.get('source') or '').replace('openclaw-', '')


def _desc_cell(skill: Dict, limit: int = 120) -> str:
    """描述单元格：压平换行/制表符并截断，防止多行长描述破坏 Markdown 表格"""
    desc = str(skill.get('description') or '')
    flat = ' '.join(desc.split())
    if len(flat) > limit:
        flat = flat[:limit].rstrip() + '…'
    return flat


def generate_category_stats(categories: Dict[tuple, List]) -> str:
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


def generate_deps_section(edges: List[Dict[str, str]]) -> str:
    """生成缺失依赖关系章节（mermaid 图 + 说明行）"""
    if not edges:
        return ''
    lines = ["", "## 🔗 缺失依赖关系", "",
             f"> 共 {len(edges)} 条缺失依赖边，指向的 bin/env/config/os 即技能进入 Ready 状态所需项",
             "", render_mermaid(edges), ""]
    return '\n'.join(lines)


def generate_markdown(skills: List[Dict[str, Any]], title: str,
                      is_activated: bool = True, include_stats: bool = True,
                      usage: Optional[Dict] = None,
                      deps_edges: Optional[List[Dict[str, str]]] = None) -> str:
    """
    生成 Markdown 格式的技能列表

    Args:
        skills: 技能列表
        title: 标题
        is_activated: 是否为已激活技能列表
        include_stats: 是否包含统计摘要
        usage: 使用统计 {技能名: {calls, last_used}}（None 则不含调用量列）
        deps_edges: 缺失依赖边（None 则不含依赖关系章节）

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

    if deps_edges:
        lines.append(generate_deps_section(deps_edges))

    def sort_key(item):
        (big_cat, sub_cat), _ = item
        big_idx = CATEGORY_ORDER.index(big_cat) if big_cat in CATEGORY_ORDER else 999
        return (big_idx, sub_cat)

    big_counter = 0
    sub_counter_map = {}
    prev_big = None
    idx = 0

    usage_col = usage is not None
    header = "| 序号 | 状态 | 技能名称 | 版本 | 来源 | 调用量 | 描述 |" if usage_col \
        else "| 序号 | 状态 | 技能名称 | 版本 | 来源 | 描述 |"
    sep = "|------|------|----------|------|------|------|------|" if usage_col \
        else "|------|------|----------|------|------|------|"

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
        lines.append(header)
        lines.append(sep)

        for skill in cat_skills:
            idx += 1
            status = skill.get('status', 'unknown')
            icon = STATUS_ICONS.get(status, '❓')
            version = skill.get('version', '')
            desc = _desc_cell(skill)
            if usage_col:
                calls = (usage.get(skill['name']) or {}).get('calls')
                lines.append(f"| {idx} | {icon} | {_name_cell(skill)} | {version} | "
                             f"{_source_cell(skill)} | {calls if calls is not None else '-'} | {desc} |")
            else:
                lines.append(f"| {idx} | {icon} | {_name_cell(skill)} | {version} | "
                             f"{_source_cell(skill)} | {desc} |")

        lines.append("")

    return '\n'.join(lines)


def export_markdown(skills: List[Dict[str, Any]], title: str,
                    is_activated: bool = True, include_stats: bool = True,
                    output_path: str = None, usage: Optional[Dict] = None,
                    deps_edges: Optional[List[Dict[str, str]]] = None) -> str:
    """
    导出 Markdown 文件

    Args:
        skills: 技能列表
        title: 标题
        is_activated: 是否为已激活技能
        include_stats: 是否包含统计
        output_path: 输出路径（默认自动生成）
        usage: 使用统计（None 则不含调用量列）
        deps_edges: 缺失依赖边（None 则不含依赖关系章节）

    Returns:
        输出文件路径
    """
    content = generate_markdown(skills, title, is_activated, include_stats,
                                usage=usage, deps_edges=deps_edges)

    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, f"{title}.md")

    Path(output_path).write_text(content, encoding='utf-8')

    return output_path
