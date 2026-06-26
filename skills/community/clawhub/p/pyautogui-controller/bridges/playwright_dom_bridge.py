#!/usr/bin/env python3
"""Practical DOM bridge demo for BrowserDOMBackend.

Usage:
    python bridges/playwright_dom_bridge.py '{"action":"click","target_text":"发送","role":"button","url":"https://example.com"}'

Env:
    DOM_BRIDGE_HEADLESS=1                       # optional, default 0
    DOM_BRIDGE_BROWSER=chromium                # chromium|firefox|webkit
    DOM_BRIDGE_STATE=runtime/playwright_bridge_state.json
    DOM_BRIDGE_PROFILE_DIR=runtime/playwright_profile
    DOM_BRIDGE_CDP_URL=http://127.0.0.1:9222   # optional, attach existing chromium session

Requirements:
    pip install playwright
    playwright install chromium
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def emit(success: bool, detail: str = "", selector: Optional[str] = None, **extra):
    payload = {"success": success, "detail": detail, "selector": selector}
    payload.update(extra)
    print(json.dumps(payload, ensure_ascii=False))


def load_state(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(path: Path, data: Dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def choose_browser(playwright, name: str):
    name = (name or "chromium").lower()
    if name == "firefox":
        return playwright.firefox
    if name == "webkit":
        return playwright.webkit
    return playwright.chromium


def normalize_role(role: Optional[str]) -> str:
    return (role or "").lower().replace("elementtype.", "")


def selector_candidates(target_text: Optional[str], role: Optional[str]) -> List[str]:
    candidates = []
    normalized_role = normalize_role(role)
    if target_text and normalized_role == "button":
        candidates.extend([
            "button:has-text('{0}')".format(target_text),
            "[role='button']:has-text('{0}')".format(target_text),
            "input[type='button'][value*='{0}']".format(target_text),
            "input[type='submit'][value*='{0}']".format(target_text),
            "text={0}".format(target_text),
        ])
    elif target_text and normalized_role in ("textbox", "input"):
        candidates.extend([
            "input[placeholder*='{0}']".format(target_text),
            "textarea[placeholder*='{0}']".format(target_text),
            "input[aria-label*='{0}']".format(target_text),
            "textarea[aria-label*='{0}']".format(target_text),
            "label:has-text('{0}') + input".format(target_text),
            "label:has-text('{0}') + textarea".format(target_text),
            "input",
            "textarea",
            "[contenteditable='true']",
        ])
    elif target_text:
        candidates.extend([
            "text={0}".format(target_text),
            "*:has-text('{0}')".format(target_text),
        ])
    else:
        if normalized_role in ("textbox", "input"):
            candidates.extend(["input", "textarea", "[contenteditable='true']"])
        elif normalized_role == "button":
            candidates.extend(["button", "[role='button']", "input[type='button']", "input[type='submit']"])
    deduped = []
    seen = set()
    for item in candidates:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def resolve_target_url(payload: Dict[str, Any], state: Dict[str, Any]) -> str:
    return payload.get("url") or state.get("last_url") or "about:blank"


def connect_browser(playwright, browser_name: str, headless: bool, cdp_url: str, profile_dir: Path):
    browser_type = choose_browser(playwright, browser_name)
    if cdp_url and browser_name.lower() == "chromium":
        browser = browser_type.connect_over_cdp(cdp_url)
        return "cdp", browser, None
    if browser_name.lower() in ("chromium", "firefox"):
        context = browser_type.launch_persistent_context(str(profile_dir), headless=headless)
        return "persistent", None, context
    browser = browser_type.launch(headless=headless)
    return "ephemeral", browser, None


def ensure_page(mode: str, browser, context, target_url: str):
    if mode == "cdp":
        contexts = browser.contexts
        if contexts:
            ctx = contexts[0]
        else:
            ctx = browser.new_context()
        pages = ctx.pages
        page = pages[0] if pages else ctx.new_page()
    elif mode == "persistent":
        ctx = context
        pages = ctx.pages
        page = pages[0] if pages else ctx.new_page()
    else:
        ctx = browser.new_context()
        page = ctx.new_page()
    current = page.url or ""
    if target_url and (current == "about:blank" or current != target_url):
        page.goto(target_url)
    return ctx, page


def locator_strategies(page, target_text: Optional[str], role: Optional[str], selectors: List[str]) -> List[Tuple[str, Any]]:
    strategies = []
    normalized_role = normalize_role(role)
    if target_text:
        if normalized_role == "button":
            try:
                strategies.append(("get_by_role(button)", page.get_by_role("button", name=target_text).first))
            except Exception:
                pass
        if normalized_role in ("textbox", "input"):
            try:
                strategies.append(("get_by_role(textbox)", page.get_by_role("textbox", name=target_text).first))
            except Exception:
                pass
            try:
                strategies.append(("get_by_label", page.get_by_label(target_text).first))
            except Exception:
                pass
            try:
                strategies.append(("get_by_placeholder", page.get_by_placeholder(target_text).first))
            except Exception:
                pass
        try:
            strategies.append(("get_by_text", page.get_by_text(target_text).first))
        except Exception:
            pass
    for selector in selectors:
        try:
            strategies.append((selector, page.locator(selector).first))
        except Exception:
            pass
    return strategies


def locate_first(page, target_text: Optional[str], role: Optional[str], selectors: List[str]):
    attempts = []
    for name, locator in locator_strategies(page, target_text, role, selectors):
        count = 0
        try:
            count = locator.count()
        except Exception:
            count = 0
        attempts.append({"strategy": name, "count": count})
        if count > 0:
            return name, locator, attempts
    return None, None, attempts


def handle_action(action: str, locator, payload: Dict[str, Any]) -> str:
    if action == "locate":
        return "located"
    if action == "click":
        locator.click(timeout=2500)
        return "clicked"
    if action == "focus_input":
        locator.click(timeout=2500)
        return "focused"
    if action == "type_into":
        text = payload.get("text", "")
        locator.click(timeout=2500)
        try:
            locator.fill(text, timeout=2500)
        except Exception:
            locator.type(text, timeout=2500)
        return "typed"
    raise ValueError("unsupported action: {0}".format(action))


def main():
    if len(sys.argv) < 2:
        emit(False, "missing payload")
        return 2

    try:
        payload = json.loads(sys.argv[1])
    except Exception as exc:
        emit(False, "invalid payload: {0}".format(exc))
        return 2

    action = payload.get("action")
    target_text = payload.get("target_text")
    role = payload.get("role")

    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        emit(False, "playwright unavailable: {0}".format(exc), candidates=selector_candidates(target_text, role))
        return 3

    state_path = Path(os.environ.get("DOM_BRIDGE_STATE", "runtime/playwright_bridge_state.json"))
    profile_dir = Path(os.environ.get("DOM_BRIDGE_PROFILE_DIR", "runtime/playwright_profile"))
    state = load_state(state_path)
    headless = os.environ.get("DOM_BRIDGE_HEADLESS", "0") == "1"
    browser_name = os.environ.get("DOM_BRIDGE_BROWSER", "chromium")
    cdp_url = payload.get("cdp_url") or os.environ.get("DOM_BRIDGE_CDP_URL", "")
    target_url = resolve_target_url(payload, state)
    selectors = selector_candidates(target_text, role)

    try:
        with sync_playwright() as p:
            mode, browser, context = connect_browser(p, browser_name, headless, cdp_url, profile_dir)
            ctx, page = ensure_page(mode, browser, context, target_url)
            state["last_url"] = page.url or target_url
            state["last_mode"] = mode
            if cdp_url:
                state["last_cdp_url"] = cdp_url

            strategy_name, locator, attempts = locate_first(page, target_text, role, selectors)
            if locator is None:
                save_state(state_path, state)
                emit(False, "no selector matched", None, url=page.url, candidates=selectors, attempts=attempts, mode=mode)
                return 5

            try:
                detail = handle_action(action, locator, payload)
            except Exception as exc:
                save_state(state_path, state)
                emit(False, "bridge action error: {0}".format(exc), strategy_name, url=page.url, candidates=selectors, attempts=attempts, mode=mode)
                return 6

            save_state(state_path, state)
            emit(True, detail, strategy_name, url=page.url, candidates=selectors, attempts=attempts, mode=mode)
            return 0
    except Exception as exc:
        emit(False, "bridge execution error: {0}".format(exc), None, url=target_url, candidates=selectors, mode="unknown")
        return 7


if __name__ == "__main__":
    raise SystemExit(main())
