from __future__ import annotations

from dataclasses import dataclass

from structural_semantics import StructuralProfile, infer_question_profile


@dataclass
class SituationAssessment:
    primary: str
    secondary: list[str]
    scores: dict[str, int]
    structural_profile: StructuralProfile
    rationale: list[str]


class SituationClassifier:
    CATEGORY_DESCRIPTIONS = {
        "以弱对强": "资源偏弱且外部压力强",
        "内部冲突": "内部摩擦与执行掣肘已经影响决策",
        "改革推进": "核心难题在于制度、流程或利益重分配",
        "联盟不稳": "需要借力合作，但信任与目标一致性不足",
        "守攻抉择": "关键决策在于先稳住还是主动推进",
        "权力控制": "控制权、任命权或组织中枢归属存在压力",
        "用人换将": "问题聚焦在人事调整与岗位重配",
    }

    def classify(self, question: str) -> SituationAssessment:
        profile = infer_question_profile(question)
        scores = self._score_categories(profile, question)
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        primary = ranked[0][0] if ranked and ranked[0][1] > 0 else "守攻抉择"
        secondary = [category for category, score in ranked[1:3] if score > 0]

        rationale = self._build_rationale(primary, secondary, profile, scores)
        return SituationAssessment(
            primary=primary,
            secondary=secondary,
            scores=scores,
            structural_profile=profile,
            rationale=rationale,
        )

    def _score_categories(self, profile: StructuralProfile, question: str) -> dict[str, int]:
        scores = {category: 0 for category in self.CATEGORY_DESCRIPTIONS}
        dims = profile.dimensions

        if dims["resource_state"] == "scarce":
            scores["以弱对强"] += 4
        if dims["external_pressure"] == "high":
            scores["以弱对强"] += 4
            scores["守攻抉择"] += 1
        elif dims["external_pressure"] == "medium":
            scores["以弱对强"] += 2

        if dims["internal_friction"] == "high":
            scores["内部冲突"] += 5
        elif dims["internal_friction"] == "medium":
            scores["内部冲突"] += 2

        if dims["change_pressure"] == "high":
            scores["改革推进"] += 5
        elif dims["change_pressure"] == "medium":
            scores["改革推进"] += 2

        if dims["execution_resistance"] == "high":
            scores["改革推进"] += 3
            scores["内部冲突"] += 2
        elif dims["execution_resistance"] == "medium":
            scores["改革推进"] += 1

        if dims["alliance_dependency"] == "high":
            scores["联盟不稳"] += 4
        elif dims["alliance_dependency"] == "medium":
            scores["联盟不稳"] += 2

        if dims["trust_risk"] == "high":
            scores["联盟不稳"] += 5
        elif dims["trust_risk"] == "medium":
            scores["联盟不稳"] += 2

        if dims["control_pressure"] == "high":
            scores["权力控制"] += 5
        elif dims["control_pressure"] == "medium":
            scores["权力控制"] += 2

        if dims["personnel_pressure"] == "high":
            scores["用人换将"] += 5
        elif dims["personnel_pressure"] == "medium":
            scores["用人换将"] += 2

        if dims["legitimacy_pressure"] == "high":
            scores["权力控制"] += 2
            scores["改革推进"] += 2
            scores["内部冲突"] += 1
        elif dims["legitimacy_pressure"] == "medium":
            scores["权力控制"] += 1
            scores["改革推进"] += 1

        if dims["time_pressure"] == "high":
            scores["守攻抉择"] += 3
            scores["改革推进"] += 1
        elif dims["time_pressure"] == "medium":
            scores["守攻抉择"] += 1

        action_bias = dims["action_bias"]
        if action_bias in {"advance", "consolidate", "mixed"}:
            scores["守攻抉择"] += 4
        if action_bias == "ally":
            scores["联盟不稳"] += 2
        if action_bias == "replace":
            scores["用人换将"] += 2
            scores["权力控制"] += 1

        if "控制权" in question and dims["personnel_pressure"] != "low":
            scores["权力控制"] += 1
        if "先稳内部还是" in question or "该守还是该攻" in question:
            scores["守攻抉择"] += 2

        return scores

    def _build_rationale(
        self,
        primary: str,
        secondary: list[str],
        profile: StructuralProfile,
        scores: dict[str, int],
    ) -> list[str]:
        focus = profile.active_focus(limit=4)
        rationale: list[str] = []
        if focus:
            rationale.append(f"识别到的结构信号：{'、'.join(focus)}。")
        rationale.append(f"主局面判为“{primary}”，因为它最能解释当前问题的核心矛盾：{self.CATEGORY_DESCRIPTIONS[primary]}。")
        for category in secondary:
            if scores.get(category, 0) > 0:
                rationale.append(f"次级局面补充为“{category}”，因为问题里同时存在：{self.CATEGORY_DESCRIPTIONS[category]}。")
        return rationale
