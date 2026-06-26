#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single-file script: attach to Chrome started with --remote-debugging-port=9222
and verify Zhihu login. No other local .py files required.

Requires: Python 3.6+, pip install selenium, and chromedriver on PATH
  (attach mode still uses chromedriver as a bridge)

Install chromedriver (once):
  bash scripts/install_chromedriver.sh
  # or set CHROMEDRIVER_PATH=/path/to/chromedriver

Usage:
  python3 zhihu_attach_standalone.py --check
  python3 zhihu_attach_standalone.py --open-write
  python3 zhihu_attach_standalone.py --publish-test          # fill draft + screenshot, no submit
  python3 zhihu_attach_standalone.py --publish-test --submit # actually click Publish (careful)
"""

import argparse
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime
import urllib.error
import urllib.request

try:
    import selenium
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print("Install selenium: pip3 install selenium", file=sys.stderr)
    sys.exit(1)

DEFAULT_DEBUG_ADDRESS = "127.0.0.1:9222"
ZHIHU_HOME = "https://www.zhihu.com/"
ZHIHU_ME_API = "https://www.zhihu.com/api/v4/me"
ZHIHU_WRITE_URL = "https://www.zhihu.com/creator"
ZHIHU_ARTICLE_WRITE_URL = "https://zhuanlan.zhihu.com/write"
DEFAULT_TEST_TITLE = "[auto-test] Selenium draft (safe to delete)"
DEFAULT_TEST_BODY = "Automated publish test from zhihu_attach_standalone.py — please delete."


def check_debug_port(debug_url):
    try:
        with urllib.request.urlopen(debug_url + "/json/version", timeout=3) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(
            "Cannot connect to %s. Start Chrome with:\n"
            "  bash start_chrome_debug.sh\n"
            "Error: %s" % (debug_url, e)
        )


def list_debug_targets(debug_url):
    with urllib.request.urlopen(debug_url + "/json/list", timeout=3) as resp:
        return json.loads(resp.read().decode())


def _selenium_major_version():
    try:
        return int(selenium.__version__.split(".")[0])
    except Exception:
        return 3


def _chromedriver_from_env_file():
    env_file = os.path.join(os.path.dirname(__file__), "chromedriver.env")
    if not os.path.isfile(env_file):
        return None
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("export CHROMEDRIVER_PATH="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return None


def resolve_chromedriver_path():
    path = os.environ.get("CHROMEDRIVER_PATH")
    if path and os.path.isfile(path) and os.access(path, os.X_OK):
        return path

    path = _chromedriver_from_env_file()
    if path and os.path.isfile(path) and os.access(path, os.X_OK):
        return path

    found = shutil.which("chromedriver")
    if found:
        return found

    home_local = os.path.expanduser("~/.local/bin/chromedriver")
    for candidate in (
        home_local,
        "/usr/local/bin/chromedriver",
        "/usr/bin/chromedriver",
        os.path.join(os.path.dirname(__file__), "chromedriver"),
    ):
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate

    try:
        from webdriver_manager.chrome import ChromeDriverManager
        return ChromeDriverManager().install()
    except Exception:
        pass

    return None


def attach_chrome(debug_address):
    check_debug_port("http://" + debug_address)

    driver_path = resolve_chromedriver_path()
    if not driver_path:
        print(
            "chromedriver not found.\n"
            "Install chromedriver matching your Chrome version, e.g.:\n"
            "  bash scripts/install_chromedriver.sh\n"
            "  export CHROMEDRIVER_PATH=$HOME/.local/bin/chromedriver\n"
            "  bash verify_chrome_stack.sh\n",
            file=sys.stderr,
        )
        sys.exit(1)

    print("Using chromedriver:", driver_path)
    options = Options()
    options.add_experimental_option("debuggerAddress", debug_address)

    major = _selenium_major_version()
    if major >= 4:
        from selenium.webdriver.chrome.service import Service
        return webdriver.Chrome(service=Service(executable_path=driver_path), options=options)

    # Selenium 3.x (Python 3.6 servers often have this)
    return webdriver.Chrome(executable_path=driver_path, options=options)


def find_zhihu_tab(driver):
    current = driver.current_window_handle
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        url = driver.current_url or ""
        if "zhihu.com" in url:
            return handle
    driver.switch_to.window(current)
    return None


def open_zhihu_tab(driver, url=ZHIHU_HOME):
    """Switch to a Zhihu tab if present, then navigate to url (always loads url)."""
    if not find_zhihu_tab(driver):
        if hasattr(driver, "switch_to") and hasattr(driver.switch_to, "new_window"):
            driver.switch_to.new_window("tab")
        else:
            driver.execute_script("window.open('about:blank','_blank');")
            driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)


def verify_login_via_api(driver):
    script = """
        var done = arguments[arguments.length - 1];
        fetch(arguments[0], { credentials: 'include', headers: { 'x-requested-with': 'fetch' } })
            .then(function(res) {
                return res.json().then(function(body) {
                    done({ status: res.status, body: body });
                }).catch(function() { done({ status: res.status, body: null }); });
            })
            .catch(function(err) { done({ status: 0, error: String(err) }); });
    """
    try:
        resp = driver.execute_async_script(script, ZHIHU_ME_API)
    except Exception as e:
        return {"api_ok": False, "error": str(e), "user_name": None}

    status = resp.get("status", 0)
    body = resp.get("body") or {}

    if status == 200 and isinstance(body, dict) and body.get("name"):
        return {
            "api_ok": True,
            "user_name": body.get("name"),
            "user_id": body.get("id") or body.get("url_token"),
        }
    if status == 401:
        return {"api_ok": False, "error": "API 401 — not logged in or session expired", "user_name": None}
    return {
        "api_ok": False,
        "error": "API status %s" % status,
        "user_name": None,
    }


def check_login(driver):
    open_zhihu_tab(driver, ZHIHU_HOME)
    time.sleep(1.5)
    return verify_login_via_api(driver)


def _save_screenshot(driver, prefix="publish"):
    out_dir = os.path.join(os.path.dirname(__file__) or ".", "screenshots")
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(out_dir, "%s_%s.png" % (prefix, ts))
    driver.save_screenshot(path)
    return path


def _element_clickable(el):
    try:
        if not el.is_displayed():
            return False
    except Exception:
        return False
    cls = el.get_attribute("class") or ""
    if "Button--disabled" in cls or " is-disabled" in (" %s " % cls):
        return False
    disabled = el.get_attribute("disabled")
    if disabled is not None and str(disabled).lower() not in ("", "false"):
        return False
    if el.get_attribute("aria-disabled") == "true":
        return False
    try:
        if not el.is_enabled():
            return False
    except Exception:
        pass
    return True


def _js_click(driver, el):
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center', inline:'nearest'});"
        "arguments[0].click();",
        el,
    )


# Zhihu write page (2025–2026): e.g.
# <button class="Button ... Button--primary Button--blue ...">发布</button>
ZHIHU_PUBLISH_BTN_CSS = "button.Button--primary.Button--blue"
ZHIHU_PUBLISH_BTN_XPATH = (
    "//button[contains(@class,'Button--primary') and contains(@class,'Button--blue')"
    " and normalize-space(.)='发布']"
)


def _button_label(el):
    return (el.text or "").strip().replace("\n", "").replace(" ", "")


def _is_exact_zhihu_publish_button(el):
    if _button_label(el) != "发布":
        return False
    cls = el.get_attribute("class") or ""
    return "Button--primary" in cls and "Button--blue" in cls


def _text_is_publish_button(text):
    return _button_label_from_str(text)


def _button_label_from_str(text):
    t = (text or "").replace(" ", "").strip()
    if t != "发布":
        return False
    return True


def _try_fill_publish_form(driver, title, body):
    """Best-effort fill; Zhihu DOM changes often — confirm in VNC."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains

    filled_title = False
    filled_body = False

    title_selectors = [
        "textarea.Input[placeholder*='标题']",
        "textarea[placeholder*='标题']",
        "input[placeholder*='标题']",
        ".WriteIndex-titleInput textarea",
        ".WriteIndex-titleInput input",
    ]
    for sel in title_selectors:
        try:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            if els:
                els[0].clear()
                els[0].send_keys(title)
                filled_title = True
                break
        except Exception:
            pass

    body_selectors = [
        "div.public-DraftEditor-content",
        "div[contenteditable='true']",
        ".DraftEditor-editorContainer div[contenteditable='true']",
    ]
    for sel in body_selectors:
        try:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            if els:
                el = els[0]
                el.click()
                time.sleep(0.3)
                try:
                    ActionChains(driver).click(el).send_keys(body).perform()
                except Exception:
                    el.send_keys(body)
                filled_body = True
                break
        except Exception:
            pass

    if not filled_body:
        try:
            driver.find_element(By.TAG_NAME, "body").send_keys(body)
            filled_body = True
        except Exception:
            pass

    return filled_title, filled_body


def _find_exact_publish_buttons(driver):
    """Only the top-bar 发布: Button--primary + Button--blue + text 发布."""
    from selenium.webdriver.common.by import By

    seen = set()
    out = []

    def add(el):
        if not _is_exact_zhihu_publish_button(el):
            return
        key = id(el)
        if key in seen:
            return
        seen.add(key)
        out.append(el)

    try:
        for el in driver.find_elements(By.XPATH, ZHIHU_PUBLISH_BTN_XPATH):
            add(el)
    except Exception:
        pass
    try:
        for el in driver.find_elements(By.CSS_SELECTOR, ZHIHU_PUBLISH_BTN_CSS):
            add(el)
    except Exception:
        pass
    return out


def _score_publish_button(el):
    """Prefer the real header 发布 (top-right, reasonable size)."""
    score = 0
    if _is_exact_zhihu_publish_button(el):
        score += 1000
    try:
        rect = el.rect
        score += min(int(rect.get("width") or 0), 120)
        y = int(rect.get("y") or 9999)
        if y < 200:
            score += 80
        if y < 80:
            score += 40
    except Exception:
        pass
    if _element_clickable(el):
        score += 200
    return score


def _collect_publish_button_candidates(driver):
    """Exact 发布 first; broad fallbacks only if exact not found."""
    exact = _find_exact_publish_buttons(driver)
    if exact:
        return sorted(exact, key=_score_publish_button, reverse=True)

    from selenium.webdriver.common.by import By
    out = []
    for xp in (
        "//button[contains(normalize-space(.),'发布')]",
        "//span[normalize-space(.)='发布']/ancestor::button[1]",
    ):
        try:
            for el in driver.find_elements(By.XPATH, xp):
                if el.is_displayed():
                    out.append(el)
        except Exception:
            pass
    return out


def _log_publish_button_debug(driver):
    print("DEBUG: exact 发布 buttons (Button--primary.Button--blue):")
    found = _find_exact_publish_buttons(driver)
    if not found:
        print("  (none — page may not be on zhuanlan.zhihu.com/write)")
    for el in found:
        try:
            print(
                "  - text=%r clickable=%s disabled=%s class=%s"
                % (
                    (el.text or "").strip()[:20],
                    _element_clickable(el),
                    el.get_attribute("disabled"),
                    el.get_attribute("class"),
                )
            )
        except Exception:
            pass
    print("DEBUG: other buttons containing 发布:")
    from selenium.webdriver.common.by import By
    for el in driver.find_elements(By.XPATH, "//button[contains(.,'发布')]"):
        try:
            if not el.is_displayed():
                continue
            if _is_exact_zhihu_publish_button(el):
                continue
            print("  - text=%r class=%s" % (
                (el.text or "").strip()[:30],
                (el.get_attribute("class") or "")[:80],
            ))
        except Exception:
            pass


def _wait_publish_button(driver, timeout=45):
    deadline = time.time() + timeout
    while time.time() < deadline:
        candidates = _collect_publish_button_candidates(driver)
        best = None
        best_score = -1
        for el in candidates:
            try:
                if _is_exact_zhihu_publish_button(el):
                    if not _element_clickable(el):
                        continue
                elif _button_label(el) != "发布":
                    continue
                elif not _element_clickable(el):
                    continue
                sc = _score_publish_button(el)
                if sc > best_score:
                    best_score = sc
                    best = el
            except Exception:
                pass
        if best is not None:
            return best
        time.sleep(0.5)
    return None


def _robust_click(driver, el):
    from selenium.webdriver.common.action_chains import ActionChains

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center', inline:'nearest'});", el
    )
    time.sleep(0.2)
    try:
        ActionChains(driver).move_to_element(el).pause(0.1).click(el).perform()
        return
    except Exception:
        pass
    try:
        _js_click(driver, el)
        return
    except Exception:
        pass
    driver.execute_script(
        """
        var el = arguments[0];
        ['pointerdown','mousedown','mouseup','click'].forEach(function(type) {
            el.dispatchEvent(new MouseEvent(type, {bubbles: true, cancelable: true, view: window}));
        });
        """,
        el,
    )


def _try_confirm_publish_dialog(driver):
    """Second step: modal 确认发布 only (avoid random 确认 on page)."""
    from selenium.webdriver.common.by import By

    clicked = False
    xpaths = [
        "//div[contains(@class,'Modal')]//button[normalize-space(.)='确认发布']",
        "//div[@role='dialog']//button[normalize-space(.)='确认发布']",
        "//button[normalize-space(.)='确认发布']",
        "//button[normalize-space(.)='继续发布']",
    ]
    for xp in xpaths:
        try:
            for el in driver.find_elements(By.XPATH, xp):
                if not el.is_displayed():
                    continue
                if not _element_clickable(el):
                    continue
                _js_click(driver, el)
                clicked = True
                time.sleep(1)
        except Exception:
            pass
    return clicked


def _publish_url_ok(driver):
    """
    True only when article is published, NOT draft edit page.
    Draft after auto-save: https://zhuanlan.zhihu.com/p/1234567890/edit
    Published:            https://zhuanlan.zhihu.com/p/1234567890
    """
    url = (driver.current_url or "").split("?")[0].rstrip("/")
    if not url or "/edit" in url:
        return False
    if url.endswith("/write") or "zhuanlan.zhihu.com/write" in url:
        return False
    return bool(re.search(r"zhuanlan\.zhihu\.com/p/\d+$", url)) or bool(
        re.search(r"www\.zhihu\.com/p/\d+$", url)
    )


def _is_draft_edit_page(driver):
    return "/edit" in (driver.current_url or "")


def _complete_publish_flow(driver, max_attempts=5):
    """
    Zhihu often auto-saves to /p/{id}/edit after typing; 发布 must be clicked on that page.
    """
    submit_clicked = False
    published = False

    for attempt in range(1, max_attempts + 1):
        url = driver.current_url or ""
        print("Publish flow %d/%d — URL: %s" % (attempt, max_attempts, url))

        if _publish_url_ok(driver):
            published = True
            break

        if _is_draft_edit_page(driver):
            print("Draft edit page detected (/p/.../edit) — clicking 发布 on this page.")

        if _try_click_publish(driver, wait_timeout=25):
            submit_clicked = True
            time.sleep(2)
            _try_confirm_publish_dialog(driver)
        else:
            print("WARN: 发布 button not found on this attempt.")

        for _ in range(12):
            if _publish_url_ok(driver):
                published = True
                break
            _try_confirm_publish_dialog(driver)
            time.sleep(1)

        if published:
            break
        time.sleep(2)

    return submit_clicked, published


# In-browser find + click (same DOM as VNC). Picks top-right visible
# button.Button--primary.Button--blue with text exactly "发布".
_JS_LIST_PUBLISH_BUTTONS = r"""
return (function() {
  var buttons = Array.from(document.querySelectorAll('button.Button--primary.Button--blue'));
  var out = [];
  for (var i = 0; i < buttons.length; i++) {
    var b = buttons[i];
    var t = (b.innerText || b.textContent || '').replace(/\s+/g, '');
    if (t !== '发布') continue;
    var r = b.getBoundingClientRect();
    var st = window.getComputedStyle(b);
    out.push({
      text: t,
      top: Math.round(r.top), left: Math.round(r.left),
      right: Math.round(r.right), width: Math.round(r.width),
      display: st.display, visibility: st.visibility,
      pointerEvents: st.pointerEvents,
      disabled: !!b.disabled,
      className: b.className
    });
  }
  out.sort(function(a, b) {
    if (Math.abs(a.top - b.top) > 40) return a.top - b.top;
    return b.right - a.right;
  });
  return out;
})();
"""

_JS_CLICK_PUBLISH_BUTTON = r"""
return (function() {
  if (document.activeElement && document.activeElement.blur) {
    try { document.activeElement.blur(); } catch (e) {}
  }
  var buttons = Array.from(document.querySelectorAll('button.Button--primary.Button--blue'));
  var candidates = [];
  for (var i = 0; i < buttons.length; i++) {
    var b = buttons[i];
    var t = (b.innerText || b.textContent || '').replace(/\s+/g, '');
    if (t !== '发布') continue;
    var r = b.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    var st = window.getComputedStyle(b);
    if (st.display === 'none' || st.visibility === 'hidden') continue;
    if (st.pointerEvents === 'none') continue;
    if (b.disabled || b.getAttribute('aria-disabled') === 'true') continue;
    candidates.push({btn: b, top: r.top, right: r.right});
  }
  if (!candidates.length) {
    return {ok: false, error: 'no_clickable_publish', matchedBluePrimary: buttons.length};
  }
  candidates.sort(function(a, b) {
    if (Math.abs(a.top - b.top) > 40) return a.top - b.top;
    return b.right - a.right;
  });
  var pick = candidates[0].btn;
  pick.scrollIntoView({block: 'center', inline: 'nearest'});
  var r = pick.getBoundingClientRect();
  var cx = r.left + r.width / 2;
  var cy = r.top + r.height / 2;
  var topEl = document.elementFromPoint(cx, cy);
  var target = pick;
  if (topEl && topEl !== pick) {
    if (pick.contains(topEl)) target = topEl;
    else if (topEl.closest && topEl.closest('button') === pick) target = topEl;
  }
  ['mouseover', 'mousedown', 'mouseup', 'click'].forEach(function(type) {
    target.dispatchEvent(new MouseEvent(type, {
      bubbles: true, cancelable: true, view: window, clientX: cx, clientY: cy
    }));
  });
  if (typeof pick.click === 'function') pick.click();
  return {
    ok: true,
    className: pick.className,
    top: Math.round(r.top), right: Math.round(r.right),
    width: Math.round(r.width), height: Math.round(r.height),
    candidates: candidates.length,
    hitTag: topEl ? topEl.tagName : null
  };
})();
"""


def _js_list_publish_buttons(driver):
    try:
        return driver.execute_script(_JS_LIST_PUBLISH_BUTTONS) or []
    except Exception as e:
        print("JS list 发布 buttons failed:", e)
        return []


def _js_click_publish(driver):
    try:
        return driver.execute_script(_JS_CLICK_PUBLISH_BUTTON) or {"ok": False}
    except Exception as e:
        print("JS click 发布 failed:", e)
        return {"ok": False, "error": str(e)}


def _try_click_publish(driver, wait_timeout=45):
    """Click the same visible header 发布 as in VNC (JS in page, not wrong Selenium element)."""
    deadline = time.time() + wait_timeout
    last_info = None
    while time.time() < deadline:
        info = _js_click_publish(driver)
        last_info = info
        if info.get("ok"):
            print("JS click 发布 OK:", json.dumps(info, ensure_ascii=False))
            time.sleep(2)
            if _try_confirm_publish_dialog(driver):
                print("Confirm dialog: clicked 确认发布.")
            time.sleep(2)
            return True
        time.sleep(0.5)

    print("JS could not click 发布. Last:", json.dumps(last_info, ensure_ascii=False))
    listed = _js_list_publish_buttons(driver)
    print("All button.Button--primary.Button--blue with text 发布 on page:")
    for row in listed:
        print(" ", json.dumps(row, ensure_ascii=False))
    if not listed:
        print("  (none visible — wrong page or button still disabled)")

    print("Fallback: Selenium element click...")
    el = _wait_publish_button(driver, timeout=8)
    if not el:
        _log_publish_button_debug(driver)
        return False
    print(
        "Selenium 发布: text=%r class=%s"
        % ((el.text or "").strip(), el.get_attribute("class"))
    )
    _robust_click(driver, el)
    time.sleep(2)
    if _try_confirm_publish_dialog(driver):
        print("Confirm dialog: clicked 确认发布.")
    time.sleep(2)
    return True


def run_publish_test(driver, title, body, submit=False, wait_after=5, emit_json=False):
    """
    Open article editor, try to fill title/body, screenshot.
    Default: dry-run (no Publish click). Use submit=True to click 发布.
    """
    open_zhihu_tab(driver, ZHIHU_ARTICLE_WRITE_URL)
    time.sleep(4)

    current = driver.current_url or ""
    print("Editor URL:", current)
    print("Page title:", driver.title)

    if "write" not in current and "creator" not in current and "zhuanlan" not in current:
        print("WARN: may not be on write page; trying creator hub then write again...")
        open_zhihu_tab(driver, ZHIHU_WRITE_URL)
        time.sleep(2)
        open_zhihu_tab(driver, ZHIHU_ARTICLE_WRITE_URL)
        time.sleep(3)
        print("Editor URL:", driver.current_url)

    filled_title, filled_body = _try_fill_publish_form(driver, title, body)
    print("Fill title:", filled_title, "| Fill body:", filled_body)

    shot = _save_screenshot(driver, "publish_test")
    print("Screenshot:", shot)

    if not filled_title or not filled_body:
        print(
            "WARN: could not fill all fields (Zhihu UI may have changed).\n"
            "  Finish the draft manually in VNC, then publish by hand to test."
        )

    submit_clicked = False
    published = False
    submit_error = None

    if submit:
        if not filled_title or not filled_body:
            submit_error = "form_not_filled"
            print(
                "FAIL: title/body not filled — Publish stays disabled on Zhihu.\n"
                "  Fix selectors or fill manually in VNC, then click 发布."
            )
        else:
            print("zhihu publish flow v4 (JS click top-right 发布 on /write and /p/.../edit)")
            print("Waiting for auto-save, then 发布 (write page or /p/.../edit draft page)...")
            time.sleep(3)
            print("URL after fill:", driver.current_url)
            submit_clicked, published = _complete_publish_flow(driver, max_attempts=5)
            print("URL after publish flow:", driver.current_url)
            print("Screenshot after submit:", _save_screenshot(driver, "after_submit"))
            if _is_draft_edit_page(driver) and not published:
                submit_error = "still_on_edit_page"
                print(
                    "FAIL: Still on draft URL (.../edit) — 发布 was not completed.\n"
                    "  In VNC: click the blue 发布 button, or add a topic if required."
                )
            elif not published:
                submit_error = "publish_not_confirmed"
                print(
                    "FAIL: Published URL not detected (need zhuanlan.zhihu.com/p/{id} without /edit).\n"
                    "  Check VNC for confirm dialog or validation errors."
                )
            elif not submit_clicked:
                submit_error = "publish_button_not_found"
                print("FAIL: Could not click 发布. See DEBUG lines above.")

        if submit_error:
            if emit_json:
                print(json.dumps({
                    "ok": False,
                    "submitted": submit_clicked,
                    "published": published,
                    "dry_run": False,
                    "url": driver.current_url,
                    "screenshot": shot,
                    "filled_title": filled_title,
                    "filled_body": filled_body,
                    "error": submit_error,
                }, ensure_ascii=False))
            return 1
    else:
        print(
            "DRY-RUN: draft not submitted.\n"
            "  1) Check VNC: title/body visible in editor\n"
            "  2) To auto-click Publish: add --submit (posts for real)"
        )

    if emit_json:
        ok = True
        if submit:
            ok = submit_clicked and published
        print(json.dumps({
            "ok": ok,
            "submitted": submit_clicked,
            "published": published,
            "dry_run": not submit,
            "url": driver.current_url,
            "screenshot": shot,
            "filled_title": filled_title,
            "filled_body": filled_body,
            "error": submit_error,
        }, ensure_ascii=False))
    return 0 if (not submit or (submit_clicked and published)) else 1


def main():
    if sys.version_info < (3, 6):
        print("Need Python 3.6+. You are using: %s" % sys.version, file=sys.stderr)
        print("Run: python3 zhihu_attach_standalone.py --check", file=sys.stderr)
        return 2

    parser = argparse.ArgumentParser(description="Attach to Chrome and check Zhihu login")
    parser.add_argument("--debug-address", default=DEFAULT_DEBUG_ADDRESS)
    parser.add_argument("--check", action="store_true", help="Verify Zhihu login via API")
    parser.add_argument("--list-tabs", action="store_true", help="List debug targets")
    parser.add_argument("--open-write", action="store_true", help="Open creator hub only")
    parser.add_argument(
        "--publish", "--publish-test",
        dest="publish_test",
        action="store_true",
        help="Open article editor, fill title/body; use --submit to publish",
    )
    parser.add_argument("--title", default=DEFAULT_TEST_TITLE, help="Article title")
    parser.add_argument("--body", default=DEFAULT_TEST_BODY, help="Article body (short text)")
    parser.add_argument(
        "--body-file",
        type=str,
        default=None,
        help="Read body from file (preferred for long posts / OpenClaw)",
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Click Publish (REAL post — use with care)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON result on stdout (last line)",
    )
    parser.add_argument("--quit-browser", action="store_true", help="Close Chrome when done")
    args = parser.parse_args()

    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as f:
            args.body = f.read()

    debug_url = "http://" + args.debug_address

    try:
        info = check_debug_port(debug_url)
        print("Connected to Chrome remote debugging:")
        print("  Browser:", info.get("Browser", info))
    except ConnectionError as e:
        print(e, file=sys.stderr)
        return 2

    if args.list_tabs:
        for i, t in enumerate(list_debug_targets(debug_url), 1):
            title = (t.get("title") or "")[:40]
            print("  [%d] %s | %s | %s" % (i, t.get("type"), title, t.get("url", "")))
        return 0

    if not args.check and not args.open_write and not args.publish_test:
        parser.print_help()
        print("\nTip: --check | --open-write | --publish-test (see --help)")
        return 0

    print("Attaching to Chrome (%s) ..." % args.debug_address)
    driver = attach_chrome(args.debug_address)
    exit_code = 0
    try:
        if args.check:
            result = check_login(driver)
            if result.get("api_ok"):
                if args.json:
                    print(json.dumps({"ok": True, "logged_in": True, **result}))
                else:
                    print("OK Zhihu logged in: %s (id=%s)" % (
                        result.get("user_name"), result.get("user_id")))
            else:
                if args.json:
                    print(json.dumps({"ok": False, "logged_in": False, **result}))
                else:
                    print("FAIL:", result.get("error", result))
                exit_code = 1

        if args.open_write:
            api = check_login(driver)
            if not api.get("api_ok"):
                print("Log in to Zhihu first:", api.get("error"), file=sys.stderr)
                exit_code = 1
            else:
                open_zhihu_tab(driver, ZHIHU_WRITE_URL)
                time.sleep(2)
                current = driver.current_url or ""
                print("URL:", current)
                print("Title:", driver.title)
                if "creator" in current or "zhuanlan" in current or "write" in current:
                    print("OK: creator/write page loaded. Confirm UI in VNC.")
                else:
                    print(
                        "WARN: still not on creator URL (Zhihu may redirect).\n"
                        "  In VNC, manually open: %s" % ZHIHU_WRITE_URL
                    )
                print("dry-run: no auto-publish; only navigation.")

        if args.publish_test:
            print("Using script:", os.path.abspath(__file__))
            api = check_login(driver)
            if not api.get("api_ok"):
                print("Log in to Zhihu first:", api.get("error"), file=sys.stderr)
                exit_code = 1
            else:
                if args.submit:
                    print("WARNING: --submit will try to publish a REAL post.")
                rc = run_publish_test(
                    driver, args.title, args.body,
                    submit=args.submit, emit_json=args.json,
                )
                if rc != 0:
                    exit_code = rc
    finally:
        if args.quit_browser:
            driver.quit()
        else:
            try:
                driver.service.stop()
            except Exception:
                pass
            print("Detached (Chrome stays open).")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
