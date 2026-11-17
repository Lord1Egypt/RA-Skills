# -*- coding: utf-8 -*-
"""V1.0.5 版本升级迁移模块

核心职责：在版本升级时自动保留用户正在制作的项目记忆记录，
并在升级完成后引导用户恢复未完成的工作。

工作流程：
1. Skill 启动时，检查本地记录的版本号（output/version_manifest.json）
2. 若本地版本号 < config.VERSION，说明发生了版本升级：
   a. 自动备份 output/ 下的所有用户数据到 output_backup_<时间戳>/
   b. 加载项目记忆，提示用户有未完成的工作可恢复
   c. 更新本地版本号为当前版本
3. 若本地版本号 == config.VERSION，正常启动
4. 若本地版本号 > config.VERSION（罕见，可能回滚），仅记录日志

版本升级时不会删除任何用户数据，只做「备份 + 记忆加载 + 版本号更新」三步。
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from core.project_memory import (
    save_project_memory,
    load_project_memory,
    has_pending_work,
    get_last_feature,
    get_last_args,
    get_last_result_files,
    backup_user_data_before_upgrade,
)

# 版本清单文件：记录上次运行的版本号
VERSION_MANIFEST_FILE = config.OUTPUT_DIR / "version_manifest.json"


def check_version_upgrade() -> Dict[str, Any]:
    """检测是否发生了版本升级，并执行对应的迁移流程

    Returns:
        {
            "upgraded": bool,           # 是否检测到版本升级
            "previous_version": str,    # 升级前的版本号
            "current_version": str,     # 当前版本号
            "backup_path": str,         # 备份目录路径（若有）
            "has_pending_work": bool,   # 是否有未完成的工作
            "last_feature": str,        # 上次执行的功能
            "last_args": dict,          # 上次的参数
            "last_result_files": list,  # 上次的输出文件
            "message": str,             # 给用户的提示信息
        }
    """
    current_version = getattr(config, "VERSION", "unknown")
    previous_version = _read_manifest_version()

    result = {
        "upgraded": False,
        "previous_version": previous_version,
        "current_version": current_version,
        "backup_path": "",
        "has_pending_work": False,
        "last_feature": "",
        "last_args": {},
        "last_result_files": [],
        "message": "",
    }

    # 首次运行（无版本记录），直接写入当前版本号
    if not previous_version:
        _write_manifest_version(current_version)
        result["message"] = f"首次运行，已记录版本号 v{current_version}"
        return result

    # 版本相同，无需迁移
    if previous_version == current_version:
        return result

    # 检测到版本变化
    is_upgrade = _compare_versions(current_version, previous_version) > 0
    result["upgraded"] = is_upgrade

    if is_upgrade:
        # === 版本升级流程 ===
        print(f"\n{'='*60}", flush=True)
        print(f"  🎉 检测到版本升级：v{previous_version} → v{current_version}", flush=True)
        print(f"{'='*60}", flush=True)

        # 1. 备份用户数据（output/ 整个目录）
        print(f"  📦 正在备份用户数据...", flush=True)
        backup_path = backup_user_data_before_upgrade()
        if backup_path:
            result["backup_path"] = backup_path
            print(f"  ✅ 备份完成：{backup_path}", flush=True)
        else:
            print(f"  ⚠️  备份失败或无数据可备份（不影响升级）", flush=True)

        # 2. 加载项目记忆，检查是否有未完成的工作
        result["has_pending_work"] = has_pending_work()
        if result["has_pending_work"]:
            result["last_feature"] = get_last_feature()
            result["last_args"] = get_last_args()
            result["last_result_files"] = get_last_result_files()
            print(f"\n  📋 检测到未完成的工作：", flush=True)
            print(f"     功能：{result['last_feature']}", flush=True)
            if result["last_args"]:
                print(f"     参数：{_summarize_args(result['last_args'])}", flush=True)
            if result["last_result_files"]:
                print(f"     输出文件：{len(result['last_result_files'])} 个", flush=True)
            print(f"\n  💡 升级已完成，您可以继续未完成的工作，或开始新的任务。", flush=True)
            print(f"  💡 如需恢复上次工作，可使用相同的参数重新执行对应功能。", flush=True)
            result["message"] = (
                f"版本升级 v{previous_version} → v{current_version} 完成。"
                f"检测到未完成的工作（功能：{result['last_feature']}），"
                f"可使用相同参数继续执行。"
            )
        else:
            print(f"\n  ✨ 无未完成的工作，可以开始新任务。", flush=True)
            result["message"] = f"版本升级 v{previous_version} → v{current_version} 完成。"

        print(f"{'='*60}\n", flush=True)
    else:
        # 版本回退（罕见情况），仅记录日志，不做破坏性操作
        print(f"  ⚠️  检测到版本回退：v{previous_version} → v{current_version}（未做数据清理）", flush=True)
        result["message"] = f"版本回退 v{previous_version} → v{current_version}，用户数据已保留。"

    # 3. 更新本地版本号
    _write_manifest_version(current_version)
    return result


def get_current_version() -> str:
    """获取当前客户端版本号"""
    return getattr(config, "VERSION", "unknown")


def get_manifest_version() -> str:
    """获取本地记录的版本号（上次运行时的版本）"""
    return _read_manifest_version()


# ==================== 内部函数 ====================

def _read_manifest_version() -> str:
    """读取本地版本清单中的版本号"""
    try:
        if VERSION_MANIFEST_FILE.exists():
            with open(VERSION_MANIFEST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("version", "")
    except (json.JSONDecodeError, OSError):
        pass
    return ""


def _write_manifest_version(version: str) -> None:
    """写入本地版本清单"""
    try:
        config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "version": version,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }
        tmp_path = VERSION_MANIFEST_FILE.with_suffix(".json.tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, VERSION_MANIFEST_FILE)
    except Exception as e:
        print(f"[version_migration] 写入版本清单失败: {e}", flush=True)


def _compare_versions(v1: str, v2: str) -> int:
    """比较两个版本号
    Returns:
        1  = v1 > v2
        0  = v1 == v2
        -1 = v1 < v2
    """
    def parse(v):
        if not v:
            return (0, 0, 0)
        core = v.split("-")[0].strip()
        parts = core.split(".")
        try:
            return (int(parts[0]) if len(parts) > 0 else 0,
                    int(parts[1]) if len(parts) > 1 else 0,
                    int(parts[2]) if len(parts) > 2 else 0)
        except (ValueError, IndexError):
            return (0, 0, 0)

    p1, p2 = parse(v1), parse(v2)
    if p1 > p2:
        return 1
    elif p1 < p2:
        return -1
    return 0


def _summarize_args(args: Dict[str, Any]) -> str:
    """将参数摘要为一行字符串用于显示"""
    if not args:
        return "（无参数）"
    parts = []
    for k, v in args.items():
        if v is None or v == "" or v is False:
            continue
        val_str = str(v)
        if len(val_str) > 40:
            val_str = val_str[:37] + "..."
        parts.append(f"{k}={val_str}")
    return ", ".join(parts[:5]) if parts else "（无参数）"
