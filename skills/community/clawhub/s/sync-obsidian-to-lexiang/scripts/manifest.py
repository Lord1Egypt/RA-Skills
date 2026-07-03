"""
manifest.py - sync_manifest.json 读写管理

管理 Obsidian vault 与乐享知识库之间的映射关系。
存储位置: {vault}/.obsidian/plugins/sync-obsidian-to-lexiang/manifest.json
"""

import json
import os
import hashlib
import time
import errno
from datetime import datetime, timezone
from typing import Optional


PLUGIN_DIR = "sync-obsidian-to-lexiang"
MANIFEST_FILE = "manifest.json"
CONFIG_FILE = "config.json"
LOCK_FILE = ".sync.lock"

# 锁超时（秒）：持锁进程若超过此时长仍未释放，视为陈旧锁可被接管。
# 取一个较大的值，覆盖大批量全量同步（几百篇）的最坏耗时。
LOCK_STALE_SECONDS = 3600

DEFAULT_CONFIG = {
    "target_space_id": "",
    "target_folder_entry_id": "",
    "conflict_strategy": "lexiang_wins",
    "exclude_patterns": [".obsidian/**", "*.canvas"],
    "sync_attachments": True,
    "attachment_folder": "",
    # 目的端移动处理：true=尊重用户移动（仍更新原 entry，不在目标目录重建）；
    # false=强制归位（被移走则在目标目录重新创建一份，旧副本保留）
    "respect_move": True,
}

MANIFEST_VERSION = 1


def get_plugin_dir(vault_path: str) -> str:
    """获取插件目录路径"""
    return os.path.join(vault_path, ".obsidian", "plugins", PLUGIN_DIR)


def ensure_plugin_dir(vault_path: str) -> str:
    """确保插件目录存在"""
    plugin_dir = get_plugin_dir(vault_path)
    os.makedirs(plugin_dir, exist_ok=True)
    return plugin_dir


def load_config(vault_path: str) -> dict:
    """加载同步配置"""
    config_path = os.path.join(get_plugin_dir(vault_path), CONFIG_FILE)
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()


def save_config(vault_path: str, config: dict) -> str:
    """保存同步配置"""
    plugin_dir = ensure_plugin_dir(vault_path)
    config_path = os.path.join(plugin_dir, CONFIG_FILE)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    return config_path


def load_manifest(vault_path: str) -> dict:
    """加载映射文件"""
    manifest_path = os.path.join(get_plugin_dir(vault_path), MANIFEST_FILE)
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return new_manifest()


def new_manifest() -> dict:
    """创建空的 manifest"""
    return {
        "version": MANIFEST_VERSION,
        "space_id": "",
        "root_entry_id": "",
        "target_folder_entry_id": "",
        "last_full_sync_at": "",
        "last_incremental_sync_at": "",
        "entries": {},
    }


def save_manifest(vault_path: str, manifest: dict) -> str:
    """保存映射文件"""
    plugin_dir = ensure_plugin_dir(vault_path)
    manifest_path = os.path.join(plugin_dir, MANIFEST_FILE)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return manifest_path


def compute_content_hash(file_path: str) -> str:
    """计算文件内容的 SHA256 哈希"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return f"sha256:{sha256.hexdigest()}"


def get_file_mtime(file_path: str) -> float:
    """获取文件修改时间戳"""
    return os.path.getmtime(file_path)


def now_iso() -> str:
    """获取当前时间 ISO 8601 格式"""
    return datetime.now(timezone.utc).astimezone().isoformat()


def get_entry(manifest: dict, rel_path: str) -> Optional[dict]:
    """查询 manifest 中的条目"""
    return manifest.get("entries", {}).get(rel_path)


def set_entry(
    manifest: dict,
    rel_path: str,
    entry_type: str,
    entry_id: str,
    content_hash: str = "",
    source_mtime: float = 0,
) -> None:
    """设置或更新 manifest 中的条目"""
    entry = {
        "type": entry_type,
        "entry_id": entry_id,
        "last_sync_at": now_iso(),
    }
    # page 和 file 都记录内容哈希与 mtime，用于增量变更检测
    if entry_type in ("page", "file"):
        entry["content_hash"] = content_hash
        entry["source_mtime"] = source_mtime
    manifest.setdefault("entries", {})[rel_path] = entry


def remove_entry(manifest: dict, rel_path: str) -> Optional[dict]:
    """从 manifest 中移除条目"""
    return manifest.get("entries", {}).pop(rel_path, None)


def list_entries(manifest: dict, entry_type: Optional[str] = None) -> dict:
    """列出 manifest 中的条目，可按类型过滤"""
    entries = manifest.get("entries", {})
    if entry_type:
        return {k: v for k, v in entries.items() if v.get("type") == entry_type}
    return entries


# ── 文件锁：防止跨会话/多进程并发同步同一 vault ──────────────────

class SyncLockError(Exception):
    """获取同步锁失败（已有其他进程在同步）"""
    pass


def _pid_alive(pid: int) -> bool:
    """判断进程是否存活（仅本机有效）"""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError as e:
        # ESRCH=进程不存在；EPERM=存在但无权限（视为存活）
        return e.errno == errno.EPERM
    return True


def _read_lock_info(lock_path: str) -> Optional[dict]:
    """读取锁文件内容，损坏/不存在返回 None"""
    try:
        with open(lock_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def acquire_lock(vault_path: str) -> str:
    """
    获取同步锁。成功返回锁文件路径；失败抛 SyncLockError。

    采用 O_CREAT|O_EXCL 原子创建，保证同一时刻只有一个进程持锁。
    若已存在锁：检查是否为陈旧锁（持锁进程已死，或超过 LOCK_STALE_SECONDS），
    是则接管，否则拒绝。
    """
    plugin_dir = ensure_plugin_dir(vault_path)
    lock_path = os.path.join(plugin_dir, LOCK_FILE)

    payload = json.dumps({
        "pid": os.getpid(),
        "host": _hostname(),
        "acquired_at": now_iso(),
        "acquired_ts": time.time(),
    }, ensure_ascii=False)

    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
        return lock_path
    except FileExistsError:
        pass  # 锁已存在，进入陈旧判定

    info = _read_lock_info(lock_path)
    stale = False
    if info is None:
        stale = True  # 锁文件损坏 → 视为陈旧
    else:
        age = time.time() - float(info.get("acquired_ts", 0) or 0)
        same_host = info.get("host") == _hostname()
        pid = int(info.get("pid", 0) or 0)
        # 同机且进程已死 → 陈旧；或超过超时阈值 → 陈旧
        if same_host and not _pid_alive(pid):
            stale = True
        elif age > LOCK_STALE_SECONDS:
            stale = True

    if not stale:
        holder = info or {}
        raise SyncLockError(
            f"已有同步任务在运行（pid={holder.get('pid')}, "
            f"host={holder.get('host')}, 开始于 {holder.get('acquired_at')}）。"
            f"请等待其完成，或确认无误后删除锁文件：{lock_path}"
        )

    # 接管陈旧锁：覆盖写入
    with open(lock_path, "w", encoding="utf-8") as f:
        f.write(payload)
    return lock_path


def release_lock(lock_path: str) -> None:
    """释放锁（仅当锁属于当前进程时才删除，避免误删接管者的锁）"""
    if not lock_path or not os.path.exists(lock_path):
        return
    info = _read_lock_info(lock_path)
    if info and int(info.get("pid", 0) or 0) == os.getpid():
        try:
            os.remove(lock_path)
        except OSError:
            pass


class sync_lock:
    """同步锁上下文管理器，保证 with 块结束（含异常）时释放。

    用法：
        with sync_lock(vault_path):
            ...  # 执行同步
    获取失败抛 SyncLockError。
    """

    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.lock_path = None

    def __enter__(self):
        self.lock_path = acquire_lock(self.vault_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        release_lock(self.lock_path)
        return False


def _hostname() -> str:
    try:
        import socket
        return socket.gethostname()
    except Exception:
        return "unknown"
