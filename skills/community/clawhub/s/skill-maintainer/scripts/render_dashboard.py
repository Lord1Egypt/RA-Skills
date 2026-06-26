#!/usr/bin/env python3
"""Render a static HTML dashboard for the ClawHub skill portfolio."""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
LOCAL_CACHE_DIR = ROOT_DIR / ".cache"
LOCAL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(LOCAL_CACHE_DIR / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(LOCAL_CACHE_DIR))

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    HAS_MATPLOTLIB = True
except Exception:
    matplotlib = None
    plt = None
    HAS_MATPLOTLIB = False


PALETTE = {
    "ink": "#23262f",
    "muted": "#6d7280",
    "line": "#d9dde7",
    "teal": "#1f7a8c",
    "green": "#4f8a5b",
    "amber": "#d99b2b",
    "red": "#bd4f4f",
    "violet": "#6c5ce7",
    "slate": "#44546a",
}


ACTION_LABELS = {
    "respond_fix_upload": "Respond / Fix / Upload",
    "keep_public": "Keep Public",
    "curate_or_improve": "Curate / Improve",
    "review_for_merge_or_private": "Review Merge / Private",
    "consider_private_or_delete": "Private / Delete Candidate",
    "data_unavailable": "Data Unavailable",
}


VERDICT_LABELS = {
    "meaningful": "Meaningful",
    "needs_evidence": "Needs Evidence",
    "plausible_but_low_signal": "Plausible, Low Signal",
    "low_signal": "Low Signal",
    "data_unavailable": "Data Unavailable",
}


DECISION_LABELS = {
    "fix_and_reply": "Fix and Reply",
    "upgrade_public": "Upgrade Public",
    "merge_into_stronger_skill": "Merge",
    "move_private_or_hide": "Private / Hide",
    "delete_candidate": "Delete Candidate",
    "monitor": "Monitor",
    "keep_public": "Keep Public",
    "data_unavailable": "Data Unavailable",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_if_exists(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_csv(path)


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return read_json(path)


def to_int(value: Any) -> int:
    try:
        if value in (None, ""):
            return 0
        return int(float(value))
    except Exception:
        return 0


def to_float(value: Any) -> float:
    try:
        if value in (None, ""):
            return 0.0
        return float(value)
    except Exception:
        return 0.0


def fmt_num(value: Any) -> str:
    return f"{to_int(value):,}"


def fmt_delta(value: Any) -> str:
    number = to_int(value)
    if number > 0:
        return f"+{number:,}"
    return f"{number:,}"


def slug_url(handle: str, slug: str) -> str:
    return f"https://clawhub.ai/{handle}/{slug}"


def slug_html(slug: str) -> str:
    return f'<code class="slug-token notranslate" translate="no">{html.escape(slug)}</code>'


def chart_label(row: dict[str, str]) -> str:
    label = row.get("display_name") or row.get("slug") or "unknown"
    return label if len(label) <= 38 else label[:35] + "..."


def clean_row(row: dict[str, str], handle: str) -> dict[str, Any]:
    return {
        "slug": row.get("slug", ""),
        "display_name": row.get("display_name", ""),
        "summary": row.get("summary", ""),
        "url": slug_url(handle, row.get("slug", "")),
        "downloads": to_int(row.get("downloads")),
        "new_downloads": to_int(row.get("new_downloads")),
        "installs": to_int(row.get("installs_all_time")),
        "new_installs": to_int(row.get("new_installs")),
        "stars": to_int(row.get("stars")),
        "comments": to_int(row.get("comments")),
        "versions": to_int(row.get("versions")),
        "score": to_float(row.get("meaning_score")),
        "verdict": row.get("meaningfulness", ""),
        "action": row.get("recommended_action", ""),
        "decision": row.get("portfolio_decision", ""),
        "decision_reason": row.get("portfolio_reason", ""),
        "detail_ok": row.get("detail_ok", ""),
        "detail_error": row.get("detail_error", ""),
        "category": row.get("category", "Other"),
        "family": row.get("merge_family_key", ""),
        "family_size": to_int(row.get("merge_family_size")),
        "merge_target": row.get("merge_target_slug", ""),
        "updated": row.get("updated_at_utc", ""),
        "flags": row.get("flags", ""),
    }


def save_action_chart(rows: list[dict[str, str]], path: Path) -> None:
    if not HAS_MATPLOTLIB:
        save_svg_placeholder(path, "Recommended action mix", "Chart rendering needs matplotlib. Table data is still available.")
        return
    counts = Counter(row.get("recommended_action", "") for row in rows)
    keys = [
        "respond_fix_upload",
        "keep_public",
        "curate_or_improve",
        "review_for_merge_or_private",
        "consider_private_or_delete",
        "data_unavailable",
    ]
    values = [counts.get(key, 0) for key in keys]
    labels = [ACTION_LABELS[key] for key in keys]
    colors = [PALETTE["red"], PALETTE["green"], PALETTE["teal"], PALETTE["amber"], PALETTE["slate"], PALETTE["violet"]]

    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=160)
    bars = ax.bar(labels, values, color=colors)
    ax.set_title("Recommended action mix", loc="left", fontsize=13, fontweight="bold", color=PALETTE["ink"])
    ax.set_ylabel("Skills")
    ax.tick_params(axis="x", labelrotation=20)
    ax.grid(axis="y", color=PALETTE["line"], linewidth=0.8)
    ax.set_axisbelow(True)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{int(bar.get_height()):,}", ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def save_decision_chart(rows: list[dict[str, str]], path: Path) -> None:
    if not HAS_MATPLOTLIB:
        save_svg_placeholder(path, "Low-signal triage decisions", "Chart rendering needs matplotlib. Table data is still available.")
        return
    low_rows = [row for row in rows if row.get("meaningfulness") in {"low_signal", "plausible_but_low_signal"}]
    counts = Counter(row.get("portfolio_decision", "") for row in low_rows)
    keys = [
        "upgrade_public",
        "merge_into_stronger_skill",
        "move_private_or_hide",
        "delete_candidate",
        "monitor",
    ]
    values = [counts.get(key, 0) for key in keys]
    labels = [DECISION_LABELS[key] for key in keys]
    colors = [PALETTE["green"], PALETTE["amber"], PALETTE["slate"], PALETTE["red"], PALETTE["teal"]]

    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=160)
    bars = ax.bar(labels, values, color=colors)
    ax.set_title("Low-signal triage decisions", loc="left", fontsize=13, fontweight="bold", color=PALETTE["ink"])
    ax.set_ylabel("Skills")
    ax.tick_params(axis="x", labelrotation=20)
    ax.grid(axis="y", color=PALETTE["line"], linewidth=0.8)
    ax.set_axisbelow(True)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{int(bar.get_height()):,}", ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def save_top_downloads_chart(rows: list[dict[str, str]], path: Path) -> None:
    if not HAS_MATPLOTLIB:
        save_svg_placeholder(path, "Top skills by downloads", "Chart rendering needs matplotlib. Table data is still available.")
        return
    top = sorted(rows, key=lambda row: to_int(row.get("downloads")), reverse=True)[:20]
    top = list(reversed(top))
    labels = [row.get("display_name") or row.get("slug") for row in top]
    values = [to_int(row.get("downloads")) for row in top]

    fig, ax = plt.subplots(figsize=(10, 7), dpi=160)
    ax.barh(labels, values, color=PALETTE["teal"])
    ax.set_title("Top skills by downloads", loc="left", fontsize=13, fontweight="bold", color=PALETTE["ink"])
    ax.set_xlabel("Downloads")
    ax.grid(axis="x", color=PALETTE["line"], linewidth=0.8)
    ax.set_axisbelow(True)
    for i, value in enumerate(values):
        ax.text(value + max(values) * 0.01, i, f"{value:,}", va="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def save_placeholder_chart(path: Path, title: str, message: str) -> None:
    if not HAS_MATPLOTLIB:
        save_svg_placeholder(path, title, message)
        return
    fig, ax = plt.subplots(figsize=(10, 5.4), dpi=160)
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold", color=PALETTE["ink"])
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=12, color=PALETTE["muted"], wrap=True)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(PALETTE["line"])
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def save_growth_chart(rows: list[dict[str, str]], path: Path, *, metric: str, title: str, color: str) -> None:
    if not HAS_MATPLOTLIB:
        save_svg_placeholder(path, title, "Chart rendering needs matplotlib. Growth data is still available.")
        return
    top = [row for row in sorted(rows, key=lambda row: (to_int(row.get(metric)), to_int(row.get("downloads"))), reverse=True) if to_int(row.get(metric)) > 0][:20]
    if not top:
        save_placeholder_chart(path, title, "Need at least two snapshots with positive growth.")
        return

    top = list(reversed(top))
    labels = [chart_label(row) for row in top]
    values = [to_int(row.get(metric)) for row in top]

    fig, ax = plt.subplots(figsize=(10, 7), dpi=160)
    ax.barh(labels, values, color=color)
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold", color=PALETTE["ink"])
    ax.set_xlabel("New events since previous snapshot")
    ax.grid(axis="x", color=PALETTE["line"], linewidth=0.8)
    ax.set_axisbelow(True)
    max_value = max(values) if values else 1
    for i, value in enumerate(values):
        ax.text(value + max_value * 0.01, i, f"+{value:,}", va="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def save_category_chart(rows: list[dict[str, str]], path: Path) -> None:
    if not HAS_MATPLOTLIB:
        save_svg_placeholder(path, "Largest skill categories", "Chart rendering needs matplotlib. Table data is still available.")
        return
    counts = Counter(row.get("category", "Other") for row in rows)
    top = counts.most_common(12)
    labels = [label for label, _ in reversed(top)]
    values = [value for _, value in reversed(top)]

    fig, ax = plt.subplots(figsize=(10, 5.4), dpi=160)
    ax.barh(labels, values, color=PALETTE["green"])
    ax.set_title("Largest skill categories", loc="left", fontsize=13, fontweight="bold", color=PALETTE["ink"])
    ax.set_xlabel("Skills")
    ax.grid(axis="x", color=PALETTE["line"], linewidth=0.8)
    ax.set_axisbelow(True)
    for i, value in enumerate(values):
        ax.text(value + max(values) * 0.01, i, f"{value:,}", va="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def save_score_scatter(rows: list[dict[str, str]], path: Path) -> None:
    if not HAS_MATPLOTLIB:
        save_svg_placeholder(path, "Meaning score versus downloads", "Chart rendering needs matplotlib. Table data is still available.")
        return
    downloads = [max(1, to_int(row.get("downloads"))) for row in rows]
    scores = [to_float(row.get("meaning_score")) for row in rows]
    comments = [to_int(row.get("comments")) for row in rows]
    sizes = [30 + min(180, to_int(row.get("installs_all_time")) * 30 + to_int(row.get("stars")) * 18) for row in rows]
    colors = [PALETTE["red"] if value > 0 else PALETTE["teal"] for value in comments]

    fig, ax = plt.subplots(figsize=(10, 5.4), dpi=160)
    ax.scatter(downloads, scores, s=sizes, color=colors, alpha=0.68, edgecolor="white", linewidth=0.6)
    ax.set_xscale("log")
    ax.set_title("Meaning score versus downloads", loc="left", fontsize=13, fontweight="bold", color=PALETTE["ink"])
    ax.set_xlabel("Downloads, log scale")
    ax.set_ylabel("Meaning score")
    ax.grid(color=PALETTE["line"], linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def save_svg_placeholder(path: Path, title: str, message: str) -> None:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="864" viewBox="0 0 1600 864" role="img" aria-label="{html.escape(title)}">
  <rect width="1600" height="864" fill="#ffffff"/>
  <rect x="1" y="1" width="1598" height="862" fill="none" stroke="#d9dde7" stroke-width="2"/>
  <text x="80" y="120" fill="#23262f" font-family="Inter, Arial, sans-serif" font-size="44" font-weight="700">{html.escape(title)}</text>
  <text x="80" y="204" fill="#6d7280" font-family="Inter, Arial, sans-serif" font-size="28">{html.escape(message)}</text>
  <text x="80" y="274" fill="#6d7280" font-family="Inter, Arial, sans-serif" font-size="22">Install matplotlib to render charts; the dashboard table and generated CSV files remain usable.</text>
</svg>
"""
    path.write_text(svg, encoding="utf-8")


def render_table_rows(rows: list[dict[str, Any]]) -> str:
    return json.dumps(rows, ensure_ascii=False, separators=(",", ":"))


def merge_growth(rows: list[dict[str, str]], growth_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    growth_by_slug = {row.get("slug", ""): row for row in growth_rows if row.get("slug")}
    merged: list[dict[str, str]] = []
    for row in rows:
        combined = dict(row)
        growth = growth_by_slug.get(row.get("slug", ""), {})
        combined["new_downloads"] = str(to_int(growth.get("new_downloads")))
        combined["new_installs"] = str(to_int(growth.get("new_installs")))
        merged.append(combined)
    return merged


def render_html(
    handle: str,
    rows: list[dict[str, str]],
    summary: dict[str, Any],
    trend_summary: dict[str, Any],
    assets: dict[str, str],
) -> str:
    clean_rows = [clean_row(row, handle) for row in rows]
    totals = summary.get("totals", {})
    counts = summary.get("counts", {})
    action_counts = counts.get("recommended_action", {})
    verdict_counts = counts.get("meaningfulness", {})
    decision_counts = counts.get("portfolio_decision", {})
    low_decision_counts = counts.get("low_signal_portfolio_decision", {})
    low_signal_count = verdict_counts.get("low_signal", 0) + verdict_counts.get("plausible_but_low_signal", 0)
    data_unavailable_count = summary.get("data_unavailable_count", verdict_counts.get("data_unavailable", 0))
    decisionable_skill_count = summary.get("decisionable_skill_count", max(0, to_int(summary.get("skill_count")) - to_int(data_unavailable_count)))
    generated = summary.get("generated_at_utc", "")
    top_score = sorted(clean_rows, key=lambda row: row["score"], reverse=True)[:8]
    action_queue = [
        row
        for row in sorted(clean_rows, key=lambda row: (-row["comments"], -row["score"], -row["downloads"]))
        if row["action"] == "respond_fix_upload"
    ][:8]
    risk_queue = [
        row
        for row in sorted(clean_rows, key=lambda row: (row["score"], row["downloads"]))
        if row["action"] in {"review_for_merge_or_private", "consider_private_or_delete"}
    ][:8]
    data_unavailable_queue = [
        row
        for row in sorted(clean_rows, key=lambda row: (row["slug"], row["display_name"]))
        if row["decision"] == "data_unavailable" or row["action"] == "data_unavailable" or row["verdict"] == "data_unavailable"
    ][:8]
    upgrade_queue = [row for row in sorted(clean_rows, key=lambda row: (-row["downloads"], -row["score"])) if row["decision"] == "upgrade_public" and row["verdict"] in {"low_signal", "plausible_but_low_signal"}][:8]
    merge_queue = [row for row in sorted(clean_rows, key=lambda row: (-row["family_size"], -row["downloads"], -row["score"])) if row["decision"] == "merge_into_stronger_skill" and row["verdict"] in {"low_signal", "plausible_but_low_signal"}][:8]
    private_queue = [row for row in sorted(clean_rows, key=lambda row: (-row["downloads"], row["score"])) if row["decision"] == "move_private_or_hide" and row["verdict"] in {"low_signal", "plausible_but_low_signal"}][:8]
    monitor_queue = [row for row in sorted(clean_rows, key=lambda row: (-row["downloads"], -row["score"])) if row["decision"] == "monitor" and row["verdict"] in {"low_signal", "plausible_but_low_signal"}][:8]
    trend_deltas = trend_summary.get("deltas", {}) if isinstance(trend_summary.get("deltas"), dict) else {}
    has_previous_snapshot = bool(trend_summary.get("has_previous"))
    snapshot_count = to_int(trend_summary.get("snapshot_count"))
    window_hours = trend_summary.get("window_hours")
    if has_previous_snapshot and isinstance(window_hours, (int, float)):
        if window_hours >= 48:
            window_label = f"{window_hours / 24:.1f} days"
        else:
            window_label = f"{window_hours:.1f} hours"
    else:
        window_label = "waiting for next snapshot"
    top_download_growth = (trend_summary.get("top_new_downloads") or [{}])[0]
    top_install_growth = (trend_summary.get("top_new_installs") or [{}])[0]
    download_growth_label = top_download_growth.get("display_name") or top_download_growth.get("slug") or "No growth yet"
    install_growth_label = top_install_growth.get("display_name") or top_install_growth.get("slug") or "No growth yet"

    def mini_list(items: list[dict[str, Any]], metric: str) -> str:
        if not items:
            return '<p class="empty">No items in this queue right now.</p>'
        out = []
        for item in items:
            title = html.escape(item["display_name"]) if item["display_name"] else slug_html(item["slug"])
            slug = slug_html(item["slug"])
            summary_text = html.escape(item["summary"][:160])
            out.append(
                f'<a class="list-item" href="{html.escape(item["url"])}" target="_blank" rel="noreferrer">'
                f'<span><strong>{title}</strong><small>{slug}</small><em>{summary_text}</em></span>'
                f'<b>{html.escape(str(item[metric]))}</b>'
                "</a>"
            )
        return "\n".join(out)

    rows_json = render_table_rows(clean_rows)
    action_options = "\n".join(
        f'<option value="{html.escape(key)}">{html.escape(label)}</option>' for key, label in ACTION_LABELS.items()
    )
    verdict_options = "\n".join(
        f'<option value="{html.escape(key)}">{html.escape(label)}</option>' for key, label in VERDICT_LABELS.items()
    )
    decision_options = "\n".join(
        f'<option value="{html.escape(key)}">{html.escape(label)}</option>' for key, label in DECISION_LABELS.items()
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ClawHub Skill Portfolio - {html.escape(handle)}</title>
  <style>
    :root {{
      --bg: #f6f7f4;
      --panel: #ffffff;
      --ink: #23262f;
      --muted: #6d7280;
      --line: #d9dde7;
      --teal: #1f7a8c;
      --green: #4f8a5b;
      --amber: #d99b2b;
      --red: #bd4f4f;
      --violet: #6c5ce7;
      --slate: #44546a;
      --shadow: 0 14px 34px rgba(35, 38, 47, .09);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }}
    a {{ color: inherit; }}
    .shell {{ width: min(1440px, calc(100vw - 32px)); margin: 0 auto; }}
    header {{
      background: #23313a;
      color: #fff;
      border-bottom: 6px solid var(--amber);
    }}
    .topbar {{
      min-height: 220px;
      display: grid;
      grid-template-columns: 1.2fr .8fr;
      gap: 28px;
      align-items: end;
      padding: 34px 0 28px;
    }}
    h1 {{ margin: 0; font-size: clamp(28px, 4vw, 52px); line-height: 1.02; letter-spacing: 0; }}
    .subtitle {{ max-width: 760px; margin: 14px 0 0; color: rgba(255,255,255,.78); font-size: 16px; line-height: 1.55; }}
    .stamp {{ justify-self: end; text-align: right; color: rgba(255,255,255,.72); font-size: 13px; line-height: 1.7; }}
    .stamp strong {{ color: #fff; }}
    main {{ padding: 24px 0 48px; }}
    .kpis {{ display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 12px; margin-top: -48px; }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}
    .kpi {{ min-height: 112px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between; }}
    .kpi span {{ color: var(--muted); font-size: 12px; text-transform: uppercase; font-weight: 700; }}
    .kpi strong {{ font-size: clamp(24px, 2.6vw, 38px); line-height: 1; }}
    .kpi em {{ color: var(--muted); font-style: normal; font-size: 12px; }}
    .growth-kpis {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 12px 0 16px; }}
    .growth-kpi {{ min-height: 92px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; }}
    .growth-kpi span {{ color: var(--muted); font-size: 12px; text-transform: uppercase; font-weight: 700; }}
    .growth-kpi strong {{ font-size: clamp(20px, 2vw, 30px); line-height: 1; }}
    .growth-kpi em {{ color: var(--muted); font-style: normal; font-size: 12px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .grid-2 {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; margin-top: 16px; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; margin-top: 16px; }}
    .grid-4 {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; margin-top: 16px; }}
    section {{ margin-top: 28px; }}
    .section-title {{ display: flex; justify-content: space-between; align-items: end; gap: 16px; margin-bottom: 12px; }}
    h2 {{ margin: 0; font-size: 22px; letter-spacing: 0; }}
    .section-title p {{ margin: 0; color: var(--muted); font-size: 13px; max-width: 680px; line-height: 1.5; }}
    .chart {{ padding: 16px; }}
    .chart img {{ display: block; width: 100%; height: auto; border-radius: 6px; border: 1px solid var(--line); background: #fff; }}
    .queue {{ padding: 16px; min-height: 320px; }}
    .queue h3 {{ margin: 0 0 12px; font-size: 16px; }}
    .list-item {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 12px;
      padding: 12px 0;
      text-decoration: none;
      border-top: 1px solid var(--line);
    }}
    .list-item span {{ min-width: 0; }}
    .list-item strong, .list-item small, .list-item em {{ display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .list-item small {{ color: var(--muted); margin-top: 2px; font-size: 12px; }}
    .list-item em {{ color: var(--muted); font-style: normal; margin-top: 4px; font-size: 12px; }}
    .list-item b {{ align-self: center; color: var(--teal); font-size: 20px; }}
    .slug-token {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; font-size: .92em; color: var(--muted); background: transparent; unicode-bidi: isolate; }}
    .table-card {{ padding: 14px; }}
    .controls {{ display: grid; grid-template-columns: 2fr repeat(4, minmax(150px, 1fr)); gap: 10px; margin-bottom: 12px; }}
    input, select {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px 11px;
      font: inherit;
      background: #fff;
      color: var(--ink);
    }}
    .table-wrap {{ overflow: auto; border: 1px solid var(--line); border-radius: 8px; background: #fff; max-height: 680px; }}
    table {{ width: 100%; min-width: 1420px; border-collapse: collapse; font-size: 13px; }}
    th, td {{ padding: 10px 11px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ position: sticky; top: 0; z-index: 1; background: #eef1f4; font-size: 11px; text-transform: uppercase; color: #4b5563; cursor: pointer; }}
    td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
    .skill-cell a {{ color: var(--ink); font-weight: 700; text-decoration: none; }}
    .skill-cell small {{ display: block; color: var(--muted); margin-top: 3px; max-width: 340px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .pill {{ display: inline-flex; align-items: center; min-height: 24px; padding: 3px 8px; border-radius: 999px; background: #eef1f4; color: #3f4652; font-size: 12px; white-space: nowrap; }}
    .pill.action-respond_fix_upload {{ background: #ffe8e6; color: #9c3838; }}
    .pill.action-keep_public {{ background: #e7f3e8; color: #356f44; }}
    .pill.action-curate_or_improve {{ background: #e5f3f5; color: #166677; }}
    .pill.action-review_for_merge_or_private {{ background: #fff2d7; color: #845b12; }}
    .pill.action-consider_private_or_delete {{ background: #e9edf2; color: #44546a; }}
    .pill.action-data_unavailable {{ background: #eeeafc; color: #5642c6; }}
    .pill.decision-fix_and_reply {{ background: #ffe8e6; color: #9c3838; }}
    .pill.decision-upgrade_public {{ background: #e7f3e8; color: #356f44; }}
    .pill.decision-merge_into_stronger_skill {{ background: #fff2d7; color: #845b12; }}
    .pill.decision-move_private_or_hide {{ background: #e9edf2; color: #44546a; }}
    .pill.decision-delete_candidate {{ background: #f7dedc; color: #9c3838; }}
    .pill.decision-monitor {{ background: #e5f3f5; color: #166677; }}
    .pill.decision-keep_public {{ background: #edf7ea; color: #356f44; }}
    .pill.decision-data_unavailable {{ background: #eeeafc; color: #5642c6; }}
    .workflow {{ padding: 18px; }}
    .workflow ol {{ margin: 8px 0 0; padding-left: 22px; color: var(--muted); line-height: 1.65; }}
    .workflow strong {{ color: var(--ink); }}
    .file-links {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin-top: 12px; }}
    .file-links a {{ display: block; padding: 11px 12px; border: 1px solid var(--line); border-radius: 6px; text-decoration: none; background: #fff; font-size: 13px; font-weight: 700; }}
    .file-links small {{ display: block; margin-top: 3px; color: var(--muted); font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .empty {{ color: var(--muted); }}
    footer {{ color: var(--muted); font-size: 12px; line-height: 1.6; padding: 22px 0 0; }}
    @media (max-width: 1040px) {{
      .topbar {{ grid-template-columns: 1fr; min-height: 260px; }}
      .stamp {{ justify-self: start; text-align: left; }}
      .kpis {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
      .growth-kpis {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .grid-2, .grid-3, .grid-4 {{ grid-template-columns: 1fr; }}
      .file-links {{ grid-template-columns: 1fr; }}
      .controls {{ grid-template-columns: 1fr 1fr; }}
    }}
    @media (max-width: 680px) {{
      .shell {{ width: min(100vw - 18px, 1440px); }}
      .topbar {{ padding-top: 24px; }}
      .kpis {{ grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: -34px; }}
      .growth-kpis {{ grid-template-columns: 1fr; }}
      .controls {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="shell topbar">
      <div>
        <h1>ClawHub Skill Portfolio</h1>
        <p class="subtitle">A maintenance view for deciding which skills are meaningful, which low-signal skills should be upgraded, merged, moved private, or monitored, and where public cleanup should start.</p>
      </div>
      <div class="stamp">
        <div><strong>@{html.escape(handle)}</strong></div>
        <div>Generated: {html.escape(generated)}</div>
        <div>Source: public ClawHub profile, listing, and skill detail APIs</div>
      </div>
    </div>
  </header>

  <main class="shell">
    <div class="kpis">
      <div class="card kpi"><span>Skills</span><strong>{fmt_num(summary.get("skill_count"))}</strong><em>{fmt_num(decisionable_skill_count)} decisionable today</em></div>
      <div class="card kpi"><span>Low Signal</span><strong>{fmt_num(low_signal_count)}</strong><em>low + plausible-low</em></div>
      <div class="card kpi"><span>Upgrade</span><strong>{fmt_num(low_decision_counts.get("upgrade_public", 0))}</strong><em>keep public, improve</em></div>
      <div class="card kpi"><span>Merge</span><strong>{fmt_num(low_decision_counts.get("merge_into_stronger_skill", 0))}</strong><em>consolidate family</em></div>
      <div class="card kpi"><span>Private/Hide</span><strong>{fmt_num(low_decision_counts.get("move_private_or_hide", 0))}</strong><em>remove public noise</em></div>
      <div class="card kpi"><span>Monitor</span><strong>{fmt_num(low_decision_counts.get("monitor", 0))}</strong><em>recheck later</em></div>
      <div class="card kpi"><span>Data Unavailable</span><strong>{fmt_num(data_unavailable_count)}</strong><em>no decision today</em></div>
    </div>

    <section>
      <div class="section-title">
        <h2>Portfolio Health</h2>
        <p>Action buckets are generated from public usage signals plus maintainability signals. The low-signal decision layer answers whether a skill should be upgraded, merged, moved private, or monitored.</p>
      </div>
      <div class="grid-2">
        <div class="card chart"><img src="{html.escape(assets["action"])}" alt="Recommended action mix"></div>
        <div class="card chart"><img src="{html.escape(assets["decision"])}" alt="Low-signal triage decisions"></div>
      </div>
      <div class="grid-2">
        <div class="card chart"><img src="{html.escape(assets["scatter"])}" alt="Meaning score versus downloads"></div>
        <div class="card chart"><img src="{html.escape(assets["category"])}" alt="Largest skill categories"></div>
      </div>
      <div class="grid-2">
        <div class="card chart"><img src="{html.escape(assets["downloads"])}" alt="Top skills by downloads"></div>
        <div class="card workflow">
          <h3>Low-Signal Rule of Thumb</h3>
          <ol>
            <li><strong>Upgrade:</strong> high downloads or real engagement, but weak packaging.</li>
            <li><strong>Merge:</strong> repeated family pattern with weak standalone demand.</li>
            <li><strong>Private/Hide:</strong> useful as a capability unit but noisy as a public product.</li>
            <li><strong>Monitor:</strong> plausible public value, not enough evidence yet.</li>
          </ol>
        </div>
      </div>
    </section>

    <section>
      <div class="section-title">
        <h2>Growth Watch</h2>
        <p>Compares the latest snapshot with the previous one so the most recently popular skills surface before older download totals dominate the queue.</p>
      </div>
      <div class="growth-kpis">
        <div class="card growth-kpi"><span>Snapshots</span><strong>{fmt_num(snapshot_count)}</strong><em>{html.escape(window_label)}</em></div>
        <div class="card growth-kpi"><span>New Downloads</span><strong>{fmt_delta(trend_deltas.get("new_downloads", 0))}</strong><em>{html.escape(download_growth_label)}</em></div>
        <div class="card growth-kpi"><span>New Installs</span><strong>{fmt_delta(trend_deltas.get("new_installs", 0))}</strong><em>{html.escape(install_growth_label)}</em></div>
        <div class="card growth-kpi"><span>New Skills</span><strong>{fmt_delta(trend_deltas.get("new_skill_count", 0))}</strong><em>since previous snapshot</em></div>
      </div>
      <div class="grid-2">
        <div class="card chart"><img src="{html.escape(assets["growth_downloads"])}" alt="Top 20 skills by new downloads"></div>
        <div class="card chart"><img src="{html.escape(assets["growth_installs"])}" alt="Top 20 skills by new installs"></div>
      </div>
    </section>

    <section>
      <div class="section-title">
        <h2>Maintenance Queues</h2>
        <p>Commented skills get the first queue because they represent active user feedback. Failed detail fetches are separated so they do not drive maintenance decisions.</p>
      </div>
      <div class="grid-4">
        <div class="card queue">
          <h3>Respond / Fix / Upload</h3>
          {mini_list(action_queue, "comments")}
        </div>
        <div class="card queue">
          <h3>Top Meaningful Skills</h3>
          {mini_list(top_score, "score")}
        </div>
        <div class="card queue">
          <h3>Review / Private Candidates</h3>
          {mini_list(risk_queue, "score")}
        </div>
        <div class="card queue">
          <h3>Data Unavailable</h3>
          {mini_list(data_unavailable_queue, "downloads")}
        </div>
      </div>
    </section>

    <section>
      <div class="section-title">
        <h2>Low-Signal Triage</h2>
        <p>These queues focus only on low and plausible-low signal skills. They are ordered to surface the most useful cleanup work first.</p>
      </div>
      <div class="grid-4">
        <div class="card queue">
          <h3>Upgrade Public</h3>
          {mini_list(upgrade_queue, "downloads")}
        </div>
        <div class="card queue">
          <h3>Merge Families</h3>
          {mini_list(merge_queue, "family_size")}
        </div>
        <div class="card queue">
          <h3>Private / Hide</h3>
          {mini_list(private_queue, "downloads")}
        </div>
        <div class="card queue">
          <h3>Monitor</h3>
          {mini_list(monitor_queue, "downloads")}
        </div>
      </div>
    </section>

    <section>
      <div class="section-title">
        <h2>Skill Explorer</h2>
        <p>Search, filter, and sort all collected skills. The table is embedded in this file, so it works offline after generation.</p>
      </div>
      <div class="card table-card">
        <div class="controls">
          <input id="search" type="search" placeholder="Search slug, name, summary, decision reason, flags">
          <select id="decision"><option value="">All decisions</option>{decision_options}</select>
          <select id="action"><option value="">All actions</option>{action_options}</select>
          <select id="verdict"><option value="">All verdicts</option>{verdict_options}</select>
          <select id="category"><option value="">All categories</option></select>
        </div>
        <div class="table-wrap">
          <table id="skill-table">
            <thead>
              <tr>
                <th data-sort="score">Score</th>
                <th data-sort="display_name">Skill</th>
                <th data-sort="decision">Decision</th>
                <th data-sort="action">Action</th>
                <th data-sort="verdict">Verdict</th>
                <th data-sort="downloads">Downloads</th>
                <th data-sort="new_downloads">New DL</th>
                <th data-sort="installs">Installs</th>
                <th data-sort="new_installs">New Installs</th>
                <th data-sort="stars">Stars</th>
                <th data-sort="comments">Comments</th>
                <th data-sort="versions">Versions</th>
                <th data-sort="category">Category</th>
                <th data-sort="merge_target">Merge Target</th>
                <th data-sort="decision_reason">Reason</th>
                <th data-sort="flags">Flags</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </section>

    <section>
      <div class="section-title">
        <h2>Operating Loop</h2>
        <p>This is the maintenance workflow to turn portfolio data into public quality improvements.</p>
      </div>
      <div class="card workflow">
        <ol>
          <li><strong>Collect:</strong> refresh profile, listing, and skill detail stats with <code>scripts/update_all.py</code>.</li>
          <li><strong>Snapshot:</strong> save the latest metric snapshot and compare it with the previous run to find new download and install growth.</li>
          <li><strong>Gate:</strong> move failed skill-detail fetches into <code>data_unavailable</code> and make no decision for them today.</li>
          <li><strong>Triage:</strong> start with skills that have comments, installs, stars, or unusually high downloads.</li>
          <li><strong>Fix:</strong> inspect the source skill, reproduce the reported problem, patch the skill, and update README/changelog metadata.</li>
          <li><strong>Validate:</strong> run <code>clawhub scan ./path/to/skill</code> before publishing.</li>
          <li><strong>Upload:</strong> publish the fixed version with <code>clawhub publish ./path/to/skill</code>.</li>
          <li><strong>Respond:</strong> reply to the user comment with what changed, the new version, and any known limitation.</li>
          <li><strong>Consolidate:</strong> move low-signal duplicates into private libraries or merge them into stronger public skills.</li>
        </ol>
        <div class="file-links">
          <a href="action_plans/{html.escape(handle)}_action_plan.md">Action Plan<small>Markdown review brief</small></a>
          <a href="action_plans/{html.escape(handle)}_hide_plan.csv">Hide Plan CSV<small>review before hiding</small></a>
          <a href="action_plans/{html.escape(handle)}_private_backlog_plan.csv">Private Backlog CSV<small>utility-shaped skills</small></a>
          <a href="action_plans/{html.escape(handle)}_merge_plan.csv">Merge Plan CSV<small>canonical target mapping</small></a>
          <a href="action_plans/{html.escape(handle)}_upgrade_plan.csv">Upgrade Plan CSV<small>public improvement queue</small></a>
          <a href="approval_packets/{html.escape(handle)}_approval_board.md">Approval Board<small>approve one batch at a time</small></a>
          <a href="approval_packets/{html.escape(handle)}_approval_manifest.json">Approval Manifest<small>machine-readable evidence</small></a>
          <a href="approval_packets/{html.escape(handle)}_approval_commands.sh">Approval Commands<small>commented by default</small></a>
          <a href="../data/processed/{html.escape(handle)}_skill_growth.csv">Growth CSV<small>new downloads and installs</small></a>
          <a href="../data/processed/{html.escape(handle)}_trend_summary.json">Trend Summary<small>latest versus previous snapshot</small></a>
          <a href="../data/processed/{html.escape(handle)}_data_unavailable.csv">Data Unavailable CSV<small>failed detail fetches, no decision today</small></a>
          <a href="action_plans/{html.escape(handle)}_data_unavailable_plan.csv">Data Unavailable Plan<small>blocked queue only</small></a>
          <a href="bulk_cleanup/{html.escape(handle)}_bulk_cleanup_report.md">Bulk Cleanup Report<small>clear delisting recommendation</small></a>
          <a href="bulk_cleanup/{html.escape(handle)}_bulk_approval_board.md">Bulk Approval Board<small>approve delisting phases</small></a>
          <a href="bulk_cleanup/{html.escape(handle)}_bulk_approval_manifest.json">Bulk Approval Manifest<small>phase evidence JSON</small></a>
          <a href="bulk_cleanup/{html.escape(handle)}_phase1_clear_hide.csv">Phase 1 Hide CSV<small>strongest bulk-risk tail</small></a>
          <a href="bulk_cleanup/{html.escape(handle)}_phase2_hide_after_spotcheck.csv">Phase 2 Hide CSV<small>spot-check then hide</small></a>
          <a href="action_plans/{html.escape(handle)}_hide_review_commands.sh">Hide Commands<small>commented out by default</small></a>
          <a href="action_plans/{html.escape(handle)}_merge_review_commands.sh">Merge Commands<small>commented out by default</small></a>
        </div>
      </div>
    </section>

    <footer>
      Scoring is directional, not a policy decision. A skill is considered meaningful when it has direct engagement, strong usage, or enough metadata and iteration history to justify public curation.
      Public stats can change; regenerate this page on a schedule before making bulk publishing decisions.
    </footer>
  </main>

  <script>
    const rows = {rows_json};
    const actionLabels = {json.dumps(ACTION_LABELS, ensure_ascii=False)};
    const verdictLabels = {json.dumps(VERDICT_LABELS, ensure_ascii=False)};
    const decisionLabels = {json.dumps(DECISION_LABELS, ensure_ascii=False)};
    let sortKey = "score";
    let sortDir = -1;

    const tbody = document.querySelector("#skill-table tbody");
    const search = document.querySelector("#search");
    const decision = document.querySelector("#decision");
    const action = document.querySelector("#action");
    const verdict = document.querySelector("#verdict");
    const category = document.querySelector("#category");

    [...new Set(rows.map(row => row.category).filter(Boolean))].sort().forEach(value => {{
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      category.appendChild(option);
    }});

    function number(value) {{
      return Number(value || 0).toLocaleString();
    }}

    function label(map, value) {{
      return map[value] || value || "";
    }}

    function renderSlug(value) {{
      return `<code class="slug-token notranslate" translate="no">${{escapeHtml(value || "")}}</code>`;
    }}

    function renderSkillTitle(row) {{
      if (row.display_name) return escapeHtml(row.display_name);
      return `<span class="notranslate" translate="no">${{escapeHtml(row.slug || "")}}</span>`;
    }}

    function text(row) {{
      return [row.slug, row.display_name, row.summary, row.decision_reason, row.flags, row.category, row.merge_target].join(" ").toLowerCase();
    }}

    function compare(a, b) {{
      const av = a[sortKey];
      const bv = b[sortKey];
      if (typeof av === "number" && typeof bv === "number") return (av - bv) * sortDir;
      return String(av || "").localeCompare(String(bv || "")) * sortDir;
    }}

    function render() {{
      const query = search.value.trim().toLowerCase();
      const filtered = rows
        .filter(row => !query || text(row).includes(query))
        .filter(row => !decision.value || row.decision === decision.value)
        .filter(row => !action.value || row.action === action.value)
        .filter(row => !verdict.value || row.verdict === verdict.value)
        .filter(row => !category.value || row.category === category.value)
        .sort(compare);

      tbody.innerHTML = filtered.map(row => `
        <tr>
          <td class="num">${{row.score.toFixed(1)}}</td>
          <td class="skill-cell"><a href="${{row.url}}" target="_blank" rel="noreferrer">${{renderSkillTitle(row)}}</a><small>${{renderSlug(row.slug)}} - ${{escapeHtml(row.summary || "")}}</small></td>
          <td><span class="pill decision-${{row.decision}}">${{escapeHtml(label(decisionLabels, row.decision))}}</span></td>
          <td><span class="pill action-${{row.action}}">${{escapeHtml(label(actionLabels, row.action))}}</span></td>
          <td><span class="pill">${{escapeHtml(label(verdictLabels, row.verdict))}}</span></td>
          <td class="num">${{number(row.downloads)}}</td>
          <td class="num">${{number(row.new_downloads)}}</td>
          <td class="num">${{number(row.installs)}}</td>
          <td class="num">${{number(row.new_installs)}}</td>
          <td class="num">${{number(row.stars)}}</td>
          <td class="num">${{number(row.comments)}}</td>
          <td class="num">${{number(row.versions)}}</td>
          <td>${{escapeHtml(row.category)}}</td>
          <td>${{row.merge_target ? renderSlug(row.merge_target) : ""}}</td>
          <td>${{escapeHtml(row.decision_reason || "")}}</td>
          <td>${{escapeHtml((row.flags || "").replaceAll("|", ", "))}}</td>
        </tr>
      `).join("");
    }}

    function escapeHtml(value) {{
      return String(value).replace(/[&<>"']/g, char => ({{
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
      }}[char]));
    }}

    [search, decision, action, verdict, category].forEach(element => element.addEventListener("input", render));
    document.querySelectorAll("th[data-sort]").forEach(th => {{
      th.addEventListener("click", () => {{
        const next = th.dataset.sort;
        if (sortKey === next) sortDir *= -1;
        else {{
          sortKey = next;
          sortDir = ["score", "downloads", "new_downloads", "installs", "new_installs", "stars", "comments", "versions", "family_size"].includes(next) ? -1 : 1;
        }}
        render();
      }});
    }});
    render();
  </script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handle", default="harrylabsj")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--out-dir", default="reports")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    assets_dir = out_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    rows = read_csv(data_dir / "processed" / f"{args.handle}_skill_analysis.csv")
    summary = read_json(data_dir / "processed" / f"{args.handle}_summary.json")
    growth_rows = read_csv_if_exists(data_dir / "processed" / f"{args.handle}_skill_growth.csv")
    trend_summary = read_json_if_exists(data_dir / "processed" / f"{args.handle}_trend_summary.json")
    rows = merge_growth(rows, growth_rows)

    chart_ext = "png" if HAS_MATPLOTLIB else "svg"
    chart_files = {
        "action": f"assets/action_mix.{chart_ext}",
        "decision": f"assets/low_signal_decision_mix.{chart_ext}",
        "downloads": f"assets/top_downloads.{chart_ext}",
        "growth_downloads": f"assets/top_new_downloads.{chart_ext}",
        "growth_installs": f"assets/top_new_installs.{chart_ext}",
        "category": f"assets/category_mix.{chart_ext}",
        "scatter": f"assets/score_scatter.{chart_ext}",
    }
    save_action_chart(rows, out_dir / chart_files["action"])
    save_decision_chart(rows, out_dir / chart_files["decision"])
    save_top_downloads_chart(rows, out_dir / chart_files["downloads"])
    save_growth_chart(growth_rows, out_dir / chart_files["growth_downloads"], metric="new_downloads", title="Top 20 by new downloads", color=PALETTE["violet"])
    save_growth_chart(growth_rows, out_dir / chart_files["growth_installs"], metric="new_installs", title="Top 20 by new installs", color=PALETTE["green"])
    save_category_chart(rows, out_dir / chart_files["category"])
    save_score_scatter(rows, out_dir / chart_files["scatter"])

    html_text = render_html(args.handle, rows, summary, trend_summary, chart_files)
    output_path = out_dir / "index.html"
    output_path.write_text(html_text, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
