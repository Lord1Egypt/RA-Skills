"""零稀泥模式 — Checkpoint 持久化管理器 checkpoint_manager.py

从 Pipeline 抽取的独立 checkpoint 管理，提供原子读写和自动裁剪。

Usage:
    from .checkpoint_manager import CheckpointManager
    ckm = CheckpointManager(state_path)
    ckm.save(bug_id, "phase1", {"regr_pass": 5})
    ckm.save(bug_id, "phase2", CheckpointData(phase="phase2", data={...}))
"""

import logging
from datetime import datetime
from typing import Optional, Union

from .config import TZ
from . import state_manager as sm

log = logging.getLogger("checkpoint")

_MAX_CHECKPOINTS = 50


class CheckpointManager:
    """独立的 checkpoint 持久化管理器

    从 Pipeline._save_checkpoint() 抽取，职责单一。
    使用文件锁保证并发安全。
    """

    def __init__(self, state_path: str):
        self.state_path = state_path or sm.locate()

    def save(self, bug_id: str, phase: str, data: Union[dict, "CheckpointData"]):
        """保存阶段 checkpoint 到 state 文件（原子写 + 文件锁）

        Args:
            bug_id: Bug 唯一 ID
            phase: 阶段名 (phase0-4)
            data: 阶段数据（dict 或 CheckpointData Pydantic 模型）
        """
        # 如果是 CheckpointData Pydantic 模型，取 data 字段
        if hasattr(data, "model_dump") and hasattr(data, "data"):
            data = data.data

        fp = self.state_path
        lock_held = sm.acquire_lock(fp)
        try:
            state = sm.read(fp)
            state.setdefault("_pipeline_checkpoints", {})
            state["_pipeline_checkpoints"].setdefault(bug_id, {})
            state["_pipeline_checkpoints"][bug_id][phase] = data
            state["_pipeline_checkpoints"][bug_id]["updated_at"] = \
                datetime.now(TZ).isoformat()

            # 自动裁剪：只保留最近 _MAX_CHECKPOINTS 条
            ckpts = state["_pipeline_checkpoints"]
            if len(ckpts) > _MAX_CHECKPOINTS:
                sorted_ids = sorted(
                    ckpts.keys(),
                    key=lambda k: ckpts[k].get("updated_at", ""),
                    reverse=True,
                )
                for stale_id in sorted_ids[_MAX_CHECKPOINTS:]:
                    del ckpts[stale_id]
                log.info("checkpoint 裁剪: 从 %d 缩至 %d",
                         len(sorted_ids), _MAX_CHECKPOINTS)

            sm.write(state, fp)
            log.debug("checkpoint 已保存: bug_id=%s phase=%s", bug_id, phase)
        except Exception as e:
            log.error("checkpoint 写入失败: %s", e)
            raise
        finally:
            if lock_held:
                sm.release_lock(fp)

    def get(self, bug_id: str) -> dict:
        """获取指定 bug_id 的 checkpoint 快照"""
        state = sm.read(self.state_path)
        return state.get("_pipeline_checkpoints", {}).get(bug_id, {})

    def has(self, bug_id: str, phase: str) -> bool:
        """检查指定 phase 是否已完成"""
        cp = self.get(bug_id)
        return phase in cp
