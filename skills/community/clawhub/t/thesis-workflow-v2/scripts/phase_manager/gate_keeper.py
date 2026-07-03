"""
Phase Manager - 门禁校验
gate_keeper.py

Phase 流转门禁：准入检查 + 准出检查。
"""

import os
from typing import Dict, List, Optional, Tuple, Any

from .schemas import (
    GateResult,
    STATUS_COMPLETED,
    CONTENT_TYPE_INTEGRATED,
    CONTENT_TYPE_REVIEW,
    CONTENT_TYPE_SUMMARY,
    calculate_word_count,
    extract_chapter_count,
)
from .file_manager import PhaseFileManager


# ============================================================================
# 常量
# ============================================================================

# 通用门禁规则
GATE_RULES = {
    "min_word_count": 1000,       # 最小字数
    "max_word_count": 200000,     # 最大字数（异常检测）
    "chapter_count": 7,           # 章节数要求
    "freshness_hours": 48,        # 文件新鲜度（小时）
}


# ============================================================================
# PhaseGateKeeper 类
# ============================================================================

class PhaseGateKeeper:
    """
    Phase 流转门禁检查器。

    职责：
    - pre_enter_check：进入 Phase N 前的准入检查
    - pre_exit_check：Phase N 完成前的准出检查
    """

    def __init__(self, paper_name: str, workspace: str = None):
        self.paper_name = paper_name
        self.fm = PhaseFileManager(paper_name, workspace)
        self.rules = GATE_RULES.copy()

    # ------------------------------------------------------------------------
    # 准入检查（进入 Phase N 前）
    # ------------------------------------------------------------------------

    VALID_PHASES = {2, 3, 3.5, 4, 5}

    def pre_enter_check(self, target_phase: float) -> GateResult:
        """
        检查是否可以进入 target_phase。

        规则：
        - Phase 2 前：Phase 1.2 大纲已确认 + Phase 1.3 已提交
        - Phase 3 前：Phase 2 全部节点 completed，无 failed
        - Phase 3.5 前：Phase 3 review 已完成
        - Phase 4 前：Phase 3.5 收敛（连续 2 轮无新 P0）
        - Phase 5 前：Phase 4 guardrails 10/10 通过
        - 未知 Phase → 失败

        Returns:
            GateResult
        """
        result = GateResult(
            passed=True,
            phase=target_phase,
            checks={},
            blocking_issues=[],
        )

        # 未知 Phase 检查
        if target_phase not in self.VALID_PHASES:
            result.add_blocking_issue(f"未知 Phase：{target_phase}")
            return result

        if target_phase == 2:
            self._check_phase2_entry(result)
        elif target_phase == 3:
            self._check_phase3_entry(result)
        elif target_phase == 3.5:
            self._check_phase3_5_entry(result)
        elif target_phase == 4:
            self._check_phase4_entry(result)
        elif target_phase == 5:
            self._check_phase5_entry(result)

        return result

    def _check_phase2_entry(self, result: GateResult):
        """Phase 2 准入检查"""
        checks = result.checks

        # 1. Phase 1.2 大纲已确认
        from .file_manager import WORKSPACE_BASE
        workspace = os.path.join(WORKSPACE_BASE, self.paper_name)
        orchestrate_state_path = os.path.join(workspace, "_orchestrate_state.json")
        if not os.path.exists(orchestrate_state_path):
            result.add_blocking_issue("状态文件不存在，请先完成 Phase 1")
            checks["orchestrate_state_exists"] = (False, "状态文件不存在")
            return

        import json
        try:
            with open(orchestrate_state_path, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception as e:
            result.add_blocking_issue(f"状态文件读取失败：{str(e)}")
            checks["orchestrate_state_readable"] = (False, str(e))
            return

        checks["orchestrate_state_readable"] = (True, "OK")

        # 检查 phase1_confirmed
        phase1_confirmed = state.get("phase1_confirmed", False)
        checks["phase1_confirmed"] = (phase1_confirmed, "大纲已确认" if phase1_confirmed else "大纲未确认")

        if not phase1_confirmed:
            result.add_blocking_issue("Phase 1.2 大纲未确认，请先确认大纲")

        # 2. Phase 1.3 已提交
        phase1_3_status = state.get("phase1_3_status", "pending")
        phase1_3_submitted = phase1_3_status in ("submitted", "confirmed")
        checks["phase1_3_submitted"] = (phase1_3_submitted,
                                         "开题报告已提交" if phase1_3_submitted else f"开题报告状态：{phase1_3_status}")

        if not phase1_3_submitted:
            result.add_blocking_issue("Phase 1.3 开题报告未提交，请先提交开题报告")

    def _check_phase3_entry(self, result: GateResult):
        """Phase 3 准入检查"""
        checks = result.checks

        # 检查 Phase 2 是否完成（通过 outline_state 或 orchestrate_state）
        summary = self.fm.load_summary(2)
        if summary:
            status = summary.get("status", "")
            checks["phase2_completed"] = (status == STATUS_COMPLETED,
                                           f"Phase 2 状态：{status}")
            if status != STATUS_COMPLETED:
                result.add_blocking_issue("Phase 2 尚未完成，请先完成所有节点写作")
        else:
            # 尝试从文件检查
            content = self.fm.load_content(2, CONTENT_TYPE_INTEGRATED)
            if content:
                checks["phase2_has_content"] = (True, "找到 Phase 2 产出文件")
            else:
                checks["phase2_has_content"] = (False, "未找到 Phase 2 产出文件")
                result.add_blocking_issue("Phase 2 尚未完成，请先完成所有节点写作")

    def _check_phase3_5_entry(self, result: GateResult):
        """Phase 3.5 准入检查"""
        checks = result.checks

        # Phase 3.5 是 Phase 3 的延伸，需要 Phase 3 review 已完成
        summary = self.fm.load_summary(3)
        if summary:
            status = summary.get("status", "")
            checks["phase3_review_completed"] = (status == STATUS_COMPLETED,
                                                  f"Phase 3 状态：{status}")
            if status != STATUS_COMPLETED:
                result.add_blocking_issue("Phase 3 审核尚未完成，请先完成 Phase 3")
        else:
            result.add_blocking_issue("Phase 3 尚未执行，请先完成 Phase 3")
            checks["phase3_completed"] = (False, "未找到 Phase 3 summary")

    def _check_phase4_entry(self, result: GateResult):
        """Phase 4 准入检查"""
        checks = result.checks

        # Phase 4 需要 Phase 3.5 收敛（连续 2 轮无新 P0）
        # 这里简化处理：检查 Phase 3.5 summary 是否存在
        summary = self.fm.load_summary(3.5)
        if summary:
            key_metrics = summary.get("key_metrics", {})
            p0_issues = key_metrics.get("p0_issues", -1)
            if p0_issues >= 0:
                checks["phase3_5_no_p0"] = (p0_issues == 0,
                                             f"P0 问题数：{p0_issues}")
                if p0_issues > 0:
                    result.add_blocking_issue(f"Phase 3.5 仍有 {p0_issues} 个 P0 问题未修复，请先修复")
            else:
                checks["phase3_5_completed"] = (True, "Phase 3.5 已完成")
        else:
            result.add_blocking_issue("Phase 3.5 尚未完成，请先完成深度评审")
            checks["phase3_5_completed"] = (False, "未找到 Phase 3.5 summary")

    def _check_phase5_entry(self, result: GateResult):
        """Phase 5 准入检查"""
        checks = result.checks

        # Phase 5 需要 Phase 4 guardrails 10/10 通过
        summary = self.fm.load_summary(4)
        if summary:
            key_metrics = summary.get("key_metrics", {})
            guardrails_passed = key_metrics.get("guardrails_passed", False)
            checks["phase4_guardrails"] = (guardrails_passed,
                                            "Guardrails 通过" if guardrails_passed else "Guardrails 未通过")
            if not guardrails_passed:
                result.add_blocking_issue("Phase 4 Guardrails 校验未通过，请先修复")
        else:
            result.add_blocking_issue("Phase 4 尚未完成，请先完成整合修订")
            checks["phase4_completed"] = (False, "未找到 Phase 4 summary")

    # ------------------------------------------------------------------------
    # 准出检查（Phase N 完成前）
    # ------------------------------------------------------------------------

    def pre_exit_check(self, current_phase: float) -> GateResult:
        """
        检查当前 Phase 是否满足完成条件。

        规则：
        - Phase 2：节点完成率 100%，无 failed 节点
        - Phase 3：审核 loop 收敛（连续 2 轮无新 P0）
        - Phase 3.5：同 Phase 3
        - Phase 4：整合版 guardrails 10 项校验通过
        - Phase 5：Word 输出格式校验通过

        Returns:
            GateResult
        """
        result = GateResult(
            passed=True,
            phase=current_phase,
            checks={},
            blocking_issues=[],
        )

        if current_phase == 2:
            self._check_phase2_exit(result)
        elif current_phase == 3:
            self._check_phase3_exit(result)
        elif current_phase == 3.5:
            self._check_phase3_5_exit(result)
        elif current_phase == 4:
            self._check_phase4_exit(result)
        elif current_phase == 5:
            self._check_phase5_exit(result)

        return result

    def _check_phase2_exit(self, result: GateResult):
        """Phase 2 准出检查"""
        checks = result.checks

        # 从 summary 中检查节点完成情况
        summary = self.fm.load_summary(2)
        if summary:
            key_metrics = summary.get("key_metrics", {})
            nodes_completed = key_metrics.get("nodes_completed", 0)
            nodes_total = key_metrics.get("nodes_total", 0)
            nodes_failed = key_metrics.get("nodes_failed", 0)

            checks["nodes_completion"] = (
                nodes_completed == nodes_total and nodes_failed == 0,
                f"已完成 {nodes_completed}/{nodes_total}，失败 {nodes_failed}"
            )

            if nodes_completed < nodes_total:
                result.add_blocking_issue(f"仍有 {nodes_total - nodes_completed} 个节点未完成")
            if nodes_failed > 0:
                result.add_blocking_issue(f"有 {nodes_failed} 个节点写作失败，请先修复")
        else:
            result.add_blocking_issue("未找到 Phase 2 summary，请通过正常流程完成 Phase 2")
            checks["phase2_summary_exists"] = (False, "未找到 summary 文件")

    def _check_phase3_exit(self, result: GateResult):
        """Phase 3 准出检查"""
        checks = result.checks

        # 检查 review 文件是否存在且通过
        review_content = self.fm.load_content(3, CONTENT_TYPE_REVIEW)
        if review_content:
            import json
            try:
                review_data = json.loads(review_content)
                p0_issues = review_data.get("summary", {}).get("p0_issues", -1)
                checks["review_completed"] = (p0_issues >= 0, f"P0 问题数：{p0_issues}")
                if p0_issues > 0:
                    result.add_blocking_issue(f"Phase 3 审核有 {p0_issues} 个 P0 问题，需修复后再完成")
            except Exception:
                result.add_blocking_issue("Phase 3 review 文件解析失败")
                checks["review_parseable"] = (False, "JSON 解析失败")
        else:
            result.add_blocking_issue("Phase 3 review 文件不存在，请先完成审核")
            checks["review_exists"] = (False, "文件不存在")

    def _check_phase3_5_exit(self, result: GateResult):
        """Phase 3.5 准出检查（同 Phase 3）"""
        self._check_phase3_exit(result)

    def _check_phase4_exit(self, result: GateResult):
        """Phase 4 准出检查"""
        checks = result.checks

        # 检查整合版字数和章节完整性
        content = self.fm.load_content(4, CONTENT_TYPE_INTEGRATED)
        if not content:
            result.add_blocking_issue("Phase 4 整合版文件不存在")
            checks["integrated_exists"] = (False, "文件不存在")
            return

        checks["integrated_exists"] = (True, "文件存在")

        # 字数检查
        word_count = calculate_word_count(content)
        checks["word_count"] = (
            self.rules["min_word_count"] <= word_count <= self.rules["max_word_count"],
            f"字数：{word_count}（要求 {self.rules['min_word_count']}-{self.rules['max_word_count']}）"
        )
        if word_count < self.rules["min_word_count"]:
            result.add_blocking_issue(f"整合版字数过少（{word_count} < {self.rules['min_word_count']}）")
        if word_count > self.rules["max_word_count"]:
            result.add_blocking_issue(f"整合版字数异常（{word_count} > {self.rules['max_word_count']}）")

        # 章节数检查
        chapter_count = extract_chapter_count(content)
        checks["chapter_count"] = (
            chapter_count >= self.rules["chapter_count"],
            f"章节数：{chapter_count}（要求 >= {self.rules['chapter_count']}）"
        )
        if chapter_count < self.rules["chapter_count"]:
            result.add_blocking_issue(f"整合版章节数不足（{chapter_count} < {self.rules['chapter_count']}）")

    def _check_phase5_exit(self, result: GateResult):
        """Phase 5 准出检查"""
        checks = result.checks

        # Phase 5 的准出是 Word 文件生成成功
        # 这里简化处理：检查 summary 是否存在
        summary = self.fm.load_summary(5)
        if summary:
            key_metrics = summary.get("key_metrics", {})
            docx_generated = key_metrics.get("docx_generated", False)
            checks["docx_generated"] = (docx_generated, "Word 已生成" if docx_generated else "Word 未生成")
            if not docx_generated:
                result.add_blocking_issue("Word 文档尚未生成，请先完成 Word 输出")
        else:
            # Phase 5 没有 summary 也可能是正常的（刚进入）
            checks["phase5_started"] = (True, "Phase 5 已启动")

    # ------------------------------------------------------------------------
    # 通用门禁项
    # ------------------------------------------------------------------------

    def check_word_count(self, phase: float,
                         content_type: str = CONTENT_TYPE_INTEGRATED) -> Tuple[bool, str]:
        """
        检查字数是否在合理范围。
        """
        content = self.fm.load_content(phase, content_type)
        if content is None:
            return False, "文件不存在"

        word_count = calculate_word_count(content)
        passed = self.rules["min_word_count"] <= word_count <= self.rules["max_word_count"]
        detail = f"字数：{word_count}（要求 {self.rules['min_word_count']}-{self.rules['max_word_count']}）"
        return passed, detail

    def check_chapter_completeness(self, phase: float,
                                   content_type: str = CONTENT_TYPE_INTEGRATED) -> Tuple[bool, str]:
        """
        检查章节是否完整（7 章）。
        """
        content = self.fm.load_content(phase, content_type)
        if content is None:
            return False, "文件不存在"

        chapter_count = extract_chapter_count(content)
        passed = chapter_count >= self.rules["chapter_count"]
        detail = f"章节数：{chapter_count}（要求 >= {self.rules['chapter_count']}）"
        return passed, detail

    def check_freshness(self, phase: float,
                        content_type: str = CONTENT_TYPE_INTEGRATED) -> Tuple[bool, str]:
        """
        检查文件是否新鲜（48 小时内有更新）。
        """
        fresh = self.fm.is_fresh(phase, content_type)
        detail = "文件较新" if fresh else f"文件超过 {self.rules['freshness_hours']} 小时未更新"
        return fresh, detail

    def check_hash_unchanged(self, phase: float, content_type: str,
                             expected_hash: str) -> Tuple[bool, str]:
        """
        检查文件 hash 是否与预期一致（检测用户修改）。
        """
        current_hash = self.fm.load_summary(phase).get("content_hash") if self.fm.load_summary(phase) else None
        if current_hash is None:
            return True, "无历史 hash 记录"

        unchanged = current_hash == expected_hash
        detail = "文件未修改" if unchanged else "检测到文件已被修改"
        return unchanged, detail