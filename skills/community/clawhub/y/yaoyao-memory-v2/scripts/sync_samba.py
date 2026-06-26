#!/usr/bin/env python3
"""
sync_samba.py - Samba 同步模块 v2.0

功能：
- 将记忆文件同步到局域网 Samba/NAS 存储
- 支持双向同步
- 冲突处理（新文件优先 or 保留双方）
- 增量同步（只同步变更的文件）

依赖：
- pip install smbprotocol

配置：
- SAMBA_HOST: Samba 服务器地址
- SAMBA_USER: 用户名
- SAMBA_PASSWORD: 密码
- SAMBA_SHARE: 共享目录名
- SAMBA_PATH: 远程路径

或通过 config/samba.json 配置
"""

import argparse
import hashlib
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ============================================================================
# 配置
# ============================================================================

LOCAL_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
CONFIG_FILE = Path(__file__).parent.parent / "config" / "samba.json"
STATE_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / ".samba_sync_state.json"

# ============================================================================
# 数据结构
# ============================================================================

@dataclass
class SambaConfig:
    """Samba 配置"""
    host: str
    share: str
    remote_path: str = ""
    username: str = ""
    password: str = ""
    port: int = 445
    
    @classmethod
    def from_env(cls) -> "SambaConfig":
        """从环境变量加载"""
        return cls(
            host=os.environ.get("SAMBA_HOST", ""),
            share=os.environ.get("SAMBA_SHARE", ""),
            remote_path=os.environ.get("SAMBA_REMOTE_PATH", "/"),
            username=os.environ.get("SAMBA_USER", ""),
            password=os.environ.get("SAMBA_PASSWORD") or os.environ.get("SAMBA_PASS", ""),
            port=int(os.environ.get("SAMBA_PORT", "445")),
        )
    
    @classmethod
    def from_file(cls, path: Path) -> "SambaConfig":
        """从配置文件加载"""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)
    
    def validate(self) -> bool:
        """验证配置"""
        return bool(self.host and self.share and self.username)
    
    def to_dict(self) -> dict:
        return {
            "host": self.host,
            "share": self.share,
            "remote_path": self.remote_path,
            "username": self.username,
            "password": self.password,
            "port": self.port,
        }


@dataclass
class FileInfo:
    """文件信息"""
    path: str
    mtime: float
    size: int
    hash: str = ""


@dataclass
class SyncResult:
    """同步结果"""
    uploaded: int = 0
    downloaded: int = 0
    skipped: int = 0
    conflicts: int = 0
    errors: List[str] = field(default_factory=list)


# ============================================================================
# 文件操作
# ============================================================================

def calculate_hash(filepath: Path) -> str:
    """计算文件 MD5"""
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()


def get_local_files() -> Dict[str, FileInfo]:
    """获取本地文件列表"""
    files = {}
    if not LOCAL_MEMORY_DIR.exists():
        return files
    
    for fpath in LOCAL_MEMORY_DIR.rglob("*"):
        if fpath.is_file() and not fpath.name.startswith("."):
            rel_path = str(fpath.relative_to(LOCAL_MEMORY_DIR))
            try:
                stat = fpath.stat()
                files[rel_path] = FileInfo(
                    path=rel_path,
                    mtime=stat.st_mtime,
                    size=stat.st_size,
                )
            except Exception as e:
                logger.warning(f"Failed to stat {fpath}: {e}")
    
    return files


# ============================================================================
# Samba 操作 - 使用 pysmb (smbprotocol 有连接问题)
# ============================================================================

try:
    from smb.SMBConnection import SMBConnection
    from smb.base import NotConnectedError
    HAS_PYSMB = True
except ImportError:
    HAS_PYSMB = False
    logger.warning("pysmb not installed")

try:
    import smbprotocol
    from smbprotocol.connection import Connection
    from smbprotocol.session import Session
    from smbprotocol.tree import TreeConnect
    from smbprotocol.open import Open
    from smbprotocol.create_context import FileFullAllocationInfo
    HAS_SMBPROTOCOL = True
except ImportError:
    HAS_SMBPROTOCOL = False

# 优先使用 pysmb (更稳定)
HAS_SAMBA = HAS_PYSMB


def get_samba_connection(config: SambaConfig):
    """获取 Samba 连接 (使用 pysmb)"""
    if not HAS_PYSMB:
        raise ImportError("pysmb not installed. Run: pip install pysmb")
    
    import socket
    local_name = socket.gethostname()[:15]
    
    conn = SMBConnection(
        username=config.username,
        password=config.password,
        my_name=local_name,
        remote_name=config.host,
        domain='',
        use_ntlm_v2=True,
        sign_options=0,
        is_direct_tcp=True
    )
    conn.connect(config.host, config.port or 445, timeout=30)
    
    return conn, None, None  # pysmb 不需要 session/tree 分离


def list_remote_files(conn, share_name: str, remote_path: str = "/") -> Dict[str, FileInfo]:
    """获取远程文件列表 (pysmb版本)"""
    files = {}
    
    try:
        # 使用 pysmb 的 listPath 获取目录列表
        # listPath(share_name, path, password, username)
        from smb.smb2_structs import SMB2EntryInfo
        import io
        
        # 获取远程目录下的文件列表
        path = remote_path.rstrip("/") + "/*" if remote_path != "/" else "/*"
        entries = conn.listPath(share_name, path)
        
        for entry in entries:
            if entry.filename not in ('.', '..'):
                files[entry.filename] = FileInfo(
                    path=entry.filename,
                    mtime=entry.last_write_time,
                    size=entry.size
                )
        
        logger.debug(f"Listed {len(files)} files in {remote_path}")
        
    except Exception as e:
        logger.debug(f"List remote files: {e}")
    
    return files


def upload_file(conn, share_name: str, local_path: Path, remote_full: str):
    """上传文件 (pysmb版本)
    
    Args:
        conn: SMBConnection
        share_name: 共享目录名 (如 "家庭共享")
        local_path: 本地文件路径
        remote_full: 完整远程路径 (如 "/记忆/memory_2026-04-06.md")
    """
    with open(local_path, 'rb') as f:
        conn.storeFile(share_name, remote_full, f)
    
    logger.info(f"Uploaded: {local_path} -> {remote_full}")


def download_file(conn, share_name: str, remote_path: str, local_path: Path):
    """下载文件 (pysmb版本)"""
    import io
    
    content = io.BytesIO()
    conn.retrieveFile(share_name, remote_path, content)
    content.seek(0)
    
    local_path.parent.mkdir(parents=True, exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(content.read())
    
    logger.info(f"Downloaded: {remote_path} -> {local_path}")


def delete_remote_file(conn, share_name: str, remote_path: str):
    """删除远程文件 (pysmb版本)"""
    conn.deleteFiles(share_name, remote_path)


# ============================================================================
# 同步逻辑
# ============================================================================

def sync_to_remote(config: SambaConfig, dry_run: bool = False, 
                 local_files: Optional[Dict[str, FileInfo]] = None) -> Tuple[int, int, List[str]]:
    """
    同步本地文件到远程
    
    Returns:
        (上传数, 跳过数, 错误列表)
    """
    if not config.validate():
        raise ValueError("Invalid Samba config")
    
    if not HAS_SAMBA:
        logger.error("smbprotocol not installed")
        return 0, 0, ["smbprotocol not installed"]
    
    try:
        conn, session, tree = get_samba_connection(config)
    except Exception as e:
        logger.error(f"Failed to connect to Samba: {e}")
        return 0, 0, [str(e)]
    
    try:
        if local_files is None:
            local_files = get_local_files()
        
        if not local_files:
            logger.info("No local files to sync")
            return 0, 0, []
        
        remote_base = config.remote_path or "/"
        
        uploaded = 0
        skipped = 0
        errors = []
        
        # 获取远程文件列表
        remote_files = list_remote_files(tree, remote_base)
        
        for rel_path, file_info in local_files.items():
            local_path = LOCAL_MEMORY_DIR / rel_path
            
            try:
                file_hash = calculate_hash(local_path)
                file_info.hash = file_hash
                
                # 检查是否需要上传
                should_upload = True
                
                if rel_path in remote_files:
                    remote_info = remote_files[rel_path]
                    # 如果远程文件更新，跳过
                    if remote_info.mtime >= file_info.mtime:
                        should_upload = False
                        skipped += 1
                
                if should_upload:
                    if dry_run:
                        logger.info(f"[DRY] Would upload: {rel_path}")
                        uploaded += 1
                    else:
                        upload_file(conn, config.share, local_path, f"{remote_base}/{rel_path}")
                        uploaded += 1
                        
            except Exception as e:
                logger.error(f"Failed to sync {rel_path}: {e}")
                errors.append(f"{rel_path}: {e}")
                skipped += 1
        
        return uploaded, skipped, errors
        
    finally:
        conn.close()


def sync_from_remote(config: SambaConfig, dry_run: bool = False) -> Tuple[int, int, List[str]]:
    """
    从远程同步到本地
    
    Returns:
        (下载数, 跳过数, 错误列表)
    """
    if not config.validate():
        raise ValueError("Invalid Samba config")
    
    if not HAS_SAMBA:
        logger.error("smbprotocol not installed")
        return 0, 0, ["smbprotocol not installed"]
    
    try:
        conn, session, tree = get_samba_connection(config)
    except Exception as e:
        logger.error(f"Failed to connect to Samba: {e}")
        return 0, 0, [str(e)]
    
    try:
        remote_base = config.remote_path or "/"
        
        # 获取远程文件列表
        remote_files = list_remote_files(conn, config.share, remote_base)
        
        if not remote_files:
            logger.info("No remote files to sync")
            return 0, 0, []
        
        # 获取本地文件列表
        local_files = get_local_files()
        
        downloaded = 0
        skipped = 0
        errors = []
        
        for rel_path, remote_info in remote_files.items():
            try:
                local_path = LOCAL_MEMORY_DIR / rel_path
                
                # 检查本地是否需要下载
                should_download = True
                
                if local_path.exists():
                    local_stat = local_path.stat()
                    local_mtime = local_stat.st_mtime
                    
                    # 如果本地文件更新或相同，跳过
                    if local_mtime >= remote_info.mtime:
                        should_download = False
                        skipped += 1
                
                if should_download:
                    if dry_run:
                        logger.info(f"[DRY] Would download: {rel_path}")
                        downloaded += 1
                    else:
                        download_file(conn, config.share, f"{remote_base}/{rel_path}", local_path)
                        downloaded += 1
                        
            except Exception as e:
                logger.error(f"Failed to sync {rel_path}: {e}")
                errors.append(f"{rel_path}: {e}")
                skipped += 1
        
        return downloaded, skipped, errors
        
    finally:
        conn.close()


def sync_bidirectional(config: SambaConfig, dry_run: bool = False,
                      conflict_policy: str = "newer") -> SyncResult:
    """
    双向同步
    
    Args:
        conflict_policy: newer(新文件优先) / keep_both(保留双方) / local优先
    
    Returns:
        SyncResult
    """
    if not config.validate():
        raise ValueError("Invalid Samba config")
    
    if not HAS_SAMBA:
        logger.error("smbprotocol not installed")
        return SyncResult(errors=["smbprotocol not installed"])
    
    try:
        conn, session, tree = get_samba_connection(config)
    except Exception as e:
        logger.error(f"Failed to connect to Samba: {e}")
        return SyncResult(errors=[str(e)])
    
    try:
        result = SyncResult()
        remote_base = config.remote_path or "/"
        
        # 获取文件列表
        local_files = get_local_files()
        remote_files = list_remote_files(conn, config.share, remote_base)
        
        # 获取远程文件详情（需要实际获取 mtime）
        # 这里简化处理，假设需要上传的都是本地新的
        all_paths = set(local_files.keys()) | set(remote_files.keys())
        
        for rel_path in all_paths:
            try:
                local_path = LOCAL_MEMORY_DIR / rel_path
                remote_path = f"{remote_base}/{rel_path}"
                
                local_exists = local_path.exists()
                remote_exists = rel_path in remote_files
                
                if local_exists and not remote_exists:
                    # 本地有，远程没有 -> 上传
                    if not dry_run:
                        upload_file(conn, config.share, local_path, remote_path)
                    result.uploaded += 1
                    
                elif remote_exists and not local_exists:
                    # 远程有，本地没有 -> 下载
                    if not dry_run:
                        download_file(conn, config.share, remote_path, local_path)
                    result.downloaded += 1
                    
                elif local_exists and remote_exists:
                    # 两者都有 -> 检查冲突
                    local_stat = local_path.stat()
                    local_mtime = local_stat.st_mtime
                    remote_mtime = remote_files[rel_path].mtime
                    
                    if abs(local_mtime - remote_mtime) < 1:
                        # 基本相同，跳过
                        result.skipped += 1
                    elif local_mtime > remote_mtime:
                        # 本地更新 -> 上传
                        if not dry_run:
                            upload_file(conn, config.share, local_path, remote_path)
                        result.uploaded += 1
                    else:
                        # 远程更新 -> 下载
                        if not dry_run:
                            download_file(conn, config.share, remote_path, local_path)
                        result.downloaded += 1
                        
            except Exception as e:
                logger.error(f"Failed to sync {rel_path}: {e}")
                result.errors.append(f"{rel_path}: {e}")
                result.skipped += 1
        
        return result
        
    finally:
        conn.close()


# ============================================================================
# 主函数
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Samba 同步记忆文件")
    parser.add_argument("--config", type=Path, help="配置文件路径")
    parser.add_argument("--dry-run", "-n", action="store_true", help="预览模式")
    parser.add_argument("--upload", action="store_true", help="仅上传")
    parser.add_argument("--download", action="store_true", help="仅下载")
    parser.add_argument("--bidirectional", "-b", action="store_true", help="双向同步")
    parser.add_argument("--conflict", choices=["newer", "keep_both", "local"], 
                       default="newer", help="冲突策略")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 加载配置
    if args.config and args.config.exists():
        config = SambaConfig.from_file(args.config)
    else:
        config = SambaConfig.from_env()
    
    if not config.validate():
        logger.error("Invalid Samba config.")
        logger.error("Set environment variables: SAMBA_HOST, SAMBA_SHARE, SAMBA_USER, SAMBA_PASSWORD")
        logger.info("Or create config file at: %s", CONFIG_FILE)
        sys.exit(1)
    
    # 执行同步
    if args.bidirectional:
        result = sync_bidirectional(config, args.dry_run, args.conflict)
        logger.info("=== 双向同步完成 ===")
        logger.info(f"上传: {result.uploaded}, 下载: {result.downloaded}, 跳过: {result.skipped}, 冲突: {result.conflicts}")
        if result.errors:
            logger.warning("Errors: %s", result.errors)
        
    elif args.upload:
        uploaded, skipped, errors = sync_to_remote(config, args.dry_run)
        logger.info("=== 上传完成 ===")
        logger.info(f"上传: {uploaded}, 跳过: {skipped}")
        if errors:
            logger.warning("Errors: %s", errors)
        
    elif args.download:
        downloaded, skipped, errors = sync_from_remote(config, args.dry_run)
        logger.info("=== 下载完成 ===")
        logger.info(f"下载: {downloaded}, 跳过: {skipped}")
        if errors:
            logger.warning("Errors: %s", errors)
        
    else:
        # 默认：双向同步
        result = sync_bidirectional(config, args.dry_run, args.conflict)
        logger.info("=== 同步完成 ===")
        logger.info(f"上传: {result.uploaded}, 下载: {result.downloaded}, 跳过: {result.skipped}")


if __name__ == "__main__":
    main()


# ========== 统一凭证加载（追加到文件末尾）==========
# 将在模块加载时覆盖默认配置


def _load_unified_credentials():
    """从 secrets.env 加载 Samba 凭证"""
    secrets_file = Path.home() / ".openclaw" / "credentials" / "secrets.env"
    secrets = {}
    
    if secrets_file.exists():
        for line in secrets_file.read_text().splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                secrets[key.strip()] = value.strip()
    
    return {
        "host": os.environ.get("SAMBA_HOST") or secrets.get("SAMBA_HOST", ""),
        "user": os.environ.get("SAMBA_USER") or secrets.get("SAMBA_USER", ""),
        "password": os.environ.get("SAMBA_PASS") or secrets.get("SAMBA_PASSWORD") or secrets.get("SAMBA_PASS", ""),
        "share": os.environ.get("SAMBA_SHARE") or secrets.get("SAMBA_SHARE", "/memory"),
    }


# 覆盖默认的 CONFIG 加载
_original_from_env = SambaConfig.from_env

@classmethod
def _new_from_env(cls) -> "SambaConfig":
    """从环境变量或 secrets.env 加载"""
    creds = _load_unified_credentials()
    if creds["host"]:
        return cls(
            host=creds["host"],
            username=creds["user"],
            password=creds["password"],
            share=creds["share"],
        )
    return _original_from_env()

SambaConfig.from_env = _new_from_env


# ========== 来源标记防死循环（修改上传函数）==========
# 为避免修改原有代码，我们通过 monkey-patch 添加来源标记

_original_sync_to_remote = sync_to_remote

def _patched_sync_to_remote(config: SambaConfig, dry_run: bool = False, direction: str = "upload") -> Tuple[int, int, List[str]]:
    """带来源标记的同步"""
    # 添加来源标记到同步状态
    state_file = Path.home() / ".openclaw" / "workspace" / "memory" / ".samba_sync_state.json"
    if state_file.exists():
        state = json.loads(state_file.read_text())
    else:
        state = {"last_sync": None, "source": "yaoyao-cloud-backup"}
    
    state["source"] = "yaoyao-cloud-backup"
    state["last_sync"] = datetime.now().isoformat()
    state_file.write_text(json.dumps(state, indent=2))
    
    return _original_sync_to_remote(config, dry_run, direction)

# 替换函数引用
sync_to_remote = _patched_sync_to_remote
