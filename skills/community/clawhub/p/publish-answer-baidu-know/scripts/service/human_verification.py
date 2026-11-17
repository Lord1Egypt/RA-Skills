"""人工验证等待：保存登录倒计时、滑块、短信验证码等（不自动破解）。"""

from __future__ import annotations

import asyncio
import logging
import random
import re
import time
from dataclasses import dataclass
from typing import Optional

from util.constants import LOG_LOGGER_NAME

logger = logging.getLogger(LOG_LOGGER_NAME)

TEXT_EXCERPT_MAX = 120

SAVE_LOGIN_STRONG_MARKERS = (
    "是否保存登录信息",
    "下次登录更便捷",
    "保存登录信息",
)

SAVE_LOGIN_CONTAINER_SELECTORS = (
    "[role=\"dialog\"]",
    ".semi-modal",
    ".semi-modal-content",
)

SLIDER_SELECTORS = [
    ".vc-captcha-verify.slide",
    ".captcha_verify_bar--title",
    ".captcha-slider-tips",
    "#captcha_verify_image",
    ".captcha-slider-btn",
]

SMS_SELECTORS = [
    ".second-verify-panel",
    ".uc-ui-verify_sms-input",
    ".uc-ui-verify-new_header-title",
    "input[placeholder='手机号']",
    "input[placeholder='请输入验证码']",
]

DIALOG_TEXT_CONTAINERS = [
    "[role='dialog']",
    ".semi-modal",
    ".semi-modal-content",
    ".vc-captcha-verify",
    ".second-verify-panel",
]

RISK_MARKERS = (
    "操作频繁",
    "访问过于频繁",
    "风险验证",
    "安全验证",
)


@dataclass
class HumanVerificationState:
    present: bool
    kind: str
    message: str
    selector: str = ""
    text_excerpt: str = ""


@dataclass
class HumanVerificationWaitResult:
    timed_out: bool
    kind: str = ""
    code: str = ""
    message: str = ""
    stage: str = ""


def _text_excerpt(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", (text or "").strip())
    if len(cleaned) <= TEXT_EXCERPT_MAX:
        return cleaned
    return cleaned[:TEXT_EXCERPT_MAX] + "..."


def _contains_any(text: str, markers: tuple[str, ...]) -> bool:
    return any(m in text for m in markers)


async def _selector_visible(page, selector: str) -> bool:
    try:
        loc = page.locator(selector).first
        return await loc.is_visible(timeout=500)
    except Exception:
        return False


async def _selector_inner_text(page, selector: str) -> str:
    try:
        return await page.locator(selector).first.inner_text(timeout=1000)
    except Exception:
        return ""


async def _visible_text_from_first_visible(page, selectors: tuple[str, ...] | list[str]) -> tuple[str, str]:
    for sel in selectors:
        try:
            loc = page.locator(sel).first
            if await loc.is_visible(timeout=500):
                text = await loc.inner_text(timeout=1000)
                return sel, text or ""
        except Exception:
            continue
    return "", ""


def _save_login_popup_from_text(text: str) -> bool:
    if not text:
        return False
    if _contains_any(text, SAVE_LOGIN_STRONG_MARKERS):
        return True
    if "保存" in text and "取消" in text and ("登录" in text or "登录信息" in text):
        return True
    return False


async def detect_save_login_popup(page) -> bool:
    sel, text = await _visible_text_from_first_visible(page, SAVE_LOGIN_CONTAINER_SELECTORS)
    if sel and _save_login_popup_from_text(text):
        return True
    return False


async def wait_save_login_countdown_if_present(page, timeout_sec: int = 8) -> bool:
    """若出现“保存登录信息”倒计时弹窗则等待其消失；未出现则立即返回 False。"""
    if not await detect_save_login_popup(page):
        return False

    logger.info("save_login_popup_detected")
    print("[登录] 检测到“保存登录信息”倒计时弹窗，等待其自动关闭...")
    start = time.monotonic()
    deadline = start + timeout_sec
    while time.monotonic() < deadline:
        if not await detect_save_login_popup(page):
            elapsed = round(time.monotonic() - start, 2)
            logger.info("save_login_popup_gone elapsed_sec=%s", elapsed)
            return True
        await asyncio.sleep(0.5)

    elapsed = round(time.monotonic() - start, 2)
    logger.warning(
        "save_login_popup_still_visible elapsed_sec=%s timeout_sec=%s",
        elapsed,
        timeout_sec,
    )
    print(
        f"[登录] 警告：保存登录信息弹窗超过 {timeout_sec} 秒仍未消失，"
        "将继续后续流程（您可能已手工点击保存/取消）。"
    )
    return True


async def detect_slider_verification(page) -> Optional[HumanVerificationState]:
    sel_slide = ".vc-captcha-verify.slide"
    if await _selector_visible(page, sel_slide):
        text = await _selector_inner_text(page, sel_slide)
        return HumanVerificationState(
            present=True,
            kind="slider",
            message="滑块验证码",
            selector=sel_slide,
            text_excerpt=_text_excerpt(text),
        )

    sel_title = ".captcha_verify_bar--title"
    if await _selector_visible(page, sel_title):
        title_text = await _selector_inner_text(page, sel_title)
        if "请完成下列验证后继续" in title_text:
            return HumanVerificationState(
                present=True,
                kind="slider",
                message="滑块验证码",
                selector=sel_title,
                text_excerpt=_text_excerpt(title_text),
            )

    sel_tips = ".captcha-slider-tips"
    if await _selector_visible(page, sel_tips):
        tips_text = await _selector_inner_text(page, sel_tips)
        if "拖动完成上方拼图" in tips_text:
            return HumanVerificationState(
                present=True,
                kind="slider",
                message="滑块验证码",
                selector=sel_tips,
                text_excerpt=_text_excerpt(tips_text),
            )

    if await _selector_visible(page, "#captcha_verify_image"):
        for btn_sel in (".captcha-slider-btn", ".captcha_verify_slide--button", ".captcha-slider"):
            if await _selector_visible(page, btn_sel):
                return HumanVerificationState(
                    present=True,
                    kind="slider",
                    message="滑块验证码",
                    selector=f"#captcha_verify_image+{btn_sel}",
                    text_excerpt="",
                )

    return None


async def detect_sms_verification(page) -> Optional[HumanVerificationState]:
    sel_panel = ".second-verify-panel"
    if await _selector_visible(page, sel_panel):
        text = await _selector_inner_text(page, sel_panel)
        return HumanVerificationState(
            present=True,
            kind="sms",
            message="短信验证码",
            selector=sel_panel,
            text_excerpt=_text_excerpt(text),
        )

    sel_sms = ".uc-ui-verify_sms-input"
    if await _selector_visible(page, sel_sms):
        text = await _selector_inner_text(page, sel_sms)
        return HumanVerificationState(
            present=True,
            kind="sms",
            message="短信验证码",
            selector=sel_sms,
            text_excerpt=_text_excerpt(text),
        )

    sel_hdr = ".uc-ui-verify-new_header-title"
    if await _selector_visible(page, sel_hdr):
        hdr_text = await _selector_inner_text(page, sel_hdr)
        if "短信验证" in hdr_text:
            return HumanVerificationState(
                present=True,
                kind="sms",
                message="短信验证码",
                selector=sel_hdr,
                text_excerpt=_text_excerpt(hdr_text),
            )

    phone_visible = await _selector_visible(
        page,
        ".second-verify-panel input[placeholder='手机号'], .uc-ui-verify_sms-input input[placeholder='手机号']",
    )
    code_visible = await _selector_visible(
        page,
        ".second-verify-panel input[placeholder='请输入验证码'], .uc-ui-verify_sms-input input[placeholder='请输入验证码']",
    )
    if phone_visible and code_visible:
        return HumanVerificationState(
            present=True,
            kind="sms",
            message="短信验证码",
            selector="sms-phone-and-code-inputs",
            text_excerpt="手机号+请输入验证码",
        )

    return None


async def detect_human_verification_from_containers(page) -> Optional[HumanVerificationState]:
    sel, text = await _visible_text_from_first_visible(page, DIALOG_TEXT_CONTAINERS)
    if not sel or not text:
        return None

    if _contains_any(text, RISK_MARKERS):
        return HumanVerificationState(
            present=True,
            kind="risk",
            message="安全/频控验证",
            selector=sel,
            text_excerpt=_text_excerpt(text),
        )

    if sel in (".vc-captcha-verify", ".vc-captcha-verify-visibility"):
        if "请完成下列验证后继续" in text or "拖动完成上方拼图" in text:
            return HumanVerificationState(
                present=True,
                kind="slider",
                message="滑块验证码",
                selector=sel,
                text_excerpt=_text_excerpt(text),
            )

    if sel in (".second-verify-panel", ".uc-ui-verify_sms-input"):
        if "短信验证" in text or "获取验证码" in text:
            return HumanVerificationState(
                present=True,
                kind="sms",
                message="短信验证码",
                selector=sel,
                text_excerpt=_text_excerpt(text),
            )

    return None


async def detect_human_verification(page) -> HumanVerificationState:
    """主检测入口：仅在验证码/弹窗容器级检测，不扫整页 body。"""
    state = await detect_slider_verification(page)
    if state is not None:
        return state
    state = await detect_sms_verification(page)
    if state is not None:
        return state
    state = await detect_human_verification_from_containers(page)
    if state is not None:
        return state
    return HumanVerificationState(present=False, kind="", message="", selector="", text_excerpt="")


def detect_human_verification_from_text(text: str) -> HumanVerificationState:
    """
    根据 HTML/容器文本判断验证弹窗（单元测试辅助，不能作为真实页面主检测入口）。
    只检查验证容器 DOM 标记，不根据正文关键词误判。
    """
    html_lower = (text or "").lower()
    has_slider_dom = (
        "vc-captcha-verify" in html_lower
        and "slide" in html_lower
        and (
            "captcha-slider-tips" in html_lower
            or "captcha_verify_bar--title" in html_lower
            or "captcha_verify_image" in html_lower
        )
    )
    if has_slider_dom:
        selector = ".vc-captcha-verify.slide"
        if "captcha-slider-tips" in html_lower:
            selector = ".captcha-slider-tips"
        return HumanVerificationState(
            present=True,
            kind="slider",
            message="滑块验证码",
            selector=selector,
            text_excerpt="",
        )

    has_sms_dom = "second-verify-panel" in html_lower or "uc-ui-verify_sms-input" in html_lower
    if has_sms_dom:
        selector = ".second-verify-panel" if "second-verify-panel" in html_lower else ".uc-ui-verify_sms-input"
        return HumanVerificationState(
            present=True,
            kind="sms",
            message="短信验证码",
            selector=selector,
            text_excerpt="",
        )

    return HumanVerificationState(present=False, kind="", message="", selector="", text_excerpt="")


def _wait_log_message(state: HumanVerificationState, wait_sec: int) -> str:
    if state.kind == "slider":
        return f"[人工验证] 检测到滑块验证码，请在浏览器中手工完成，最多等待 {wait_sec} 秒..."
    if state.kind == "sms":
        return f"[人工验证] 检测到短信验证码，请在浏览器中手工完成，最多等待 {wait_sec} 秒..."
    return f"[人工验证] 检测到安全验证，请在浏览器中手工处理，最多等待 {wait_sec} 秒..."


def _timeout_error_code(kind: str) -> str:
    if kind == "slider":
        return "SLIDER_VERIFICATION_TIMEOUT"
    if kind == "sms":
        return "SMS_VERIFICATION_TIMEOUT"
    return "HUMAN_VERIFICATION_TIMEOUT"


def _timeout_error_message(kind: str, wait_sec: int) -> str:
    if kind == "slider":
        return (
            f"滑块验证码未在 {wait_sec} 秒内完成，任务已停止。"
            "请重新运行任务并及时在浏览器中完成验证。"
        )
    if kind == "sms":
        return (
            f"短信验证码未在 {wait_sec} 秒内完成，任务已停止。"
            "请重新运行任务并及时完成短信验证。"
        )
    return (
        f"安全验证未在 {wait_sec} 秒内完成，任务已停止。"
        "请重新运行任务并及时在浏览器中完成验证。"
    )


async def wait_human_verification_if_present(
    page,
    *,
    wait_sec: int = 180,
    stage: str = "unknown",
) -> Optional[HumanVerificationWaitResult]:
    """
    若存在人工验证则等待用户完成；无验证或已完成返回 None；超时返回 HumanVerificationWaitResult。
    不自动拖动滑块、不自动填写短信验证码。
    """
    state = await detect_human_verification(page)
    if not state.present:
        return None

    logger.warning(
        "human_verification_detected stage=%s kind=%s selector=%s text=%s",
        stage,
        state.kind,
        state.selector,
        state.text_excerpt,
    )
    print(_wait_log_message(state, wait_sec))

    last_state = state
    start = time.monotonic()
    deadline = start + wait_sec

    while time.monotonic() < deadline:
        state = await detect_human_verification(page)
        if not state.present:
            elapsed = round(time.monotonic() - start, 2)
            logger.info(
                "human_verification_passed stage=%s kind=%s elapsed_sec=%s",
                stage,
                last_state.kind,
                elapsed,
            )
            await asyncio.sleep(random.uniform(1.0, 2.0))
            return None
        last_state = state
        await asyncio.sleep(2.0)

    logger.warning(
        "human_verification_timeout stage=%s kind=%s wait_sec=%s selector=%s",
        stage,
        last_state.kind,
        wait_sec,
        last_state.selector,
    )
    return HumanVerificationWaitResult(
        timed_out=True,
        kind=last_state.kind,
        code=_timeout_error_code(last_state.kind),
        message=_timeout_error_message(last_state.kind, wait_sec),
        stage=stage,
    )
