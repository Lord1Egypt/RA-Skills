#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render synthesis.argument_graph from Roundtable Memory as Mermaid Markdown."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


NODE_TYPE_LABELS = {
    "question": "问题",
    "claim": "观点",
    "evidence": "证据",
    "assumption": "前提",
    "decision": "决策",
    "next_step": "下一步",
}

NODE_STATUS_LABELS = {
    "neutral": "中性",
    "consensus": "共识",
    "divergent": "分歧",
    "open": "未决",
}

RELATION_LABELS = {
    "supports": "支持",
    "extends": "延伸",
    "contradicts": "冲突",
    "challenges": "质疑",
    "qualifies": "限定",
    "depends_on": "依赖",
    "answers": "回答",
    "raises": "引出",
}

RELATION_DESCRIPTIONS = {
    "supports": "为目标观点提供证据或理由",
    "extends": "在兼容方向上补充新维度",
    "contradicts": "在相同条件下与目标直接冲突",
    "challenges": "质疑目标的前提、证据或可行性",
    "qualifies": "为目标增加条件、例外或边界",
    "depends_on": "只有目标前提成立时才成立",
    "answers": "直接回答目标问题",
    "raises": "引出目标问题或议题",
}

RELATION_COLORS = {
    "supports": "#16a34a",
    "extends": "#2563eb",
    "contradicts": "#dc2626",
    "challenges": "#ea580c",
    "qualifies": "#ca8a04",
    "depends_on": "#7c3aed",
    "answers": "#0f766e",
    "raises": "#64748b",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a roundtable Memory argument graph to Mermaid Markdown."
    )
    parser.add_argument("memory", help="Path to the roundtable Memory JSON file.")
    parser.add_argument(
        "--output",
        "-o",
        help="Path to output Markdown. Defaults to <memory>.argument-graph.md.",
    )
    return parser.parse_args()


def _markdown_cell(value: object) -> str:
    return str(value or "—").replace("|", "\\|").replace("\n", " ")


def _mermaid_label(value: object) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return (
        text.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _mermaid_ids(nodes: list[dict]) -> dict[str, str]:
    result: dict[str, str] = {}
    used = set()
    for index, node in enumerate(nodes):
        graph_id = str(node.get("id", f"node-{index + 1}"))
        base = "n_" + re.sub(r"[^A-Za-z0-9_]", "_", graph_id)
        candidate = base
        suffix = 2
        while candidate in used:
            candidate = f"{base}_{suffix}"
            suffix += 1
        used.add(candidate)
        result[graph_id] = candidate
    return result


def render_mermaid(graph: dict) -> str:
    """Render only declared nodes and edges; never infer missing relationships."""
    nodes = graph.get("nodes", []) or []
    edges = graph.get("edges", []) or []
    mermaid_ids = _mermaid_ids(nodes)
    root_node_id = graph.get("root_node_id", "")

    lines = ["flowchart LR"]
    for node in nodes:
        graph_id = str(node.get("id", ""))
        mermaid_id = mermaid_ids[graph_id]
        label = _mermaid_label(node.get("label", graph_id))
        node_type = node.get("type", "claim")
        type_label = NODE_TYPE_LABELS.get(node_type, node_type)
        display = f"{type_label}｜{label}"
        if graph_id == root_node_id:
            lines.append(f'    {mermaid_id}{{{{"{display}"}}}}')
        else:
            lines.append(f'    {mermaid_id}["{display}"]')

    edge_styles = []
    for index, edge in enumerate(edges):
        source = mermaid_ids.get(str(edge.get("source", "")))
        target = mermaid_ids.get(str(edge.get("target", "")))
        if not source or not target:
            continue
        relation = edge.get("relation", "")
        relation_label = _mermaid_label(RELATION_LABELS.get(relation, relation))
        lines.append(f"    {source} -->|{relation_label}| {target}")
        color = RELATION_COLORS.get(relation, "#64748b")
        edge_styles.append(
            f"    linkStyle {index} stroke:{color},stroke-width:2px;"
        )

    lines.extend(
        [
            "    classDef neutral fill:#f8fafc,stroke:#64748b,color:#0f172a;",
            "    classDef consensus fill:#dcfce7,stroke:#16a34a,color:#14532d;",
            "    classDef divergent fill:#fee2e2,stroke:#dc2626,color:#7f1d1d;",
            "    classDef open fill:#fef3c7,stroke:#d97706,color:#78350f;",
        ]
    )
    status_groups: dict[str, list[str]] = {}
    for node in nodes:
        graph_id = str(node.get("id", ""))
        status = node.get("status", "neutral")
        if status not in NODE_STATUS_LABELS:
            status = "neutral"
        status_groups.setdefault(status, []).append(mermaid_ids[graph_id])
    for status, ids in status_groups.items():
        lines.append(f"    class {','.join(ids)} {status};")
    lines.extend(edge_styles)
    return "\n".join(lines)


def render_argument_graph(memory: dict) -> str:
    synthesis = memory.get("synthesis", {}) or {}
    graph = synthesis.get("argument_graph")
    if not isinstance(graph, dict) or not graph.get("nodes"):
        raise ValueError("synthesis.argument_graph is missing or has no nodes")

    topic = memory.get("topic", "")
    title = graph.get("title") or f"{topic}观点关系图"
    disclaimer = memory.get("disclaimer", "")
    characters = {
        item.get("id"): item
        for item in memory.get("characters", []) or []
        if isinstance(item, dict) and item.get("id")
    }
    nodes = graph.get("nodes", []) or []
    edges = graph.get("edges", []) or []
    root_node_id = graph.get("root_node_id", "")

    lines = [f"# 观点关系图：{title}", ""]
    if disclaimer:
        lines.extend([disclaimer, "", "---", ""])
    if topic:
        lines.extend([f"**圆桌主题**：{topic}", ""])
    lines.extend(
        [
            "> 本图是 Memory 中原子观点及其关系的可追溯投影，不替代完整发言与合成结论。",
            "",
            "## 核心图谱",
            "",
            "```mermaid",
            render_mermaid(graph),
            "```",
            "",
            "## 阅读图例",
            "",
            "| 关系 | 含义 |",
            "|---|---|",
        ]
    )
    for relation, label in RELATION_LABELS.items():
        lines.append(
            f"| `{relation}`（{label}） | {RELATION_DESCRIPTIONS[relation]} |"
        )

    lines.extend(
        [
            "",
            "| 节点状态 | 含义 |",
            "|---|---|",
        ]
    )
    for status, label in NODE_STATUS_LABELS.items():
        lines.append(f"| `{status}` | {label} |")

    lines.extend(
        [
            "",
            "## 节点溯源",
            "",
            "| 节点 | 类型 / 状态 | 观点归属 | 原始发言 |",
            "|---|---|---|---|",
        ]
    )
    for node in nodes:
        node_id = node.get("id", "")
        label = node.get("label", "")
        node_type = NODE_TYPE_LABELS.get(node.get("type", ""), node.get("type", ""))
        status = NODE_STATUS_LABELS.get(node.get("status", ""), node.get("status", ""))
        character_names = [
            characters.get(char_id, {}).get("name", char_id)
            for char_id in node.get("character_ids", []) or []
        ]
        speech_ids = node.get("source_speech_ids", []) or []
        if node_id == root_node_id and not speech_ids:
            source_text = "`user_question`"
        else:
            source_text = ", ".join(f"`{item}`" for item in speech_ids) or "—"
        lines.append(
            "| "
            + " | ".join(
                [
                    _markdown_cell(f"{node_id} · {label}"),
                    _markdown_cell(f"{node_type} / {status}"),
                    _markdown_cell("、".join(character_names)),
                    _markdown_cell(source_text),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 关系依据",
            "",
            "| 关系 | 理由 | 原始发言 | 置信度 |",
            "|---|---|---|---|",
        ]
    )
    for edge in edges:
        relation = edge.get("relation", "")
        relation_text = (
            f"{edge.get('source', '')} → {edge.get('target', '')} · "
            f"{RELATION_LABELS.get(relation, relation)}"
        )
        speech_text = ", ".join(
            f"`{item}`" for item in edge.get("source_speech_ids", []) or []
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    _markdown_cell(relation_text),
                    _markdown_cell(edge.get("rationale", "")),
                    _markdown_cell(speech_text),
                    _markdown_cell(edge.get("confidence", "")),
                ]
            )
            + " |"
        )

    if disclaimer:
        lines.extend(["", "---", "", disclaimer])
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    memory_path = Path(args.memory)
    if not memory_path.exists():
        print(f"Error: Memory file not found: {memory_path}", file=sys.stderr)
        return 1

    try:
        memory = json.loads(memory_path.read_text(encoding="utf-8"))
        markdown = render_argument_graph(memory)
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    output_path = (
        Path(args.output)
        if args.output
        else memory_path.with_name(f"{memory_path.stem}.argument-graph.md")
    )
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Rendered argument graph: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
