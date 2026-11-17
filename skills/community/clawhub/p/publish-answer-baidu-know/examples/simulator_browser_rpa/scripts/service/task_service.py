"""轻量任务编排：校验输入 → 选 adapter → 提交批次。"""

from __future__ import annotations

import os
import tempfile
import uuid
from typing import Any, Dict, List, Optional

from service.adapter import BatchItem, select_adapter
from util.logging import get_logger

logger = get_logger(__name__)


def _validate_items(items: List[Dict[str, Any]]) -> tuple[List[BatchItem], Optional[str]]:
    if not items:
        return [], "items 不能为空"
    parsed: List[BatchItem] = []
    for idx, raw in enumerate(items, start=1):
        name = str(raw.get("name") or "").strip()
        account = str(raw.get("account") or "").strip()
        note = str(raw.get("note") or "").strip()
        try:
            amount = float(raw.get("amount"))
        except (TypeError, ValueError):
            return [], f"第 {idx} 行 amount 无效"
        if amount <= 0:
            return [], f"第 {idx} 行 amount 必须大于 0"
        if not name or not account:
            return [], f"第 {idx} 行 name/account 不能为空"
        parsed.append(
            BatchItem(
                row_index=int(raw.get("row_index") or idx),
                name=name,
                account=account,
                amount=amount,
                note=note,
            )
        )
    return parsed, None


async def run_batch_submit(
    target: str,
    items: List[Dict[str, Any]],
    *,
    force: bool = False,
    artifacts_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    最小编排示例。

    真实 skill 中还应：写 task_logs、entitlement、RpaVideoSession 等。
    账号 pick / lease 在 adapter 内完成，编排层不直接碰 account-manager。
    """
    del force  # 示例占位；真实 skill 可用于跳过确认

    target_key = (target or "").strip()
    if not target_key:
        return {"success": False, "error": {"code": "INVALID_TARGET", "message": "target 不能为空"}}

    batch_items, err = _validate_items(items)
    if err:
        return {"success": False, "error": {"code": "INVALID_ITEMS", "message": err}}

    art_dir = artifacts_dir or os.path.join(
        tempfile.gettempdir(),
        "openclaw-simulator-rpa-artifacts",
        uuid.uuid4().hex[:8],
    )
    os.makedirs(art_dir, exist_ok=True)
    logger.info(
        "batch_submit_start target=%s item_count=%s artifacts_dir=%s",
        target_key,
        len(batch_items),
        art_dir,
    )

    adapter = select_adapter(artifacts_dir=art_dir)
    result = await adapter.submit_batch(target_key, batch_items)
    summary: Dict[str, Any] = {
        "success": result.ok,
        "target": target_key,
        "adapter": result.artifacts.get("adapter") or adapter.name,
        "submitted_count": result.submitted_count,
        "submitted_amount": result.submitted_amount,
        "batch_id": result.batch_id,
        "artifacts": result.artifacts,
        "artifacts_dir": art_dir,
    }
    if not result.ok:
        summary["error"] = {"code": "BATCH_SUBMIT_FAILED", "message": result.error_msg or "提交失败"}
    logger.info(
        "batch_submit_done success=%s batch_id=%s adapter=%s",
        result.ok,
        result.batch_id,
        adapter.name,
    )
    return summary
