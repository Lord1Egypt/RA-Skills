"""adapter 工厂：按 OPENCLAW_TEST_TARGET 选择实现。"""

from __future__ import annotations

import logging
from typing import Optional

from jiangchang_skill_core import config

from service.adapter.base import BatchAdapterBase, BatchItem, BatchSubmitResult
from service.adapter.mock import MockBatchAdapter
from service.adapter.simulator_rpa import SimulatorBrowserRpaAdapter

logger = logging.getLogger(__name__)

__all__ = [
    "select_adapter",
    "BatchAdapterBase",
    "BatchItem",
    "BatchSubmitResult",
    "MockBatchAdapter",
    "SimulatorBrowserRpaAdapter",
]


def select_adapter(artifacts_dir: Optional[str] = None) -> BatchAdapterBase:
    target = (config.get("OPENCLAW_TEST_TARGET") or "").strip().lower()

    if target in ("mock", "unit"):
        logger.info("target '%s': MockBatchAdapter", target)
        return MockBatchAdapter()

    if target == "real_rpa":
        logger.warning("target real_rpa 未实现，回退 MockBatchAdapter")
        return MockBatchAdapter()

    if target and target != "simulator_rpa":
        logger.warning("未知 target '%s'，回退 simulator_rpa", target)

    logger.info("target '%s': SimulatorBrowserRpaAdapter", target or "(unset=default)")
    return SimulatorBrowserRpaAdapter(artifacts_dir=artifacts_dir)
