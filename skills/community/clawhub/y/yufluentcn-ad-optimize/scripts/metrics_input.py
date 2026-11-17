"""CLI 广告指标入参（与 tokenapi_harness.ad_metrics 保持语义一致）。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _summary_lines(summary: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for key in ("spend", "roas", "acos", "ctr", "cpc", "cpa", "impressions", "clicks", "conversions"):
        val = summary.get(key)
        if val is not None and str(val).strip():
            lines.append(f"{key}: {str(val).strip()}")
    return lines


def _campaign_lines(campaigns: list[Any], *, limit: int = 8) -> list[str]:
    lines: list[str] = []
    for idx, item in enumerate(campaigns[:limit], start=1):
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        bits = [name]
        status = str(item.get("status") or "").strip()
        if status:
            bits.append(f"status={status}")
        metrics = item.get("metrics")
        if isinstance(metrics, dict):
            for mk, mv in metrics.items():
                if mv is not None and str(mv).strip():
                    bits.append(f"{mk}={str(mv).strip()}")
        lines.append(f"campaign_{idx}: " + ", ".join(bits))
    return lines


def format_metrics_snapshot_from_data(data: dict[str, Any]) -> str:
    if not data:
        return ""
    preset = str(data.get("metrics_snapshot") or "").strip()
    if preset:
        return preset[:4000]

    parts: list[str] = []
    date_range = str(data.get("date_range") or "").strip()
    if date_range:
        parts.append(f"date_range: {date_range}")
    platform = str(data.get("platform") or "").strip()
    if platform:
        parts.append(f"platform: {platform}")
    summary = data.get("summary")
    if isinstance(summary, dict):
        parts.extend(_summary_lines(summary))
    campaigns = data.get("campaigns")
    if isinstance(campaigns, list):
        parts.extend(_campaign_lines(campaigns))
    data_source = str(data.get("data_source") or "").strip()
    if data_source:
        parts.append(f"data_source: {data_source}")
    if data.get("partial") is True:
        parts.append("partial: true")
    return "; ".join(parts)[:4000]


def load_metrics_json_arg(raw: str | None) -> dict[str, Any] | None:
    text = str(raw or "").strip()
    if not text:
        return None
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("metrics JSON 必须是对象")
    return parsed


def load_metrics_file(path: str | None) -> dict[str, Any] | None:
    p = str(path or "").strip()
    if not p:
        return None
    text = Path(p).read_text(encoding="utf-8")
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("metrics 文件 JSON 必须是对象")
    return parsed


def build_metrics_payload(
    *,
    metrics_text: str | None = None,
    metrics_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """组装 API payload 中的 metrics / metrics_data 字段。

    metrics 仅放用户原始文本，结构化 dict 只放 metrics_data；
    服务端 normalize_ad_metrics 会把结构化展开后单层合并进快照，
    避免此处预合并导致指标明细在 prompt 里重复。
    """
    out: dict[str, Any] = {}
    text = str(metrics_text or "").strip()
    structured = dict(metrics_data) if isinstance(metrics_data, dict) else None

    if text:
        out["metrics"] = text[:4000]

    if structured:
        out["metrics_data"] = structured
    return out
