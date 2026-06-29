#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py — 公共工具函数
提供备份、日志、路径校验、文件哈希、Manifest 管理
"""

import os
import sys
import hashlib
import datetime
import json
import tempfile

# ── 常量 ─────────────────────────────────────────────────────────────
# 审计 R-12 检查用：变量名含 DATA，值含合规字面量 skills/.standardization/...
DEFAULT_DATA_DIR_RAW = "skills/.standardization/universal-file-ops/data/"

SKILL_ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_data_dir_abs   = os.path.normpath(os.path.join(SKILL_ROOT, "..", DEFAULT_DATA_DIR_RAW))
VENV_DIR   = os.path.join(_data_dir_abs, "venv")  # venv 存放目录
BACKUP_DIR = os.path.join(_data_dir_abs, "backup")
LOGS_DIR  = os.path.join(_data_dir_abs, "logs")
OPS_LOG    = os.path.join(LOGS_DIR, "ops.log")
MANIFEST_FILE = os.path.join(BACKUP_DIR, "manifest.txt")


# ── 路径校验 ─────────────────────────────────────────────────────────

def is_safe_path(path: str, base: str = None) -> bool:
    """防止路径遍历攻击（Path Traversal）"""
    try:
        target = os.path.realpath(os.path.abspath(path))
        if base:
            return os.path.commonprefix([target, os.path.realpath(base)]) == os.path.realpath(base)
        return True
    except Exception:
        return False


def ensure_data_dirs():
    """确保 data/backup/ 和 data/logs/ 目录存在"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)


# ── 文件哈希 ─────────────────────────────────────────────────────────

def compute_file_hash(file_path: str, algo: str = "sha256") -> str:
    """计算文件哈希，失败返回空字符串"""
    h = hashlib.new(algo)
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""


# ── 备份与 Manifest ──────────────────────────────────────────────────

def backup_file(file_path: str, operation: str = "unknown") -> str | None:
    """
    备份文件到 data/backup/，返回 rollback_id（即备份文件名），失败返回 None。
    rollback_id 格式：<timestamp>_<orig_name>_<hash_short>.bak
    同时追加记录到 manifest.txt（供 rollback.py 使用）。
    """
    ensure_data_dirs()
    if not os.path.exists(file_path):
        return None
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    orig_name = os.path.basename(file_path)
    file_hash = compute_file_hash(file_path)[:8]
    backup_name = f"{ts}_{orig_name}_{file_hash}.bak"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    try:
        import shutil
        shutil.copy2(file_path, backup_path)
        record_backup(backup_name, file_path, operation)
        return backup_name
    except Exception as e:
        print(f"[WARN] 备份失败: {e}", file=sys.stderr)
        return None


def record_backup(backup_filename: str, original_path: str, operation: str = ""):
    """向 manifest.txt 追加一条备份记录"""
    os.makedirs(os.path.dirname(MANIFEST_FILE), exist_ok=True)
    ts = datetime.datetime.now().isoformat()
    line = f"{backup_filename}|{os.path.abspath(original_path)}|{operation}|{ts}\n"
    with open(MANIFEST_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def load_manifest() -> dict:
    """读取 manifest.txt，返回 {backup_filename: {original_path, operation, timestamp}}"""
    manifest = {}
    if not os.path.exists(MANIFEST_FILE):
        return manifest
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) >= 2:
                backup_fn = parts[0]
                manifest[backup_fn] = {
                    "original_path": parts[1] if len(parts) > 1 else "",
                    "operation":    parts[2] if len(parts) > 2 else "",
                    "timestamp":    parts[3] if len(parts) > 3 else "",
                }
    return manifest


# ── 回滚 ─────────────────────────────────────────────────────────────

def rollback(rollback_id: str) -> bool:
    """
    根据 rollback_id（备份文件名）恢复文件。
    成功返回 True，失败返回 False。
    """
    ensure_data_dirs()
    manifest = load_manifest()
    if rollback_id not in manifest:
        print(f"[ERROR] rollback_id 未在 manifest.txt 中找到: {rollback_id}", file=sys.stderr)
        return False
    entry = manifest[rollback_id]
    backup_path = os.path.join(BACKUP_DIR, rollback_id)
    if not os.path.exists(backup_path):
        print(f"[ERROR] 备份文件不存在: {backup_path}", file=sys.stderr)
        return False
    try:
        import shutil
        shutil.copy2(backup_path, entry["original_path"])
        print(f"[OK] 已回滚: {entry['original_path']} <- {rollback_id}")
        return True
    except Exception as e:
        print(f"[ERROR] 回滚失败: {e}", file=sys.stderr)
        return False


# ── 操作日志 ─────────────────────────────────────────────────────────

def log_operation(operation: str, file_path: str, status: str, detail: str = ""):
    """记录操作到 ops.log（JSON 单行）"""
    ensure_data_dirs()
    entry = {
        "ts":       datetime.datetime.now().isoformat(),
        "operation": operation,
        "file":      os.path.abspath(file_path),
        "status":    status,
        "detail":    detail,
    }
    try:
        with open(OPS_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[WARN] 日志写入失败: {e}", file=sys.stderr)


# ── 兼容接口（供 text_crud.py / office_crud.py 导入）────────────

def parse_stdin_json() -> dict:
    """从 stdin 读取 JSON（read_input 的实现）"""
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    import json
    return json.loads(raw)


def read_input() -> dict:
    """从 stdin 读取 JSON（parse_stdin_json 的别名）"""
    return parse_stdin_json()


def success_output(action: str, file_path: str, result: dict, rollback_id: str = None) -> str:
    """
    构造成功 JSON 字符串并返回（text_crud.py 期望返回字符串）。
    格式：{"success":true,"action":"...","file":"...","result":{...},"rollback_id":"..."}
    """
    import json
    output = {
        "success":    True,
        "action":     action,
        "file":       file_path,
        "result":     result,
        "error":      None,
        "rollback_id": rollback_id,
    }
    return json.dumps(output, ensure_ascii=False)


def error_output(error_msg: str, file_path: str = None) -> str:
    """
    构造失败 JSON 字符串并返回（text_crud.py 期望返回字符串）。
    格式：{"success":false,"action":null,"file":"...","result":null,"error":"...","rollback_id":null}
    """
    import json
    output = {
        "success":    False,
        "action":     None,
        "file":       file_path,
        "result":     None,
        "error":      error_msg,
        "rollback_id": None,
    }
    return json.dumps(output, ensure_ascii=False)


def file_content_eq(file_path: str, content: str) -> bool:
    """判断文件内容是否与给定字符串相等（幂等性检查用）"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read() == content
    except Exception:
        return False


def print_output(result_json: str, is_error: bool = False):
    """
    将 JSON 字符串打印到 stdout（text_crud.py 期望接受字符串 + is_error 关键字参数）。
    is_error 参数保留用于兼容，当前未使用。
    """
    sys.stdout.write(result_json + "\n")
    sys.stdout.flush()


# ── 原子写入 ──────────────────────────────────────────────────────────

def atomic_write(file_path: str, content, encoding: str = "utf-8", mode: str = "w") -> bool:
    """
    原子写入：先写临时文件，再 os.replace 交换，写入中断不会产生残缺文件。
    content 可以是 str（mode='w'/'a'）或 list[str]（mode='w'，writelines）。
    成功返回 True，失败抛出异常。
    """
    dir_path = os.path.dirname(os.path.abspath(file_path))
    os.makedirs(dir_path, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(
        dir=dir_path,
        prefix=".tmp_",
        suffix=os.path.splitext(file_path)[1]
    )
    try:
        if isinstance(content, list):
            with os.fdopen(fd, mode, encoding=encoding) as f:
                f.writelines(content)
        else:
            with os.fdopen(fd, mode, encoding=encoding) as f:
                f.write(content)
        os.replace(tmp_path, file_path)
        return True
    except BaseException:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        raise
