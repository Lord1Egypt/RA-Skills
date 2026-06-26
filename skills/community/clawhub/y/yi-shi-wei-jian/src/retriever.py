from __future__ import annotations

from pathlib import Path

from case_store import CaseStore
from classifier import SituationAssessment
from structural_semantics import infer_case_profile, structural_similarity


class CaseRetriever:
    QUERY_TERMS = [
        "改革", "新制度", "制度上线", "试点", "执行链", "中层拖延", "表面支持",
        "联盟", "合作方", "翻脸", "不完全信任", "背刺", "共同敌人",
        "更强", "头部竞争者", "资源不多", "资源不够", "弱势", "窗口期",
        "换人", "换将", "负责人", "削权", "架空", "控制权", "接班", "继任",
        "守住", "进攻", "防守", "扩张", "收缩", "基本盘", "后手",
    ]

    def __init__(self, cases_path: Path, user_cases_path: Path | None = None) -> None:
        self.cases_path = cases_path
        self.user_cases_path = user_cases_path
        self.case_store = CaseStore(cases_path, user_cases_path)
        self.cases = self.case_store.load_all_cases()
        self.case_profiles = {case["id"]: infer_case_profile(case) for case in self.cases}

    def retrieve(self, question: str, assessment: SituationAssessment, top_k: int = 3) -> list[dict]:
        scored_cases: list[tuple[int, dict]] = []
        query_fragments = self._extract_query_fragments(question)
        for case in self.cases:
            score = 0
            tags = set(case["situation_tags"])
            case_profile = self.case_profiles[case["id"]]
            semantic_score, semantic_reasons = structural_similarity(assessment.structural_profile, case_profile)

            if assessment.primary in tags:
                score += 10
            score += 4 * len(tags.intersection(assessment.secondary))
            score += semantic_score
            score += self._score_textual_support(case, question, query_fragments)

            if case["success_or_failure"] != "success" and assessment.primary in tags:
                score += 2

            annotated_case = dict(case)
            annotated_case["_match_reasons"] = semantic_reasons or ["该案例在结构约束上与当前问题接近。"]
            annotated_case["_semantic_score"] = semantic_score
            scored_cases.append((score, annotated_case))

        ranked = [case for _, case in sorted(scored_cases, key=lambda item: item[0], reverse=True)]
        selected = self._select_diverse_cases(ranked, top_k)
        selected = self._ensure_outcome_diversity(selected, ranked, assessment)
        return selected if selected else ranked[:top_k]

    def _extract_query_fragments(self, question: str) -> set[str]:
        return {term for term in self.QUERY_TERMS if term in question}

    def _score_textual_support(self, case: dict, question: str, query_fragments: set[str]) -> int:
        score = 0
        support_fields = [
            case["summary"],
            case["objective"],
            case["chosen_action"],
            *case["hidden_constraints"],
            *case["visible_information"],
            *case["modern_analogy_keywords"],
        ]
        for text in support_fields:
            if text in question:
                score += 2
                continue
            if any(fragment and fragment in str(text) for fragment in query_fragments):
                score += 1
        return min(score, 8)

    def _select_diverse_cases(self, ranked: list[dict], top_k: int) -> list[dict]:
        selected: list[dict] = []
        seen_titles: set[str] = set()
        seen_dynasties: set[str] = set()

        for case in ranked:
            if case["title"] in seen_titles:
                continue
            dynasty_penalty = case["dynasty"] in seen_dynasties and len(selected) < max(top_k - 1, 1)
            if dynasty_penalty:
                continue
            selected.append(case)
            seen_titles.add(case["title"])
            seen_dynasties.add(case["dynasty"])
            if len(selected) >= top_k:
                break
        return selected

    def _ensure_outcome_diversity(
        self, selected: list[dict], ranked: list[dict], assessment: SituationAssessment
    ) -> list[dict]:
        if len(selected) < 3:
            return selected

        if any(case["success_or_failure"] != "success" for case in selected):
            return selected

        for candidate in ranked:
            if candidate in selected:
                continue
            if assessment.primary not in candidate["situation_tags"]:
                continue
            if candidate["success_or_failure"] == "success":
                continue
            selected[-1] = candidate
            break
        return selected
