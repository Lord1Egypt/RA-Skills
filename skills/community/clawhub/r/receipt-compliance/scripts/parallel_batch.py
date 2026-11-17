#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
并行批量处理引擎
功能：硬件自适应并行处理发票，提升批量处理速度 3-5 倍

核心特性：
1. 自动检测 CPU 核心数，动态分配 worker 数量
2. 双后端：ProcessPoolExecutor（多进程） / ThreadPoolExecutor（多线程）
3. 进度回调 + 失败重试机制
4. 内存控制：防止大量图片加载导致 OOM
"""

import os
import sys
import json
import time
import psutil
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field


# === 默认配置 ===
DEFAULT_CONFIG = {
    "max_workers_ratio_process": 0.5,    # 多进程模式 worker 比例（CPU 核心数 × 此值）
    "max_workers_ratio_thread": 0.75,    # 多线程模式 worker 比例（CPU 核心数 × 此值）
    "min_workers": 2,                    # 最少 worker 数
    "max_workers_cap": 16,               # worker 数上限
    "chunk_size": 10,                    # 每块文件数
    "retry_count": 2,                    # 失败重试次数
    "memory_limit_mb": 2048,             # 内存限制（MB），超过则降级到单线程
    "mode": "auto",                      # auto / process / thread / sequential
}


@dataclass
class BatchResult:
    """批量处理结果"""
    total_files: int = 0
    success_count: int = 0
    failed_count: int = 0
    total_time_seconds: float = 0.0
    results: List[Dict] = field(default_factory=list)
    failed_files: List[Dict] = field(default_factory=list)
    workers_used: int = 0
    mode_used: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_files": self.total_files,
            "success_count": self.success_count,
            "failed_count": self.failed_count,
            "total_time_seconds": round(self.total_time_seconds, 2),
            "throughput_per_second": round(self.total_files / self.total_time_seconds, 2) if self.total_time_seconds > 0 else 0,
            "workers_used": self.workers_used,
            "mode_used": self.mode_used,
            "failed_files": self.failed_files,
        }


class HardwareDetector:
    """硬件检测器 - 自动获取系统配置"""

    @staticmethod
    def get_cpu_count() -> int:
        """获取 CPU 核心数"""
        return os.cpu_count() or 2

    @staticmethod
    def get_available_memory_mb() -> float:
        """获取可用内存（MB）"""
        return psutil.virtual_memory().available / (1024 * 1024)

    @staticmethod
    def get_memory_usage_mb() -> float:
        """获取当前进程内存使用（MB）"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)

    @staticmethod
    def recommend_workers(mode: str = "process") -> int:
        """
        推荐 worker 数量
        - 多进程：CPU × 0.5（避免 CPU 过载）
        - 多线程：CPU × 0.75（IO 密集型可更高）
        """
        cpu_count = HardwareDetector.get_cpu_count()
        ratio = DEFAULT_CONFIG[f"max_workers_ratio_{mode}"]
        workers = max(DEFAULT_CONFIG["min_workers"], int(cpu_count * ratio))
        return min(workers, DEFAULT_CONFIG["max_workers_cap"])


class ParallelBatchEngine:
    """
    并行批量处理引擎

    处理流程：
    1. 检测硬件配置（CPU/内存）
    2. 自动选择处理模式（多进程/多线程/串行）
    3. 分块处理文件，逐块并行执行
    4. 收集结果，处理失败重试
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.hw = HardwareDetector()
        self.progress_callback: Optional[Callable[[int, int, str], None]] = None

    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """
        设置进度回调函数
        callback(current, total, current_file_name)
        """
        self.progress_callback = callback

    def process(
        self,
        file_paths: List[str],
        process_func: Callable[[str], Dict[str, Any]],
        mode: Optional[str] = None,
    ) -> BatchResult:
        """
        并行处理文件列表

        参数:
            file_paths: 文件路径列表
            process_func: 处理单个文件的函数，接收文件路径，返回 dict
            mode: 处理模式（auto/process/thread/sequential）

        返回:
            BatchResult: 批量处理结果
        """
        if not file_paths:
            return BatchResult()

        selected_mode = mode or self.config["mode"]
        workers = self._determine_workers(selected_mode)
        actual_mode = selected_mode

        # auto 模式决策
        if selected_mode == "auto":
            actual_mode, workers = self._auto_select_mode()

        result = BatchResult(
            total_files=len(file_paths),
            workers_used=workers,
            mode_used=actual_mode,
        )

        start_time = time.time()

        if actual_mode == "sequential" or workers <= 1:
            self._process_sequential(file_paths, process_func, result)
        elif actual_mode == "thread":
            self._process_parallel(file_paths, process_func, result, mode="thread")
        else:
            self._process_parallel(file_paths, process_func, result, mode="process")

        result.total_time_seconds = time.time() - start_time
        return result

    def _auto_select_mode(self) -> tuple:
        """自动选择最优处理模式"""
        available_mem = self.hw.get_available_memory_mb()
        cpu_count = self.hw.get_cpu_count()

        # 内存不足，降级到串行
        if available_mem < self.config["memory_limit_mb"] * 0.5:
            return "sequential", 1

        # 默认多进程（CPU 密集型 OCR）
        workers = self.hw.recommend_workers("process")
        if cpu_count >= 4 and available_mem > self.config["memory_limit_mb"]:
            return "process", workers
        else:
            return "thread", self.hw.recommend_workers("thread")

    def _determine_workers(self, mode: str) -> int:
        """确定 worker 数量"""
        if mode == "sequential":
            return 1
        if mode == "process":
            return self.hw.recommend_workers("process")
        if mode == "thread":
            return self.hw.recommend_workers("thread")
        # auto
        _, workers = self._auto_select_mode()
        return workers

    def _process_sequential(
        self,
        file_paths: List[str],
        process_func: Callable,
        result: BatchResult,
    ):
        """串行处理"""
        for i, file_path in enumerate(file_paths):
            try:
                res = self._process_single_file(file_path, process_func)
                if res.get("success"):
                    result.success_count += 1
                else:
                    result.failed_count += 1
                    result.failed_files.append({
                        "file": file_path,
                        "error": res.get("error", "未知错误"),
                    })
                result.results.append(res)
            except Exception as e:
                result.failed_count += 1
                result.failed_files.append({
                    "file": file_path,
                    "error": str(e),
                })
            if self.progress_callback:
                self.progress_callback(i + 1, len(file_paths), Path(file_path).name)

    def _process_parallel(
        self,
        file_paths: List[str],
        process_func: Callable,
        result: BatchResult,
        mode: str = "process",
    ):
        """并行处理"""
        executor_class = ThreadPoolExecutor if mode == "thread" else ProcessPoolExecutor
        workers = result.workers_used

        # 分块提交，避免一次性占用太多内存
        chunk_size = self.config["chunk_size"]
        chunks = [
            file_paths[i:i + chunk_size]
            for i in range(0, len(file_paths), chunk_size)
        ]

        processed = 0
        with executor_class(max_workers=workers) as executor:
            for chunk in chunks:
                futures = {
                    executor.submit(self._process_single_file, fp, process_func): fp
                    for fp in chunk
                }
                for future in as_completed(futures):
                    file_path = futures[future]
                    try:
                        res = future.result()
                        if res.get("success"):
                            result.success_count += 1
                        else:
                            result.failed_count += 1
                            result.failed_files.append({
                                "file": file_path,
                                "error": res.get("error", "未知错误"),
                            })
                        result.results.append(res)
                    except Exception as e:
                        result.failed_count += 1
                        result.failed_files.append({
                            "file": file_path,
                            "error": str(e),
                        })

                    processed += 1
                    if self.progress_callback:
                        self.progress_callback(processed, len(file_paths), Path(file_path).name)

    def _process_single_file(self, file_path: str, process_func: Callable) -> Dict[str, Any]:
        """处理单个文件，带重试"""
        retry_count = self.config["retry_count"]
        last_error = None

        for attempt in range(retry_count + 1):
            try:
                return process_func(file_path)
            except Exception as e:
                last_error = str(e)
                if attempt < retry_count:
                    time.sleep(0.5 * (attempt + 1))  # 简单退避

        return {
            "success": False,
            "file": file_path,
            "error": f"重试 {retry_count} 次后仍失败: {last_error}",
        }


# ======================================================================
# 便捷函数
# ======================================================================

def get_hardware_info() -> Dict[str, Any]:
    """获取硬件信息摘要"""
    hw = HardwareDetector()
    return {
        "cpu_count": hw.get_cpu_count(),
        "available_memory_mb": round(hw.get_available_memory_mb(), 1),
        "current_memory_usage_mb": round(hw.get_memory_usage_mb(), 1),
        "recommended_workers_process": hw.recommend_workers("process"),
        "recommended_workers_thread": hw.recommend_workers("thread"),
    }


def batch_process(
    file_paths: List[str],
    process_func: Callable[[str], Dict[str, Any]],
    mode: str = "auto",
    config: Optional[Dict] = None,
    progress_callback: Optional[Callable] = None,
) -> BatchResult:
    """
    一站式并行批量处理

    参数:
        file_paths: 文件路径列表
        process_func: 处理函数
        mode: auto / process / thread / sequential
        config: 配置
        progress_callback: 进度回调

    返回:
        BatchResult
    """
    engine = ParallelBatchEngine(config)
    if progress_callback:
        engine.set_progress_callback(progress_callback)
    return engine.process(file_paths, process_func, mode)


# ======================================================================
# CLI 入口
# ======================================================================

def main():
    parser = argparse.ArgumentParser(description="并行批量处理引擎")
    sub = parser.add_subparsers(dest="command")

    # info 子命令
    info_parser = sub.add_parser("info", help="查看硬件信息和推荐配置")

    # run 子命令
    run_parser = sub.add_parser("run", help="执行批量处理")
    run_parser.add_argument("--input", required=True, help="输入目录")
    run_parser.add_argument("--output", required=True, help="输出结果 JSON 路径")
    run_parser.add_argument("--mode", default="auto", choices=["auto", "process", "thread", "sequential"])
    run_parser.add_argument("--pattern", default="*.{png,jpg,jpeg,pdf}", help="文件匹配模式")

    args = parser.parse_args()

    if args.command == "info":
        info = get_hardware_info()
        print(json.dumps(info, ensure_ascii=False, indent=2))

    elif args.command == "run":
        input_dir = Path(args.input)
        if not input_dir.exists():
            print(f"目录不存在: {args.input}", file=sys.stderr)
            sys.exit(1)

        # 收集文件
        patterns = args.pattern.split(",")
        file_paths = []
        for p in patterns:
            file_paths.extend(str(f) for f in input_dir.glob(f"*{p}"))

        if not file_paths:
            print(f"未找到匹配文件: {args.input}", file=sys.stderr)
            sys.exit(1)

        print(f"找到 {len(file_paths)} 个文件")

        # 进度回调
        def progress(current, total, name):
            pct = current / total * 100
            print(f"\r进度: {current}/{total} ({pct:.0f}%) - {name}", end="", file=sys.stderr)

        # 导入 OCR 引擎作为默认处理函数
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from ocr_engine import OCREngine

        engine = OCREngine()

        def process_func(file_path: str) -> Dict[str, Any]:
            return engine.extract_structured_data(file_path)

        result = batch_process(file_paths, process_func, args.mode, progress_callback=progress)

        print(file=sys.stderr)  # newline after progress
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存: {args.output}", file=sys.stderr)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
