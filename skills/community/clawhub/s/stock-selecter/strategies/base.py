#!/usr/bin/env python3
"""
策略基类
定义所有策略必须实现的接口契约，统一参数验证、结果格式、评分框架。
支持串行和并发两种执行模式。

并发说明：
  - workers > 1 时使用 ThreadPoolExecutor 并发分析股票
  - 适合 IO 密集型（API 调用等待），可提速 3-8 倍
  - 技术面策略（需要大量历史数据下载）建议开启并发
  - 财务面策略（数据量小）可保持串行以节省资源
"""

import time
import logging
import os
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

from utils.loader import import_shared_libs
_stock_utils, _stock_indicators = import_shared_libs()

logger = logging.getLogger("stock_screener")


class BaseStrategy(ABC):

    """
    所有筛选策略的抽象基类

    子类必须实现：
        - strategy_name (property)       ：策略唯一标识
        - default_params (property)      ：默认参数字典
        - analyze_stock(ts_code, name, params) → Optional[dict]

    子类可选覆盖：
        - sort_key / sort_reverse        ：排序规则
        - calculate_score / get_sort_field
        - post_process                    ：自定义后处理
        - _run_impl                      ：自定义 run() 实现（如需并发）
    """

    # ── 必须由子类实现的接口 ─────────────────────────────────────

    @property
    @abstractmethod
    def strategy_name(self) -> str:
        """策略唯一标识，如 'roe', 'macd'"""

    @property
    @abstractmethod
    def default_params(self) -> Dict[str, Any]:
        """默认参数字典（扁平结构）"""

    @abstractmethod
    def analyze_stock(self, ts_code: str, name: str,
                      params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        分析单只股票
        - 符合条件：返回包含 ts_code, name, score 等字段的 dict
        - 不符合条件：返回 None
        """

    # ── 可选覆盖的排序配置 ───────────────────────────────────────

    @property
    def sort_key(self) -> str:
        return "score"

    @property
    def sort_reverse(self) -> bool:
        return True   # 降序

    # ── 通用方法 ─────────────────────────────────────────────────

    def validate_params(self, user_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        将用户参数合并到默认参数中。
        只接受 default_params 中定义的 key，忽略未知参数。
        """
        merged = self.default_params.copy()
        if not user_params:
            return merged
        for key, value in user_params.items():
            if key not in merged:
                logger.debug(f"[{self.strategy_name}] 忽略未知参数: {key}")
                continue
            default_val = merged[key]
            try:
                if isinstance(default_val, bool):
                    merged[key] = bool(value)
                elif isinstance(default_val, int):
                    merged[key] = int(value)
                elif isinstance(default_val, float):
                    merged[key] = float(value)
                else:
                    merged[key] = value
            except (ValueError, TypeError):
                logger.warning(
                    f"[{self.strategy_name}] 参数 '{key}' 类型转换失败，"
                    f"使用默认值 {default_val}"
                )
        return merged

    def get_sort_value(self, result: Dict[str, Any]) -> float:
        val = result.get(self.sort_key, 0)
        return val if val is not None else 0

    def post_process(self, results: List[Dict[str, Any]],
                     params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """后处理：排序 + 截断。子类可覆盖以实现自定义逻辑。"""
        results.sort(key=self.get_sort_value, reverse=self.sort_reverse)
        top_n = params.get("top_n", 0)
        if top_n and top_n > 0:
            results = results[:top_n]
        return results

    # ── 执行入口（支持串行 / 并发两种模式）──────────────────────

    def run(self, params: Dict[str, Any] = None,
            limit: int = None) -> Dict[str, Any]:
        """
        完整执行流程：
          参数验证 → 获取股票列表 → 逐只分析 → 后处理 → 返回标准结果

        并发控制参数（来自 params）：
          workers (int)              ：并发线程数，默认 1（串行）
          sleep_between_stocks (float)：每只股票间休眠秒数，默认 0（不限速）
          batch_print (int)          ：每分析多少只打印一次进度，默认 50
        """
        start_time = time.time()
        validated  = self.validate_params(params or {})

        # 检查子类是否自定义 run 实现（如 MACD 策略）
        custom_impl = getattr(self, "_run_impl", None)
        if custom_impl is not None:
            return custom_impl(validated, limit, start_time)

        # 标准流程：尝试并发，失败则降级串行
        workers       = int(validated.get("workers", 1))
        sleep_between = float(validated.get("sleep_between_stocks", 0))
        batch_print   = int(validated.get("batch_print", 50))

        stocks = _stock_utils.get_stock_list(
            exclude_st=validated.get("exclude_st", True)
        )
        if not stocks:
            return self._error_result("无法获取股票列表", start_time, validated)

        if limit and limit > 0:
            stocks = stocks[:limit]

        total = len(stocks)
        logger.info(f"[{self.strategy_name}] 开始分析 {total} 只股票（workers={workers}）")

        results = []
        if workers > 1:
            results = self._run_parallel(stocks, validated, total, workers,
                                         sleep_between, batch_print, start_time)
        else:
            results = self._run_serial(stocks, validated, total,
                                      sleep_between, batch_print, start_time)

        results = self.post_process(results, validated)
        elapsed = round(time.time() - start_time, 2)

        return {
            "success": True,
            "strategy": self.strategy_name,
            "results": results,
            "count": len(results),
            "message": f"[{self.strategy_name}] 完成，命中 {len(results)}/{total} 只",
            "metadata": {
                "strategy": self.strategy_name,
                "execution_time": elapsed,
                "parameters_used": validated,
                "total_stocks_analyzed": total,
                "pass_rate": round(len(results) / total * 100, 2) if total else 0,
                "timestamp": datetime.now().isoformat(),
            }
        }

    # ── 串行执行（默认）──────────────────────────────────────────

    def _run_serial(self, stocks: List, validated: Dict, total: int,
                    sleep_between: float, batch_print: int,
                    start_time: float) -> List[Dict[str, Any]]:
        results = []
        for i, stock in enumerate(stocks):
            ts_code = stock[0]
            name    = stock[1] if len(stock) > 1 else ts_code
            indus   = stock[2] if len(stock) > 2 else "未知"

            if (i + 1) % batch_print == 0 or (i + 1) == total:
                elapsed = round(time.time() - start_time, 1)
                print(f"[{self.strategy_name}] 进度 {i+1}/{total}，"
                      f"命中 {len(results)} 只，耗时 {elapsed}s")

            try:
                r = self.analyze_stock(ts_code, name, validated)
                if r:
                    r.setdefault("industry", indus)
                    r.setdefault("strategy", self.strategy_name)
                    results.append(r)
            except Exception as e:
                logger.debug(f"[{self.strategy_name}] {ts_code} 分析异常: {e}")

            if sleep_between > 0:
                time.sleep(sleep_between)

        return results

    # ── 并发执行（workers > 1 时启用）────────────────────────────

    def _run_parallel(self, stocks: List, validated: Dict, total: int,
                      workers: int, sleep_between: float, batch_print: int,
                      start_time: float) -> List[Dict[str, Any]]:
        results_map: Dict[int, Dict] = {}
        lock_idx = [0]   # 用列表包装以便内部修改

        def _analyze_one(idx: int, stock: tuple) -> Tuple[int, Optional[Dict], str]:
            ts_code = stock[0]
            name    = stock[1] if len(stock) > 1 else ts_code
            indus   = stock[2] if len(stock) > 2 else "未知"
            try:
                r = self.analyze_stock(ts_code, name, validated)
                if r:
                    r.setdefault("industry", indus)
                    r.setdefault("strategy", self.strategy_name)
                    return idx, r, indus
            except Exception as e:
                logger.debug(f"[{self.strategy_name}] {ts_code} 分析异常: {e}")
            return idx, None, indus

        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {
                pool.submit(_analyze_one, i, s): i
                for i, s in enumerate(stocks)
            }

            for future in as_completed(futures):
                idx, r, _ = future.result()
                results_map[idx] = r

                completed = len(results_map)
                if completed % batch_print == 0 or completed == total:
                    print(f"[{self.strategy_name}] [并发] "
                          f"进度 {completed}/{total}，命中 {sum(1 for v in results_map.values() if v)} 只")

                if sleep_between > 0:
                    time.sleep(sleep_between)

        return [r for r in results_map.values() if r is not None]

    # ── 错误结果构造 ─────────────────────────────────────────────

    def _error_result(self, message: str,
                      start_time: float, params: Dict) -> Dict[str, Any]:
        return {
            "success": False,
            "strategy": self.strategy_name,
            "results": [],
            "count": 0,
            "message": message,
            "metadata": {
                "strategy": self.strategy_name,
                "execution_time": round(time.time() - start_time, 2),
                "parameters_used": params,
                "timestamp": datetime.now().isoformat(),
            }
        }
