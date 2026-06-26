#!/usr/bin/env python3
"""
Cache - Simple TTL-based cache for API responses
"""

import json
import os
import time
from typing import Any, Dict, Optional


class Cache:
    DEFAULT_TTL = {
        "wikibooks": 24 * 3600,  # 24 hours
        "mealdb": 6 * 3600,      # 6 hours
        "nutrition": 24 * 3600,   # 24 hours
    }
    
    def __init__(self, cache_dir: str = None, ttl_config: Dict[str, int] = None):
        if cache_dir is None:
            # Default to skill's state directory
            skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cache_dir = os.path.join(skill_dir, "state")
        
        os.makedirs(cache_dir, exist_ok=True)
        
        self.cache_file = os.path.join(cache_dir, "cache.json")
        self.ttl_config = ttl_config or self.DEFAULT_TTL
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load cache from disk"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def _get_ttl(self, source: str) -> int:
        """Get TTL for a source"""
        return self.ttl_config.get(source, 3600)
    
    def get(self, key: str, source: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        timestamp = entry.get("timestamp", 0)
        ttl = self._get_ttl(source)
        
        if time.time() - timestamp > ttl:
            # Expired
            del self.cache[key]
            self._save_cache()
            return None
        
        return entry.get("value")
    
    def set(self, key: str, value: Any, source: str = "default"):
        """Set value in cache"""
        self.cache[key] = {
            "value": value,
            "timestamp": time.time(),
            "source": source
        }
        self._save_cache()
    
    def invalidate(self, key: str):
        """Remove key from cache"""
        if key in self.cache:
            del self.cache[key]
            self._save_cache()
    
    def clear(self, source: str = None):
        """Clear cache, optionally by source"""
        if source:
            to_remove = []
            for key, entry in self.cache.items():
                if entry.get("source") == source:
                    to_remove.append(key)
            for key in to_remove:
                del self.cache[key]
        else:
            self.cache = {}
        
        self._save_cache()
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = len(self.cache)
        by_source = {}
        
        now = time.time()
        expired = 0
        active = 0
        
        for key, entry in self.cache.items():
            source = entry.get("source", "unknown")
            by_source[source] = by_source.get(source, 0) + 1
            
            ttl = self._get_ttl(source)
            if now - entry.get("timestamp", 0) > ttl:
                expired += 1
            else:
                active += 1
        
        return {
            "total": total,
            "active": active,
            "expired": expired,
            "by_source": by_source
        }


# Test if run directly
if __name__ == "__main__":
    cache = Cache()
    
    print("🧪 Testando cache...")
    
    # Test set/get
    cache.set("test_key", {"data": "test_value"}, "mealdb")
    value = cache.get("test_key", "mealdb")
    print(f"  Set/Get: {value}")
    
    # Test stats
    stats = cache.get_stats()
    print(f"  Stats: {stats}")
    
    # Test expired (using short TTL)
    cache.set("expire_test", "will_expire", "test")
    import time
    cache.ttl_config["test"] = 0  # Immediate expiry
    expired_value = cache.get("expire_test", "test")
    print(f"  Expired value: {expired_value}")
