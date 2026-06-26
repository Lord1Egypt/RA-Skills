"""
基准运行器 — SkillHub 模拟基准
对选定 skill 运行 N 次，统计成功率和耗时，生成基准数据
"""

import json
import os
import time
import uuid
import statistics
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from skills_monitor.data.store import DataStore
from skills_monitor.adapters.skill_registry import SkillInfo, SkillRegistry
from skills_monitor.adapters.runners import SkillRunner, get_adapter


# ──────── 标准化测试任务 ────────

STANDARD_TEST_CASES: Dict[str, List[Dict[str, Any]]] = {
    "a-share-short-decision": [
        {"task": "get_market_sentiment", "params": {}, "description": "获取市场情绪"},
        {"task": "get_sector_rotation", "params": {}, "description": "板块轮动分析"},
        {"task": "scan_strong_stocks", "params": {}, "description": "强势股扫描"},
        {"task": "analyze_capital_flow", "params": {}, "description": "资金流向分析"},
    ],
    "stock-screener-cn": [
        {"task": "screen_stocks", "params": {"strategy": "金叉", "limit": 10}, "description": "金叉策略筛选"},
        {"task": "screen_stocks", "params": {"strategy": "均线多头排列", "limit": 10}, "description": "均线多头策略"},
        {"task": "screen_stocks", "params": {"strategy": "放量突破", "limit": 10}, "description": "放量突破策略"},
    ],
    "trading-signals": [
        {"task": "analyze_signals", "params": {}, "description": "综合交易信号分析"},
    ],
    "finance-news-analyzer": [
        {"task": "", "params": {}, "description": "每日新闻摘要"},
    ],
    "a-stock-monitor": [
        {"task": "", "params": {}, "description": "A股监控"},
    ],
    "macro-analyst": [
        {"task": "", "params": {}, "description": "宏观经济分析"},
    ],
}


class BenchmarkResult:
    """单次基准运行结果"""

    def __init__(
        self,
        skill_id: str,
        task_name: str,
        run_index: int,
        success: bool,
        duration_ms: float,
        output: Any = None,
        error: Optional[str] = None,
        timestamp: Optional[str] = None,
    ):
        self.skill_id = skill_id
        self.task_name = task_name
        self.run_index = run_index
        self.success = success
        self.duration_ms = duration_ms
        self.output = output
        self.error = error
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "task_name": self.task_name,
            "run_index": self.run_index,
            "success": self.success,
            "duration_ms": round(self.duration_ms, 2),
            "error": self.error,
            "timestamp": self.timestamp,
        }


class BenchmarkStats:
    """基准运行统计"""

    def __init__(self, skill_id: str, task_name: str, results: List[BenchmarkResult]):
        self.skill_id = skill_id
        self.task_name = task_name
        self.total_runs = len(results)
        self.success_count = sum(1 for r in results if r.success)
        self.error_count = self.total_runs - self.success_count
        self.success_rate = (
            round(self.success_count / self.total_runs * 100, 1)
            if self.total_runs > 0
            else 0
        )

        durations = [r.duration_ms for r in results if r.success]
        if durations:
            self.avg_duration_ms = round(statistics.mean(durations), 2)
            self.median_duration_ms = round(statistics.median(durations), 2)
            self.min_duration_ms = round(min(durations), 2)
            self.max_duration_ms = round(max(durations), 2)
            self.p95_duration_ms = round(
                sorted(durations)[int(len(durations) * 0.95)], 2
            )
            self.stddev_duration_ms = (
                round(statistics.stdev(durations), 2) if len(durations) > 1 else 0
            )
        else:
            self.avg_duration_ms = None
            self.median_duration_ms = None
            self.min_duration_ms = None
            self.max_duration_ms = None
            self.p95_duration_ms = None
            self.stddev_duration_ms = None

        self.results = results
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "task_name": self.task_name,
            "total_runs": self.total_runs,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": self.success_rate,
            "avg_duration_ms": self.avg_duration_ms,
            "median_duration_ms": self.median_duration_ms,
            "min_duration_ms": self.min_duration_ms,
            "max_duration_ms": self.max_duration_ms,
            "p95_duration_ms": self.p95_duration_ms,
            "stddev_duration_ms": self.stddev_duration_ms,
            "timestamp": self.timestamp,
        }

    def summary_line(self) -> str:
        """一行式汇总"""
        dur = f"{self.avg_duration_ms:.0f}ms" if self.avg_duration_ms else "N/A"
        p95 = f"{self.p95_duration_ms:.0f}ms" if self.p95_duration_ms else "N/A"
        return (
            f"成功率: {self.success_rate}% ({self.success_count}/{self.total_runs})  "
            f"平均: {dur}  P95: {p95}"
        )


class BenchmarkRunner:
    """基准运行器"""

    def __init__(
        self,
        registry: SkillRegistry,
        store: DataStore,
        agent_id: str,
        cache_dir: Optional[str] = None,
    ):
        self.registry = registry
        self.store = store
        self.agent_id = agent_id
        self.cache_dir = cache_dir
        if cache_dir:
            Path(cache_dir).mkdir(parents=True, exist_ok=True)

    def get_test_cases(self, skill_id: str) -> List[Dict[str, Any]]:
        """获取指定 skill 的标准化测试任务"""
        return STANDARD_TEST_CASES.get(skill_id, [])

    def run_benchmark(
        self,
        skill_id: str,
        task_name: str = "",
        params: Optional[Dict] = None,
        n_runs: int = 10,
        delay_between: float = 0.5,
        progress_callback: Optional[Callable[[int, int, BenchmarkResult], None]] = None,
    ) -> BenchmarkStats:
        """
        对指定 skill+task 运行 N 次，返回统计结果

        Args:
            skill_id: skill 标识
            task_name: 任务名称
            params: 任务参数
            n_runs: 运行次数
            delay_between: 每次运行间隔（秒）
            progress_callback: 进度回调 (current, total, result)
        """
        if params is None:
            params = {}

        skill_info = self.registry.get_skill(skill_id)
        if not skill_info:
            raise ValueError(f"未找到 skill: {skill_id}")

        adapter = get_adapter(skill_info)
        results: List[BenchmarkResult] = []

        for i in range(n_runs):
            start_time = time.time()
            success = False
            output = None
            error = None

            try:
                if isinstance(adapter, SkillRunner):
                    run_result = adapter.run(task_name=task_name, params=params)
                elif hasattr(adapter, "run_task"):
                    run_result = adapter.run_task(task_name, **params)
                else:
                    run_result = {"success": False, "error": "无适配器"}

                success = run_result.get("success", False)
                output = run_result.get("output")
                error = run_result.get("error")
            except Exception as e:
                success = False
                error = f"{type(e).__name__}: {e}"

            duration_ms = (time.time() - start_time) * 1000

            result = BenchmarkResult(
                skill_id=skill_id,
                task_name=task_name or "default",
                run_index=i + 1,
                success=success,
                duration_ms=duration_ms,
                output=output,
                error=error,
            )
            results.append(result)

            # 同时记录到数据库（作为基准运行记录）
            run_id = f"bench-{str(uuid.uuid4())[:8]}"
            self.store.insert_run({
                "run_id": run_id,
                "agent_id": self.agent_id,
                "skill_id": skill_id,
                "task_name": f"[benchmark] {task_name or 'default'}",
                "status": "success" if success else "error",
                "start_time": result.timestamp,
                "end_time": datetime.now().isoformat(),
                "duration_ms": round(duration_ms, 2),
                "input_data": {"benchmark": True, "run_index": i + 1, "params": params},
                "output_data": None,  # 不存基准输出
                "error_msg": error,
                "metadata": {"benchmark_run": True, "n_runs": n_runs},
            })

            if progress_callback:
                progress_callback(i + 1, n_runs, result)

            # 运行间隔
            if i < n_runs - 1 and delay_between > 0:
                time.sleep(delay_between)

        stats = BenchmarkStats(skill_id, task_name or "default", results)

        # 缓存结果
        if self.cache_dir:
            self._cache_stats(stats)

        return stats

    def run_full_benchmark(
        self,
        skill_id: str,
        n_runs: int = 5,
        delay_between: float = 0.5,
        progress_callback: Optional[Callable] = None,
    ) -> Dict[str, BenchmarkStats]:
        """
        对指定 skill 的所有标准测试任务运行基准

        Returns:
            {task_name: BenchmarkStats}
        """
        test_cases = self.get_test_cases(skill_id)
        if not test_cases:
            # 没有预定义的测试任务，运行默认
            stats = self.run_benchmark(
                skill_id, n_runs=n_runs,
                delay_between=delay_between,
                progress_callback=progress_callback,
            )
            return {"default": stats}

        results = {}
        for tc in test_cases:
            task = tc["task"]
            params = tc.get("params", {})
            desc = tc.get("description", task)

            if progress_callback:
                progress_callback(-1, -1, None)  # signal: new task starting

            stats = self.run_benchmark(
                skill_id,
                task_name=task,
                params=params,
                n_runs=n_runs,
                delay_between=delay_between,
                progress_callback=progress_callback,
            )
            results[desc] = stats

        return results

    def run_simulated_benchmark(
        self,
        skill_id: str,
        n_runs: int = 10,
        base_duration_ms: float = 2000,
        success_rate: float = 0.85,
        duration_variance: float = 0.3,
    ) -> BenchmarkStats:
        """
        模拟基准运行（不实际执行 skill，用于非交易时段或快速 Demo）

        Args:
            base_duration_ms: 基线耗时
            success_rate: 模拟成功率
            duration_variance: 耗时波动系数 (0-1)
        """
        import random

        results: List[BenchmarkResult] = []
        for i in range(n_runs):
            success = random.random() < success_rate

            # 生成有波动的耗时
            factor = 1 + random.uniform(-duration_variance, duration_variance)
            duration = base_duration_ms * factor
            if not success:
                # 失败通常更快（超时除外）
                duration = base_duration_ms * random.choice([0.1, 0.3, 2.5])

            result = BenchmarkResult(
                skill_id=skill_id,
                task_name="simulated",
                run_index=i + 1,
                success=success,
                duration_ms=duration,
                error="模拟失败：超时" if not success else None,
            )
            results.append(result)

        return BenchmarkStats(skill_id, "simulated", results)

    # ──────── 缓存 ────────

    def _cache_stats(self, stats: BenchmarkStats):
        """将基准结果缓存到本地 JSON"""
        if not self.cache_dir:
            return
        cache_file = os.path.join(
            self.cache_dir,
            f"bench_{stats.skill_id}_{stats.task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        )
        with open(cache_file, "w", encoding="utf-8") as f:
            data = stats.to_dict()
            data["results"] = [r.to_dict() for r in stats.results]
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_cached_stats(self, skill_id: str, task_name: str = "") -> Optional[BenchmarkStats]:
        """加载最近的缓存基准数据"""
        if not self.cache_dir:
            return None

        prefix = f"bench_{skill_id}_{task_name or ''}"
        cache_files = sorted(
            [
                f
                for f in os.listdir(self.cache_dir)
                if f.startswith(prefix) and f.endswith(".json")
            ],
            reverse=True,
        )

        if not cache_files:
            return None

        try:
            with open(os.path.join(self.cache_dir, cache_files[0]), "r", encoding="utf-8") as f:
                data = json.load(f)

            results = [
                BenchmarkResult(
                    skill_id=r["skill_id"],
                    task_name=r["task_name"],
                    run_index=r["run_index"],
                    success=r["success"],
                    duration_ms=r["duration_ms"],
                    error=r.get("error"),
                    timestamp=r.get("timestamp"),
                )
                for r in data.get("results", [])
            ]
            return BenchmarkStats(skill_id, task_name, results)
        except Exception:
            return None
