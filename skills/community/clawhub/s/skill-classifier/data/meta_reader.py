# -*- coding: utf-8 -*-
"""
元数据读取模块
读取 _meta.json，获取版本、作者、依赖等信息
"""
import os
import json
import glob
from typing import Dict, Any, Tuple
import logging
from utils.config import SKILLS_DIR

logger = logging.getLogger(__name__)


def load_all_meta() -> Dict[str, Dict[str, Any]]:
    """
    加载所有技能的 _meta.json
    
    Returns:
        { skill_name: { version, author, requires, ... } }
    """
    meta_data = {}
    
    for meta_file in glob.glob(os.path.join(SKILLS_DIR, "*", "_meta.json")):
        dir_name = os.path.basename(os.path.dirname(meta_file))
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            meta_data[dir_name] = {
                'version': data.get('version', ''),
                'author': data.get('ownerId', ''),
                'requires': data.get('metadata', {}).get('openclaw', {}).get('requires', {}),
                'description': data.get('description', ''),
                'name': data.get('name', dir_name)
            }
            
            # 尝试从 slug 映射
            if 'slug' in data:
                meta_data[data['slug']] = meta_data[dir_name]
                
        except Exception as e:
            logger.warning(f"读取 _meta.json 失败 {meta_file}: {e}")
    
    logger.info(f"加载了 {len(meta_data)} 个技能的元数据")
    return meta_data


def get_meta_info(skill_name: str, meta_data: Dict[str, Dict[str, Any]]) -> Tuple[str, str]:
    """
    获取技能的版本号和作者
    
    Args:
        skill_name: 技能名称
        meta_data: 元数据字典
        
    Returns:
        (version, author)
    """
    info = meta_data.get(skill_name, {})
    return info.get('version', ''), info.get('author', '')
