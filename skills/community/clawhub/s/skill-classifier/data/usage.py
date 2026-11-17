# -*- coding: utf-8 -*-
"""
技能使用统计
主路：state 库 skill_usage 表；回退：openclaw skills curator status --json
"""
import json
import logging
import os
import sqlite3
import subprocess
from datetime import datetime
from typing import Dict, Optional

from utils.config import STATE_DB

logger = logging.getLogger(__name__)


def _ms_to_iso(ms) -> Optional[str]:
    """毫秒时间戳转 ISO 字符串，无效时返回 None"""
    if not ms:
        return None
    try:
        return datetime.fromtimestamp(int(ms) / 1000).strftime('%Y-%m-%d %H:%M')
    except (ValueError, OSError, OverflowError):
        return None


def _from_state_db() -> Optional[Dict[str, Dict]]:
    """读 state 库 skill_usage 表（只读连接），库不可读时返回 None"""
    if not os.path.exists(STATE_DB):
        return None
    try:
        con = sqlite3.connect(f'file:{STATE_DB}?mode=ro', uri=True)
        try:
            rows = con.execute(
                'SELECT skill_name, use_count, last_used_at_ms FROM skill_usage'
            ).fetchall()
        finally:
            con.close()
    except sqlite3.Error as e:
        logger.warning(f"读取 state 库失败: {e}")
        return None
    stats: Dict[str, Dict] = {}
    for name, count, last_ms in rows:
        if not name:
            continue
        prev = stats.get(name)
        calls = int(count or 0)
        if prev is None or calls > prev['calls']:
            stats[name] = {'calls': calls, 'last_used': _ms_to_iso(last_ms)}
    return stats


def _from_curator() -> Optional[Dict[str, Dict]]:
    """回退路：解析 curator status --json（字段名做防御式兼容）"""
    try:
        out = subprocess.run(
            ['openclaw', 'skills', 'curator', 'status', '--json'],
            capture_output=True, text=True, encoding='utf-8', timeout=60)
    except Exception as e:
        logger.warning(f"curator 调用失败: {e}")
        return None
    if out.returncode != 0:
        return None
    try:
        data = json.loads(out.stdout or '{}')
    except json.JSONDecodeError:
        return None
    stats: Dict[str, Dict] = {}
    for item in data.get('skills') or []:
        if not isinstance(item, dict):
            continue
        name = item.get('name') or item.get('skill') or item.get('slug')
        if not name:
            continue
        calls = item.get('useCount') or item.get('invocations') or item.get('count') or 0
        last = item.get('lastUsedAtMs') or item.get('last_used_at_ms')
        stats[name] = {'calls': int(calls or 0), 'last_used': _ms_to_iso(last)}
    return stats


def get_usage_stats() -> Dict[str, Dict]:
    """
    获取使用统计 {技能名: {calls, last_used}}

    优先 state 库；为空或不可读时回退 curator。
    两路都无数据时返回空 dict。
    """
    stats = _from_state_db()
    if stats:
        logger.info(f"使用统计来源: state 库 skill_usage（{len(stats)} 条）")
        return stats
    stats = _from_curator()
    if stats:
        logger.info(f"使用统计来源: curator（{len(stats)} 条）")
        return stats
    logger.info("暂无使用统计数据（skill_usage 表为空且 curator 无记录）")
    return {}
