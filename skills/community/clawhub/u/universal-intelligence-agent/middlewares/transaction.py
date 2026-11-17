"""
两阶段提交事务管理 (2PC)
─────────────────────────
原设计回滚只回滚当前阶段，跨阶段副作用（已写盘文件、已调用API）
无法撤销。现在改为两阶段提交：

Phase 1 (Prepare): 所有副作用操作先写入缓冲区/先不落盘
Phase 2 (Commit):  全部 Prepare 成功 → 统一落盘
Phase 2 (Rollback): 任何一个 Prepare 失败 → 逆序执行回滚动作
"""
from __future__ import annotations

import json
import logging
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


# ── WAL 日志条目 ────────────────────────────────────────────

@dataclass
class WALEntry:
    """Write-Ahead Log 条目"""
    session_id: str
    phase: str
    action: str
    status: str  # "prepared" | "committed" | "rolled_back"
    details: str
    timestamp: float = field(default_factory=__import__("time").time)


class WALLogger:
    """WAL 日志管理器 — 用于跨会话恢复"""

    def __init__(self, wal_dir: Optional[Path] = None):
        from pathlib import Path as _Path
        import os as _os
        self.wal_dir = wal_dir or _Path(_os.path.expanduser("~")) / ".uia" / "wal"
        self.wal_dir.mkdir(parents=True, exist_ok=True)

    def write(self, entry: WALEntry):
        wal_file = self.wal_dir / f"{entry.session_id}.wal"
        with open(wal_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "session_id": entry.session_id,
                "phase": entry.phase,
                "action": entry.action,
                "status": entry.status,
                "details": entry.details,
                "timestamp": entry.timestamp,
            }, ensure_ascii=False) + "\n")

    def read(self, session_id: str) -> list[WALEntry]:
        wal_file = self.wal_dir / f"{session_id}.wal"
        if not wal_file.exists():
            return []
        entries = []
        with open(wal_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    data = json.loads(line)
                    entries.append(WALEntry(
                        session_id=data["session_id"],
                        phase=data["phase"],
                        action=data["action"],
                        status=data["status"],
                        details=data["details"],
                        timestamp=data["timestamp"],
                    ))
        return entries

    def get_last_phase(self, session_id: str) -> Optional[str]:
        """获取上次中断的阶段，用于跨会话恢复"""
        entries = self.read(session_id)
        if not entries:
            return None
        # 找到最后一个 committed 的阶段
        committed = [e for e in entries if e.status == "committed"]
        if committed:
            return committed[-1].phase
        return None

    def clear(self, session_id: str):
        wal_file = self.wal_dir / f"{session_id}.wal"
        if wal_file.exists():
            wal_file.unlink()


# ── 两阶段提交 UnitOfWork ────────────────────────────────────

class TransactionError(Exception):
    """事务执行失败"""
    pass


class UnitOfWork:
    """
    工作单元 — 两阶段提交

    用法:
        uow = UnitOfWork(session_id="abc123")

        # 注册副作用操作
        uow.register_write(
            path="/tmp/report.md",
            content=b"# Report",
            rollback=lambda: os.remove("/tmp/report.md"),
        )
        uow.register_api_call(
            call=lambda: api.send(data),
            rollback=lambda: api.delete(msg_id),
        )

        # 两阶段提交
        try:
            uow.commit()
        except TransactionError:
            uow.rollback()
    """

    def __init__(self, session_id: str, wal_logger: Optional[WALLogger] = None):
        self.session_id = session_id
        self.wal = wal_logger or WALLogger()
        self._pending_writes: list[tuple[Path, bytes, Callable[[], None]]] = []
        self._pending_api_calls: list[tuple[Callable, Callable]] = []
        self._committed: bool = False
        self._rolled_back: bool = False

        # 使用临时目录做原子写入缓冲
        self._temp_dir = Path(tempfile.mkdtemp(prefix=f"uow_{session_id}_"))

    def register_write(
        self,
        path: Path | str,
        content: bytes,
        rollback: Callable[[], None],
    ):
        """
        注册文件写入 — 先写入临时缓冲区，commit 时才原子移动到目标路径

        Args:
            path: 目标文件路径
            content: 要写入的内容
            rollback: 回滚函数（如果 commit 后需要回滚）
        """
        path = Path(path) if not isinstance(path, Path) else path
        # 写入临时缓冲区
        temp_path = self._temp_dir / path.name
        temp_path.write_bytes(content)
        self._pending_writes.append((path, content, rollback))
        logger.debug(f"[UOW:{self.session_id}] Registered write: {path}")

    def register_api_call(
        self,
        call: Callable,
        rollback: Callable[[], None],
    ):
        """
        注册 API 调用 — Prepare 阶段执行，失败时调用 rollback

        Args:
            call: 实际的 API 调用函数
            rollback: 撤销该 API 调用的函数
        """
        self._pending_api_calls.append((call, rollback))
        logger.debug(f"[UOW:{self.session_id}] Registered API call")

    def commit(self):
        """
        两阶段提交:
        Phase 1 (Prepare): 执行所有 API 调用
        Phase 2 (Commit):  将所有缓冲写入原子移动到目标路径
        """
        if self._committed or self._rolled_back:
            raise TransactionError("UnitOfWork already finalized")

        # Phase 1: Prepare — 执行 API 调用
        self.wal.write(WALEntry(
            session_id=self.session_id,
            phase="transaction",
            action="prepare",
            status="preparing",
            details=f"Preparing {len(self._pending_api_calls)} API calls, {len(self._pending_writes)} writes",
        ))

        executed_calls = []
        for i, (call, rollback) in enumerate(self._pending_api_calls):
            try:
                result = call()
                executed_calls.append((call, rollback, result))
                self.wal.write(WALEntry(
                    session_id=self.session_id,
                    phase="transaction",
                    action="api_call",
                    status="prepared",
                    details=f"API call #{i} prepared",
                ))
            except Exception as e:
                logger.error(f"[UOW:{self.session_id}] API call #{i} failed: {e}")
                # Prepare 阶段失败 → 回滚已执行的 API 调用
                for _, rb, _ in reversed(executed_calls):
                    try:
                        rb()
                    except Exception as rb_e:
                        logger.error(f"Rollback failed: {rb_e}")
                self.rollback()
                raise TransactionError(f"Prepare phase failed at API call #{i}: {e}")

        # Phase 2: Commit — 原子移动文件
        self.wal.write(WALEntry(
            session_id=self.session_id,
            phase="transaction",
            action="commit",
            status="committing",
            details=f"Committing {len(self._pending_writes)} writes",
        ))

        moved_files = []
        for path, content, rollback in self._pending_writes:
            try:
                # 确保父目录存在
                path.parent.mkdir(parents=True, exist_ok=True)
                # 从临时缓冲区移动到目标
                temp_path = self._temp_dir / path.name
                shutil.move(str(temp_path), str(path))
                moved_files.append((path, rollback))
            except Exception as e:
                logger.error(f"[UOW:{self.session_id}] Write to {path} failed: {e}")
                # Commit 阶段文件写入失败 → 回滚已移动的文件
                for moved_path, rb in reversed(moved_files):
                    try:
                        rb()
                    except Exception:
                        pass
                # 回滚 API 调用
                for _, rb, _ in reversed(executed_calls):
                    try:
                        rb()
                    except Exception:
                        pass
                self.rollback()
                raise TransactionError(f"Commit phase failed at {path}: {e}")

        self._committed = True

        # Phase 4.1: 成功后清理临时目录
        self._cleanup_temp_dir()

        self.wal.write(WALEntry(
            session_id=self.session_id,
            phase="transaction",
            action="commit",
            status="committed",
            details="All operations committed successfully",
        ))
        logger.info(f"[UOW:{self.session_id}] Transaction committed: "
                     f"{len(executed_calls)} API calls, {len(moved_files)} writes")

    def rollback(self):
        """
        回滚所有操作 — 逆序执行回滚函数
        这是最佳努力回滚，单个回滚失败不影响其他回滚继续执行
        """
        if self._rolled_back:
            return

        self.wal.write(WALEntry(
            session_id=self.session_id,
            phase="transaction",
            action="rollback",
            status="rolled_back",
            details="Rollback initiated",
        ))

        # 逆序回滚所有注册的副作用
        all_rollbacks = (
            [rb for _, _, rb in self._pending_writes] +
            [rb for _, rb in self._pending_api_calls]
        )

        for rb in reversed(all_rollbacks):
            try:
                rb()
            except Exception as e:
                logger.error(f"[UOW:{self.session_id}] Rollback action failed: {e}")

        self._rolled_back = True

        # 清理临时目录
        self._cleanup_temp_dir()

        logger.info(f"[UOW:{self.session_id}] Rollback complete")

    def _cleanup_temp_dir(self):
        """清理临时缓冲区目录"""
        try:
            if hasattr(self, '_temp_dir') and self._temp_dir.exists():
                shutil.rmtree(str(self._temp_dir), ignore_errors=True)
        except Exception as e:
            logger.warning(f"[UOW:{self.session_id}] Temp dir cleanup failed: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            try:
                self.commit()
            except TransactionError:
                self.rollback()
                raise
        return False  # 不抑制异常
