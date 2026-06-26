from __future__ import annotations

import json
import re
from pathlib import Path


REQUIRED_FIELDS = {
    "id",
    "title",
    "dynasty",
    "era",
    "year_range",
    "main_figures",
    "summary",
    "situation_tags",
    "decision_maker",
    "objective",
    "visible_information",
    "hidden_constraints",
    "options_available",
    "chosen_action",
    "short_term_outcome",
    "long_term_outcome",
    "success_or_failure",
    "key_reasons",
    "transferable_principles",
    "non_transferable_factors",
    "modern_analogy_keywords",
    "source_note",
}

FIELD_ORDER = [
    "id",
    "title",
    "dynasty",
    "era",
    "year_range",
    "main_figures",
    "summary",
    "situation_tags",
    "decision_maker",
    "objective",
    "visible_information",
    "hidden_constraints",
    "options_available",
    "chosen_action",
    "short_term_outcome",
    "long_term_outcome",
    "success_or_failure",
    "key_reasons",
    "transferable_principles",
    "non_transferable_factors",
    "modern_analogy_keywords",
    "source_note",
]

LIST_FIELDS = {
    "main_figures",
    "situation_tags",
    "visible_information",
    "hidden_constraints",
    "options_available",
    "key_reasons",
    "transferable_principles",
    "non_transferable_factors",
    "modern_analogy_keywords",
}

STRING_FIELDS = REQUIRED_FIELDS - LIST_FIELDS
VALID_OUTCOMES = {"success", "failure", "mixed"}
ID_PATTERN = re.compile(r"^[a-z0-9-]+$")


class CaseValidationError(ValueError):
    pass


def build_case_template() -> dict:
    return {
        "id": "new-historical-case-id",
        "title": "案例标题",
        "dynasty": "朝代或时期",
        "era": "历史阶段",
        "year_range": "时间范围",
        "main_figures": ["关键人物甲", "关键人物乙"],
        "summary": "用 1-2 句话概括事件与局面。",
        "situation_tags": ["改革推进", "联盟不稳"],
        "decision_maker": "主要决策者",
        "objective": "决策者想达成什么。",
        "visible_information": ["当时公开可见的条件 1", "当时公开可见的条件 2"],
        "hidden_constraints": ["不易被外部直接看到的限制 1", "不易被外部直接看到的限制 2"],
        "options_available": ["可选路径 1", "可选路径 2"],
        "chosen_action": "最终采取的动作。",
        "short_term_outcome": "短期结果。",
        "long_term_outcome": "中长期结果。",
        "success_or_failure": "mixed",
        "key_reasons": ["成败原因 1", "成败原因 2"],
        "transferable_principles": ["可迁移原则 1", "可迁移原则 2"],
        "non_transferable_factors": ["不可直接照搬的因素 1", "不可直接照搬的因素 2"],
        "modern_analogy_keywords": ["适用场景关键词 1", "适用场景关键词 2"],
        "source_note": "史料来源或用户提供的来源说明",
    }


class CaseStore:
    def __init__(self, core_cases_path: Path, user_cases_path: Path | None = None) -> None:
        self.core_cases_path = core_cases_path
        self.user_cases_path = user_cases_path or core_cases_path.with_name("user_cases.json")
        self.ensure_user_cases_file()

    def ensure_user_cases_file(self) -> None:
        if not self.user_cases_path.exists():
            self.user_cases_path.write_text("[]\n", encoding="utf-8")

    def load_core_cases(self) -> list[dict]:
        cases = self._load_cases(self.core_cases_path)
        if len(cases) < 40:
            raise CaseValidationError("基础案例数量不足，至少需要 40 条。")
        return cases

    def load_user_cases(self) -> list[dict]:
        return self._load_cases(self.user_cases_path)

    def load_all_cases(self) -> list[dict]:
        all_cases = self.load_core_cases() + self.load_user_cases()
        self._ensure_unique_ids(all_cases)
        return all_cases

    def add_case(self, case: dict) -> dict:
        normalized = self.normalize_case(case)
        existing_cases = self.load_all_cases()
        existing_ids = {item["id"] for item in existing_cases}
        if normalized["id"] in existing_ids:
            raise CaseValidationError(f"案例 id 已存在: {normalized['id']}")

        user_cases = self.load_user_cases()
        user_cases.append(normalized)
        self.user_cases_path.write_text(
            json.dumps(user_cases, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return normalized

    def load_case_candidate(self, path: Path) -> dict:
        payload = self.parse_case_payload(path.read_text(encoding="utf-8"))
        return payload

    def parse_case_payload(self, payload_text: str) -> dict:
        payload = json.loads(payload_text)
        if isinstance(payload, list):
            if len(payload) != 1:
                raise CaseValidationError("新增案例文件必须是单个对象，或只包含 1 条案例的数组。")
            payload = payload[0]
        if not isinstance(payload, dict):
            raise CaseValidationError("新增案例文件必须是 JSON 对象。")
        return payload

    def _load_cases(self, path: Path) -> list[dict]:
        if not path.exists():
            return []

        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise CaseValidationError(f"{path.name} 必须是案例数组。")

        normalized_cases = [self.normalize_case(case) for case in payload]
        self._ensure_unique_ids(normalized_cases, source_name=path.name)
        return normalized_cases

    def normalize_case(self, case: dict) -> dict:
        if not isinstance(case, dict):
            raise CaseValidationError("案例必须是 JSON 对象。")

        missing = REQUIRED_FIELDS - set(case)
        if missing:
            raise CaseValidationError(f"案例缺少字段: {sorted(missing)}")

        extra = set(case) - REQUIRED_FIELDS
        if extra:
            raise CaseValidationError(f"案例包含未定义字段: {sorted(extra)}")

        normalized: dict[str, str | list[str]] = {}
        for field in FIELD_ORDER:
            value = case[field]
            if field in LIST_FIELDS:
                if not isinstance(value, list):
                    raise CaseValidationError(f"字段 {field} 必须是数组。")
                items = [str(item).strip() for item in value if str(item).strip()]
                if not items:
                    raise CaseValidationError(f"字段 {field} 不能为空数组。")
                if field == "options_available" and len(items) < 2:
                    raise CaseValidationError("字段 options_available 至少需要 2 个选项。")
                normalized[field] = items
                continue

            text = str(value).strip()
            if not text:
                raise CaseValidationError(f"字段 {field} 不能为空。")
            normalized[field] = text

        case_id = str(normalized["id"])
        if not ID_PATTERN.match(case_id):
            raise CaseValidationError("字段 id 只能包含小写字母、数字和连字符。")

        if normalized["success_or_failure"] not in VALID_OUTCOMES:
            raise CaseValidationError("字段 success_or_failure 必须是 success、failure 或 mixed。")

        return normalized  # type: ignore[return-value]

    def _ensure_unique_ids(self, cases: list[dict], source_name: str = "案例集合") -> None:
        seen_ids: set[str] = set()
        for case in cases:
            case_id = case["id"]
            if case_id in seen_ids:
                raise CaseValidationError(f"{source_name} 中存在重复案例 id: {case_id}")
            seen_ids.add(case_id)
