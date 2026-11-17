"""
规则格式化器 - 将提取的规则格式化为不同输出格式
"""
import json
from typing import List
from dataclasses import dataclass


@dataclass
class Rule:
    """规则定义"""
    rule_id: str
    category: str
    description: str
    pattern: str = None
    confidence: float = 0.0
    source_count: int = 0


class RuleFormatter:
    """规则格式化器"""

    def format_as_prompt(self, rules: List[Rule]) -> str:
        """格式化为 System Prompt

        Args:
            rules: 规则列表

        Returns:
            格式化后的 prompt 字符串
        """
        if not rules:
            return ""

        lines = ["【历史经验规则（请遵循）】"]

        # 按类别分组
        avoid_rules = [r for r in rules if r.category == "avoid"]
        prefer_rules = [r for r in rules if r.category == "prefer"]

        if avoid_rules:
            lines.append("\n## 避免操作")
            for r in sorted(avoid_rules, key=lambda x: -x.confidence):
                lines.append(f"- {r.description}（置信度: {r.confidence:.0%}）")

        if prefer_rules:
            lines.append("\n## 推荐做法")
            for r in sorted(prefer_rules, key=lambda x: -x.confidence):
                lines.append(f"- {r.description}（置信度: {r.confidence:.0%}）")

        return "\n".join(lines)

    def format_as_json(self, rules: List[Rule]) -> str:
        """格式化为 JSON"""
        return json.dumps([
            {
                "rule_id": r.rule_id,
                "category": r.category,
                "description": r.description,
                "confidence": r.confidence,
                "source_count": r.source_count,
            }
            for r in rules
        ], ensure_ascii=False, indent=2)

    def format_as_markdown(self, rules: List[Rule]) -> str:
        """格式化为 Markdown 文档"""
        lines = ["# 自动提取的规则\n"]

        avoid_rules = [r for r in rules if r.category == "avoid"]
        prefer_rules = [r for r in rules if r.category == "prefer"]

        if avoid_rules:
            lines.append("## 避免操作\n")
            lines.append("| 规则ID | 描述 | 置信度 | 来源数 |")
            lines.append("|--------|------|--------|--------|")
            for r in sorted(avoid_rules, key=lambda x: -x.confidence):
                lines.append(f"| {r.rule_id} | {r.description} | {r.confidence:.0%} | {r.source_count} |")
            lines.append("")

        if prefer_rules:
            lines.append("## 推荐做法\n")
            lines.append("| 规则ID | 描述 | 置信度 | 来源数 |")
            lines.append("|--------|------|--------|--------|")
            for r in sorted(prefer_rules, key=lambda x: -x.confidence):
                lines.append(f"| {r.rule_id} | {r.description} | {r.confidence:.0%} | {r.source_count} |")

        return "\n".join(lines)
