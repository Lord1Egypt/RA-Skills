#!/usr/bin/env python3
"""
ultra-memory: LangGraph Checkpointer 集成
提供 UltraMemoryCheckpointer 类，作为 LangGraph 的状态持久化后端。

用法:
    from integrations.langgraph_checkpointer import UltraMemoryCheckpointer
    checkpointer = UltraMemoryCheckpointer(session_id="sess_langgraph_proj")
    compiled = graph.compile(checkpointer=checkpointer)
"""

import json
import os
from pathlib import Path
from typing import Any, Optional

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))


class UltraMemoryCheckpointer:
    """
    LangGraph checkpointer backed by ultra-memory。
    在每个节点执行后保存/恢复 agent graph 状态。
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.checkpoint_dir = ULTRA_MEMORY_HOME / "sessions" / session_id / "checkpoints"
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def _checkpoint_file(self, thread_id: str, step: int) -> Path:
        """获取检查点文件路径"""
        return self.checkpoint_dir / f"thread_{thread_id}_step_{step:04d}.json"

    def get(self, thread_id: str, step: int) -> Optional[dict[str, Any]]:
        """获取指定 thread 和 step 的检查点状态"""
        checkpoint_file = self._checkpoint_file(thread_id, step)
        if not checkpoint_file.exists():
            return None
        try:
            with open(checkpoint_file, encoding="utf-8") as f:
                data = json.load(f)
            return data.get("state")
        except (json.JSONDecodeError, IOError):
            return None

    def put(self, thread_id: str, step: int, state: dict[str, Any]) -> None:
        """保存检查点状态"""
        checkpoint_file = self._checkpoint_file(thread_id, step)
        data = {
            "step": step,
            "state": state,
            "session_id": self.session_id,
            "thread_id": thread_id,
        }
        with open(checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_latest(self, thread_id: str) -> Optional[dict[str, Any]]:
        """获取指定 thread 的最新检查点"""
        checkpoints = sorted(
            self.checkpoint_dir.glob(f"thread_{thread_id}_step_*.json"),
            key=lambda p: int(p.stem.split("_")[-1]),
        )
        if not checkpoints:
            return None
        return self.get(thread_id, int(checkpoints[-1].stem.split("_")[-1]))

    def list_threads(self) -> list[str]:
        """列出所有已有 thread ID"""
        threads = set()
        for f in self.checkpoint_dir.glob("thread_*_step_*.json"):
            parts = f.stem.split("_")
            if len(parts) >= 2:
                threads.add(parts[1])
        return sorted(threads)
