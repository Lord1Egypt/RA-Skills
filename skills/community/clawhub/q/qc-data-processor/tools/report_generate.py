def ascii_control_chart(chart_data: dict) -> str:
    subgroups = chart_data.get("subgroups", [])
    xbar_values = chart_data.get("xbar_values", [])
    r_values = chart_data.get("r_values", [])
    ucl_x = chart_data.get("ucl_xbar_line") or chart_data.get("ucl_x_line", 0)
    lcl_x = chart_data.get("lcl_xbar_line") or chart_data.get("lcl_x_line", 0)
    cl_x = chart_data.get("cl_xbar_line") or chart_data.get("cl_x_line", 0)
    ucl_r = chart_data.get("ucl_r_line", 0)
    lcl_r = chart_data.get("lcl_r_line", 0)
    cl_r = chart_data.get("cl_r_line", 0)
    usl = chart_data.get("usl")
    lsl = chart_data.get("lsl")

    lines = []
    lines.append("Xbar Chart")
    lines.append("-" * 60)

    if not xbar_values:
        lines.append("(no data)")
        return "\n".join(lines)

    width = 50
    all_vals = xbar_values + [ucl_x, lcl_x, cl_x]
    if usl is not None:
        all_vals.append(usl)
    if lsl is not None:
        all_vals.append(lsl)
    vmin, vmax = min(all_vals), max(all_vals)
    rng = vmax - vmin if vmax != vmin else 1
    rng *= 1.1

    for i, val in enumerate(xbar_values):
        if subgroups:
            label = f"{subgroups[i] if i < len(subgroups) else i + 1:>3}"
        else:
            label = f"{i + 1:>3}"
        pos = int((val - vmin) / rng * width)
        if val > ucl_x or val < lcl_x:
            bar = " " * pos + "*"
        else:
            bar = " " * pos + "|"
        ucl_pos = int((ucl_x - vmin) / rng * width) if ucl_x is not None else None
        lcl_pos = int((lcl_x - vmin) / rng * width) if lcl_x is not None else None
        cl_pos = int((cl_x - vmin) / rng * width) if cl_x is not None else None
        parts = list(bar.ljust(width))
        for p, ch in [(ucl_pos, "U"), (lcl_pos, "L"), (cl_pos, "C")]:
            if p is not None and 0 <= p < width:
                parts[p] = ch
        lines.append(f"{label} {''.join(parts)} {val:.4f}")

    lines.append(" " * 4 + "-" * width)
    lines.append(f"     UCL={ucl_x:.4f}  CL={cl_x:.4f}  LCL={lcl_x:.4f}")
    if usl is not None:
        lines.append(f"     USL={usl:.4f}")
    if lsl is not None:
        lines.append(f"     LSL={lsl:.4f}")

    lines.append("")
    lines.append("R Chart")
    lines.append("-" * 60)

    if not r_values:
        lines.append("(no data)")
        return "\n".join(lines)

    rall = r_values + [ucl_r, lcl_r, cl_r]
    rmin, rmax = min(rall), max(rall)
    rrng = rmax - rmin if rmax != rmin else 1
    rrng *= 1.1

    for i, val in enumerate(r_values):
        if subgroups and len(r_values) < len(subgroups):
            r_label_idx = i + 1
            label = f"{subgroups[r_label_idx] if r_label_idx < len(subgroups) else i + 1:>3}"
        elif subgroups:
            label = f"{subgroups[i] if i < len(subgroups) else i + 1:>3}"
        else:
            label = f"{i + 1:>3}"
        pos = int((val - rmin) / rrng * width)
        bar = " " * pos + "|"
        ucl_rpos = int((ucl_r - rmin) / rrng * width) if ucl_r is not None else None
        lcl_rpos = int((lcl_r - rmin) / rrng * width) if lcl_r is not None else None
        cl_rpos = int((cl_r - rmin) / rrng * width) if cl_r is not None else None
        parts = list(bar.ljust(width))
        for p, ch in [(ucl_rpos, "U"), (lcl_rpos, "L"), (cl_rpos, "C")]:
            if p is not None and 0 <= p < width:
                parts[p] = ch
        if val > ucl_r:
            parts[pos] = "*"
        lines.append(f"{label} {''.join(parts)} {val:.4f}")

    lines.append(" " * 4 + "-" * width)
    lines.append(f"     UCL={ucl_r:.4f}  CL={cl_r:.4f}  LCL={lcl_r:.4f}")

    return "\n".join(lines)


def ascii_histogram(values: list, bins: int = 10) -> str:
    if not values:
        return "(no data)"

    import numpy as np
    counts, edges = np.histogram(values, bins=bins)
    max_count = max(counts) if max(counts) > 0 else 1
    width = 40
    lines = []
    lines.append("Histogram")
    lines.append("-" * 50)

    for i in range(len(counts)):
        bar_len = int(counts[i] / max_count * width)
        bar = "#" * bar_len
        lines.append(f"{edges[i]:.2f}-{edges[i + 1]:.2f} |{bar} {counts[i]}")

    return "\n".join(lines)


def ascii_probability_plot(pp_data: dict) -> str:
    lines = []
    lines.append("Probability Plot")
    lines.append("-" * 60)
    lines.append(f"{'Time':>10}  {'F(t)%':>8}  {'Censored':>8}")
    lines.append("-" * 30)

    times = pp_data.get("times", [])
    ranks = pp_data.get("benard_ranks", [])
    censors = pp_data.get("censor", [])
    for i in range(min(len(times), 30)):
        c_flag = "Y" if i < len(censors) and censors[i] == 0 else ""
        lines.append(f"{times[i]:>10.1f}  {ranks[i] * 100:>7.2f}%  {c_flag:>8}")

    if len(times) > 30:
        lines.append(f"... ({len(times)} total points)")

    fit_line = pp_data.get("fit_line", [])
    if fit_line:
        lines.append("")
        lines.append("Fitted line points (sample):")
        step = max(1, len(fit_line) // 10)
        for i in range(0, len(fit_line), step):
            lines.append(f"  t={fit_line[i][0]:.1f}, F(t)={fit_line[i][1] * 100:.1f}%")

    return "\n".join(lines)


def ascii_pareto(labels: list, values: list, top_n: int = 5) -> str:
    if not labels or not values:
        return "(no data)"

    sorted_pairs = sorted(zip(labels, values), key=lambda x: x[1], reverse=True)
    total = sum(values)
    lines = []
    lines.append("Pareto Chart")
    lines.append("-" * 50)

    max_val = sorted_pairs[0][1] if sorted_pairs else 1
    cum_pct = 0
    width = 30

    for i, (label, val) in enumerate(sorted_pairs[:top_n]):
        pct = val / total * 100 if total > 0 else 0
        cum_pct += pct
        bar_len = int(val / max_val * width)
        bar = "#" * bar_len
        lines.append(f"{label:<15} |{bar.ljust(width)} {val:>5} ({pct:.0f}%) cum={cum_pct:.0f}%")

    return "\n".join(lines)


def _render_daily(result: dict, metadata: dict) -> str:
    product = metadata.get("product", "Product")
    date = metadata.get("date", "Date")
    n = result.get("rows", result.get("n_samples", "N"))
    stats = result.get("statistics", {})
    cpk = stats.get("cpk", "N/A")
    alarms = result.get("alarms", [])
    metrics = result.get("metrics", {})

    lines = []
    lines.append(f"# {product} 品质日报 | {date}")
    lines.append("")
    lines.append("## 检验概况")
    lines.append("")
    lines.append("| 项目 | 数值 |")
    lines.append("|--- | ---|")
    lines.append(f"| 抽检数 | {n} |")
    if cpk and cpk != "N/A":
        lines.append(f"| Cpk | {cpk} |")
    if metrics:
        for k, v in metrics.items():
            if isinstance(v, (int, float)):
                lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append("## SPC 异常点")
    lines.append("")
    if alarms:
        for a in alarms[:5]:
            points = a.get("points", [])
            pts_str = ",".join(str(p) for p in points)
            lines.append(f"- {a.get('rule', '')} (点: {pts_str}) [{a.get('severity', '')}]")
    else:
        lines.append("无异常点")
    lines.append("")
    lines.append("## 备注/改善措施")
    lines.append("")
    lines.append("（待填写）")

    return "\n".join(lines)


def _render_weekly(result: dict, metadata: dict) -> str:
    product = metadata.get("product", "Product")
    week = metadata.get("week", "Week")
    stats = result.get("statistics", {})
    cpk = stats.get("cpk", "N/A")
    ppk = stats.get("ppk", "N/A")
    sigma = stats.get("sigma_level", "N/A")
    alarms = result.get("alarms", [])

    lines = []
    lines.append(f"# {product} 品质周报 | {week}")
    lines.append("")
    lines.append("## 本周趋势")
    lines.append("")
    if cpk and cpk != "N/A":
        lines.append(f"本周过程能力 Cpk = {cpk}，Ppk = {ppk}，Sigma Level = {sigma}")
    if alarms:
        lines.append(f"共发现 {len(alarms)} 个SPC异常点")
    else:
        lines.append("本周无SPC异常，过程受控")
    lines.append("")
    lines.append("## SPC Cpk 汇总")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("|--- | ---|")
    lines.append(f"| Cpk | {cpk} |")
    lines.append(f"| Ppk | {ppk} |")
    lines.append(f"| Sigma Level | {sigma} |")
    lines.append("")
    lines.append("## 下周重点")
    lines.append("")
    lines.append("（待填写）")

    return "\n".join(lines)


def _render_8d(result: dict, metadata: dict) -> str:
    customer = metadata.get("customer", "Customer")
    date = metadata.get("date", "Date")
    lines = []
    lines.append(f"# 8D 客诉报告 | {customer} | {date}")
    lines.append("")
    for section in ["D1 团队", "D2 问题描述", "D3 围堵措施", "D4 根因分析", "D5 永久纠正措施", "D6 验证", "D7 预防措施", "D8 团队确认"]:
        lines.append(f"## {section}")
        lines.append("")
        lines.append("（待填写）")
        lines.append("")
    return "\n".join(lines)


def _render_reliability(result: dict, metadata: dict) -> str:
    product = metadata.get("product", "Product")
    best_fit = result.get("best_fit", "N/A")
    params = result.get("parameters", {})
    metrics = result.get("metrics", {})
    n = result.get("n_samples", "N")
    n_fail = result.get("n_failures", "N")
    warning = result.get("warning", "")

    lines = []
    lines.append(f"# {product} 可靠性鉴定报告")
    lines.append("")
    lines.append("## 试验概况")
    lines.append("")
    lines.append(f"样品数: {n}，失效数: {n_fail}")
    if warning:
        lines.append(f"**警告**: {warning}")
    lines.append(f"最优分布: {best_fit}")
    lines.append("")
    lines.append("## 分布参数")
    lines.append("")
    for k, v in params.items():
        if isinstance(v, (int, float)):
            lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## B10/B50 寿命")
    lines.append("")
    for k, v in metrics.items():
        if isinstance(v, (int, float)):
            lines.append(f"- {k}: {v}")
        elif isinstance(v, list) and len(v) == 2:
            lines.append(f"- {k}: {v[0]} ~ {v[1]}")
    lines.append("")
    lines.append("## 结论")
    lines.append("")
    if best_fit == "Weibull" and "beta" in params:
        b = params["beta"]
        if b > 1:
            lines.append(f"产品处于耗损失效期（β={b}），建议关注寿命末期失效率上升趋势")
        elif b < 1:
            lines.append(f"产品处于早期失效期（β={b}），建议加强出厂前筛选")
        else:
            lines.append(f"产品处于随机失效期（β≈{b}），失效率稳定")
    lines.append("")
    lines.append(f"B10寿命: {metrics.get('b10_life', 'N/A')}")

    return "\n".join(lines)


TEMPLATES = {
    "daily": _render_daily,
    "weekly": _render_weekly,
    "8d": _render_8d,
    "reliability": _render_reliability,
}


def qc_report_generate(analysis_result: dict, template: str, metadata: dict = None) -> str:
    if metadata is None:
        metadata = {}
    if template not in TEMPLATES:
        available = list(TEMPLATES.keys())
        return f"Error: template '{template}' not found. Available: {available}"
    return TEMPLATES[template](analysis_result, metadata)
