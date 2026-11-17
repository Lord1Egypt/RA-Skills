"""mock / unit 档位：不启动浏览器。"""

from __future__ import annotations

import time
from typing import List

from service.adapter.base import BatchAdapterBase, BatchItem, BatchSubmitResult


class MockBatchAdapter(BatchAdapterBase):
    name = "mock"

    async def submit_batch(self, target: str, items: List[BatchItem]) -> BatchSubmitResult:
        del target
        if not items:
            return BatchSubmitResult(
                ok=False,
                batch_id=None,
                submitted_count=0,
                submitted_amount=0.0,
                error_msg="items 为空",
                artifacts={"adapter": self.name},
            )

        time.sleep(0.05)
        total = sum(it.amount for it in items)
        fake_batch_id = f"MOCK-{int(time.time())}"
        return BatchSubmitResult(
            ok=True,
            batch_id=fake_batch_id,
            submitted_count=len(items),
            submitted_amount=total,
            error_msg=None,
            artifacts={"adapter": self.name},
        )
