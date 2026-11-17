#!/usr/bin/env python3
"""检测站斧 check.html 插件页是否可进入业务自动化。"""

from __future__ import annotations

import argparse
import json
import sys
import time

from playwright.sync_api import BrowserContext, Page, sync_playwright

from headed_mode import ensure_headed_mode

CUSTOMER_FAIL_MSG = "没检测成功无法进行自动化"
DEFAULT_TIMEOUT_SEC = 15
POLL_INTERVAL_SEC = 1.0
KNOWN_CHECKS = ("设备安全检测", "环境安全检测", "线路优化检测")

_OPEN_MALL_BTN_JS = """() => {
    const btn = document.querySelector('.openMallOpenBtn')
        || [...document.querySelectorAll('button')].find(
            b => (b.textContent || '').includes('打开店铺')
        );
    if (!btn) return null;
    const disabled = btn.disabled
        || btn.getAttribute('aria-disabled') === 'true'
        || btn.classList.contains('is-disabled');
    return !disabled;
}"""


def find_check_page(context: BrowserContext) -> Page | None:
    for page in context.pages:
        if "check.html" in page.url:
            return page
    return context.pages[0] if context.pages else None


def is_open_mall_button_enabled(page: Page) -> bool | None:
    try:
        return page.evaluate(_OPEN_MALL_BTN_JS)
    except Exception:
        return None


def evaluate_detection_passed(context: BrowserContext, page: Page) -> dict:
    tab_count = len(context.pages)
    button_enabled = is_open_mall_button_enabled(page)

    passed = tab_count >= 2 or button_enabled is True
    if tab_count >= 2:
        pass_reason = "tabs>=2"
    elif button_enabled is True:
        pass_reason = "open_mall_button_enabled"
    else:
        pass_reason = None

    return {
        "tab_count": tab_count,
        "open_mall_button_enabled": button_enabled,
        "device_security_success": passed,
        "pass_reason": pass_reason,
        "verdict": "success" if passed else "in_progress",
    }


def parse_security_status(text: str) -> dict:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    checks: dict[str, str | None] = {name: None for name in KNOWN_CHECKS}
    current: str | None = None
    for ln in lines:
        if ln in KNOWN_CHECKS:
            current = ln
            continue
        if ln in ("成功", "失败") and current:
            checks[current] = ln
            current = None

    return {
        "device_security_check": checks.get("设备安全检测"),
        "environment_check": checks.get("环境安全检测"),
        "line_check": checks.get("线路优化检测"),
        "safe_to_login": "当前环境检测安全" in text,
        "all_checks": checks,
        "related_lines": [
            ln for ln in lines
            if any(k in ln for k in ("设备安全", "环境安全", "线路优化", "检测安全", "检测失败"))
        ],
        "body_preview": text[:500],
    }


def read_check_status(context: BrowserContext, page: Page) -> dict:
    info = evaluate_detection_passed(context, page)
    try:
        text = page.inner_text("body", timeout=5000)
        info.update(parse_security_status(text))
    except Exception as exc:
        info["read_error"] = str(exc)
    return info


def wait_device_security_success(
    context: BrowserContext,
    page: Page,
    timeout_sec: int = DEFAULT_TIMEOUT_SEC,
) -> dict:
    deadline = time.monotonic() + timeout_sec
    last: dict = {"verdict": "in_progress", "device_security_success": False}

    while time.monotonic() < deadline:
        try:
            last = read_check_status(context, page)
            if last.get("device_security_success"):
                last["verdict"] = "success"
                last["waited_sec"] = round(timeout_sec - (deadline - time.monotonic()), 1)
                return last
        except Exception as exc:
            last["read_error"] = str(exc)
        time.sleep(POLL_INTERVAL_SEC)

    last = read_check_status(context, page)
    if not last.get("device_security_success"):
        last["verdict"] = "timeout"
        last["device_security_success"] = False
        last["customer_message"] = CUSTOMER_FAIL_MSG
    last["waited_sec"] = timeout_sec
    return last


def inspect(webdriver_port: int, wait: bool = False, timeout_sec: int = DEFAULT_TIMEOUT_SEC) -> dict:
    ensure_headed_mode()
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(
            f"http://127.0.0.1:{webdriver_port}"
        )
        context = browser.contexts[0]
        page = find_check_page(context)
        if page is None:
            raise RuntimeError("未找到任何标签页")

        info: dict = {"url": page.url, "title": page.title()}

        if wait:
            info.update(wait_device_security_success(context, page, timeout_sec=timeout_sec))
        else:
            info.update(read_check_status(context, page))

        browser.close()
        return info


def main() -> int:
    ensure_headed_mode()
    parser = argparse.ArgumentParser(description="检测站斧设备安全检测是否成功")
    parser.add_argument("--port", type=int, required=True, help="WebDriver CDP 端口")
    parser.add_argument("--wait", action="store_true", help="等待检测通过，超时则失败")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SEC, help="等待超时秒数，默认 15")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    result = inspect(args.port, wait=args.wait, timeout_sec=args.timeout)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.wait and not result.get("device_security_success"):
        print(CUSTOMER_FAIL_MSG, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
