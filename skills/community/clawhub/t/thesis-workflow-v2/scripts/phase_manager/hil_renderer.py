"""
Phase Manager - HIL 消息渲染
hil_renderer.py

只输出文件路径 + 摘要，不塞正文内容。
"""

from typing import Dict, Optional, List

from .schemas import (
    PhaseSummary,
    GateResult,
    PHASE_NAMES,
    STATUS_COMPLETED,
    STATUS_FAILED,
    STATUS_MODIFIED,
    CONTENT_TYPE_INTEGRATED,
)
from .file_manager import PhaseFileManager


# ============================================================================
# PhaseHILRenderer 类
# ============================================================================

class PhaseHILRenderer:
    """
    Phase HIL 消息渲染器。

    职责：
    - 渲染 HIL 确认消息（只含路径+摘要）
    - 渲染门禁失败消息
    - 渲染 Phase 状态查询消息
    - 渲染用户修改警告
    """

    def __init__(self, paper_name: str, workspace: str = None):
        self.paper_name = paper_name
        self.fm = PhaseFileManager(paper_name, workspace)

    def render_hil_message(
        self,
        phase: float,
        summary: PhaseSummary,
        next_phase: float = None,
        user_modified: bool = False,
    ) -> str:
        """
        渲染 HIL 确认消息。

        输出格式（Markdown）：

        ✅ Phase {N} 整合完成

        📄 文件：{file_path}
        📊 字数：{word_count} 字 | 章节：{chapter_count} 章
        🔍 审核结果：{审核摘要}
        🛡️ Guardrails：{通过情况}
        🕐 时间：{timestamp}
        {用户修改提示（如有）}

        下一阶段：Phase {N+1}
        操作指令：
        - [确认] → 进入 Phase {N+1}
        - [修改文件] → 直接编辑上方文件后说"确认修改"
        - [重新审核] → 重新跑 Phase {N} review

        Args:
            phase: 当前 Phase
            summary: PhaseSummary 对象
            next_phase: 下一 Phase 编号
            user_modified: 是否检测到用户修改

        Returns:
            Markdown 格式的 HIL 消息
        """
        phase_name = PHASE_NAMES.get(phase, f"Phase {phase}")
        next_phase_name = PHASE_NAMES.get(next_phase, f"Phase {next_phase}") if next_phase else None

        # 状态图标
        if summary is None:
            phase_name = PHASE_NAMES.get(phase, f"Phase {phase}")
            file_path = self.fm.get_file_path(phase, CONTENT_TYPE_INTEGRATED)
            return (
                f"📋 {phase_name} 产出文件：\n\n"
                f"📄 文件：`{file_path}`\n\n"
                f"请确认是否继续。"
            )

        if summary.status == STATUS_FAILED:
            status_icon = "❌"
        elif summary.status == STATUS_MODIFIED or user_modified:
            status_icon = "🔄"
        else:
            status_icon = "✅"

        # 基础信息
        lines = [
            f"{status_icon} {phase_name} 完成",
            "",
            f"📄 文件：`{summary.file_path}`",
            f"📊 字数：{summary.word_count:,} 字 | 章节：{summary.chapter_count} 章",
            f"🕐 时间：{summary.timestamp}",
            "",
        ]

        # 关键指标
        key_metrics = summary.key_metrics
        if key_metrics:
            metrics_lines = self._format_key_metrics(phase, key_metrics)
            lines.extend(metrics_lines)
            lines.append("")

        # 用户修改提示
        if summary.user_modifications or user_modified:
            lines.append("⚠️ **检测到文件已被修改**，请确认是否使用新版本继续。")
            lines.append("")

        # 操作指令
        lines.append("**操作指令：**")
        if next_phase:
            lines.append(f"- **确认** → 进入 {next_phase_name}")
        lines.append("- **修改文件** → 直接编辑上方文件，完成后说「确认修改」")
        if phase in (3, 3.5, 4):
            lines.append(f"- **重新审核** → 重新跑 {phase_name}")

        return "\n".join(lines)

    def _format_key_metrics(self, phase: float, key_metrics: Dict) -> List[str]:
        """格式化关键指标为可读行"""
        lines = []

        if phase in (1, 1.3):
            if phase == 1:
                chapter_count = key_metrics.get("chapter_count", 0)
                issues_count = key_metrics.get("issues_count", 0)
                input_type = key_metrics.get("input_type", "unknown")
                lines.append(f"📋 大纲解析：章节 {chapter_count} 个 | 问题 {issues_count} 个")
                lines.append(f"📥 输入类型：{input_type}")
            else:
                chapter_count = key_metrics.get("chapter_count", 0)
                node_count = key_metrics.get("node_count", 0)
                summary = key_metrics.get("summary", "")
                lines.append(f"🔗 归因分析：{chapter_count} 章节 | {node_count} 个节点")
                if summary:
                    lines.append(f"📝 摘要：{summary}")

        elif phase == 2:
            completed = key_metrics.get("nodes_completed", 0)
            total = key_metrics.get("nodes_total", 0)
            failed = key_metrics.get("nodes_failed", 0)
            rate = key_metrics.get("completion_rate", 0)
            lines.append(f"🔧 节点：已完成 {completed}/{total}（{rate}%）| 失败 {failed}")
            if failed > 0:
                lines.append(f"  ⚠️ 有 {failed} 个节点写作失败，需要修复")

        elif phase in (3, 3.5):
            p0 = key_metrics.get("p0_issues", 0)
            p1 = key_metrics.get("p1_issues", 0)
            p2 = key_metrics.get("p2_issues", 0)
            guardrails_passed = key_metrics.get("guardrails_passed", False)
            guardrails_detail = key_metrics.get("guardrails_detail", "")

            guardrails_icon = "✅" if guardrails_passed else "❌"
            lines.append(f"🔍 审核结果：P0:{p0} P1:{p1} P2:{p2}")
            lines.append(f"{guardrails_icon} Guardrails：{guardrails_detail or ('通过' if guardrails_passed else '未通过')}")

        elif phase == 4:
            word_count = key_metrics.get("integrated_word_count", 0)
            changes = key_metrics.get("changes_applied", 0)
            guardrails_passed = key_metrics.get("guardrails_passed", False)
            guardrails_icon = "✅" if guardrails_passed else "❌"
            lines.append(f"📝 整合版：字数 {word_count:,} | 应用修改 {changes} 处")
            lines.append(f"{guardrails_icon} Guardrails：{'通过' if guardrails_passed else '未通过'}")

        elif phase == 5:
            word_count = key_metrics.get("word_count", 0)
            docx_generated = key_metrics.get("docx_generated", False)
            guardrails_passed = key_metrics.get("guardrails_passed", False)
            docx_icon = "✅" if docx_generated else "⏳"
            guardrails_icon = "✅" if guardrails_passed else "❌"
            lines.append(f"📝 最终版：字数 {word_count:,}")
            lines.append(f"{docx_icon} Word 文档：{'已生成' if docx_generated else '生成中'}")
            lines.append(f"{guardrails_icon} Guardrails：{'通过' if guardrails_passed else '未通过'}")

        return lines

    def render_gate_failure(self, phase: float, gate_result: GateResult) -> str:
        """
        渲染门禁未通过的消息。

        输出格式：

        ❌ Phase {N} 门禁未通过

        阻塞问题：
        - {issue 1}
        - {issue 2}

        请修复上述问题后重试。

        Args:
            phase: 当前 Phase
            gate_result: GateResult 对象

        Returns:
            Markdown 格式的错误消息
        """
        phase_name = PHASE_NAMES.get(phase, f"Phase {phase}")

        lines = [
            f"❌ {phase_name} 门禁未通过",
            "",
        ]

        if gate_result.blocking_issues:
            lines.append("**阻塞问题：**")
            for issue in gate_result.blocking_issues:
                lines.append(f"- {issue}")
            lines.append("")
        else:
            lines.append("**检查详情：**")
            for check_name, (passed, detail) in gate_result.checks.items():
                icon = "✅" if passed else "❌"
                lines.append(f"{icon} {check_name}：{detail}")
            lines.append("")

        lines.append("请修复上述问题后重试。")

        return "\n".join(lines)

    def render_phase_status(self, phase: float) -> str:
        """
        渲染 Phase 当前状态（用于 --status 查询）。

        Args:
            phase: Phase 编号

        Returns:
            Markdown 格式的状态消息
        """
        phase_name = PHASE_NAMES.get(phase, f"Phase {phase}")

        lines = [
            f"📋 {phase_name} 状态",
            "",
        ]

        # 加载 summary
        summary_data = self.fm.load_summary(phase)
        if summary_data:
            status = summary_data.get("status", "unknown")
            timestamp = summary_data.get("timestamp", "unknown")
            word_count = summary_data.get("word_count", 0)
            chapter_count = summary_data.get("chapter_count", 0)
            user_mod = summary_data.get("user_modifications", False)

            status_icon = "✅" if status == STATUS_COMPLETED else "🔄" if status == STATUS_MODIFIED else "❌" if status == STATUS_FAILED else "⏳"
            lines.append(f"状态：{status_icon} {status}")
            lines.append(f"更新时间：{timestamp}")
            lines.append(f"字数：{word_count:,} | 章节：{chapter_count}")

            if user_mod:
                lines.append("⚠️ 文件已被用户修改")

            key_metrics = summary_data.get("key_metrics", {})
            if key_metrics:
                lines.append("")
                lines.extend(self._format_key_metrics(phase, key_metrics))
        else:
            lines.append("状态：⏳ 尚未开始")
            lines.append(f"文件：{self.fm.get_file_path(phase, 'integrated')}")

        return "\n".join(lines)

    def render_all_phases_status(self) -> str:
        """
        渲染所有 Phase 的状态列表。

        Returns:
            Markdown 格式的状态汇总
        """
        lines = [
            "📊 论文进度总览",
            "",
        ]

        for phase in [1, 2, 3, 3.5, 4, 5]:
            phase_name = PHASE_NAMES.get(phase, f"Phase {phase}")
            summary_data = self.fm.load_summary(phase)

            if summary_data:
                status = summary_data.get("status", "unknown")
                status_icon = "✅" if status == STATUS_COMPLETED else "🔄" if status == STATUS_MODIFIED else "❌" if status == STATUS_FAILED else "⏳"
                word_count = summary_data.get("word_count", 0)
                lines.append(f"Phase {phase} {phase_name}：{status_icon} {status}（{word_count:,} 字）")
            else:
                lines.append(f"Phase {phase} {phase_name}：⏳ 尚未开始")

        return "\n".join(lines)

    def render_user_modification_warning(
        self,
        phase: float,
        old_hash: str,
        new_hash: str,
    ) -> str:
        """
        检测到用户修改文件时的提示。

        Args:
            phase: Phase 编号
            old_hash: 之前的 hash
            new_hash: 当前的 hash

        Returns:
            Markdown 格式的警告消息
        """
        phase_name = PHASE_NAMES.get(phase, f"Phase {phase}")

        lines = [
            f"⚠️ 检测到 {phase_name} 文件已被修改",
            "",
            "**变更说明：**",
            f"- 之前 hash：`{old_hash[:8]}...`",
            f"- 当前 hash：`{new_hash[:8]}...`",
            "",
            "**下一步：**",
            "请确认是否使用新版本继续，或撤销修改。",
            "",
            "操作指令：",
            "- **确认修改** → 使用新版本进入下一 Phase",
            "- **撤销修改** → 恢复上一版本",
        ]

        return "\n".join(lines)

    def render_hil_for_confirm(
        self,
        phase: float,
        summary: PhaseSummary,
        next_phase: float,
    ) -> str:
        """
        渲染用户说「确认」后的 HIL 消息。

        与 render_hil_message 类似，但更简洁，用于确认流程。

        Args:
            phase: 当前 Phase
            summary: PhaseSummary 对象
            next_phase: 下一 Phase 编号

        Returns:
            Markdown 格式的确认消息
        """
        phase_name = PHASE_NAMES.get(phase, f"Phase {phase}")
        next_phase_name = PHASE_NAMES.get(next_phase, f"Phase {next_phase}")

        lines = [
            f"✅ {phase_name} 已确认",
            "",
            f"→ 正在进入 {next_phase_name}...",
        ]

        return "\n".join(lines)

    def render_transition_record(self) -> str:
        """
        渲染流转记录。

        Returns:
            Markdown 格式的流转历史
        """
        transitions = self.fm.load_transitions()

        if not transitions:
            return "📝 暂无流转记录"

        lines = [
            "📝 Phase 流转记录",
            "",
        ]

        for i, t in enumerate(reversed(transitions[-10:]), 1):  # 最近10条
            from_phase = t.get("from_phase", "?")
            to_phase = t.get("to_phase", "?")
            triggered_by = t.get("triggered_by", "?")
            triggered_at = t.get("triggered_at", "?")
            gate_passed = t.get("gate_passed", False)

            icon = "✅" if gate_passed else "❌"
            from_name = PHASE_NAMES.get(from_phase, f"Phase {from_phase}")
            to_name = PHASE_NAMES.get(to_phase, f"Phase {to_phase}")

            lines.append(
                f"{icon} {from_name} → {to_name} "
                f"（{triggered_by}，{triggered_at[:16]}）"
            )

        return "\n".join(lines)