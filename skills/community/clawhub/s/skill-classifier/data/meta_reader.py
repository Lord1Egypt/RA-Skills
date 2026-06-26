# -*- coding: utf-8 -*-
"""
元数据读取模块
读取 _meta.json，获取版本、作者、依赖等信息
"""
import os
import json
import glob
from typing import Dict, Any, List, Tuple
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


def check_dependencies(skill_name: str, meta_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    检查技能的依赖是否满足
    
    Args:
        skill_name: 技能名称
        meta_data: 元数据字典
        
    Returns:
        { satisfied: bool, missing: List[str], requires: Dict }
    """
    import shutil
    
    info = meta_data.get(skill_name, {})
    requires = info.get('requires', {})
    bins = requires.get('bins', [])
    envs = requires.get('env', [])
    
    missing_bins = [b for b in bins if not shutil.which(b)]
    missing_envs = [e for e in envs if e not in os.environ]
    
    satisfied = len(missing_bins) == 0 and len(missing_envs) == 0
    
    return {
        'satisfied': satisfied,
        'missing_bins': missing_bins,
        'missing_envs': missing_envs,
        'requires': requires
    }


def get_install_time(dir_path: str) -> float:
    """
    获取技能的安装时间（目录创建时间）
    
    Args:
        dir_path: 技能目录路径
        
    Returns:
        时间戳（秒）
    """
    try:
        return os.path.getctime(dir_path)
    except:
        return 0


def get_dir_size(dir_path: str) -> int:
    """
    获取目录大小（字节）
    
    Args:
        dir_path: 技能目录路径
        
    Returns:
        目录总大小（字节）
    """
    total = 0
    try:
        for entry in os.scandir(dir_path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    except:
        pass
    return total


def format_dir_size(size_bytes: int) -> str:
    """
    格式化目录大小为可读字符串
    
    Args:
        size_bytes: 字节数
        
    Returns:
        格式化后的字符串（如 "12.5 KB"）
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
