"""
infra.metrics - 统一监控指标模块

合并自三个原始模块：
- metrics.py (MetricsCollector)
- prometheus_metrics.py (counter_inc, gauge_set, histogram_observe, ...)
- monitoring.py (MonitoringSystem, get_monitoring_system)

提供：
1. MetricsCollector — 业务指标收集（写入/检索 QPS、延迟、缓存命中率等）
2. PrometheusCollector — Prometheus 周期性采集器
3. 底层 Prometheus 原语（counter_inc / gauge_set / histogram_observe / get_metrics_text）
4. MonitoringSystem — 系统级监控（CPU/内存/磁盘、健康检查、异常检测、告警）
5. get_monitoring_system — 全局监控系统单例

用法:
    from agent_memory.infra.metrics import MetricsCollector, counter_inc, MonitoringSystem

    # 业务指标
    mc = MetricsCollector(store, pipeline)
    mc.record_write(latency_ms=12)
    print(mc.export_prometheus())

    # Prometheus 原语
    counter_inc("requests_total")
    gauge_set("active_connections", 42)
    histogram_observe("request_duration_seconds", 0.15)

    # 系统监控
    monitor = MonitoringSystem()
    status = monitor.get_system_status()
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Section 1: 底层 Prometheus 原语（源自 prometheus_metrics.py）
# ---------------------------------------------------------------------------

_COUNTERS: dict[str, int] = {}
_GAUGES: dict[str, float] = {}
_HISTOGRAMS: dict[str, list[float]] = {}
_BUCKETS = (0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0, 60.0)

_lock = threading.Lock()

METRICS_PREFIX = os.environ.get("AGENT_MEMORY_METRICS_PREFIX", "agent_memory")


def counter_inc(name: str, value: int = 1):
    with _lock:
        _COUNTERS[name] = _COUNTERS.get(name, 0) + value


def gauge_set(name: str, value: float):
    with _lock:
        _GAUGES[name] = value


def histogram_observe(name: str, value: float):
    with _lock:
        if name not in _HISTOGRAMS:
            _HISTOGRAMS[name] = []
        _HISTOGRAMS[name].append(value)
        if len(_HISTOGRAMS[name]) > 10000:
            _HISTOGRAMS[name] = _HISTOGRAMS[name][-5000:]


def get_metrics_text() -> str:
    with _lock:
        lines = []

        for name, value in sorted(_COUNTERS.items()):
            lines.append(f"# HELP {METRICS_PREFIX}_{name} Counter metric")
            lines.append(f"# TYPE {METRICS_PREFIX}_{name} counter")
            lines.append(f"{METRICS_PREFIX}_{name} {value}")

        for name, value in sorted(_GAUGES.items()):
            lines.append(f"# HELP {METRICS_PREFIX}_{name} Gauge metric")
            lines.append(f"# TYPE {METRICS_PREFIX}_{name} gauge")
            lines.append(f"{METRICS_PREFIX}_{name} {value}")

        for name, values in sorted(_HISTOGRAMS.items()):
            lines.append(f"# HELP {METRICS_PREFIX}_{name} Histogram metric")
            lines.append(f"# TYPE {METRICS_PREFIX}_{name} histogram")
            for b in _BUCKETS:
                count = sum(1 for v in values if v <= b)
                lines.append(
                    f'{METRICS_PREFIX}_{name}_bucket{{le="{b}"}} {count}'
                )
            lines.append(f'{METRICS_PREFIX}_{name}_bucket{{le="+Inf"}} {len(values)}')
            if values:
                lines.append(f"{METRICS_PREFIX}_{name}_sum {sum(values)}")
                lines.append(f"{METRICS_PREFIX}_{name}_count {len(values)}")

        lines.append(f"# HELP {METRICS_PREFIX}_uptime_seconds Process uptime")
        lines.append(f"# TYPE {METRICS_PREFIX}_uptime_seconds gauge")

        lines.append("")

    return "\n".join(lines)


def collect_memory_stats(store, embedding_store=None):
    try:
        stats = store.get_storage_stats()
        gauge_set("memory_hot_count", stats.get("hot_count", 0))
        gauge_set("memory_cold_count", stats.get("cold_count", 0))
        gauge_set("memory_db_size_mb", stats.get("hot_size_mb", 0.0))
        if embedding_store:
            vector_count = embedding_store.count()
            gauge_set("memory_vector_count", vector_count)
    except Exception as e:
        logger.warning("prometheus_metrics: %s", e)


# ---------------------------------------------------------------------------
# Section 2: PrometheusCollector（源自 prometheus_metrics.py 的 MetricsCollector）
# ---------------------------------------------------------------------------

class PrometheusCollector:
    """Prometheus 周期性采集器 — 定期将存储层指标写入 Prometheus 原语"""

    def __init__(self, store=None, encoder=None, recall_engine=None, embedding_store=None):
        self.store = store
        self.encoder = encoder
        self.recall_engine = recall_engine
        self.embedding_store = embedding_store
        self._last_collect = 0
        self._collect_interval = 15

    def collect(self):
        now = time.time()
        if now - self._last_collect < self._collect_interval:
            return
        self._last_collect = now

        if self.store:
            collect_memory_stats(self.store, self.embedding_store)

        gauge_set("uptime_seconds", time.time() - _START_TIME)


_START_TIME = time.time()


# ---------------------------------------------------------------------------
# Section 3: MetricsCollector（源自 metrics.py）
# ---------------------------------------------------------------------------

class MetricsCollector:
    """业务指标收集器 — 线程安全，零依赖"""

    def __init__(self, store=None, pipeline=None, embedding_store=None):
        self.store = store
        self.pipeline = pipeline
        self.embedding_store = embedding_store

        self._lock = threading.Lock()
        self._start_time = time.time()

        self._counters = defaultdict(int)

        self._latency_buckets = {
            "write": [],
            "recall": [],
            "embed": [],
        }

        self._write_timestamps: list[float] = []
        self._recall_timestamps: list[float] = []
        self._window_sec = 60

    def record_write(self, latency_ms: float = 0, success: bool = True):
        with self._lock:
            self._counters["writes_total"] += 1
            if success:
                self._counters["writes_success"] += 1
            else:
                self._counters["writes_failed"] += 1
            if latency_ms > 0:
                self._latency_buckets["write"].append(latency_ms)
                if len(self._latency_buckets["write"]) > 1000:
                    self._latency_buckets["write"] = self._latency_buckets["write"][-500:]
            self._write_timestamps.append(time.time())

    def record_recall(self, latency_ms: float = 0, result_count: int = 0, cached: bool = False):
        with self._lock:
            self._counters["recalls_total"] += 1
            self._counters["recall_results_total"] += result_count
            if cached:
                self._counters["recall_cache_hits"] += 1
            if latency_ms > 0:
                self._latency_buckets["recall"].append(latency_ms)
                if len(self._latency_buckets["recall"]) > 1000:
                    self._latency_buckets["recall"] = self._latency_buckets["recall"][-500:]
            self._recall_timestamps.append(time.time())

    def record_embed(self, latency_ms: float = 0):
        with self._lock:
            self._counters["embeds_total"] += 1
            if latency_ms > 0:
                self._latency_buckets["embed"].append(latency_ms)
                if len(self._latency_buckets["embed"]) > 500:
                    self._latency_buckets["embed"] = self._latency_buckets["embed"][-250:]

    def record_throttle(self):
        with self._lock:
            self._counters["throttled_total"] += 1

    def get_summary(self) -> dict:
        with self._lock:
            now = time.time()
            cutoff = now - self._window_sec
            self._write_timestamps = [t for t in self._write_timestamps if t >= cutoff]
            self._recall_timestamps = [t for t in self._recall_timestamps if t >= cutoff]

            write_qps = len(self._write_timestamps) / self._window_sec
            recall_qps = len(self._recall_timestamps) / self._window_sec

            uptime_sec = now - self._start_time

            def percentile(arr, p):
                if not arr:
                    return 0
                s = sorted(arr)
                idx = int(len(s) * p / 100)
                return round(s[min(idx, len(s) - 1)], 1)

            summary = {
                "uptime_seconds": round(uptime_sec),
                "write_qps": round(write_qps, 2),
                "recall_qps": round(recall_qps, 2),
                "counters": dict(self._counters),
                "latency": {},
            }

            for name, arr in self._latency_buckets.items():
                if arr:
                    summary["latency"][name] = {
                        "p50": percentile(arr, 50),
                        "p95": percentile(arr, 95),
                        "p99": percentile(arr, 99),
                        "max": round(max(arr), 1),
                        "count": len(arr),
                    }

            if self.store:
                try:
                    mem_count = self.store.conn.execute("SELECT COUNT(*) as c FROM memories").fetchone()["c"]
                    link_count = self.store.conn.execute("SELECT COUNT(*) as c FROM memory_links").fetchone()["c"]
                    summary["storage"] = {
                        "memories": mem_count,
                        "links": link_count,
                    }
                except Exception as e:
                    logger.warning("metrics: %s", e)

            if self.embedding_store:
                try:
                    summary["vectors"] = self.embedding_store.count()
                except Exception as e:
                    logger.warning("metrics: %s", e)

            if self.pipeline:
                queue_stats = self.pipeline.get_queue_stats()
                if queue_stats:
                    summary["write_queue"] = queue_stats

            return summary

    def export_prometheus(self) -> str:
        summary = self.get_summary()
        lines = [
            "# HELP agent_memory_uptime_seconds System uptime in seconds",
            "# TYPE agent_memory_uptime_seconds gauge",
            f"agent_memory_uptime_seconds {summary['uptime_seconds']}",
            "",
            "# HELP agent_memory_write_qps Write operations per second",
            "# TYPE agent_memory_write_qps gauge",
            f"agent_memory_write_qps {summary['write_qps']}",
            "",
            "# HELP agent_memory_recall_qps Recall operations per second",
            "# TYPE agent_memory_recall_qps gauge",
            f"agent_memory_recall_qps {summary['recall_qps']}",
            "",
        ]

        for name, value in summary.get("counters", {}).items():
            lines.append(f"# HELP agent_memory_{name} {name.replace('_', ' ')}")
            lines.append(f"# TYPE agent_memory_{name} counter")
            lines.append(f"agent_memory_{name} {value}")
            lines.append("")

        for op, stats in summary.get("latency", {}).items():
            lines.append(f"# HELP agent_memory_{op}_latency_ms {op} latency in ms")
            lines.append(f"# TYPE agent_memory_{op}_latency_ms summary")
            lines.append(f'agent_memory_{op}_latency_ms{{quantile="0.5"}} {stats["p50"]}')
            lines.append(f'agent_memory_{op}_latency_ms{{quantile="0.95"}} {stats["p95"]}')
            lines.append(f'agent_memory_{op}_latency_ms{{quantile="0.99"}} {stats["p99"]}')
            lines.append(f'agent_memory_{op}_latency_ms_count {stats["count"]}')
            lines.append("")

        if "storage" in summary:
            lines.append("# HELP agent_memory_storage_memories Total memories in SQLite")
            lines.append("# TYPE agent_memory_storage_memories gauge")
            lines.append(f"agent_memory_storage_memories {summary['storage']['memories']}")
            lines.append("")

        if "vectors" in summary:
            lines.append("# HELP agent_memory_vectors_total Total vectors in store")
            lines.append("# TYPE agent_memory_vectors_total gauge")
            lines.append(f"agent_memory_vectors_total {summary['vectors']}")
            lines.append("")

        return "\n".join(lines)

    def export_json(self) -> str:
        return json.dumps(self.get_summary(), ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Section 4: MonitoringSystem（源自 monitoring.py）
# ---------------------------------------------------------------------------

class MonitoringSystem:
    """系统级监控 — CPU/内存/磁盘、健康检查、异常检测、告警"""

    def __init__(self, data_dir: str = None, check_interval: int = 60):
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), "..", "data")
        self.check_interval = check_interval
        self.metrics_file = os.path.join(self.data_dir, "metrics.json")
        self.alerts_file = os.path.join(self.data_dir, "alerts.json")

        os.makedirs(self.data_dir, exist_ok=True)

        self.metrics_history: List[Dict] = []
        self.max_history_size = 1000
        self.alerts: List[Dict] = []
        self.max_alerts_size = 500

        self.running = False
        self.monitor_thread: Optional[threading.Thread] = None

    def start(self):
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            logger.info("监控系统已启动")

    def stop(self):
        if self.running:
            self.running = False
            if self.monitor_thread:
                self.monitor_thread.join()
            logger.info("监控系统已停止")

    def _monitor_loop(self):
        while self.running:
            try:
                system_status = self.get_system_status()
                health_status = self.check_health()
                metrics = self.get_metrics()

                alerts = self.detect_anomalies(metrics)
                if alerts:
                    self.alerts.extend(alerts)
                    if len(self.alerts) > self.max_alerts_size:
                        self.alerts = self.alerts[-self.max_alerts_size:]
                    self._save_alerts()

                self.metrics_history.append(metrics)
                if len(self.metrics_history) > self.max_history_size:
                    self.metrics_history = self.metrics_history[-self.max_history_size:]
                self._save_metrics()

                time.sleep(self.check_interval)
            except Exception as e:
                logger.error("监控循环错误: %s", e)
                time.sleep(self.check_interval)

    def get_system_status(self) -> Dict:
        try:
            import psutil

            cpu_percent = psutil.cpu_percent(interval=1)

            memory = psutil.virtual_memory()
            memory_used_percent = memory.percent
            memory_used_gb = memory.used / (1024 * 1024 * 1024)
            memory_total_gb = memory.total / (1024 * 1024 * 1024)

            disk = psutil.disk_usage('/')
            disk_used_percent = disk.percent
            disk_used_gb = disk.used / (1024 * 1024 * 1024)
            disk_total_gb = disk.total / (1024 * 1024 * 1024)

            network = psutil.net_io_counters()

            return {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "percent": cpu_percent
                },
                "memory": {
                    "used_percent": memory_used_percent,
                    "used_gb": round(memory_used_gb, 2),
                    "total_gb": round(memory_total_gb, 2)
                },
                "disk": {
                    "used_percent": disk_used_percent,
                    "used_gb": round(disk_used_gb, 2),
                    "total_gb": round(disk_total_gb, 2)
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv
                }
            }
        except Exception as e:
            logger.error("获取系统状态失败: %s", e)
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

    def check_health(self) -> Dict:
        try:
            db_health = self._check_database_health()
            network_health = self._check_network_health()
            service_health = self._check_service_health()

            overall_health = "healthy"
            if not db_health["healthy"] or not network_health["healthy"] or not service_health["healthy"]:
                overall_health = "unhealthy"

            return {
                "timestamp": datetime.now().isoformat(),
                "overall": overall_health,
                "database": db_health,
                "network": network_health,
                "service": service_health
            }
        except Exception as e:
            logger.error("检查健康状态失败: %s", e)
            return {
                "timestamp": datetime.now().isoformat(),
                "overall": "unhealthy",
                "error": str(e)
            }

    def _check_database_health(self) -> Dict:
        try:
            db_path = os.path.join(self.data_dir, "memory.db")
            db_exists = os.path.exists(db_path)
            db_readable = os.access(db_path, os.R_OK) if db_exists else False
            db_writable = os.access(db_path, os.W_OK) if db_exists else False

            return {
                "healthy": db_exists and db_readable and db_writable,
                "exists": db_exists,
                "readable": db_readable,
                "writable": db_writable
            }
        except Exception as e:
            return {
                "healthy": False,
                "error": str(e)
            }

    def _check_network_health(self) -> Dict:
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('8.8.8.8', 53))
            sock.close()
            network_available = result == 0

            return {
                "healthy": network_available,
                "available": network_available
            }
        except Exception as e:
            return {
                "healthy": False,
                "error": str(e)
            }

    def _check_service_health(self) -> Dict:
        try:
            return {
                "healthy": True
            }
        except Exception as e:
            return {
                "healthy": False,
                "error": str(e)
            }

    def get_metrics(self) -> Dict:
        try:
            import psutil

            system_status = self.get_system_status()
            health_status = self.check_health()

            request_time = 0.1

            process = psutil.Process(os.getpid())
            process_memory = process.memory_info().rss / (1024 * 1024)

            return {
                "timestamp": datetime.now().isoformat(),
                "system": system_status,
                "health": health_status,
                "process": {
                    "memory_mb": round(process_memory, 2),
                    "cpu_percent": process.cpu_percent(interval=0.1)
                },
                "performance": {
                    "request_time": request_time
                }
            }
        except Exception as e:
            logger.error("获取性能指标失败: %s", e)
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

    def detect_anomalies(self, metrics: Dict) -> List[Dict]:
        alerts = []

        try:
            cpu_percent = metrics.get("system", {}).get("cpu", {}).get("percent", 0)
            if cpu_percent > 80:
                alerts.append({
                    "timestamp": datetime.now().isoformat(),
                    "level": "warning",
                    "message": f"CPU使用率过高: {cpu_percent}%",
                    "metric": "cpu.percent",
                    "value": cpu_percent,
                    "threshold": 80
                })

            memory_percent = metrics.get("system", {}).get("memory", {}).get("used_percent", 0)
            if memory_percent > 85:
                alerts.append({
                    "timestamp": datetime.now().isoformat(),
                    "level": "warning",
                    "message": f"内存使用率过高: {memory_percent}%",
                    "metric": "memory.used_percent",
                    "value": memory_percent,
                    "threshold": 85
                })

            disk_percent = metrics.get("system", {}).get("disk", {}).get("used_percent", 0)
            if disk_percent > 90:
                alerts.append({
                    "timestamp": datetime.now().isoformat(),
                    "level": "critical",
                    "message": f"磁盘使用率过高: {disk_percent}%",
                    "metric": "disk.used_percent",
                    "value": disk_percent,
                    "threshold": 90
                })

            overall_health = metrics.get("health", {}).get("overall", "healthy")
            if overall_health != "healthy":
                alerts.append({
                    "timestamp": datetime.now().isoformat(),
                    "level": "critical",
                    "message": f"服务健康状态异常: {overall_health}",
                    "metric": "health.overall",
                    "value": overall_health
                })

        except Exception as e:
            logger.error("检测异常失败: %s", e)

        return alerts

    def get_alerts(self, limit: int = 50) -> List[Dict]:
        return self.alerts[-limit:]

    def get_metrics_history(self, limit: int = 100) -> List[Dict]:
        return self.metrics_history[-limit:]

    def get_summary(self) -> Dict:
        try:
            system_status = self.get_system_status()
            health_status = self.check_health()
            metrics = self.get_metrics()
            recent_alerts = self.get_alerts(10)

            alert_counts = {
                "total": len(self.alerts),
                "recent": len(recent_alerts),
                "by_level": {}
            }
            for alert in recent_alerts:
                level = alert.get("level", "info")
                alert_counts["by_level"][level] = alert_counts["by_level"].get(level, 0) + 1

            return {
                "timestamp": datetime.now().isoformat(),
                "system_status": system_status,
                "health_status": health_status,
                "recent_metrics": metrics,
                "alert_summary": alert_counts,
                "recent_alerts": recent_alerts
            }
        except Exception as e:
            logger.error("获取监控摘要失败: %s", e)
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

    def _save_metrics(self):
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "metrics": self.metrics_history
            }
            with open(self.metrics_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error("保存性能指标失败: %s", e)

    def _load_metrics(self):
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.metrics_history = data.get("metrics", [])
        except Exception as e:
            logger.error("加载性能指标失败: %s", e)

    def _save_alerts(self):
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "alerts": self.alerts
            }
            with open(self.alerts_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error("保存警报失败: %s", e)

    def _load_alerts(self):
        try:
            if os.path.exists(self.alerts_file):
                with open(self.alerts_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.alerts = data.get("alerts", [])
        except Exception as e:
            logger.error("加载警报失败: %s", e)

    def clear_alerts(self):
        self.alerts = []
        self._save_alerts()
        logger.info("警报已清空")

    def clear_metrics(self):
        self.metrics_history = []
        self._save_metrics()
        logger.info("性能指标历史已清空")


# ---------------------------------------------------------------------------
# Section 5: 全局单例
# ---------------------------------------------------------------------------

_monitoring_system: Optional[MonitoringSystem] = None


def get_monitoring_system() -> MonitoringSystem:
    global _monitoring_system
    if _monitoring_system is None:
        _monitoring_system = MonitoringSystem()
    return _monitoring_system


# ---------------------------------------------------------------------------
# __all__ — 显式导出清单
# ---------------------------------------------------------------------------

__all__ = [
    "MetricsCollector",
    "PrometheusCollector",
    "counter_inc",
    "gauge_set",
    "histogram_observe",
    "get_metrics_text",
    "collect_memory_stats",
    "METRICS_PREFIX",
    "MonitoringSystem",
    "get_monitoring_system",
]
