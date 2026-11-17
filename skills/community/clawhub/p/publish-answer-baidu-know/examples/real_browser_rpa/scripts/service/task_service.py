"""轻量任务编排示例（无真实数据库依赖）。"""

from __future__ import annotations

import asyncio
import uuid
from typing import Any, Optional

from service.account_client import AccountManagerError, pick_web_account, release_lease
from service.task_rpa import (
    ScrapeRunResult,
    format_stop_reason_for_user,
    run_keyword_search_async,
)
from util.constants import (
    DEFAULT_MAX_ITEMS,
    DEFAULT_MAX_SCROLLS,
    SKILL_SLUG,
    TARGET_PLATFORM,
)


def _error_payload(
    code: str,
    message: str,
    *,
    browser_started: Optional[bool] = None,
    stage: Optional[str] = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "success": False,
        "error": {"code": code, "message": message},
    }
    if browser_started is not None:
        payload["browser_started"] = browser_started
    if stage:
        payload["stage"] = stage
    return payload


def _success_payload(
    *,
    keyword: str,
    collected_count: int,
    items: list[dict[str, Any]],
    stop_reason: Optional[str],
) -> dict[str, Any]:
    return {
        "success": True,
        "skill": SKILL_SLUG,
        "keyword": keyword,
        "collected_count": collected_count,
        "items": items,
        "stop_reason": stop_reason,
        "stop_reason_message": format_stop_reason_for_user(stop_reason, collected_count),
    }


async def run_keyword_search_task(
    keyword: str,
    *,
    max_items: int = DEFAULT_MAX_ITEMS,
    max_scrolls: int = DEFAULT_MAX_SCROLLS,
    account_id: Optional[str] = None,
    platform: str = TARGET_PLATFORM,
) -> dict[str, Any]:
    """
    编排一次关键词搜索采集。

    真实 skill 中还应：
    - 写 SQLite 入库（items 表）
    - 写 scrape_tasks / task_logs 任务日志
    - 使用 RpaVideoSession 录制步骤留痕
    - 失败时 capture_failure 截图
    """
    batch_id = uuid.uuid4().hex[:12]
    data_dir = ""  # 示例占位；真实 skill 使用 get_skill_data_dir()
    lease_token: Optional[str] = None
    account: Optional[dict[str, Any]] = None

    try:
        account = pick_web_account(platform, account_id)
        lease_token = account.get("lease_token")

        scrape_result: ScrapeRunResult = await run_keyword_search_async(
            account,
            keyword,
            max_items=max_items,
            max_scrolls=max_scrolls,
            data_dir=data_dir,
            batch_id=batch_id,
        )

        if not scrape_result.success:
            err = scrape_result.error
            return _error_payload(
                err.code if err else "UNKNOWN_ERROR",
                err.message if err else "未知错误",
                browser_started=err.browser_started if err else True,
                stage=err.stage if err else "rpa",
            )

        collected_count = len(scrape_result.items)
        return _success_payload(
            keyword=keyword,
            collected_count=collected_count,
            items=scrape_result.items[:10],
            stop_reason=scrape_result.stop_reason,
        )
    except AccountManagerError as exc:
        return _error_payload(
            exc.code,
            exc.message,
            browser_started=False,
            stage="account_prepare",
        )
    finally:
        release_lease(lease_token)


def run_keyword_search_task_sync(
    keyword: str,
    *,
    max_items: int = DEFAULT_MAX_ITEMS,
    max_scrolls: int = DEFAULT_MAX_SCROLLS,
    account_id: Optional[str] = None,
    platform: str = TARGET_PLATFORM,
) -> dict[str, Any]:
    return asyncio.run(
        run_keyword_search_task(
            keyword,
            max_items=max_items,
            max_scrolls=max_scrolls,
            account_id=account_id,
            platform=platform,
        )
    )
