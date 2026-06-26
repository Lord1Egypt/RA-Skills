#!/usr/bin/env python3.11
"""Build dashboard spec from query, semantics, and chart plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

SIZE_BY_CHART = {
    "kpi": (3, 2),
    "line": (6, 4),
    "bar": (6, 4),
    "grouped_bar": (6, 4),
    "table": (12, 5),
}

GRID_COLS = 12


def next_position(cursor_x: int, cursor_y: int, h_row_max: int, w: int, h: int) -> Tuple[int, int, int, int, int]:
    if cursor_x + w > GRID_COLS:
        cursor_x = 0
        cursor_y += h_row_max
        h_row_max = 0

    x, y = cursor_x, cursor_y
    cursor_x += w
    h_row_max = max(h_row_max, h)
    return x, y, cursor_x, cursor_y, h_row_max


def unique_keep_order(values: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for v in values:
        if not v or v in seen:
            continue
        seen.add(v)
        out.append(v)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Build dashboard.json")
    parser.add_argument("--queries", required=True, help="Path to query_catalog.json")
    parser.add_argument("--semantics", required=True, help="Path to semantic_catalog.json")
    parser.add_argument("--charts", required=True, help="Path to chart_plan.json")
    parser.add_argument("--output", required=True, help="Path to dashboard.json")
    args = parser.parse_args()

    queries = json.loads(Path(args.queries).read_text(encoding="utf-8")).get("queries", [])
    semantics = json.loads(Path(args.semantics).read_text(encoding="utf-8")).get("queries", [])
    charts = json.loads(Path(args.charts).read_text(encoding="utf-8")).get("charts", [])

    sem_by_id = {s.get("id"): s for s in semantics}
    chart_by_id = {c.get("id"): c for c in charts}

    widgets: List[Dict] = []
    global_filter_map: Dict[str, Dict] = {}
    x, y, row_h = 0, 0, 0

    for q in queries:
        qid = q.get("id")
        sem = sem_by_id.get(qid, {})
        chart_item = chart_by_id.get(qid, {})
        chart = chart_item.get("chart", "table")
        w, h = SIZE_BY_CHART.get(chart, SIZE_BY_CHART["table"])
        pos_x, pos_y, x, y, row_h = next_position(x, y, row_h, w, h)
        dsl_filters = sem.get("dsl_filters", [])
        dsl_filter_fields = sem.get("dsl_filter_fields", [])
        meta_filters = q.get("filters", [])
        widget_filters = unique_keep_order([*meta_filters, *dsl_filter_fields])

        for field in widget_filters:
            item = global_filter_map.setdefault(
                field,
                {
                    "id": f"gf_{field}",
                    "field": field,
                    "suggested_widget": "select",
                    "is_time": False,
                    "operators": [],
                    "source_queries": [],
                },
            )
            item["source_queries"] = unique_keep_order([*item["source_queries"], qid])

        for f in dsl_filters:
            field = f.get("field")
            if not field:
                continue
            item = global_filter_map.setdefault(
                field,
                {
                    "id": f"gf_{field}",
                    "field": field,
                    "suggested_widget": f.get("suggested_widget", "select"),
                    "is_time": bool(f.get("is_time")),
                    "operators": [],
                    "source_queries": [],
                },
            )
            item["suggested_widget"] = f.get("suggested_widget", item["suggested_widget"])
            item["is_time"] = bool(item["is_time"] or f.get("is_time"))
            op = f.get("operator")
            if op:
                item["operators"] = unique_keep_order([*item["operators"], op])
            item["source_queries"] = unique_keep_order([*item["source_queries"], qid])

        widget = {
            "id": f"widget_{qid}",
            "query_id": qid,
            "title": q.get("title") or qid,
            "chart": chart,
            "position": {"x": pos_x, "y": pos_y, "w": w, "h": h},
            "fields": {
                "metrics": sem.get("metrics", []),
                "dimensions": sem.get("dimensions", []),
                "time_fields": sem.get("time_fields", []),
            },
            "filters": widget_filters,
            "dsl_filters": dsl_filters,
            "datasource": q.get("datasource", ""),
            "refresh": q.get("refresh", ""),
        }
        widgets.append(widget)

    global_filters = list(global_filter_map.values())

    dashboard = {
        "version": "0.1.0",
        "name": "SQL Generated Dashboard",
        "ui": {
            "theme": {
                "name": "studio_sky",
                "font_family": '"Source Sans 3", "Noto Sans SC", sans-serif',
                "app_bg": "#f5f7fb",
                "canvas_bg": "#eef2ff",
                "panel_bg": "#ffffff",
                "line_soft": "#dce4f3",
                "line_strong": "#c7d4ec",
                "text_main": "#0f172a",
                "text_sub": "#334155",
                "text_mute": "#64748b",
                "brand": "#0ea5e9",
                "brand_weak": "#e0f2fe",
                "radius_sm": 8,
                "radius_md": 14,
                "card_shadow": "0 10px 28px rgba(15, 23, 42, 0.08)",
            },
            "chart_palette": ["#0ea5e9", "#f59e0b", "#14b8a6", "#f43f5e", "#8b5cf6"],
        },
        "grid": {"columns": GRID_COLS, "rowHeight": 1},
        "pages": [
            {
                "id": "page_main",
                "title": "Overview",
                "global_filters": global_filters,
                "widgets": widgets,
            }
        ],
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(dashboard, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Built dashboard spec with {len(widgets)} widgets -> {out_path}")


if __name__ == "__main__":
    main()
