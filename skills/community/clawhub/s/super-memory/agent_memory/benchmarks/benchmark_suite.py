"""Agent Memory V12 Performance Benchmark Suite.

Measures key performance indicators:
- Write throughput (insert)
- Read throughput (query / get_memory)
- Search latency (FTS5 keyword, structured filters)
- Update / Delete operations
- Concurrency (multi-threaded read/write)
"""
from __future__ import annotations

import gc
import hashlib
import os
import statistics
import tempfile
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Callable

BENCHMARK_RESULTS: list[dict] = []


@dataclass
class BenchmarkResult:
    name: str
    iterations: int
    latencies_ms: list[float] = field(default_factory=list)

    @property
    def mean_ms(self) -> float:
        return statistics.mean(self.latencies_ms) if self.latencies_ms else 0

    @property
    def p50_ms(self) -> float:
        return self._percentile(50)

    @property
    def p95_ms(self) -> float:
        return self._percentile(95)

    @property
    def p99_ms(self) -> float:
        return self._percentile(99)

    @property
    def throughput_ops_sec(self) -> float:
        total_sec = sum(self.latencies_ms) / 1000
        return self.iterations / total_sec if total_sec > 0 else 0

    def _percentile(self, pct: float) -> float:
        if not self.latencies_ms:
            return 0
        sorted_lat = sorted(self.latencies_ms)
        idx = int(len(sorted_lat) * pct / 100)
        return sorted_lat[min(idx, len(sorted_lat) - 1)]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "iterations": self.iterations,
            "mean_ms": round(self.mean_ms, 2),
            "p50_ms": round(self.p50_ms, 2),
            "p95_ms": round(self.p95_ms, 2),
            "p99_ms": round(self.p99_ms, 2),
            "throughput_ops_sec": round(self.throughput_ops_sec, 1),
        }


@contextmanager
def measure(name: str):
    start = time.perf_counter()
    yield
    elapsed_ms = (time.perf_counter() - start) * 1000
    BENCHMARK_RESULTS.append({"name": name, "latency_ms": round(elapsed_ms, 2)})


def run_benchmark(name: str, func: Callable, iterations: int = 100, warmup: int = 5) -> BenchmarkResult:
    for _ in range(warmup):
        func()

    gc.collect()

    result = BenchmarkResult(name=name, iterations=iterations)
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        elapsed_ms = (time.perf_counter() - start) * 1000
        result.latencies_ms.append(elapsed_ms)

    return result


def _make_memory_id() -> str:
    return str(uuid.uuid4())


def _make_content(idx: int) -> str:
    return f"Benchmark test content {idx} at {time.time()}"


def _make_content_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


class MemoryBenchmark:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or tempfile.mktemp(suffix=".db")
        self.store = None

    def setup(self):
        from ..store import MemoryStore
        self.store = MemoryStore(db_path=self.db_path)

    def teardown(self):
        if getattr(self, "store", None) is not None:
            try:
                self.store.close_all()
            except Exception:
                pass
            self.store = None
        try:
            os.unlink(self.db_path)
        except OSError:
            pass

    def bench_insert_single(self, n: int = 1000) -> BenchmarkResult:
        counter = [0]

        def insert_one():
            idx = counter[0]
            counter[0] += 1
            content = _make_content(idx)
            mid = _make_memory_id()
            self.store.insert_memory(
                memory_id=mid,
                time_id=f"T{idx}",
                time_ts=int(time.time()),
                person_id="bench_user",
                nature_id="FACT(1)",
                content=content,
                content_hash=_make_content_hash(content),
                importance="medium",
            )

        return run_benchmark("insert_single", insert_one, iterations=n)

    def bench_query_by_keyword(self, n: int = 500) -> BenchmarkResult:
        for i in range(100):
            content = f"Performance test document number {i} with keywords like machine learning and data science"
            mid = _make_memory_id()
            self.store.insert_memory(
                memory_id=mid,
                time_id=f"TQ{i}",
                time_ts=int(time.time()),
                person_id="bench_user",
                nature_id="FACT(1)",
                content=content,
                content_hash=_make_content_hash(content),
                importance="medium",
            )

        def query_one():
            self.store.query(keyword="machine learning", limit=10)

        return run_benchmark("query_keyword", query_one, iterations=n)

    def bench_query_by_importance(self, n: int = 500) -> BenchmarkResult:
        def query_meta():
            self.store.query(importance="medium", limit=10)

        return run_benchmark("query_importance", query_meta, iterations=n)

    def bench_get_memory(self, n: int = 500) -> BenchmarkResult:
        content = "Get benchmark test"
        mid = _make_memory_id()
        self.store.insert_memory(
            memory_id=mid,
            time_id="TGet",
            time_ts=int(time.time()),
            person_id="bench_user",
            nature_id="FACT(1)",
            content=content,
            content_hash=_make_content_hash(content),
            importance="medium",
        )

        def get_one():
            self.store.get_memory(mid)

        return run_benchmark("get_memory", get_one, iterations=n)

    def bench_update_memory(self, n: int = 500) -> BenchmarkResult:
        content = "Update benchmark test"
        mid = _make_memory_id()
        self.store.insert_memory(
            memory_id=mid,
            time_id="TUpd",
            time_ts=int(time.time()),
            person_id="bench_user",
            nature_id="FACT(1)",
            content=content,
            content_hash=_make_content_hash(content),
            importance="medium",
        )

        counter = [0]

        def update_one():
            counter[0] += 1
            self.store.update_memory(mid, new_content=f"Updated at {counter[0]}")

        return run_benchmark("update_memory", update_one, iterations=n)

    def bench_delete_memory(self, n: int = 100) -> BenchmarkResult:
        ids = []
        for i in range(n):
            content = f"Delete benchmark {i}"
            mid = _make_memory_id()
            self.store.insert_memory(
                memory_id=mid,
                time_id=f"TDel{i}",
                time_ts=int(time.time()),
                person_id="bench_user",
                nature_id="FACT(1)",
                content=content,
                content_hash=_make_content_hash(content),
                importance="low",
            )
            ids.append(mid)

        idx = [0]

        def delete_one():
            if idx[0] < len(ids):
                self.store.delete_memory(ids[idx[0]])
                idx[0] += 1

        return run_benchmark("delete_memory", delete_one, iterations=n)

    def bench_concurrent_reads(self, n_threads: int = 8, n_ops: int = 100) -> BenchmarkResult:
        for i in range(50):
            content = f"Concurrent read test {i}"
            mid = _make_memory_id()
            self.store.insert_memory(
                memory_id=mid,
                time_id=f"TCR{i}",
                time_ts=int(time.time()),
                person_id="bench_user",
                nature_id="FACT(1)",
                content=content,
                content_hash=_make_content_hash(content),
                importance="medium",
            )

        latencies = []
        barrier = threading.Barrier(n_threads)

        def reader():
            barrier.wait()
            for _ in range(n_ops):
                start = time.perf_counter()
                self.store.query(keyword="concurrent", limit=5)
                latencies.append((time.perf_counter() - start) * 1000)

        threads = [threading.Thread(target=reader) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        result = BenchmarkResult(
            name=f"concurrent_reads_{n_threads}t",
            iterations=n_threads * n_ops,
            latencies_ms=latencies,
        )
        return result

    def run_all(self) -> list[BenchmarkResult]:
        self.setup()
        try:
            results = [
                self.bench_insert_single(1000),
                self.bench_query_by_keyword(500),
                self.bench_query_by_importance(500),
                self.bench_get_memory(500),
                self.bench_update_memory(500),
                self.bench_delete_memory(100),
                self.bench_concurrent_reads(8, 100),
            ]
            return results
        finally:
            self.teardown()


def format_results(results: list[BenchmarkResult]) -> str:
    lines = [
        "=" * 80,
        "Agent Memory V12 Performance Benchmark Results",
        "=" * 80,
        f"{'Benchmark':<30} {'Iter':>6} {'Mean':>8} {'P50':>8} {'P95':>8} {'P99':>8} {'Ops/s':>10}",
        "-" * 80,
    ]
    for r in results:
        d = r.to_dict()
        lines.append(
            f"{d['name']:<30} {d['iterations']:>6} {d['mean_ms']:>7.1f}ms "
            f"{d['p50_ms']:>7.1f}ms {d['p95_ms']:>7.1f}ms {d['p99_ms']:>7.1f}ms "
            f"{d['throughput_ops_sec']:>9.0f}"
        )
    lines.append("=" * 80)
    return "\n".join(lines)


REGRESSION_THRESHOLDS = {
    "insert_single": {"p95_ms": 50, "throughput_ops_sec": 100},
    "query_keyword": {"p95_ms": 100, "throughput_ops_sec": 50},
    "query_importance": {"p95_ms": 80, "throughput_ops_sec": 50},
    "get_memory": {"p95_ms": 10, "throughput_ops_sec": 500},
    "update_memory": {"p95_ms": 50, "throughput_ops_sec": 100},
    "delete_memory": {"p95_ms": 50, "throughput_ops_sec": 80},
    "concurrent_reads_8t": {"p95_ms": 200, "throughput_ops_sec": 50},
}


def check_regression(results: list[BenchmarkResult]) -> list[str]:
    warnings = []
    for r in results:
        d = r.to_dict()
        thresholds = REGRESSION_THRESHOLDS.get(r.name, {})
        if "p95_ms" in thresholds and d["p95_ms"] > thresholds["p95_ms"]:
            warnings.append(
                f"REGRESSION: {r.name} P95={d['p95_ms']:.1f}ms exceeds threshold {thresholds['p95_ms']}ms"
            )
        if "throughput_ops_sec" in thresholds and d["throughput_ops_sec"] < thresholds["throughput_ops_sec"]:
            warnings.append(
                f"REGRESSION: {r.name} throughput={d['throughput_ops_sec']:.0f} ops/s below threshold {thresholds['throughput_ops_sec']} ops/s"
            )
    return warnings


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Agent Memory V12 Performance Benchmark")
    parser.add_argument("--check-regression", action="store_true", help="Exit with error on regression")
    args = parser.parse_args()

    bench = MemoryBenchmark()
    results = bench.run_all()
    print(format_results(results))

    warnings = check_regression(results)
    if warnings:
        print("\n⚠️ Performance Regressions Detected:")
        for w in warnings:
            print(f"  - {w}")
        if args.check_regression:
            raise SystemExit(1)
    else:
        print("\n✅ All benchmarks within acceptable thresholds.")


if __name__ == "__main__":
    main()
