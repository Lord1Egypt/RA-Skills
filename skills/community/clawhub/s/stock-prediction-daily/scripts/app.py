"""
Flask web app: display prediction results, model report, and evaluation.
"""
import html
import json
import os
import re
from datetime import datetime

import pandas as pd
from flask import Flask, render_template, request
from markupsafe import Markup

import config
from features import get_feature_metadata

app = Flask(
    __name__,
    template_folder=config.TEMPLATE_DIR,
    static_folder=config.STATIC_DIR,
)


def _load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path).to_dict(orient="records")
    return []


def _dedupe_daily_rows(rows, date_field):
    if not rows:
        return []

    df = pd.DataFrame(rows).copy()
    if "股票代码" not in df.columns or date_field not in df.columns:
        return rows

    df["股票代码"] = df["股票代码"].astype(str).str.zfill(6)
    df[date_field] = pd.to_datetime(df[date_field], errors="coerce").dt.strftime("%Y-%m-%d")

    generated_field = "预测生成时间"
    if generated_field not in df.columns:
        df[generated_field] = df[date_field] + " 00:00:00"
    df[generated_field] = pd.to_datetime(df[generated_field], errors="coerce")
    df = df.sort_values([generated_field, date_field, "股票代码"], ascending=[False, False, True])
    df = df.drop_duplicates(subset=["股票代码", date_field], keep="first")
    df[generated_field] = df[generated_field].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df.to_dict(orient="records")


def _get_headers(rows):
    if not rows:
        return []
    return list(rows[0].keys())


def _extract_dates(rows, field_name):
    dates = []
    for row in rows:
        value = row.get(field_name)
        if value and value not in dates:
            dates.append(value)
    return sorted(dates, reverse=True)


def _filter_rows_by_date(rows, field_name, selected_date):
    if not selected_date:
        return rows
    return [row for row in rows if str(row.get(field_name, "")) == selected_date]


def _prepare_report_view(report):
    if not report:
        return None

    eda = report.get("eda", {})
    feature_dimensions = report.get("feature_dimensions", {})
    model_performance = report.get("model_performance", {})
    label_distribution = eda.get("label_distribution", {})
    feature_importance = feature_dimensions.get("feature_importance", {})
    selected_feature_names = feature_dimensions.get("selected_feature_names", [])
    cv_results = model_performance.get("cv_results", [])
    mean_metrics = next((item for item in cv_results if str(item.get("fold")) == "mean"), {})
    fold_metrics = [item for item in cv_results if str(item.get("fold")) != "mean"]

    feature_metadata = get_feature_metadata()
    feature_catalog = []
    report_catalog = feature_dimensions.get("feature_catalog", [])
    if report_catalog:
        for item in report_catalog:
            stats = item.get("stats", {})
            feature_catalog.append({
                "english_name": item.get("english_name"),
                "chinese_name": item.get("chinese_name"),
                "logic": item.get("logic"),
                "category": item.get("category"),
                "importance": item.get("importance", 0),
                "selected": item.get("selected", False),
                "mean": stats.get("mean"),
                "std": stats.get("std"),
                "min": stats.get("min"),
                "max": stats.get("max"),
            })
    else:
        for feature_name, importance in sorted(feature_importance.items(), key=lambda item: item[1], reverse=True):
            meta = feature_metadata.get(feature_name, {})
            stats = eda.get("feature_stats", {}).get(feature_name, {})
            feature_catalog.append({
                "english_name": feature_name,
                "chinese_name": meta.get("chinese_name", feature_name),
                "logic": meta.get("logic", "-"),
                "category": meta.get("category", "未分类"),
                "importance": importance,
                "selected": feature_name in selected_feature_names,
                "mean": stats.get("mean"),
                "std": stats.get("std"),
                "min": stats.get("min"),
                "max": stats.get("max"),
            })

    top_features = sorted(
        feature_catalog,
        key=lambda item: item["importance"],
        reverse=True,
    )[:10]
    max_importance = top_features[0]["importance"] if top_features else 0
    feature_bars = []
    for item in top_features:
        width = (item["importance"] / max_importance * 100) if max_importance else 0
        feature_bars.append({
            "name": item["english_name"],
            "chinese_name": item["chinese_name"],
            "logic": item["logic"],
            "value": item["importance"],
            "width": round(width, 2),
        })

    metrics = [
        {"label": "Accuracy", "value": mean_metrics.get("accuracy", 0)},
        {"label": "Precision", "value": mean_metrics.get("precision", 0)},
        {"label": "Recall", "value": mean_metrics.get("recall", 0)},
        {"label": "F1", "value": mean_metrics.get("f1", 0)},
        {"label": "AUC", "value": mean_metrics.get("auc", 0)},
    ]

    usage_steps = []
    for line in report.get("usage_guide", "").splitlines():
        line = line.strip()
        if line:
            usage_steps.append(line)

    selected_features = feature_dimensions.get("selected_features", 0)
    total_candidate = feature_dimensions.get("total_candidate_features", 0)
    selection_ratio = (selected_features / total_candidate * 100) if total_candidate else 0
    up_ratio = float(label_distribution.get("up_ratio", 0) or 0)
    down_ratio = 1 - up_ratio if up_ratio else 0

    project_background = (
        "本项目面向 A 股个股日线涨跌预测场景，基于沪深300 成份股历史日线数据训练 "
        "XGBoost 二分类模型。训练阶段先生成技术指标特征，再通过特征重要性筛选出核心入模特征，"
        "最终用十折交叉验证评估模型稳定性。预测和评估均统一采用腾讯财经日线数据，"
        "评估口径为 T+1，即用下一交易日收盘价验证预测方向。"
    )

    return {
        "generated_at": report.get("generated_at"),
        "project_background": project_background,
        "eda": eda,
        "feature_dimensions": feature_dimensions,
        "model_performance": model_performance,
        "summary_cards": [
            {"label": "训练股票数", "value": eda.get("num_stocks", "N/A")},
            {"label": "原始样本行数", "value": eda.get("total_raw_rows", "N/A")},
            {"label": "建模样本数", "value": eda.get("total_samples_after_fe", "N/A")},
            {"label": "入模特征数", "value": selected_features},
        ],
        "dataset_cards": [
            {"label": "时间范围", "value": eda.get("date_range", "N/A")},
            {"label": "上涨样本", "value": label_distribution.get("up (1)", 0)},
            {"label": "下跌样本", "value": label_distribution.get("down (0)", 0)},
            {"label": "上涨占比", "value": f"{up_ratio * 100:.2f}%"},
        ],
        "label_mix": {
            "up_width": round(up_ratio * 100, 2),
            "down_width": round(down_ratio * 100, 2),
            "up_count": label_distribution.get("up (1)", 0),
            "down_count": label_distribution.get("down (0)", 0),
        },
        "feature_bars": feature_bars,
        "feature_catalog": feature_catalog,
        "selection_ratio": round(selection_ratio, 2),
        "metrics": metrics,
        "fold_metrics": fold_metrics,
        "usage_steps": usage_steps,
    }


def _apply_inline_formatting(text):
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def _parse_markdown_table(lines, start_index):
    table_lines = []
    index = start_index
    while index < len(lines):
        current = lines[index].strip()
        if "|" not in current or not current:
            break
        table_lines.append(current)
        index += 1

    if len(table_lines) < 2:
        return None, start_index

    header_cells = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    separator_cells = [cell.strip() for cell in table_lines[1].strip("|").split("|")]
    if not separator_cells or not all(set(cell) <= {"-", ":"} for cell in separator_cells if cell):
        return None, start_index

    rows = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < len(header_cells):
            cells.extend([""] * (len(header_cells) - len(cells)))
        row_data = {header_cells[idx]: cells[idx] if idx < len(cells) else "" for idx in range(len(header_cells))}
        rows.append(row_data)

    return {
        "headers": header_cells,
        "rows": rows,
    }, index


def _render_table_html(table):
    table_html = ["<div class=\"table-wrap\"><table class=\"report-table\"><thead><tr>"]
    for cell in table["headers"]:
        table_html.append(f"<th>{_apply_inline_formatting(cell)}</th>")
    table_html.append("</tr></thead><tbody>")
    for row in table["rows"]:
        table_html.append("<tr>")
        for cell in table["headers"]:
            table_html.append(f"<td>{_apply_inline_formatting(row.get(cell, ''))}</td>")
        table_html.append("</tr>")
    table_html.append("</tbody></table></div>")
    return "".join(table_html)


def _consume_table(lines, start_index):
    table, index = _parse_markdown_table(lines, start_index)
    if not table:
        return None, start_index

    return _render_table_html(table), index


def _extract_tables_from_lines(lines):
    tables = []
    index = 0
    while index < len(lines):
        table, next_index = _parse_markdown_table(lines, index)
        if table:
            tables.append(table)
            index = next_index
            continue
        index += 1
    return tables


def _parse_numeric_value(text):
    if text is None:
        return None

    value = str(text).replace(",", "").strip()
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    if not match:
        return None
    return float(match.group())


def _parse_percent_value(text):
    if text is None:
        return None

    value = str(text).replace(",", "").strip()
    match = re.search(r"(-?\d+(?:\.\d+)?)\s*%", value)
    if not match:
        return None
    return float(match.group(1))


def _build_bar_chart(title, items, subtitle="", signed=False):
    usable_items = [item for item in items if item.get("value") is not None]
    if not usable_items:
        return None

    max_value = max(abs(item["value"]) for item in usable_items) or 1
    normalized_items = []
    for item in usable_items:
        raw_value = item["value"]
        tone = item.get("tone")
        if not tone:
            if signed:
                tone = "up" if raw_value >= 0 else "down"
            else:
                tone = "neutral"
        normalized_items.append({
            "label": item["label"],
            "secondary": item.get("secondary", ""),
            "display": item.get("display", str(raw_value)),
            "width": round(abs(raw_value) / max_value * 100, 2),
            "tone": tone,
        })

    return {
        "title": title,
        "subtitle": subtitle,
        "bars": normalized_items,
    }


def _build_fallback_charts(report):
    section_chart = _build_bar_chart(
        "章节信息密度",
        [
            {
                "label": section["title"],
                "secondary": f"{section.get('table_count', 0)} 张表格",
                "display": f"{section.get('line_count', 0)} 行",
                "value": section.get("line_count", 0),
                "tone": "neutral",
            }
            for section in report.get("sections", [])
        ],
        subtitle="按章节内容行数估算各部分信息密度。",
    )
    return [chart for chart in [section_chart] if chart]


def _build_sector_charts(report):
    charts = []
    ranking_table = next(
        (
            table for table in report.get("tables", [])
            if "板块" in table.get("headers", []) and "梯队" in table.get("headers", [])
        ),
        None,
    )
    if ranking_table:
        ranking_items = []
        total = len(ranking_table["rows"])
        for index, row in enumerate(ranking_table["rows"]):
            ranking_items.append({
                "label": row.get("板块", "-"),
                "secondary": row.get("梯队", ""),
                "display": row.get("交易结论") or row.get("近阶段判断") or "",
                "value": total - index,
                "tone": "neutral",
            })
        charts.append(_build_bar_chart("重点板块排序", ranking_items, "按照报告中的优先顺序展示当前主线。"))

    tag_counts = {}
    for table in report.get("tables", []):
        if "操作标签" not in table.get("headers", []):
            continue
        for row in table["rows"]:
            tag = row.get("操作标签", "").strip() or "未标注"
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    if tag_counts:
        tag_items = [
            {
                "label": label,
                "secondary": "出现次数",
                "display": f"{count} 次",
                "value": count,
                "tone": "neutral",
            }
            for label, count in sorted(tag_counts.items(), key=lambda item: item[1], reverse=True)
        ]
        charts.append(_build_bar_chart("操作标签分布", tag_items, "统计报告中出现的配置型、观察型、情绪型等标签。"))

    return [chart for chart in charts if chart] or _build_fallback_charts(report)


def _build_stock_charts(report):
    charts = []
    overview_table = next(
        (
            table for table in report.get("tables", [])
            if "股票" in table.get("headers", []) and any(
                ("涨跌幅" in header) or ("涨跌" in header)
                for header in table.get("headers", [])
            )
        ),
        None,
    )
    if overview_table:
        return_header = next(
            (
                header for header in overview_table["headers"]
                if ("涨跌幅" in header) or ("涨跌" in header)
            ),
            None,
        )
        if return_header:
            return_items = []
            sorted_rows = sorted(
                overview_table["rows"],
                key=lambda row: _parse_percent_value(row.get(return_header)) if _parse_percent_value(row.get(return_header)) is not None else -10**9,
                reverse=True,
            )
            for row in sorted_rows[:8]:
                value = _parse_percent_value(row.get(return_header))
                if value is None:
                    continue
                return_items.append({
                    "label": row.get("股票", "-"),
                    "secondary": row.get("一句话建议", ""),
                    "display": f"{value:+.2f}%",
                    "value": value,
                })
            charts.append(_build_bar_chart("近 7 日涨跌幅", return_items, "从全名单概览表提取收益表现最高和最低的个股。", signed=True))

    section_labels = ["第一优先级", "第二优先级", "观察不出手", "回避"]
    section_items = []
    for label in section_labels:
        section = next((item for item in report.get("sections", []) if item["title"].endswith(label)), None)
        if not section:
            continue
        count = sum(len(table["rows"]) for table in section.get("tables", []))
        if count <= 0:
            continue
        section_items.append({
            "label": label,
            "secondary": "股票数量",
            "display": f"{count} 只",
            "value": count,
            "tone": "neutral",
        })
    if section_items:
        charts.append(_build_bar_chart("决策分层分布", section_items, "按报告中的优先级和回避区划分股票数量。"))

    return [chart for chart in charts if chart] or _build_fallback_charts(report)


def _render_markdown_blocks(block_lines):
    html_parts = []
    index = 0
    while index < len(block_lines):
        raw_line = block_lines[index]
        stripped = raw_line.strip()
        if not stripped:
            index += 1
            continue

        table_html, next_index = _consume_table(block_lines, index)
        if table_html:
            html_parts.append(table_html)
            index = next_index
            continue

        if stripped.startswith(("- ", "* ")):
            items = []
            while index < len(block_lines):
                item_line = block_lines[index].strip()
                if not item_line.startswith(("- ", "* ")):
                    break
                items.append(f"<li>{_apply_inline_formatting(item_line[2:].strip())}</li>")
                index += 1
            html_parts.append("<ul class=\"article-list\">" + "".join(items) + "</ul>")
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while index < len(block_lines):
                item_line = block_lines[index].strip()
                if not re.match(r"^\d+\.\s+", item_line):
                    break
                cleaned_item = re.sub(r"^\d+\.\s+", "", item_line)
                items.append(f"<li>{_apply_inline_formatting(cleaned_item)}</li>")
                index += 1
            html_parts.append("<ol class=\"article-list\">" + "".join(items) + "</ol>")
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(block_lines):
            next_line = block_lines[index].strip()
            if not next_line:
                index += 1
                break
            if next_line.startswith(("- ", "* ")) or re.match(r"^\d+\.\s+", next_line) or next_line.startswith("#"):
                break
            if "|" in next_line:
                break
            paragraph_lines.append(next_line)
            index += 1
        html_parts.append(f"<p>{_apply_inline_formatting(' '.join(paragraph_lines))}</p>")
    return Markup("".join(html_parts))


def _parse_report_document(text, fallback_title):
    lines = text.splitlines()
    title = fallback_title
    subtitle = ""
    report_time = ""
    intro_lines = []
    sections = []
    current_section = None
    current_major_title = ""

    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped.startswith("# ") and title == fallback_title:
            title = stripped[2:].strip()
            continue
        if not subtitle and stripped.startswith(">"):
            subtitle = stripped[1:].strip()
            continue
        if not report_time and re.match(r"^(报告时间|生成时间)\s*[：:]", stripped):
            report_time = re.sub(r"^(报告时间|生成时间)\s*[：:]\s*", "", stripped)
            continue
        if stripped.startswith("## "):
            if current_section:
                sections.append(current_section)
            current_major_title = stripped[3:].strip()
            current_section = {"title": current_major_title, "lines": []}
            continue
        if stripped.startswith("### "):
            subsection_title = stripped[4:].strip()
            if current_section and current_section["lines"]:
                sections.append(current_section)
            composed_title = f"{current_major_title} / {subsection_title}" if current_major_title else subsection_title
            current_section = {"title": composed_title, "lines": []}
            continue

        if current_section:
            current_section["lines"].append(raw_line)
        else:
            intro_lines.append(raw_line)

    if current_section:
        sections.append(current_section)

    intro_html = _render_markdown_blocks(intro_lines)
    intro_tables = _extract_tables_from_lines(intro_lines)
    rendered_sections = []
    highlights = []
    all_tables = list(intro_tables)
    for section in sections:
        section_tables = _extract_tables_from_lines(section["lines"])
        rendered_sections.append({
            "title": section["title"],
            "anchor_id": f"section-{len(rendered_sections) + 1}",
            "body_html": _render_markdown_blocks(section["lines"]),
            "tables": section_tables,
            "table_count": len(section_tables),
            "line_count": len([line for line in section["lines"] if line.strip()]),
        })
        all_tables.extend(section_tables)
        if len(highlights) < 4:
            for line in section["lines"]:
                stripped = line.strip()
                if stripped.startswith(("- ", "* ")):
                    highlights.append(stripped[2:].strip())
                if len(highlights) >= 4:
                    break

    if not rendered_sections and intro_lines:
        rendered_sections.append({
            "title": "报告正文",
            "body_html": intro_html,
        })
        intro_html = Markup("")

    return {
        "title": title,
        "subtitle": subtitle,
        "report_time": report_time,
        "intro_html": intro_html,
        "sections": rendered_sections,
        "highlights": highlights[:4],
        "tables": all_tables,
        "table_count": len(all_tables),
        "bullet_count": sum(1 for line in lines if line.strip().startswith(("- ", "* "))),
        "line_count": len([line for line in lines if line.strip()]),
    }


def _parse_report_datetime(value):
    if not value:
        return None

    text = str(value).strip()
    if not text:
        return None

    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y%m%d_%H%M%S",
        "%Y%m%d%H%M%S",
    ):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue

    parsed = pd.to_datetime(text, errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed.to_pydatetime()


def _build_report_menu_item(path, modified_at, size_kb):
    name = os.path.basename(path)
    fallback_title = name.rsplit(".", 1)[0].replace("_", " ")
    raw_text = _load_report_file(path)
    report = _parse_report_document(raw_text, fallback_title)
    display_time = report.get("report_time") or modified_at
    sort_time = _parse_report_datetime(report.get("report_time")) or _parse_report_datetime(modified_at) or datetime.min
    return {
        "name": name,
        "path": path,
        "modified_at": modified_at,
        "size_kb": size_kb,
        "display_title": report.get("title") or fallback_title,
        "display_time": display_time,
        "report": report,
        "sort_time": sort_time,
    }


def _list_report_files(report_dir):
    files = []
    if not os.path.exists(report_dir):
        return files

    for name in os.listdir(report_dir):
        path = os.path.join(report_dir, name)
        if not os.path.isfile(path):
            continue
        if not name.lower().endswith((".md", ".txt", ".json")):
            continue
        stat = os.stat(path)
        files.append(
            _build_report_menu_item(
                path,
                datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                round(stat.st_size / 1024, 1),
            )
        )
    files.sort(key=lambda item: item["sort_time"], reverse=True)
    return files


def _load_report_file(path):
    if path.lower().endswith(".json"):
        with open(path, "r", encoding="utf-8") as file_obj:
            payload = json.load(file_obj)
        return json.dumps(payload, ensure_ascii=False, indent=2)

    with open(path, "r", encoding="utf-8") as file_obj:
        return file_obj.read()


def _prepare_analysis_page(report_dir, selected_name, kind):
    file_items = _list_report_files(report_dir)
    selected_item = None
    if file_items:
        selected_item = next((item for item in file_items if item["name"] == selected_name), file_items[0])

    report = selected_item.get("report") if selected_item else None

    if kind == "sector":
        empty_hint = "暂无板块分析报告。调用 stock-sector-research 后，请将结果保存到 scripts/reports/sector_analysis/。"
        page_title = "板块分析"
    else:
        empty_hint = "暂无个股分析报告。调用 stock-watchlist-briefing 后，请将结果保存到 scripts/reports/stock_analysis/。"
        page_title = "个股分析"

    summary_cards = []
    charts = []
    nav_sections = []
    if selected_item and report:
        summary_cards = [
            {"label": "报告章节", "value": len(report.get("sections", []))},
            {"label": "关键表格", "value": report.get("table_count", 0)},
            {"label": "要点条目", "value": report.get("bullet_count", 0)},
            {"label": "文件大小", "value": f"{selected_item['size_kb']} KB"},
        ]
        nav_sections = [section for section in report.get("sections", []) if " / " not in section.get("title", "")]
        if kind == "sector":
            charts = _build_sector_charts(report)
        else:
            charts = _build_stock_charts(report)

    return {
        "title": page_title,
        "files": file_items,
        "selected_file": selected_item,
        "report": report,
        "empty_hint": empty_hint,
        "summary_cards": summary_cards,
        "charts": charts,
        "nav_sections": nav_sections,
    }


@app.route("/")
@app.route("/predictions")
def predictions():
    rows = _dedupe_daily_rows(_load_csv(config.PREDICTION_PATH), "当前时间")
    available_dates = _extract_dates(rows, "当前时间")
    selected_date = request.args.get("date") or (available_dates[0] if available_dates else None)
    filtered_rows = _filter_rows_by_date(rows, "当前时间", selected_date)
    up_count = sum(1 for row in filtered_rows if row.get("预测结果") == "上涨")
    down_count = sum(1 for row in filtered_rows if row.get("预测结果") == "下跌")
    return render_template(
        "predictions.html",
        rows=filtered_rows,
        headers=_get_headers(filtered_rows or rows),
        up_count=up_count,
        down_count=down_count,
        available_dates=available_dates,
        selected_date=selected_date,
        active="predictions",
    )


@app.route("/report")
def report():
    data = _load_json(config.REPORT_PATH)
    return render_template(
        "report.html",
        report=_prepare_report_view(data),
        active="report",
    )


@app.route("/evaluation")
def evaluation():
    rows = _dedupe_daily_rows(_load_csv(config.EVALUATION_PATH), "预测时间")
    available_dates = _extract_dates(rows, "预测时间")
    selected_date = request.args.get("date") or (available_dates[0] if available_dates else None)
    filtered_rows = _filter_rows_by_date(rows, "预测时间", selected_date)
    valid = [r for r in filtered_rows if r.get("预测是否准确") in ("✓", "✗")]
    if valid:
        acc = sum(1 for r in valid if r["预测是否准确"] == "✓") / len(valid)
    else:
        acc = None
    return render_template(
        "evaluation.html",
        rows=filtered_rows,
        headers=_get_headers(filtered_rows or rows),
        accuracy=acc,
        available_dates=available_dates,
        selected_date=selected_date,
        active="evaluation",
    )


@app.route("/sector-analysis")
def sector_analysis():
    return render_template(
        "sector_analysis.html",
        page=_prepare_analysis_page(
            config.SECTOR_REPORTS_DIR,
            request.args.get("file"),
            "sector",
        ),
        active="sector-analysis",
        title="板块分析",
    )


@app.route("/stock-analysis")
def stock_analysis():
    return render_template(
        "stock_analysis.html",
        page=_prepare_analysis_page(
            config.STOCK_REPORTS_DIR,
            request.args.get("file"),
            "stock",
        ),
        active="stock-analysis",
        title="个股分析",
    )


if __name__ == "__main__":
    print("Starting web server at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
