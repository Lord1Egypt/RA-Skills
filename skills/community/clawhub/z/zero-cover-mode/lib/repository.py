"""零稀泥模式 — 持久化层 (repository.py)

封装所有 ndjson + state 读写。
提供:
- 事务性双写（ndjson + state 原子化）
- 安全轮转（带备份）
- 完整性校验
- 自动恢复

实现架构审查 7.3 的 Unit of Work 升级方案。
"""

import os, logging
from typing import Optional

from .config import DEFAULT_STATE_PATH, DEFAULT_NDJSON_PATH
from . import file_ops as _fo
from . import uow as _uow
from .contracts import FixRecord

log = logging.getLogger("repository")


class FixRepository:
    """修复记录持久化仓库

    提供 ndjson 和 state 的事务性双写。
    所有写入操作通过 UnitOfWork 保证原子性。

    架构位置: Layer 3 (持久化层)
    """

    def __init__(self, state_path: str = ""):
        from . import state_manager as _sm
        self.state_path = state_path or _sm.locate()
        self.ndjson_path = os.path.join(
            os.path.dirname(self.state_path), DEFAULT_NDJSON_PATH
        )
        self._state = None

    # ── 状态路径 ──

    def get_state_path(self) -> str:
        return self.state_path

    def get_ndjson_path(self) -> str:
        return self.ndjson_path

    # ── 原子保存（事务性） ──

    def save_fix(self, record: FixRecord, uow: Optional[_uow.UnitOfWork] = None) -> dict:
        """原子保存修复记录（ndjson + state）

        返回包含 success, bug_id, existed 的 dict。
        """
        from .persistence_facade import PersistenceFacade
        facade = PersistenceFacade(self.state_path)
        return facade.save_fix(record.model_dump(), uow)

    # ── 批量保存 ──

    def save_fix_batch(self, records: list[FixRecord]) -> list[dict]:
        """批量保存多个修复记录（共享同一个事务）"""
        with _uow.UnitOfWork() as uow:
            results = []
            for record in records:
                result = self.save_fix(record, uow)
                results.append(result)
                if not result.get("success"):
                    uow.rollback()
                    return results
            uow.commit()
        return results

    # ── 验证与恢复 ──

    def verify_integrity(self) -> dict:
        """验证 ndjson 与 state 的一致性"""
        from . import state_manager as _sm
        issues = []

        if not os.path.exists(self.ndjson_path):
            return {"ok": True, "issues": [], "note": "ndjson 不存在（首次运行）"}

        # 计算 ndjson 行数
        ndjson_count = 0
        with open(self.ndjson_path, "r", encoding="utf-8-sig", errors="replace") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    try:
                        json.loads(stripped)
                        ndjson_count += 1
                    except json.JSONDecodeError:
                        issues.append(f"ndjson 第 {ndjson_count + 1} 行 JSON 损坏")

        # 读出 state 的计数
        state = _sm.read(self.state_path)
        state_count = state.get("ndjson_line_count", 0)

        if ndjson_count != state_count:
            issues.append(
                f"计数不一致: ndjson={ndjson_count}, state={state_count}"
            )

        return {
            "ok": len(issues) == 0,
            "issues": issues,
            "ndjson_count": ndjson_count,
            "state_count": state_count,
        }

    def auto_repair(self) -> bool:
        """检测不一致时自动恢复"""
        integrity = self.verify_integrity()
        if integrity["ok"]:
            return True

        log.warning("检测到不一致，尝试自动恢复: %s", integrity["issues"])
        from . import state_manager as _sm

        # 从 ndjson 重建 state 的可计算字段
        lock_held = _fo.acquire_file_lock(self.state_path)
        try:
            state = _sm.read(self.state_path)
            _sm._rebuild_from_ndjson(state, self.state_path)
            _sm.write(state, self.state_path)
            log.info("自动恢复完成: ndjson 重建 state")
            return True
        except Exception as e:
            log.error("自动恢复失败: %s", e)
            return False
        finally:
            if lock_held:
                _fo.release_file_lock(self.state_path)
