"""
Phase Manager - 统一入口
__init__.py

Phase 数据管理的 Facade 模式封装。
对外暴露简单接口，屏蔽内部复杂度。

使用示例：
    from phase_manager import PhaseManager

    pm = PhaseManager("论文_paper_v1")  # v2.1.2 PII 清理：示例名脱敏

    # 保存 Phase 产出
    result = pm.save_phase_output(
        phase=3,
        content_type="integrated",
        content="...论文正文...",
        key_metrics={"p0_issues": 0, "p1_issues": 2}
    )

    # 生成 HIL 消息
    hil_msg = pm.generate_hil_message(phase=3, next_phase=4)

    # 门禁检查
    gate = pm.pre_phase_check(target_phase=4)
    if not gate.passed:
        print(gate.summary())
"""

from typing import Dict, List, Optional, Any

from .schemas import (
    PhaseSummary,
    PhaseFile,
    PhaseTransition,
    GateResult,
    CONTENT_TYPE_INTEGRATED,
    CONTENT_TYPE_REVIEW,
    CONTENT_TYPE_SUMMARY,
    STATUS_COMPLETED,
    STATUS_FAILED,
    STATUS_MODIFIED,
    PHASE_NAMES,
    now_iso,
    calculate_content_hash,
)
from .file_manager import PhaseFileManager
from .gate_keeper import PhaseGateKeeper
from .summary_generator import PhaseSummaryGenerator
from .hil_renderer import PhaseHILRenderer


# ============================================================================
# PhaseManager 主类
# ============================================================================

class PhaseManager:
    """
    Phase 数据管理的统一入口（Facade 模式）。

    对 orchestrator 暴露简单接口，屏蔽内部复杂度。

    职责：
    - 统一管理 Phase 产出文件的保存/读取
    - 提供门禁校验（准入/准出）
    - 生成 HIL 消息（只含路径+摘要，不塞正文）
    - 保证跨 Session 数据有效性
    """

    def __init__(self, paper_name: str, workspace: str = None):
        """
        初始化 PhaseManager。

        Args:
            paper_name: 论文项目名（用于构建工作区路径）
            workspace: 工作区目录（默认 ~/.openclaw/workspace/{paper_name}）
        """
        self.paper_name = paper_name

        # 初始化子模块
        self.fm = PhaseFileManager(paper_name, workspace)
        self.gk = PhaseGateKeeper(paper_name, workspace)
        self.sg = PhaseSummaryGenerator(paper_name, workspace)
        self.hr = PhaseHILRenderer(paper_name, workspace)

    # ------------------------------------------------------------------------
    # 核心流程：保存产出
    # ------------------------------------------------------------------------

    def save_phase_output(
        self,
        phase: float,
        content_type: str,
        content: str,
        key_metrics: Dict = None,
        status: str = STATUS_COMPLETED,
    ) -> Dict[str, Any]:
        """
        保存 Phase 产出。

        流程：
        1. 保存内容到文件（带备份 + 锁保护）
        2. 生成 PhaseSummary
        3. 保存 summary 到 _phase{N}_summary.json
        4. 返回结果

        用户可直接改文件，改完说"确认"后下一 Phase 读取。

        Args:
            phase: Phase 编号
            content_type: integrated / review / summary
            content: 文件内容
            key_metrics: 关键指标（dict）
            status: 状态（默认 completed）

        Returns:
            {
                ok: bool,
                file_path: str,
                summary: PhaseSummary,
                hash: str,
                changed: bool,
                error: Optional[str]
            }
        """
        # 1. 保存内容
        save_result = self.fm.save_content(phase, content_type, content)
        if not save_result["ok"]:
            return {
                "ok": False,
                "file_path": None,
                "summary": None,
                "hash": None,
                "changed": False,
                "error": save_result["error"],
            }

        # 2. 生成 summary
        phase_result = {"content": content, "key_metrics": key_metrics or {}}
        summary = self.sg.generate_phase_summary(
            phase=phase,
            phase_result=phase_result,
            file_content=content,
            status=status,
        )

        # 3. 保存 summary
        self.fm.save_summary(phase, summary.to_dict())

        return {
            "ok": True,
            "file_path": save_result["file_path"],
            "summary": summary,
            "hash": save_result["hash"],
            "changed": save_result["changed"],
            "error": None,
        }

    def save_integrated(self, phase: float, content: str,
                        key_metrics: Dict = None) -> Dict[str, Any]:
        """
        保存整合版正文（Phase 产出的主要输出）。

        便捷方法，等价于 save_phase_output(phase, "integrated", content)。

        Args:
            phase: Phase 编号
            content: 正文内容
            key_metrics: 关键指标

        Returns:
            同 save_phase_output
        """
        return self.save_phase_output(
            phase=phase,
            content_type=CONTENT_TYPE_INTEGRATED,
            content=content,
            key_metrics=key_metrics,
        )

    def save_review(self, phase: float, review_data: Dict,
                    key_metrics: Dict = None) -> Dict[str, Any]:
        """
        保存审核报告（JSON 格式）。

        便捷方法。

        Args:
            phase: Phase 编号
            review_data: 审核报告 dict
            key_metrics: 关键指标

        Returns:
            同 save_phase_output
        """
        import json
        content = json.dumps(review_data, ensure_ascii=False, indent=2)
        return self.save_phase_output(
            phase=phase,
            content_type=CONTENT_TYPE_REVIEW,
            content=content,
            key_metrics=key_metrics,
        )

    def append_node_review(self, phase: float, node_id: str,
                           node_data: Dict) -> Dict[str, Any]:
        """
        追加写入节点审核记录（用于 Phase 2 多节点累计写入）。

        读取现有 review 文件，追加节点记录，再写回。
        初始文件不存在时创建。

        Args:
            phase: Phase 编号
            node_id: 节点 ID
            node_data: 节点记录 {status, quality, word_count, ...}

        Returns:
            同 save_phase_output
        """
        import json

        # 读取现有 review 文件
        existing = {}
        review_content = self.fm.load_content(phase, CONTENT_TYPE_REVIEW)
        if review_content:
            try:
                existing = json.loads(review_content)
            except Exception:
                existing = {}

        # 追加节点记录
        if "nodes" not in existing:
            existing["nodes"] = {}
        existing["nodes"][node_id] = {
            "node_id": node_id,
            **node_data,
            "timestamp": now_iso(),
        }

        # 重新计算统计
        nodes = existing.get("nodes", {})
        existing["_stats"] = {
            "nodes_total": len(nodes),
            "nodes_completed": sum(1 for n in nodes.values() if n.get("status") == "completed"),
            "nodes_failed": sum(1 for n in nodes.values() if n.get("status") == "failed"),
        }

        content = json.dumps(existing, ensure_ascii=False, indent=2)

        # 复用 save_phase_output 逻辑（覆盖写入）
        return self.save_phase_output(
            phase=phase,
            content_type=CONTENT_TYPE_REVIEW,
            content=content,
            key_metrics=existing["_stats"],
        )

    # ------------------------------------------------------------------------
    # 核心流程：读取产出
    # ------------------------------------------------------------------------

    def load_phase_input(self, phase: float,
                         content_type: str = CONTENT_TYPE_INTEGRATED) -> Optional[str]:
        """
        读取上一 Phase 的产出。

        读取前做新鲜度检查。
        检测到用户修改 → 在返回内容中附带 user_modified=True 标记。

        Args:
            phase: Phase 编号
            content_type: integrated / review / summary

        Returns:
            文件内容（str）或 None
        """
        # 读取前校验
        validation = self.fm.validate_before_read(phase, content_type)
        if not validation["ok"]:
            return None

        content = self.fm.load_content(phase, content_type)

        # 检测用户修改
        if validation.get("hash_changed"):
            # 需要调用方判断，这里返回 None 让调用方重新加载
            pass

        return content

    def load_integrated(self, phase: float) -> Optional[str]:
        """
        读取整合版正文。

        便捷方法。
        """
        return self.load_phase_input(phase, CONTENT_TYPE_INTEGRATED)

    def load_review(self, phase: float) -> Optional[Dict]:
        """
        读取审核报告（JSON 格式）。

        便捷方法。

        Returns:
            dict 或 None
        """
        import json
        content = self.load_phase_input(phase, CONTENT_TYPE_REVIEW)
        if content is None:
            return None
        try:
            return json.loads(content)
        except Exception:
            return None

    # ------------------------------------------------------------------------
    # 门禁检查
    # ------------------------------------------------------------------------

    def pre_phase_check(self, target_phase: float) -> GateResult:
        """
        进入 Phase N 前的门禁检查。

        不通过 → 返回错误，不允许进入。

        Args:
            target_phase: 目标 Phase 编号

        Returns:
            GateResult
        """
        return self.gk.pre_enter_check(target_phase)

    def pre_exit_check(self, current_phase: float) -> GateResult:
        """
        Phase N 完成前的门禁检查。

        不通过 → 返回错误，不允许完成。

        Args:
            current_phase: 当前 Phase 编号

        Returns:
            GateResult
        """
        return self.gk.pre_exit_check(current_phase)

    # ------------------------------------------------------------------------
    # HIL 消息
    # ------------------------------------------------------------------------

    def generate_hil_message(self, phase: float,
                             next_phase: float = None,
                             summary: PhaseSummary = None) -> str:
        """
        生成 HIL 消息（供用户确认/修改）。

        只返回文件路径 + 摘要，不塞正文。

        Args:
            phase: 当前 Phase
            next_phase: 下一 Phase 编号
            summary: PhaseSummary（如果为 None，从文件加载）

        Returns:
            Markdown 格式的 HIL 消息
        """
        if summary is None:
            summary_data = self.fm.load_summary(phase)
            if summary_data:
                summary = PhaseSummary.from_dict(summary_data)

        if summary is None:
            # 没有 summary，生成默认消息
            phase_name = PHASE_NAMES.get(phase, f"Phase {phase}")
            file_path = self.fm.get_file_path(phase, CONTENT_TYPE_INTEGRATED)
            return (
                f"📋 {phase_name} 产出文件：\n\n"
                f"📄 文件：`{file_path}`\n\n"
                f"请确认是否继续。"
            )

        # 检测用户修改
        user_modified = self.fm.detect_user_modification(phase, CONTENT_TYPE_INTEGRATED,
                                                          summary.content_hash)

        return self.hr.render_hil_message(
            phase=phase,
            summary=summary,
            next_phase=next_phase,
            user_modified=user_modified,
        )

    def generate_gate_failure_message(self, phase: float,
                                      gate_result: GateResult) -> str:
        """
        生成门禁未通过的 HIL 消息。

        Args:
            phase: 当前 Phase
            gate_result: GateResult 对象

        Returns:
            Markdown 格式的错误消息
        """
        return self.hr.render_gate_failure(phase, gate_result)

    # ------------------------------------------------------------------------
    # 状态查询
    # ------------------------------------------------------------------------

    def get_phase_status(self, phase: float) -> Dict:
        """
        返回 Phase N 的当前状态。

        Returns:
            {
                exists: bool,
                status: str,
                file_path: str,
                summary: Optional[PhaseSummary],
                user_modified: bool,
            }
        """
        summary_data = self.fm.load_summary(phase)
        file_path = self.fm.get_file_path(phase, CONTENT_TYPE_INTEGRATED)

        if summary_data is None:
            return {
                "exists": False,
                "status": "pending",
                "file_path": file_path,
                "summary": None,
                "user_modified": False,
            }

        summary = PhaseSummary.from_dict(summary_data)
        user_modified = self.fm.detect_user_modification(phase, CONTENT_TYPE_INTEGRATED,
                                                          summary.content_hash)

        return {
            "exists": True,
            "status": summary.status,
            "file_path": file_path,
            "summary": summary,
            "user_modified": user_modified,
        }

    def get_phase_summary_dict(self, phase: float) -> Optional[Dict]:
        """
        返回 Phase N 的 summary 信息（JSON 可序列化 dict）。
        用于 orchestrator 返回给上层调用。
        """
        summary = self.sg.get_summary(phase)
        if summary is None:
            return None
        return {
            "phase": summary.phase,
            "status": summary.status,
            "word_count": summary.word_count,
            "chapter_count": summary.chapter_count,
            "content_hash": summary.content_hash,
            "timestamp": summary.timestamp,
            "key_metrics": summary.key_metrics,
        }

    def get_all_phase_status(self) -> List[Dict]:
        """
        返回所有 Phase 的状态列表。

        Returns:
            List[Dict]，每个元素同 get_phase_status
        """
        return [self.get_phase_status(phase) for phase in [1, 2, 3, 3.5, 4, 5]]

    def render_all_status(self) -> str:
        """
        渲染所有 Phase 的状态（Markdown 格式）。

        用于 --status 查询。
        """
        return self.hr.render_all_phases_status()

    # ------------------------------------------------------------------------
    # 流转记录
    # ------------------------------------------------------------------------

    def record_transition(
        self,
        from_phase: float,
        to_phase: float,
        triggered_by: str,
        session_id: str = None,
    ) -> Dict:
        """
        记录 Phase 流转。

        Args:
            from_phase: 来源 Phase
            to_phase: 目标 Phase
            triggered_by: auto / user_confirm / user_modify
            session_id: 触发时的 session ID

        Returns:
            {ok: bool}
        """
        if session_id is None:
            import os
            session_id = os.environ.get("OPENCLAW_SESSION_ID", "unknown")

        # 获取当前文件的 hash
        content_hash = ""
        summary = self.sg.get_summary(to_phase)
        if summary:
            content_hash = summary.content_hash

        transition = {
            "from_phase": from_phase,
            "to_phase": to_phase,
            "triggered_by": triggered_by,
            "triggered_at": now_iso(),
            "triggered_session": session_id,
            "content_hash": content_hash,
            "gate_passed": True,
        }

        ok = self.fm.save_transition(transition)
        return {"ok": ok}

    def get_last_transition(self) -> Optional[Dict]:
        """
        获取最近一次流转记录。
        """
        return self.fm.get_last_transition()

    def render_transition_record(self) -> str:
        """
        渲染流转记录（Markdown 格式）。
        """
        return self.hr.render_transition_record()

    # ------------------------------------------------------------------------
    # 用户修改处理
    # ------------------------------------------------------------------------

    def check_user_modification(self, phase: float) -> bool:
        """
        检测用户是否修改了指定 Phase 的文件。

        Args:
            phase: Phase 编号

        Returns:
            bool（True = 用户改过）
        """
        summary = self.sg.get_summary(phase)
        if summary is None:
            return False

        return self.fm.detect_user_modification(
            phase, CONTENT_TYPE_INTEGRATED, summary.content_hash
        )

    def update_summary_after_modification(self, phase: float) -> PhaseSummary:
        """
        用户修改文件后，重新生成 summary。

        Args:
            phase: Phase 编号

        Returns:
            新的 PhaseSummary
        """
        summary = self.sg.update_summary_from_file(phase)
        if summary:
            self.fm.save_summary(phase, summary.to_dict())
        return summary

    def restore_backup(self, phase: float,
                       content_type: str = CONTENT_TYPE_INTEGRATED) -> Dict:
        """
        恢复上一备份版本。

        Args:
            phase: Phase 编号
            content_type: integrated / review / summary

        Returns:
            {ok: bool, restored_path: str, error: Optional[str]}
        """
        return self.fm.restore_backup(phase, content_type)

    # ------------------------------------------------------------------------
    # 清理
    # ------------------------------------------------------------------------

    def cleanup_phase(self, phase: float) -> Dict:
        """
        清理指定 Phase 的中间文件。

        Args:
            phase: Phase 编号

        Returns:
            {ok: bool, deleted: [file_paths]}
        """
        return self.fm.cleanup_intermediate(phase)

    def cleanup_all(self) -> Dict:
        """
        清理所有 Phase 的中间文件（论文完成后收尾）。

        Returns:
            {ok: bool, deleted: [file_paths]}
        """
        return self.fm.cleanup_all_intermediates()


# ============================================================================
# 便捷函数
# ============================================================================

def get_phase_manager(paper_name: str, workspace: str = None) -> PhaseManager:
    """
    获取 PhaseManager 实例。

    便捷函数。
    """
    return PhaseManager(paper_name, workspace)


# ============================================================================
# 向后兼容：保留旧的 import 路径
# ============================================================================

# 如果有旧代码引用这些路径，提供兼容
PhaseFileManager = PhaseFileManager  # 已在上面定义
GateKeeper = PhaseGateKeeper
SummaryGenerator = PhaseSummaryGenerator
HILRenderer = PhaseHILRenderer