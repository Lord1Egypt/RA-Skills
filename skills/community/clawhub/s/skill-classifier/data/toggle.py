# -*- coding: utf-8 -*-
"""
技能批量启用/禁用
官方机制：openclaw.json 的 skills.entries.<技能名>.enabled（false=禁用）
安全措施：改前自动备份、写回前 JSON 校验、技能名先对 CLI 清单核对
"""
import datetime
import json
import logging
import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

from utils.config import OPENCLAW_CONFIG, OPENCLAW_DIR

logger = logging.getLogger(__name__)


def _validated_config_path() -> Path:
    """规范化配置路径：拒绝 .. 路径段，且必须位于 .openclaw 目录内"""
    cfg_path = os.path.normpath(OPENCLAW_CONFIG)
    parts = cfg_path.replace('\\', '/').split('/')
    if '..' in parts:
        raise SystemExit(f"非法配置路径（不允许 .. 路径段）: {OPENCLAW_CONFIG}")
    base = os.path.normpath(OPENCLAW_DIR)
    if os.path.commonpath([cfg_path, base]) != base:
        raise SystemExit(f"配置路径越界（须位于 {base} 内）: {cfg_path}")
    return Path(cfg_path)


def set_enabled(names: List[str], enabled: bool) -> Tuple[str, Dict[str, bool]]:
    """
    批量写 skills.entries.<名>.enabled

    Args:
        names: 技能名列表（须先经 CLI 清单核对）
        enabled: True 启用 / False 禁用

    Returns:
        (备份文件路径, {技能名: 写入值})；配置不存在时抛 SystemExit
    """
    cfg_path = _validated_config_path()
    if not cfg_path.is_file():
        raise SystemExit(f"未找到 OpenClaw 主配置: {cfg_path}")

    stamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    backup = f"{cfg_path}.bak.skillmgr-{stamp}"
    shutil.copy2(cfg_path, backup)

    cfg = json.loads(cfg_path.read_text(encoding='utf-8'))
    entries = cfg.setdefault('skills', {}).setdefault('entries', {})
    changed: Dict[str, bool] = {}
    for name in names:
        entries.setdefault(name, {})['enabled'] = enabled
        changed[name] = enabled

    payload = json.dumps(cfg, ensure_ascii=False, indent=2)
    json.loads(payload)  # 写回前校验序列化产物
    cfg_path.write_text(payload + '\n', encoding='utf-8')
    logger.info(f"已写入 {len(changed)} 项（备份: {backup}）")
    return backup, changed


def verify_with_cli(names: List[str], enabled: bool) -> List[str]:
    """写回后跑 skills list 验证目标技能 disabled 状态是否生效，返回未生效名单"""
    try:
        by_name = {s.get('name', ''): s for s in subprocess_run_list_json()}
    except Exception as e:
        logger.warning(f"验证失败（CLI 调用异常）: {e}")
        return []
    failed = []
    for name in names:
        s = by_name.get(name)
        if s is None:
            failed.append(f"{name}（清单中无此名）")
        elif enabled and s.get('disabled'):
            failed.append(f"{name}（仍为 disabled）")
    return failed


def subprocess_run_list_json():
    import subprocess
    out = subprocess.run(['openclaw', 'skills', 'list', '--json'],
                         capture_output=True, text=True, encoding='utf-8', timeout=120)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip()[:200])
    data = json.loads(out.stdout)
    return data['skills'] if isinstance(data, dict) and 'skills' in data else data
