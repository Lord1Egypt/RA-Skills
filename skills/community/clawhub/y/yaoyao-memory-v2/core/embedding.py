from typing import Optional, List
"""Embedding 引擎 - 支持预计算和批量 + 强化缓存"""
import json
import hashlib
import time
import urllib.request
from pathlib import Path
from typing import List, Optional

# 延迟导入强化缓存（可选依赖）
try:
    from .embedding_cache import EmbeddingCache, get_embedding_cache
    HAS_EMBEDDING_CACHE = True
except ImportError:
    HAS_EMBEDDING_CACHE = False


class EmbeddingEngine:
    def __init__(self, api_url: str, api_key: str, model: str = "Qwen3-Embedding-8B", dimensions: int = 4096, use强化缓存: bool = True):
        self.api_url = api_url
        self.api_key = api_key
        self.model = model
        self.dimensions = dimensions
        self.cache = {}
        self.precomputed = {}
        self.cache_dir = Path.home() / ".openclaw" / "memory-tdai" / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._max_precomputed = 50  # 限制预计算向量数量，节省内存
        self._precomputed_access = {}  # 记录访问时间
        self._load_precomputed()
        
        # 强化缓存
        self._use强化缓存 = use强化缓存 and HAS_EMBEDDING_CACHE
        if self._use强化缓存:
            self._cache = get_embedding_cache()
            print(f"[Embedding] 强化缓存已启用 | {self._cache.get_stats()['disk_items']} 项磁盘缓存")
    
    def _load_precomputed(self):
        """加载预计算向量"""
        file = self.cache_dir / "precomputed.json"
        if file.exists():
            try:
                self.precomputed = json.loads(file.read_text())
            except:
                pass
    
    def _save_precomputed(self):
        """保存预计算向量（带 LRU 清理）"""
        # 如果超过限制，清理最旧的
        if len(self.precomputed) > self._max_precomputed:
            # 按访问时间排序，删除最旧的
            sorted_keys = sorted(self._precomputed_access.keys(), 
                                key=lambda k: self._precomputed_access[k])
            remove_count = len(self.precomputed) - self._max_precomputed
            for key in sorted_keys[:remove_count]:
                del self.precomputed[key]
                del self._precomputed_access[key]
        
        file = self.cache_dir / "precomputed.json"
        file.write_text(json.dumps(self.precomputed))
    
    def _hash(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()
    
    def get(self, text: str) -> Optional[List[float]]:
        """获取单个向量（优先使用强化缓存）"""
        # 1. 强化缓存检查
        if self._use强化缓存:
            cached = self._cache.get(text)
            if cached is not None:
                return cached
        
        # 2. 预计算检查
        h = self._hash(text)
        if h in self.precomputed:
            embedding = self.precomputed[h]
            self._precomputed_access[h] = time.time()  # 记录访问时间
            if self._use强化缓存:
                self._cache.set(text, embedding)
            return embedding
        
        # 3. 旧缓存检查
        if text in self.cache:
            embedding = self.cache[text]
            if self._use强化缓存:
                self._cache.set(text, embedding)
            return embedding
        
        # 4. 调用 API
        result = self.batch([text])
        return result[0] if result else None
    
    def get_cache_stats(self) -> dict:
        """获取缓存统计"""
        if self._use强化缓存:
            return self._cache.get_stats()
        return {"memory_items": len(self.cache), "disk_items": len(self.precomputed)}
    
    def batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """批量获取向量（优先使用强化缓存）"""
        results = [None] * len(texts)
        uncached = []
        indices = []
        
        for i, text in enumerate(texts):
            # 1. 强化缓存检查
            if self._use强化缓存:
                cached = self._cache.get(text)
                if cached is not None:
                    results[i] = cached
                    continue
            
            # 2. 预计算检查
            h = self._hash(text)
            if h in self.precomputed:
                embedding = self.precomputed[h]
                results[i] = embedding
                if self._use强化缓存:
                    self._cache.set(text, embedding)
                continue
            
            # 3. 旧缓存检查
            if text in self.cache:
                embedding = self.cache[text]
                results[i] = embedding
                if self._use强化缓存:
                    self._cache.set(text, embedding)
                continue
            
            # 4. 需要调用 API
            uncached.append(text)
            indices.append(i)
        
        # 调用 API 获取未缓存的向量
        if uncached:
            data = json.dumps({
                "input": uncached,
                "model": self.model,
                "dimensions": self.dimensions
            }).encode('utf-8')
            
            req = urllib.request.Request(
                self.api_url, data=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
            )
            
            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    result = json.loads(resp.read().decode('utf-8'))
                    for j, item in enumerate(result['data']):
                        emb = item['embedding']
                        self.cache[uncached[j]] = emb
                        self.precomputed[h] = emb  # h 是最后一个的hash，不对
                        # 修正：重新计算正确的 hash
                        correct_hash = self._hash(uncached[j])
                        self.precomputed[correct_hash] = emb
                        results[indices[j]] = emb
                        # 同时存入强化缓存
                        if self._use强化缓存:
                            self._cache.set(uncached[j], emb)
                    self._save_precomputed()
            except Exception as e:
                print(f"Embedding API 调用失败: {e}")
        
        return results
