# -*- coding: utf-8 -*-
"""
差异对比模块
用于增量更新和技能状态变化对比
"""
import os
import json
import hashlib
from typing import Dict, List, Any, Tuple
from datetime import datetime
import logging
from utils.config import CACHE_DIR

logger = logging.getLogger(__name__)

# 快照文件
SNAPSHOT_FILE = os.path.join(CACHE_DIR, 'skill_snapshot.json')
DIFF_HISTORY_FILE = os.path.join(CACHE_DIR, 'diff_history.json')


def generate_skill_hash(skill: Dict[str, Any]) -> str:
    """
    生成技能的哈希值，用于检测变化
    
    Args:
        skill: 技能数据字典
        
    Returns:
        哈希字符串
    """
    data = json.dumps(skill, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def save_snapshot(skills: List[Dict[str, Any]]):
    """
    保存当前技能列表的快照
    
    Args:
        skills: 技能列表
    """
    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'skills': {
            skill['name']: {
                'hash': generate_skill_hash(skill),
                'status': skill.get('status', 'unknown'),
                'version': skill.get('version', ''),
                'description': skill.get('description', '')
            }
            for skill in skills
        }
    }
    
    try:
        with open(SNAPSHOT_FILE, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)
        logger.info(f"已保存技能快照，共 {len(skills)} 个技能")
    except Exception as e:
        logger.error(f"保存快照失败: {e}")


def load_snapshot() -> Dict[str, Any]:
    """
    加载上次的技能快照
    
    Returns:
        快照数据，不存在则返回空字典
    """
    if os.path.exists(SNAPSHOT_FILE):
        try:
            with open(SNAPSHOT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载快照失败: {e}")
    
    return {'timestamp': None, 'skills': {}}


def compare_skills(current: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    对比当前技能与上次快照的差异
    
    Args:
        current: 当前技能列表
        
    Returns:
        {
            'added': [...],  # 新增的技能
            'removed': [...],  # 删除的技能
            'changed': [...],  # 状态变化的技能
            'unchanged': [...]  # 未变化的技能
        }
    """
    snapshot = load_snapshot()
    old_skills = snapshot.get('skills', {})
    current_names = {s['name'] for s in current}
    old_names = set(old_skills.keys())
    
    result = {
        'added': [],
        'removed': [],
        'changed': [],
        'unchanged': []
    }
    
    # 新增的技能
    for skill in current:
        name = skill['name']
        if name not in old_names:
            result['added'].append(skill)
        else:
            # 检查是否变化
            old_info = old_skills[name]
            if old_info.get('status') != skill.get('status') or \
               old_info.get('version') != skill.get('version'):
                result['changed'].append({
                    'name': name,
                    'old': old_info,
                    'new': {
                        'status': skill.get('status'),
                        'version': skill.get('version'),
                        'description': skill.get('description')
                    }
                })
            else:
                result['unchanged'].append(skill)
    
    # 删除的技能
    for name in old_names - current_names:
        result['removed'].append({
            'name': name,
            'old': old_skills[name]
        })
    
    # 记录差异历史
    if any(result.values()):
        _record_diff_history(result, snapshot.get('timestamp'))
    
    return result


def _record_diff_history(diff: Dict[str, List[Dict[str, Any]]], old_timestamp: str):
    """
    记录差异历史
    
    Args:
        diff: 差异结果
        old_timestamp: 旧快照时间戳
    """
    history = _load_diff_history()
    
    record = {
        'timestamp': datetime.now().isoformat(),
        'old_timestamp': old_timestamp,
        'added_count': len(diff['added']),
        'removed_count': len(diff['removed']),
        'changed_count': len(diff['changed']),
        'details': diff
    }
    
    history.insert(0, record)
    
    # 只保留最近 10 条
    history = history[:10]
    
    try:
        with open(DIFF_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存差异历史失败: {e}")


def _load_diff_history() -> List[Dict[str, Any]]:
    """
    加载差异历史
    
    Returns:
        历史记录列表
    """
    if os.path.exists(DIFF_HISTORY_FILE):
        try:
            with open(DIFF_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载差异历史失败: {e}")
    
    return []


def is_incremental_update_needed() -> bool:
    """
    检查是否需要增量更新
    
    Returns:
        True 需要更新，False 不需要
    """
    if not os.path.exists(SNAPSHOT_FILE):
        return True
    
    # 检查快照是否过期（24小时）
    mtime = os.path.getmtime(SNAPSHOT_FILE)
    age = datetime.now().timestamp() - mtime
    
    return age > 24 * 3600  # 24小时


def get_diff_summary(diff: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    生成差异摘要文本
    
    Args:
        diff: 差异结果
        
    Returns:
        摘要文本
    """
    lines = ["## 📊 技能变化摘要"]
    
    if diff['added']:
        lines.append(f"\n### ✅ 新增技能 ({len(diff['added'])})")
        for skill in diff['added']:
            lines.append(f"- {skill['name']}: {skill.get('description', '')}")
    
    if diff['removed']:
        lines.append(f"\n### ❌ 移除技能 ({len(diff['removed'])})")
        for skill in diff['removed']:
            lines.append(f"- {skill['name']}")
    
    if diff['changed']:
        lines.append(f"\n### 🔄 状态变化 ({len(diff['changed'])})")
        for change in diff['changed']:
            old_status = change['old'].get('status', 'unknown')
            new_status = change['new'].get('status', 'unknown')
            lines.append(f"- {change['name']}: {old_status} → {new_status}")
    
    if not any(diff.values()):
        lines.append("\n无变化")
    
    return '\n'.join(lines)
