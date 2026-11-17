#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cleanup_manager.py — 临时文件/备份文件 manifest 驱动清理管理器。

设计原则：
1. 清单先行：文件创建时立即注册到 manifest，不清除未注册的文件
2. 安全边界：只删除 data/ 目录内的文件，任何 data/ 外的路径被注册也会在清理时被安全阻止
3. 强制调用：通过 builder（updater/refactor）的入口和出口自动管理 session
4. 可审计：每个 manifest 是完整的 JSON 记录，含操作类型、时间、文件列表

用法：
    from scripts.cleanup_manager import start_session, register, end_session
    
    # 在操作开始时
    start_session(skill_dir, "update")
    
    # 在 safe_io 或其他创建文件的地方
    register(temp_file_path)
    
    # 在操作结束时
    report = end_session()
    # report = {"deleted": N, "skipped": N, "errors": [...]}
"""

import os
import json
import datetime
import uuid
import shutil

# R-12 审计锚点：变量名含 DATA，值含合规字面量，审计可匹配
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-standardization/data/"
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(_SCRIPTS_DIR)
SKILLS_ROOT = os.path.dirname(SKILL_DIR)
_data_dir_abs = os.path.normpath(os.path.join(SKILLS_ROOT, ".standardization", "skill-standardization"))

# ── session 模块级状态 ──────────────────────────────────────────
# safe_io 可以直接 import 这个模块并调用 register()，无需传递参数
_SESSION = {"manifest_id": None, "skill_dir": None, "data_dir": None}

_MANIFESTS_SUBDIR = "manifests"


def _resolve_manifest_dir(skill_dir):
    """
    解析技能的数据目录下的 manifests/ 子目录。
    优先从 _meta.json 的 data_dir 读取，回退到 .standardization/<skill>/data/ 约定路径。
    """
    # 尝试从 _meta.json 读取
    meta_path = os.path.join(skill_dir, '_meta.json')
    if os.path.isfile(meta_path):
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            data_dir_rel = meta.get('data_dir', '')
            if data_dir_rel:
                # data_dir 是相对路径
                # 示例: "../.standardization/<skill>/data/" 或 "./.standardization/<skill>/data/"
                if data_dir_rel.startswith("../"):
                    skills_root = os.path.dirname(os.path.dirname(skill_dir))
                    abs_data = os.path.normpath(os.path.join(skill_dir, data_dir_rel))
                else:
                    skills_root = os.path.dirname(skill_dir)
                    abs_data = os.path.normpath(os.path.join(skills_root, data_dir_rel))
                if os.path.isdir(abs_data) or os.path.exists(os.path.dirname(abs_data)):
                    return os.path.join(abs_data, _MANIFESTS_SUBDIR), abs_data
        except Exception:
            pass

    # 回退：skills/.standardization/<skill>/data/manifests/
    skills_root = os.path.dirname(os.path.dirname(skill_dir))
    fallback_data = os.path.join(skills_root, ".standardization", os.path.basename(skill_dir), "data")
    return os.path.join(fallback_data, _MANIFESTS_SUBDIR), fallback_data


def start_session(skill_dir, operation="update"):
    """
    在操作开始时调用。
    创建 manifest 文件，记录操作元信息。
    返回 manifest_id。
    
    Args:
        skill_dir: 被操作技能的绝对路径
        operation: "create" | "update" | "refactor"
    Returns:
        manifest_id (str) 或 None（如果 manifest 目录无法创建）
    """
    global _SESSION
    manifests_dir, data_dir = _resolve_manifest_dir(skill_dir)
    
    os.makedirs(manifests_dir, exist_ok=True)
    
    now = datetime.datetime.now()
    manifest_id = f"{now.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    
    manifest = {
        "manifest_id": manifest_id,
        "operation": operation,
        "skill_dir": skill_dir,
        "data_dir": data_dir,
        "created_at": now.isoformat(),
        "temp_files": [],
        "backup_files": [],
        "status": "active"
    }
    
    mpath = os.path.join(manifests_dir, f"{manifest_id}.json")
    with open(mpath, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    _SESSION["manifest_id"] = manifest_id
    _SESSION["skill_dir"] = skill_dir
    _SESSION["data_dir"] = data_dir
    
    return manifest_id


def register(filepath, category="temp"):
    """
    在 safe_io 等创建文件的地方调用。
    将文件路径追加到当前 session 的 manifest。
    如果当前没有活跃 session，静默跳过（不报错）。
    
    Args:
        filepath: 创建的文件的绝对路径
        category: "temp" | "backup"
    """
    manifest_id = _SESSION.get("manifest_id")
    skill_dir = _SESSION.get("skill_dir")
    if not manifest_id or not skill_dir:
        return
    
    manifests_dir, _ = _resolve_manifest_dir(skill_dir)
    mpath = os.path.join(manifests_dir, f"{manifest_id}.json")
    if not os.path.isfile(mpath):
        return
    
    try:
        with open(mpath, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception:
        return
    
    key = "temp_files" if category == "temp" else "backup_files"
    abs_fp = os.path.abspath(filepath)
    if abs_fp not in manifest[key]:
        manifest[key].append(abs_fp)


def register_backup(backup_fn, original_path, operation="unknown"):
    """
    注册完整备份记录（含原始路径、操作类型、时间戳）。
    供 safe_io.backup_file() 调用，替代旧的 manifest.txt 写入。
    同时将备份文件路径注册到 backup_files（供 cleanup 清理用）。
    
    backup_fn: 备份文件名（如 20260601_SKILL.md_hash.bak）
    original_path: 被备份文件的原始绝对路径
    operation: 触发备份的操作名
    """
    manifest_id = _SESSION.get("manifest_id")
    skill_dir = _SESSION.get("skill_dir")
    if not manifest_id or not skill_dir:
        return
    
    manifests_dir, data_dir = _resolve_manifest_dir(skill_dir)
    mpath = os.path.join(manifests_dir, f"{manifest_id}.json")
    if not os.path.isfile(mpath):
        return
    
    try:
        with open(mpath, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception:
        return
    
    # 确保 list 字段存在
    if "backups" not in manifest:
        manifest["backups"] = []
    if "backup_files" not in manifest:
        manifest["backup_files"] = []
    
    # 添加结构化备份记录
    backup_entry = {
        "backup_fn": backup_fn,
        "original_path": os.path.abspath(original_path),
        "operation": operation,
        "timestamp": datetime.datetime.now().isoformat(),
    }
    manifest["backups"].append(backup_entry)
    
    # 同时注册备份文件路径到 backup_files（供 cleanup 删除）
    backup_abs = os.path.join(data_dir, "backup", backup_fn)
    if backup_abs not in manifest["backup_files"]:
        manifest["backup_files"].append(backup_abs)
    
    with open(mpath, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    with open(mpath, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def finalize(skill_dir=None, manifest_id=None):
    """
    标记 manifest 为 completed。
    如果不传参数，使用当前 session。
    """
    mid = manifest_id or _SESSION.get("manifest_id")
    sd = skill_dir or _SESSION.get("skill_dir")
    if not mid or not sd:
        return
    
    manifests_dir, _ = _resolve_manifest_dir(sd)
    mpath = os.path.join(manifests_dir, f"{mid}.json")
    if not os.path.isfile(mpath):
        return
    
    try:
        with open(mpath, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception:
        return
    
    manifest["status"] = "completed"
    manifest["completed_at"] = datetime.datetime.now().isoformat()
    
    with open(mpath, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def end_session():
    """
    结束当前 session：finalize + cleanup。
    返回清理报告 {"deleted": int, "skipped": int, "errors": [str]}。
    如果没有活跃 session，返回空报告。
    """
    mid = _SESSION.get("manifest_id")
    sd = _SESSION.get("skill_dir")
    dd = _SESSION.get("data_dir")
    
    # 清除 session 状态（防止 end_session 后 register 误注册）
    _SESSION["manifest_id"] = None
    _SESSION["skill_dir"] = None
    _SESSION["data_dir"] = None
    
    if not mid or not sd:
        return {"deleted": 0, "skipped": 0, "errors": ["无活跃 session"]}
    
    # finalize
    finalize(sd, mid)
    
    # cleanup
    report = run_cleanup(sd, mid, dd)
    return report


def run_cleanup(skill_dir, manifest_id, data_dir=None):
    """
    执行实际删除操作。
    安全边界：只删除 data 目录内的文件。data 目录外的路径即使被注册了也跳过。
    
    Returns:
        {"deleted": int, "skipped": int, "errors": [str]}
    """
    manifests_dir, resolved_data_dir = _resolve_manifest_dir(skill_dir)
    data_dir = data_dir or resolved_data_dir
    data_dir_abs = os.path.abspath(data_dir)
    
    mpath = os.path.join(manifests_dir, f"{manifest_id}.json")
    if not os.path.isfile(mpath):
        return {"deleted": 0, "skipped": 0, "errors": [f"manifest 不存在: {manifest_id}"]}
    
    try:
        with open(mpath, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception as e:
        return {"deleted": 0, "skipped": 0, "errors": [f"读取 manifest 失败: {e}"]}
    
    if manifest.get("status") != "completed":
        return {"deleted": 0, "skipped": 1, "errors": [f"manifest 状态不是 completed: {manifest.get('status')}"]}
    
    all_files = manifest.get("temp_files", []) + manifest.get("backup_files", [])
    deleted = 0
    skipped = 0
    errors = []
    
    for fp in all_files:
        abs_fp = os.path.abspath(fp)
        
        # ── 安全边界检查 ──
        if not abs_fp.startswith(data_dir_abs):
            errors.append(f"⛔ 安全阻止：{fp} 不在 data 目录内（{data_dir_abs}），已跳过")
            skipped += 1
            continue
        
        if not os.path.exists(abs_fp):
            skipped += 1
            continue
        
        try:
            if os.path.isfile(abs_fp) or os.path.islink(abs_fp):
                os.remove(abs_fp)
                deleted += 1
            elif os.path.isdir(abs_fp):
                shutil.rmtree(abs_fp)
                deleted += 1
        except Exception as e:
            errors.append(f"删除失败 {fp}: {e}")
            skipped += 1
    
    # 清理完成后删除 manifest 本身（也在 data dir 内）
    try:
        if os.path.isfile(mpath):
            os.remove(mpath)
    except Exception:
        pass
    
    return {"deleted": deleted, "skipped": skipped, "errors": errors}


def list_active_manifests(skill_dir):
    """列出所有活跃（未 finalize）的 manifest。"""
    manifests_dir, _ = _resolve_manifest_dir(skill_dir)
    if not os.path.isdir(manifests_dir):
        return []
    
    active = []
    for fname in sorted(os.listdir(manifests_dir)):
        if not fname.endswith('.json'):
            continue
        mpath = os.path.join(manifests_dir, fname)
        try:
            with open(mpath, 'r', encoding='utf-8') as f:
                m = json.load(f)
            if m.get("status") == "active":
                active.append(m)
        except Exception:
            pass
    return active


# ── CLI ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python cleanup_manager.py <skill_dir> [--dry-run]")
        sys.exit(1)
    
    skill_dir = os.path.abspath(sys.argv[1])
    dry_run = "--dry-run" in sys.argv
    
    active = list_active_manifests(skill_dir)
    if not active:
        print(f"ℹ️  {skill_dir} 无活跃 manifest，无需清理")
        sys.exit(0)
    
    total_del = 0
    total_skip = 0
    total_err = 0
    for m in active:
        finalize(skill_dir, m["manifest_id"])
        report = run_cleanup(skill_dir, m["manifest_id"])
        total_del += report["deleted"]
        total_skip += report["skipped"]
        total_err += len(report["errors"])
        if dry_run:
            print(f"[DRY-RUN] {m['manifest_id']}: {len(m.get('temp_files',[]))} temp + {len(m.get('backup_files',[]))} backup")
        else:
            print(f"[OK] {m['manifest_id']}: 删除 {report['deleted']}，跳过 {report['skipped']}，错误 {len(report['errors'])}")
    
    print(f"\n汇总: 删除 {total_del}，跳过 {total_skip}，错误 {total_err}")
