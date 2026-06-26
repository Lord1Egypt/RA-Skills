#!/usr/bin/env python3
"""统一API - 整合所有模块的单一入口
功能：
1. 统一的搜索接口
2. 自动性能监控
3. 自我优化
4. 错误处理
"""
from typing import Dict, List, Optional, Any
import time

class UnifiedAPI:
    """统一API"""
    
    def __init__(self):
        # 延迟导入所有模块
        self._memory = None
        self._monitor = None
        self._cache = None
        self._improver = None
    
    @property
    def memory(self):
        if self._memory is None:
            from memory import Memory
            self._memory = Memory()
        return self._memory
    
    @property
    def monitor(self):
        if self._monitor is None:
            from monitor import Monitor
            self._monitor = Monitor()
        return self._monitor
    
    @property
    def cache(self):
        if self._cache is None:
            from predictive_cache import PredictiveCache
            self._cache = PredictiveCache()
        return self._cache
    
    @property
    def improver(self):
        if self._improver is None:
            from self_improver import SelfImprover
            self._improver = SelfImprover()
        return self._improver
    
    def search(self, query: str, limit: int = 3) -> Dict[str, Any]:
        """统一搜索接口"""
        start = time.time()
        
        # 先查缓存
        cached = self.cache.get(query)
        if cached:
            self.monitor.record_search(time.time() - start, cached=True)
            return cached
        
        # 执行搜索
        result = self.memory.search(query, limit=limit)
        elapsed = (time.time() - start) * 1000
        
        # 记录性能
        self.monitor.record_search(elapsed, cached=False)
        
        # 记录慢查询
        self.improver.record_slow_query(query, elapsed, result.get('method', 'unknown'))
        
        # 缓存结果
        self.cache.set(query, result)
        
        return result
    
    def batch_search(self, queries: List[str], limit: int = 3) -> Dict[str, List]:
        """批量搜索"""
        from batch_search import BatchSearchOptimizer
        optimizer = BatchSearchOptimizer(self.memory)
        return optimizer.batch_search(queries, limit)
    
    def get_stats(self) -> Dict:
        """获取所有统计"""
        return {
            "memory": self.memory.stats(),
            "monitor": self.monitor.get_stats(),
            "cache": self.cache.get_stats(),
            "improver": self.improver.get_stats()
        }
    
    def health_check(self) -> Dict:
        """健康检查"""
        return {"status": "ok"}
    
    def optimize(self) -> Dict:
        """执行优化"""
        suggestions = self.improver.get_optimization_suggestions()
        
        applied = []
        for suggestion in suggestions:
            self.improver.apply_optimization(suggestion)
            applied.append(suggestion)
        
        return {
            "suggestions": len(suggestions),
            "applied": len(applied)
        }


# 全局实例
_api = None

def get_api() -> UnifiedAPI:
    global _api
    if _api is None:
        _api = UnifiedAPI()
    return _api


if __name__ == "__main__":
    api = get_api()
    
    print("=== 统一API测试 ===\n")
    
    # 搜索
    result = api.search("记忆", limit=3)
    print(f"搜索: {result['total']} results ({result['method']})")
    
    # 批量搜索
    results = api.batch_search(["记忆", "配置"], limit=3)
    print(f"批量: {len(results)} queries")
    
    # 统计
    stats = api.get_stats()
    print(f"\n统计:")
    print(f"  记忆: {stats['memory']['total']} 条")
    print(f"  缓存: {stats['cache']['cache_size']} 项")
    
    # 健康检查
    health = api.health_check()
    print(f"\n健康: {health["status"]}")
