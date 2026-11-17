"""百度知道回答发布 RPA（async Playwright）。

按 development/REQUIREMENTS.md §6 的 25 步主流程实现：
  阶段 A（步 1-14）：账号租约、浏览器启动、登录门、问题页就绪、幂等预检、文稿加载、编辑器打开
  阶段 B（步 15-25）：粘贴正文、点击发布、等待结果、解析状态、写记录、释放租约

selector 实测状态（2026-07-20 F12 实测确认）：
  - QUESTION_TITLE_SELECTOR          ✅ 已验证（span.ask-title）
  - ANSWER_EDITOR_OPEN_SELECTORS     ✅ 已验证（#answer-bar，<span> 标签，文案「我来答」）
  - ANSWER_EDITOR_IFRAME_SELECTORS   ✅ 已验证（UEditor iframe，body contenteditable=true）
  - ANSWER_PUBLISH_BUTTON_SELECTORS  ✅ 已验证（a.new-editor-deliver-btn，文案「提交回答」）
  - PUBLISH_TOAST_SELECTOR           ✅ 已验证（.tipLayer.success-tip，文案「提交成功」）
  - LOGGED_IN_SELECTORS              ⚠️ 公开资料推断，需登录态 F12 复核

注意：
  - 滑块、短信验证码一律走 human_verification.wait_human_verification_if_present，
    不自动拖动、不自动填写。
  - 正文字段写入：UEditor 是 iframe + contenteditable body，
    用 frame_locator 进 iframe 后 click 聚焦 + keyboard.type 逐字输入。
"""

from __future__ import annotations

import asyncio
import logging
import os
import random
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from service.browser_session import close_browser_context, start_browser_session
from service.human_verification import (
    HumanVerificationWaitResult,
    wait_human_verification_if_present,
    wait_save_login_countdown_if_present,
)
from util.constants import (
    ANSWER_EDITOR_BODY_SELECTOR,
    ANSWER_EDITOR_IFRAME_SELECTORS,
    ANSWER_EDITOR_OPEN_SELECTORS,
    ANSWER_EDITOR_TEXTAREA_SELECTORS,
    ANSWER_PUBLISH_BUTTON_SELECTORS,
    HUMAN_WAIT_TIMEOUT,
    LOG_LOGGER_NAME,
    LOGGED_IN_SELECTORS,
    LOGGED_OUT_SELECTOR,
    PUBLISH_FAILED_MARKERS,
    PUBLISH_FAILED_TOAST_SELECTOR,
    PUBLISH_PENDING_REVIEW_MARKERS,
    PUBLISH_SUCCESS_MARKERS,
    PUBLISH_SUCCESS_TOAST_SELECTOR,
    PUBLISH_TOAST_SELECTOR,
    PUBLISH_WAIT_TIMEOUT_SEC,
    QUESTION_TITLE_SELECTOR,
    QUESTION_URL_PREFIXES,
)
from util.logging import mask_text, safe_log_value

logger = logging.getLogger(LOG_LOGGER_NAME)


# 发布状态枚举
STATUS_SUCCESS = "success"
STATUS_PENDING_REVIEW = "pending_review"
STATUS_FAILED = "failed"


@dataclass
class PublishError:
    code: str
    message: str
    browser_started: bool = False
    stage: Optional[str] = None


@dataclass
class PublishRunResult:
    success: bool
    status: str = STATUS_FAILED
    platform_message: str = ""
    account_id: str = ""
    question_url: str = ""
    answer_path: str = ""
    publish_record_id: Optional[int] = None
    error: Optional[PublishError] = None


StepCallback = Callable[[str], None]


def _step_cb(cb: Optional[StepCallback], text: str) -> None:
    if cb:
        cb(text)


def _mask_account_ref(account: Dict[str, Any]) -> str:
    for key in ("login_id", "phone", "mobile"):
        raw = str(account.get(key) or "").strip()
        if raw:
            return mask_text(raw)
    aid = account.get("id") or account.get("account_id")
    if aid is not None:
        return f"id:{aid}"
    return "unknown"


async def _random_delay() -> None:
    lo = int(os.getenv("RPA_STEP_DELAY_MIN_MS") or "900")
    hi = int(os.getenv("RPA_STEP_DELAY_MAX_MS") or "2600")
    await asyncio.sleep(random.uniform(lo / 1000.0, hi / 1000.0))


def _headless() -> bool:
    v = (os.getenv("OPENCLAW_BROWSER_HEADLESS") or "0").strip().lower()
    return v in ("1", "true", "yes", "on")


def _human_wait_sec() -> int:
    return int(os.getenv("HUMAN_WAIT_TIMEOUT") or str(HUMAN_WAIT_TIMEOUT))


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
    """登录态检测。

    LOGGED_IN_SELECTORS 当前为基于公开资料的候选集合（href 含 /user/center 或 /usercenter，
    以及 .user-name / .user-icon class）。LOGGED_OUT_SELECTOR 为 a:has-text('登录')。
    实际登录态 class/id 建议在首次真实运行时 F12 复核，但当前组合对百度通行证通用登录
    路径已具备基本识别能力。
    """
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
    """登录门 HITL：若未登录则提示用户在浏览器中完成登录，最多等待 wait_sec 秒。"""
    if await _is_logged_in(page):
        return

    await _open_login_panel_if_needed(page)
    if await _is_logged_in(page):
        return

    print(f"[登录] 请在浏览器中完成百度账号登录，最多等待 {wait_sec} 秒...")
    deadline = time.monotonic() + wait_sec
    while time.monotonic() < deadline:
        if await _is_logged_in(page):
            print("[登录] 检测到登录成功")
            return
        await asyncio.sleep(2.0)

    raise RuntimeError(
        "ERROR:REQUIRE_LOGIN 浏览器已打开，但未完成百度账号登录。"
        "请重新运行任务并在浏览器打开后及时完成登录。"
    )


def _validate_question_url(url: str) -> None:
    url = (url or "").strip()
    if not url:
        raise ValueError("QUESTION_URL_EMPTY 未提供问题 URL。")
    if not url.startswith(QUESTION_URL_PREFIXES):
        raise ValueError(
            "QUESTION_URL_INVALID 问题 URL 必须形如 "
            "https://zhidao.baidu.com/question/XXXXXXX"
        )


async def _wait_question_page_ready(page, question_url: str) -> None:
    """步 6：问题页就绪检测（标题可见）。

    selector 已 F12 实测确认：百度知道问题标题稳定 class 为 `ask-title`（<span> 标签）。
    """
    try:
        loc = page.locator(QUESTION_TITLE_SELECTOR).first
        await loc.wait_for(state="visible", timeout=15_000)
    except Exception as exc:
        raise RuntimeError(
            "ERROR:QUESTION_NOT_FOUND 问题页未就绪，未找到问题标题。"
            f"请检查问题 URL 是否有效（{question_url}）。"
            f"（{exc}）"
        ) from exc


async def _load_answer_content(answer_path: str) -> str:
    """步 8-9：加载回答文稿并校验正文非空。"""
    path = (answer_path or "").strip()
    if not path:
        raise ValueError("ANSWER_PATH_EMPTY 未提供回答文稿路径。")
    if not os.path.isfile(path):
        raise ValueError(f"ANSWER_FILE_NOT_FOUND 回答文稿不存在：{path}")
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(path, encoding="utf-8", errors="replace") as f:
            content = f.read()
    content = content.strip()
    if not content:
        raise ValueError("INVALID_BODY 回答文稿内容为空。")
    return content


async def _check_question_not_answerable(page) -> Optional[str]:
    """检测问题是否不可回答（已回答/已关闭），返回原因或 None。

    注意：百度知道即使已有最佳答案，仍允许追加回答，故不将"有最佳答案"视为不可回答。
    """
    # 当前用户已回答过
    my_answer = page.locator(".answer-mine, .my-answer").first
    if await _visible(my_answer):
        return "ALREADY_ANSWERED 您已回答过该问题，不能重复回答。"
    # 问题已关闭
    closed = page.locator(".question-closed, .closed-tip, :text('问题已关闭')").first
    if await _visible(closed):
        return "QUESTION_CLOSED 该问题已关闭，不再接受回答。"
    return None


async def _open_answer_editor(page) -> Tuple[Any, str]:
    """步 10-11：点击「我来答」打开编辑器，返回 (frame_locator, body_selector)。

    selector 演变：
      2026-07-20 旧版：<span id="answer-bar" alog-alias="qb-answer-bar">
      2026-07-22 新版：<a class="push-item-btn"> / <a class="answer-btn">
      编辑器：UEditor iframe + 内部 <body contenteditable="true">

    返回的 frame_locator 用于后续在 iframe 内执行 click / type 操作。
    若 iframe 定位失败，会 fallback 到 textarea 模式（兼容未来改版）。
    """
    # 步 10：点击「我来答」按钮
    # 优先尝试问题主体区域的按钮（排除底部推荐区 a.push-item-btn）
    opened = False
    for sel in ANSWER_EDITOR_OPEN_SELECTORS:
        try:
            loc = page.locator(sel).first
            if await _visible(loc):
                # 对 a 标签做 href 校验：推荐区按钮 href 指向其他问题 URL
                # 当前问题的"我来答"按钮 href 为 # 或 javascript:void(0) 或无 href
                try:
                    href = await loc.get_attribute("href", timeout=500) or ""
                except Exception:
                    href = ""
                if href and href.startswith("http") and "zhidao.baidu.com/question" in href:
                    logger.debug("skip_recommendation_link selector=%s href=%s", sel, href)
                    continue
                await loc.click()
                await _random_delay()
                opened = True
                break
        except Exception:
            continue

    if not opened:
        # 先检测是否因问题不可回答
        reason = await _check_question_not_answerable(page)
        if reason:
            raise RuntimeError(f"ERROR:{reason}")
        raise RuntimeError(
            "ERROR:EDITOR_OPEN_FAILED 未找到「我来答」入口。"
            "请确认页面已加载完成或 F12 校正 ANSWER_EDITOR_OPEN_SELECTORS。"
        )

    # 步 11：等待 UEditor iframe 出现
    for sel in ANSWER_EDITOR_IFRAME_SELECTORS:
        try:
            iframe_loc = page.locator(sel).first
            await iframe_loc.wait_for(state="visible", timeout=10_000)
            frame = page.frame_locator(sel)
            # 验证 iframe 内的 contenteditable body 可见
            body_loc = frame.locator(ANSWER_EDITOR_BODY_SELECTOR).first
            await body_loc.wait_for(state="visible", timeout=5_000)
            return frame, ANSWER_EDITOR_BODY_SELECTOR
        except Exception:
            continue

    # fallback：尝试 textarea 模式（兼容未来 UEditor 改回 textarea）
    for sel in ANSWER_EDITOR_TEXTAREA_SELECTORS:
        try:
            loc = page.locator(sel).first
            await loc.wait_for(state="visible", timeout=5_000)
            # 返回 None 表示不走 iframe，用 page.locator 直接操作
            return None, sel
        except Exception:
            continue

    raise RuntimeError(
        "ERROR:EDITOR_NOT_READY 回答编辑器未就绪。"
        "请 F12 校正 ANSWER_EDITOR_IFRAME_SELECTORS / ANSWER_EDITOR_BODY_SELECTOR。"
    )


async def _type_answer_content(page, editor_frame: Any, editor_selector: str, content: str) -> None:
    """步 15-16：逐字粘贴正文。

    UEditor 是 iframe + contenteditable body，操作策略：
      1. 通过 frame_locator 进入 iframe
      2. click body 聚焦
      3. Control+A 全选 + Delete 清空（防止残留草稿）
      4. keyboard.type 逐字输入，加入随机延迟模拟人类

    若 editor_frame 为 None，表示编辑器是 textarea 模式，直接用 page.locator 操作。
    """
    if editor_frame is None:
        # textarea 模式
        loc = page.locator(editor_selector).first
    else:
        # iframe + contenteditable body 模式
        loc = editor_frame.locator(editor_selector).first

    await loc.click()
    await _random_delay()
    # 清空已有内容（防止残留草稿）
    await page.keyboard.press("Control+A")
    await page.keyboard.press("Delete")
    await _random_delay()
    # 逐字输入，加入随机延迟模拟人类
    # 过长内容分片输入，避免 keyboard.type 一次过长导致丢失
    chunk_size = 200
    for i in range(0, len(content), chunk_size):
        chunk = content[i : i + chunk_size]
        await page.keyboard.type(chunk, delay=random.randint(50, 150))
        await asyncio.sleep(random.uniform(0.3, 0.8))
    await _random_delay()


async def _click_publish_button(page) -> None:
    """步 17：点击「提交回答」。

    selector 已 F12 实测确认（2026-07-20）：
      <a class="btn-32-green grid-r new-editor-deliver-btn">提交回答</a>
    优先用 new-editor-deliver-btn 业务 class，fallback 到文案匹配。
    """
    for sel in ANSWER_PUBLISH_BUTTON_SELECTORS:
        try:
            loc = page.locator(sel).first
            if await _visible(loc):
                # 检查按钮是否 disabled（<a> 标签用 aria-disabled 或 class 判断）
                disabled = await loc.get_attribute("disabled")
                aria_disabled = await loc.get_attribute("aria-disabled")
                if disabled is not None or aria_disabled == "true":
                    raise RuntimeError(
                        "ERROR:PUBLISH_BUTTON_DISABLED 发布按钮当前不可点击（disabled）。"
                        "可能是正文未填或触发了平台限制。"
                    )
                await loc.click()
                return
        except RuntimeError:
            raise
        except Exception:
            continue
    raise RuntimeError(
        "ERROR:PUBLISH_BUTTON_NOT_FOUND 未找到「提交回答」按钮（a.new-editor-deliver-btn）。"
        "请 F12 校正 ANSWER_PUBLISH_BUTTON_SELECTORS。"
    )


async def _wait_publish_result(page) -> Tuple[str, str]:
    """步 19-20：等待 toast / 跳转，解析发布状态。

    返回 (status, platform_message)：
      - status: success / pending_review / failed
      - platform_message: 平台返回的提示文本

    selector 已 F12 实测确认（2026-07-20）：
      成功 toast：<div class="tipLayer success-tip"><span class="icon"></span><div>提交成功</div></div>
    优先用 .tipLayer 定位 toast，再读取内部文案；同时扫描页面正文应对跳转型反馈。
    """
    deadline = time.monotonic() + PUBLISH_WAIT_TIMEOUT_SEC
    while time.monotonic() < deadline:
        # 优先检查 .tipLayer toast（实测确认的容器）
        toast_text = ""
        try:
            # 先尝试成功 toast
            success_loc = page.locator(PUBLISH_SUCCESS_TOAST_SELECTOR).first
            if await _visible(success_loc):
                toast_text = (await success_loc.inner_text(timeout=500)).strip()
                if toast_text:
                    return STATUS_SUCCESS, toast_text
        except Exception:
            pass

        try:
            # 再尝试失败 toast
            failed_loc = page.locator(PUBLISH_FAILED_TOAST_SELECTOR).first
            if await _visible(failed_loc):
                toast_text = (await failed_loc.inner_text(timeout=500)).strip()
                if toast_text:
                    return STATUS_FAILED, toast_text
        except Exception:
            pass

        try:
            # 通用 toast 容器（应对审核中等其他状态）
            toast_loc = page.locator(PUBLISH_TOAST_SELECTOR).first
            if await _visible(toast_loc):
                toast_text = (await toast_loc.inner_text(timeout=500)).strip()
        except Exception:
            toast_text = ""

        # 也检查页面正文（发布成功后通常会跳转到回答列表页）
        page_text = ""
        try:
            page_text = await page.content()
        except Exception:
            page_text = ""

        combined = f"{toast_text}\n{page_text}"

        if toast_text:
            if any(m in toast_text for m in PUBLISH_SUCCESS_MARKERS):
                return STATUS_SUCCESS, toast_text
            if any(m in toast_text for m in PUBLISH_PENDING_REVIEW_MARKERS):
                return STATUS_PENDING_REVIEW, toast_text
            if any(m in toast_text for m in PUBLISH_FAILED_MARKERS):
                return STATUS_FAILED, toast_text

        # fallback：扫描整页文本（应对跳转型反馈，toast 已消失）
        if any(m in combined for m in PUBLISH_SUCCESS_MARKERS):
            return STATUS_SUCCESS, toast_text or "提交成功"
        if any(m in combined for m in PUBLISH_PENDING_REVIEW_MARKERS):
            return STATUS_PENDING_REVIEW, toast_text or "内容审核中"
        if any(m in combined for m in PUBLISH_FAILED_MARKERS):
            return STATUS_FAILED, toast_text or "提交失败"

        await asyncio.sleep(1.0)

    return STATUS_FAILED, "发布结果未在规定时间内出现（超时）"


def _fail_result(error: PublishError) -> PublishRunResult:
    logger.warning(
        "rpa_failed code=%s stage=%s message=%s",
        error.code,
        error.stage,
        error.message,
    )
    return PublishRunResult(success=False, status=STATUS_FAILED, error=error)


def _fail_on_verification_timeout(
    verification_timeout: HumanVerificationWaitResult,
) -> PublishRunResult:
    return _fail_result(
        PublishError(
            code=verification_timeout.code,
            message=verification_timeout.message,
            browser_started=True,
            stage=verification_timeout.stage or "unknown",
        )
    )


async def run_publish_answer_async(
    account: Dict[str, Any],
    question_url: str,
    answer_path: str,
    *,
    idempotency_key: str = "",
    step_callback: Optional[StepCallback] = None,
    optimize: bool = False,
    auto_approve: bool = False,
) -> PublishRunResult:
    """百度知道回答发布主流程（25 步）。"""
    profile_dir = account.get("profile_dir") or ""
    account_id = str(account.get("id") or account.get("account_id") or "")
    account_ref = _mask_account_ref(account)
    wait_sec = _human_wait_sec()

    logger.info(
        "rpa_start question_url=%s answer_path=%s idempotency_key=%s account_ref=%s",
        safe_log_value(question_url),
        answer_path,
        idempotency_key,
        account_ref,
    )

    # 步 3：校验问题 URL
    try:
        _validate_question_url(question_url)
    except ValueError as exc:
        return _fail_result(
            PublishError(
                code=str(exc).split(" ", 1)[0] if " " in str(exc) else "QUESTION_URL_INVALID",
                message=str(exc).split(" ", 1)[1] if " " in str(exc) else str(exc),
                browser_started=False,
                stage="param_validate",
            )
        )

    # 步 8-9：提前加载回答文稿（账号租约前校验，避免无效占用）
    # --optimize 模式下 answer_path 可为空（将由 AI 生成）
    answer_content = ""
    if answer_path:
        try:
            answer_content = await _load_answer_content(answer_path)
        except ValueError as exc:
            return _fail_result(
                PublishError(
                    code=str(exc).split(" ", 1)[0] if " " in str(exc) else "INVALID_BODY",
                    message=str(exc).split(" ", 1)[1] if " " in str(exc) else str(exc),
                    browser_started=False,
                    stage="param_validate",
                )
            )
    elif not optimize:
        return _fail_result(
            PublishError(
                code="ANSWER_PATH_EMPTY",
                message="非 --optimize 模式下必须提供回答文稿（--input-id）。",
                browser_started=False,
                stage="param_validate",
            )
        )

    if not profile_dir:
        return _fail_result(
            PublishError(
                code="ACCOUNT_NOT_FOUND",
                message="账号缺少 profile_dir。",
                browser_started=False,
                stage="account_prepare",
            )
        )

    pw = None
    context = None
    browser_started = False

    try:
        # 步 2：启动浏览器
        _step_cb(step_callback, "启动浏览器并打开百度知道")
        try:
            pw, context, page = await start_browser_session(profile_dir, headless=_headless())
        except RuntimeError as exc:
            msg = str(exc)
            err = PublishError(
                "MISSING_BROWSER" if "MISSING_BROWSER" in msg else "UNKNOWN_ERROR",
                msg.replace("ERROR:MISSING_BROWSER ", "").replace("ERROR:", ""),
                browser_started="未能打开目标首页" in msg,
                stage="browser_start" if "未能打开目标首页" in msg else "account_prepare",
            )
            return _fail_result(err)
        browser_started = True

        # 步 4：跳转到问题 URL
        _step_cb(step_callback, f"打开问题页：{question_url}")
        try:
            await page.goto(question_url, wait_until="domcontentloaded", timeout=60_000)
        except Exception as exc:
            return _fail_result(
                PublishError(
                    code="QUESTION_NOT_FOUND",
                    message=f"无法打开问题页：{exc}",
                    browser_started=True,
                    stage="goto_question",
                )
            )
        await _random_delay()

        # 步 5：登录门 HITL
        verification_timeout = await wait_human_verification_if_present(
            page, wait_sec=wait_sec, stage="browser_start"
        )
        if verification_timeout:
            return _fail_on_verification_timeout(verification_timeout)

        _step_cb(step_callback, "检查百度账号登录状态")
        logger.info("login_check_start current_url=%s", page.url)
        try:
            await _ensure_logged_in(page, wait_sec=wait_sec)
        except RuntimeError as exc:
            msg = str(exc)
            code = "REQUIRE_LOGIN" if "REQUIRE_LOGIN" in msg else "LOGIN_TIMEOUT"
            err = PublishError(
                code,
                msg.replace("ERROR:REQUIRE_LOGIN ", "").replace("ERROR:", ""),
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

        # 步 6：问题页就绪检测
        _step_cb(step_callback, "确认问题页已加载")
        await _wait_question_page_ready(page, question_url)
        await _random_delay()

        # 步 6.5：AI 回答优化（可选）
        if optimize:
            _step_cb(step_callback, "AI 优化：提取问题上下文并生成/优化回答")
            from service.answer_optimizer import (
                QuestionContext,
                extract_question_context,
                run_optimize_flow,
            )
            ctx = await extract_question_context(page, question_url)
            logger.info("optimize_question title=%s existing_answers=%d", ctx.title, len(ctx.existing_answers))
            _step_cb(step_callback, f"问题：{ctx.title}")

            # 如果已有草稿（answer_content），基于它优化；否则从头生成
            draft = answer_content if answer_content else None
            final_content, approved = run_optimize_flow(ctx, draft, auto_approve=auto_approve)
            if not approved or not final_content:
                return _fail_result(PublishError(
                    code="OPTIMIZE_REJECTED",
                    message="AI 优化流程被用户取消或审核未通过。",
                    browser_started=True,
                    stage="optimize",
                ))
            answer_content = final_content
            logger.info("optimize_done content_len=%d", len(answer_content))

        # 步 10-11：打开回答编辑器
        _step_cb(step_callback, "打开回答编辑器")
        editor_frame, editor_selector = await _open_answer_editor(page)
        logger.info(
            "answer_editor_ready mode=%s selector=%s",
            "iframe" if editor_frame is not None else "textarea",
            editor_selector,
        )

        verification_timeout = await wait_human_verification_if_present(
            page, wait_sec=wait_sec, stage="editor_open"
        )
        if verification_timeout:
            return _fail_on_verification_timeout(verification_timeout)

        # 步 15-16：逐字粘贴正文
        _step_cb(step_callback, "填写回答内容")
        await _type_answer_content(page, editor_frame, editor_selector, answer_content)
        logger.info("answer_typed content_len=%s", len(answer_content))

        verification_timeout = await wait_human_verification_if_present(
            page, wait_sec=wait_sec, stage="before_publish"
        )
        if verification_timeout:
            return _fail_on_verification_timeout(verification_timeout)

        # 步 17：点击发布
        _step_cb(step_callback, "点击发布回答")
        await _click_publish_button(page)
        logger.info("publish_clicked current_url=%s", page.url)

        # 步 18：二次确认弹窗（如有）
        await _random_delay()
        verification_timeout = await wait_human_verification_if_present(
            page, wait_sec=wait_sec, stage="publish_confirm"
        )
        if verification_timeout:
            return _fail_on_verification_timeout(verification_timeout)

        # 步 19-20：等待发布结果
        _step_cb(step_callback, "等待发布结果")
        status, platform_message = await _wait_publish_result(page)
        logger.info(
            "publish_result status=%s platform_message=%s current_url=%s",
            status,
            platform_message,
            page.url,
        )

        _step_cb(step_callback, "发布流程完成")
        return PublishRunResult(
            success=status != STATUS_FAILED,
            status=status,
            platform_message=platform_message,
            account_id=account_id,
            question_url=question_url,
            answer_path=answer_path,
        )

    except Exception as exc:
        err = PublishError(
            "UNKNOWN_ERROR",
            str(exc),
            browser_started=browser_started,
            stage="rpa",
        )
        return _fail_result(err)
    finally:
        # 步 25：关闭浏览器
        await close_browser_context(pw, context)
