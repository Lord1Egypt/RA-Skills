#!/usr/bin/env python3
"""
多数据源智能选择模块
自动选择最优数据源，支持失败回退
"""

import time
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DataSource:
    """数据源配置"""
    name: str
    fetch_func: Callable
    priority: int = 0  # 优先级，数字越小越优先
    timeout: int = 30  # 超时时间（秒）
    enabled: bool = True
    last_success: Optional[datetime] = None
    fail_count: int = 0
    max_fail_count: int = 3  # 最大连续失败次数，超过后禁用


class MultiSourceFetcher:
    """多数据源抓取器"""
    
    def __init__(self):
        self.sources: List[DataSource] = []
        self.results_cache: Dict[str, Dict] = {}
    
    def add_source(self, source: DataSource):
        """添加数据源"""
        self.sources.append(source)
        # 按优先级排序
        self.sources.sort(key=lambda x: x.priority)
    
    def fetch(self, steel_type: str, region: str, 
              use_cache: bool = True, cache_hours: int = 2) -> Optional[Dict]:
        """
        智能抓取价格
        
        策略：
        1. 优先使用缓存（在有效期内）
        2. 按优先级尝试各数据源
        3. 某个数据源连续失败3次后暂时禁用
        4. 记录成功时间，优先使用最近成功的源
        
        Returns:
            {
                "price": 价格,
                "source": 数据来源,
                "timestamp": 时间戳,
                "method": "fetch"/"cache"
            }
        """
        cache_key = f"{steel_type}_{region}"
        
        # 1. 检查缓存
        if use_cache and cache_key in self.results_cache:
            cached = self.results_cache[cache_key]
            cached_time = cached.get("timestamp")
            if cached_time:
                elapsed = (datetime.now() - datetime.fromisoformat(cached_time)).total_seconds() / 3600
                if elapsed < cache_hours:
                    return {**cached, "method": "cache"}
        
        # 2. 按优先级尝试数据源
        for source in self.sources:
            if not source.enabled:
                continue
            if source.fail_count >= source.max_fail_count:
                continue
            
            try:
                print(f"尝试数据源: {source.name}")
                result = source.fetch_func(steel_type, region)
                
                if result and result.get("price"):
                    # 成功
                    source.last_success = datetime.now()
                    source.fail_count = 0
                    
                    data = {
                        "price": result["price"],
                        "source": source.name,
                        "timestamp": datetime.now().isoformat(),
                        "method": "fetch",
                        "raw": result
                    }
                    
                    # 更新缓存
                    self.results_cache[cache_key] = data
                    
                    return data
                    
            except Exception as e:
                print(f"  {source.name} 失败: {e}")
                source.fail_count += 1
                if source.fail_count >= source.max_fail_count:
                    print(f"  {source.name} 连续失败{source.max_fail_count}次，暂时禁用")
                continue
        
        # 3. 所有源都失败，返回缓存（即使过期）
        if cache_key in self.results_cache:
            print("使用过期缓存")
            return {**self.results_cache[cache_key], "method": "cache_stale"}
        
        return None
    
    def get_source_status(self) -> List[Dict]:
        """获取各数据源状态"""
        return [
            {
                "name": s.name,
                "enabled": s.enabled,
                "priority": s.priority,
                "fail_count": s.fail_count,
                "last_success": s.last_success.isoformat() if s.last_success else None
            }
            for s in self.sources
        ]
    
    def reset_fail_count(self):
        """重置失败计数（每天调用一次）"""
        for source in self.sources:
            source.fail_count = 0
            source.enabled = True


# 预配置的数据源

def create_default_fetcher() -> MultiSourceFetcher:
    """创建默认的数据源抓取器"""
    from scrape_price import scrape_zhaogang, scrape_mysteel
    
    fetcher = MultiSourceFetcher()
    
    # 找钢网 - 优先级1（最优先）
    fetcher.add_source(DataSource(
        name="找钢网",
        fetch_func=scrape_zhaogang,
        priority=1,
        timeout=30
    ))
    
    # 我的钢铁网 - 优先级2（备用）
    fetcher.add_source(DataSource(
        name="我的钢铁网",
        fetch_func=scrape_mysteel,
        priority=2,
        timeout=45
    ))
    
    return fetcher


# 单例模式
_default_fetcher = None

def get_fetcher() -> MultiSourceFetcher:
    """获取默认抓取器实例"""
    global _default_fetcher
    if _default_fetcher is None:
        _default_fetcher = create_default_fetcher()
    return _default_fetcher


def smart_fetch(steel_type: str, region: str, 
                use_cache: bool = True, cache_hours: int = 2) -> Optional[Dict]:
    """
    智能抓取价格（便捷函数）
    
    自动选择最优数据源
    """
    fetcher = get_fetcher()
    return fetcher.fetch(steel_type, region, use_cache, cache_hours)


def get_data_sources_status() -> str:
    """获取数据源状态报告"""
    fetcher = get_fetcher()
    status = fetcher.get_source_status()
    
    lines = ["📊 数据源状态"]
    lines.append("")
    
    for s in status:
        status_emoji = "✅" if s["enabled"] and s["fail_count"] < 3 else "❌"
        lines.append(f"{status_emoji} {s['name']}")
        lines.append(f"   优先级: {s['priority']}")
        lines.append(f"   失败次数: {s['fail_count']}")
        if s["last_success"]:
            lines.append(f"   最后成功: {s['last_success'][:10]}")
        lines.append("")
    
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    
    # 测试
    print(get_data_sources_status())
    print("\n测试抓取:")
    result = smart_fetch("螺纹钢", "唐山")
    if result:
        print(f"✓ 获取成功: {result['price']} 元/吨 ({result['source']})")
    else:
        print("✗ 所有数据源都失败")
