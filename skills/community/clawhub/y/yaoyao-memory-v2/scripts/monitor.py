#!/usr/bin/env python3
"""监控系统 - 实时监控关键指标并告警
功能：
1. 性能监控 - 延迟、吞吐量
2. 错误监控 - 异常检测
3. 缓存监控 - 命中率
4. 告警系统 - 自动通知
"""
import time
from datetime import datetime
from typing import Dict, List, Callable

class Monitor:
    """监控系统"""
    
    def __init__(self):
        self.metrics = {
            "search_count": 0,
            "total_search_time": 0,
            "errors": [],
            "cache_hits": 0,
            "cache_misses": 0
        }
        self.alert_handlers = []
        self.thresholds = {
            "search_latency_ms": 100,
            "error_rate": 0.1,
            "memory_percent": 80
        }
    
    def record_search(self, elapsed_ms: float, cached: bool):
        """记录搜索"""
        self.metrics["search_count"] += 1
        self.metrics["total_search_time"] += elapsed_ms
        
        if cached:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1
        
        # 检查延迟告警
        if elapsed_ms > self.thresholds["search_latency_ms"]:
            self._alert("search_latency", {
                "elapsed_ms": elapsed_ms,
                "threshold": self.thresholds["search_latency_ms"]
            })
    
    def record_error(self, error_msg: str):
        """记录错误"""
        self.metrics["errors"].append({
            "timestamp": datetime.now().isoformat(),
            "message": error_msg[:100]
        })
        
        # 检查错误率
        if self.metrics["search_count"] > 10:
            error_rate = len(self.metrics["errors"]) / self.metrics["search_count"]
            if error_rate > self.thresholds["error_rate"]:
                self._alert("error_rate", {
                    "rate": error_rate,
                    "threshold": self.thresholds["error_rate"]
                })
    
    def get_stats(self) -> Dict:
        """获取统计"""
        avg_latency = (self.metrics["total_search_time"] / self.metrics["search_count"]
                   if self.metrics["search_count"] > 0 else 0)
        
        total_cache = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        cache_hit_rate = (self.metrics["cache_hits"] / total_cache if total_cache > 0 else 0)
        
        return {
            "search_count": self.metrics["search_count"],
            "avg_latency_ms": round(avg_latency, 2),
            "cache_hit_rate": f"{cache_hit_rate*100:.1f}%",
            "error_count": len(self.metrics["errors"]),
            "memory_percent": "N/A (psutil not available)"
        }
    
    def add_alert_handler(self, handler: Callable):
        """添加告警处理器"""
        self.alert_handlers.append(handler)
    
    def _alert(self, alert_type: str, data: Dict):
        """触发告警"""
        alert = {
            "type": alert_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                print(f"Alert handler error: {e}")
    
    def reset(self):
        """重置统计"""
        self.metrics = {
            "search_count": 0,
            "total_search_time": 0,
            "errors": [],
            "cache_hits": 0,
            "cache_misses": 0
        }


class AlertHandler:
    """告警处理器"""
    
    @staticmethod
    def log_alert(alert: Dict):
        """记录告警到文件"""
        from pathlib import Path
        log_file = Path.home() / ".openclaw" / "workspace" / "memory" / "alerts.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, "a") as f:
            f.write(f"[{alert['timestamp']}] {alert['type']}: {alert['data']}\n")
    
    @staticmethod
    def print_alert(alert: Dict):
        """打印告警"""
        print(f"ALERT [{alert['type']}] {alert['data']}")


if __name__ == "__main__":
    monitor = Monitor()
    monitor.add_alert_handler(AlertHandler.print_alert)
    
    print("=== 监控系统测试 ===\n")
    
    # 模拟搜索
    for i in range(10):
        monitor.record_search(50 + i * 10, cached=(i % 2 == 0))
    
    # 模拟错误
    monitor.record_error("Test error 1")
    monitor.record_search(150, cached=False)  # 触发延迟告警
    
    # 统计
    stats = monitor.get_stats()
    print(f"\n统计:")
    print(f"  搜索次数: {stats['search_count']}")
    print(f"  平均延迟: {stats['avg_latency_ms']}ms")
    print(f"  缓存命中率: {stats['cache_hit_rate']}")
    print(f"  错误数: {stats['error_count']}")
