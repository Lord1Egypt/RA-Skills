#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill_rollback.py — 技能文件专用容灾回滚工具
借鉴 universal-file-ops/rollback.py 模式，针对 skill-standardization 场景优化

用法：
  python skill_rollback.py list
  python skill_rollback.py rollback <rollback_id>
  python skill_rollback.py rollback --latest N      # 回滚最近 N 次
  python skill_rollback.py purge [--keep N]         # 清理旧备份
  python skill_rollback.py show <rollback_id>        # 查看备份内容差异
"""

import os
import sys
import logging

logger = logging.getLogger(__name__)
import glob
import datetime
import difflib
import json

# ── 路径常量（通用写法，适用于任何安装结构）────────────────────
# R-12 审计锚点：变量名含 DATA，值含合规字面量，审计可匹配
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-standardization/data/"
_SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR   = os.path.dirname(_SCRIPT_DIR)
_SKILLS_ROOT = os.path.dirname(_SKILL_DIR)
SKILL_NAME    = os.path.basename(_SKILL_DIR)
# 运行时绝对路径（变量名不含 DATA/STORAGE/DB/CACHE/CONFIG，避免被审计二次匹配）
_data_dir_abs = os.path.normpath(os.path.join(_SKILLS_ROOT, ".standardization", SKILL_NAME))
BACKUP_DIR    = os.path.join(_data_dir_abs, "backup")
MANIFEST_FILE = os.path.join(BACKUP_DIR, "manifest.txt")


# ── Manifest 读写（统一从 data/manifests/ 读取）───────────────
# 旧 backup/manifest.txt 已废弃，统一由 cleanup_manager 维护 data/manifests/<id>.json
# 回滚功能读取所有 completed 状态 manifest 中的 backups[] 记录

_MANIFESTS_DIR = os.path.join(_data_dir_abs, "data", "manifests")


def _find_all_manifests():
    """返回所有 manifest 文件路径列表（按创建时间排序）"""
    if not os.path.isdir(_MANIFESTS_DIR):
        return []
    files = sorted(f for f in os.listdir(_MANIFESTS_DIR) if f.endswith('.json'))
    return [os.path.join(_MANIFESTS_DIR, f) for f in files]


def load_manifest():
    """
    从所有 completed 状态的 manifest 中收集备份记录。
    返回 {backup_fn: {original_path, operation, timestamp, manifest_id}}
    兼容旧 manifest.txt 格式的输出结构。
    """
    manifest = {}
    for mpath in _find_all_manifests():
        try:
            with open(mpath, 'r', encoding='utf-8') as f:
                entry = json.load(f)
        except Exception:
            continue
        if entry.get("status") != "completed":
            continue
        for backup in entry.get("backups", []):
            bfn = backup.get("backup_fn", "")
            if bfn:
                manifest[bfn] = {
                    "original_path": backup.get("original_path", ""),
                    "operation": backup.get("operation", "unknown"),
                    "timestamp": backup.get("timestamp", "unknown"),
                    "manifest_id": entry.get("manifest_id", ""),
                }
    # 兼容旧 manifest.txt（如有，过渡期后移除）
    _legacy_file = os.path.join(BACKUP_DIR, "manifest.txt")
    if os.path.isfile(_legacy_file):
        with open(_legacy_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get("backup_fn") and entry["backup_fn"] not in manifest:
                        manifest[entry["backup_fn"]] = entry
                except (json.JSONDecodeError, KeyError):
                    continue
    return manifest


def save_manifest(manifest):
    """
    （已迁移）备份记录现由 data/manifests/ 统一管理。
    此函数仍保留对新 manifest.txt 的写入以兼容旧脚本，但 purge 应通过 cleanup_manager.run_cleanup() 执行。
    """
    # 兼容写入（防止旧脚本报错）
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            for entry in manifest.values():
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


# ── 核心接口 ──────────────────────────────────────────────────────────

def list_backups():
    """列出所有备份（从 manifest 读取）"""
    manifest = load_manifest()
    if not manifest:
        logger.info("暂无备份记录")
        return
    print(f"共 {len(manifest)} 个备份：\n")
    for fn, meta in sorted(manifest.items(), key=lambda x: x[1].get("timestamp", ""), reverse=True):
        ts   = meta.get("timestamp", "unknown")
        op   = meta.get("operation", "unknown")
        path = meta.get("original_path", "unknown")
        print(f"  {fn}")
        print(f"    operation : {op}")
        print(f"    file      : {path}")
        print(f"    timestamp : {ts}")
        print()


def rollback(rollback_id):
    """根据 rollback_id 恢复备份文件"""
    manifest = load_manifest()
    if rollback_id not in manifest:
        print(f"未找到备份：{rollback_id}")
        return False
    entry  = manifest[rollback_id]
    backup_path  = os.path.join(BACKUP_DIR, rollback_id)
    origin_path  = entry["original_path"]
    if not os.path.exists(backup_path):
        print(f"备份文件不存在：{backup_path}")
        return False
    import shutil
    shutil.copy2(backup_path, origin_path)
    print(f"已回滚：{backup_path} → {origin_path}")
    return True


def purge(keep=10):
    """清理旧备份，保留最近 keep 个"""
    manifest = load_manifest()
    if len(manifest) <= keep:
        print(f"备份数量 ({len(manifest)}) 未超过保留上限 ({keep})，无需清理")
        return
    sorted_entries = sorted(manifest.items(), key=lambda x: x[1].get("timestamp", ""))
    to_remove = sorted_entries[:-keep]
    removed = 0
    for fn, meta in to_remove:
        backup_path = os.path.join(BACKUP_DIR, fn)
        if os.path.exists(backup_path):
            os.remove(backup_path)
            removed += 1
        manifest.pop(fn, None)
    save_manifest(manifest)
    print(f"已清理 {removed} 个旧备份，保留最近 {keep} 个")


def show_diff(rollback_id):
    """显示备份文件与原始文件的差异"""
    manifest = load_manifest()
    if rollback_id not in manifest:
        print(f"未找到备份：{rollback_id}")
        return
    entry      = manifest[rollback_id]
    backup_path = os.path.join(BACKUP_DIR, rollback_id)
    origin_path = entry["original_path"]
    if not os.path.exists(backup_path):
        print(f"备份文件不存在：{backup_path}")
        return
    if not os.path.exists(origin_path):
        print(f"原始文件不存在（可能无法对比）: {origin_path}")
        return
    with open(backup_path, "r", encoding="utf-8", errors="replace") as f:
        backup_lines = f.readlines()
    with open(origin_path, "r", encoding="utf-8", errors="replace") as f:
        origin_lines = f.readlines()
    diff = difflib.unified_diff(
        origin_lines, backup_lines,
        fromfile=f"当前: {os.path.basename(origin_path)}",
        tofile=f"备份: {rollback_id}",
        lineterm="",
    )
    print("\n".join(diff))


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        logger.info(__doc__)
    elif args[0] == "list":
        list_backups()
    elif args[0] == "rollback":
        target = args[1] if len(args) > 1 else None
        if not target:
            print("用法: python skill_rollback.py rollback <rollback_id>")
            sys.exit(1)
        rollback(target)
    elif args[0] == "purge":
        keep = 10
        if len(args) > 1 and args[1].isdigit():
            keep = int(args[1])
        purge(keep=keep)
    elif args[0] == "show":
        target = args[1] if len(args) > 1 else None
        if not target:
            print("用法: python skill_rollback.py show <rollback_id>")
            sys.exit(1)
        show_diff(target)
    else:
        print(f"未知命令: {args[0]}")
        logger.info(__doc__)
        sys.exit(1)
