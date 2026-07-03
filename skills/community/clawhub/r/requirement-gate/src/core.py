"""Requirement Gate — 需求门禁核心引擎。

提供三类检查：
- 完整性检查（check_completeness）：标题、描述、优先级、验收标准、范围、约束是否齐备
- 验收标准检查（check_acceptance_criteria）：每条标准是否可量化、可测试
- 范围边界检查（check_scope_boundary）：范围内外是否清晰、是否有重叠、描述是否充分

用法:
    from src import RequirementGate, Requirement, AcceptanceCriteria, Scope, Priority

    gate = RequirementGate()
    req = Requirement(
        title="登录功能",
        description="实现用户名密码登录并返回 token。",
        priority=Priority.HIGH,
        acceptance_criteria=[
            AcceptanceCriteria("登录成功返回 200 和 token", measurable=True, testable=True),
        ],
        scope=Scope(in_scope=["账号密码登录"], out_of_scope=["第三方登录"]),
        constraints=["必须兼容移动端"],
    )
    results = gate.run_all_checks(req)
"""

from __future__ import annotations

from typing import List

from src.models import (
    AcceptanceCriteria,
    GateResult,
    Requirement,
    Scope,
)


class RequirementGate:
    """需求门禁检查器。

    默认 pass_threshold=1.0，即所有检查项全部通过才判定通过。
    可通过参数自定义阈值与长度下限。
    """

    DEFAULT_MIN_DESCRIPTION_LENGTH = 10
    DEFAULT_MIN_CRITERION_LENGTH = 5
    DEFAULT_MIN_SCOPE_ITEM_LENGTH = 3
    DEFAULT_PASS_THRESHOLD = 1.0

    def __init__(
        self,
        min_description_length: int = DEFAULT_MIN_DESCRIPTION_LENGTH,
        min_criterion_length: int = DEFAULT_MIN_CRITERION_LENGTH,
        min_scope_item_length: int = DEFAULT_MIN_SCOPE_ITEM_LENGTH,
        pass_threshold: float = DEFAULT_PASS_THRESHOLD,
    ) -> None:
        self.min_description_length = min_description_length
        self.min_criterion_length = min_criterion_length
        self.min_scope_item_length = min_scope_item_length
        self.pass_threshold = pass_threshold

    # ------------------------------------------------------------------
    # 完整性检查
    # ------------------------------------------------------------------
    def check_completeness(self, requirement: Requirement) -> GateResult:
        """检查需求字段完整性。"""
        checks = [
            (
                "title",
                bool(requirement.title and requirement.title.strip()),
                "标题非空",
            ),
            (
                "description",
                len(requirement.description.strip()) >= self.min_description_length,
                f"描述长度 >= {self.min_description_length}",
            ),
            (
                "priority",
                requirement.priority is not None,
                "优先级已设置",
            ),
            (
                "acceptance_criteria",
                len(requirement.acceptance_criteria) > 0,
                "至少一条验收标准",
            ),
            (
                "scope_in_scope",
                len(requirement.scope.in_scope) > 0,
                "范围内有项",
            ),
            (
                "constraints",
                len(requirement.constraints) > 0,
                "至少一条约束",
            ),
        ]

        return self._build_result(
            check_name="completeness",
            checks=checks,
            pass_message="完整性检查通过",
            fail_prefix="完整性检查未通过",
            extra={
                "in_scope_count": len(requirement.scope.in_scope),
                "out_of_scope_count": len(requirement.scope.out_of_scope),
                "criteria_count": len(requirement.acceptance_criteria),
            },
        )

    # ------------------------------------------------------------------
    # 验收标准检查
    # ------------------------------------------------------------------
    def check_acceptance_criteria(
        self, criteria: List[AcceptanceCriteria]
    ) -> GateResult:
        """检查验收标准的可量化性与可测试性。"""
        if not criteria:
            return GateResult(
                check_name="acceptance_criteria",
                passed=False,
                score=0.0,
                message="无验收标准",
                details={
                    "total": 0,
                    "passed": 0,
                    "issues": ["no acceptance criteria provided"],
                },
            )

        issues = []
        good = 0
        for index, item in enumerate(criteria):
            item_issues = []
            criterion_text = item.criterion or ""
            if not criterion_text.strip() or len(criterion_text.strip()) < self.min_criterion_length:
                item_issues.append("criterion too short or empty")
            if not item.measurable:
                item_issues.append("not measurable")
            if not item.testable:
                item_issues.append("not testable")
            if item_issues:
                issues.append(
                    {"index": index, "criterion": item.criterion, "issues": item_issues}
                )
            else:
                good += 1

        total = len(criteria)
        score = good / total if total else 0.0
        passed = score >= self.pass_threshold
        message = (
            "验收标准检查通过"
            if passed
            else f"验收标准检查未通过: {len(issues)} 条存在问题"
        )
        return GateResult(
            check_name="acceptance_criteria",
            passed=passed,
            score=score,
            message=message,
            details={
                "total": total,
                "passed": good,
                "failed": len(issues),
                "issues": issues,
            },
        )

    # ------------------------------------------------------------------
    # 范围边界检查
    # ------------------------------------------------------------------
    def check_scope_boundary(self, scope: Scope) -> GateResult:
        """检查范围边界清晰度。"""
        in_scope = [s for s in scope.in_scope if s and s.strip()]
        out_scope = [s for s in scope.out_of_scope if s and s.strip()]

        in_lower = {s.strip().lower() for s in in_scope}
        out_lower = {s.strip().lower() for s in out_scope}
        overlap = in_lower & out_lower

        in_short = [s for s in in_scope if len(s.strip()) < self.min_scope_item_length]
        out_short = [s for s in out_scope if len(s.strip()) < self.min_scope_item_length]

        checks = [
            ("in_scope_not_empty", len(in_scope) > 0, "范围内有项"),
            ("out_of_scope_not_empty", len(out_scope) > 0, "范围外有项"),
            ("no_overlap", len(overlap) == 0, "范围内外无重叠"),
            ("in_scope_descriptive", len(in_short) == 0, "范围内项足够描述"),
            ("out_of_scope_descriptive", len(out_short) == 0, "范围外项足够描述"),
        ]

        return self._build_result(
            check_name="scope_boundary",
            checks=checks,
            pass_message="范围边界检查通过",
            fail_prefix="范围边界检查未通过",
            extra={
                "in_scope_count": len(in_scope),
                "out_of_scope_count": len(out_scope),
                "overlap": sorted(overlap),
                "in_scope_short": in_short,
                "out_of_scope_short": out_short,
            },
        )

    # ------------------------------------------------------------------
    # 全部检查
    # ------------------------------------------------------------------
    def run_all_checks(self, requirement: Requirement) -> List[GateResult]:
        """按顺序运行完整性、验收标准、范围边界三类检查。"""
        return [
            self.check_completeness(requirement),
            self.check_acceptance_criteria(requirement.acceptance_criteria),
            self.check_scope_boundary(requirement.scope),
        ]

    # ------------------------------------------------------------------
    # 内部工具
    # ------------------------------------------------------------------
    def _build_result(
        self,
        check_name: str,
        checks: List,
        pass_message: str,
        fail_prefix: str,
        extra: dict,
    ) -> GateResult:
        """根据 (name, ok, detail) 列表构造 GateResult。"""
        total = len(checks)
        passed_count = sum(1 for _, ok, _ in checks if ok)
        score = passed_count / total if total else 0.0
        passed = score >= self.pass_threshold
        failed = [name for name, ok, _ in checks if not ok]
        message = pass_message if passed else f"{fail_prefix}: {failed}"
        details = {
            "total": total,
            "passed": passed_count,
            "failed": failed,
            "checks": [{"name": n, "ok": o, "detail": d} for n, o, d in checks],
        }
        details.update(extra)
        return GateResult(
            check_name=check_name,
            passed=passed,
            score=score,
            message=message,
            details=details,
        )
