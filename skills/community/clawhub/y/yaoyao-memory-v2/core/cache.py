from typing import Optional
"""缓存管理器 - 增量缓存 + 压缩"""
import json
import gzip
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, cache_dir: str, ttl: int = 3600):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl
        self.index_file = self.cache_dir / "index.json"
        self.index = self._load_index()
    
    def _load_index(self) -> dict:
        if self.index_file.exists():
            try:
                return json.loads(self.index_file.read_text())
            except:
                pass
        return {}
    
    def _save_index(self):
        self.index_file.write_text(json.dumps(self.index, ensure_ascii=False))
    
    def _compress(self, data: dict) -> bytes:
        return gzip.compress(json.dumps(data, ensure_ascii=False).encode())
    
    def _decompress(self, data: bytes) -> dict:
        return json.loads(gzip.decompress(data).decode())
    
    def get(self, key: str) -> Optional[dict]:
        if key not in self.index:
            return None
        
        entry = self.index[key]
        cached_time = datetime.fromisoformat(entry["time"])
        
        if datetime.now() - cached_time > timedelta(seconds=self.ttl):
            self.delete(key)
            return None
        
        file = self.cache_dir / f"{key}.cache"
        if file.exists():
            try:
                return self._decompress(file.read_bytes())
            except:
                pass
        return None
    
    def set(self, key: str, data: dict):
        file = self.cache_dir / f"{key}.cache"
        compressed = self._compress(data)
        file.write_bytes(compressed)
        
        self.index[key] = {
            "time": datetime.now().isoformat(),
            "size": len(compressed)
        }
        self._save_index()
    
    def delete(self, key: str):
        file = self.cache_dir / f"{key}.cache"
        if file.exists():
            file.unlink()
        if key in self.index:
            del self.index[key]
            self._save_index()
    
    def cleanup(self) -> int:
        """清理过期缓存"""
        expired = []
        for key, entry in self.index.items():
            cached_time = datetime.fromisoformat(entry["time"])
            if datetime.now() - cached_time > timedelta(seconds=self.ttl):
                expired.append(key)
        
        for key in expired:
            self.delete(key)
        
        return len(expired)
    
    def stats(self) -> dict:
        total_size = sum(e.get("size", 0) for e in self.index.values())
        return {
            "count": len(self.index),
            "total_size_kb": total_size / 1024
        }
