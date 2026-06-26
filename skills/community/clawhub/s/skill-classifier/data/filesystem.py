# -*- coding: utf-8 -*-
"""
文件系统扫描模块
扫描 workspace/skills 目录，发现未注册的技能
"""
import os
import glob
from typing import List, Dict, Set
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
                        seen_names.add(sub_entry.name)
                        
    except Exception as e:
        logger.error(f"扫描技能目录失败: {e}")
    
    logger.info(f"文件系统扫描发现 {len(skills)} 个技能")
    return skills


def read_skill_description(skill_md_path: str) -> str:
    """
    从 SKILL.md 读取描述（第一个标题）
    
    Args:
        skill_md_path: SKILL.md 文件路径
        
    Returns:
        描述字符串
    """
    try:
        with open(skill_md_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    return line.lstrip("#").strip()
    except Exception as e:
        logger.warning(f"读取 SKILL.md 失败 {skill_md_path}: {e}")
    return ""


def get_unregistered_skills(registered_names: Set[str]) -> List[Dict[str, str]]:
    """
    获取未在 OpenClaw 中注册但存在于文件系统的技能
    注意：OpenClaw 已扫描所有技能，此函数主要用于分类映射参考，不建议直接添加到列表
    
    Args:
        registered_names: 已注册的技能名称集合
        
    Returns:
        未注册技能列表
    """
    all_skills = scan_skills_directory()
    unregistered = []
    
    for skill in all_skills:
        name = skill['name']
        if name not in registered_names:
            desc = read_skill_description(skill['skill_md_path'])
            unregistered.append({
                'name': name,
                'description': desc,
                'status': 'ready',
                'dir_path': skill['dir_path']
            })
    
    logger.info(f"发现 {len(unregistered)} 个未注册技能（仅用于参考）")
    return unregistered


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
