"""仿真批量提交 RPA 主流程（async Playwright）。"""

from __future__ import annotations

import asyncio
import logging
import os
import random
import re
import time
from dataclasses import dataclass
from typing import Any, List, Optional

from jiangchang_skill_core import config

from service.adapter.base import BatchItem, BatchSubmitResult
from service.browser_session import (
    close_browser_session,
    find_chrome_executable,
    start_browser_session,
)
from util.constants import (
    DEFAULT_DEMO_CAPTCHA,
    DEFAULT_DEMO_LOGIN_ID,
    DEFAULT_DEMO_PASSWORD,
    DEFAULT_DEMO_TOKEN_PIN,
    DEFAULT_TIMEOUT_MS,
    ENV_SIMULATOR_PASSWORD,
    ENV_SIMULATOR_TOKEN_PIN,
    LOGIN_NAVIGATE_TIMEOUT_MS,
    SUBMIT_NAVIGATE_TIMEOUT_MS,
    portal_login_wait_sec,
)

logger = logging.getLogger(__name__)

GOTO_TIMEOUT_MS = 60_000

_PAUSE_MIN_MS = 500
_PAUSE_MAX_MS = 2000


class RpaError(Exception):
    def __init__(self, message: str, screenshot_path: Optional[str] = None):
        super().__init__(message)
        self.screenshot_path = screenshot_path


@dataclass
class _Credentials:
    login_id: str
    password: str
    token_pin: str


def _resolve_credentials(account: dict[str, Any]) -> _Credentials:
    login_id = str(
        account.get("login_id") or account.get("username") or DEFAULT_DEMO_LOGIN_ID
    ).strip()
    password = str(
        account.get("password")
        or os.getenv(ENV_SIMULATOR_PASSWORD)
        or config.get(ENV_SIMULATOR_PASSWORD)
        or DEFAULT_DEMO_PASSWORD
    ).strip()
    token_pin = str(
        account.get("token_pin")
        or account.get("pin")
        or os.getenv(ENV_SIMULATOR_TOKEN_PIN)
        or config.get(ENV_SIMULATOR_TOKEN_PIN)
        or DEFAULT_DEMO_TOKEN_PIN
    ).strip()
    return _Credentials(login_id=login_id, password=password, token_pin=token_pin)


def _headless() -> bool:
    return config.get_bool("OPENCLAW_BROWSER_HEADLESS", default=False)


async def _pause(min_ms: int = _PAUSE_MIN_MS, max_ms: int = _PAUSE_MAX_MS) -> None:
    await asyncio.sleep(random.uniform(min_ms, max_ms) / 1000.0)


async def _visible(locator) -> bool:
    try:
        return await locator.count() > 0 and await locator.is_visible(timeout=500)
    except Exception:
        return False


async def _wait_portal_gate(page, wait_sec: int) -> None:
    portal_user = page.locator("#portal-user")
    try:
        if not await _visible(portal_user):
            return
    except Exception:
        return

    print(f"[门户] 检测到平台门户登录门闩，请手工完成门户登录，最多等待 {wait_sec} 秒...")
    deadline = time.monotonic() + wait_sec
    while time.monotonic() < deadline:
        try:
            portal_section = page.locator("#portal-section")
            login_step1 = page.locator('form[name="simLoginStep1"]')
            if not await _visible(portal_section) or await _visible(login_step1):
                print("[门户] 门户门闩已通过，进入业务系统登录")
                return
        except Exception:
            pass
        await asyncio.sleep(2.0)

    raise RpaError("ERROR:LOGIN_TIMEOUT 门户登录超时，请重新运行并及时完成门户登录。")


async def _login(page, creds: _Credentials, artifacts_dir: str | None) -> None:
    try:
        await page.wait_for_selector(
            'form[name="simLoginStep1"]', timeout=LOGIN_NAVIGATE_TIMEOUT_MS
        )
        await _pause()
        await page.fill('form[name="simLoginStep1"] input[name="loginId"]', creds.login_id)
        await _pause()
        await page.click('form[name="simLoginStep1"] button[type="submit"]')
    except Exception as exc:
        sp = await _safe_screenshot(page, artifacts_dir, "login_step1_failed")
        raise RpaError(f"登录第一步失败：{exc}", screenshot_path=sp) from exc

    try:
        await page.wait_for_selector('form[name="simLoginStep2"]', timeout=DEFAULT_TIMEOUT_MS)
        await _pause()
        await page.fill('form[name="simLoginStep2"] input[name="password"]', creds.password)
        await page.fill('form[name="simLoginStep2"] input[name="captcha"]', DEFAULT_DEMO_CAPTCHA)
        await _pause()
        await page.click('form[name="simLoginStep2"] button[type="submit"]')
    except Exception as exc:
        sp = await _safe_screenshot(page, artifacts_dir, "login_step2_failed")
        raise RpaError(f"登录第二步失败：{exc}", screenshot_path=sp) from exc

    try:
        await page.wait_for_selector('form[name="simBatchForm"]', timeout=LOGIN_NAVIGATE_TIMEOUT_MS)
    except Exception as exc:
        sp = await _safe_screenshot(page, artifacts_dir, "login_navigate_failed")
        raise RpaError(f"登录后未进入批量提交页：{exc}", screenshot_path=sp) from exc


async def _goto_batch_page(page, artifacts_dir: str | None) -> None:
    try:
        await page.wait_for_selector('form[name="simBatchForm"]', timeout=DEFAULT_TIMEOUT_MS)
        await _pause()
    except Exception as exc:
        sp = await _safe_screenshot(page, artifacts_dir, "goto_batch_failed")
        raise RpaError(f"进入批量提交页失败：{exc}", screenshot_path=sp) from exc


async def _select_target_account(page, target: str) -> None:
    sel = page.locator('select[name="fromAccountNo"]')
    await sel.wait_for(timeout=DEFAULT_TIMEOUT_MS)
    n = await sel.locator("option").count()
    matched_value: Optional[str] = None
    first_value: Optional[str] = None
    for i in range(n):
        opt = sel.locator("option").nth(i)
        val = (await opt.get_attribute("value")) or ""
        if not val.strip():
            continue
        label_txt = await opt.inner_text()
        if first_value is None:
            first_value = val
        if target.strip() and target.strip() in label_txt:
            matched_value = val
            break
    pick = matched_value or first_value
    if not pick:
        raise RpaError("来源账户下拉无可选项")
    if not matched_value and target.strip():
        logger.warning("target '%s' 未匹配选项，回退 value=%s", target, pick)
    await sel.select_option(value=pick)
    await _pause()


async def _fill_batch_form(
    page, target: str, items: List[BatchItem], artifacts_dir: str | None
) -> None:
    try:
        await page.get_by_role("button", name=re.compile(r"页面填写")).click()
    except Exception as exc:
        sp = await _safe_screenshot(page, artifacts_dir, "tab_switch_failed")
        raise RpaError(f"切换到页面填写失败：{exc}", screenshot_path=sp) from exc

    try:
        await _select_target_account(page, target)
    except RpaError:
        raise
    except Exception as exc:
        sp = await _safe_screenshot(page, artifacts_dir, "select_account_failed")
        raise RpaError(f"选择来源账户失败：{exc}", screenshot_path=sp) from exc

    try:
        existing = await page.locator("tr[data-row-index]").count()
        need_more = max(0, len(items) - existing)
        add_btn = page.get_by_role("button", name=re.compile(r"新增一行"))
        for _ in range(need_more):
            await _pause(400, 900)
            await add_btn.click()
    except Exception as exc:
        sp = await _safe_screenshot(page, artifacts_dir, "add_rows_failed")
        raise RpaError(f"新增明细行失败：{exc}", screenshot_path=sp) from exc

    for it in items:
        try:
            row = page.locator(f'tr[data-row-index="{it.row_index}"]')
            await row.wait_for(timeout=DEFAULT_TIMEOUT_MS)
            await _pause(300, 800)
            await row.locator('input[name="name"]').fill(it.name)
            await row.locator('input[name="account"]').fill(it.account)
            await row.locator('input[name="note"]').fill(it.note or "")
            await row.locator('input[name="amount"]').fill(f"{it.amount}")
        except Exception as exc:
            sp = await _safe_screenshot(page, artifacts_dir, f"fill_row_{it.row_index}_failed")
            raise RpaError(f"填第 {it.row_index} 行失败：{exc}", screenshot_path=sp) from exc

    try:
        await page.fill('input[name="purpose"]', "仿真批量提交示例")
    except Exception as exc:
        logger.warning("填写用途失败（非致命）：%s", exc)


async def _submit_and_get_batch_id(page, token_pin: str, artifacts_dir: str | None) -> str:
    try:
        await _pause(800, 1500)
        await page.locator('form[name="simBatchForm"] button[type="submit"]').click()
    except Exception as exc:
        sp = await _safe_screenshot(page, artifacts_dir, "click_submit_failed")
        raise RpaError(f"点击提交失败：{exc}", screenshot_path=sp) from exc

    dlg_sel = 'div[role="dialog"][aria-modal="true"]'
    try:
        await page.wait_for_selector(dlg_sel, timeout=DEFAULT_TIMEOUT_MS)
    except Exception as exc:
        sp = await _safe_screenshot(page, artifacts_dir, "pin_dialog_not_open")
        raise RpaError(f"PIN 弹窗未出现：{exc}", screenshot_path=sp) from exc

    try:
        pin_input = page.locator(f'{dlg_sel} input[type="password"][inputmode="numeric"]')
        await _pause(500, 1200)
        await pin_input.fill(token_pin)
    except Exception as exc:
        sp = await _safe_screenshot(page, artifacts_dir, "fill_pin_failed")
        raise RpaError(f"填写 PIN 失败：{exc}", screenshot_path=sp) from exc

    try:
        await page.locator(dlg_sel).get_by_role("button", name=re.compile(r"确认提交")).click()
    except Exception as exc:
        sp = await _safe_screenshot(page, artifacts_dir, "click_confirm_failed")
        raise RpaError(f"确认提交失败：{exc}", screenshot_path=sp) from exc

    try:
        await page.wait_for_selector('[data-testid="batch-id"]', timeout=SUBMIT_NAVIGATE_TIMEOUT_MS)
    except Exception as exc:
        sp = await _safe_screenshot(page, artifacts_dir, "success_area_not_visible")
        raise RpaError(f"提交后未出现成功区域：{exc}", screenshot_path=sp) from exc

    batch_id = await page.locator('[data-testid="batch-id"]').get_attribute("data-batch-id") or ""
    if not batch_id:
        batch_id = (await page.locator('[data-testid="batch-id"]').inner_text()).strip()
    url = page.url
    if not batch_id and "#/batch/" in url:
        batch_id = url.split("#/batch/", 1)[1].split("?")[0].split("#")[0].strip("/")
    if not batch_id:
        sp = await _safe_screenshot(page, artifacts_dir, "batch_id_empty")
        raise RpaError(f"无法解析 batch_id，url={url}", screenshot_path=sp)
    return batch_id


async def _safe_screenshot(page, artifacts_dir: str | None, tag: str) -> Optional[str]:
    if not artifacts_dir:
        return None
    try:
        os.makedirs(artifacts_dir, exist_ok=True)
        path = os.path.join(artifacts_dir, f"{tag}_{int(time.time())}.png")
        await page.screenshot(path=path, full_page=True)
        logger.info("screenshot_saved path=%s", path)
        return path
    except Exception as exc:
        logger.warning("screenshot_failed tag=%s err=%s", tag, exc)
        return None


async def submit_batch_rpa(
    account: dict[str, Any],
    *,
    target: str,
    items: list[BatchItem],
    base_url: str,
    artifacts_dir: str | None,
    video_session: Any = None,
    headless: bool | None = None,
) -> BatchSubmitResult:
    del video_session  # 示例占位；真实 skill 可接入 RpaVideoSession

    profile_dir = str(account.get("profile_dir") or "").strip()
    if not profile_dir:
        return BatchSubmitResult(
            ok=False,
            batch_id=None,
            submitted_count=0,
            submitted_amount=0.0,
            error_msg="账号缺少 profile_dir",
            artifacts={"adapter": "simulator_rpa"},
        )

    if not items:
        return BatchSubmitResult(
            ok=False,
            batch_id=None,
            submitted_count=0,
            submitted_amount=0.0,
            error_msg="items 为空",
            artifacts={"adapter": "simulator_rpa"},
        )

    if not find_chrome_executable():
        return BatchSubmitResult(
            ok=False,
            batch_id=None,
            submitted_count=0,
            submitted_amount=0.0,
            error_msg="未检测到 Chrome 或 Edge 浏览器，请安装系统浏览器后重试。",
            artifacts={"adapter": "simulator_rpa"},
        )

    creds = _resolve_credentials(account)
    portal_wait = portal_login_wait_sec()
    hl = headless if headless is not None else _headless()

    pw = None
    context = None
    page = None
    try:
        pw, context, page = await start_browser_session(profile_dir, headless=hl)
        logger.info("rpa_goto url=%s", base_url)
        await page.goto(base_url, wait_until="domcontentloaded", timeout=GOTO_TIMEOUT_MS)

        await _wait_portal_gate(page, portal_wait)
        logger.info("rpa_login_start")
        await _login(page, creds, artifacts_dir)
        logger.info("rpa_login_done")

        await _goto_batch_page(page, artifacts_dir)
        logger.info("rpa_batch_page_ready")

        await _fill_batch_form(page, target, items, artifacts_dir)
        logger.info("rpa_batch_form_filled rows=%s", len(items))

        batch_id = await _submit_and_get_batch_id(page, creds.token_pin, artifacts_dir)
        logger.info("rpa_submit_success batch_id=%s", batch_id)

        total = sum(it.amount for it in items)
        return BatchSubmitResult(
            ok=True,
            batch_id=batch_id,
            submitted_count=len(items),
            submitted_amount=total,
            error_msg=None,
            artifacts={"adapter": "simulator_rpa"},
        )
    except RpaError as exc:
        logger.error("rpa_failed: %s", exc)
        arts = {"adapter": "simulator_rpa"}
        if exc.screenshot_path:
            arts["screenshot"] = exc.screenshot_path
        elif page is not None:
            sp = await _safe_screenshot(page, artifacts_dir, "rpa_error")
            if sp:
                arts["screenshot"] = sp
        return BatchSubmitResult(
            ok=False,
            batch_id=None,
            submitted_count=0,
            submitted_amount=0.0,
            error_msg=str(exc),
            artifacts=arts,
        )
    except Exception as exc:
        logger.exception("rpa_unexpected: %s", exc)
        arts = {"adapter": "simulator_rpa"}
        if page is not None:
            sp = await _safe_screenshot(page, artifacts_dir, "unexpected_error")
            if sp:
                arts["screenshot"] = sp
        return BatchSubmitResult(
            ok=False,
            batch_id=None,
            submitted_count=0,
            submitted_amount=0.0,
            error_msg=f"未预期异常：{type(exc).__name__}: {exc}",
            artifacts=arts,
        )
    finally:
        await close_browser_session(pw, context)
