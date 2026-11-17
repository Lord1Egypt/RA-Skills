# -*- coding: utf-8 -*-
"""
技能更新检查（只报告，不自动升级）
- git 安装：对比本地 HEAD 或安装记录 commit 与远端默认分支
- ClawHub 安装：提示由 openclaw skills update --all 管理
"""
import json
import logging
import os
import subprocess
from typing import Any, Dict, List
from urllib.parse import urlparse

from utils.config import SKILLS_DIR

logger = logging.getLogger(__name__)


def _safe_git_url(url: str) -> bool:
    """git 远端须为 https 公网地址（拒绝明文与本机/内网目标）"""
    parsed = urlparse(url)
    if parsed.scheme != 'https' or not parsed.hostname:
        return False
    host = parsed.hostname
    if host == 'localhost' or host.endswith('.local'):
        return False
    parts = host.split('.')
    if len(parts) == 4 and all(p.isdigit() for p in parts):
        if parts[0] in ('10', '127') or (parts[0] == '192' and parts[1] == '168') \
                or (parts[0] == '172' and parts[1].isdigit() and 16 <= int(parts[1]) <= 31):
            return False
    return True


def _local_head(skill_dir: str) -> str:
    """技能目录是 git 仓库时返回本地 HEAD，否则空串"""
    if not os.path.isdir(os.path.join(skill_dir, '.git')):
        return ''
    try:
        out = subprocess.run(['git', '-C', skill_dir, 'rev-parse', 'HEAD'],
                             capture_output=True, text=True, timeout=30)
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception as e:
        logger.warning(f"读取本地 HEAD 失败 {skill_dir}: {e}")
    return ''


def _remote_head(url: str) -> str:
    """远端默认分支 HEAD，失败返回空串"""
    try:
        out = subprocess.run(['git', 'ls-remote', url, 'HEAD'],
                             capture_output=True, text=True, timeout=60)
        if out.returncode == 0 and out.stdout:
            return out.stdout.split()[0]
    except Exception as e:
        logger.warning(f"ls-remote 失败 {url}: {e}")
    return ''


def check_updates(skills: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    检查可更新技能

    Args:
        skills: openclaw skills list --json 的原始列表（用于识别 ClawHub 轨）

    Returns:
        [{skill, track, status, detail}]；status: up_to_date / outdated / managed / unknown
    """
    results: List[Dict[str, str]] = []

    for s in skills:
        if 'clawhub' in str(s.get('source', '')).lower():
            results.append({'skill': s.get('name', ''), 'track': 'clawhub',
                            'status': 'managed', 'detail': '由 openclaw skills update --all 管理'})

    if not os.path.isdir(SKILLS_DIR):
        return results
    for entry in sorted(os.listdir(SKILLS_DIR)):
        skill_dir = os.path.join(SKILLS_DIR, entry)
        origin_file = os.path.join(skill_dir, '.openclaw', 'source-origin.json')
        if not os.path.isfile(origin_file):
            continue
        try:
            with open(origin_file, 'r', encoding='utf-8') as f:
                origin = json.load(f)
        except Exception as e:
            logger.warning(f"读取安装记录失败 {origin_file}: {e}")
            continue
        git_info = origin.get('git') or {}
        url = git_info.get('url', '')
        if not url or not _safe_git_url(url):
            results.append({'skill': entry, 'track': 'git', 'status': 'unknown',
                            'detail': '安装记录缺少可用 https 远端地址'})
            continue
        remote = _remote_head(url)
        if not remote:
            results.append({'skill': entry, 'track': 'git', 'status': 'unknown',
                            'detail': f'无法获取远端 HEAD: {url}'})
            continue
        local = _local_head(skill_dir) or git_info.get('commit', '')
        if not local:
            results.append({'skill': entry, 'track': 'git', 'status': 'unknown',
                            'detail': '本地无 HEAD 也无安装 commit 记录'})
        elif local == remote:
            results.append({'skill': entry, 'track': 'git', 'status': 'up_to_date',
                            'detail': f'与远端一致 ({local[:7]})'})
        else:
            results.append({'skill': entry, 'track': 'git', 'status': 'outdated',
                            'detail': f'本地 {local[:7]} -> 远端 {remote[:7]}，可 git pull 更新'})
    return results
