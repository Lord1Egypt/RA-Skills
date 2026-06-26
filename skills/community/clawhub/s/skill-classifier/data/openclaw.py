# -*- coding: utf-8 -*-
"""
OpenClaw CLI 数据获取模块
封装 openclaw skills list 命令，增加错误处理和重试机制
"""
import subprocess
import json
import re
from typing import List, Dict, Any, Optional
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def clean_json_text(text: str) -> str:
    """清理 JSON 文本中的特殊字符"""
    if not text:
        return ""
    if text.startswith('\ufeff'):
        text = text[1:]
    text = re.sub(r'[\ue000-\uf8ff]', '', text)
    return text


def get_skills_from_cli(max_retries: int = 3) -> Optional[List[Dict[str, Any]]]:
    """
    执行 openclaw skills list --json 获取技能列表
    带重试机制和错误处理
    
    Args:
        max_retries: 最大重试次数
        
    Returns:
        技能列表，失败返回 None
    """
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                'openclaw skills list --json',
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=60,
                shell=True
            )
            
            if result.returncode == 0:
                try:
                    cleaned = clean_json_text(result.stdout)
                    data = json.loads(cleaned)
                    # OpenClaw 返回的是对象，skills 在 data['skills'] 中
                    if isinstance(data, dict) and 'skills' in data:
                        skills = data['skills']
                    else:
                        skills = data
                    logger.info(f"成功获取 {len(skills)} 个技能数据")
                    return skills
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON 解析失败（尝试 {attempt + 1}/{max_retries}）: {e}")
                    # 尝试从 stdout 中提取 JSON 部分
                    match = re.search(r'\{.*\}', result.stdout, re.DOTALL)
                    if match:
                        try:
                            data = json.loads(match.group(0))
                            if isinstance(data, dict) and 'skills' in data:
                                skills = data['skills']
                            else:
                                skills = data
                            logger.info(f"成功提取 {len(skills)} 个技能数据")
                            return skills
                        except:
                            pass
            else:
                logger.warning(f"命令执行失败（尝试 {attempt + 1}/{max_retries}）: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            logger.warning(f"命令超时（尝试 {attempt + 1}/{max_retries}）")
        except Exception as e:
            logger.error(f"未知错误（尝试 {attempt + 1}/{max_retries}）: {e}")
    
    logger.error(f"执行 {max_retries} 次后仍然失败，无法获取技能列表")
    return None


def get_skill_status(skill: Dict[str, Any]) -> str:
    """
    获取技能状态
    
    Args:
        skill: 技能数据字典
        
    Returns:
        状态字符串: ready / needsetup / disabled / unknown
    """
    # 正确的状态判断逻辑:
    # 1. disabled=true → disabled
    # 2. 否则，如果有缺失依赖 (missing.bins/env/config/os) → needsetup
    # 3. 否则 → ready
    is_disabled = skill.get('disabled', False)
    
    if is_disabled:
        return 'disabled'
    
    # 检查是否有缺失的依赖
    missing = skill.get('missing', {})
    has_missing_deps = (
        bool(missing.get('bins', [])) or
        bool(missing.get('env', [])) or
        bool(missing.get('config', [])) or
        bool(missing.get('os', []))
    )
    
    if has_missing_deps:
        return 'needsetup'
    else:
        return 'ready'


def get_activated_skills(skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """筛选已激活技能"""
    return [s for s in skills if get_skill_status(s) == 'ready']


def get_not_activated_skills(skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """筛选未激活技能"""
    return [s for s in skills if get_skill_status(s) != 'ready']
