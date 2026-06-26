# -*- coding: utf-8 -*-
"""
Trading_Agents_for_Futures - 主入口

期货六维分析数据引擎。获取数据、计算指标、输出纯结构化 JSON。
零 API Key 依赖，纯本地规则引擎驱动。通过 AkShare 从公开平台获取行情数据。
"""

import argparse
import json
import logging
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Optional

SKILL_DIR = Path(__file__).resolve().parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from core.core_engine import CoreEngine, Config, has_real_indicators

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _sanitize(obj):
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    elif hasattr(obj, 'item'):
        v = obj.item()
        return None if v != v else v
    elif hasattr(obj, '__float__'):
        return float(obj)
    elif obj is None:
        return None
    elif isinstance(obj, (bool, int, float, str)):
        return obj
    else:
        return str(obj)


def _check_dependencies():
    """启动前检查关键依赖，缺失则提示用户手动安装"""
    missing = []
    for mod_name in ["akshare", "pyarrow", "pyyaml", "pandas", "numpy"]:
        pkg = "yaml" if mod_name == "pyyaml" else mod_name
        try:
            __import__(pkg)
        except ImportError:
            missing.append(mod_name)

    if not missing:
        return

    print(f"[错误] 缺少依赖: {', '.join(missing)}", file=sys.stderr)
    print("", file=sys.stderr)
    print("请先在虚拟环境中手动安装依赖:", file=sys.stderr)
    print(f"  python setup.py", file=sys.stderr)
    print(f"  或者: pip install -r requirements.txt", file=sys.stderr)
    print("", file=sys.stderr)
    print("为安全起见，本 skill 不会自动修改你的 Python 环境。", file=sys.stderr)
    sys.exit(1)


def _suppress_noise():
    """抑制 AkShare 等第三方库的噪音警告"""
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", message=".*非交易日.*")
    os.environ.setdefault("PYTHONWARNINGS", "ignore")


# ============================================================
#  AI Fillability 分级体系
# ============================================================
# Tier 1 (fillable):      AI 搜索可拿到可靠数据，可参与评分
# Tier 2 (direction_only): AI 只能拿到定性方向，降权参与评分
# Tier 3 (not_fillable):   AI 搜索拿不到精确数据，不可回填，维度保持 0 权重
# ============================================================

AI_FILL_SCHEMA = {
    "news_analysis": {
        "fillability": "fillable",
        "fillability_reason": "公开资讯充足，财经门户/交易所公告可直接获取多空事件",
        "max_confidence": 0.70,
        "ai_fill_weight_multiplier": 0.90,
        "fields": ["bullish_news_count", "bearish_news_count", "neutral_news_count",
                    "sentiment_ratio", "key_headlines"],
        "format": {
            "bullish_news_count": "number 利多新闻数",
            "bearish_news_count": "number 利空新闻数",
            "neutral_news_count": "number 中性新闻数",
            "sentiment_ratio": "number (bullish-bearish)/total",
            "key_headlines": "string[] 关键新闻标题列表（每条标注来源URL）",
        },
        "data_date": "YYYYMMDD 数据日期",
    },
    "basis_analysis": {
        "fillability": "fillable",
        "fillability_reason": "生意社/我的钢铁网/百川盈孚有公开现货报价，可推基差方向",
        "max_confidence": 0.60,
        "ai_fill_weight_multiplier": 0.75,
        "fields": ["spot_price", "futures_price", "basis_pct", "structure"],
        "cannot_fill": ["basis_zscore"],
        "cannot_fill_reason": "Z-score 依赖完整历史序列，AI 搜索无法重建，保持 null",
        "format": {
            "spot_price": "number 现货价格（标注来源）",
            "futures_price": "number 主力合约价格",
            "basis_pct": "number 基差率(%) = (futures-spot)/spot*100",
            "structure": '"contango"|"backwardation"|"flat"（从基差正负判断）',
        },
        "data_date": "YYYYMMDD 数据日期",
    },
    "inventory_analysis": {
        "fillability": "direction_only",
        "fillability_reason": "第三方有周度库存统计，可拿「增减方向」但无法重建历史 Z-score",
        "max_confidence": 0.45,
        "ai_fill_weight_multiplier": 0.50,
        "fields": ["latest_inventory", "inv_change_wow", "inv_change_mom"],
        "cannot_fill": ["inv_zscore", "latest_warehouse_receipt", "wr_change_5d"],
        "cannot_fill_reason": "Z-score/仓单精确值依赖交易所历史数据，AI 搜索不可重建",
        "format": {
            "latest_inventory": "number 库存量(吨)，标注来源和统计口径",
            "inv_change_wow": "number 周度变化率(%)，若不可得标近似值+unverified:true",
            "inv_change_mom": "number 月度变化率(%)，若不可得标近似值+unverified:true",
        },
        "data_date": "YYYYMMDD 数据日期",
    },
    "term_structure_analysis": {
        "fillability": "direction_only",
        "fillability_reason": "研报有定性描述但无原始价差数字，AI 可推断 contango/backwardation 方向，无法计算精确 spread_pct",
        "max_confidence": 0.30,
        "ai_fill_weight_multiplier": 0.30,
        "fields": ["structure", "structure_note"],
        "cannot_fill": ["contracts", "prices", "spread_pct", "front_price", "back_price"],
        "cannot_fill_reason": "合约价差精确数字仅交易所和付费终端有，AI 搜索不可得",
        "format": {
            "structure": '"contango"|"backwardation"|"flat"（从研报定性描述推断，必须标注来源）',
            "structure_note": "string 推断依据，如'某期货研报称远月贴水加深'",
        },
        "search_actions": [
            {"query": "{symbol} 期货 期限结构 contango backwardation 升贴水", "source": "web", "priority": "high"},
            {"query": "{symbol} 期货 研报 跨期价差 展期", "source": "research", "priority": "medium"},
        ],
        "data_date": "YYYYMMDD 数据日期",
    },
    "positioning_analysis": {
        "fillability": "direction_only",
        "fillability_reason": "会员持仓明细不公开，第三方只披露总量变化方向，AI 可推断资金流入/流出方向",
        "max_confidence": 0.30,
        "ai_fill_weight_multiplier": 0.30,
        "fields": ["oi_change_direction", "oi_change_note"],
        "cannot_fill": ["net_position", "net_change", "top20_long", "top20_short", "top20_long_pct", "key_players"],
        "cannot_fill_reason": "前20会员多空分项数据不公开，AI 无法区分谁加多谁加空",
        "format": {
            "oi_change_direction": '"increase"|"decrease"|"flat"（从第三方总持仓变化推断）',
            "oi_change_note": "string 推断依据，如'曲合数据显示JD总持仓环比+2.3%'",
        },
        "search_actions": [
            {"query": "{symbol} 期货 持仓 持仓量 增减 资金流向", "source": "web", "priority": "high"},
            {"query": "{symbol} 期货 前20会员 持仓排名", "source": "web", "priority": "medium"},
        ],
        "data_date": "YYYYMMDD 数据日期",
    },
}

SKILL_CN_MAP = {
    "technical_analysis": "技术面",
    "basis_analysis": "基差",
    "term_structure_analysis": "期限结构",
    "inventory_analysis": "库存仓单",
    "positioning_analysis": "持仓席位",
    "news_analysis": "新闻情绪",
}


def _build_gap_report(symbol: str, analysis_details: dict, warning_flags: list) -> dict:
    """生成数据缺口报告，按 fillability 分级，明确 AI 能补和不能补的维度"""
    gaps = []
    skill_order = ["technical_analysis", "basis_analysis", "term_structure_analysis",
                   "inventory_analysis", "positioning_analysis", "news_analysis"]

    for sk in skill_order:
        detail = analysis_details.get(sk, {})
        data_source = detail.get("data_source", "unknown")
        data_quality = detail.get("data_quality", "ok")
        status = detail.get("status", "")

        if status == "empty":
            gap_type = "api_unavailable"
        elif data_source in ("api_fallback",) or data_quality == "stale":
            gap_type = "stale_data"
        elif data_source in ("api_all_neutral", "insufficient") or data_quality in ("low_value", "insufficient"):
            gap_type = "low_quality"
        else:
            continue

        fill_schema = AI_FILL_SCHEMA.get(sk, {})
        fillability = fill_schema.get("fillability", "fillable")

        # 优先用 detail 的 search_actions，没有则从 schema 取并解析占位符
        search_actions = detail.get("search_actions", [])
        if not search_actions:
            schema_actions = fill_schema.get("search_actions", [])
            if schema_actions:
                search_actions = []
                for sa in schema_actions:
                    resolved = dict(sa)
                    if isinstance(resolved.get("query"), str):
                        resolved["query"] = resolved["query"].replace("{symbol}", symbol)
                    search_actions.append(resolved)
        if not search_actions:
            soft_hint = detail.get("soft_data_hint", "")
            search_actions = [{"query": soft_hint, "source": "hint_only"}] if soft_hint else []

        gap_entry = {
            "skill": sk,
            "skill_cn": SKILL_CN_MAP.get(sk, sk),
            "gap_type": gap_type,
            "fillability": fillability,
            "ai_fill_weight_multiplier": fill_schema.get("ai_fill_weight_multiplier", 0.0),
        }

        if fillability == "fillable":
            gap_entry["action"] = f"AI 搜索补全后参与评分（权重 ×{fill_schema.get('ai_fill_weight_multiplier', 0)}）"
            gap_entry["search_actions"] = search_actions
            gap_entry["ai_fill_schema"] = {
                "fields": fill_schema.get("fields", []),
                "format": fill_schema.get("format", {}),
                "cannot_fill": fill_schema.get("cannot_fill", []),
            }
            gap_entry["priority"] = "high"

        elif fillability == "direction_only":
            gap_entry["action"] = (
                f"AI 搜索仅补方向性信息（权重 ×{fill_schema.get('ai_fill_weight_multiplier', 0)}），"
                f"不参与历史分位计算"
            )
            gap_entry["search_actions"] = search_actions
            gap_entry["ai_fill_schema"] = {
                "fields": fill_schema.get("fields", []),
                "format": fill_schema.get("format", {}),
                "cannot_fill": fill_schema.get("cannot_fill", []),
                "cannot_fill_reason": fill_schema.get("cannot_fill_reason", ""),
            }
            gap_entry["priority"] = "medium"

        else:
            gap_entry["action"] = (
                f"该维度 AI 无法补全（{fill_schema.get('fillability_reason', '')}），"
                f"保持 weight=0，不参与 scoring"
            )
            gap_entry["search_actions"] = None
            gap_entry["ai_fill_schema"] = None
            gap_entry["can_infer"] = fill_schema.get("can_infer", {})
            gap_entry["fallback_action"] = fill_schema.get("fallback_action", "")
            gap_entry["priority"] = "info"

        gaps.append(gap_entry)

    fillable_count = sum(1 for g in gaps if g["fillability"] == "fillable")
    direction_only_count = sum(1 for g in gaps if g["fillability"] == "direction_only")
    not_fillable_count = sum(1 for g in gaps if g["fillability"] == "not_fillable")

    return {
        "total_gaps": len(gaps),
        "summary": {
            "fillable": fillable_count,
            "direction_only": direction_only_count,
            "not_fillable": not_fillable_count,
            "expected_recovery": fillable_count + direction_only_count,
            "permanent_loss": not_fillable_count,
        },
        "gaps": gaps,
        "instructions": (
            "每个 gap 都会尝试 AI 搜索补全，按 fillability 分级决定数据可信度：\n"
            "1. fillable (权重×0.75~0.90): 搜索补全后正常参与多空评分，可填充大部分字段\n"
            "2. direction_only (权重×0.30~0.50): 搜索补全但仅定性方向参与评分，cannot_fill 字段不要编造\n"
            "3. not_fillable (权重×0): 保留分类，当前版本所有维度都可尝试搜索"
        ),
    }


AI_FILL_TEMPLATE_DOC = """\
ai_fill 字段格式（AI Agent 回填时使用）:
{
  "filled_at": "2026-05-18T12:00:00",
  "source": "web_search",
  "search_queries_used": ["实际使用的搜索 query 1", "..."],
  "confidence": "high|medium|low",
  "fillability_tier": "fillable|direction_only",
  "weight_multiplier": 0.90,
  "data": {
    # 按 ai_fill_schema.fields 填充对应字段，
    # 每个数字标注来源URL，拿不准的标 "unverified": true
    # cannot_fill 中的字段不要填，保持缺失
  },
  "urls": ["来源URL1", "来源URL2"],
  "note": "AI Agent 的补充说明"
}

weight_multiplier 取值规则（从 data_gap_report.gaps[].ai_fill_weight_multiplier 复制）:
  fillable:      0.75 ~ 0.90（新闻 0.90, 基差 0.75）
  direction_only: 0.30（期限结构、持仓、库存方向）

警告:
- fillability=direction_only 的维度，只填 ai_fill_schema.fields 中的字段
  （如 term_structure 只填 structure，不要编造 spread_pct）
- 每个数字必须标注来源URL，不可编造
- weight_multiplier 必须从 data_gap_report 对应 gap 中复制

AI Agent 工作流:
1. 解析 output JSON 中的 data_gap_report
2. 对每个 gap，执行 search_actions 中的搜索
3. 按 ai_fill_schema 回填数据到对应 analysis_details[skill].ai_fill
4. weight_multiplier 从 gap 中复制到 ai_fill 对象
5. 将完整 JSON 保存为新文件，或交给后续决策流程
"""


def run_analysis(symbol: str, config_path: Optional[str] = None) -> dict:
    engine = CoreEngine(config_path=config_path, skill_dir=str(SKILL_DIR))
    analysis_results = engine.run_analysis(symbol=symbol.upper())

    analysis_details = {}
    coverage = {"total": 0, "available": 0, "missing": []}
    warning_flags = []

    for r in analysis_results:
        sk = r.skill_name
        coverage["total"] += 1
        indicators = r.data.get("indicators", {})
        soft_hint = indicators.get("soft_data_hint", "") if isinstance(indicators, dict) else ""
        data_date = r.data.get("data_date", None)
        fallback_date = indicators.get("fallback_date", "") if isinstance(indicators, dict) else ""

        if soft_hint:
            search_actions = indicators.get("search_actions", []) if isinstance(indicators, dict) else []
            flag_entry = {
                "skill": sk,
                "flag": "soft_data_hint",
                "hint": soft_hint,
                "severity": "warning",
            }
            if search_actions:
                flag_entry["search_actions"] = search_actions
            warning_flags.append(flag_entry)

        if indicators and has_real_indicators(indicators, soft_hint):
            entry = _sanitize(indicators)
            coverage["available"] += 1
            if data_date:
                entry["data_date"] = str(data_date)
            if isinstance(indicators, dict):
                if indicators.get("fallback_date") or indicators.get("data_source_note"):
                    entry["data_source"] = "api_fallback"
                    entry["data_quality"] = "stale"
                    if fallback_date:
                        warning_flags.append({
                            "skill": sk,
                            "flag": "stale_data",
                            "detail": f"回退数据日期: {fallback_date}",
                        })
                    # 回退数据也预留 ai_fill 槽位，鼓励 AI 验证
                    entry["ai_fill"] = None
                elif sk == "news_analysis":
                    q = indicators.get("quality", "unknown")
                    if q == "all_neutral":
                        entry["data_source"] = "api_all_neutral"
                        entry["data_quality"] = "low_value"
                        if "soft_data_hint" in indicators:
                            entry["soft_data_hint"] = indicators["soft_data_hint"]
                        entry["ai_fill"] = None
                    elif q in ("insufficient", "unavailable"):
                        entry["data_source"] = "insufficient"
                        entry["data_quality"] = "insufficient"
                        entry["note"] = indicators.get("note", "")
                        if "soft_data_hint" in indicators:
                            entry["soft_data_hint"] = indicators["soft_data_hint"]
                        entry["ai_fill"] = None
                    else:
                        entry["data_source"] = "api"
                else:
                    entry["data_source"] = "api"
            else:
                entry["data_source"] = "api"
            analysis_details[sk] = entry
        else:
            coverage["missing"].append(sk)
            search_actions = indicators.get("search_actions", []) if isinstance(indicators, dict) else []
            analysis_details[sk] = {
                "status": "empty",
                "data_source": "insufficient",
                "error": r.error,
                "ai_fill": None,
            }
            if soft_hint:
                analysis_details[sk]["soft_data_hint"] = soft_hint
            if search_actions:
                analysis_details[sk]["search_actions"] = search_actions

    # ---- 生成 data_gap_report ----
    data_gap_report = _build_gap_report(symbol.upper(), analysis_details, warning_flags)

    result = {
        "symbol": symbol.upper(),
        "timestamp": datetime.now().isoformat(),
        "success": True,
        "coverage": coverage,
        "analysis_details": analysis_details,
    }
    if warning_flags:
        result["warning_flags"] = warning_flags
    if data_gap_report["total_gaps"] > 0:
        result["data_gap_report"] = data_gap_report
    result = _sanitize(result)

    output_dir = Path(engine.config.get("project", "output_dir", default="output"))
    if not output_dir.is_absolute():
        output_dir = engine.config.skill_dir / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"data_{symbol.upper()}_{ts}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    logger.info(f"数据已保存: {output_file}")
    return result


def run_decision_mode(symbol: str, config_path: Optional[str] = None) -> dict:
    """运行完整决策流程：六维分析 → 多空辩论 → 风控评估 → CIO决策"""
    engine = CoreEngine(config_path=config_path, skill_dir=str(SKILL_DIR))
    decision = engine.run_full_pipeline(symbol=symbol.upper())

    result = _sanitize(decision.to_dict())
    result["symbol"] = symbol.upper()
    result["success"] = True
    result["mode"] = "decision"

    analysis_details = {}
    coverage = {"total": 0, "available": 0, "missing": []}
    warning_flags = []
    for r in decision.get_analysis_results():
        sk = r.skill_name
        coverage["total"] += 1
        indicators = r.data.get("indicators", {})
        soft_hint = indicators.get("soft_data_hint", "") if isinstance(indicators, dict) else ""
        fallback_date = indicators.get("fallback_date", "") if isinstance(indicators, dict) else ""

        if soft_hint:
            search_actions = indicators.get("search_actions", []) if isinstance(indicators, dict) else []
            flag_entry = {
                "skill": sk,
                "flag": "soft_data_hint",
                "hint": soft_hint,
                "severity": "warning",
            }
            if search_actions:
                flag_entry["search_actions"] = search_actions
            warning_flags.append(flag_entry)

        if indicators and has_real_indicators(indicators, soft_hint):
            coverage["available"] += 1
            entry = _sanitize(indicators)
            if fallback_date:
                entry["data_source"] = "api_fallback"
                entry["data_quality"] = "stale"
                entry["ai_fill"] = None
                warning_flags.append({
                    "skill": sk,
                    "flag": "stale_data",
                    "detail": f"回退数据日期: {fallback_date}",
                })
            elif sk == "news_analysis":
                q = indicators.get("quality", "unknown")
                if q == "all_neutral":
                    entry["data_source"] = "api_all_neutral"
                    entry["data_quality"] = "low_value"
                    entry["ai_fill"] = None
                    if "soft_data_hint" in indicators:
                        entry["soft_data_hint"] = indicators["soft_data_hint"]
                elif q in ("insufficient", "unavailable"):
                    entry["data_source"] = "insufficient"
                    entry["data_quality"] = "insufficient"
                    entry["ai_fill"] = None
                else:
                    entry["data_source"] = "api"
            else:
                entry["data_source"] = "api"
            analysis_details[sk] = entry
        else:
            coverage["missing"].append(sk)
            search_actions = indicators.get("search_actions", []) if isinstance(indicators, dict) else []
            analysis_details[sk] = {
                "status": "empty",
                "data_source": "insufficient",
                "ai_fill": None,
            }
            if soft_hint:
                analysis_details[sk]["soft_data_hint"] = soft_hint
            if search_actions:
                analysis_details[sk]["search_actions"] = search_actions
    result["coverage"] = coverage
    result["analysis_details"] = analysis_details
    if warning_flags:
        result["warning_flags"] = warning_flags

    data_gap_report = _build_gap_report(symbol.upper(), analysis_details, warning_flags)
    if data_gap_report["total_gaps"] > 0:
        result["data_gap_report"] = data_gap_report

    return result


def run_batch(symbols: list, config_path: Optional[str] = None, decision_mode: bool = False) -> list:
    """批量分析多个品种"""
    results = []
    for sym in symbols:
        try:
            if decision_mode:
                result = run_decision_mode(sym, config_path)
            else:
                result = run_analysis(sym, config_path)
            results.append(result)
        except Exception as e:
            logger.error(f"品种 {sym} 分析失败: {e}")
            results.append({"symbol": sym, "success": False, "error": str(e)})
    return results


DEFAULT_SYMBOLS = [
    "RB", "HC", "CU", "AL", "ZN", "NI", "SN", "AU", "AG",
    "I", "J", "JM", "M", "RM", "Y", "P", "CF", "SR",
    "MA", "TA", "PP", "L", "V", "RU", "SA", "FG", "SC", "FU",
    "LH", "C", "PG", "EB", "EG", "BU", "SS", "OI",
]


def main():
    _suppress_noise()
    _check_dependencies()

    parser = argparse.ArgumentParser(
        description="Trading_Agents_for_Futures - 期货六维分析数据引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py -s RB              # 分析螺纹钢，输出纯指标
  python main.py -s RB --decision    # 指标 + 辩论 + 风控 + CIO决策
  python main.py -s RB,CU,M         # 批量分析指定品种
  python main.py -s ALL             # 扫描全部 38 个品种
  python main.py -s RB -o out.json  # 额外输出到文件
  python main.py --list-skills      # 列出可用模块
        """,
    )
    parser.add_argument("-s", "--symbol", type=str, help="品种代码，多个用逗号分隔，或 ALL 扫描全部（如 CU,RB,M）")
    parser.add_argument("-c", "--config", type=str, default=None, help="自定义配置文件路径")
    parser.add_argument("--list-skills", action="store_true", default=False, help="列出可用分析模块")
    parser.add_argument("--log-level", type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--decision", action="store_true", default=False, help="运行完整决策流程（辩论+风控+CIO）")
    parser.add_argument("-o", "--output", type=str, default=None, help="额外输出 JSON 文件路径")

    args = parser.parse_args()
    setup_logging(args.log_level)

    if args.list_skills:
        engine = CoreEngine(skill_dir=str(SKILL_DIR))
        skills = engine.get_available_skills()
        print(json.dumps({"available_skills": skills}, ensure_ascii=False, indent=2))
        return

    if not args.symbol:
        parser.print_help()
        print("\n错误: 请使用 -s 参数指定品种代码")
        sys.exit(1)

    symbol_str = args.symbol.strip()
    if symbol_str.upper() == "ALL":
        symbols = DEFAULT_SYMBOLS
    else:
        symbols = [s.strip() for s in symbol_str.split(",")]

    logger.info(f"启动分析 | 品种: {symbols}")

    results = run_batch(symbols, args.config, decision_mode=args.decision)

    for r in results:
        if r.get("success"):
            print(json.dumps(_sanitize(r), ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"symbol": r.get("symbol"), "success": False, "error": r.get("error")}, ensure_ascii=False, indent=2))

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        logger.info(f"结果已保存: {output_path}")


if __name__ == "__main__":
    main()
