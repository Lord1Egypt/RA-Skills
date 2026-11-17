"""仿真浏览器 RPA 薄 adapter：pick 账号、lease、委托 RPA、release lease。"""

from __future__ import annotations

import logging
from typing import List, Optional

from jiangchang_skill_core import config

from service.account_client import AccountManagerError, pick_web_account, release_lease
from service.adapter.base import BatchAdapterBase, BatchItem, BatchSubmitResult
from service.browser_session import find_chrome_executable
from service.simulator_playwright import submit_batch_rpa
from util.constants import TARGET_PLATFORM, resolve_simulator_base_url

logger = logging.getLogger(__name__)


def _resolve_entry_url(account: dict) -> str:
    url = str(account.get("url") or "").strip()
    if url:
        return url.rstrip("/")
    return resolve_simulator_base_url()


class SimulatorBrowserRpaAdapter(BatchAdapterBase):
    name = "simulator_rpa"

    def __init__(
        self,
        artifacts_dir: Optional[str] = None,
        headless: Optional[bool] = None,
    ) -> None:
        self.artifacts_dir = artifacts_dir
        if headless is None:
            self.headless = config.get_bool("OPENCLAW_BROWSER_HEADLESS", default=False)
        else:
            self.headless = headless

    async def submit_batch(self, target: str, items: List[BatchItem]) -> BatchSubmitResult:
        try:
            from playwright.async_api import async_playwright  # noqa: F401
        except ImportError:
            return BatchSubmitResult(
                ok=False,
                batch_id=None,
                submitted_count=0,
                submitted_amount=0.0,
                error_msg=(
                    "playwright Python 包不可用。"
                    "生产/宿主运行由共享 runtime 提供；技能侧不要 pip install playwright。"
                ),
                artifacts={"adapter": self.name},
            )

        if not items:
            return BatchSubmitResult(
                ok=False,
                batch_id=None,
                submitted_count=0,
                submitted_amount=0.0,
                error_msg="items 为空",
                artifacts={"adapter": self.name},
            )

        if not find_chrome_executable():
            return BatchSubmitResult(
                ok=False,
                batch_id=None,
                submitted_count=0,
                submitted_amount=0.0,
                error_msg="未检测到 Chrome 或 Edge 浏览器，请安装系统浏览器后重试。",
                artifacts={"adapter": self.name},
            )

        lease_token: Optional[str] = None
        try:
            account = pick_web_account(TARGET_PLATFORM)
            lease_token = account.get("lease_token")
            base_url = _resolve_entry_url(account)
            return await submit_batch_rpa(
                account,
                target=target,
                items=items,
                base_url=base_url,
                artifacts_dir=self.artifacts_dir,
                headless=self.headless,
            )
        except AccountManagerError as exc:
            return BatchSubmitResult(
                ok=False,
                batch_id=None,
                submitted_count=0,
                submitted_amount=0.0,
                error_msg=f"ERROR:{exc.code} {exc.message}",
                artifacts={"adapter": self.name},
            )
        except Exception as exc:
            logger.exception("adapter_unexpected: %s", exc)
            return BatchSubmitResult(
                ok=False,
                batch_id=None,
                submitted_count=0,
                submitted_amount=0.0,
                error_msg=f"未预期异常：{type(exc).__name__}: {exc}",
                artifacts={"adapter": self.name},
            )
        finally:
            release_lease(lease_token)
