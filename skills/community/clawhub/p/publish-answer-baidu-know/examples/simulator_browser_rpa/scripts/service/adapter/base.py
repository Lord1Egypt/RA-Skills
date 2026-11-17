"""批量提交 adapter 基类与数据契约。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BatchItem:
    row_index: int
    name: str
    account: str
    amount: float
    note: str = ""


@dataclass
class BatchSubmitResult:
    ok: bool
    batch_id: Optional[str]
    submitted_count: int
    submitted_amount: float
    error_msg: Optional[str]
    artifacts: Dict[str, Any] = field(default_factory=dict)


class BatchAdapterBase:
    name: str = "base"

    async def submit_batch(self, target: str, items: List[BatchItem]) -> BatchSubmitResult:
        raise NotImplementedError
