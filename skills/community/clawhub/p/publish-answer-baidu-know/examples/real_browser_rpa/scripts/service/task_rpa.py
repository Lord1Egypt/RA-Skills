"""真实网站关键词搜索 RPA 示例（async Playwright）。"""

from __future__ import annotations

import asyncio
import logging
import os
import random
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from service.browser_session import close_browser_context, get_start_url, start_browser_session
from service.human_verification import (
    HumanVerificationWaitResult,
    wait_human_verification_if_present,
    wait_save_login_countdown_if_present,
)
from util.constants import (
    DEFAULT_MAX_ITEMS,
    DEFAULT_MAX_SCROLLS,
    DEFAULT_NO_NEW_ROUNDS_LIMIT,
    HUMAN_WAIT_TIMEOUT,
    LOG_LOGGER_NAME,
    RESULT_CONTAINER_SELECTOR,
    RESULT_END_TEXT,
    RESULT_ITEM_SELECTOR,
    SCROLL_CONTAINER_SELECTORS,
    SEARCH_BUTTON_SELECTOR,
    SEARCH_INPUT_SELECTORS,
)
from util.logging import mask_text, safe_log_value

logger = logging.getLogger(LOG_LOGGER_NAME)


@dataclass
class ScrapeError:
    code: str
    message: str
    browser_started: bool = False
    stage: Optional[str] = None


@dataclass
class ScrapeRunResult:
    success: bool
    items: List[Dict[str, Any]] = field(default_factory=list)
    stop_reason: Optional[str] = None
    error: Optional[ScrapeError] = None


StepCallback = Callable[[str], None]

# 示例登录态 selector — 复制到新 skill 后必须用目标站点 F12/DOM 实测替换，禁止凭经验猜测或跨平台照抄
LOGGED_IN_SELECTORS = (
    "a[href*='/user/self']",
    "[data-user-avatar]",
    ".user-avatar",
)
LOGGED_OUT_SELECTOR = "button:has-text('登录')"


def format_stop_reason_for_user(stop_reason: str | None, collected_count: int) -> str:
    """将内部 stop_reason 枚举翻译为用户可理解的中文说明。"""
    if stop_reason == "max_items":
        return (
            f"已达到本次默认采集规模（{collected_count} 条）。"
            "如需更多，可以继续说「继续采集更多」或「尽量多采集」。"
        )
    if stop_reason == "end_marker":
        return "页面提示没有更多结果，本次采集已完成。"
    if stop_reason == "no_new_rounds":
        return "连续多次加载没有发现新结果，本次采集已完成。"
    if stop_reason == "max_scrolls":
        return (
            "已达到本次页面加载保护范围，本次采集已完成。"
            "如需更深度采集，可以说明「尽量多采集」。"
        )
    if stop_reason == "human_verification_timeout":
        return "人工验证未在规定时间内完成，任务已停止。"
    return "本次采集已完成。"


def _mask_account_ref(account: Dict[str, Any]) -> str:
    for key in ("login_id", "phone", "mobile"):
        raw = str(account.get(key) or "").strip()
        if raw:
            return mask_text(raw)
    aid = account.get("id") or account.get("account_id")
    if aid is not None:
        return f"id:{aid}"
    return "unknown"


def _step_cb(cb: Optional[StepCallback], text: str) -> None:
    if cb:
        cb(text)


async def _random_delay() -> None:
    lo = int(os.getenv("RPA_STEP_DELAY_MIN_MS") or "900")
    hi = int(os.getenv("RPA_STEP_DELAY_MAX_MS") or "2600")
    await asyncio.sleep(random.uniform(lo / 1000.0, hi / 1000.0))


async def _scroll_wait() -> None:
    await asyncio.sleep(random.uniform(1.2, 3.5))


def _headless() -> bool:
    v = (os.getenv("OPENCLAW_BROWSER_HEADLESS") or "0").strip().lower()
    return v in ("1", "true", "yes", "on")


def _no_new_limit() -> int:
    try:
        return int(os.getenv("RPA_NO_NEW_ROUNDS_LIMIT") or str(DEFAULT_NO_NEW_ROUNDS_LIMIT))
    except ValueError:
        return DEFAULT_NO_NEW_ROUNDS_LIMIT


async def _visible(locator) -> bool:
    try:
        return await locator.count() > 0 and await locator.is_visible(timeout=500)
    except Exception:
        return False


async def _is_logged_out(page) -> bool:
    try:
        btn = page.locator(LOGGED_OUT_SELECTOR).first
        return await _visible(btn)
    except Exception:
        return False


async def _is_logged_in(page) -> bool:
    if await _is_logged_out(page):
        return False
    for sel in LOGGED_IN_SELECTORS:
        try:
            loc = page.locator(sel).first
            if await _visible(loc):
                return True
        except Exception:
            continue
    return False


async def _open_login_panel_if_needed(page) -> None:
    if not await _is_logged_out(page):
        return
    try:
        btn = page.locator(LOGGED_OUT_SELECTOR).first
        if await _visible(btn):
            await btn.click()
            await asyncio.sleep(random.uniform(1.0, 3.0))
    except Exception:
        pass


async def _ensure_logged_in(page, *, wait_sec: int) -> None:
    if await _is_logged_in(page):
        return

    await _open_login_panel_if_needed(page)
    if await _is_logged_in(page):
        return

    print(f"[登录] 请在浏览器中完成登录，最多等待 {wait_sec} 秒...")
    deadline = time.monotonic() + wait_sec
    while time.monotonic() < deadline:
        if await _is_logged_in(page):
            print("[登录] 检测到登录成功")
            return
        await asyncio.sleep(2.0)

    raise RuntimeError(
        f"ERROR:LOGIN_TIMEOUT 浏览器已打开，但未完成登录。"
        f"请重新运行任务并在浏览器打开后及时完成登录。"
    )


async def _find_search_input(page) -> Tuple[Optional[Any], str]:
    for sel in SEARCH_INPUT_SELECTORS:
        try:
            loc = page.locator(sel).first
            if await _visible(loc):
                return loc, sel
        except Exception:
            continue

    candidates: List[Tuple[int, Any, str]] = []
    try:
        inputs = await page.locator("input").all()
    except Exception:
        inputs = []
    for inp in inputs:
        try:
            if not await inp.is_visible():
                continue
            box = await inp.bounding_box()
            if not box or box.get("width", 0) < 120:
                continue
            placeholder = await inp.get_attribute("placeholder") or ""
            score = box.get("width", 0)
            if "搜索" in placeholder:
                score += 500
            if box.get("y", 9999) < 200:
                score += 200
            candidates.append((score, inp, f"input placeholder={placeholder!r}"))
        except Exception:
            continue
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        _, inp, sel = candidates[0]
        return inp, sel

    try:
        ph = page.get_by_placeholder(re.compile("搜索"))
        if await ph.count() > 0 and await ph.first.is_visible():
            return ph.first, "placeholder=搜索"
    except Exception:
        pass
    return None, ""


async def _find_search_button(page):
    try:
        btn = page.get_by_role("button", name="搜索")
        if await btn.count() > 0 and await btn.first.is_visible():
            return btn.first
    except Exception:
        pass
    try:
        btn = page.locator(SEARCH_BUTTON_SELECTOR).first
        if await btn.count() > 0 and await btn.is_visible():
            return btn
    except Exception:
        pass
    return None


async def _wait_search_results(page, timeout_sec: float = 45.0) -> bool:
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        try:
            url = page.url or ""
            if "/search" in url or "search" in url.lower():
                if await page.locator(RESULT_CONTAINER_SELECTOR).count() > 0:
                    return True
        except Exception:
            pass
        await asyncio.sleep(0.8)
    return False


async def _has_end_marker(page) -> bool:
    try:
        container = page.locator(RESULT_CONTAINER_SELECTOR).first
        if await container.count() > 0:
            text = await container.inner_text(timeout=2000)
            if RESULT_END_TEXT in text or "暂时没有更多了" in text:
                return True
    except Exception:
        pass
    try:
        if await page.locator(f"text={RESULT_END_TEXT}").count() > 0:
            return True
    except Exception:
        pass
    return False


async def _mouse_wheel_scroll(page) -> Tuple[str, int]:
    wheel_delta = random.randint(650, 1200)
    for sel in SCROLL_CONTAINER_SELECTORS:
        loc = page.locator(sel)
        try:
            if await loc.count() > 0 and await loc.first.is_visible():
                await loc.first.hover()
                await _random_delay()
                await page.mouse.wheel(0, wheel_delta)
                return sel, wheel_delta
        except Exception:
            continue
    await page.mouse.wheel(0, wheel_delta)
    return "page", wheel_delta


async def _parse_item_locator(item) -> Dict[str, Any]:
    item_id = await item.get_attribute("data-item-id") or await item.get_attribute("id") or ""
    title = ""
    try:
        title = (await item.inner_text(timeout=1000)).strip()[:200]
    except Exception:
        pass
    return {
        "item_id": item_id or title[:32] or str(id(item)),
        "title": title,
    }


async def _collect_visible_items(page, seen_ids: set[str]) -> List[Dict[str, Any]]:
    new_items: List[Dict[str, Any]] = []
    try:
        items = await page.locator(RESULT_ITEM_SELECTOR).all()
    except Exception:
        items = []
    for item in items:
        try:
            parsed = await _parse_item_locator(item)
            item_id = parsed.get("item_id")
            if not item_id or item_id in seen_ids:
                continue
            seen_ids.add(str(item_id))
            new_items.append(parsed)
        except Exception:
            continue
    return new_items


async def _count_visible_items(page) -> int:
    try:
        return await page.locator(RESULT_ITEM_SELECTOR).count()
    except Exception:
        return 0


def _fail_result(error: ScrapeError, *, collected: int = 0) -> ScrapeRunResult:
    logger.warning(
        "rpa_failed code=%s stage=%s message=%s collected=%s",
        error.code,
        error.stage,
        error.message,
        collected,
    )
    return ScrapeRunResult(success=False, error=error)


def _fail_on_verification_timeout(
    verification_timeout: HumanVerificationWaitResult,
    *,
    collected: int = 0,
) -> ScrapeRunResult:
    return _fail_result(
        ScrapeError(
            code=verification_timeout.code,
            message=verification_timeout.message,
            browser_started=True,
            stage=verification_timeout.stage or "unknown",
        ),
        collected=collected,
    )


async def run_keyword_search_async(
    account: Dict[str, Any],
    keyword: str,
    *,
    max_items: int = DEFAULT_MAX_ITEMS,
    max_scrolls: int = DEFAULT_MAX_SCROLLS,
    data_dir: str = "",
    batch_id: str = "",
    step_callback: Optional[StepCallback] = None,
) -> ScrapeRunResult:
    profile_dir = account.get("profile_dir") or ""
    account_ref = _mask_account_ref(account)
    wait_sec = int(os.getenv("HUMAN_WAIT_TIMEOUT") or str(HUMAN_WAIT_TIMEOUT))
    no_new_limit = _no_new_limit()

    logger.info(
        "rpa_start keyword=%s max_items=%s max_scrolls=%s wait_sec=%s batch_id=%s account_ref=%s",
        safe_log_value(keyword),
        max_items,
        max_scrolls,
        wait_sec,
        batch_id,
        account_ref,
    )

    if not profile_dir:
        err = ScrapeError(
            "ACCOUNT_NOT_FOUND",
            "账号缺少 profile_dir。",
            browser_started=False,
            stage="account_prepare",
        )
        return _fail_result(err)

    pw = None
    context = None
    page = None
    browser_started = False
    collected_count = 0

    try:
        _step_cb(step_callback, "启动关键词搜索采集任务")
        try:
            pw, context, page = await start_browser_session(profile_dir, headless=_headless())
        except RuntimeError as exc:
            msg = str(exc)
            err = ScrapeError(
                "MISSING_BROWSER" if "MISSING_BROWSER" in msg else "UNKNOWN_ERROR",
                msg.replace("ERROR:MISSING_BROWSER ", "").replace("ERROR:", ""),
                browser_started="未能打开目标首页" in msg,
                stage="browser_start" if "未能打开目标首页" in msg else "account_prepare",
            )
            return _fail_result(err)
        browser_started = True

        logger.info(
            "browser_ready start_url=%s current_url=%s profile_dir_exists=%s",
            get_start_url(),
            page.url,
            os.path.isdir(profile_dir),
        )

        _step_cb(step_callback, "打开目标站点首页")
        await _random_delay()

        verification_timeout = await wait_human_verification_if_present(
            page, wait_sec=wait_sec, stage="browser_start"
        )
        if verification_timeout:
            return _fail_on_verification_timeout(verification_timeout)

        _step_cb(step_callback, "检查账号登录状态")
        logger.info("login_check_start current_url=%s", page.url)
        try:
            await _ensure_logged_in(page, wait_sec=wait_sec)
        except RuntimeError as exc:
            msg = str(exc)
            code = "LOGIN_TIMEOUT" if "LOGIN_TIMEOUT" in msg else "REQUIRE_LOGIN"
            err = ScrapeError(
                code,
                msg.replace("ERROR:LOGIN_TIMEOUT ", "").replace("ERROR:", ""),
                browser_started=True,
                stage="login_check",
            )
            return _fail_result(err)
        logger.info("login_check_done current_url=%s", page.url)

        await wait_save_login_countdown_if_present(page)

        verification_timeout = await wait_human_verification_if_present(
            page, wait_sec=wait_sec, stage="login_check"
        )
        if verification_timeout:
            return _fail_on_verification_timeout(verification_timeout)

        _step_cb(step_callback, "定位搜索框")
        search_input, input_selector = await _find_search_input(page)
        if search_input is None:
            err = ScrapeError(
                "SEARCH_INPUT_NOT_FOUND",
                "未找到搜索输入框。",
                browser_started=True,
                stage="search",
            )
            return _fail_result(err)
        logger.info("search_input_found selector=%s", input_selector)

        _step_cb(step_callback, f"输入关键词：{keyword}")
        await search_input.click()
        await _random_delay()
        await page.keyboard.press("Control+A")
        await page.keyboard.type(keyword, delay=random.randint(90, 240))
        await _random_delay()

        _step_cb(step_callback, "点击搜索")
        search_btn = await _find_search_button(page)
        search_method = "button"
        if search_btn is not None:
            await search_btn.click()
        else:
            search_method = "enter"
            await page.keyboard.press("Enter")
        logger.info(
            "search_submitted keyword=%s method=%s current_url=%s",
            safe_log_value(keyword),
            search_method,
            page.url,
        )
        await _random_delay()

        verification_timeout = await wait_human_verification_if_present(
            page, wait_sec=wait_sec, stage="search_verification"
        )
        if verification_timeout:
            return _fail_on_verification_timeout(verification_timeout)

        _step_cb(step_callback, "等待搜索结果")
        if not await _wait_search_results(page):
            verification_timeout = await wait_human_verification_if_present(
                page, wait_sec=wait_sec, stage="search_results"
            )
            if verification_timeout:
                return _fail_on_verification_timeout(verification_timeout)

            if not await _wait_search_results(page, timeout_sec=10.0):
                err = ScrapeError(
                    "RESULT_CONTAINER_NOT_FOUND",
                    "搜索结果未出现，且未检测到需要人工处理的验证码，请检查关键词或页面状态。",
                    browser_started=True,
                    stage="search",
                )
                return _fail_result(err)

        container_count = await page.locator(RESULT_CONTAINER_SELECTOR).count()
        logger.info(
            "search_results_ready current_url=%s container_count=%s",
            page.url,
            container_count,
        )

        try:
            await page.locator(RESULT_CONTAINER_SELECTOR).first.wait_for(state="visible", timeout=15_000)
        except Exception:
            err = ScrapeError(
                "RESULT_CONTAINER_NOT_FOUND",
                "搜索结果容器未出现。",
                browser_started=True,
                stage="search",
            )
            return _fail_result(err)

        seen_ids: set[str] = set()
        collected: List[Dict[str, Any]] = []
        no_new_rounds = 0
        stop_reason = "max_scrolls"
        rounds_executed = 0

        for scroll_round in range(max_scrolls + 1):
            rounds_executed = scroll_round
            _step_cb(step_callback, "读取当前结果列表")
            visible_count = await _count_visible_items(page)
            batch = await _collect_visible_items(page, seen_ids)
            new_count = len(batch)
            if batch:
                collected.extend(batch)
                no_new_rounds = 0
            else:
                no_new_rounds += 1

            collected_count = len(collected)
            end_marker = await _has_end_marker(page)
            logger.info(
                "collect_round round=%s max_scrolls=%s visible_count=%s new_count=%s "
                "collected=%s no_new_rounds=%s no_new_limit=%s end_marker=%s current_url=%s",
                scroll_round,
                max_scrolls,
                visible_count,
                new_count,
                collected_count,
                no_new_rounds,
                no_new_limit,
                end_marker,
                page.url,
            )

            if len(collected) >= max_items:
                collected = collected[:max_items]
                stop_reason = "max_items"
                break

            if end_marker:
                stop_reason = "end_marker"
                _step_cb(step_callback, "发现结果到底或达到采集数量")
                break

            if no_new_rounds >= no_new_limit:
                stop_reason = "no_new_rounds"
                logger.info(
                    "collect_no_new_stop round=%s no_new_rounds=%s no_new_limit=%s collected=%s",
                    scroll_round,
                    no_new_rounds,
                    no_new_limit,
                    collected_count,
                )
                break

            if scroll_round >= max_scrolls:
                break

            _step_cb(step_callback, "滚动加载更多结果")
            scroll_target, wheel_delta = await _mouse_wheel_scroll(page)
            logger.info(
                "scroll round=%s target=%s wheel_delta=%s",
                scroll_round,
                scroll_target,
                wheel_delta,
            )
            await _scroll_wait()

            verification_timeout = await wait_human_verification_if_present(
                page, wait_sec=wait_sec, stage="collect"
            )
            if verification_timeout:
                return _fail_on_verification_timeout(
                    verification_timeout,
                    collected=collected_count,
                )

        logger.info(
            "collect_stop reason=%s collected=%s rounds=%s no_new_rounds=%s",
            stop_reason,
            collected_count,
            rounds_executed,
            no_new_rounds,
        )

        if not collected:
            err = ScrapeError(
                "NO_RESULTS",
                "未采集到任何结果。",
                browser_started=True,
                stage="collect",
            )
            return _fail_result(err, collected=0)

        _step_cb(step_callback, "采集完成")
        logger.info(
            "rpa_success collected=%s stop_reason=%s",
            len(collected[:max_items]),
            stop_reason,
        )
        return ScrapeRunResult(success=True, items=collected[:max_items], stop_reason=stop_reason)

    except Exception as exc:
        err = ScrapeError(
            "UNKNOWN_ERROR",
            str(exc),
            browser_started=browser_started,
            stage="rpa",
        )
        return _fail_result(err, collected=collected_count)
    finally:
        await close_browser_context(pw, context)
