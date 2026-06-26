#!/usr/bin/env python3
"""资源位转化数据波动分析工具

使用连环替代法（Sequential Substitution）对资源位漏斗数据进行因子分解，
输出 Markdown 格式的波动归因分析报告。

Usage:
    python analyze.py data.xlsx --mode dod --date 2026-03-25
    python analyze.py data.xlsx --mode wow --date 2026-03-25
    python analyze.py data.xlsx --mode custom --base-start 2026-03-18 --base-end 2026-03-24 \
        --compare-start 2026-03-11 --compare-end 2026-03-17
"""

import argparse
import subprocess
import sys
from datetime import datetime, timedelta


def _ensure_deps():
    """Check and auto-install missing dependencies."""
    missing = []
    try:
        import pandas  # noqa: F401
    except ImportError:
        missing.append("pandas")
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        missing.append("openpyxl")
    if missing:
        print(f"正在安装缺失依赖: {', '.join(missing)} ...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet"] + missing,
        )


_ensure_deps()

import pandas as pd  # noqa: E402


COLUMN_ALIASES = {
    "日期": "date",
    "date": "date",
    "资源位": "resource_position",
    "资源位名称": "resource_position",
    "位置": "resource_position",
    "resource_position": "resource_position",
    "曝光UV": "exposure_uv",
    "曝光人数": "exposure_uv",
    "exposure_uv": "exposure_uv",
    "点击UV": "click_uv",
    "点击人数": "click_uv",
    "click_uv": "click_uv",
    "转化量": "conversion_count",
    "业务转化量": "conversion_count",
    "转化数": "conversion_count",
    "conversion_count": "conversion_count",
    "曝光PV": "exposure_pv",
    "exposure_pv": "exposure_pv",
    "点击PV": "click_pv",
    "click_pv": "click_pv",
}

REQUIRED_COLUMNS = ["date", "resource_position", "exposure_uv", "click_uv", "conversion_count"]

RECOMMENDATION_MAP = {
    ("exposure", "down"): "排查流量分配策略，检查资源位是否因页面改版/AB实验导致可见性降低，确认是否有大盘流量波动",
    ("exposure", "up"): "关注新增流量质量，观察CTR/CVR是否同步提升；如CTR/CVR下降，需排查流量精准度",
    ("ctr", "down"): "检查素材创意是否需要更新（用户疲劳度），排查资源位位置/样式是否有变动，建议启动AB测试对比新素材",
    ("ctr", "up"): "沉淀当前有效素材策略，评估是否可复用到同类型资源位，持续监控后续趋势稳定性",
    ("cvr", "down"): "排查落地页加载速度与交互体验，检查业务流程是否有卡点（如新增验证步骤），分析目标人群画像是否发生偏移",
    ("cvr", "up"): "分析转化率提升的具体原因（活动策略/流程优化/人群变化），评估提升是否可持续和可规模化",
}


def read_and_normalize(file_path: str) -> pd.DataFrame:
    """读取 Excel 并统一列名"""
    df = pd.read_excel(file_path)
    rename_map = {}
    for col in df.columns:
        col_stripped = str(col).strip()
        if col_stripped in COLUMN_ALIASES:
            rename_map[col] = COLUMN_ALIASES[col_stripped]
    df = df.rename(columns=rename_map)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        print(f"错误：缺少必需列: {', '.join(missing)}", file=sys.stderr)
        print(f"当前列: {', '.join(df.columns.tolist())}", file=sys.stderr)
        sys.exit(1)

    df["date"] = pd.to_datetime(df["date"])
    return df


def compute_period_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """按资源位聚合并计算衍生指标"""
    grouped = df.groupby("resource_position").agg(
        exposure_uv=("exposure_uv", "sum"),
        click_uv=("click_uv", "sum"),
        conversion_count=("conversion_count", "sum"),
    ).reset_index()

    grouped["ctr"] = grouped["click_uv"] / grouped["exposure_uv"].replace(0, float("nan"))
    grouped["cvr"] = grouped["conversion_count"] / grouped["click_uv"].replace(0, float("nan"))
    grouped["overall_rate"] = grouped["conversion_count"] / grouped["exposure_uv"].replace(0, float("nan"))
    return grouped


def factor_decomposition(base: pd.Series, compare: pd.Series) -> dict:
    """连环替代法因子分解

    base = 本期（当前/目标日期），compare = 上期（对比日期）
    公式: Conversion = Exposure × CTR × CVR
    变化方向: 本期 - 上期（正数=上升，负数=下降）
    固定替代顺序: 曝光 → CTR → CVR
    """
    exp_curr = base["exposure_uv"]
    ctr_curr = base["ctr"]
    cvr_curr = base["cvr"]
    exp_prev = compare["exposure_uv"]
    ctr_prev = compare["ctr"]
    cvr_prev = compare["cvr"]

    conv_curr = exp_curr * ctr_curr * cvr_curr
    conv_prev = exp_prev * ctr_prev * cvr_prev
    delta = conv_curr - conv_prev

    exposure_effect = (exp_curr - exp_prev) * ctr_prev * cvr_prev
    ctr_effect = exp_curr * (ctr_curr - ctr_prev) * cvr_prev
    cvr_effect = exp_curr * ctr_curr * (cvr_curr - cvr_prev)

    if abs(delta) > 0.5:
        exposure_pct = exposure_effect / delta * 100
        ctr_pct = ctr_effect / delta * 100
        cvr_pct = cvr_effect / delta * 100
    else:
        exposure_pct = ctr_pct = cvr_pct = 0.0

    abs_effects = [abs(exposure_pct), abs(ctr_pct), abs(cvr_pct)]
    factors = ["exposure", "ctr", "cvr"]
    factor_labels = ["曝光变化", "CTR变化", "CVR变化"]
    main_idx = abs_effects.index(max(abs_effects))

    return {
        "conv_base": conv_curr,
        "conv_compare": conv_prev,
        "delta": delta,
        "delta_pct": (delta / conv_prev * 100) if conv_prev != 0 else 0,
        "exposure_effect": exposure_effect,
        "ctr_effect": ctr_effect,
        "cvr_effect": cvr_effect,
        "exposure_pct": exposure_pct,
        "ctr_pct": ctr_pct,
        "cvr_pct": cvr_pct,
        "main_factor": factors[main_idx],
        "main_factor_label": factor_labels[main_idx],
        "main_factor_direction": "up" if [exposure_effect, ctr_effect, cvr_effect][main_idx] > 0 else "down",
    }


def get_periods(args) -> tuple:
    """根据模式计算基准期和对比期日期范围"""
    if args.mode == "dod":
        target = pd.to_datetime(args.date)
        return (target, target), (target - timedelta(days=1), target - timedelta(days=1))
    elif args.mode == "wow":
        target = pd.to_datetime(args.date)
        return (target, target), (target - timedelta(days=7), target - timedelta(days=7))
    elif args.mode == "custom":
        return (
            (pd.to_datetime(args.base_start), pd.to_datetime(args.base_end)),
            (pd.to_datetime(args.compare_start), pd.to_datetime(args.compare_end)),
        )
    else:
        print(f"错误：未知模式 {args.mode}", file=sys.stderr)
        sys.exit(1)


def fmt_num(n, decimals=0):
    if pd.isna(n):
        return "-"
    if decimals == 0:
        return f"{int(round(n)):,}"
    return f"{n:,.{decimals}f}"


def fmt_pct(n, decimals=2):
    if pd.isna(n):
        return "-"
    return f"{n:.{decimals}f}%"


def fmt_pp(n, decimals=2):
    """格式化百分点变化"""
    if pd.isna(n):
        return "-"
    sign = "+" if n > 0 else ""
    return f"{sign}{n * 100:.{decimals}f}pp"


def fmt_change(n, decimals=0):
    if pd.isna(n):
        return "-"
    sign = "+" if n > 0 else ""
    if decimals == 0:
        return f"{sign}{int(round(n)):,}"
    return f"{sign}{n:,.{decimals}f}"


def get_main_factor_tag(pct):
    abs_pct = abs(pct)
    if abs_pct >= 50:
        return "**主因**"
    elif abs_pct >= 20:
        return "次因"
    else:
        return "微弱"


def generate_report(
    base_metrics: pd.DataFrame,
    compare_metrics: pd.DataFrame,
    decompositions: dict,
    base_period: tuple,
    compare_period: tuple,
    mode: str,
):
    """生成 Markdown 分析报告"""
    lines = []

    mode_labels = {"dod": "日环比", "wow": "周同比", "custom": "自定义区间"}
    base_label = _period_label(base_period)
    compare_label = _period_label(compare_period)

    lines.append("# 资源位转化数据波动分析报告\n")
    lines.append(f"> 分析模式: {mode_labels.get(mode, mode)} | "
                 f"本期: {base_label} | 上期: {compare_label}\n")
    lines.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    positions = sorted(decompositions.keys())

    # --- 数据概览 ---
    lines.append("## 一、数据概览\n")
    for pos in positions:
        base_row = base_metrics[base_metrics["resource_position"] == pos].iloc[0]
        comp_row = compare_metrics[compare_metrics["resource_position"] == pos].iloc[0]

        lines.append(f"### {pos}\n")
        lines.append("| 指标 | 本期 | 上期 | 变化量 | 变化率 |")
        lines.append("|------|------|------|--------|--------|")

        rows_data = [
            ("曝光UV", base_row["exposure_uv"], comp_row["exposure_uv"], False),
            ("点击UV", base_row["click_uv"], comp_row["click_uv"], False),
            ("CTR", base_row["ctr"], comp_row["ctr"], True),
            ("业务转化量", base_row["conversion_count"], comp_row["conversion_count"], False),
            ("CVR", base_row["cvr"], comp_row["cvr"], True),
            ("整体转化率", base_row["overall_rate"], comp_row["overall_rate"], True),
        ]

        for label, b_val, c_val, is_rate in rows_data:
            if is_rate:
                lines.append(
                    f"| {label} | {fmt_pct(b_val * 100)} | {fmt_pct(c_val * 100)} | "
                    f"{fmt_pp(b_val - c_val)} | - |"
                )
            else:
                change = b_val - c_val
                change_pct = (change / c_val * 100) if c_val != 0 else 0
                lines.append(
                    f"| {label} | {fmt_num(b_val)} | {fmt_num(c_val)} | "
                    f"{fmt_change(change)} | {fmt_change(change_pct, 1)}% |"
                )
        lines.append("")

    # --- 波动归因 ---
    lines.append("## 二、波动归因分析\n")
    for pos in positions:
        d = decompositions[pos]
        lines.append(f"### {pos}\n")

        if abs(d["delta"]) < 1:
            lines.append("> 波动极小（变化量 < 1），无需归因分析。\n")
            continue

        lines.append(f"业务转化量变化: {fmt_change(d['delta'])} ({fmt_change(d['delta_pct'], 1)}%)\n")
        lines.append("| 因素 | 贡献量 | 贡献占比 | 判定 |")
        lines.append("|------|--------|----------|------|")
        lines.append(
            f"| 曝光变化 | {fmt_change(d['exposure_effect'], 1)} | "
            f"{fmt_pct(d['exposure_pct'])} | {get_main_factor_tag(d['exposure_pct'])} |"
        )
        lines.append(
            f"| CTR变化 | {fmt_change(d['ctr_effect'], 1)} | "
            f"{fmt_pct(d['ctr_pct'])} | {get_main_factor_tag(d['ctr_pct'])} |"
        )
        lines.append(
            f"| CVR变化 | {fmt_change(d['cvr_effect'], 1)} | "
            f"{fmt_pct(d['cvr_pct'])} | {get_main_factor_tag(d['cvr_pct'])} |"
        )
        lines.append("")

    # --- 多资源位对比 ---
    if len(positions) > 1:
        lines.append("## 三、多资源位横向对比\n")
        lines.append("| 资源位 | 转化变化量 | 转化变化率 | 主要波动因素 | 方向 |")
        lines.append("|--------|-----------|-----------|-------------|------|")
        for pos in positions:
            d = decompositions[pos]
            direction = "↑" if d["delta"] > 0 else ("↓" if d["delta"] < 0 else "→")
            lines.append(
                f"| {pos} | {fmt_change(d['delta'])} | {fmt_change(d['delta_pct'], 1)}% | "
                f"{d['main_factor_label']} | {direction} |"
            )
        lines.append("")

    # --- 关键发现 ---
    lines.append("## 四、关键发现\n")
    findings = _generate_findings(decompositions, base_metrics, compare_metrics)
    for i, finding in enumerate(findings, 1):
        lines.append(f"{i}. {finding}")
    lines.append("")

    # --- 建议 ---
    lines.append("## 五、后续建议\n")
    recommendations = _generate_recommendations(decompositions)
    for i, rec in enumerate(recommendations, 1):
        lines.append(f"{i}. {rec}")
    lines.append("")

    return "\n".join(lines)


def _period_label(period: tuple) -> str:
    start, end = period
    if start == end:
        return start.strftime("%Y-%m-%d")
    return f"{start.strftime('%Y-%m-%d')} ~ {end.strftime('%Y-%m-%d')}"


def _generate_findings(decompositions: dict, base_metrics: pd.DataFrame, compare_metrics: pd.DataFrame) -> list:
    findings = []

    for pos, d in decompositions.items():
        if abs(d["delta"]) < 1:
            findings.append(f"**{pos}**: 业务转化量基本无波动，各项指标稳定")
            continue

        direction = "上升" if d["delta"] > 0 else "下降"
        findings.append(
            f"**{pos}**: 业务转化量{direction} {fmt_num(abs(d['delta']))}（{fmt_num(abs(d['delta_pct']), 1)}%），"
            f"主要由 **{d['main_factor_label']}** 驱动（贡献占比 {fmt_pct(abs(d[d['main_factor'] + '_pct']))}）"
        )

    base_total = base_metrics["conversion_count"].sum()
    comp_total = compare_metrics["conversion_count"].sum()
    if comp_total > 0:
        total_change_pct = (base_total - comp_total) / comp_total * 100
        if abs(total_change_pct) > 5:
            direction = "上升" if total_change_pct > 0 else "下降"
            findings.append(
                f"**整体**: 所有资源位合计业务转化量{direction} {fmt_num(abs(total_change_pct), 1)}%"
            )

    factor_counts = {}
    for d in decompositions.values():
        if abs(d["delta"]) >= 1:
            key = d["main_factor_label"]
            factor_counts[key] = factor_counts.get(key, 0) + 1
    if factor_counts and len(decompositions) > 1:
        top_factor = max(factor_counts, key=factor_counts.get)
        findings.append(
            f"在 {len(decompositions)} 个资源位中，有 {factor_counts[top_factor]} 个的主要波动因素为 "
            f"**{top_factor}**，建议重点关注此维度"
        )

    # 曝光上升但转化不涨
    for pos, d in decompositions.items():
        base_row = base_metrics[base_metrics["resource_position"] == pos].iloc[0]
        comp_row = compare_metrics[compare_metrics["resource_position"] == pos].iloc[0]
        exp_change = base_row["exposure_uv"] - comp_row["exposure_uv"]
        if exp_change > 0 and comp_row["exposure_uv"] > 0:
            exp_change_pct = exp_change / comp_row["exposure_uv"] * 100
            if exp_change_pct > 10 and d["delta"] <= 0:
                findings.append(
                    f"**{pos}**: 曝光UV上升 {fmt_change(exp_change_pct, 1)}% 但转化量未增长，"
                    f"新增流量质量可能较差"
                )

    return findings if findings else ["各资源位数据波动均在正常范围内"]


def _generate_recommendations(decompositions: dict) -> list:
    recommendations = []
    seen = set()

    sorted_items = sorted(decompositions.items(), key=lambda x: abs(x[1]["delta"]), reverse=True)

    for pos, d in sorted_items:
        if abs(d["delta"]) < 1:
            continue
        key = (d["main_factor"], d["main_factor_direction"])
        rec_text = RECOMMENDATION_MAP.get(key)
        if rec_text and key not in seen:
            seen.add(key)
            recommendations.append(f"**{d['main_factor_label']}{('上升' if d['main_factor_direction'] == 'up' else '下降')}**（影响资源位: {pos}）: {rec_text}")

    if not recommendations:
        recommendations.append("当前各资源位数据波动较小，建议保持现有策略，持续关注日常数据趋势")

    recommendations.append("建议建立资源位数据监控看板，对核心指标设置波动阈值告警，做到问题早发现早处理")
    return recommendations


def main():
    parser = argparse.ArgumentParser(description="资源位转化数据波动分析")
    parser.add_argument("file", help="Excel 数据文件路径")
    parser.add_argument("--mode", required=True, choices=["dod", "wow", "custom"],
                        help="对比模式: dod(日环比), wow(周同比), custom(自定义)")
    parser.add_argument("--date", help="目标日期 (dod/wow 模式使用, 格式: YYYY-MM-DD)")
    parser.add_argument("--base-start", help="基准期开始日期 (custom 模式)")
    parser.add_argument("--base-end", help="基准期结束日期 (custom 模式)")
    parser.add_argument("--compare-start", help="对比期开始日期 (custom 模式)")
    parser.add_argument("--compare-end", help="对比期结束日期 (custom 模式)")
    parser.add_argument("--position", help="仅分析指定资源位（可逗号分隔多个）")
    parser.add_argument("--output", help="输出文件路径（默认输出到 stdout）")

    args = parser.parse_args()

    if args.mode in ("dod", "wow") and not args.date:
        parser.error(f"{args.mode} 模式需要 --date 参数")
    if args.mode == "custom" and not all([args.base_start, args.base_end, args.compare_start, args.compare_end]):
        parser.error("custom 模式需要 --base-start, --base-end, --compare-start, --compare-end 参数")

    df = read_and_normalize(args.file)
    base_period, compare_period = get_periods(args)

    base_df = df[(df["date"] >= base_period[0]) & (df["date"] <= base_period[1])]
    compare_df = df[(df["date"] >= compare_period[0]) & (df["date"] <= compare_period[1])]

    if base_df.empty:
        print(f"错误：基准期 {_period_label(base_period)} 无数据", file=sys.stderr)
        sys.exit(1)
    if compare_df.empty:
        print(f"错误：对比期 {_period_label(compare_period)} 无数据", file=sys.stderr)
        sys.exit(1)

    if args.position:
        filter_positions = [p.strip() for p in args.position.split(",")]
        base_df = base_df[base_df["resource_position"].isin(filter_positions)]
        compare_df = compare_df[compare_df["resource_position"].isin(filter_positions)]

    base_metrics = compute_period_metrics(base_df)
    compare_metrics = compute_period_metrics(compare_df)

    common_positions = set(base_metrics["resource_position"]) & set(compare_metrics["resource_position"])
    if not common_positions:
        print("错误：基准期和对比期没有共同的资源位", file=sys.stderr)
        sys.exit(1)

    base_metrics = base_metrics[base_metrics["resource_position"].isin(common_positions)]
    compare_metrics = compare_metrics[compare_metrics["resource_position"].isin(common_positions)]

    decompositions = {}
    for pos in common_positions:
        base_row = base_metrics[base_metrics["resource_position"] == pos].iloc[0]
        comp_row = compare_metrics[compare_metrics["resource_position"] == pos].iloc[0]
        decompositions[pos] = factor_decomposition(base_row, comp_row)

    report = generate_report(
        base_metrics, compare_metrics, decompositions,
        base_period, compare_period, args.mode,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"报告已保存至: {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
