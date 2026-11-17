"""
声明式字段映射层 — Schema → OutputAdapter 单向映射
────────────────────────────────────────────────
替代 OutputAdapter._resolve_analysis_fields() 的 80 行类型猜测。

映射表是单向的、声明式的、可独立测试的。
任何 Schema 字段变更只需修改此表，无需改动 OutputAdapter。
"""
from __future__ import annotations

from typing import Any, Callable, Optional

from contracts.analysis_schema import AnalysisOutput


# 声明式映射表：Schema 点号路径 → 输出 key → 默认值 → 可选转换函数
ANALYSIS_FIELD_MAP: list[tuple[str, str, Any, Optional[Callable]]] = [
    # (schema_dot_path, output_key, default, transform)
    ("query",              "query",           "未知主题", None),
    ("sources",            "sources",         [],         None),
    (
        "sources",
        "total_engines",
        0,
        lambda v: len({
            (s.source if hasattr(s, 'source') else s.get('source', ''))
            for s in v
        }),
    ),
    ("sources",            "total_results",   0,          lambda v: len(v)),
    ("nlp_results.entities", "entities",      {},         None),
    (
        "credibility_scores",
        "credibility",
        {},
        lambda v: {
            "high": v.high if hasattr(v, 'high') else v.get('high', 0),
            "medium": v.medium if hasattr(v, 'medium') else v.get('medium', 0),
            "low": v.low if hasattr(v, 'low') else v.get('low', 0),
            "dubious": v.dubious if hasattr(v, 'dubious') else v.get('dubious', 0),
        },
    ),
    (
        "llm_analysis.sentiment",
        "sentiment",
        {"overall": "中性"},
        lambda v: {"overall": v.overall if hasattr(v, 'overall') else v.get('overall', '中性')},
    ),
    ("llm_analysis.cross_validation", "cross_validation", {}, None),
    ("conclusions",        "conclusions",     [],         None),
    ("key_findings",       "key_findings",    [],         None),
    # 以下字段仅用于 generate_analysis() 的深度报告
    ("sources",            "deduplicated",    0,          lambda v: len(v)),
    ("credibility_scores", "cn_count",        0,          None),  # 占位，从 sources 推断
    ("credibility_scores", "global_count",    0,          None),  # 占位，从 sources 推断
    ("sources",            "date_range",      "? ~ ?",    None),  # 占位，从 sources 推断
]


class FieldMapper:
    """声明式字段映射器 — 单向、可测试、零类型猜测

    从 Pydantic Schema 对象按映射表提取字段，生成 OutputAdapter 需要的 dict。

    用法:
        mapper = FieldMapper()
        output_dict = mapper.map_analysis_to_output(analysis_output)
        # → {"query": "...", "total_engines": 5, ...}
    """

    def map_analysis_to_output(self, analysis: AnalysisOutput) -> dict:
        """将 AnalysisOutput Schema 映射为 OutputAdapter 期望的 dict"""
        data = analysis.model_dump()
        result = {}
        for schema_path, output_key, default, transform in ANALYSIS_FIELD_MAP:
            value = self._resolve_dot_path(data, schema_path)
            if value is not None and transform:
                try:
                    value = transform(value)
                except Exception:
                    value = default
            result[output_key] = value if value is not None else default

        # 补充推断字段：cn_count / global_count / date_range 从 sources 推断
        sources = result.get("sources", [])
        if isinstance(sources, list):
            result["cn_count"] = sum(
                1 for s in sources
                if (isinstance(s, dict) and s.get("source", "") in {
                    "baidu", "bing_cn", "360", "sogou", "wechat", "shenma"
                })
            )
            result["global_count"] = len(sources) - result["cn_count"]

            dates = [
                s.get("date", "N/A") if isinstance(s, dict) else "N/A"
                for s in sources
                if isinstance(s, dict) and s.get("date") and s.get("date") != "N/A"
            ]
            if dates:
                result["date_range"] = f"{min(dates)} ~ {max(dates)}"
            else:
                result["date_range"] = "? ~ ?"

        return result

    def _resolve_dot_path(self, data: dict, dot_path: str) -> Any:
        """解析点号路径 'nlp_results.entities' → data['nlp_results']['entities']"""
        keys = dot_path.split(".")
        current = data
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            else:
                return None
        return current
