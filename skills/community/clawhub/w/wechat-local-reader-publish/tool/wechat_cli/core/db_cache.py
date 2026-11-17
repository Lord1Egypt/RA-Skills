"""解密数据库缓存 — mtime 检测变化，跨会话复用"""

import hashlib
import json
import os
import tempfile

from .crypto import full_decrypt, decrypt_wal
from .key_utils import get_key_info


def _restrict_dir(path):
    """尽量收紧目录权限（macOS/Linux 生效；Windows 依赖系统用户隔离）。"""
    try:
        os.chmod(path, 0o700)
    except OSError:
        pass


def _restrict_file(path):
    """尽量收紧文件权限为 0600（明文解密库，含隐私）。"""
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


class DBCache:
    CACHE_DIR = os.path.join(tempfile.gettempdir(), "wechat_cli_cache")
    MTIME_FILE = os.path.join(tempfile.gettempdir(), "wechat_cli_cache", "_mtimes.json")

    def __init__(self, all_keys, db_dir):
        self._all_keys = all_keys
        self._db_dir = db_dir
        self._cache = {}  # rel_key -> (db_mtime, wal_mtime, tmp_path)
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        _restrict_dir(self.CACHE_DIR)
        self._load_persistent_cache()

    def _cache_path(self, rel_key):
        h = hashlib.md5(rel_key.encode()).hexdigest()[:12]
        return os.path.join(self.CACHE_DIR, f"{h}.db")

    def _load_persistent_cache(self):
        if not os.path.exists(self.MTIME_FILE):
            return
        try:
            with open(self.MTIME_FILE, encoding="utf-8") as f:
                saved = json.load(f)
        except (json.JSONDecodeError, OSError):
            return
        for rel_key, info in saved.items():
            tmp_path = info["path"]
            if not os.path.exists(tmp_path):
                continue
            rel_path = rel_key.replace('\\', os.sep)
            db_path = os.path.join(self._db_dir, rel_path)
            wal_path = db_path + "-wal"
            try:
                db_mtime = os.path.getmtime(db_path)
                wal_mtime = os.path.getmtime(wal_path) if os.path.exists(wal_path) else 0
            except OSError:
                continue
            if db_mtime == info["db_mt"] and wal_mtime == info["wal_mt"]:
                self._cache[rel_key] = (db_mtime, wal_mtime, tmp_path)

    def _save_persistent_cache(self):
        data = {}
        for rel_key, (db_mt, wal_mt, path) in self._cache.items():
            data[rel_key] = {"db_mt": db_mt, "wal_mt": wal_mt, "path": path}
        try:
            with open(self.MTIME_FILE, 'w', encoding="utf-8") as f:
                json.dump(data, f)
        except OSError:
            pass

    def get(self, rel_key):
        key_info = get_key_info(self._all_keys, rel_key)
        if not key_info:
            return None
        rel_path = rel_key.replace('\\', '/').replace('/', os.sep)
        db_path = os.path.join(self._db_dir, rel_path)
        wal_path = db_path + "-wal"
        if not os.path.exists(db_path):
            return None

        try:
            db_mtime = os.path.getmtime(db_path)
            wal_mtime = os.path.getmtime(wal_path) if os.path.exists(wal_path) else 0
        except OSError:
            return None

        if rel_key in self._cache:
            c_db_mt, c_wal_mt, c_path = self._cache[rel_key]
            if c_db_mt == db_mtime and c_wal_mt == wal_mtime and os.path.exists(c_path):
                return c_path

        tmp_path = self._cache_path(rel_key)
        enc_key = bytes.fromhex(key_info["enc_key"])
        full_decrypt(db_path, tmp_path, enc_key)
        _restrict_file(tmp_path)
        if os.path.exists(wal_path):
            decrypt_wal(wal_path, tmp_path, enc_key)
        self._cache[rel_key] = (db_mtime, wal_mtime, tmp_path)
        self._save_persistent_cache()
        return tmp_path

    def cleanup(self):
        self._save_persistent_cache()

    @classmethod
    def clear_cache(cls):
        """彻底删除解密缓存（明文数据库 + 状态文件），用于退出即清、避免明文残留。

        仅删除本工具在 $TMPDIR 下创建的内容，不影响微信原始加密数据库。
        返回删除的文件数。
        """
        removed = 0
        if os.path.isdir(cls.CACHE_DIR):
            for entry in os.listdir(cls.CACHE_DIR):
                p = os.path.join(cls.CACHE_DIR, entry)
                try:
                    if os.path.isfile(p):
                        os.remove(p)
                        removed += 1
                    else:
                        import shutil
                        shutil.rmtree(p)
                        removed += 1
                except OSError:
                    pass
            try:
                os.rmdir(cls.CACHE_DIR)
            except OSError:
                pass
        return removed
