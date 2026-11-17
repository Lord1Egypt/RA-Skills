#!/usr/bin/env python3
"""
v20.44: Prometheus 指标收集 (纯 Python, 无依赖)
"""
import time
import threading
from collections import deque

class Metrics:
    def __init__(self):
        self._lock = threading.Lock()
        self.start_time = time.time()
        # 计数器
        self.requests_total = 0
        self.requests_errors = 0
        self.search_total = 0
        self.search_cached = 0
        self.answer_total = 0
        self.answer_cached = 0
        self.answer_errors = 0
        # 时延 (滑动窗口最近 100 次)
        self.search_latencies = deque(maxlen=100)
        self.answer_latencies = deque(maxlen=100)
        self.llm_latencies = deque(maxlen=100)
        # 各端点
        self.endpoints = {
            '/v1/search': 0,
            '/v1/search/stream': 0,
            '/v1/search/refresh': 0,
            '/v1/answer': 0,
            '/v1/scholar': 0,
            '/v1/code': 0,
            '/v1/health': 0,
            '/v1/engines': 0,
            '/v1/modes': 0,
            '/v1/academic_mode': 0,
        }
        self.error_endpoints = {
            '/v1/search': 0,
            '/v1/search/stream': 0,
            '/v1/search/refresh': 0,
            '/v1/answer': 0,
            '/v1/scholar': 0,
            '/v1/code': 0,
        }
        self._pid = None
        try:
            import os
            self._pid = os.getpid()
        except Exception:
            pass

    def incr_requests(self, endpoint, error=False):
        with self._lock:
            self.requests_total += 1
            if endpoint in self.endpoints:
                self.endpoints[endpoint] += 1
            if error and endpoint in self.error_endpoints:
                self.error_endpoints[endpoint] += 1

    def incr_search(self, cached=False, elapsed_ms=0):
        with self._lock:
            self.search_total += 1
            if cached:
                self.search_cached += 1
            if elapsed_ms:
                self.search_latencies.append(elapsed_ms)

    def incr_answer(self, cached=False, error=False, elapsed_ms=0, llm_ms=0):
        with self._lock:
            self.answer_total += 1
            if cached:
                self.answer_cached += 1
            if error:
                self.answer_errors += 1
            if elapsed_ms:
                self.answer_latencies.append(elapsed_ms)
            if llm_ms:
                self.llm_latencies.append(llm_ms)

    def _percentile(self, data, p):
        if not data:
            return 0
        sorted_data = sorted(data)
        idx = int(len(sorted_data) * p / 100)
        return sorted_data[min(idx, len(sorted_data) - 1)]

    def to_prometheus(self):
        with self._lock:
            uptime = time.time() - self.start_time
            lines = []
            lines.append('# HELP star_search_uptime_seconds 服务运行时长 (秒)')
            lines.append('# TYPE star_search_uptime_seconds gauge')
            lines.append(f'star_search_uptime_seconds {uptime:.2f}')
            lines.append('')
            lines.append('# HELP star_search_pid 进程 ID')
            lines.append('# TYPE star_search_pid gauge')
            if self._pid:
                lines.append(f'star_search_pid {self._pid}')
            lines.append('')
            lines.append('# HELP star_search_requests_total 总请求数')
            lines.append('# TYPE star_search_requests_total counter')
            lines.append(f'star_search_requests_total {self.requests_total}')
            lines.append('')
            lines.append('# HELP star_search_requests_errors_total 总错误数')
            lines.append('# TYPE star_search_requests_errors_total counter')
            lines.append(f'star_search_requests_errors_total {self.requests_errors}')
            lines.append('')
            lines.append('# HELP star_search_endpoint_requests_total 各端点请求数')
            lines.append('# TYPE star_search_endpoint_requests_total counter')
            for ep, count in self.endpoints.items():
                lines.append(f'star_search_endpoint_requests_total{{endpoint="{ep}"}} {count}')
            lines.append('')
            lines.append('# HELP star_search_endpoint_errors_total 各端点错误数')
            lines.append('# TYPE star_search_endpoint_errors_total counter')
            for ep, count in self.error_endpoints.items():
                if count > 0:
                    lines.append(f'star_search_endpoint_errors_total{{endpoint="{ep}"}} {count}')
            lines.append('')
            lines.append('# HELP star_search_search_total 搜索调用数')
            lines.append('# TYPE star_search_search_total counter')
            lines.append(f'star_search_search_total {self.search_total}')
            lines.append('')
            lines.append('# HELP star_search_search_cached_total 搜索缓存命中数')
            lines.append('# TYPE star_search_search_cached_total counter')
            lines.append(f'star_search_search_cached_total {self.search_cached}')
            cache_hit_rate = (self.search_cached / self.search_total * 100) if self.search_total else 0
            lines.append('# HELP star_search_cache_hit_rate 缓存命中率 (百分比)')
            lines.append('# TYPE star_search_cache_hit_rate gauge')
            lines.append(f'star_search_cache_hit_rate {cache_hit_rate:.2f}')
            lines.append('')
            lines.append('# HELP star_search_answer_total 答案生成数')
            lines.append('# TYPE star_search_answer_total counter')
            lines.append(f'star_search_answer_total {self.answer_total}')
            lines.append('')
            lines.append('# HELP star_search_answer_cached_total 答案缓存命中')
            lines.append('# TYPE star_search_answer_cached_total counter')
            lines.append(f'star_search_answer_cached_total {self.answer_cached}')
            lines.append('')
            lines.append('# HELP star_search_answer_errors_total 答案失败数')
            lines.append('# TYPE star_search_answer_errors_total counter')
            lines.append(f'star_search_answer_errors_total {self.answer_errors}')
            lines.append('')
            for name, data in [('search', self.search_latencies), ('answer', self.answer_latencies), ('llm', self.llm_latencies)]:
                if not data:
                    continue
                lines.append(f'# HELP star_search_{name}_latency_ms {name} 时延 (毫秒)')
                lines.append(f'# TYPE star_search_{name}_latency_ms summary')
                lines.append(f'star_search_{name}_latency_ms{{quantile="0.5"}} {self._percentile(data, 50)}')
                lines.append(f'star_search_{name}_latency_ms{{quantile="0.95"}} {self._percentile(data, 95)}')
                lines.append(f'star_search_{name}_latency_ms{{quantile="0.99"}} {self._percentile(data, 99)}')
                lines.append(f'star_search_{name}_latency_ms_sum {sum(data)}')
                lines.append(f'star_search_{name}_latency_ms_count {len(data)}')
                lines.append('')
            return '\n'.join(lines)

metrics = Metrics()
