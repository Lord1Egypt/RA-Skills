"""
backup.py - 备份与恢复工具

支持：
- SQLite 在线备份（不阻塞读写）
- 向量库快照（ChromaDB 导出）
- 全量 JSON 导出（可读、可迁移）
- 增量备份（基于时间戳）
- 自动清理过期备份
- 一键恢复
- Fernet 对称加密
- 远程存储（S3 / OSS / 本地）
- 定时备份调度

用法:
    python3 backup.py create                    # 创建完整备份
    python3 backup.py create --type json        # 仅 JSON 导出
    python3 backup.py list                      # 列出备份
    python3 backup.py restore backup_20260412   # 恢复备份
    python3 backup.py cleanup --keep-days 7     # 清理过期备份
"""

from __future__ import annotations

import os
import sys
import json
import shutil
import sqlite3
import logging
import threading
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# Remote Storage Interface
# ═══════════════════════════════════════════════════════════════

class BackupStorage(ABC):
    """Abstract interface for backup remote storage."""

    @abstractmethod
    def upload(self, local_path: str, remote_name: str) -> dict:
        """Upload a local file to remote storage.

        Returns: {"uploaded": bool, "remote_name": str, "size_bytes": int}
        """

    @abstractmethod
    def download(self, remote_name: str, local_path: str) -> dict:
        """Download a file from remote storage.

        Returns: {"downloaded": bool, "local_path": str, "size_bytes": int}
        """

    @abstractmethod
    def list_backups(self) -> list[dict]:
        """List all backups in remote storage.

        Returns: [{"name": str, "size_bytes": int, "last_modified": str}, ...]
        """

    @abstractmethod
    def delete(self, remote_name: str) -> bool:
        """Delete a backup from remote storage."""


class LocalBackupStorage(BackupStorage):
    """Local filesystem backup storage (existing behavior)."""

    def __init__(self, backup_dir: str = None):
        self.backup_dir = backup_dir or os.path.join(
            os.environ.get("AGENT_MEMORY_DATA_DIR", os.path.expanduser("~/.agent_memory")),
            "backups",
        )
        os.makedirs(self.backup_dir, exist_ok=True)

    def upload(self, local_path: str, remote_name: str) -> dict:
        target = os.path.join(self.backup_dir, remote_name)
        try:
            shutil.copy2(local_path, target)
            return {
                "uploaded": True,
                "remote_name": remote_name,
                "size_bytes": os.path.getsize(target),
            }
        except Exception as e:
            logger.error("LocalBackupStorage upload failed: %s", e)
            return {"uploaded": False, "remote_name": remote_name, "size_bytes": 0}

    def download(self, remote_name: str, local_path: str) -> dict:
        source = os.path.join(self.backup_dir, remote_name)
        try:
            shutil.copy2(source, local_path)
            return {
                "downloaded": True,
                "local_path": local_path,
                "size_bytes": os.path.getsize(local_path),
            }
        except Exception as e:
            logger.error("LocalBackupStorage download failed: %s", e)
            return {"downloaded": False, "local_path": local_path, "size_bytes": 0}

    def list_backups(self) -> list[dict]:
        result = []
        if not os.path.exists(self.backup_dir):
            return result
        for item in os.listdir(self.backup_dir):
            path = os.path.join(self.backup_dir, item)
            if os.path.isfile(path):
                stat = os.stat(path)
                result.append({
                    "name": item,
                    "size_bytes": stat.st_size,
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
        return sorted(result, key=lambda x: x["last_modified"], reverse=True)

    def delete(self, remote_name: str) -> bool:
        path = os.path.join(self.backup_dir, remote_name)
        try:
            if os.path.exists(path):
                os.unlink(path)
            # Also delete meta file
            meta_path = path + ".meta.json"
            if os.path.exists(meta_path):
                os.unlink(meta_path)
            return True
        except Exception as e:
            logger.error("LocalBackupStorage delete failed: %s", e)
            return False


class S3BackupStorage(BackupStorage):
    """AWS S3 backup storage (requires boto3, lazy-imported)."""

    def __init__(self, bucket: str = None, region: str = None, prefix: str = "backups/"):
        self.bucket = bucket or os.environ.get("AGENT_MEMORY_BACKUP_BUCKET", "")
        self.region = region or os.environ.get("AGENT_MEMORY_BACKUP_REGION", "us-east-1")
        self.prefix = prefix
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client
        try:
            import boto3
        except ImportError:
            raise ImportError(
                "S3 backup storage requires 'boto3'. Install with: pip install boto3"
            )
        if not self.bucket:
            raise ValueError(
                "S3 bucket not configured. Set AGENT_MEMORY_BACKUP_BUCKET env var."
            )
        self._client = boto3.client("s3", region_name=self.region)
        return self._client

    def upload(self, local_path: str, remote_name: str) -> dict:
        try:
            client = self._get_client()
            key = self.prefix + remote_name
            client.upload_file(local_path, self.bucket, key)
            return {
                "uploaded": True,
                "remote_name": remote_name,
                "size_bytes": os.path.getsize(local_path),
            }
        except Exception as e:
            logger.error("S3BackupStorage upload failed: %s", e)
            return {"uploaded": False, "remote_name": remote_name, "size_bytes": 0}

    def download(self, remote_name: str, local_path: str) -> dict:
        try:
            client = self._get_client()
            key = self.prefix + remote_name
            client.download_file(self.bucket, key, local_path)
            return {
                "downloaded": True,
                "local_path": local_path,
                "size_bytes": os.path.getsize(local_path),
            }
        except Exception as e:
            logger.error("S3BackupStorage download failed: %s", e)
            return {"downloaded": False, "local_path": local_path, "size_bytes": 0}

    def list_backups(self) -> list[dict]:
        try:
            client = self._get_client()
            response = client.list_objects_v2(Bucket=self.bucket, Prefix=self.prefix)
            result = []
            for obj in response.get("Contents", []):
                result.append({
                    "name": obj["Key"].replace(self.prefix, ""),
                    "size_bytes": obj["Size"],
                    "last_modified": obj["LastModified"].isoformat(),
                })
            return result
        except Exception as e:
            logger.error("S3BackupStorage list_backups failed: %s", e)
            return []

    def delete(self, remote_name: str) -> bool:
        try:
            client = self._get_client()
            key = self.prefix + remote_name
            client.delete_object(Bucket=self.bucket, Key=key)
            return True
        except Exception as e:
            logger.error("S3BackupStorage delete failed: %s", e)
            return False


class OSSBackupStorage(BackupStorage):
    """Alibaba Cloud OSS backup storage (requires oss2, lazy-imported)."""

    def __init__(self, bucket: str = None, endpoint: str = None, prefix: str = "backups/"):
        self.bucket = bucket or os.environ.get("AGENT_MEMORY_BACKUP_BUCKET", "")
        self.endpoint = endpoint or os.environ.get("AGENT_MEMORY_BACKUP_OSS_ENDPOINT", "")
        self.prefix = prefix
        self._bucket_obj = None

    def _get_bucket(self):
        if self._bucket_obj is not None:
            return self._bucket_obj
        try:
            import oss2
        except ImportError:
            raise ImportError(
                "OSS backup storage requires 'oss2'. Install with: pip install oss2"
            )
        if not self.bucket:
            raise ValueError(
                "OSS bucket not configured. Set AGENT_MEMORY_BACKUP_BUCKET env var."
            )
        auth = oss2.Auth(
            os.environ.get("AGENT_MEMORY_BACKUP_OSS_ACCESS_KEY", ""),
            os.environ.get("AGENT_MEMORY_BACKUP_OSS_SECRET_KEY", ""),
        )
        self._bucket_obj = oss2.Bucket(auth, self.endpoint, self.bucket)
        return self._bucket_obj

    def upload(self, local_path: str, remote_name: str) -> dict:
        try:
            bucket = self._get_bucket()
            key = self.prefix + remote_name
            bucket.put_object_from_file(key, local_path)
            return {
                "uploaded": True,
                "remote_name": remote_name,
                "size_bytes": os.path.getsize(local_path),
            }
        except Exception as e:
            logger.error("OSSBackupStorage upload failed: %s", e)
            return {"uploaded": False, "remote_name": remote_name, "size_bytes": 0}

    def download(self, remote_name: str, local_path: str) -> dict:
        try:
            bucket = self._get_bucket()
            key = self.prefix + remote_name
            bucket.get_object_to_file(key, local_path)
            return {
                "downloaded": True,
                "local_path": local_path,
                "size_bytes": os.path.getsize(local_path),
            }
        except Exception as e:
            logger.error("OSSBackupStorage download failed: %s", e)
            return {"downloaded": False, "local_path": local_path, "size_bytes": 0}

    def list_backups(self) -> list[dict]:
        try:
            bucket = self._get_bucket()
            import oss2  # noqa: F811 — re-import after _get_bucket ensures availability
            result = []
            for obj in oss2.ObjectIterator(bucket, prefix=self.prefix):
                result.append({
                    "name": obj.key.replace(self.prefix, ""),
                    "size_bytes": obj.size,
                    "last_modified": obj.last_modified,
                })
            return result
        except Exception as e:
            logger.error("OSSBackupStorage list_backups failed: %s", e)
            return []

    def delete(self, remote_name: str) -> bool:
        try:
            bucket = self._get_bucket()
            key = self.prefix + remote_name
            bucket.delete_object(key)
            return True
        except Exception as e:
            logger.error("OSSBackupStorage delete failed: %s", e)
            return False


def create_storage_from_env() -> BackupStorage:
    """Create a BackupStorage instance based on AGENT_MEMORY_BACKUP_STORAGE env var."""
    storage_type = os.environ.get("AGENT_MEMORY_BACKUP_STORAGE", "local").lower()
    if storage_type == "s3":
        return S3BackupStorage()
    elif storage_type == "oss":
        return OSSBackupStorage()
    else:
        return LocalBackupStorage()


# ═══════════════════════════════════════════════════════════════
# Backup Encryption
# ═══════════════════════════════════════════════════════════════

def _get_fernet():
    """Get Fernet instance for backup encryption."""
    key = os.environ.get("AGENT_MEMORY_BACKUP_ENCRYPTION_KEY") or os.environ.get("AGENT_MEMORY_ENCRYPTION_KEY")
    if not key:
        raise ValueError(
            "备份加密需要设置 AGENT_MEMORY_BACKUP_ENCRYPTION_KEY 环境变量。"
            "请运行: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
        )
    if key == "_fail":
        raise ValueError("备份加密密钥配置为 _fail，拒绝操作")
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        raise ImportError(
            "Backup encryption requires 'cryptography'. Install with: pip install cryptography"
        )
    return Fernet(key.encode())


def encrypt_file(source_path: str, dest_path: str = None, key_path: str = None) -> dict:
    """Encrypt a file using Fernet symmetric encryption.

    Args:
        source_path: Path to the file to encrypt
        dest_path: Output path (default: source_path + '.enc')
        key_path: Path to save the encryption key (optional)

    Returns: {"encrypted": bool, "path": str, "size_bytes": int}
    """
    try:
        fernet = _get_fernet()
    except (ImportError, ValueError) as e:
        return {"encrypted": False, "path": source_path, "size_bytes": 0, "error": str(e)}

    dest_path = dest_path or source_path + ".enc"

    try:
        with open(source_path, "rb") as f:
            data = f.read()

        encrypted = fernet.encrypt(data)

        with open(dest_path, "wb") as f:
            f.write(encrypted)

        # Optionally save key
        if key_path:
            with open(key_path, "wb") as f:
                f.write(fernet._signing_key + fernet._encryption_key)

        return {
            "encrypted": True,
            "path": dest_path,
            "size_bytes": len(encrypted),
        }
    except Exception as e:
        logger.error("encrypt_file failed: %s", e)
        return {"encrypted": False, "path": dest_path, "size_bytes": 0, "error": str(e)}


def decrypt_file(encrypted_path: str, dest_path: str = None, key_path: str = None) -> dict:
    """Decrypt a Fernet-encrypted file.

    Args:
        encrypted_path: Path to the encrypted file
        dest_path: Output path (default: encrypted_path without .enc suffix)
        key_path: Path to the encryption key file (optional, env var used if not provided)

    Returns: {"decrypted": bool, "path": str, "size_bytes": int}
    """
    try:
        fernet = _get_fernet()
    except (ImportError, ValueError) as e:
        return {"decrypted": False, "path": encrypted_path, "size_bytes": 0, "error": str(e)}

    if dest_path is None:
        if encrypted_path.endswith(".enc"):
            dest_path = encrypted_path[:-4]
        else:
            dest_path = encrypted_path + ".dec"

    try:
        with open(encrypted_path, "rb") as f:
            encrypted = f.read()

        decrypted = fernet.decrypt(encrypted)

        with open(dest_path, "wb") as f:
            f.write(decrypted)

        return {
            "decrypted": True,
            "path": dest_path,
            "size_bytes": len(decrypted),
        }
    except Exception as e:
        logger.error("decrypt_file failed: %s", e)
        return {"decrypted": False, "path": dest_path, "size_bytes": 0, "error": str(e)}


# ═══════════════════════════════════════════════════════════════
# Backup Scheduler
# ═══════════════════════════════════════════════════════════════

class BackupScheduler:
    """Periodic backup scheduler using threading.Timer.

    Features:
    - Anti-pile-up: skips backup if last one was too recent
    - Monotonic clock for interval tracking (immune to NTP adjustments)
    - Concurrent backup prevention via lock

    Usage:
        scheduler = BackupScheduler(backup_manager, interval_hours=24)
        scheduler.start()
        # ... later ...
        scheduler.stop()
    """

    def __init__(self, backup_manager: 'BackupManager', interval_hours: int = 24):
        self.manager = backup_manager
        self._interval_seconds = interval_hours * 3600
        self._last_backup_mono = 0.0  # monotonic timestamp of last backup
        self._backup_running = False
        self._lock = threading.Lock()
        self._timer = None
        self._stopped = False
        self._last_backup = None

    def __repr__(self):
        running = not getattr(self, '_stopped', True)
        return f"BackupScheduler(running={running})"

    def start(self):
        """Start periodic backups."""
        if not self._stopped and self._timer is not None:
            logger.warning("BackupScheduler already running")
            return
        self._stopped = False
        logger.info("BackupScheduler started (interval=%dh)", self._interval_seconds // 3600)
        self._schedule_next()

    def stop(self):
        """Stop the scheduler."""
        self._stopped = True
        if self._timer:
            self._timer.cancel()
            self._timer = None
        logger.info("BackupScheduler stopped")

    def _schedule_next(self):
        """Schedule the next backup."""
        if self._stopped:
            return
        self._timer = threading.Timer(self._interval_seconds, self._run_scheduled_backup)
        self._timer.daemon = True
        self._timer.start()

    def _run_scheduled_backup(self):
        """Execute a scheduled backup with anti-pile-up protection."""
        # Prevent concurrent backups
        with self._lock:
            if self._backup_running:
                logger.info("上一次备份仍在执行，跳过本次调度")
                self._schedule_next()
                return
            self._backup_running = True

        try:
            # Anti-pile-up: skip if last backup was too recent
            elapsed_since_last = time.monotonic() - self._last_backup_mono
            if self._last_backup_mono > 0 and elapsed_since_last < self._interval_seconds * 0.9:
                logger.info(
                    "距上次备份仅 %.0f 秒，跳过本次调度（间隔 %d 秒）",
                    elapsed_since_last, self._interval_seconds
                )
                self._schedule_next()
                return

            # Execute backup
            result = self.manager.create_backup(
                backup_type="full",
                compress=True,
                encrypt_backup=True,
                tag="scheduled",
            )
            self._last_backup_mono = time.monotonic()
            self._last_backup = result
            logger.info("定时备份完成: %s", result.get("backup_path", result.get("backup_id", "N/A")))
        except Exception as e:
            logger.error("定时备份失败: %s", e)
        finally:
            with self._lock:
                self._backup_running = False
            self._schedule_next()


# ═══════════════════════════════════════════════════════════════
# Backup Manager
# ═══════════════════════════════════════════════════════════════

class BackupManager:
    """备份与恢复管理器"""

    def __init__(self, db_path: str = None, backup_dir: str = None, project_dir: str = None):
        self.project_dir = project_dir or str(Path(__file__).parent)
        self.db_path = db_path or os.path.join(self.project_dir, "memory.db")
        self.backup_dir = backup_dir or os.path.join(self.project_dir, "backups")
        os.makedirs(self.backup_dir, exist_ok=True)

        # Remote storage (lazy initialization)
        self._storage = None
        self._scheduler = None
        self._backup_lock = threading.Lock()

    def __repr__(self):
        return f"BackupManager(dir={self.backup_dir!r})"

    @property
    def storage(self) -> BackupStorage:
        """Get or create the remote storage backend."""
        if self._storage is None:
            self._storage = create_storage_from_env()
        return self._storage

    @storage.setter
    def storage(self, value: BackupStorage):
        self._storage = value

    def create_backup(
        self,
        backup_type: str = "full",
        compress: bool = True,
        tag: str = None,
        encrypt_backup: bool = False,
    ) -> dict:
        """
        创建备份。

        参数:
            backup_type: "full" (SQLite + 向量 + JSON) / "db" (仅 SQLite) / "json" (仅 JSON)
            compress: 是否压缩
            tag: 备份标签（用于标识用途）
            encrypt_backup: 是否加密备份文件（使用 Fernet 对称加密）

        返回: {"backup_id": str, "files": list, "size_bytes": int, "duration_ms": int}
        """
        if not self._backup_lock.acquire(blocking=False):
            return {"error": "备份正在进行中，请稍后再试"}
        try:
            return self._create_backup_impl(backup_type, compress, tag, encrypt_backup)
        finally:
            self._backup_lock.release()

    def _create_backup_impl(
        self,
        backup_type: str = "full",
        compress: bool = True,
        tag: str = None,
        encrypt_backup: bool = False,
    ) -> dict:
        import time
        start = time.time()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tag_suffix = f"_{tag}" if tag else ""
        backup_id = f"backup_{timestamp}{tag_suffix}"
        backup_path = os.path.join(self.backup_dir, backup_id)
        os.makedirs(backup_path, exist_ok=True)

        files = []

        # 1. SQLite 在线备份
        if backup_type in ("full", "db"):
            db_backup = os.path.join(backup_path, "memory.db")
            self._backup_sqlite(db_backup)
            files.append("memory.db")

            # 冷库备份（如果存在）
            cold_db_path = self.db_path.replace(".db", "_cold.db")
            if os.path.exists(cold_db_path):
                cold_backup = os.path.join(backup_path, "memory_cold.db")
                self._backup_sqlite_to(cold_db_path, cold_backup)
                files.append("memory_cold.db")

            # 附带迁移记录
            try:
                conn = sqlite3.connect(self.db_path)
                try:
                    migrations = conn.execute("SELECT * FROM _migrations ORDER BY version").fetchall()
                finally:
                    conn.close()
                if migrations:
                    mig_file = os.path.join(backup_path, "migrations.json")
                    with open(mig_file, "w") as f:
                        json.dump([dict(m) for m in migrations], f, indent=2)
                    files.append("migrations.json")
            except Exception as e:
                logger.warning("backup: %s", e)

        # 2. 向量库（v6.0: 已合并到 SQLite，无需单独备份）

        # 3. JSON 导出（可读、可迁移）
        if backup_type in ("full", "json"):
            json_file = os.path.join(backup_path, "memories.json")
            self._export_json(json_file)
            files.append("memories.json")

        # 4. 质量统计
        quality_file = os.path.join(self.project_dir, "quality_stats.json")
        if os.path.exists(quality_file):
            shutil.copy2(quality_file, os.path.join(backup_path, "quality_stats.json"))
            files.append("quality_stats.json")

        # 5. 注册表
        registry_dir = os.path.join(self.project_dir, "registry")
        if os.path.exists(registry_dir):
            reg_backup = os.path.join(backup_path, "registry")
            shutil.copytree(registry_dir, reg_backup, dirs_exist_ok=True)
            files.append("registry/")

        # 6. 压缩
        total_size = sum(
            os.path.getsize(os.path.join(backup_path, f))
            for f in os.listdir(backup_path)
            if os.path.isfile(os.path.join(backup_path, f))
        )

        if compress:
            archive_path = shutil.make_archive(backup_path, "gztar", backup_path)
            # 删除未压缩的目录
            shutil.rmtree(backup_path)
            final_path = archive_path
            total_size = os.path.getsize(archive_path)
        else:
            final_path = backup_path

        # 7. 加密（可选）
        encrypted = False
        if encrypt_backup:
            try:
                _get_fernet()  # Validate key is available
            except ValueError as e:
                logger.error("备份加密失败: %s", e)
                logger.warning("将创建未加密备份（请尽快配置加密密钥）")
                encrypt_backup = False
            except ImportError as e:
                logger.error("备份加密失败: %s", e)
                logger.warning("将创建未加密备份（请安装 cryptography 库）")
                encrypt_backup = False

        if encrypt_backup:
            enc_result = encrypt_file(final_path)
            if enc_result["encrypted"]:
                # 删除未加密的备份文件
                try:
                    if os.path.exists(final_path) and final_path != enc_result["path"]:
                        os.unlink(final_path)
                except Exception:
                    pass
                final_path = enc_result["path"]
                total_size = enc_result["size_bytes"]
                encrypted = True
            else:
                logger.warning("备份加密失败: %s", enc_result.get("error", "unknown"))

        duration_ms = int((time.time() - start) * 1000)

        # 写入元数据
        meta = {
            "backup_id": backup_id,
            "created_at": timestamp,
            "type": backup_type,
            "files": files,
            "size_bytes": total_size,
            "duration_ms": duration_ms,
            "compressed": compress,
            "encrypted": encrypted,
            "tag": tag,
            "db_path": self.db_path,
        }

        # 备份验证：确保备份可用（仅对未加密的备份验证）
        if not encrypted:
            verify_result = self._verify_backup(backup_path if not compress else final_path, compress)
            meta["verified"] = verify_result["ok"]
            meta["verify_details"] = verify_result
            if not verify_result["ok"]:
                logger.error("备份验证失败: %s", verify_result['issues'])
                meta["verify_warning"] = "BACKUP VERIFICATION FAILED - may not be restorable"
        else:
            meta["verified"] = None
            meta["verify_details"] = {"note": "Skipped verification for encrypted backup"}

        meta_path = final_path + ".meta.json"
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)

        # 8. 上传到远程存储
        try:
            remote_name = os.path.basename(final_path)
            upload_result = self.storage.upload(final_path, remote_name)
            meta["remote_upload"] = upload_result
            # Also upload meta
            meta_remote = os.path.basename(meta_path)
            self.storage.upload(meta_path, meta_remote)
        except Exception as e:
            logger.warning("远程上传失败: %s", e)
            meta["remote_upload"] = {"uploaded": False, "error": str(e)}

        logger.info("备份完成: %s (%s bytes, %sms, verified=%s, encrypted=%s)",
                     backup_id, f"{total_size:,}", duration_ms,
                     meta.get("verified"), encrypted,
                     extra={
                         "event": "backup_created",
                         "backup_path": final_path,
                         "size_bytes": total_size,
                         "duration_ms": duration_ms,
                         "encrypted": encrypted,
                     })
        return meta

    def decrypt_backup(self, encrypted_path: str, key_path: str = None) -> dict:
        """Decrypt an encrypted backup file.

        Args:
            encrypted_path: Path to the encrypted backup file
            key_path: Path to the encryption key file (optional)

        Returns: {"decrypted": bool, "path": str, "size_bytes": int}
        """
        return decrypt_file(encrypted_path, key_path=key_path)

    def _verify_backup(self, backup_path: str, is_compressed: bool) -> dict:
        """验证备份完整性：SQLite 完整性 + 记忆条数 + 外键检查"""
        import tempfile
        issues = []
        db_path = None
        tmp_dir = None
        conn = None
        src_conn = None

        try:
            if is_compressed:
                # 解压到临时目录
                tmp_dir = tempfile.mkdtemp()
                shutil.unpack_archive(backup_path, tmp_dir)
                db_path = os.path.join(tmp_dir, "memory.db")
            else:
                db_path = os.path.join(backup_path, "memory.db")

            if not os.path.exists(db_path):
                issues.append("memory.db not found in backup")
                return {"ok": False, "issues": issues}

            # 打开备份数据库做验证
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row

            # 1. SQLite 完整性检查
            row = conn.execute("PRAGMA integrity_check").fetchone()
            if row and row[0] != "ok":
                issues.append(f"integrity_check: {row[0]}")

            # 2. 外键检查
            fk_violations = conn.execute("PRAGMA foreign_key_check").fetchall()
            if fk_violations:
                issues.append(f"foreign_key violations: {len(fk_violations)}")

            # 3. 记忆条数 vs 源数据库
            backup_count = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            try:
                src_conn = sqlite3.connect(self.db_path)
                src_count = src_conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
                if backup_count == 0 and src_count > 0:
                    issues.append(f"backup has 0 memories but source has {src_count}")
                elif backup_count < src_count:
                    # 增量差异允许（备份过程中可能有新写入），只记录不报错
                    pass
            except Exception as e:
                logger.warning("backup: %s", e)

            # 4. 关键表存在性检查
            tables = [r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()]
            required_tables = ["memories", "memory_topics", "memory_links", "memory_tools"]
            for t in required_tables:
                if t not in tables:
                    issues.append(f"missing table: {t}")

        except Exception as e:
            issues.append(f"verification error: {e}")
        finally:
            if src_conn:
                src_conn.close()
            if conn:
                conn.close()
            if tmp_dir and os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir, ignore_errors=True)

        return {"ok": len(issues) == 0, "issues": issues}

    def _backup_sqlite(self, target_path: str):
        """SQLite 在线备份（不阻塞读写）"""
        src = sqlite3.connect(self.db_path)
        dst = sqlite3.connect(target_path)
        try:
            with dst:
                src.backup(dst)
        finally:
            src.close()
            dst.close()

    def _backup_sqlite_to(self, src_path: str, target_path: str):
        """SQLite 在线备份（指定源路径）"""
        src = sqlite3.connect(src_path)
        dst = sqlite3.connect(target_path)
        try:
            with dst:
                src.backup(dst)
        finally:
            src.close()
            dst.close()

    def _export_json(self, output_path: str) -> int:
        """导出全部记忆为 JSON（流式写入，避免 OOM）"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            batch_size = 1000
            offset = 0
            total_exported = 0

            with open(output_path, "w", encoding="utf-8") as f:
                f.write('{\n  "version": "12.0",\n  "exported_at": ' +
                        json.dumps(time.strftime("%Y-%m-%dT%H:%M:%S")) +
                        ',\n  "memories": [\n')

                first = True
                while True:
                    rows = conn.execute(
                        "SELECT * FROM memories ORDER BY time_ts LIMIT ? OFFSET ?",
                        (batch_size, offset)
                    ).fetchall()
                    if not rows:
                        break

                    for row in rows:
                        record = dict(row)
                        # Convert special types
                        for key, val in record.items():
                            if isinstance(val, bytes):
                                record[key] = val.decode('utf-8', errors='replace')

                        if not first:
                            f.write(",\n")
                        first = False
                        json.dump(record, f, ensure_ascii=False, default=str)
                        total_exported += 1

                    offset += batch_size

                f.write('\n  ]\n}\n')

            return total_exported
        except Exception as e:
            logger.error("JSON导出失败: %s", e)
            return 0
        finally:
            if conn:
                conn.close()

    def list_backups(self) -> list[dict]:
        """列出所有备份"""
        backups = []
        for item in sorted(os.listdir(self.backup_dir)):
            item_path = os.path.join(self.backup_dir, item)
            meta_path = item_path + ".meta.json"

            if os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    meta = json.load(f)
                backups.append(meta)
            elif item.startswith("backup_"):
                # 没有元数据的旧备份
                size = os.path.getsize(item_path) if os.path.isfile(item_path) else sum(
                    os.path.getsize(os.path.join(dp, fn))
                    for dp, dn, fns in os.walk(item_path) for fn in fns
                )
                backups.append({
                    "backup_id": item,
                    "size_bytes": size,
                    "type": "unknown",
                })

        return backups

    def _verify_backup_integrity(self, backup_path: str) -> dict:
        """验证备份文件的完整性（文件存在性 + SQLite 完整性检查）。"""
        if not os.path.exists(backup_path):
            return {"valid": False, "reason": f"备份文件不存在: {backup_path}"}
        if not os.access(backup_path, os.R_OK):
            return {"valid": False, "reason": f"备份文件不可读: {backup_path}"}
        try:
            self._quick_verify_db(backup_path)
        except ValueError as e:
            return {"valid": False, "reason": str(e)}
        except Exception as e:
            return {"valid": False, "reason": f"备份验证异常: {e}"}
        return {"valid": True}

    def _quick_verify_db(self, db_path: str) -> bool:
        """快速数据库完整性检查。"""
        if not os.path.exists(db_path):
            raise ValueError(f"数据库文件不存在: {db_path}")
        if os.path.getsize(db_path) < 100:  # SQLite header is at least 100 bytes
            raise ValueError(f"数据库文件过小，可能损坏: {db_path}")
        conn = sqlite3.connect(db_path)
        try:
            result = conn.execute("PRAGMA integrity_check").fetchone()
            if result[0] != "ok":
                raise ValueError(f"数据库完整性检查失败: {result[0]}")
        finally:
            conn.close()
        return True

    def restore(self, backup_id: str, target_db: str = None) -> dict:
        """
        从备份恢复（原子写入 + 自动回滚）。

        参数:
            backup_id: 备份 ID
            target_db: 恢复目标路径（默认覆盖原数据库）

        返回: {"restored": list, "errors": list}
        """
        _restore_start = time.time()
        target_db = target_db or self.db_path

        # 查找备份
        backup_path = os.path.join(self.backup_dir, backup_id)
        archive_path = backup_path + ".tar.gz"
        encrypted_path = archive_path + ".enc"

        # 尝试解密
        if os.path.exists(encrypted_path):
            dec_result = decrypt_file(encrypted_path)
            if dec_result["decrypted"]:
                archive_path = dec_result["path"]
            else:
                return {"restored": [], "errors": [f"备份解密失败: {dec_result.get('error', 'unknown')}"]}

        if os.path.exists(archive_path):
            # 解压
            import tempfile
            tmp_dir = tempfile.mkdtemp()
            shutil.unpack_archive(archive_path, tmp_dir)
            backup_path = tmp_dir
        elif not os.path.exists(backup_path):
            # 尝试从远程下载
            try:
                remote_name = backup_id + ".tar.gz"
                local_archive = os.path.join(self.backup_dir, remote_name)
                dl_result = self.storage.download(remote_name, local_archive)
                if dl_result["downloaded"]:
                    import tempfile
                    tmp_dir = tempfile.mkdtemp()
                    shutil.unpack_archive(local_archive, tmp_dir)
                    backup_path = tmp_dir
                else:
                    return {"restored": [], "errors": [f"备份不存在: {backup_id}"]}
            except Exception as e:
                return {"restored": [], "errors": [f"备份不存在: {backup_id} ({e})"]}

        restored = []
        errors = []

        # 1. 原子恢复 SQLite
        db_backup = os.path.join(backup_path, "memory.db")
        if os.path.exists(db_backup):
            try:
                # 验证备份完整性
                verify_result = self._verify_backup_integrity(db_backup)
                if not verify_result.get("valid"):
                    errors.append(f"备份验证失败: {verify_result.get('reason')}")
                else:
                    # 创建 pre-restore 备份
                    pre_restore_path = target_db + ".pre_restore"
                    if os.path.exists(target_db):
                        shutil.copy2(target_db, pre_restore_path)

                    # 原子恢复: 写入 .tmp 后 os.replace()
                    tmp_path = target_db + ".tmp_restore"
                    try:
                        shutil.copy2(db_backup, tmp_path)
                        # 验证临时文件完整性
                        self._quick_verify_db(tmp_path)
                        # 原子替换
                        os.replace(tmp_path, target_db)
                        logger.info("原子恢复完成: %s → %s", db_backup, target_db)
                        restored.append("memory.db")
                    except Exception as e:
                        # 自动回滚: 从 pre_restore 恢复
                        logger.error("恢复失败，自动回滚: %s", e)
                        try:
                            if os.path.exists(pre_restore_path):
                                os.replace(pre_restore_path, target_db)
                                logger.info("已自动回滚到恢复前状态")
                        except Exception as rollback_err:
                            logger.critical("自动回滚也失败了！手动恢复: %s → %s", pre_restore_path, target_db)
                        errors.append(f"SQLite 恢复失败（已自动回滚）: {e}")
                    finally:
                        # 清理临时文件
                        if os.path.exists(tmp_path):
                            os.remove(tmp_path)
            except Exception as e:
                errors.append(f"SQLite 恢复失败: {e}")

        # 恢复冷库
        cold_backup = os.path.join(backup_path, "memory_cold.db")
        target_cold = target_db.replace(".db", "_cold.db") if target_db else self.db_path.replace(".db", "_cold.db")
        if os.path.exists(cold_backup):
            try:
                # 冷库也使用原子恢复
                verify_result = self._verify_backup_integrity(cold_backup)
                if not verify_result.get("valid"):
                    errors.append(f"冷库备份验证失败: {verify_result.get('reason')}")
                else:
                    pre_restore_cold = target_cold + ".pre_restore"
                    if os.path.exists(target_cold):
                        shutil.copy2(target_cold, pre_restore_cold)
                    tmp_cold = target_cold + ".tmp_restore"
                    try:
                        shutil.copy2(cold_backup, tmp_cold)
                        self._quick_verify_db(tmp_cold)
                        os.replace(tmp_cold, target_cold)
                        logger.info("冷库原子恢复完成: %s → %s", cold_backup, target_cold)
                        restored.append("memory_cold.db")
                    except Exception as e:
                        logger.error("冷库恢复失败，自动回滚: %s", e)
                        try:
                            if os.path.exists(pre_restore_cold):
                                os.replace(pre_restore_cold, target_cold)
                                logger.info("冷库已自动回滚到恢复前状态")
                        except Exception as rollback_err:
                            logger.critical("冷库自动回滚也失败了！手动恢复: %s → %s", pre_restore_cold, target_cold)
                        errors.append(f"冷库恢复失败（已自动回滚）: {e}")
                    finally:
                        if os.path.exists(tmp_cold):
                            os.remove(tmp_cold)
            except Exception as e:
                errors.append(f"冷库恢复失败: {e}")

        # 2. 恢复向量库（v6.0: 已合并到 SQLite，旧 chroma_db 备份忽略）
        chroma_backup = os.path.join(backup_path, "chroma_db")
        if os.path.exists(chroma_backup):
            restored.append("chroma_db/ (跳过: v6.0 向量已合入 SQLite)")

        # 3. 恢复质量统计
        quality_backup = os.path.join(backup_path, "quality_stats.json")
        if os.path.exists(quality_backup):
            try:
                shutil.copy2(quality_backup, os.path.join(self.project_dir, "quality_stats.json"))
                restored.append("quality_stats.json")
            except Exception as e:
                errors.append(f"质量统计恢复失败: {e}")

        _restore_elapsed = time.time() - _restore_start
        logger.info("backup_restored", extra={
            "event": "backup_restored",
            "backup_path": backup_path,
            "duration_ms": int(_restore_elapsed * 1000),
            "memories_restored": len(restored),
        })

        return {"restored": restored, "errors": errors}

    def cleanup(self, keep_days: int = 7) -> dict:
        """清理过期备份"""
        cutoff = datetime.now() - timedelta(days=keep_days)
        cleaned = []
        freed_bytes = 0

        for item in os.listdir(self.backup_dir):
            item_path = os.path.join(self.backup_dir, item)

            # 从名称提取时间
            try:
                # backup_20260412_120000[_tag]
                parts = item.replace(".tar.gz", "").replace(".meta.json", "").replace(".enc", "").split("_")
                if len(parts) >= 2 and parts[0] == "backup":
                    date_str = parts[1]
                    file_date = datetime.strptime(date_str, "%Y%m%d")
                    if file_date < cutoff:
                        size = os.path.getsize(item_path) if os.path.isfile(item_path) else 0
                        os.unlink(item_path) if os.path.isfile(item_path) else shutil.rmtree(item_path)
                        cleaned.append(item)
                        freed_bytes += size
                        # 清理元数据
                        meta = item_path + ".meta.json"
                        if os.path.exists(meta):
                            os.unlink(meta)
            except (ValueError, IndexError):
                continue

        return {"cleaned": cleaned, "count": len(cleaned), "freed_bytes": freed_bytes}

    # ── Scheduler Integration ──────────────────────────────────

    def start_scheduler(self, interval_hours: int = 24) -> BackupScheduler:
        """Start periodic backup scheduler.

        Args:
            interval_hours: Hours between backups

        Returns:
            The BackupScheduler instance
        """
        if self._scheduler and not self._scheduler._stopped:
            logger.warning("Scheduler already running")
            return self._scheduler
        self._scheduler = BackupScheduler(self, interval_hours=interval_hours)
        self._scheduler.start()
        return self._scheduler

    def stop_scheduler(self):
        """Stop the backup scheduler."""
        if self._scheduler:
            self._scheduler.stop()
            self._scheduler = None


def main():
    import argparse
    from logging_config import configure_logging
    configure_logging(level="INFO", fmt="%(message)s")

    parser = argparse.ArgumentParser(description="备份与恢复工具")
    parser.add_argument("command", choices=["create", "list", "restore", "cleanup"])
    parser.add_argument("--type", choices=["full", "db", "json"], default="full")
    parser.add_argument("--db", type=str, help="数据库路径")
    parser.add_argument("--backup-dir", type=str, help="备份目录")
    parser.add_argument("--keep-days", type=int, default=7, help="保留天数")
    parser.add_argument("--tag", type=str, help="备份标签")
    parser.add_argument("--encrypt", action="store_true", help="加密备份")
    parser.add_argument("backup_id", nargs="?", help="备份 ID (restore)")

    args = parser.parse_args()
    mgr = BackupManager(db_path=args.db, backup_dir=args.backup_dir)

    if args.command == "create":
        result = mgr.create_backup(backup_type=args.type, tag=args.tag, encrypt_backup=args.encrypt)
        print(f"备份 ID: {result['backup_id']}")
        print(f"大小: {result['size_bytes']:,} bytes")
        print(f"耗时: {result['duration_ms']}ms")
        print(f"文件: {', '.join(result['files'])}")
        if result.get('encrypted'):
            print("加密: 是")

    elif args.command == "list":
        backups = mgr.list_backups()
        if not backups:
            print("无备份")
        else:
            for b in backups:
                size_mb = b.get("size_bytes", 0) / 1024 / 1024
                enc = " [加密]" if b.get("encrypted") else ""
                print(f"  {b['backup_id']}  ({size_mb:.1f} MB)  [{b.get('type', '?')}]{enc}")

    elif args.command == "restore":
        if not args.backup_id:
            print("错误: 请提供备份 ID")
            sys.exit(1)
        result = mgr.restore(args.backup_id)
        print(f"已恢复: {', '.join(result['restored'])}")
        if result["errors"]:
            for e in result["errors"]:
                print(f"  ❌ {e}")

    elif args.command == "cleanup":
        result = mgr.cleanup(keep_days=args.keep_days)
        print(f"清理完成: 删除 {result['count']} 个备份, 释放 {result['freed_bytes']:,} bytes")


if __name__ == "__main__":
    main()
