#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
daily_pipeline.py — 日常 Pipeline 运行器

根据当前时间自动判断运行哪个阶段(盘前 / 盘中 / 盘后),依次执行:
    1. 调用 data_fetcher 获取数据(行情/基本面/龙虎榜/北向/广度/板块)
    2. 使用 templates/ 中的模板生成报告
    3. 调用 risk_manager 进行风控检查
    4. 将报告输出到 reports/ 目录

支持命令行参数:
    --phase morning|intraday|evening|weekly|monthly   指定运行阶段
    --stock 600519                                    指定标的代码
    --config ./config.json                            指定配置文件
    --out ./reports                                   指定输出目录

用法示例:
    python3 daily_pipeline.py                          # 自动按时间判断阶段
    python3 daily_pipeline.py --phase morning --stock 600519
    python3 daily_pipeline.py --phase weekly
    python3 daily_pipeline.py --phase monthly --stock 000858
"""

from __future__ import annotations

import os
import sys
import json
import argparse
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

# 将脚本所在目录加入 sys.path,便于直接以脚本方式运行时导入同目录模块
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

# 导入同目录的 data_fetcher 与 risk_manager
from data_fetcher import DataFetcher  # noqa: E402
from risk_manager import (  # noqa: E402
    Position,
    run_all_checks,
    summarize_alerts,
    save_alerts,
    RiskAlert,
)

# ----------------------------------------------------------------------------
# 日志配置
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("daily_pipeline")

# 项目根目录(脚本目录的上一级)
_PROJECT_DIR = os.path.dirname(_SCRIPT_DIR)
_DEFAULT_CONFIG = os.path.join(_PROJECT_DIR, "config.json")
_DEFAULT_TEMPLATES = os.path.join(_PROJECT_DIR, "templates")
_DEFAULT_REPORTS = os.path.join(_PROJECT_DIR, "reports")

# 阶段定义
VALID_PHASES = ["morning", "intraday", "evening", "weekly", "monthly"]
PHASE_CN = {
    "morning": "盘前",
    "intraday": "盘中",
    "evening": "盘后",
    "weekly": "周报",
    "monthly": "月报",
}


# =============================================================================
# 配置加载
# =============================================================================

def load_config(config_path: str) -> Dict[str, Any]:
    """加载 config.json 配置文件,缺失时返回空字典。"""

    if not os.path.exists(config_path):
        logger.warning("配置文件不存在: %s,使用默认值", config_path)
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:  # noqa: BLE001
        logger.error("配置文件读取失败: %s", exc)
        return {}


# =============================================================================
# 阶段自动判断
# =============================================================================

def auto_detect_phase(cfg: Dict[str, Any]) -> str:
    """根据当前时间自动判断运行阶段。

    判断规则(可被 config.json 的 pipeline.phases 段覆盖):
        - pre_market_end(默认 09:15)之前         -> morning(盘前)
        - pre_market_end ~ post_market_start      -> intraday(盘中)
        - post_market_start(默认 15:00)之后       -> evening(盘后)

    Args:
        cfg: 配置字典。

    Returns:
        阶段名称(morning / intraday / evening)。
    """

    now = datetime.now()
    pipeline_cfg = cfg.get("pipeline", {}) if cfg else {}
    phases = pipeline_cfg.get("phases", {}) if pipeline_cfg else {}
    # 盘前结束(pre_market_end)之前为盘前;盘后开始(post_market_start)之后为盘后
    morning_t = _parse_hhmm(phases.get("pre_market_end", "09:15"))
    evening_t = _parse_hhmm(phases.get("post_market_start", "15:00"))

    cur = now.hour * 60 + now.minute
    if cur < morning_t:
        return "morning"
    if cur < evening_t:
        return "intraday"
    return "evening"


def _parse_hhmm(text: str) -> int:
    """将 "HH:MM" 转换为当日分钟数,失败返回 0。"""

    try:
        hh, mm = str(text).split(":")
        return int(hh) * 60 + int(mm)
    except Exception:  # noqa: BLE001
        return 0


# =============================================================================
# 数据采集
# =============================================================================

def collect_market_data(
    fetcher: DataFetcher,
    stock_code: str,
    phase: str,
) -> Dict[str, Any]:
    """调用 data_fetcher 采集本阶段所需数据。

    Args:
        fetcher:     DataFetcher 实例。
        stock_code:  目标股票代码。
        phase:       运行阶段。

    Returns:
        包含各数据项的字典。
    """

    logger.info("开始采集数据(阶段=%s, 标的=%s)", phase, stock_code)
    today = datetime.now().strftime("%Y%m%d")
    # 周/月报使用更早的起始日
    if phase == "weekly":
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
    elif phase == "monthly":
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
    else:
        start_date = today

    data: Dict[str, Any] = {
        "stock_code": stock_code,
        "phase": phase,
        "date": today,
        "start_date": start_date,
    }

    # 实时行情 / 基本面
    data["quote"] = fetcher.get_realtime_quote(stock_code)
    data["fundamentals"] = fetcher.get_stock_fundamentals(stock_code)

    # 盘中关注广度与板块轮动
    if phase in ("intraday", "evening"):
        data["breadth"] = fetcher.get_market_breadth()
        data["sector_rotation"] = fetcher.get_sector_rotation()

    # 盘后 / 周报 / 月报关注龙虎榜与北向资金
    if phase in ("evening", "weekly", "monthly"):
        data["dragon_tiger"] = fetcher.get_dragon_tiger_list(today)
        data["north_flow"] = fetcher.get_north_flow(today)

    # 月报额外拉取财务报表
    if phase == "monthly":
        data["financial_report"] = fetcher.get_financial_report(
            stock_code, report_type="income"
        )

    logger.info("数据采集完成")
    return data


# =============================================================================
# 风控检查
# =============================================================================

def run_risk_checks(
    market_data: Dict[str, Any],
    cfg: Dict[str, Any],
) -> List[RiskAlert]:
    """基于市场数据构造持仓并运行风控检查。

    为演示完整性,这里以目标标的构造一个虚拟持仓(基于 config 中持仓配置,
    若无则用行情价格构造)进行风控检查。

    Args:
        market_data: 采集到的市场数据。
        cfg:         配置字典。

    Returns:
        风控告警列表。
    """

    quote = market_data.get("quote", {}) or {}
    stock_code = market_data.get("stock_code", "")
    price = float(quote.get("price", 0) or 0)
    change_pct = float(quote.get("change_pct", 0) or 0)

    # 从 config 读取持仓配置(若有),否则用默认虚拟持仓
    holdings = cfg.get("holdings", [])
    if not holdings:
        holdings = [
            {
                "stock_code": stock_code,
                "name": quote.get("name", ""),
                "cost_price": round(price * 1.05, 2) if price else 0.0,
                "current_price": price,
                "volume": 100,
                "industry": quote.get("industry", "未知"),
                "pnl_pct": -0.05 if price else 0.0,
            }
        ]

    portfolio = [
        Position(
            stock_code=h.get("stock_code", ""),
            name=h.get("name", ""),
            cost_price=float(h.get("cost_price", 0) or 0),
            current_price=float(h.get("current_price", 0) or 0),
            volume=int(h.get("volume", 0) or 0),
            industry=h.get("industry", ""),
            pnl_pct=float(h.get("pnl_pct", 0) or 0),
        )
        for h in holdings
    ]

    # 情绪分数:用市场广度推算一个简易情绪分数
    sentiment = _estimate_sentiment(market_data)

    # 从 config.json 的 risk_control.rules 读取阈值(对应 references/risk_rules.md)
    # 未配置时回退到 run_all_checks 的函数默认值(即用户指定的默认阈值)
    rc_rules = ((cfg.get("risk_control") or {}).get("rules")) or {}

    def _to_frac(val: Any, default: float) -> float:
        """百分比数值转小数(如 -5.0 -> -0.05, 30.0 -> 0.30);非法值返回默认。"""
        try:
            f = float(val)
        except (TypeError, ValueError):
            return default
        return f / 100.0 if abs(f) > 1.0 else f

    single_stop = _to_frac((rc_rules.get("stop_loss") or {}).get("threshold_pct"), -0.05)
    port_stop = _to_frac((rc_rules.get("portfolio_stop_loss") or {}).get("threshold_pct"), -0.08)
    pos_max = _to_frac((rc_rules.get("single_position_limit") or {}).get("threshold_pct"), 0.30)
    ind_max = _to_frac((rc_rules.get("industry_concentration_limit") or {}).get("threshold_pct"), 0.40)

    alerts = run_all_checks(
        portfolio=portfolio,
        market_data=market_data,
        sentiment_score=sentiment,
        single_stop_threshold=single_stop,
        portfolio_stop_threshold=port_stop,
        position_max_pct=pos_max,
        industry_max_pct=ind_max,
    )
    logger.info("风控检查完成,告警数=%d", len(alerts))
    return alerts


def _estimate_sentiment(market_data: Dict[str, Any]) -> Optional[float]:
    """根据市场涨跌家数估算情绪分数(0-100)。

    涨家数占比越高,情绪越乐观。
    """

    breadth = market_data.get("breadth", {}) or {}
    advance = float(breadth.get("advance", 0) or 0)
    decline = float(breadth.get("decline", 0) or 0)
    total = advance + decline
    if total <= 0:
        return None
    return round(advance / total * 100.0, 1)


# =============================================================================
# 报告生成
# =============================================================================

def render_report(
    market_data: Dict[str, Any],
    alerts: List[RiskAlert],
    phase: str,
    templates_dir: str,
) -> str:
    """使用模板渲染 Markdown 报告。

    优先使用 templates/daily_report.md;若不存在则使用内置模板。

    Args:
        market_data: 市场数据。
        alerts:      风控告警列表。
        phase:       阶段。
        templates_dir: 模板目录。

    Returns:
        渲染后的 Markdown 字符串。
    """

    template_path = os.path.join(templates_dir, "daily_report.md")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    else:
        logger.warning("模板不存在: %s,使用内置模板", template_path)
        template = _BUILTIN_TEMPLATE

    quote = market_data.get("quote", {}) or {}
    fund = market_data.get("fundamentals", {}) or {}
    breadth = market_data.get("breadth", {}) or {}
    north = market_data.get("north_flow", {}) or {}
    sector = market_data.get("sector_rotation", {}) or {}
    dragon = market_data.get("dragon_tiger", {}) or {}

    sectors_text = "\n".join(
        f"  - {s.get('name', '')}: {s.get('change_pct', 0):.2f}%"
        for s in (sector.get("sectors", []) or [])[:10]
    ) or "  无数据"
    dragon_text = (
        f"  龙虎榜条目数: {len(dragon.get('items', []) or [])}"
        if dragon else "  无数据"
    )

    fields = {
        "report_title": f"超级股票交易 {PHASE_CN.get(phase, phase)}报告",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "phase": PHASE_CN.get(phase, phase),
        "stock_code": market_data.get("stock_code", ""),
        "sh_index": "—",
        "sz_index": "—",
        "cyb_index": "—",
        "breadth": (
            f"涨 {breadth.get('advance', '—')} / 跌 {breadth.get('decline', '—')} / "
            f"平 {breadth.get('flat', '—')}"
            if breadth else "—"
        ),
        "north_flow": (
            f"{north.get('net_buy', '—')} 元"
            if north else "—"
        ),
        "realtime_price": quote.get("price", "—"),
        "change_pct": f"{quote.get('change_pct', 0) * 100:.2f}%" if quote else "—",
        "volume": quote.get("volume", "—"),
        "fundamentals": (
            f"PE={fund.get('pe', '—')} PB={fund.get('pb', '—')} "
            f"市值={fund.get('total_mv', '—')}"
            if fund else "—"
        ),
        "dragon_tiger": dragon_text,
        "sector_rotation": sectors_text,
        "risk_check_summary": summarize_alerts(alerts),
        "suggestion": _build_suggestion(alerts, phase),
    }

    # 简易模板替换:支持 {{key}}
    rendered = template
    for key, val in fields.items():
        rendered = rendered.replace("{{" + key + "}}", str(val))
    return rendered


def _build_suggestion(alerts: List[RiskAlert], phase: str) -> str:
    """根据风控告警与阶段生成操作建议。"""

    if not alerts:
        return f"{PHASE_CN.get(phase, phase)}无风控告警,可按既定计划执行。"
    has_block = any(a.level.value == "block" for a in alerts)
    has_danger = any(a.level.value == "danger" for a in alerts)
    if has_block:
        return "存在阻断级告警(杠杆/连续亏损),建议暂停下单,复核交易计划。"
    if has_danger:
        return "存在危险级告警(止损/集中度),建议减仓降风险,谨慎操作。"
    return "存在警告级告警,建议持续监控,控制仓位。"


# 内置模板(当 templates/daily_report.md 不存在时使用)
_BUILTIN_TEMPLATE = """# {{report_title}}

> 生成时间: {{generated_at}} | 阶段: {{phase}} | 标的: {{stock_code}}

## 一、市场概览
- 市场涨跌家数: {{breadth}}
- 北向资金净流入: {{north_flow}}

## 二、标的分析 ({{stock_code}})
- 实时价格: {{realtime_price}}
- 涨跌幅: {{change_pct}}
- 成交量: {{volume}}
- 基本面摘要: {{fundamentals}}

## 三、龙虎榜 / 板块轮动
{{dragon_tiger}}
{{sector_rotation}}

## 四、风控检查结果
{{risk_check_summary}}

## 五、操作建议
{{suggestion}}

---
*本报告由 daily_pipeline.py 自动生成,仅供参考,不构成投资建议。*
"""


# =============================================================================
# 报告输出
# =============================================================================

def save_report(
    content: str,
    phase: str,
    stock_code: str,
    reports_dir: str,
) -> str:
    """将报告写入 reports/ 目录,返回文件路径。

    文件名格式: report_<phase>_<stock>_<YYYYMMDD_HHMMSS>.md
    """

    os.makedirs(reports_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{phase}_{stock_code}_{ts}.md"
    path = os.path.join(reports_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info("报告已保存: %s", path)
    return path


def save_raw_data(
    market_data: Dict[str, Any],
    phase: str,
    stock_code: str,
    reports_dir: str,
) -> str:
    """将原始市场数据以 JSON 形式保存,便于回溯。"""

    os.makedirs(reports_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_{phase}_{stock_code}_{ts}.json"
    path = os.path.join(reports_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(market_data, f, ensure_ascii=False, indent=2, default=str)
    return path


# =============================================================================
# Pipeline 主流程
# =============================================================================

def run_pipeline(
    phase: Optional[str],
    stock_code: str,
    config_path: str,
    reports_dir: str,
    templates_dir: str,
) -> Dict[str, str]:
    """执行完整 Pipeline:采集 -> 风控 -> 渲染 -> 输出。

    Args:
        phase:        指定阶段;为 None 时自动判断。
        stock_code:   目标股票代码。
        config_path:  配置文件路径。
        reports_dir:  报告输出目录。
        templates_dir:模板目录。

    Returns:
        包含 report_path / data_path / phase 的字典。
    """

    cfg = load_config(config_path)

    # 阶段判断
    if not phase:
        phase = auto_detect_phase(cfg)
    logger.info("运行阶段: %s (%s)", phase, PHASE_CN.get(phase, ""))

    # 数据源: 读取 api_keys,过滤占位符,并尊重 use_env_override(环境变量优先)
    api_cfg = cfg.get("api_keys", {}) if cfg else {}
    use_env = bool(api_cfg.get("use_env_override", True))

    def _clean_key(val: Any) -> str:
        """剔除占位符(含 YOUR_ / PLACEHOLDER)的密钥值。"""
        s = "" if val is None else str(val)
        if "YOUR_" in s or "PLACEHOLDER" in s:
            return ""
        return s

    wind_key = _clean_key(api_cfg.get("wind_api_key", ""))
    tushare_tok = _clean_key(api_cfg.get("tushare_token", ""))
    if use_env:
        wind_key = os.environ.get("WIND_API_KEY", "") or wind_key
        tushare_tok = os.environ.get("TUSHARE_TOKEN", "") or tushare_tok

    # 缓存目录: 从 pipeline.cache_dir 读取,相对路径基于项目根目录
    pipeline_cfg = cfg.get("pipeline", {}) if cfg else {}
    cache_dir = pipeline_cfg.get("cache_dir", "")
    if cache_dir and not os.path.isabs(cache_dir):
        cache_dir = os.path.normpath(os.path.join(_PROJECT_DIR, cache_dir))

    fetcher = DataFetcher(
        wind_api_key=wind_key,
        tushare_token=tushare_tok,
        cache_dir=cache_dir,
    )

    # 1. 采集数据
    market_data = collect_market_data(fetcher, stock_code, phase)

    # 2. 风控检查
    alerts = run_risk_checks(market_data, cfg)

    # 3. 渲染报告
    report_md = render_report(market_data, alerts, phase, templates_dir)

    # 4. 输出
    report_path = save_report(report_md, phase, stock_code, reports_dir)
    data_path = save_raw_data(market_data, phase, stock_code, reports_dir)

    # 风控告警单独保存
    alert_path = os.path.join(reports_dir, os.path.basename(report_path).replace("report_", "alerts_").replace(".md", ".json"))
    save_alerts(alerts, alert_path)

    # 控制台摘要
    print("\n" + "=" * 60)
    print(f"  Pipeline 完成 — 阶段: {PHASE_CN.get(phase, phase)}")
    print("=" * 60)
    print(f"  标的:     {stock_code}")
    print(f"  报告:     {report_path}")
    print(f"  原始数据: {data_path}")
    print(f"  风控告警: {alert_path} ({len(alerts)} 条)")
    print("=" * 60 + "\n")

    return {
        "phase": phase,
        "report_path": report_path,
        "data_path": data_path,
        "alerts_path": alert_path,
        "alerts_count": str(len(alerts)),
    }


# =============================================================================
# 命令行入口
# =============================================================================

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(
        description="超级股票交易 Skill — 日常 Pipeline 运行器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python3 daily_pipeline.py --phase morning --stock 600519\n"
               "  python3 daily_pipeline.py --phase weekly\n"
               "  python3 daily_pipeline.py --phase monthly --stock 000858\n",
    )
    parser.add_argument(
        "--phase", "-p",
        choices=VALID_PHASES,
        default=None,
        help="运行阶段(morning/intraday/evening/weekly/monthly);不指定则按当前时间自动判断",
    )
    parser.add_argument(
        "--stock", "-s",
        default="",
        help="目标股票代码(默认从 config.json 读取 pipeline.default_stock)",
    )
    parser.add_argument(
        "--config", "-c",
        default=_DEFAULT_CONFIG,
        help=f"配置文件路径(默认: {_DEFAULT_CONFIG})",
    )
    parser.add_argument(
        "--out", "-o",
        default=_DEFAULT_REPORTS,
        help=f"报告输出目录(默认: {_DEFAULT_REPORTS})",
    )
    parser.add_argument(
        "--templates",
        default=_DEFAULT_TEMPLATES,
        help=f"模板目录(默认: {_DEFAULT_TEMPLATES})",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """主函数入口。"""

    args = parse_args(argv)

    # 标的:命令行 > config > 默认
    cfg = load_config(args.config)
    stock_code = args.stock or (
        cfg.get("pipeline", {}).get("default_stock", "600519")
    )

    try:
        result = run_pipeline(
            phase=args.phase,
            stock_code=stock_code,
            config_path=args.config,
            reports_dir=args.out,
            templates_dir=args.templates,
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Pipeline 执行失败: %s", exc)
        return 1

    # 退出码:存在阻断级告警时返回 2,供调度系统识别
    if int(result.get("alerts_count", 0)) > 0:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
