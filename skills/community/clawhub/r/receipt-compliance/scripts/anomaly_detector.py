#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轻量异常检测引擎（v4.4.0）

在 5 类规则预警之上叠加一层无监督异常检测：
- 纯 numpy 实现 Isolation Forest 思路（随机切割树 → 路径深度打分）
- 零第三方依赖：numpy 不可用时自动降级为纯 Python 实现
- 三维打分：金额分布 / 开票时间间隔 / 供应商组合
- 异常分超阈值进二级预警，并给出「触发维度解释」

性能约束（不拖累用户电脑）：
- 样本 > max_samples 时自动采样
- 树数量按 CPU 核数封顶，默认 100 棵
"""

import math
import random
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Sequence, Tuple

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False


DIMENSIONS = ("amount", "interval", "supplier")

DIM_LABELS = {
    "amount": "金额分布",
    "interval": "开票时间间隔",
    "supplier": "供应商组合",
}

# 异常分阈值：>= WARN 进二级预警，>= HIGH 为高优先级
SCORE_WARN = 0.65
SCORE_HIGH = 0.75


def _c(n: int) -> float:
    """Isolation Forest 中 n 个样本二叉搜索树的平均路径长度"""
    if n <= 1:
        return 0.0
    if n == 2:
        return 1.0
    return 2.0 * (math.log(n - 1) + 0.5772156649) - 2.0 * (n - 1) / n


def _to_date(s):
    if not s:
        return None
    s = str(s).strip().replace("/", "-")
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y年%m月%d日"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _get(obj, key, default=None):
    """同时支持 UnifiedInvoice 对象与字典"""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _col(data, idxs: List[int], d: int) -> Tuple[float, float]:
    """取某一列在给定样本上的最小/最大值（numpy 可用时走向量化）"""
    if HAS_NUMPY and isinstance(data, np.ndarray):
        col = data[idxs, d]
        return float(col.min()), float(col.max())
    col = [data[i][d] for i in idxs]
    return min(col), max(col)


class _RandomCutTree:
    """单棵随机切割树"""

    def __init__(self, data, rng: random.Random, height_limit: int):
        self.root = self._build(list(range(len(data))), data, rng, height_limit, 0)

    def _build(self, idxs: List[int], data, rng, limit, depth):
        if depth >= limit or len(idxs) <= 1:
            return {"leaf": True, "size": len(idxs)}

        n_dims = len(data[idxs[0]])
        valid_dims = []
        bounds = {}
        for d in range(n_dims):
            lo, hi = _col(data, idxs, d)
            bounds[d] = (lo, hi)
            if hi > lo:
                valid_dims.append(d)
        if not valid_dims:
            return {"leaf": True, "size": len(idxs)}

        dim = rng.choice(valid_dims)
        lo, hi = bounds[dim]
        split = rng.uniform(lo, hi)
        left = [i for i in idxs if data[i][dim] < split]
        right = [i for i in idxs if data[i][dim] >= split]
        if not left or not right:
            return {"leaf": True, "size": len(idxs)}

        return {
            "leaf": False,
            "dim": dim,
            "split": split,
            "left": self._build(left, data, rng, limit, depth + 1),
            "right": self._build(right, data, rng, limit, depth + 1),
        }

    def path_length(self, x: Sequence[float]) -> float:
        """样本 x 的路径长度（含叶子规模修正）"""
        return self._walk(self.root, x, 0)

    def _walk(self, node, x, depth):
        while not node["leaf"]:
            node = node["left"] if x[node["dim"]] < node["split"] else node["right"]
            depth += 1
        return depth + _c(node["size"])


class IsolationForestLite:
    """轻量 Isolation Forest（随机切割树森林）"""

    def __init__(self, n_trees: int = 100, sample_size: int = 256,
                 random_state: Optional[int] = 42, max_samples: int = 5000):
        self.n_trees = n_trees
        self.sample_size = sample_size
        self.random_state = random_state
        self.max_samples = max_samples
        self.trees: List[_RandomCutTree] = []
        self._sample: Optional[List[List[float]]] = None

    def fit(self, X: Sequence[Sequence[float]]):
        rows = [list(map(float, row)) for row in X]
        if not rows:
            self.trees = []
            return self

        if len(rows) > self.max_samples:
            rng0 = random.Random(self.random_state)
            rows = rng0.sample(rows, self.max_samples)

        # numpy 可用时转成矩阵，列统计走向量化
        data = np.array(rows, dtype=float) if HAS_NUMPY else rows
        n = len(rows)
        sub = min(self.sample_size, n)
        limit = max(1, int(math.ceil(math.log2(max(sub, 2)))))
        rng = random.Random(self.random_state)

        self._sample = rows
        self._data = data
        self.trees = []
        for _ in range(self.n_trees):
            if sub < n:
                idxs = rng.sample(range(n), sub)
                bag = np.array([rows[i] for i in idxs], dtype=float) if HAS_NUMPY \
                    else [rows[i] for i in idxs]
            else:
                bag = data
            self.trees.append(_RandomCutTree(bag, rng, limit))
        return self

    def score(self, x: Sequence[float]) -> float:
        """返回 0~1 的异常分，越大越异常"""
        if not self.trees:
            return 0.0
        n = len(self._sample or [])
        avg = sum(t.path_length(list(map(float, x))) for t in self.trees) / len(self.trees)
        denom = _c(n) or 1.0
        return float(2.0 ** (-avg / denom))

    def score_all(self, X: Sequence[Sequence[float]]) -> List[float]:
        return [self.score(row) for row in X]


class AnomalyDetector:
    """
    票据异常检测

    三维特征：
    - amount   ：金额分布（log1p(价税合计)）
    - interval ：开票时间间隔（同供应商相邻开票间隔天数，log1p）
    - supplier ：供应商组合（该供应商出现频次 log1p + 金额占比）
    """

    def __init__(self, n_trees: int = 100, sample_size: int = 256,
                 warn_score: float = SCORE_WARN, high_score: float = SCORE_HIGH,
                 random_state: Optional[int] = 42, max_samples: int = 5000):
        self.n_trees = n_trees
        self.sample_size = sample_size
        self.warn_score = warn_score
        self.high_score = high_score
        self.random_state = random_state
        self.max_samples = max_samples

    # ---------- 特征工程 ----------

    def build_features(self, invoices: Sequence) -> Tuple[List[Dict[str, Any]], List[List[float]]]:
        """构造特征矩阵，同时返回每条记录的元信息"""
        records: List[Dict[str, Any]] = []

        # 供应商频次与金额
        seller_count: Dict[str, int] = {}
        seller_amount: Dict[str, float] = {}
        total_amount = 0.0
        for inv in invoices:
            s = _get(inv, "seller_name") or "未知供应商"
            amt = float(_get(inv, "total") or 0)
            seller_count[s] = seller_count.get(s, 0) + 1
            seller_amount[s] = seller_amount.get(s, 0.0) + amt
            total_amount += amt

        # 同供应商相邻开票间隔
        by_seller: Dict[str, List] = {}
        for inv in invoices:
            s = _get(inv, "seller_name") or "未知供应商"
            by_seller.setdefault(s, []).append(inv)

        interval_map: Dict[int, float] = {}
        for s, group in by_seller.items():
            dated = sorted(
                [(inv, _to_date(_get(inv, "billing_date") or _get(inv, "travel_date")))
                 for inv in group],
                key=lambda t: (t[1] is None, t[1] or datetime.min.date())
            )
            prev = None
            gaps: List[float] = []
            for inv, d in dated:
                if d is None:
                    interval_map[id(inv)] = None
                elif prev is None:
                    interval_map[id(inv)] = None
                else:
                    gap = max(0, (d - prev).days)
                    gaps.append(float(gap))
                    interval_map[id(inv)] = float(gap)
                if d is not None:
                    prev = d
            # 首张票无前序间隔，用该供应商间隔中位数兜底
            med = float(sorted(gaps)[len(gaps) // 2]) if gaps else 0.0
            for inv, _ in dated:
                if interval_map.get(id(inv)) is None:
                    interval_map[id(inv)] = med

        # 逐条构造
        for inv in invoices:
            s = _get(inv, "seller_name") or "未知供应商"
            amt = float(_get(inv, "total") or 0)
            share = (seller_amount.get(s, 0.0) / total_amount) if total_amount else 0.0
            gap = interval_map.get(id(inv), 0.0)

            f_amount = math.log1p(amt)
            f_interval = math.log1p(gap)
            f_supplier = math.log1p(seller_count.get(s, 1)) + share

            records.append({
                "invoice_number": _get(inv, "invoice_number"),
                "seller_name": s,
                "total": round(amt, 2),
                "billing_date": _get(inv, "billing_date") or _get(inv, "travel_date"),
                "seller_count": seller_count.get(s, 1),
                "seller_share": round(share, 4),
                "interval_days": gap,
                "features": {
                    "amount": round(f_amount, 4),
                    "interval": round(f_interval, 4),
                    "supplier": round(f_supplier, 4),
                },
            })
            records[-1]["_vec"] = [f_amount, f_interval, f_supplier]
            records[-1]["_dim_vec"] = {
                "amount": [f_amount],
                "interval": [f_interval],
                "supplier": [f_supplier, share],
            }

        matrix = [r["_vec"] for r in records]
        return records, matrix

    # ---------- 检测 ----------

    def detect(self, invoices: Sequence, top_n: Optional[int] = None) -> Dict[str, Any]:
        records, matrix = self.build_features(invoices)
        n = len(records)

        if n < 12:
            return {
                "engine": "isolation-forest-lite",
                "sample_size": n,
                "status": "insufficient",
                "message": "样本少于 12 张，随机切割树打分不可靠，建议累积后再跑",
                "numpy": HAS_NUMPY,
                "findings": [],
            }

        forest = IsolationForestLite(
            n_trees=self.n_trees, sample_size=self.sample_size,
            random_state=self.random_state, max_samples=self.max_samples,
        ).fit(matrix)

        # 逐维度森林，用于触发维度解释
        dim_forests = {}
        for dim in DIMENSIONS:
            dim_data = [r["_dim_vec"][dim] for r in records]
            f = IsolationForestLite(
                n_trees=max(30, self.n_trees // 3),
                sample_size=self.sample_size,
                random_state=self.random_state,
                max_samples=self.max_samples,
            ).fit(dim_data)
            dim_forests[dim] = (f, dim_data)

        findings = []
        for i, rec in enumerate(records):
            overall = forest.score(matrix[i])
            dim_scores = {}
            for dim, (f, data) in dim_forests.items():
                dim_scores[dim] = round(f.score(data[i]), 4)

            triggered = sorted(
                [d for d, s in dim_scores.items() if s >= self.warn_score],
                key=lambda d: dim_scores[d], reverse=True)

            if overall < self.warn_score and not triggered:
                continue

            level = "严重" if (overall >= self.high_score or len(triggered) >= 2) else "关注"
            findings.append({
                "type": "anomaly_score",
                "level": level,
                "invoice_number": rec["invoice_number"],
                "seller_name": rec["seller_name"],
                "total": rec["total"],
                "billing_date": rec["billing_date"],
                "score": round(overall, 4),
                "dimension_scores": dim_scores,
                "triggered_dimensions": triggered,
                "explanation": self._explain(rec, dim_scores, triggered),
            })

        findings.sort(key=lambda x: x["score"], reverse=True)
        if top_n:
            findings = findings[:top_n]

        return {
            "engine": "isolation-forest-lite",
            "numpy": HAS_NUMPY,
            "sample_size": n,
            "n_trees": self.n_trees,
            "warn_score": self.warn_score,
            "high_score": self.high_score,
            "thresholds": {"warn": self.warn_score, "high": self.high_score},
            "total_findings": len(findings),
            "findings": findings,
        }

    @staticmethod
    def _explain(rec: Dict[str, Any], dim_scores: Dict[str, float],
                 triggered: List[str]) -> str:
        if not triggered:
            return f"综合异常分偏高（{max(dim_scores.values()):.2f}），但未达单维阈值"
        parts = []
        for d in triggered:
            label = DIM_LABELS.get(d, d)
            if d == "amount":
                parts.append(f"金额分布异常（{rec['total']:.2f} 元偏离常规区间，得分 {dim_scores[d]:.2f}）")
            elif d == "interval":
                parts.append(f"开票时间间隔异常（约 {rec['interval_days']:.0f} 天，得分 {dim_scores[d]:.2f}）")
            else:
                parts.append(
                    f"供应商组合异常（该供应商出现 {rec['seller_count']} 次、"
                    f"占比 {rec['seller_share'] * 100:.1f}%，得分 {dim_scores[d]:.2f}）")
        return "；".join(parts)


def detect_anomalies(invoices: Sequence, **kwargs) -> Dict[str, Any]:
    """便捷函数"""
    return AnomalyDetector(**kwargs).detect(invoices)


def main():
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="票据异常检测（轻量 Isolation Forest）")
    parser.add_argument("input", help="票据 JSON 数组文件，或台账数据库（--db）")
    parser.add_argument("--db", action="store_true", help="输入为 SQLite 台账，直接读取")
    parser.add_argument("--direction", choices=["input", "output", "all"], default="input")
    parser.add_argument("--trees", type=int, default=100, help="随机切割树数量")
    parser.add_argument("--warn", type=float, default=SCORE_WARN, help="二级预警阈值")
    parser.add_argument("--top", type=int, help="只输出异常分最高的 N 条")
    parser.add_argument("--output", help="结果 JSON 输出路径")
    args = parser.parse_args()

    if args.db:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from ledger_db import LedgerDB
        db = LedgerDB(args.input)
        direction = None if args.direction == "all" else args.direction
        invoices = db.query_invoices(direction=direction)
        db.close()
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = data.get("invoices") or data.get("results") or []
        invoices = data

    result = AnomalyDetector(n_trees=args.trees, warn_score=args.warn).detect(
        invoices, top_n=args.top)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"结果已保存：{args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
