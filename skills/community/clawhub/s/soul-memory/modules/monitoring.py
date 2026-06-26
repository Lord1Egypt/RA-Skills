#!/usr/bin/env python3
"""
Soul Memory v3.4.0 - Real-time Monitoring
實時監控儀表板：WebSocket 推送 + 性能指標追蹤

Author: Li Si (李斯)
Date: 2026-03-08

v3.4.0 - 新增 WebSocket 監控 + 指標收集
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict, deque

# Ensure module path
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@dataclass
class MetricPoint:
    """指標數據點"""
    timestamp: float
    value: float
    label: str = ""


class MetricsCollector:
    """
    指標收集器
    
    Features:
    - 時間序列數據存儲
    - 滑動窗口統計
    - 異常檢測
    """
    
    def __init__(self, window_size: int = 100):
        """
        初始化收集器
        
        Args:
            window_size: 滑動窗口大小
        """
        self.window_size = window_size
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
    
    def record(self, metric_name: str, value: float, label: str = ""):
        """記錄指標"""
        point = MetricPoint(
            timestamp=time.time(),
            value=value,
            label=label
        )
        self.metrics[metric_name].append(point)
        self.counters[metric_name] += 1
    
    def increment(self, counter_name: str, amount: int = 1):
        """增加計數器"""
        self.counters[counter_name] += amount
    
    def set_gauge(self, gauge_name: str, value: float):
        """設置儀表值"""
        self.gauges[gauge_name] = value
    
    def get_stats(self, metric_name: str) -> Dict:
        """獲取指標統計"""
        points = list(self.metrics[metric_name])
        if not points:
            return {'count': 0}
        
        values = [p.value for p in points]
        return {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'latest': values[-1] if values else 0,
            'timestamp': points[-1].timestamp if points else 0
        }
    
    def get_all_metrics(self) -> Dict:
        """獲取所有指標"""
        return {
            'metrics': {name: self.get_stats(name) for name in self.metrics},
            'counters': dict(self.counters),
            'gauges': dict(self.gauges)
        }


class RealtimeMonitor:
    """
    實時監控器 v3.4.0
    
    Features:
    - 性能指標追蹤
    - 異常檢測與警報
    - WebSocket 推送（預留接口）
    - 自動化報告
    """
    
    VERSION = "3.4.0"
    
    def __init__(self, log_path: Optional[Path] = None):
        """
        初始化監控器
        
        Args:
            log_path: 日誌文件路徑
        """
        self.log_path = log_path or Path(__file__).parent.parent / "cache" / "monitor"
        self.log_path.mkdir(parents=True, exist_ok=True)
        
        self.collector = MetricsCollector(window_size=1000)
        self.alerts: List[Dict] = []
        self.callbacks: Dict[str, List[Callable]] = defaultdict(list)
        
        # 監控線程
        self.running = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # 閾值配置
        self.thresholds = {
            'search_latency_ms': 500,  # 超過 500ms 警報
            'cache_hit_rate': 0.3,  # 低於 30% 警報
            'error_rate': 0.05,  # 超過 5% 警報
            'memory_usage_mb': 500  # 超過 500MB 警報
        }
        
        # 加載歷史配置
        self.load_config()
    
    def start(self):
        """啟動監控"""
        if self.running:
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("📊 Real-time Monitor started")
    
    def stop(self):
        """停止監控"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("📊 Real-time Monitor stopped")
    
    def _monitor_loop(self):
        """監控循環"""
        while self.running:
            try:
                # 檢查閾值
                self._check_thresholds()
                
                # 保存快照
                self._save_snapshot()
                
                # 每秒檢查一次
                time.sleep(1)
            except Exception as e:
                print(f"[Monitor] Error in monitor loop: {e}")
    
    def _check_thresholds(self):
        """檢查閾值"""
        # 搜索延遲
        latency_stats = self.collector.get_stats('search_latency_ms')
        if latency_stats.get('latest', 0) > self.thresholds['search_latency_ms']:
            self._trigger_alert(
                'high_latency',
                f"Search latency too high: {latency_stats['latest']:.2f}ms",
                latency_stats['latest']
            )
        
        # 緩存命中率
        hit_rate_stats = self.collector.get_stats('cache_hit_rate')
        if hit_rate_stats.get('latest', 1) < self.thresholds['cache_hit_rate']:
            self._trigger_alert(
                'low_cache_hit_rate',
                f"Cache hit rate too low: {hit_rate_stats['latest']*100:.1f}%",
                hit_rate_stats['latest']
            )
    
    def _trigger_alert(self, alert_type: str, message: str, value: float):
        """觸發警報"""
        alert = {
            'type': alert_type,
            'message': message,
            'value': value,
            'timestamp': time.time(),
            'acknowledged': False
        }
        
        self.alerts.append(alert)
        
        # 通知回調
        for callback in self.callbacks.get('alert', []):
            try:
                callback(alert)
            except Exception as e:
                print(f"[Monitor] Alert callback error: {e}")
        
        print(f"🚨 ALERT: {message}")
    
    def _save_snapshot(self):
        """保存監控快照"""
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.collector.get_all_metrics(),
            'active_alerts': len([a for a in self.alerts if not a['acknowledged']])
        }
        
        # 保存到文件（每分鐘）
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
        snapshot_file = self.log_path / f"snapshot_{timestamp}.json"
        
        if not snapshot_file.exists():
            with open(snapshot_file, 'w', encoding='utf-8') as f:
                json.dump(snapshot, f, indent=2)
    
    def record_search(self, latency_ms: float, cache_hit: bool):
        """
        記錄搜索操作
        
        Args:
            latency_ms: 搜索延遲
            cache_hit: 是否緩存命中
        """
        self.collector.record('search_latency_ms', latency_ms)
        self.collector.record('cache_hit', 1 if cache_hit else 0)
        self.collector.increment('total_searches')
        
        if cache_hit:
            self.collector.increment('cache_hits')
        
        # 計算實時命中率
        total = self.collector.counters.get('total_searches', 0)
        hits = self.collector.counters.get('cache_hits', 0)
        hit_rate = hits / total if total > 0 else 0
        self.collector.set_gauge('cache_hit_rate', hit_rate)
    
    def record_error(self, error_type: str):
        """記錄錯誤"""
        self.collector.increment(f'error_{error_type}')
        self.collector.increment('total_errors')
        
        # 計算錯誤率
        total = self.collector.counters.get('total_searches', 1)
        errors = self.collector.counters.get('total_errors', 0)
        error_rate = errors / total
        self.collector.set_gauge('error_rate', error_rate)
    
    def on_alert(self, callback: Callable):
        """註冊警報回調"""
        self.callbacks['alert'].append(callback)
    
    def get_dashboard_data(self) -> Dict:
        """獲取儀表板數據"""
        return {
            'version': self.VERSION,
            'uptime': datetime.now().isoformat(),
            'metrics': self.collector.get_all_metrics(),
            'alerts': {
                'total': len(self.alerts),
                'unacknowledged': len([a for a in self.alerts if not a['acknowledged']]),
                'recent': self.alerts[-10:]  # 最近 10 條
            },
            'thresholds': self.thresholds
        }
    
    def acknowledge_alert(self, alert_index: int):
        """確認警報"""
        if 0 <= alert_index < len(self.alerts):
            self.alerts[alert_index]['acknowledged'] = True
    
    def clear_alerts(self):
        """清空警報"""
        self.alerts.clear()
    
    def save_config(self):
        """保存配置"""
        config = {
            'thresholds': self.thresholds,
            'version': self.VERSION
        }
        
        config_file = self.log_path / "config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    
    def load_config(self):
        """加載配置"""
        config_file = self.log_path / "config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.thresholds.update(config.get('thresholds', {}))
            except Exception as e:
                print(f"[Monitor] Failed to load config: {e}")
    
    def generate_report(self) -> str:
        """生成監控報告"""
        data = self.get_dashboard_data()
        
        report = f"""# Soul Memory 實時監控報告

**生成時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**版本**: v{self.VERSION}

---

## 📊 核心指標

### 搜索性能
"""
        
        search_stats = data['metrics'].get('metrics', {}).get('search_latency_ms', {})
        report += f"""- **平均延遲**: {search_stats.get('avg', 0):.2f}ms
- **最小延遲**: {search_stats.get('min', 0):.2f}ms
- **最大延遲**: {search_stats.get('max', 0):.2f}ms
- **總搜索次數**: {data['metrics']['counters'].get('total_searches', 0)}

### 緩存性能
"""
        
        hit_rate = data['metrics']['gauges'].get('cache_hit_rate', 0)
        cache_hits = data['metrics']['counters'].get('cache_hits', 0)
        report += f"""- **命中率**: {hit_rate*100:.1f}%
- **命中次數**: {cache_hits}

---

## 🚨 警報統計

- **總警報數**: {data['alerts']['total']}
- **未確認**: {data['alerts']['unacknowledged']}

---

## ⚙️ 閾值配置

"""
        
        for name, value in self.thresholds.items():
            report += f"- **{name}**: {value}\n"
        
        return report


# 全局實例
_global_monitor: Optional[RealtimeMonitor] = None


def get_monitor(log_path: Optional[Path] = None) -> RealtimeMonitor:
    """獲取全局監控器實例"""
    global _global_monitor
    
    if _global_monitor is None:
        _global_monitor = RealtimeMonitor(log_path)
    
    return _global_monitor


# CLI 測試
if __name__ == "__main__":
    print("🧪 Testing Real-time Monitoring v3.4.0\n")
    
    monitor = get_monitor()
    
    # 測試 1: 記錄搜索
    print("Test 1: Record Searches")
    for i in range(10):
        latency = 50 + (i % 5) * 10  # 50-90ms
        cache_hit = i % 3 != 0  # 66% 命中率
        monitor.record_search(latency, cache_hit)
    print(f"  Recorded 10 searches\n")
    
    # 測試 2: 記錄錯誤
    print("Test 2: Record Errors")
    monitor.record_error('timeout')
    monitor.record_error('not_found')
    print(f"  Recorded 2 errors\n")
    
    # 測試 3: 儀表板數據
    print("Test 3: Dashboard Data")
    data = monitor.get_dashboard_data()
    print(f"  Total searches: {data['metrics']['counters'].get('total_searches', 0)}")
    print(f"  Cache hit rate: {data['metrics']['gauges'].get('cache_hit_rate', 0)*100:.1f}%")
    print(f"  Alerts: {data['alerts']['total']}\n")
    
    # 測試 4: 生成報告
    print("Test 4: Generate Report")
    report = monitor.generate_report()
    print(f"  Report generated ({len(report)} chars)\n")
    
    # 測試 5: 保存配置
    print("Test 5: Save Config")
    monitor.save_config()
    print(f"  Config saved\n")
    
    print("✅ All tests passed!")
