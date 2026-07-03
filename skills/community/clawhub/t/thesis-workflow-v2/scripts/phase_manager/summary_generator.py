"""
Phase Manager - 摘要生成
summary_generator.py

将 Phase 产出转化为结构化 PhaseSummary。
"""

from typing import Dict, Optional, Any

from .schemas import (
    PhaseSummary,
    STATUS_COMPLETED,
    STATUS_FAILED,
    STATUS_MODIFIED,
    CONTENT_TYPE_INTEGRATED,
    CONTENT_TYPE_REVIEW,
    CONTENT_TYPE_SUMMARY,
    calculate_content_hash,
    calculate_word_count,
    extract_chapter_count,
    now_iso,
    PHASE_NAMES,
)
from .file_manager import PhaseFileManager


# ============================================================================
# PhaseSummaryGenerator 类
# ============================================================================

class PhaseSummaryGenerator:
    """
    将 Phase 产出转化为结构化 PhaseSummary。

    职责：
    - 从文件或 phase_result 中提取摘要信息
    - 计算 word_count、chapter_count、content_hash
    - 构建 key_metrics（根据 Phase 类型不同）
    """

    def __init__(self, paper_name: str, workspace: str = None):
        self.paper_name = paper_name
        self.fm = PhaseFileManager(paper_name, workspace)

    def generate_phase_summary(
        self,
        phase: float,
        phase_result: Dict = None,
        file_content: str = None,
        status: str = STATUS_COMPLETED,
    ) -> PhaseSummary:
        """
        从 Phase 执行结果或文件中提取 PhaseSummary。

        优先使用 phase_result 中的数据，其次从文件读取。

        Args:
            phase: Phase 编号
            phase_result: Phase 执行结果（可能包含大量 content）
            file_content: 直接传入的文件内容（优先使用）
            status: Phase 状态（默认 completed）

        Returns:
            PhaseSummary
        """
        # 优先使用直接传入的文件内容
        if file_content is not None:
            content = file_content
        elif phase_result and "content" in phase_result:
            content = phase_result["content"]
        else:
            content = self.fm.load_content(phase, CONTENT_TYPE_INTEGRATED) or ""

        # 计算基本信息
        content_hash = calculate_content_hash(content)
        word_count = calculate_word_count(content)
        chapter_count = extract_chapter_count(content)

        # 构建 key_metrics
        key_metrics = self.build_key_metrics(phase, phase_result or {}, content)

        # 检测用户修改
        expected_hash = None
        old_summary = self.fm.load_summary(phase)
        if old_summary:
            expected_hash = old_summary.get("content_hash")
        user_modifications = (expected_hash is not None and content_hash != expected_hash)

        # 更新状态
        if user_modifications:
            status = STATUS_MODIFIED

        # 生成一句话摘要
        message = self._generate_message(phase, status, key_metrics, word_count, chapter_count)

        # 文件路径
        file_path = self.fm.get_file_path(phase, CONTENT_TYPE_INTEGRATED)

        return PhaseSummary(
            phase=phase,
            status=status,
            timestamp=now_iso(),
            file_path=file_path,
            content_hash=content_hash,
            word_count=word_count,
            chapter_count=chapter_count,
            key_metrics=key_metrics,
            user_modifications=user_modifications,
            message=message,
        )

    def build_key_metrics(self, phase: float, phase_result: Dict,
                          content: str = None) -> Dict[str, Any]:
        """
        根据 Phase 类型构建 key_metrics。

        Phase 2: {nodes_total, nodes_completed, nodes_failed, completion_rate}
        Phase 3: {p0_issues, p1_issues, p2_issues, guardrails_passed, guardrails_detail}
        Phase 3.5: 同 Phase 3
        Phase 4: {integrated_word_count, changes_applied, guardrails_passed}
        Phase 5: {word_count, guardrails_passed, docx_generated}
        """
        metrics = {}

        if phase in (1, 1.3):
            # Phase 1: outline 结构统计；Phase 1.3: 归因结果统计
            review_data = phase_result.get("review_data", {})
            if not review_data:
                review_content = self.fm.load_content(phase, CONTENT_TYPE_REVIEW)
                if review_content:
                    import json
                    try:
                        review_data = json.loads(review_content)
                    except Exception:
                        pass
            if phase == 1:
                outline = review_data.get("outline", {})
                chapter_count = len(outline) if isinstance(outline, dict) else 0
                metrics = {
                    "chapter_count": chapter_count,
                    "issues_count": len(review_data.get("issues", [])),
                    "input_type": review_data.get("input_type", "unknown"),
                }
            else:  # 1.3
                metrics = {
                    "chapter_count": review_data.get("chapter_count", 0),
                    "node_count": review_data.get("node_count", 0),
                    "summary": str(review_data.get("summary", ""))[:50],
                }

        elif phase == 2:
            # 从 review_report（由 append_node_review 写入）或 phase_result 中提取统计
            review_data = phase_result.get("review_report") if phase_result else None

            if review_data is None:
                review_content = self.fm.load_content(phase, CONTENT_TYPE_REVIEW)
                if review_content:
                    import json
                    try:
                        review_data = json.loads(review_content)
                    except Exception:
                        pass

            # 优先从 review_data._stats 读（append_node_review 写入的累计统计）
            if review_data and "_stats" in review_data:
                stats = review_data["_stats"]
                nodes_total = stats.get("nodes_total", 0)
                nodes_completed = stats.get("nodes_completed", 0)
                nodes_failed = stats.get("nodes_failed", 0)
            elif review_data and "nodes" in review_data:
                nodes = review_data["nodes"]
                nodes_total = len(nodes)
                nodes_completed = sum(1 for n in nodes.values() if n.get("status") == "completed")
                nodes_failed = sum(1 for n in nodes.values() if n.get("status") == "failed")
            else:
                # 尝试从 summary 加载
                summary = self.fm.load_summary(phase)
                if summary:
                    km = summary.get("key_metrics", {})
                    nodes_total = km.get("nodes_total", 0)
                    nodes_completed = km.get("nodes_completed", 0)
                    nodes_failed = km.get("nodes_failed", 0)
                else:
                    nodes_total = nodes_completed = nodes_failed = 0

            completion_rate = (nodes_completed / nodes_total * 100) if nodes_total > 0 else 0

            metrics = {
                "nodes_total": nodes_total,
                "nodes_completed": nodes_completed,
                "nodes_failed": nodes_failed,
                "completion_rate": round(completion_rate, 1),
            }

        elif phase in (3, 3.5):
            # 从 review_report 中提取审核结果（review_data 由 _build_hil_result 注入）
            review_data = phase_result.get("review_report") if phase_result else None
            if review_data is None:
                review_content = self.fm.load_content(phase, CONTENT_TYPE_REVIEW)
                if review_content:
                    import json
                    try:
                        review_data = json.loads(review_content)
                    except Exception:
                        pass

            if review_data:
                summary_data = review_data.get("summary", {})
                # summary_data 现在是 dict：{p0_issues, p1_issues, p2_issues, text}
                # guardrails_passed 在 review_data 顶层（Phase 3.5）
                guardrails_passed = review_data.get("guardrails_passed", False)
                if isinstance(summary_data, dict):
                    metrics = {
                        "p0_issues": summary_data.get("p0_issues", 0),
                        "p1_issues": summary_data.get("p1_issues", 0),
                        "p2_issues": summary_data.get("p2_issues", 0),
                        "guardrails_passed": guardrails_passed,
                        "guardrails_detail": summary_data.get("guardrails_detail", ""),
                    }
                else:
                    # 兼容旧格式：summary 是字符串
                    metrics = {
                        "p0_issues": review_data.get("p0_issues", 0),
                        "p1_issues": review_data.get("p1_issues", 0),
                        "p2_issues": review_data.get("p2_issues", 0),
                        "guardrails_passed": guardrails_passed,
                        "guardrails_detail": str(summary_data) if summary_data else "",
                    }
            else:
                metrics = {
                    "p0_issues": -1,
                    "p1_issues": -1,
                    "p2_issues": -1,
                    "guardrails_passed": False,
                    "guardrails_detail": "review 数据不可用",
                }

        elif phase == 4:
            # Phase 4 整合
            review_data = phase_result.get("review_report") if phase_result else None
            changes_applied = review_data.get("fixed_p0", 0) if review_data else 0
            pending_p1 = review_data.get("pending_p1", 0) if review_data else 0
            if content:
                word_count = calculate_word_count(content)
            else:
                word_count = 0

            metrics = {
                "integrated_word_count": word_count,
                "changes_applied": changes_applied,
                "pending_p1": pending_p1,
                "guardrails_passed": review_data.get("guardrails_passed", False) if review_data else False,
            }

        elif phase == 5:
            # Phase 5 终审
            review_data = phase_result.get("review_report") if phase_result else None
            if content:
                word_count = calculate_word_count(content)
            else:
                word_count = 0

            guardrails_pass = review_data.get("guardrails_pass", False) if review_data else False
            docx_generated = phase_result.get("docx_generated", False) if phase_result else False

            metrics = {
                "word_count": word_count,
                "guardrails_passed": guardrails_pass,
                "docx_generated": docx_generated,
            }

        return metrics

    def _generate_message(self, phase: float, status: str,
                          key_metrics: Dict, word_count: int,
                          chapter_count: int) -> str:
        """生成一句话摘要"""
        phase_name = PHASE_NAMES.get(phase, f"Phase {phase}")

        if status == STATUS_FAILED:
            return f"❌ {phase_name} 失败"

        if status == STATUS_MODIFIED:
            return f"🔄 {phase_name} 完成（用户已修改）"

        if phase == 2:
            completed = key_metrics.get("nodes_completed", 0)
            total = key_metrics.get("nodes_total", 0)
            failed = key_metrics.get("nodes_failed", 0)
            return f"✅ {phase_name} 完成（已完成 {completed}/{total} 节点，失败 {failed}）"

        elif phase in (3, 3.5):
            p0 = key_metrics.get("p0_issues", 0)
            p1 = key_metrics.get("p1_issues", 0)
            guardrails = "通过" if key_metrics.get("guardrails_passed") else "未通过"
            return f"✅ {phase_name} 完成（P0:{p0} P1:{p1} Guardrails:{guardrails}）"

        elif phase == 4:
            changes = key_metrics.get("changes_applied", 0)
            return f"✅ {phase_name} 完成（应用 {changes} 处修改，字数 {word_count}）"

        elif phase == 5:
            docx = "已生成" if key_metrics.get("docx_generated") else "未生成"
            return f"✅ {phase_name} 完成（Word {docx}）"

        return f"✅ {phase_name} 完成"

    def update_summary_from_file(self, phase: float) -> Optional[PhaseSummary]:
        """
        从已存在的文件更新 summary。

        用于用户修改文件后重新生成 summary。

        Returns:
            PhaseSummary 或 None
        """
        content = self.fm.load_content(phase, CONTENT_TYPE_INTEGRATED)
        if content is None:
            return None

        return self.generate_phase_summary(
            phase=phase,
            file_content=content,
            status=STATUS_MODIFIED,
        )

    def get_summary(self, phase: float) -> Optional[PhaseSummary]:
        """
        获取指定 Phase 的 summary。

        优先从文件加载，否则返回 None。
        """
        summary_data = self.fm.load_summary(phase)
        if summary_data is None:
            return None

        try:
            return PhaseSummary.from_dict(summary_data)
        except Exception:
            return None