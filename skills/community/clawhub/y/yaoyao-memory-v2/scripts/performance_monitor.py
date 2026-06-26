#!/usr/bin/env python3
"""
性能监控模块 - 实时监控系统性能指标

功能：
- 记忆操作延迟监控
- 缓存命中率监控
- API 调用统计
- 错误率监控
- 资源使用监控
"""

import sys
import time
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import deque, defaultdict
import json

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size  # 滑动窗口大小
        self.db_path = get_vectors_db()
        self.memory_base = get_memory_base()
        
        # 性能指标缓存
        self._latencies = deque(maxlen=window_size)
        self._cache_hits = deque(maxlen=window_size)
        self._cache_misses = deque(maxlen=window_size)
        self._errors = deque(maxlen=window_size)
        self._operations = defaultdict(int)
        
        # 时间戳
        self._start_time = time.time()
        
        self.conn = None
        self._connect()
    
    def _connect(self):
        """连接数据库"""
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def record_latency(self, operation: str, latency_ms: float):
        """记录操作延迟"""
        self._latencies.append({
            'operation': operation,
            'latency': latency_ms,
            'timestamp': time.time()
        })
        self._operations[operation] += 1
    
    def record_cache_hit(self):
        """记录缓存命中"""
        self._cache_hits.append(time.time())
    
    def record_cache_miss(self):
        """记录缓存未命中"""
        self._cache_misses.append(time.time())
    
    def record_error(self, error_type: str):
        """记录错误"""
        self._errors.append({
            'type': error_type,
            'timestamp': time.time()
        })
    
    def get_latency_stats(self) -> Dict:
        """获取延迟统计"""
        if not self._latencies:
            return {'avg': 0, 'p50': 0, 'p95': 0, 'p99': 0, 'max': 0}
        
        latencies = sorted([l['latency'] for l in self._latencies])
        n = len(latencies)
        
        return {
            'avg': round(sum(latencies) / n, 2),
            'p50': round(latencies[int(n * 0.5)], 2),
            'p95': round(latencies[int(n * 0.95)], 2),
            'p99': round(latencies[int(n * 0.99)], 2),
            'max': round(max(latencies), 2),
            'count': n
        }
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计"""
        hits = len(self._cache_hits)
        misses = len(self._cache_misses)
        total = hits + misses
        
        if total == 0:
            return {'hit_rate': 0, 'hits': 0, 'misses': 0}
        
        return {
            'hit_rate': round(hits / total * 100, 1),
            'hits': hits,
            'misses': misses,
            'total': total
        }
    
    def get_error_stats(self) -> Dict:
        """获取错误统计"""
        if not self._errors:
            return {'count': 0, 'rate': 0}
        
        # 计算错误率（过去1小时）
        now = time.time()
        recent_errors = [e for e in self._errors if now - e['timestamp'] < 3600]
        ops = sum(self._operations.values())
        
        return {
            'count': len(recent_errors),
            'rate': round(len(recent_errors) / max(ops, 1) * 100, 2),
            'by_type': self._get_error_breakdown()
        }
    
    def _get_error_breakdown(self) -> Dict[str, int]:
        """获取错误类型分布"""
        breakdown = defaultdict(int)
        for e in self._errors:
            breakdown[e['type']] += 1
        return dict(breakdown)
    
    def get_operation_stats(self) -> Dict:
        """获取操作统计"""
        total = sum(self._operations.values())
        ops = {k: {'count': v, 'pct': round(v / max(total, 1) * 100, 1)} 
               for k, v in sorted(self._operations.items(), key=lambda x: -x[1])}
        return {'total': total, 'by_operation': ops}
    
    def get_uptime_stats(self) -> Dict:
        """获取运行时间统计"""
        uptime = time.time() - self._start_time
        return {
            'uptime_seconds': round(uptime, 1),
            'uptime_formatted': self._format_uptime(uptime)
        }
    
    def _format_uptime(self, seconds: float) -> str:
        """格式化运行时间"""
        if seconds < 60:
            return f"{seconds:.0f}秒"
        elif seconds < 3600:
            return f"{seconds/60:.1f}分钟"
        else:
            return f"{seconds/3600:.1f}小时"
    
    def get_database_stats(self) -> Dict:
        """获取数据库统计"""
        if not self.conn:
            return {}
        
        try:
            # 记忆数量
            cursor = self.conn.execute("SELECT COUNT(*) as count FROM l1_records")
            memory_count = cursor.fetchone()['count']
            
            # 数据库大小
            db_path = Path(self.db_path)
            if db_path.exists():
                db_size = db_path.stat().st_size
            else:
                db_size = 0
            
            return {
                'memory_count': memory_count,
                'db_size_bytes': db_size,
                'db_size_formatted': self._format_bytes(db_size)
            }
        except:
            return {}
    
    def _format_bytes(self, size: int) -> str:
        """格式化字节大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    
    def get_comprehensive_report(self) -> str:
        """生成综合性能报告"""
        lines = ["# 📊 性能监控报告", ""]
        
        # 运行时间
        uptime = self.get_uptime_stats()
        lines.append(f"## ⏱️ 运行时间：{uptime['uptime_formatted']}")
        lines.append("")
        
        # 延迟统计
        latency = self.get_latency_stats()
        lines.append("## ⚡ 延迟统计")
        lines.append(f"- 平均：{latency['avg']}ms")
        lines.append(f"- P50：{latency['p50']}ms")
        lines.append(f"- P95：{latency['p95']}ms")
        lines.append(f"- P99：{latency['p99']}ms")
        lines.append(f"- 最大：{latency['max']}ms")
        lines.append("")
        
        # 缓存统计
        cache = self.get_cache_stats()
        lines.append("## 💾 缓存统计")
        lines.append(f"- 命中率：{cache['hit_rate']}%")
        lines.append(f"- 命中：{cache['hits']} 次")
        lines.append(f"- 未命中：{cache['misses']} 次")
        lines.append("")
        
        # 错误统计
        errors = self.get_error_stats()
        lines.append("## ⚠️ 错误统计")
        lines.append(f"- 错误数：{errors['count']} (1小时内)")
        lines.append(f"- 错误率：{errors['rate']}%")
        for etype, count in errors.get('by_type', {}).items():
                lines.append(f"  - {etype}：{count}")
        lines.append("")
        
        # 操作统计
        ops = self.get_operation_stats()
        lines.append("## 📈 操作统计")
        lines.append(f"- 总操作数：{ops['total']}")
        for op, stats in list(ops['by_operation'].items())[:5]:
            lines.append(f"- {op}：{stats['count']} 次 ({stats['pct']}%)")
        lines.append("")
        
        # 数据库统计
        db = self.get_database_stats()
        if db:
            lines.append("## 🗄️ 数据库")
            lines.append(f"- 记忆数量：{db['memory_count']} 条")
            lines.append(f"- 数据库大小：{db['db_size_formatted']}")
        
        return "\n".join(lines)
    
    def get_real_time_metrics(self) -> Dict:
        """获取实时指标（用于仪表盘）"""
        return {
            'latency': self.get_latency_stats(),
            'cache': self.get_cache_stats(),
            'errors': self.get_error_stats(),
            'operations': self.get_operation_stats(),
            'uptime': self.get_uptime_stats(),
            'database': self.get_database_stats()
        }
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


class OperationTimer:
    """操作计时器上下文管理器"""
    
    def __init__(self, monitor: PerformanceMonitor, operation: str):
        self.monitor = monitor
        self.operation = operation
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        latency_ms = (time.time() - self.start_time) * 1000
        self.monitor.record_latency(self.operation, latency_ms)
        
        if exc_type is not None:
            self.monitor.record_error(str(exc_type.__name__))
            return False
        return True


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='性能监控')
    parser.add_argument('--report', '-r', action='store_true', help='生成报告')
    parser.add_argument('--latency', '-l', action='store_true', help='延迟统计')
    parser.add_argument('--cache', '-c', action='store_true', help='缓存统计')
    parser.add_argument('--errors', '-e', action='store_true', help='错误统计')
    parser.add_argument('--db', '-d', action='store_true', help='数据库统计')
    args = parser.parse_args()
    
    monitor = PerformanceMonitor()
    
    if args.latency:
        stats = monitor.get_latency_stats()
        print(f"# ⚡ 延迟统计")
        for k, v in stats.items():
            print(f"- {k}: {v}")
    elif args.cache:
        stats = monitor.get_cache_stats()
        print(f"# 💾 缓存统计")
        for k, v in stats.items():
            print(f"- {k}: {v}")
    elif args.errors:
        stats = monitor.get_error_stats()
        print(f"# ⚠️ 错误统计")
        for k, v in stats.items():
            print(f"- {k}: {v}")
    elif args.db:
        stats = monitor.get_database_stats()
        print(f"# 🗄️ 数据库统计")
        for k, v in stats.items():
            print(f"- {k}: {v}")
    else:
        print(monitor.get_comprehensive_report())
    
    monitor.close()


if __name__ == '__main__':
    main()
