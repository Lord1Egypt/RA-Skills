# -*- coding: utf-8 -*-
"""
文件系统扫描模块
扫描 workspace/skills 目录，构建目录名到技能名的映射
"""
import os
from typing import Dict, List, Set
import logging
from utils.config import SKILLS_DIR

logger = logging.getLogger(__name__)


def scan_skills_directory() -> List[Dict[str, str]]:
    """
    扫描技能目录，发现所有包含 SKILL.md 的目录
    
    Returns:
        技能列表，每个元素包含 name, skill_md_path, dir_path
    """
    skills = []
    seen_names: Set[str] = set()
    
    try:
        # 一级目录扫描
        for entry in os.scandir(SKILLS_DIR):
            if not entry.is_dir():
                continue
            if entry.name.startswith('.'):
                continue
                
            # 检查 SKILL.md
            skill_md = os.path.join(entry.path, "SKILL.md")
            if os.path.exists(skill_md):
                if entry.name not in seen_names:
                    skills.append({
                        'name': entry.name,
                        'dir_path': entry.path,
                        'skill_md_path': skill_md
                    })
                    seen_names.add(entry.name)
                continue
                
            # 尝试子目录（嵌套技能）
            for sub_entry in os.scandir(entry.path):
                if not sub_entry.is_dir():
                    continue
                sub_skill_md = os.path.join(sub_entry.path, "SKILL.md")
                if os.path.exists(sub_skill_md):
                    full_name = f"{entry.name}/{sub_entry.name}"
                    if full_name not in seen_names:
                        skills.append({
                            'name': sub_entry.name,
                            'dir_path': sub_entry.path,
                            'skill_md_path': sub_skill_md
                        })
                        seen_names.add(full_name)
                        
    except Exception as e:
        logger.error(f"扫描技能目录失败: {e}")
    
    logger.info(f"文件系统扫描发现 {len(skills)} 个技能")
    return skills


def get_dir_to_name_map() -> Dict[str, str]:
    """
    自动构建目录名到技能名的映射
    替代原来的硬编码 DIR_TO_NAME
    
    Returns:
        目录名到技能名的映射
    """
    mapping = {}
    all_skills = scan_skills_directory()
    
    for skill in all_skills:
        dir_name = os.path.basename(skill['dir_path'])
        mapping[dir_name] = skill['name']
        
    # 常见的别名映射
    common_aliases = {
        'mx-data': 'eastmoney_fin_data',
        'mx-search': 'eastmoney_fin_search',
        'mx-mon': 'eastmoney_stock_simulator',
        'mx-xuangu': 'mx_xuangu',
        'mx-zixuan': 'mx_zixuan',
    }
    mapping.update(common_aliases)
    
    return mapping
