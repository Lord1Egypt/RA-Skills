#!/usr/bin/env python3
"""
Unified archive query entrypoint for AlphaPai and local knowledge bases.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from registry import SourceQueryRequest, select_adapters


WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
ALPHAPAI_SCRIPT_DIR = WORKSPACE_ROOT / "skills/alphapai-scraper/scripts"
sys.path.insert(0, str(ALPHAPAI_SCRIPT_DIR))

from analyze import run_ai_analysis  # type: ignore  # noqa: E402
from common import load_settings as load_alphapai_settings  # type: ignore  # noqa: E402


OUTPUT_ROOT = Path.home() / ".openclaw/data/research-archive-query"
NO_RESULT_TEMPLATE = "最近{days:g}天未在指定归档范围内找到与“{query}”相关的内容"
NEGATION_HINTS = ["无直接关系", "不相关", "无关", "没有关系", "关联不大"]


def ensure_output_dirs() -> dict[str, Path]:
    report_dir = OUTPUT_ROOT / "reports"
    runtime_dir = OUTPUT_ROOT / "runtime"
    for path in (OUTPUT_ROOT, report_dir, runtime_dir):
        path.mkdir(parents=True, exist_ok=True)
    return {"base_dir": OUTPUT_ROOT, "report_dir": report_dir, "runtime_dir": runtime_dir}


def run_json_command(command: list[str]) -> Any:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "command failed")
    return json.loads(result.stdout or "null")


def normalize_alphapai_item(item: dict[str, Any], *, retrieval_mode: str) -> dict[str, Any]:
    return {
        "source": "alphapai",
        "source_label": "AlphaPai",
        "doc_id": str(item.get("id") or ""),
        "title": str(item.get("title") or "未命名点评"),
        "content": str(item.get("content") or ""),
        "summary": str(item.get("content") or "")[:240],
        "timestamp": str(item.get("scraped_at") or ""),
        "time_label": str(item.get("time_label") or ""),
        "scope": str(item.get("scope") or "alphapai"),
        "visibility": str(item.get("visibility") or "shared"),
        "container": "alphapai",
        "path": str(item.get("raw_file") or ""),
        "retrieval_modes": sorted(set(item.get("retrieval_modes") or [retrieval_mode])),
        "exact_score": float(item.get("exact_score") or 0.0),
        "vector_score": float(item.get("vector_score") or 0.0),
        "score": float(item.get("retrieval_score") or item.get("vector_score") or item.get("exact_score") or 0.0),
    }


def normalize_kb_item(item: dict[str, Any], *, retrieval_mode: str) -> dict[str, Any]:
    content = str(item.get("content") or item.get("summary") or item.get("text") or "")
    return {
        "source": "knowledge_bases",
        "source_label": "Knowledge Bases",
        "doc_id": str(item.get("doc_id") or item.get("source") or item.get("title") or ""),
        "title": str(item.get("title") or item.get("source") or "未命名资料"),
        "content": content,
        "summary": content[:240],
        "timestamp": str(item.get("updated_at") or item.get("ingested_at") or ""),
        "time_label": str(item.get("updated_at") or item.get("ingested_at") or ""),
        "scope": str(item.get("scope") or ""),
        "visibility": str(item.get("visibility") or "shared"),
        "container": str(item.get("kb") or "knowledge_bases"),
        "path": str(item.get("source_path") or item.get("source") or ""),
        "retrieval_modes": [retrieval_mode],
        "exact_score": 1.0 if retrieval_mode == "exact" else 0.0,
        "vector_score": float(item.get("score") or 0.0) if retrieval_mode == "vector" else 0.0,
        "score": float(item.get("score") or 1.0 if retrieval_mode == "exact" else 0.0),
    }


def normalize_results(source_name: str, payload: Any, *, retrieval_mode: str) -> list[dict[str, Any]]:
    if source_name == "alphapai":
        items = list((payload or {}).get("items") or [])
        return [normalize_alphapai_item(item, retrieval_mode=retrieval_mode) for item in items]
    if source_name == "knowledge_bases":
        items = list(payload or [])
        return [normalize_kb_item(item, retrieval_mode=retrieval_mode) for item in items]
    return []


def merge_hits(hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for item in hits:
        key = f"{item['source']}::{item['container']}::{item['doc_id']}"
        existing = merged.get(key)
        if not existing:
            merged[key] = dict(item)
            continue
        modes = set(existing.get("retrieval_modes") or [])
        modes.update(item.get("retrieval_modes") or [])
        existing["retrieval_modes"] = sorted(modes)
        existing["exact_score"] = max(float(existing.get("exact_score") or 0.0), float(item.get("exact_score") or 0.0))
        existing["vector_score"] = max(float(existing.get("vector_score") or 0.0), float(item.get("vector_score") or 0.0))
        existing["score"] = max(
            float(existing.get("score") or 0.0),
            float(existing.get("exact_score") or 0.0) * 1.1 + float(existing.get("vector_score") or 0.0),
            float(item.get("score") or 0.0),
        )
        if len(item.get("content") or "") > len(existing.get("content") or ""):
            existing["content"] = item.get("content") or existing.get("content")
            existing["summary"] = item.get("summary") or existing.get("summary")
        if item.get("timestamp") and item["timestamp"] > str(existing.get("timestamp") or ""):
            existing["timestamp"] = item["timestamp"]
            existing["time_label"] = item.get("time_label") or existing.get("time_label")
    return sorted(
        [_apply_precision_hints(item) for item in merged.values()],
        key=lambda item: (float(item.get("score") or 0.0), item.get("timestamp") or ""),
        reverse=True,
    )


def _apply_precision_hints(item: dict[str, Any]) -> dict[str, Any]:
    text = f"{item.get('title', '')}\n{item.get('content', '')}"
    penalty = 0.35 if any(marker in text for marker in NEGATION_HINTS) else 0.0
    if penalty:
        item["score"] = max(float(item.get("score") or 0.0) - penalty, 0.0)
        item["negation_hint"] = True
    return item


def query_sources(
    *,
    query: str,
    days: float,
    limit: int,
    retrieval_mode: str,
    source_names: list[str] | None,
    include_private: bool,
    exclude_kbs: list[str],
) -> dict[str, Any]:
    request = SourceQueryRequest(
        query=query,
        days=days,
        limit=limit,
        include_private=include_private,
        exclude_kbs=tuple(exclude_kbs),
    )
    hits: list[dict[str, Any]] = []
    source_meta: list[dict[str, Any]] = []
    for adapter in select_adapters(source_names):
        exact_count = 0
        vector_count = 0
        errors: list[str] = []
        if retrieval_mode in {"exact", "hybrid"} and adapter.supports_exact:
            try:
                payload = run_json_command(adapter.build_exact_command(request) or [])
                normalized = normalize_results(adapter.name, payload, retrieval_mode="exact")
                exact_count = len(normalized)
                hits.extend(normalized)
            except Exception as exc:
                errors.append(f"exact: {exc}")
        if retrieval_mode in {"vector", "hybrid"} and adapter.supports_vector:
            try:
                payload = run_json_command(adapter.build_vector_command(request) or [])
                normalized = normalize_results(adapter.name, payload, retrieval_mode="vector")
                vector_count = len(normalized)
                hits.extend(normalized)
            except Exception as exc:
                errors.append(f"vector: {exc}")
        source_meta.append(
            {
                "source": adapter.name,
                "label": adapter.label,
                "exact_count": exact_count,
                "vector_count": vector_count,
                "errors": errors,
            }
        )

    merged = merge_hits(hits)[:limit]
    return {
        "query": query,
        "days": days,
        "retrieval_mode": retrieval_mode,
        "include_private": include_private,
        "exclude_kbs": exclude_kbs,
        "sources": source_meta,
        "items": merged,
        "matched": len(merged),
    }


def build_summary_prompt(query: str, days: float, items: list[dict[str, Any]]) -> str:
    snippets: list[str] = []
    for index, item in enumerate(items[:20], start=1):
        snippets.extend(
            [
                f"[{index:02d}] 来源: {item['source_label']} / {item['container']}",
                f"标题: {item['title']}",
                f"时间: {item['timestamp'] or item['time_label']}",
                f"命中方式: {', '.join(item.get('retrieval_modes') or [])}",
                (item.get("content") or "")[:600],
                "",
            ]
        )
    evidence = "\n".join(snippets).strip()
    return f"""你是一位本地投研资料库检索助手。请根据最近 {days:g} 天关于“{query}”的命中文本，生成一份适合手机阅读的中文摘要。

必须遵守以下要求：
1. 第一段必须叫“检索结论”，直接回答最近 {days:g} 天关于“{query}”有哪些确定更新。
2. 第二部分必须叫“时间线 / 重点更新”，优先按时间顺序列出高价值变化。
3. 第三部分必须叫“行业 / 标的归类”，按行业或具体标的分组。
4. 第四部分必须叫“边际变化”，重点突出加单、涨价、公告、订单、政策、业绩、预期差。
5. 第五部分必须叫“来源分布”，指出这些信息主要来自哪些库或归档源。
6. 最后一部分必须叫“待验证”，单独放传闻、重复或证据弱的内容。
7. 总字数控制在 900-1200 字，每个要点尽量 1-2 行，适合手机阅读。
8. 重要公司、行业、产品关键词请加粗。

建议输出骨架：
# 统一归档检索摘要
## 检索结论
## 时间线 / 重点更新
## 行业 / 标的归类
## 边际变化
## 来源分布
## 待验证

下面是命中的原文片段：

{evidence}
"""


def fallback_summary(query: str, days: float, items: list[dict[str, Any]]) -> str:
    by_source: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        by_source.setdefault(item["source_label"], []).append(item)

    lines = [
        "# 统一归档检索摘要",
        "",
        "## 检索结论",
        f"- 最近 {days:g} 天关于“{query}”共命中 {len(items)} 条资料，重点线索已经按来源合并去重。",
        "",
        "## 时间线 / 重点更新",
    ]
    for item in items[:8]:
        lines.append(
            f"- [{item['source_label']}] {item['timestamp'] or item['time_label']} | {item['title']} | {(item.get('summary') or '')[:100]}"
        )
    if len(lines) == 6:
        lines.append("- 暂无足够高质量命中。")

    lines.extend(["", "## 行业 / 标的归类"])
    seen_titles: set[str] = set()
    for item in items[:10]:
        title = item["title"]
        if title in seen_titles:
            continue
        seen_titles.add(title)
        lines.append(f"- {title}")

    lines.extend(["", "## 边际变化"])
    for item in items[:6]:
        lines.append(f"- {(item.get('summary') or item.get('content') or '')[:120]}")

    lines.extend(["", "## 来源分布"])
    for source_label, source_items in by_source.items():
        lines.append(f"- {source_label}: {len(source_items)} 条")

    lines.extend(
        [
            "",
            "## 待验证",
            "- 当前为规则兜底版摘要，建议结合原文和正式 AI 摘要进一步核实。",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def generate_report(result: dict[str, Any]) -> dict[str, Any]:
    dirs = ensure_output_dirs()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = dirs["report_dir"] / f"{stamp}_unified_query.md"
    meta_path = dirs["runtime_dir"] / f"{stamp}_unified_query.json"

    if not result["items"]:
        message = NO_RESULT_TEMPLATE.format(days=result["days"], query=result["query"])
        report_path.write_text(message + "\n", encoding="utf-8")
        meta_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"ok": True, "matched": 0, "report_file": str(report_path), "meta_file": str(meta_path), "message": message}

    prompt = build_summary_prompt(result["query"], result["days"], result["items"])
    settings = load_alphapai_settings(None)
    report = run_ai_analysis(prompt, settings)
    engine = "ai"
    if not report:
        report = fallback_summary(result["query"], result["days"], result["items"])
        engine = "fallback"

    report_path.write_text(report.strip() + "\n", encoding="utf-8")
    payload = dict(result)
    payload["engine"] = engine
    payload["report_file"] = str(report_path)
    meta_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "ok": True,
        "matched": result["matched"],
        "report_file": str(report_path),
        "meta_file": str(meta_path),
        "engine": engine,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified archive query")
    parser.add_argument("--query", required=True, help="Query topic or entity")
    parser.add_argument("--days", type=float, default=7, help="Look back N days")
    parser.add_argument("--limit", type=int, default=30, help="Maximum merged hits")
    parser.add_argument(
        "--mode",
        choices=["exact", "vector", "hybrid"],
        default="hybrid",
        help="Retrieval mode",
    )
    parser.add_argument("--sources", help="Comma-separated source names, e.g. alphapai,knowledge_bases")
    parser.add_argument("--include-private", action="store_true", help="Include private scopes such as personal")
    parser.add_argument("--exclude-kb", action="append", default=[], help="Exclude KB names when querying knowledge_bases")
    parser.add_argument("--json", action="store_true", help="Print merged retrieval result as JSON")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    sources = [item.strip() for item in (args.sources or "").split(",") if item.strip()] or None
    result = query_sources(
        query=args.query,
        days=args.days,
        limit=args.limit,
        retrieval_mode=args.mode,
        source_names=sources,
        include_private=args.include_private,
        exclude_kbs=args.exclude_kb,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    report = generate_report(result)
    if report["ok"]:
        print(report["report_file"])
        return 0
    print(report.get("error", "query failed"))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
