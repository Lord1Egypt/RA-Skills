"""
dialogue_handler.py - 验证对话处理器
用于交互式生时校正流程
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

from .calibrator import CorrectionResult, format_shift_description


@dataclass
class DialogueState:
    """对话状态"""
    session_id: str
    original_packet: Dict
    birth_dt: datetime
    candidates: List[CorrectionResult]
    selected_index: Optional[int] = None
    confirmed: bool = False


class VerificationDialogueHandler:
    """验证对话处理器（供主Agent调用）"""
    
    def __init__(self):
        self.sessions: Dict[str, DialogueState] = {}
    
    def start_session(
        self,
        session_id: str,
        original_packet: Dict,
        birth_dt: datetime,
        candidates: List[CorrectionResult]
    ) -> str:
        """
        开始新的校正会话
        
        返回：会话初始提示文本
        """
        state = DialogueState(
            session_id=session_id,
            original_packet=original_packet,
            birth_dt=birth_dt,
            candidates=candidates,
            selected_index=None,
            confirmed=False
        )
        self.sessions[session_id] = state
        
        return self._render_welcome_message(state)
    
    def _render_welcome_message(self, state: DialogueState) -> str:
        """渲染欢迎消息"""
        lines = [
            "🔮 **生时校正候选方案**",
            f"原始时间：{state.birth_dt.strftime('%Y-%m-%d %H:%M')}",
            "",
            "系统已生成以下校正方案，请选择：",
            ""
        ]
        
        # 渲染对比表
        table = self._format_comparison_table(state.candidates)
        lines.append(table)
        lines.append("")
        lines.append("请回复数字选择方案（0-2），或回复 `skip` 跳过校正")
        
        return "\n".join(lines)
    
    def _format_comparison_table(self, candidates: List[CorrectionResult]) -> str:
        """
        格式化对比表（Markdown 风格）
        
        示例：
        ```
        │ 方案 │ 偏移       │ 置信度 │ 高影响点 │ 关键变化                  │
        ├──────┼────────────┼────────┼──────────┼───────────────────────────┤
        │ 0    │ 提前1时辰  │ 0.82   │ 0        │ 命宫主星从空宫变为紫微+天府│
        │ 1    │ 推后1时辰  │ 0.65   │ 2        │ 迁移宫变动                │
        │ 2    │ 提前2时辰  │ 0.58   │ 3        │ 财帛宫化禄                │
        ```
        """
        if not candidates:
            return "（无候选方案）"
        
        # 表头
        header = f"{'方案':<4} │ {'偏移':<12} │ {'置信度':<8} │ {'高影响点':<6} │ {'关键变化':<30}"
        separator = "-" * 80
        
        lines = [header, separator]
        
        for idx, c in enumerate(candidates[:3]):  # 最多显示前3个
            shift_desc = format_shift_description(c.shift_hours)
            confidence_str = f"{c.confidence:.3f}"
            high_impact = str(c.verification_points_remaining)
            
            # 关键变化摘要（取前2个，截断至20字）
            changes = ", ".join(c.key_changes[:2]) if c.key_changes else "无显著变化"
            if len(changes) > 25:
                changes = changes[:22] + "..."
            
            line = f"{idx:<4} │ {shift_desc:<12} │ {confidence_str:<8} │ {high_impact:<6} │ {changes:<30}"
            lines.append(line)
        
        return "\n".join(lines)
    
    def present_candidates(self, results: List[CorrectionResult]) -> str:
        """
        展示校正候选结果（兼容旧接口）
        
        返回：格式化字符串（表格）
        """
        if not results:
            return "未生成任何校正候选方案"
        
        return self._format_comparison_table(results[:3])
    
    def confirm_selection(
        self,
        session_id: str,
        selected_index: int
    ) -> Dict:
        """
        用户确认选择
        
        参数：
        - session_id: 会话ID
        - selected_index: 用户选择的索引（0, 1, 2）
        
        返回：{"action": "apply" | "reject", "result": CorrectionResult}
        """
        if session_id not in self.sessions:
            return {
                "action": "reject",
                "message": "会话不存在或已过期"
            }
        
        state = self.sessions[session_id]
        
        if 0 <= selected_index < len(state.candidates):
            state.selected_index = selected_index
            state.confirmed = True
            
            return {
                "action": "apply",
                "result": state.candidates[selected_index],
                "message": f"已选择方案 {selected_index}：{format_shift_description(state.candidates[selected_index].shift_hours)}"
            }
        else:
            return {
                "action": "reject",
                "message": f"无效选择 {selected_index}，请选择 0-{len(state.candidates)-1}"
            }
    
    def skip_session(self, session_id: str) -> Dict:
        """跳过本次校正"""
        if session_id in self.sessions:
            del self.sessions[session_id]
        
        return {
            "action": "skip",
            "message": "已跳过生时校正，维持原命盘"
        }
    
    def get_session_summary(self, session_id: str) -> Optional[str]:
        """获取会话摘要"""
        if session_id not in self.sessions:
            return None
        
        state = self.sessions[session_id]
        if not state.confirmed:
            return "会话尚未完成确认"
        
        selected = state.candidates[state.selected_index]
        return (
            f"校正方案已确认：{format_shift_description(selected.shift_hours)}\n"
            f"置信度：{selected.confidence:.3f}\n"
            f"变化：{'；'.join(selected.key_changes[:3])}"
        )
    
    def cleanup_old_sessions(self, max_age_seconds: int = 300):
        """清理过期会话（5分钟超时）"""
        # 简化实现：不记录时间戳，暂不清理
        pass
