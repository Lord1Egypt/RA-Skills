#!/usr/bin/env python3
"""
stock-selecter 统一选股技能包
将多种选股策略聚合为单一入口，支持单策略、多策略组合（AND/OR/SCORE模式），
并发执行加速，以及 HTML 可视化报告输出。

用法示例：
  # 单策略 ROE
  python main.py --strategy roe --roe_threshold 15

  # 多策略交集（AND）
  python main.py --strategy roe,macd,trend --mode and

  # 并发执行（workers=8）
  python main.py --strategy roe --workers 8

  # 综合评分模式
  python main.py --strategy all --mode score --top 50

  # 生成 HTML 报告
  python main.py --strategy roe,macd --report --output_dir "~/Desktop"
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any

# ── 路径修正 ─────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# ── 配置加载 ─────────────────────────────────────────────────────────
_CONFIG_PATH = os.path.join(_HERE, "config.json")
_DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Desktop")


def _load_config() -> Dict[str, Any]:
    if os.path.exists(_CONFIG_PATH):
        with open(_CONFIG_PATH, encoding="utf-8") as f:
            cfg = json.load(f)
        token = cfg.get("token", "")
        if token and token != "YOUR_TUSHARE_TOKEN_HERE":
            os.environ["TUSHARE_TOKEN"] = token
        return cfg
    return {}


_CONFIG = _load_config()

# ── 共享库加载 ───────────────────────────────────────────────────────
from utils.loader import import_shared_libs
_stock_utils, _stock_indicators = import_shared_libs()

# ── 策略注册表 ──────────────────────────────────────────────────────
from strategies.roe                           import ROEStrategy
from strategies.macd                          import MACDStrategy
from strategies.dividend                      import DividendStrategy
from strategies.valuation                     import ValuationStrategy
from strategies.growth                        import GrowthStrategy
from strategies.low_position                  import LowPositionStrategy
from strategies.volume_surge                  import VolumeSurgeStrategy
from strategies.trend                         import TrendStrategy
from strategies.pattern                       import PatternStrategy
from strategies.bollinger                     import BollingerStrategy
from strategies.shareholder_concentration     import ShareholderConcentrationStrategy
from strategies.cashflow_quality             import CashflowQualityStrategy
from strategies.northbound_flow              import NorthboundFlowStrategy
from strategies.shareholder_buyback           import ShareholderBuybackStrategy
from strategies.analyst_target               import AnalystTargetStrategy

STRATEGY_REGISTRY: Dict[str, Any] = {
    "roe":                          ROEStrategy,
    "macd":                         MACDStrategy,
    "dividend":                     DividendStrategy,
    "valuation":                    ValuationStrategy,
    "growth":                       GrowthStrategy,
    "low_position":                 LowPositionStrategy,
    "volume_surge":                 VolumeSurgeStrategy,
    "trend":                        TrendStrategy,
    "pattern":                      PatternStrategy,
    "bollinger":                    BollingerStrategy,
    "shareholder_concentration":    ShareholderConcentrationStrategy,
    "cashflow_quality":            CashflowQualityStrategy,
    "northbound_flow":              NorthboundFlowStrategy,
    "shareholder_buyback":         ShareholderBuybackStrategy,
    "analyst_target":              AnalystTargetStrategy,
}

ALL_STRATEGIES = list(STRATEGY_REGISTRY.keys())

# 策略中文名映射
STRATEGY_NAMES_CN = {
    "roe":                          "ROE盈利能力",
    "macd":                         "MACD底背离",
    "dividend":                     "高股息",
    "valuation":                    "低估值",
    "growth":                       "费雪成长股",
    "low_position":                 "长期低位",
    "volume_surge":                 "近期放量",
    "trend":                        "趋势分析",
    "pattern":                      "K线形态",
    "bollinger":                    "布林带下轨",
    "shareholder_concentration":    "筹码集中",
    "cashflow_quality":             "现金流质量",
    "northbound_flow":              "北向资金",
    "shareholder_buyback":          "股东增持",
    "analyst_target":               "分析师目标价",
}

# ── 日志 ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s [%(name)s] %(message)s"
)
logger = logging.getLogger("stock_screener")


# ══════════════════════════════════════════════════════════════════════
# 核心调度逻辑
# ══════════════════════════════════════════════════════════════════════

def _parse_strategies(strategy_str: str) -> List[str]:
    if strategy_str.strip().lower() == "all":
        return ALL_STRATEGIES
    names = [s.strip().lower() for s in strategy_str.split(",") if s.strip()]
    unknown = [n for n in names if n not in STRATEGY_REGISTRY]
    if unknown:
        raise ValueError(f"未知策略: {unknown}。可用: {ALL_STRATEGIES}")
    return names


def _extract_strategy_params(params: Dict, strategy_name: str) -> Dict:
    """从全局 params 中提取某策略的参数，支持 namespace 前缀"""
    result = {}
    for k, v in params.items():
        prefix = f"{strategy_name}."
        if k.startswith(prefix):
            result[k[len(prefix):]] = v
        elif "." not in k:     # 无前缀的通用参数透传给所有策略
            result[k] = v
    return result


def _run_single_strategy(name: str, params: Dict, limit: int = None) -> Dict:
    StrategyClass = STRATEGY_REGISTRY[name]
    strategy = StrategyClass()
    strategy_params = _extract_strategy_params(params, name)
    return strategy.run(strategy_params, limit=limit)


def _combine_and(results_map: Dict[str, Dict]) -> List[Dict]:
    """AND 模式：交集，按各策略得分之和排序"""
    if not results_map:
        return []
    code_sets = []
    code_to_results: Dict[str, Dict] = {}
    for strategy_name, res in results_map.items():
        codes = set()
        for r in res.get("results", []):
            code = r["ts_code"]
            codes.add(code)
            if code not in code_to_results:
                code_to_results[code] = {}
            code_to_results[code][strategy_name] = r
        code_sets.append(codes)

    intersection = code_sets[0].copy()
    for s in code_sets[1:]:
        intersection &= s

    combined = []
    for code in intersection:
        merged = {
            "ts_code": code,
            "strategies_hit": list(results_map.keys()),
            "scores": {},
        }
        for strategy_name, r in code_to_results[code].items():
            merged.setdefault("name", r.get("name", code))
            merged.setdefault("industry", r.get("industry", "未知"))
            merged["scores"][strategy_name] = r.get("score", 0)
            for k, v in r.items():
                if k not in ("ts_code", "name", "industry", "strategy"):
                    merged[f"{strategy_name}_{k}"] = v
        merged["total_score"] = sum(merged["scores"].values())
        merged["score"] = merged["total_score"]
        combined.append(merged)

    combined.sort(key=lambda x: x["total_score"], reverse=True)
    return combined


def _combine_or(results_map: Dict[str, Dict]) -> List[Dict]:
    """OR 模式：并集，去重，按命中策略数+总分排序"""
    all_codes: Dict[str, Dict] = {}
    for strategy_name, res in results_map.items():
        for r in res.get("results", []):
            code = r["ts_code"]
            if code not in all_codes:
                all_codes[code] = {
                    "ts_code": code,
                    "name": r.get("name", code),
                    "industry": r.get("industry", "未知"),
                    "strategies_hit": [],
                    "scores": {},
                    "score": 0,
                }
            all_codes[code]["strategies_hit"].append(strategy_name)
            all_codes[code]["scores"][strategy_name] = r.get("score", 0)
            all_codes[code]["score"] += r.get("score", 0)

    result = list(all_codes.values())
    result.sort(key=lambda x: (len(x["strategies_hit"]), x["score"]), reverse=True)
    return result


def _combine_score(results_map: Dict) -> List[Dict]:
    """SCORE 模式：综合评分，同 OR"""
    return _combine_or(results_map)


def _save_results(results: Dict, output_dir: str, generate_report: bool) -> Dict[str, str]:
    """保存 JSON + CSV，可选 HTML 报告"""
    if output_dir is None:
        output_dir = _CONFIG.get("output_dir") or _DEFAULT_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    strategies_label = "_".join(results.get("metadata", {}).get("strategies_used", ["unk"]))[:40]
    base = f"screener_{strategies_label}_{ts}"

    paths = {}
    # JSON
    json_path = os.path.join(output_dir, base + ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    paths["json"] = json_path

    # CSV
    try:
        import pandas as pd
        df = pd.DataFrame(results["results"])
        csv_path = os.path.join(output_dir, base + ".csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        paths["csv"] = csv_path
        print(f"[stock-selecter] CSV: {csv_path}")
    except Exception as e:
        print(f"[stock-selecter] CSV 保存失败: {e}")

    # HTML
    if generate_report:
        try:
            from utils.report import generate_html_report
            html_path = generate_html_report(results, output_dir)
            paths["html"] = html_path
        except Exception as e:
            print(f"[stock-selecter] HTML 报告生成失败: {e}")

    return paths


# ══════════════════════════════════════════════════════════════════════
# 公开接口
# ══════════════════════════════════════════════════════════════════════

def execute(params: Dict[str, Any] = None, limit: int = None) -> Dict[str, Any]:
    """
    统一选股技能入口

    关键参数：
      strategy (str)   : 策略名，逗号分隔或 'all'
      mode     (str)  : 组合模式 and / or / score（默认 and）
      top_n    (int)  : 最终截断数量（0=不限）
      save     (bool) : 是否保存文件（默认 True）
      workers  (int)  : 并发线程数（传入各策略，默认 1）
      report   (bool) : 是否生成 HTML 报告（默认 False）
      output_dir (str): 输出目录

    返回：
      {
        success: bool,
        results: [...],
        count: int,
        message: str,
        metadata: {...}
      }
    """
    params = params or {}
    start_time = time.time()

    strategy_str = str(params.get("strategy", "roe"))
    mode         = str(params.get("mode", "and")).lower()
    top_n        = int(params.get("top_n", 0))
    save         = params.get("save", True)
    generate_report = params.get("report", False)
    output_dir    = params.get("output_dir")

    if mode not in ("and", "or", "score"):
        mode = "and"

    try:
        strategy_names = _parse_strategies(strategy_str)
    except ValueError as e:
        return {
            "success": False, "results": [], "count": 0,
            "message": str(e),
            "metadata": {
                "strategies_used": [], "mode": mode,
                "execution_time": 0, "timestamp": datetime.now().isoformat()
            }
        }

    print(f"[stock-selecter] 策略: {strategy_names}  模式: {mode.upper()}")

    # ── 运行各策略 ──────────────────────────────────────────────
    results_map: Dict[str, Dict] = {}
    for name in strategy_names:
        t0 = time.time()
        print(f"[stock-selecter] >>> {STRATEGY_NAMES_CN.get(name, name)} [{name}]")
        results_map[name] = _run_single_strategy(name, params, limit)
        took = round(time.time() - t0, 1)
        cnt  = results_map[name].get("count", 0)
        print(f"[stock-selecter]     命中 {cnt} 只，耗时 {took}s")

    # ── 组合结果 ───────────────────────────────────────────────
    if len(strategy_names) == 1:
        final_results = results_map[strategy_names[0]].get("results", [])
    elif mode == "and":
        final_results = _combine_and(results_map)
    else:
        final_results = _combine_score(results_map)

    if top_n and top_n > 0:
        final_results = final_results[:top_n]

    elapsed = round(time.time() - start_time, 2)

    output = {
        "success": True,
        "results": final_results,
        "count": len(final_results),
        "message": (
            f"[stock-selecter] {mode.upper()} 模式，策略 {strategy_names}，"
            f"最终命中 {len(final_results)} 只，耗时 {elapsed}s"
        ),
        "metadata": {
            "strategies_used": strategy_names,
            "mode": mode,
            "execution_time": elapsed,
            "timestamp": datetime.now().isoformat(),
            "per_strategy_counts": {
                n: results_map[n].get("count", 0) for n in strategy_names
            },
        }
    }

    if save:
        paths = _save_results(output, output_dir, generate_report)
        output["metadata"]["saved_files"] = paths

    return output


# ══════════════════════════════════════════════════════════════════════
# 命令行入口
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="stock-selecter 统一选股技能",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
可用策略: {', '.join(ALL_STRATEGIES)}

示例:
  # 单策略 ROE 筛选（默认 AND 交集）
  python main.py --strategy roe --roe_threshold 15

  # ROE + MACD 双策略交集
  python main.py --strategy roe,macd --mode and

  # 并发执行（8线程）
  python main.py --strategy roe --workers 8

  # 全策略综合评分，取前50
  python main.py --strategy all --mode score --top 50

  # 生成 HTML 可视化报告
  python main.py --strategy roe,macd,dividend --report --output_dir ~/Desktop

  # 调试：限制每策略分析前20只
  python main.py --strategy roe --limit 20
        """
    )

    # 公共参数
    parser.add_argument("--strategy",  type=str, default="roe",
                         help="策略名，逗号分隔或 'all'")
    parser.add_argument("--mode",      type=str, default="and",
                         choices=["and", "or", "score"],
                         help="多策略组合模式（默认 and）")
    parser.add_argument("--top",       type=int, default=0,
                         help="最终结果数量上限（0=不限）")
    parser.add_argument("--limit",     type=int, default=0,
                         help="调试：限制每策略分析的股票数量")
    parser.add_argument("--workers",   type=int, default=1,
                         help="并发线程数（默认 1=串行）")
    parser.add_argument("--no_save",   action="store_true",
                         help="不保存结果")
    parser.add_argument("--report",    action="store_true",
                         help="生成 HTML 可视化报告")
    parser.add_argument("--output_dir", type=str,
                         help="输出目录（默认 /Volumes/Alan HD/股票筛选）")
    parser.add_argument("--verbose",   action="store_true",
                         help="显示详细日志")

    # 各策略参数（通用，不加前缀）
    parser.add_argument("--roe_threshold",         type=float)
    parser.add_argument("--roa_threshold",         type=float)
    parser.add_argument("--min_dv_ratio",           type=float)
    parser.add_argument("--min_consecutive_years",  type=int)
    parser.add_argument("--max_pe",                type=float)
    parser.add_argument("--max_pb",                type=float)
    parser.add_argument("--max_peg",               type=float)
    parser.add_argument("--min_revenue_growth",    type=float)
    parser.add_argument("--min_profit_growth",     type=float)
    parser.add_argument("--min_gross_margin",       type=float)
    parser.add_argument("--volume_surge_ratio",    type=float)
    parser.add_argument("--rsi_oversold",          type=float)
    parser.add_argument("--adx_min",               type=float)
    parser.add_argument("--trend_r2_min",          type=float)
    parser.add_argument("--min_pattern_score",      type=int)

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger("stock_screener").setLevel(logging.DEBUG)

    # 构造 params
    all_param_keys = [
        "roe_threshold", "roa_threshold", "min_dv_ratio", "min_consecutive_years",
        "max_pe", "max_pb", "max_peg", "min_revenue_growth", "min_profit_growth",
        "min_gross_margin", "volume_surge_ratio", "rsi_oversold",
        "adx_min", "trend_r2_min", "min_pattern_score",
    ]

    params = {
        "strategy":  args.strategy,
        "mode":      args.mode,
        "top_n":     args.top,
        "save":      not args.no_save,
        "report":    args.report,
        "output_dir": args.output_dir,
        "workers":   args.workers,
    }
    for key in all_param_keys:
        val = getattr(args, key, None)
        if val is not None:
            params[key] = val

    result = execute(params, limit=args.limit if args.limit > 0 else None)

    # ── 输出摘要 ───────────────────────────────────────────────
    print("\n" + "=" * 72)
    print(f"  stock-selecter 结果摘要")
    print("=" * 72)
    print(f"  状态   : {'✓ 成功' if result['success'] else '✗ 失败'}")
    print(f"  消息   : {result['message']}")
    meta = result.get("metadata", {})
    print(f"  策略   : {meta.get('strategies_used')}")
    print(f"  模式   : {meta.get('mode', '').upper()}")
    print(f"  耗时   : {meta.get('execution_time')}s")
    if "per_strategy_counts" in meta:
        print("  各策略命中数:")
        for k, v in meta["per_strategy_counts"].items():
            cn = STRATEGY_NAMES_CN.get(k, k)
            print(f"    {cn:<15} {v:>5} 只")
    print(f"  最终结果: {result['count']} 只")
    if "saved_files" in meta:
        print("  已保存:")
        for k, v in meta["saved_files"].items():
            print(f"    {k.upper()}: {v}")
    print("=" * 72)

    if result["success"] and result["results"]:
        items = result["results"][:20]
        print(f"\nTop {len(items)}（最多显示20条）:")
        print(f"{'#':<4} {'代码':<12} {'名称':<10} {'行业':<10} {'评分':<6} {'命中策略'}")
        print("-" * 68)
        for i, r in enumerate(items, 1):
            strategies = r.get("strategies_hit", [r.get("strategy", "?")])
            indus = r.get("industry", "")
            print(f"{i:<4} {r['ts_code']:<12} {r.get('name',''):<10} "
                  f"{indus[:8]:<10} {r.get('score', 0):<6.1f} {','.join(strategies)}")
