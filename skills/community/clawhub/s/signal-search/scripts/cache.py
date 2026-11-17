"""scripts/cache.py - 结果缓存（默认关，M03）。file-based JSON，TTL。

D6 修复：过期条目在 get() 时即删除（不再残留 .cache/ 无限增长）；另提供
cleanup() 主动清过期，run 长进程可周期性调用。同时消除 get() 的 TOCTOU
（exists 后 open 之间的竞态）——改为直接 open 并吞 FileNotFoundError。
"""

import hashlib
import json
import os
import time
from typing import Any

from common import load_config as _load_cfg


class Cache:
    def __init__(self, cfg: dict = None):
        c = (cfg or _load_cfg()).get("cache", {})
        self.enabled = c.get("enabled", True)
        self.ttl = c.get("ttl_minutes", 1440)
        self.dir = c.get("dir", ".cache/")
        if self.enabled:
            os.makedirs(self.dir, exist_ok=True)

    def _path(self, key: str) -> str:
        h = hashlib.md5(key.encode("utf-8")).hexdigest()
        return os.path.join(self.dir, h + ".json")

    def _expired(self, rec: dict) -> bool:
        # TTL<=0 视为立即过期（如测试用 ttl_minutes=0）。用 >=0 的严格 > 在
        # put/get 落在同一时钟刻度时会得到 elapsed==0 而不过期，造成偶发失败。
        if self.ttl <= 0:
            return True
        return time.time() - rec.get("ts", 0) > self.ttl * 60

    def get(self, key: str) -> Any:
        if not self.enabled:
            return None
        p = self._path(key)
        try:
            with open(p, "r", encoding="utf-8") as f:
                rec = json.load(f)
        except FileNotFoundError:
            return None  # TOCTOU 修复：直接 open，缺失即未命中
        except Exception:
            return None
        if self._expired(rec):
            try:
                os.remove(p)  # D6：过期即删，避免 .cache/ 无界增长
            except Exception:
                pass
            return None
        return rec.get("val")

    def put(self, key: str, val: Any) -> None:
        if not self.enabled:
            return
        try:
            with open(self._path(key), "w", encoding="utf-8") as f:
                json.dump({"ts": time.time(), "val": val}, f, ensure_ascii=False)
        except Exception:
            pass

    def cleanup(self) -> int:
        """删除所有过期缓存文件，返回清理条数（enabled=False 时返回 0）。"""
        if not self.enabled:
            return 0
        n = 0
        try:
            for fn in os.listdir(self.dir):
                if not fn.endswith(".json"):
                    continue
                p = os.path.join(self.dir, fn)
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        rec = json.load(f)
                    if self._expired(rec):
                        os.remove(p)
                        n += 1
                except Exception:
                    continue
        except Exception:
            pass
        return n
