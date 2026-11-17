"""
回滚协调器 — 统一回滚管理 + UoW 互斥检查
────────────────────────────────────────
从 PipelineCoordinator 拆分出的独立模块。
协调 _rollback() 与 UnitOfWork.__exit__() 的关系，避免双重回滚。
"""
from __future__ import annotations

import logging
from pathlib import Path

from middlewares.side_effect_log import SideEffectLogger, SideEffectType

logger = logging.getLogger(__name__)


class RollbackCoordinator:
    """回滚协调器 — 统一管理全局回滚

    与 UnitOfWork 的 __exit__ 互斥：跳过 reporting 阶段的副作用
    （由 UoW 管理），只处理其他阶段的 FILE_WRITE 副作用。

    用法:
        coordinator = RollbackCoordinator()
        coordinator.rollback(session_id="abc", side_effect_logger=logger)
    """

    def rollback(self, session_id: str, side_effect_logger: SideEffectLogger):
        """执行全局回滚 — 仅处理 UoW 之外的副作用"""
        logger.warning(f"[Rollback:{session_id}] Initiating global rollback")

        rollback_plan = side_effect_logger.get_rollback_plan(session_id)

        rolled_back = 0
        skipped = 0
        for record in rollback_plan:
            # 跳过 reporting 阶段的副作用（UoW 的 __exit__ 已处理）
            if record.phase == "reporting":
                skipped += 1
                continue

            try:
                if record.effect_type == SideEffectType.FILE_WRITE:
                    if record.rollback_action and record.rollback_action.startswith("delete:"):
                        file_path = record.rollback_action.split(":", 1)[1]
                        p = Path(file_path)
                        if p.exists():
                            p.unlink()
                            rolled_back += 1
                            logger.info(f"[Rollback:{session_id}] Deleted: {file_path}")
                elif record.effect_type == SideEffectType.API_CALL:
                    # API 调用默认不可逆，只记录
                    logger.warning(
                        f"[Rollback:{session_id}] API call to {record.target} is irreversible"
                    )
            except Exception as e:
                logger.error(f"[Rollback:{session_id}] Failed for {record.effect_id}: {e}")

        logger.info(
            f"[Rollback:{session_id}] Complete: {rolled_back} files rolled back, "
            f"{skipped} UoW-managed effects skipped"
        )
