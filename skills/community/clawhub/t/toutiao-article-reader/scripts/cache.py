"""
缓存模块
避免重复读取同一篇文章
"""

import json
import os
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict


class ArticleCache:
    """文章缓存"""
    
    def __init__(self, cache_dir: str = None, ttl_hours: int = 24):
        """
        初始化缓存
        
        Args:
            cache_dir: 缓存目录
            ttl_hours: 缓存有效期（小时）
        """
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / '.cache'
        
        self.cache_dir = Path(cache_dir)
        self.ttl_hours = ttl_hours
        self.cache_file = self.cache_dir / 'cache.json'
        
        # 创建缓存目录
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载缓存
        self.cache: Dict[str, Dict] = {}
        self._load_cache()
    
    def _generate_key(self, url: str) -> str:
        """生成缓存键"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _load_cache(self):
        """加载缓存文件"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            except:
                self.cache = {}
    
    def _save_cache(self):
        """保存缓存文件"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存缓存失败：{e}", file=__import__('sys').stderr)
    
    def get(self, url: str) -> Optional[Dict]:
        """
        从缓存获取文章
        
        Args:
            url: 文章 URL
        
        Returns:
            缓存的文章数据，如果不存在或已过期则返回 None
        """
        key = self._generate_key(url)
        
        if key not in self.cache:
            return None
        
        cached = self.cache[key]
        cached_time = datetime.fromisoformat(cached['cached_at'])
        
        # 检查是否过期
        if datetime.now() - cached_time > timedelta(hours=self.ttl_hours):
            # 过期，删除
            del self.cache[key]
            self._save_cache()
            return None
        
        return cached['data']
    
    def set(self, url: str, data: Dict):
        """
        缓存文章数据
        
        Args:
            url: 文章 URL
            data: 文章数据
        """
        key = self._generate_key(url)
        
        self.cache[key] = {
            'cached_at': datetime.now().isoformat(),
            'url': url,
            'data': data
        }
        
        self._save_cache()
    
    def clear(self):
        """清空缓存"""
        self.cache = {}
        if self.cache_file.exists():
            self.cache_file.unlink()
    
    def cleanup(self):
        """清理过期缓存"""
        expired_keys = []
        
        for key, cached in self.cache.items():
            cached_time = datetime.fromisoformat(cached['cached_at'])
            if datetime.now() - cached_time > timedelta(hours=self.ttl_hours):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self._save_cache()
        
        return len(expired_keys)
    
    def stats(self) -> Dict:
        """获取缓存统计信息"""
        self.cleanup()
        
        return {
            'total_items': len(self.cache),
            'cache_file_size': self.cache_file.stat().st_size if self.cache_file.exists() else 0,
            'ttl_hours': self.ttl_hours
        }


def main():
    """测试缓存"""
    cache = ArticleCache(ttl_hours=1)
    
    # 测试设置缓存
    test_data = {
        'title': '测试文章',
        'content': '测试内容'
    }
    cache.set('https://example.com/article/1', test_data)
    
    # 测试获取缓存
    cached = cache.get('https://example.com/article/1')
    print(f"从缓存获取：{cached}")
    
    # 测试统计
    stats = cache.stats()
    print(f"缓存统计：{stats}")


if __name__ == '__main__':
    main()
