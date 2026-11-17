"""
副作用日志与追踪
─────────────────
记录所有副作用的完整审计轨迹，用于调试和回滚。
每个副作用操作（文件写入、API调用、状态变更）都在此登记。
"""
from __future__ import annotations

import json
import logging
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class SideEffectType(str, Enum):
    FILE_WRITE = "file_write"
    FILE_DELETE = "file_delete"
    API_CALL = "api_call"
    STATE_CHANGE = "state_change"
    CRON_REGISTER = "cron_register"
    CRON_UNREGISTER = "cron_unregister"


@dataclass
class SideEffectRecord:
    """单条副作用记录"""
    effect_id: str
    session_id: str
    phase: str
    effect_type: SideEffectType
    target: str                    # 目标文件路径 / API endpoint / 状态名
    details: dict[str, Any] = field(default_factory=dict)
    reversible: bool = True        # 是否可逆
    rollback_action: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


class SideEffectLogger:
    """
    副作用日志管理器

    用法:
        sel = SideEffectLogger()
        sel.log_file_write(session_id="abc", phase="reporting", path="/tmp/report.md")
        # ... 发生错误 ...
        sel.rollback_session("abc")  # 列出所有需要回滚的操作
    """

    def __init__(self, log_dir: Optional[Path] = None):
        import os as _os
        self.log_dir = log_dir or Path(_os.path.expanduser("~")) / ".uia" / "side_effects"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._records: dict[str, list[SideEffectRecord]] = {}  # session_id → records

    def _get_log_path(self, session_id: str) -> Path:
        return self.log_dir / f"{session_id}_effects.jsonl"

    def log(
        self,
        session_id: str,
        phase: str,
        effect_type: SideEffectType,
        target: str,
        details: dict[str, Any] | None = None,
        reversible: bool = True,
        rollback_action: Optional[str] = None,
    ):
        """记录一条副作用"""
        import uuid

        record = SideEffectRecord(
            effect_id=str(uuid.uuid4())[:8],
            session_id=session_id,
            phase=phase,
            effect_type=effect_type,
            target=target,
            details=details or {},
            reversible=reversible,
            rollback_action=rollback_action,
        )

        with self._lock:
            if session_id not in self._records:
                self._records[session_id] = []
            self._records[session_id].append(record)

        # 持久化到磁盘
        log_path = self._get_log_path(session_id)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "effect_id": record.effect_id,
                "session_id": record.session_id,
                "phase": record.phase,
                "effect_type": record.effect_type.value,
                "target": record.target,
                "details": record.details,
                "reversible": record.reversible,
                "rollback_action": record.rollback_action,
                "timestamp": record.timestamp,
            }, ensure_ascii=False) + "\n")

        logger.debug(f"[Effect:{record.effect_id}] {effect_type.value}: {target}")

    def log_file_write(self, session_id: str, phase: str, path: str, size: int = 0):
        self.log(
            session_id=session_id,
            phase=phase,
            effect_type=SideEffectType.FILE_WRITE,
            target=path,
            details={"size_bytes": size},
            rollback_action=f"delete:{path}",
        )

    def log_api_call(self, session_id: str, phase: str, endpoint: str, method: str = "GET"):
        self.log(
            session_id=session_id,
            phase=phase,
            effect_type=SideEffectType.API_CALL,
            target=endpoint,
            details={"method": method},
            reversible=False,  # API 调用默认不可逆
        )

    def log_state_change(self, session_id: str, phase: str, from_state: str, to_state: str):
        self.log(
            session_id=session_id,
            phase=phase,
            effect_type=SideEffectType.STATE_CHANGE,
            target=f"{from_state}→{to_state}",
            details={"from": from_state, "to": to_state},
            rollback_action=f"restore_state:{from_state}",
        )

    def get_session_effects(self, session_id: str) -> list[SideEffectRecord]:
        """获取某个会话的所有副作用记录"""
        with self._lock:
            return list(self._records.get(session_id, []))

    def get_rollback_plan(self, session_id: str) -> list[SideEffectRecord]:
        """获取回滚计划 — 逆序返回所有可逆操作"""
        effects = self.get_session_effects(session_id)
        return [e for e in reversed(effects) if e.reversible]

    def clear_session(self, session_id: str):
        """清除会话的副作用记录"""
        with self._lock:
            self._records.pop(session_id, None)
        log_path = self._get_log_path(session_id)
        if log_path.exists():
            log_path.unlink()

    def export_audit_trail(self, session_id: str) -> str:
        """导出审计轨迹为可读文本"""
        effects = self.get_session_effects(session_id)
        if not effects:
            return f"Session {session_id}: No side effects recorded."

        lines = [f"=== Side Effect Audit Trail: {session_id} ==="]
        for e in effects:
            reversible_mark = "↩" if e.reversible else "✗"
            lines.append(
                f"  [{e.phase}] {e.effect_type.value} {reversible_mark} {e.target}"
            )
        return "\n".join(lines)
