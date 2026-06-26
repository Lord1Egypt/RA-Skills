from __future__ import annotations


class ResponseRenderer:
    def render(self, analysis: dict) -> str:
        situation = analysis["situation"]
        cases = analysis["cases"]
        variables = analysis["variables"]
        paths = analysis["paths"]
        principles = analysis["principles"]
        assumptions = analysis["assumptions"]

        sections: list[str] = []

        sections.append("【局面判断】")
        sections.append(f"主局面：{situation.primary}")
        if situation.secondary:
            sections.append(f"次局面：{'、'.join(situation.secondary)}")
        if assumptions:
            sections.append("默认假设：")
            sections.extend([f"- {item}" for item in assumptions])
        sections.append("判断依据：")
        sections.extend([f"- {item}" for item in situation.rationale])
        sections.append("")

        sections.append("【历史参照】")
        for index, case in enumerate(cases, start=1):
            sections.append(f"{index}. {case['title']}（{case['dynasty']}）")
            sections.append(f"- 事件：{case['summary']}")
            sections.append(f"- 核心局面：{'、'.join(case['situation_tags'])}")
            sections.append(f"- 关键决策：{case['chosen_action']}")
            sections.append(f"- 成败原因：{'；'.join(case['key_reasons'])}")
            if case.get("_match_reasons"):
                sections.append(f"- 为什么像当前问题：{'；'.join(case['_match_reasons'])}")
        sections.append("")

        sections.append("【关键变量】")
        for name, explanation in variables:
            sections.append(f"- {name}：{explanation}")
        sections.append("")

        sections.append("【可选路径】")
        for index, path in enumerate(paths, start=1):
            sections.append(f"{index}. {path.name}：{path.summary}")
        sections.append("")

        sections.append("【沙盘推演】")
        for index, path in enumerate(paths, start=1):
            sections.append(f"{index}. {path.name}")
            sections.append(f"- 适用条件：{path.suitable_conditions}")
            sections.append(f"- 短期收益：{path.short_term_benefit}")
            sections.append(f"- 短期风险：{path.short_term_risk}")
            sections.append(f"- 中期演化：{path.mid_term_evolution}")
            sections.append(f"- 最容易失败点：{path.failure_point}")
        sections.append("")

        sections.append("【借鉴原则】")
        for principle in principles:
            sections.append(f"- {principle}")
        sections.append("")

        sections.append("【边界提醒】")
        for warning in analysis["boundary"]:
            sections.append(f"- {warning}")

        return "\n".join(sections)
