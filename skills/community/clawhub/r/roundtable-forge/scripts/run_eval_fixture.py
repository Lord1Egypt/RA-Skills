#!/usr/bin/env python3
"""Execute deterministic Roundtable eval fixtures and emit one JSON object."""

from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Callable


SKILL_DIR = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str) -> ModuleType:
    path = SKILL_DIR / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load fixture dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lint_memory = load_module("roundtable_eval_lint_memory", "scripts/lint_memory.py")
render_all = load_module("roundtable_eval_render_all", "scripts/render_all.py")
podcast_renderer = load_module(
    "roundtable_eval_podcast_renderer",
    "scripts/render_memory_to_podcast_script.py",
)
argument_graph_renderer = load_module(
    "roundtable_eval_argument_graph_renderer",
    "scripts/render_memory_to_argument_graph.py",
)


def report_payload(report: object) -> dict[str, object]:
    errors = getattr(report, "errors", [])
    warnings = getattr(report, "warnings", [])
    return {
        "error_codes": [str(item.get("code", "")) for item in errors],
        "warning_codes": [str(item.get("code", "")) for item in warnings],
        "exit_code": 1 if errors else 0,
    }


def illegal_state_transition() -> dict[str, object]:
    report = lint_memory.LintReport("eval-36.json")
    lint_memory.lint_state_machine(
        {
            "state": "round_open",
            "metadata": {"completed": False},
            "state_log": [
                {
                    "from": "completed",
                    "to": "round_open",
                    "round_number": 2,
                    "trigger": "next_round_dispatched",
                    "at": "2026-07-26T10:00:00+08:00",
                }
            ],
        },
        report,
    )
    return report_payload(report)


def divergent_contract() -> dict[str, object]:
    report = lint_memory.LintReport("eval-37.json")
    lint_memory.lint_versioned_contract(
        {
            "version": "2.5.0",
            "contract_version": "3.0.0",
            "contract_compat": {
                "min_compatible": "2.5.0",
                "max_compatible": "3.0.0",
            },
        },
        report,
    )
    return report_payload(report)


def podcast_memory(*, legacy_shownotes: bool = False) -> dict[str, object]:
    shownotes: dict[str, object] = {
        "cast": ["周衡（主播）", "林澜"],
        "timestamps": [{"time": "00:00", "topic": "开场"}],
        "resources": [],
    }
    if not legacy_shownotes:
        shownotes.update(
            {
                "team": {"host": "周衡", "editor": "", "producer": ""},
                "about_show": "一档讨论技术与人的节目。",
                "legal_disclaimer": "本期内容仅供信息交流。",
                "ai_generated_disclaimer": "本期文本由 AI 生成。",
            }
        )
    return {
        "topic": "技术与人",
        "created_at": "2026-07-26T10:00:00+08:00",
        "characters": [
            {
                "id": "host",
                "name": "周衡",
                "type": "archetype",
                "role": "host",
            },
            {
                "id": "guest",
                "name": "林澜",
                "type": "archetype",
            },
        ],
        "podcast_script": {
            "show_title": "技术与人",
            "tagline": "一次兼容性回归",
            "host_id": "host",
            "segments": [
                {
                    "segment_id": "segment-1",
                    "title": "第一章",
                    "intro": "**周衡**：先从问题本身开始。",
                    "dialogue": [
                        {
                            "character_id": "guest",
                            "content": "真正重要的是让契约可以持续验证。",
                        }
                    ],
                    "transition": "**周衡**: 接着进入下一部分。",
                }
            ],
            "outro": "周衡：感谢收听，我们下期再见。",
            "shownotes": shownotes,
        },
    }


def defensive_host_prefix() -> dict[str, object]:
    markdown = podcast_renderer.render_podcast_script(podcast_memory())
    duplicate_patterns = (
        "**周衡**：**周衡**：",
        "**周衡**：**周衡**:",
        "**周衡**：周衡：",
        "**周衡**：周衡:",
    )
    return {
        "renderer_exit_code": 0,
        "duplicate_host_prefix": any(pattern in markdown for pattern in duplicate_patterns),
        "full_width_stripped": (
            podcast_renderer._strip_host_prefix("**周衡**：测试", "周衡") == "测试"
        ),
        "half_width_stripped": (
            podcast_renderer._strip_host_prefix("**周衡**: 测试", "周衡") == "测试"
        ),
    }


def plural_format_precedence() -> dict[str, object]:
    formats = render_all.resolve_formats(
        {
            "metadata": {
                "output_format": "minutes",
                "output_formats": ["podcast"],
            }
        },
        None,
    )
    return {
        "effective_formats": formats,
        "plural_precedence": formats == ["podcast"],
    }


def untransferable_checklist() -> dict[str, object]:
    payload = json.loads(
        (SKILL_DIR / "assets" / "untransferable-checklist.json").read_text(
            encoding="utf-8"
        )
    )
    categories = payload.get("categories", [])
    credential_item: dict[str, object] = {}
    for category in categories if isinstance(categories, list) else []:
        if not isinstance(category, dict):
            continue
        for item in category.get("items", []):
            if isinstance(item, dict) and item.get("id") == "credentials":
                credential_item = item
                break
    return {
        "schema_version": payload.get("schema_version"),
        "category_count": len(categories) if isinstance(categories, list) else 0,
        "credential_item_detected": bool(credential_item),
        "danger_signs": credential_item.get("danger_signs", []),
        "high_risk_signals": credential_item.get("high_risk_signals", []),
    }


def podcast_backward_compat() -> dict[str, object]:
    markdown = podcast_renderer.render_podcast_script(
        podcast_memory(legacy_shownotes=True)
    )
    required_sections = (
        "### 创作者们",
        "### 关于本节目",
        "### 免责声明",
        "### AI 生成说明",
    )
    missing_sections = [
        section for section in required_sections if section not in markdown
    ]
    return {
        "renderer_exit_code": 0,
        "missing_sections": missing_sections,
        "all_required_sections": not missing_sections,
    }


def argument_graph_memory() -> dict[str, object]:
    return {
        "topic": "需求验证",
        "user_question": "团队应先验证需求还是先建设完整能力？",
        "disclaimer": "AI 生成内容，仅供参考。",
        "state": "completed",
        "metadata": {
            "completed": True,
            "discussion_structure": "standard",
            "output_format": "minutes",
            "output_formats": ["minutes"],
            "output_artifacts": ["argument_graph"],
        },
        "characters": [{"id": "expert", "name": "产品专家"}],
        "rounds": [
            {
                "round_number": 1,
                "focus_question": "先验证还是先建设？",
                "speeches": [
                    {
                        "speech_id": "s1e1",
                        "character_id": "expert",
                        "content": "先用小规模实验验证需求。",
                        "key_points": ["小规模实验可以减少错误投入"],
                    }
                ],
            }
        ],
        "synthesis": {
            "argument_graph": {
                "schema_version": "1.0.0",
                "title": "需求验证观点关系图",
                "root_node_id": "ag-n001",
                "nodes": [
                    {
                        "id": "ag-n001",
                        "type": "question",
                        "label": "先验证还是先建设？",
                        "status": "open",
                        "character_ids": [],
                        "source_speech_ids": [],
                    },
                    {
                        "id": "ag-n002",
                        "type": "claim",
                        "label": "先用小规模实验验证需求",
                        "status": "consensus",
                        "character_ids": ["expert"],
                        "source_speech_ids": ["s1e1"],
                    },
                ],
                "edges": [
                    {
                        "id": "ag-e001",
                        "source": "ag-n002",
                        "target": "ag-n001",
                        "relation": "answers",
                        "rationale": "该观点直接回答核心决策问题",
                        "source_speech_ids": ["s1e1"],
                        "confidence": "high",
                    }
                ],
            }
        },
    }


def argument_graph_contract() -> dict[str, object]:
    memory = argument_graph_memory()
    report = lint_memory.LintReport("eval-57.json")
    lint_memory.lint_argument_graph(memory, report, {"expert"})
    markdown = argument_graph_renderer.render_argument_graph(memory)
    return {
        **report_payload(report),
        "resolved_artifacts": render_all.resolve_artifacts(memory, None),
        "contains_mermaid": "```mermaid" in markdown and "flowchart LR" in markdown,
        "contains_traceability": "`s1e1`" in markdown,
        "contains_relation_basis": "ag-n002 → ag-n001 · 回答" in markdown,
    }


def argument_graph_rejects_dangling_refs() -> dict[str, object]:
    memory = argument_graph_memory()
    graph = memory["synthesis"]["argument_graph"]
    graph["edges"][0]["target"] = "ag-n999"
    graph["edges"][0]["source_speech_ids"] = ["missing-speech"]
    report = lint_memory.LintReport("eval-58.json")
    lint_memory.lint_argument_graph(memory, report, {"expert"})
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        encoding="utf-8",
    ) as handle:
        json.dump(memory, handle, ensure_ascii=False)
        handle.flush()
        preflight_exit_code, _ = render_all.preflight_memory(Path(handle.name))
    return {
        **report_payload(report),
        "render_preflight_exit_code": preflight_exit_code,
    }


HANDLERS: dict[int, Callable[[], dict[str, object]]] = {
    36: illegal_state_transition,
    37: divergent_contract,
    39: defensive_host_prefix,
    40: plural_format_precedence,
    41: untransferable_checklist,
    44: podcast_backward_compat,
    57: argument_graph_contract,
    58: argument_graph_rejects_dangling_refs,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run one deterministic roundtable eval fixture."
    )
    parser.add_argument("--eval-id", type=int, required=True)
    args = parser.parse_args()
    handler = HANDLERS.get(args.eval_id)
    if handler is None:
        parser.error(f"unsupported deterministic eval id: {args.eval_id}")
    print(json.dumps(handler(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
