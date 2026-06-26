#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Attach to Chrome (127.0.0.1:9222) and publish Xiaohongshu long-form notes (写长文).

Requires: Python 3.6+, selenium, chromedriver (same as zhihu-publish-attach).

Flow: 写长文 -> 新的创作 -> title/body -> 一键排版 -> wait -> 下一步 -> (--submit) 发布

Usage:
  python3 xhs_attach_standalone.py --check --check-creator --json
  python3 xhs_attach_standalone.py --publish --title "标题" --body-file /tmp/xhs_post_body.txt --json
  python3 xhs_attach_standalone.py --publish ... --tags "数码" --submit --json
"""

import argparse
import json
import os
import random
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
XHS_HOME = "https://www.xiaohongshu.com/"
XHS_SELF_API = "https://edith.xiaohongshu.com/api/sns/web/v1/user/selfinfo"
XHS_PUBLISH_URL = (
    "https://creator.xiaohongshu.com/publish/publish?source=official&from=menu"
)
XHS_CREATOR_ORIGIN = "https://creator.xiaohongshu.com"
XHS_TITLE_MAX_LONGFORM = 64
LONGFORM_LAYOUT_WAIT_SEC = 120
HUMAN_PAUSE_MIN = 2.0
HUMAN_PAUSE_MAX = 4.0
HUMAN_TYPE_DELAY_MIN = 0.06
HUMAN_TYPE_DELAY_MAX = 0.14


def _human_pause(reason=""):
    sec = random.uniform(HUMAN_PAUSE_MIN, HUMAN_PAUSE_MAX)
    if reason:
        print("Wait %.1fs — %s" % (round(sec, 1), reason), flush=True)
    time.sleep(sec)


def _human_type_keys(element, text):
    """Type text in small chunks with random delays (human-like)."""
    if not text:
        return
    i = 0
    n = len(text)
    while i < n:
        chunk_len = min(random.randint(1, 4), n - i)
        element.send_keys(text[i : i + chunk_len])
        i += chunk_len
        time.sleep(random.uniform(HUMAN_TYPE_DELAY_MIN, HUMAN_TYPE_DELAY_MAX))


def check_debug_port(debug_url):
    try:
        with urllib.request.urlopen(debug_url + "/json/version", timeout=3) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(
            "Cannot connect to %s. Start Chrome with:\n"
            "  bash dev/mac/start_chrome_debug.sh --detach\n"
            "Error: %s" % (debug_url, e)
        )


def list_debug_targets(debug_url):
    with urllib.request.urlopen(debug_url + "/json/list", timeout=3) as resp:
        return json.loads(resp.read().decode())


def ensure_debug_page(debug_url, fallback_url=XHS_HOME):
    """Chromedriver attach needs at least one open page tab."""
    pages = [t for t in list_debug_targets(debug_url) if t.get("type") == "page"]
    if pages:
        return len(pages)
    new_endpoint = debug_url.rstrip("/") + "/json/new?" + fallback_url
    req = urllib.request.Request(new_endpoint, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(
            "Chrome on %s has no open tabs and failed to open one.\n"
            "Open the debug Chrome window and keep at least one tab, or restart:\n"
            "  bash dev/mac/start_chrome_debug.sh --detach\n"
            "Error: %s" % (debug_url, e)
        )
    time.sleep(0.8)
    return 1


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
    for candidate in (home_local, "/usr/local/bin/chromedriver", "/usr/bin/chromedriver"):
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def attach_chrome(debug_address):
    debug_url = "http://" + debug_address
    check_debug_port(debug_url)
    pages = ensure_debug_page(debug_url)
    if pages < 1:
        print("No Chrome page tabs available on %s" % debug_address, file=sys.stderr)
        sys.exit(1)

    driver_path = resolve_chromedriver_path()
    if not driver_path:
        print(
            "chromedriver not found. Run: bash scripts/install_chromedriver.sh",
            file=sys.stderr,
        )
        sys.exit(1)
    print("Using chromedriver:", driver_path)
    options = Options()
    options.add_experimental_option("debuggerAddress", debug_address)
    major = _selenium_major_version()
    if major >= 4:
        from selenium.webdriver.chrome.service import Service
        from selenium.common.exceptions import SessionNotCreatedException
        try:
            return webdriver.Chrome(
                service=Service(executable_path=driver_path), options=options,
            )
        except SessionNotCreatedException as e:
            if "unable to discover open pages" in str(e).lower():
                ensure_debug_page(debug_url)
                return webdriver.Chrome(
                    service=Service(executable_path=driver_path), options=options,
                )
            raise
    return webdriver.Chrome(executable_path=driver_path, options=options)


def _tab_url_score(url, prefer_creator=False):
    u = url or ""
    if u in ("about:blank", "chrome://newtab/"):
        return -100
    if "creator.xiaohongshu.com" in u:
        return 100 if prefer_creator else 60
    if "www.xiaohongshu.com" in u:
        return 80 if not prefer_creator else 40
    if "xiaohongshu.com" in u:
        return 30
    return 0


def _list_xhs_tabs(driver):
    current = driver.current_window_handle
    tabs = []
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        url = driver.current_url or ""
        if "xiaohongshu.com" in url:
            tabs.append((handle, url))
    try:
        driver.switch_to.window(current)
    except Exception:
        pass
    return tabs


def focus_best_tab(driver, prefer_creator=False, log=True):
    """Chromedriver attach often leaves the active tab on about:blank — fix before any JS."""
    best_handle = None
    best_url = ""
    best_score = -999
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        url = driver.current_url or ""
        score = _tab_url_score(url, prefer_creator=prefer_creator)
        if score > best_score:
            best_score = score
            best_handle = handle
            best_url = url
    if best_handle and best_score >= 0:
        driver.switch_to.window(best_handle)
        if log:
            print("Active tab: %s" % best_url[:110], flush=True)
        return best_handle, best_url
    return None, best_url


def find_xhs_tab(driver, prefer_creator=False):
    tabs = _list_xhs_tabs(driver)
    if not tabs:
        return None
    best = max(tabs, key=lambda item: _tab_url_score(item[1], prefer_creator=prefer_creator))
    driver.switch_to.window(best[0])
    return best[0]


def open_xhs_tab(driver, url):
    want_creator = "creator.xiaohongshu.com" in url
    tabs = _list_xhs_tabs(driver)
    target = None
    if want_creator:
        for handle, tab_url in tabs:
            if "creator.xiaohongshu.com" in tab_url:
                target = handle
                break
    else:
        for handle, tab_url in tabs:
            if "www.xiaohongshu.com" in tab_url:
                target = handle
                break
    if not target and tabs:
        target = tabs[0][0]
    if not target:
        if hasattr(driver, "switch_to") and hasattr(driver.switch_to, "new_window"):
            driver.switch_to.new_window("tab")
        else:
            driver.execute_script("window.open('about:blank','_blank');")
            driver.switch_to.window(driver.window_handles[-1])
    else:
        driver.switch_to.window(target)
    cur = driver.current_url or ""
    if want_creator and "creator.xiaohongshu.com" in cur and url.split("?")[0] in cur:
        return
    driver.get(url)


def verify_login_via_dom(driver):
    """Detect www.xiaohongshu.com login from page DOM (API fetch often returns 406)."""
    script = """
    var me = Array.from(document.querySelectorAll('a')).find(function(a) {
      return (a.innerText || '').trim() === '我' && (a.href || '').indexOf('/user/profile/') >= 0;
    });
    var hasLoginBtn = !!Array.from(document.querySelectorAll('button,a,span')).find(function(el) {
      var t = (el.innerText || '').trim();
      return t === '登录' || t === '登 录';
    });
    var hasA1 = document.cookie.indexOf('a1=') >= 0;
    var href = me ? me.getAttribute('href') : '';
    var userId = '';
    var m = href.match(/\\/user\\/profile\\/([a-f0-9]+)/i);
    if (m) userId = m[1];
    var loggedIn = !!(me && !hasLoginBtn && hasA1);
    return {
      api_ok: loggedIn,
      user_name: loggedIn ? '我' : null,
      user_id: userId || null,
      method: 'dom',
      has_login_button: hasLoginBtn,
    };
    """
    try:
        return driver.execute_script(script) or {
            "api_ok": False, "error": "dom_check_empty", "user_name": None,
        }
    except Exception as e:
        return {"api_ok": False, "error": str(e), "user_name": None}


def verify_login_via_api(driver):
    script = """
        var done = arguments[arguments.length - 1];
        fetch(arguments[0], { credentials: 'include', headers: { 'x-requested-with': 'XMLHttpRequest' } })
            .then(function(res) {
                return res.json().then(function(body) {
                    done({ status: res.status, body: body });
                }).catch(function() { done({ status: res.status, body: null }); });
            })
            .catch(function(err) { done({ status: 0, error: String(err) }); });
    """
    try:
        resp = driver.execute_async_script(script, XHS_SELF_API)
    except Exception as e:
        return {"api_ok": False, "error": str(e), "user_name": None}

    status = resp.get("status", 0)
    body = resp.get("body") or {}
    data = body.get("data") if isinstance(body, dict) else None
    if status == 200 and isinstance(data, dict):
        name = data.get("nickname") or data.get("nick_name") or data.get("user_name")
        if name:
            return {"api_ok": True, "user_name": name, "user_id": data.get("user_id"), "method": "api"}
    if status == 406:
        return {"api_ok": False, "error": "API 406 — anti-bot signature required (not logout)", "user_name": None, "method": "api"}
    if "login" in (driver.current_url or "").lower():
        return {"api_ok": False, "error": "redirected to login", "user_name": None}
    return {"api_ok": False, "error": "API status %s" % status, "user_name": None, "method": "api"}


def verify_creator_access(driver):
    """Creator publish needs creator.xiaohongshu.com session (separate from www login)."""
    current = driver.current_url or ""
    open_xhs_tab(driver, XHS_PUBLISH_URL)
    time.sleep(2.5)
    url = driver.current_url or ""
    if "login" in url.lower():
        return {
            "creator_ok": False,
            "error": "creator_not_logged_in — log in at https://creator.xiaohongshu.com (www login not required)",
            "url": url,
        }
    return {"creator_ok": True, "url": url}


def check_creator_ready(driver):
    """Long-form publish only needs creator.xiaohongshu.com (not www.xiaohongshu.com)."""
    creator = verify_creator_access(driver)
    ok = bool(creator.get("creator_ok"))
    return {
        "api_ok": ok,
        "creator_ok": ok,
        "user_name": None,
        "user_id": None,
        "method": "creator_publish_url",
        "error": None if ok else creator.get("error"),
        "url": creator.get("url"),
    }


def check_login(driver, check_creator=False):
    """Optional www login check. Publishing uses check_creator_ready() instead."""
    if check_creator:
        return check_creator_ready(driver)
    open_xhs_tab(driver, XHS_HOME)
    time.sleep(1.5)
    result = verify_login_via_dom(driver)
    if not result.get("api_ok"):
        api = verify_login_via_api(driver)
        if api.get("api_ok"):
            result = api
        elif not result.get("error"):
            result["error"] = api.get("error")
    return result


def _save_screenshot(driver, prefix="xhs"):
    out_dir = os.path.join(os.path.dirname(__file__) or ".", "screenshots")
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(out_dir, "%s_%s.png" % (prefix, ts))
    driver.save_screenshot(path)
    return path


def _normalize_tags(tags_str):
    if not tags_str:
        return []
    parts = re.split(r"[,，\s#]+", tags_str.strip())
    return [p.strip() for p in parts if p.strip()]


def _append_tags_to_body(body, tags):
    if not tags:
        return body
    suffix = "\n\n" + " ".join("#" + t for t in tags)
    if suffix.strip() in body:
        return body
    return body.rstrip() + suffix


def _js_find_by_texts(driver, labels, partial=False, pick="bottom"):
    """Locate a visible control by label without clicking."""
    payload = {"labels": labels, "partial": partial, "pick": pick}
    script = r"""
    var cfg = arguments[0];
    var labels = cfg.labels || [];
    var partial = !!cfg.partial;
    var pickMode = cfg.pick || 'bottom';
    function norm(t) { return (t || '').replace(/\s+/g, ' ').trim(); }
    function match(t) {
      for (var i = 0; i < labels.length; i++) {
        var want = labels[i];
        if (partial) {
          if (t.indexOf(want) >= 0) return true;
        } else if (t === want) return true;
      }
      return false;
    }
    var nodes = Array.from(document.querySelectorAll(
      'button, [role="button"], a, div, span, p'
    ));
    var candidates = [];
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var t = norm(el.innerText || el.textContent);
      if (!t || t.length > 40) continue;
      if (!match(t)) continue;
      var r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) continue;
      var st = window.getComputedStyle(el);
      if (st.display === 'none' || st.visibility === 'hidden' || st.opacity === '0') continue;
      if (el.disabled || el.getAttribute('aria-disabled') === 'true') continue;
      var clickable = el;
      if (el.tagName === 'SPAN' || el.tagName === 'P' || el.tagName === 'DIV') {
        var parent = el.closest('button, [role="button"], a');
        if (parent) clickable = parent;
      }
      var cr = clickable.getBoundingClientRect();
      candidates.push({top: cr.top, bottom: cr.bottom, left: cr.left, text: t});
    }
    if (!candidates.length) return {ok: false, error: 'not_found', labels: labels};
    candidates.sort(function(a, b) {
      if (pickMode === 'bottom') {
        if (Math.abs(a.bottom - b.bottom) > 20) return b.bottom - a.bottom;
        return b.left - a.left;
      }
      if (Math.abs(a.top - b.top) > 30) return a.top - b.top;
      return a.left - b.left;
    });
    return {
      ok: true, text: candidates[0].text, count: candidates.length,
      picked_bottom: Math.round(candidates[0].bottom), pick: pickMode
    };
    """
    try:
        return driver.execute_script(script, payload) or {"ok": False}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _js_click_by_texts(driver, labels, partial=False, pick="bottom"):
    """Click a visible button-like element whose text matches one of labels.

    pick=bottom: footer actions (下一步 / 一键排版) — page often has multiple matches.
    pick=top: header / menu items.
    """
    payload = {"labels": labels, "partial": partial, "pick": pick}
    script = r"""
    var cfg = arguments[0];
    var labels = cfg.labels || [];
    var partial = !!cfg.partial;
    var pickMode = cfg.pick || 'bottom';
    function norm(t) { return (t || '').replace(/\s+/g, ' ').trim(); }
    function match(t) {
      for (var i = 0; i < labels.length; i++) {
        var want = labels[i];
        if (partial) {
          if (t.indexOf(want) >= 0) return true;
        } else if (t === want) return true;
      }
      return false;
    }
    var nodes = Array.from(document.querySelectorAll(
      'button, [role="button"], a, div, span, p'
    ));
    var candidates = [];
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var t = norm(el.innerText || el.textContent);
      if (!t || t.length > 40) continue;
      if (!match(t)) continue;
      var r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) continue;
      var st = window.getComputedStyle(el);
      if (st.display === 'none' || st.visibility === 'hidden' || st.opacity === '0') continue;
      if (el.disabled || el.getAttribute('aria-disabled') === 'true') continue;
      var clickable = el;
      if (el.tagName === 'SPAN' || el.tagName === 'P' || el.tagName === 'DIV') {
        var parent = el.closest('button, [role="button"], a');
        if (parent) clickable = parent;
      }
      var cr = clickable.getBoundingClientRect();
      candidates.push({el: clickable, top: cr.top, bottom: cr.bottom, left: cr.left, text: t});
    }
    if (!candidates.length) return {ok: false, error: 'not_found', labels: labels};
    candidates.sort(function(a, b) {
      if (pickMode === 'bottom') {
        if (Math.abs(a.bottom - b.bottom) > 20) return b.bottom - a.bottom;
        return b.left - a.left;
      }
      if (Math.abs(a.top - b.top) > 30) return a.top - b.top;
      return a.left - b.left;
    });
    var pick = candidates[0].el;
    pick.scrollIntoView({block: 'center', inline: 'nearest'});
    var r = pick.getBoundingClientRect();
    var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    ['mouseover','mousedown','mouseup','click'].forEach(function(type) {
      pick.dispatchEvent(new MouseEvent(type, {bubbles: true, cancelable: true, view: window, clientX: cx, clientY: cy}));
    });
    if (typeof pick.click === 'function') pick.click();
    return {
      ok: true, text: candidates[0].text, count: candidates.length,
      picked_bottom: Math.round(candidates[0].bottom), pick: pickMode
    };
    """
    try:
        return driver.execute_script(script, payload) or {"ok": False}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _human_click_retry(driver, labels, partial=False, timeout=30, interval=0.8, pick="bottom"):
    """Wait until control exists, pause 2–4s, then click (human-like)."""
    deadline = time.time() + timeout
    last = {"ok": False}
    label = labels[0] if labels else ""
    while time.time() < deadline:
        last = _js_find_by_texts(driver, labels, partial=partial, pick=pick)
        if last.get("ok"):
            _human_pause("点击「%s」前" % label)
            clicked = _js_click_by_texts(driver, labels, partial=partial, pick=pick)
            if clicked.get("ok"):
                _human_pause("点击「%s」后" % label)
            return clicked
        time.sleep(interval)
    return last


def _wait_longform_body_editor(driver, timeout=45):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            ok = driver.execute_script(
                """
                var bestA = 0, found = false;
                document.querySelectorAll(
                  '.tiptap.ProseMirror,.ProseMirror,[contenteditable="true"]'
                ).forEach(function(el) {
                  var r = el.getBoundingClientRect();
                  if (r.width < 80 || r.height < 24) return;
                  var a = r.width * r.height;
                  if (a > bestA) { bestA = a; found = true; }
                });
                return found;
                """
            )
            if ok:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def _fill_longform_body_best_effort(driver, body):
    """Insert body via execCommand (faster than send_keys on Linux)."""
    try:
        r = driver.execute_script(
            """
            var text = arguments[0];
            var best = null, bestA = 0;
            document.querySelectorAll(
              '.tiptap.ProseMirror,.ProseMirror,[contenteditable="true"]'
            ).forEach(function(el) {
              var r = el.getBoundingClientRect();
              if (r.width < 80 || r.height < 24) return;
              var a = r.width * r.height;
              if (a > bestA) { bestA = a; best = el; }
            });
            if (!best) return {ok: false, error: 'no_editor'};
            best.focus();
            best.click();
            try { document.execCommand('selectAll', false, null); } catch (e) {}
            try { document.execCommand('delete', false, null); } catch (e) {}
            document.execCommand('insertText', false, text);
            return {ok: true, via: 'execCommand-insertText'};
            """,
            body,
        )
        return bool(r and r.get("ok"))
    except Exception as exc:
        print("WARN: JS body fill: %s" % exc, flush=True)
        return False


def _fill_longform_fields(driver, title, body):
    """Best-effort fill title/body. No DOM verify."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

    title = (title or "")[:XHS_TITLE_MAX_LONGFORM]
    body = body or ""
    out = {"filled_title": False, "filled_body": False}

    _human_pause("填写标题前")
    for sel in ("input[placeholder*='标题']", "textarea[placeholder*='标题']", "input.d-text"):
        try:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            if els and els[0].is_displayed():
                el = els[0]
                el.click()
                time.sleep(0.3)
                el.send_keys(Keys.CONTROL, "a")
                time.sleep(0.15)
                el.send_keys(Keys.BACKSPACE)
                time.sleep(0.2)
                _human_type_keys(el, title)
                out["filled_title"] = True
                break
        except Exception:
            pass

    _human_pause("填写正文前")
    if body and _fill_longform_body_best_effort(driver, body):
        out["filled_body"] = True
    else:
        for sel in (
            "div.tiptap.ProseMirror",
            "div.ProseMirror[contenteditable='true']",
            "div[contenteditable='true']",
        ):
            try:
                els = driver.find_elements(By.CSS_SELECTOR, sel)
                for el in els:
                    if not el.is_displayed():
                        continue
                    r = el.rect
                    if r.get("width", 0) < 120 or r.get("height", 0) < 24:
                        continue
                    el.click()
                    time.sleep(0.4)
                    try:
                        el.send_keys(Keys.CONTROL, "a")
                        time.sleep(0.15)
                        el.send_keys(Keys.BACKSPACE)
                        time.sleep(0.2)
                    except Exception:
                        pass
                    _human_type_keys(el, body)
                    out["filled_body"] = True
                    break
                if out["filled_body"]:
                    break
            except Exception:
                pass

    _human_pause("填写完成")
    return out


def _page_has_text(driver, text):
    try:
        return bool(driver.execute_script(
            "return (document.body && (document.body.innerText || '').indexOf(arguments[0]) >= 0);",
            text,
        ))
    except Exception:
        return False


def _wait_longform_layout_ready(driver, timeout=LONGFORM_LAYOUT_WAIT_SEC):
    """After 一键排版, wait until 下一步 / 版式选择 / 预览底栏出现。"""
    deadline = time.time() + timeout
    last = {}
    while time.time() < deadline:
        last = driver.execute_script(_JS_XHS_PUBLISH_HELPERS + r"""
            var body = document.body.innerText || '';
            var loading = document.querySelector(
              '.el-loading-mask:not([style*="display: none"])'
            );
            var loadingVisible = false;
            if (loading) {
              var lr = loading.getBoundingClientRect();
              loadingVisible = lr.width > 40 && lr.height > 40;
            }
            var templates = document.querySelectorAll(
              '[class*="template"], [class*="layout"], [class*="style-card"]'
            ).length;
            return {
              next_exact: xhsExactVisibleText('下一步'),
              next_bottom: xhsLiveBottomExact('下一步'),
              preview: xhsPreviewStrictEntered(),
              templates: templates,
              layout_done_text: body.indexOf('排版完成') >= 0
                || body.indexOf('选择版式') >= 0
                || body.indexOf('选择模板') >= 0,
              loading: loadingVisible
            };
        """) or {}
        if last.get("preview"):
            print("Layout wait: preview footer already visible.", flush=True)
            return True
        if last.get("next_bottom") or last.get("next_exact"):
            if not last.get("loading"):
                print("Layout wait: 下一步 ready.", flush=True)
                return True
        if last.get("layout_done_text") or (last.get("templates") or 0) >= 3:
            print("Layout wait: template picker visible.", flush=True)
            return True
        elapsed = int(timeout - (deadline - time.time()))
        if elapsed > 0 and elapsed % 15 == 0:
            print(
                "Layout still waiting (%ss): %s"
                % (elapsed, json.dumps(last, ensure_ascii=False)),
                flush=True,
            )
        time.sleep(1.5)
    print(
        "Layout timeout after %ss: %s"
        % (timeout, json.dumps(last, ensure_ascii=False)),
        flush=True,
    )
    return False


def _enter_longform_editor(driver):
    """写长文 -> 新的创作."""
    steps = []
    focus_best_tab(driver, prefer_creator=True)
    open_xhs_tab(driver, XHS_PUBLISH_URL)
    _human_pause("打开发布页后")
    steps.append({"navigate": driver.current_url})

    if "login" in (driver.current_url or "").lower():
        return False, "not_logged_in", steps

    r1 = _human_click_retry(driver, ["写长文"], timeout=25, pick="top")
    steps.append({"click_写长文": r1})
    if not r1.get("ok"):
        return False, "click_写长文_failed", steps

    r2 = _human_click_retry(driver, ["新的创作", "新建创作"], timeout=25, pick="top")
    steps.append({"click_新的创作": r2})
    if not r2.get("ok"):
        return False, "click_新的创作_failed", steps
    _human_pause("进入编辑器后")
    if not _wait_longform_body_editor(driver, timeout=25):
        print("WARN: body editor not visible yet (will still try fill)", flush=True)
    return True, None, steps


_JS_XHS_PUBLISH_HELPERS = r"""
function xhsNorm(t) { return (t || '').replace(/\s+/g, ' ').trim(); }
function xhsIsPublishLabel(t) { return t === '发布' || t === '发 布'; }
function xhsIsSaveLeaveLabel(t) {
  var n = xhsNorm(t);
  return n === '暂存离开' || n.indexOf('暂存离开') >= 0;
}
function xhsVisible(el) {
  if (!el || !el.getBoundingClientRect) return false;
  var r = el.getBoundingClientRect();
  if (r.width < 36 || r.height < 18) return false;
  var st = window.getComputedStyle(el);
  return st.display !== 'none' && st.visibility !== 'hidden' && st.opacity !== '0';
}
function xhsExactVisibleText(text) {
  var nodes = document.querySelectorAll('button, [role="button"], a, span, div');
  for (var i = 0; i < nodes.length; i++) {
    var el = nodes[i];
    var t = xhsNorm(el.innerText || el.textContent);
    if (t !== text) continue;
    if (!xhsVisible(el)) continue;
    if (el.disabled || el.getAttribute('aria-disabled') === 'true') continue;
    return true;
  }
  return false;
}
function xhsDeepEachRoot(root, fn) {
  if (!root) return false;
  if (fn(root) === true) return true;
  var all = root.querySelectorAll ? root.querySelectorAll('*') : [];
  for (var i = 0; i < all.length; i++) {
    if (all[i].shadowRoot && xhsDeepEachRoot(all[i].shadowRoot, fn)) return true;
  }
  return false;
}
function xhsDeepListCeBtns() {
  var list = [];
  function scan(root) {
    if (!root || !root.querySelectorAll) return;
    root.querySelectorAll('button, [class*="ce-btn"]').forEach(function(el) {
      var cls = String(el.className || '');
      if (cls.indexOf('ce-btn') < 0) return;
      if (!xhsVisible(el)) return;
      var r = el.getBoundingClientRect();
      list.push({
        text: xhsNorm(el.innerText || el.textContent).slice(0, 12),
        cls: cls.slice(0, 50),
        top: Math.round(r.top),
        left: Math.round(r.left)
      });
    });
    root.querySelectorAll('*').forEach(function(el) {
      if (el.shadowRoot) scan(el.shadowRoot);
    });
  }
  scan(document);
  return list;
}
function xhsLiveBottomExact(text) {
  var vh = window.innerHeight || 800, vw = window.innerWidth || 1200;
  var nodes = document.querySelectorAll('button, [role="button"], span, div');
  for (var i = 0; i < nodes.length; i++) {
    var el = nodes[i];
    if (xhsNorm(el.innerText || el.textContent) !== text) continue;
    if (!xhsVisible(el)) continue;
    var r = el.getBoundingClientRect();
    if (r.top < vh * 0.45 || r.left < vw * 0.2) continue;
    return true;
  }
  return false;
}
function xhsNodeVisible(node) {
  if (!node || !node.parentElement) return false;
  var p = node.parentElement;
  var st = window.getComputedStyle(p);
  if (st.display === 'none' || st.visibility === 'hidden' || parseFloat(st.opacity) === 0) return false;
  var r = p.getBoundingClientRect();
  return r.width > 1 && r.height > 1;
}
function xhsLiveVisibleText(text) {
  if (!document.body) return false;
  var tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  while (tw.nextNode()) {
    var n = tw.currentNode;
    if ((n.textContent || '').indexOf(text) < 0) continue;
    if (xhsNodeVisible(n)) return true;
  }
  return false;
}
function xhsFindPublishBtn(doc) {
  doc = doc || document;
  if (!doc.querySelector) return null;
  return doc.querySelector('xhs-publish-btn');
}
function xhsPublishBtnReady(el) {
  if (!el || !xhsVisible(el)) return false;
  var save = el.getAttribute('save-text') || '';
  var submit = xhsNorm(el.getAttribute('submit-text') || '');
  if (save.indexOf('暂存离开') < 0) return false;
  if (!xhsIsPublishLabel(submit)) return false;
  var r = el.getBoundingClientRect();
  var vh = window.innerHeight || 800;
  if (r.top < vh * 0.2) return false;
  return true;
}
function xhsFindSaveLeaveInDoc(doc) {
  var pb = xhsFindPublishBtn(doc);
  if (pb && xhsPublishBtnReady(pb)) return pb;
  return null;
}
function xhsPreviewStrictEntered() {
  return xhsPublishBtnReady(xhsFindPublishBtn(document));
}
function xhsPreviewEntered() {
  return xhsPreviewStrictEntered();
}
function xhsGeneratingVisible() {
  var vh = window.innerHeight || 800;
  var hit = false;
  document.querySelectorAll('div, span, p').forEach(function(el) {
    if (hit) return;
    var t = xhsNorm(el.innerText || el.textContent);
    if (t.indexOf('笔记图片生成中') < 0) return;
    var r = el.getBoundingClientRect();
    if (r.width < 80 || r.height < 14) return;
    if (r.top > vh * 0.25) return;
    hit = true;
  });
  return hit;
}
function xhsFindFinalPublishEl() {
  var el = xhsFindPublishBtn(document);
  if (el && xhsPublishBtnReady(el)) {
    var r = el.getBoundingClientRect();
    return {el: el, via: 'xhs-publish-btn', bottom: r.bottom, left: r.left};
  }
  return null;
}
function xhsFindPublishSubmitBtn(doc) {
  doc = doc || document;
  if (!doc.querySelector) return null;
  return doc.querySelector('xhs-publish-btn[submit-text="发布"]')
    || doc.querySelector('xhs-publish-btn[submit-text="发 布"]')
    || doc.querySelector('xhs-publish-btn');
}
function xhsClickNode(el, cx, cy) {
  if (!el) return;
  ['pointerover','pointerdown','mousedown','mouseup','pointerup','click'].forEach(function(type) {
    el.dispatchEvent(new MouseEvent(type, {
      bubbles: true, composed: true, cancelable: true, view: window,
      clientX: cx, clientY: cy, buttons: 1, detail: 1
    }));
  });
  if (typeof el.click === 'function') el.click();
}
function xhsFindSubmitClickTarget(host) {
  if (!host) return null;
  var hostR = host.getBoundingClientRect();
  var best = null, bestScore = -1;
  host.querySelectorAll('*').forEach(function(node) {
    var t = xhsNorm(node.innerText || node.textContent);
    var cls = String(node.className || '');
    var r = node.getBoundingClientRect();
    if (r.width < 20 || r.height < 16) return;
    var score = r.width * r.height;
    if (t === '发布' || t === '发 布') score += 5000;
    if (cls.indexOf('bg-red') >= 0) score += 4000;
    if (cls.indexOf('ce-btn') >= 0) score += 2000;
    if (r.left > hostR.left + hostR.width * 0.45) score += 1500;
    if (score > bestScore) { bestScore = score; best = node; }
  });
  return best;
}
function xhsProbePublishBtn() {
  var el = xhsFindPublishSubmitBtn(document);
  if (!el) return {found: false};
  var kids = [];
  el.querySelectorAll('*').forEach(function(node) {
    var r = node.getBoundingClientRect();
    if (r.width < 8 || r.height < 8) return;
    kids.push({
      tag: node.tagName,
      cls: String(node.className || '').slice(0, 50),
      text: xhsNorm(node.innerText || node.textContent).slice(0, 16),
      left: Math.round(r.left), top: Math.round(r.top), w: Math.round(r.width)
    });
  });
  var r = el.getBoundingClientRect();
  return {
    found: true, hasShadow: !!el.shadowRoot, child_count: kids.length,
    children: kids.slice(0, 20), rect: {left: Math.round(r.left), top: Math.round(r.top),
      w: Math.round(r.width), h: Math.round(r.height)}
  };
}
function xhsClickPublishSubmit() {
  var el = xhsFindPublishSubmitBtn(document);
  if (!el) return {ok: false, error: 'no_xhs_publish_submit_btn'};
  if ((el.getAttribute('submit-disabled') || '').toString() === 'true') {
    return {ok: false, error: 'submit_disabled'};
  }
  el.scrollIntoView({block: 'center', inline: 'nearest'});
  el.focus();
  var inner = xhsFindSubmitClickTarget(el);
  var target = inner || el;
  var r = target.getBoundingClientRect();
  var cx = r.left + r.width / 2;
  var cy = r.top + r.height / 2;
  xhsClickNode(target, cx, cy);
  if (target !== el) {
    var hr = el.getBoundingClientRect();
    xhsClickNode(el, hr.left + hr.width * 0.82, hr.top + hr.height * 0.5);
  }
  try {
    el.dispatchEvent(new CustomEvent('submit', {bubbles: true, composed: true, cancelable: true}));
  } catch (e) {}
  return {
    ok: true,
    text: xhsNorm(el.getAttribute('submit-text')) || '发布',
    via: inner ? 'composed-click-inner' : 'composed-click-host',
    picked_bottom: Math.round(r.bottom),
    picked_left: Math.round(r.left),
    hit: 'xhs-publish-btn-closed-shadow',
    probe: xhsProbePublishBtn()
  };
}
"""

_JS_PREVIEW_STATE = _JS_XHS_PUBLISH_HELPERS + r"""
return (function() {
  var pb = xhsFindPublishBtn(document);
  var found = xhsFindFinalPublishEl();
  return {
    preview_entered: xhsPreviewStrictEntered(),
    preview_strict: xhsPreviewStrictEntered(),
    xhs_publish_btn: !!pb,
    save_text: pb ? (pb.getAttribute('save-text') || '') : '',
    submit_text: pb ? (pb.getAttribute('submit-text') || '') : '',
    submit_disabled: pb ? (pb.getAttribute('submit-disabled') || '') : '',
    save_leave_dom: !!pb,
    generating_visible: xhsGeneratingVisible(),
    publish_ready: !!found,
    via: found ? found.via : '',
    picked_bottom: found ? Math.round(found.bottom) : 0,
    picked_left: found ? Math.round(found.left) : 0
  };
})();
"""

_JS_CLICK_FINAL_PUBLISH = _JS_XHS_PUBLISH_HELPERS + r"""
return (function() {
  if (!xhsPreviewStrictEntered()) {
    return {ok: false, error: 'preview_page_not_entered'};
  }
  return xhsClickPublishSubmit();
})();
"""

_JS_CDP_CLICK_BOTTOM_PUBLISH = _JS_XHS_PUBLISH_HELPERS + r"""
return (function() {
  var vw = window.innerWidth, vh = window.innerHeight;
  var x = vw * 0.5, y = vh - 58;
  var el = document.elementFromPoint(x, y);
  if (!el) return {ok: false, error: 'elementFromPoint_miss'};
  var node = el;
  for (var i = 0; i < 8 && node; i++) {
    var t = xhsNorm(node.innerText || node.textContent);
    var cls = String(node.className || '');
    if (xhsIsPublishLabel(t) || cls.indexOf('bg-red') >= 0) {
      var r = node.getBoundingClientRect();
      var cx = r.left + r.width/2, cy = r.top + r.height/2;
      ['mouseover','mousedown','mouseup','click'].forEach(function(type) {
        node.dispatchEvent(new MouseEvent(type, {bubbles:true, cancelable:true, view:window, clientX:cx, clientY:cy}));
      });
      if (typeof node.click === 'function') node.click();
      return {ok:true, text:t||'发布', via:'cdp-point', x:Math.round(x), y:Math.round(y)};
    }
    node = node.parentElement;
  }
  return {ok:false, error:'point_not_publish', hit: el.tagName, cls: String(el.className).slice(0,40)};
})();
"""


def _preview_state(driver):
    try:
        return driver.execute_script(_JS_PREVIEW_STATE) or {}
    except Exception as e:
        return {"error": str(e)}


def _debug_publish_page(driver):
    try:
        return driver.execute_script(_JS_XHS_PUBLISH_HELPERS + r"""
          return (function() {
            var b = document.body.innerText || '';
            var cands = [];
            document.querySelectorAll('button, .ce-btn, [class*="bg-red"]').forEach(function(el) {
              var t = xhsNorm(el.innerText || el.textContent);
              if (t.indexOf('发') < 0) return;
              var r = el.getBoundingClientRect();
              cands.push({tag: el.tagName, text: t.slice(0,12), cls: String(el.className).slice(0,60),
                top: Math.round(r.top), left: Math.round(r.left), w: Math.round(r.width)});
            });
            var pb = xhsFindPublishBtn(document);
            return {
              url: location.href,
              preview_entered: xhsPreviewEntered(),
              xhs_publish_btn: !!pb,
              save_text: pb ? (pb.getAttribute('save-text') || '') : '',
              submit_text: pb ? (pb.getAttribute('submit-text') || '') : '',
              submit_disabled: pb ? (pb.getAttribute('submit-disabled') || '') : '',
              has_note_preview: b.indexOf('笔记预览') >= 0,
              button_count: document.querySelectorAll('button').length,
              candidates: cands.slice(0, 15)
            };
          })();
        """)
    except Exception as e:
        return {"error": str(e)}


def _js_click_final_publish(driver):
    try:
        return driver.execute_script(_JS_CLICK_FINAL_PUBLISH) or {"ok": False}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _click_first_layout_template(driver):
    """After 一键排版, pick the first layout card if template picker is shown."""
    try:
        found = driver.execute_script(_JS_XHS_PUBLISH_HELPERS + r"""
          return (function() {
            var cards = Array.from(document.querySelectorAll(
              '[class*="template"], [class*="layout"], [class*="style-card"], img'
            ));
            for (var i = 0; i < cards.length; i++) {
              var el = cards[i];
              var r = el.getBoundingClientRect();
              if (r.width < 120 || r.height < 120) continue;
              if (r.top < 120 || r.left < 200) continue;
              return {ok: true, tag: el.tagName};
            }
            return {ok: false};
          })();
        """) or {"ok": False}
        if not found.get("ok"):
            return found
        _human_pause("选择版式前")
        return driver.execute_script(_JS_XHS_PUBLISH_HELPERS + r"""
          return (function() {
            var cards = Array.from(document.querySelectorAll(
              '[class*="template"], [class*="layout"], [class*="style-card"], img'
            ));
            for (var i = 0; i < cards.length; i++) {
              var el = cards[i];
              var r = el.getBoundingClientRect();
              if (r.width < 120 || r.height < 120) continue;
              if (r.top < 120 || r.left < 200) continue;
              el.click();
              return {ok: true, tag: el.tagName};
            }
            return {ok: false};
          })();
        """) or {"ok": False}
    except Exception:
        return {"ok": False}


def _find_xhs_publish_btn(driver):
    """Preview footer component (save-text=暂存离开)."""
    from selenium.webdriver.common.by import By

    try:
        driver.switch_to.default_content()
    except Exception:
        pass
    for xpath in (
        '//xhs-publish-btn[@save-text="暂存离开"]',
        "//xhs-publish-btn",
    ):
        try:
            el = driver.find_element(By.XPATH, xpath)
            if el.is_displayed():
                return el
        except Exception:
            pass
    return None


def _find_xhs_publish_submit_btn(driver):
    """Submit control: must use submit-text=发布 (same as manual debug)."""
    from selenium.webdriver.common.by import By

    try:
        driver.switch_to.default_content()
    except Exception:
        pass
    for xpath in (
        '//xhs-publish-btn[@submit-text="发布"]',
        '//xhs-publish-btn[contains(@submit-text,"发布")]',
    ):
        try:
            el = driver.find_element(By.XPATH, xpath)
            if el.is_displayed():
                return el
        except Exception:
            pass
    return None


def _selenium_preview_entered(driver):
    try:
        if driver.execute_script(_JS_XHS_PUBLISH_HELPERS + "return xhsPreviewStrictEntered();"):
            return True
    except Exception:
        pass
    el = _find_xhs_publish_btn(driver)
    if not el:
        return False
    save = (el.get_attribute("save-text") or "").strip()
    submit = (el.get_attribute("submit-text") or "").strip().replace(" ", "")
    return "暂存离开" in save and submit in ("发布", "发 布")


def _preview_strict(driver):
    try:
        st = _preview_state(driver)
        if st.get("preview_strict") or st.get("preview_entered"):
            return True
        return _selenium_preview_entered(driver)
    except Exception:
        return False


def _click_next_step_after_layout(driver, steps, max_wait=90):
    """After AI layout: must click bottom 下一步 before preview (do not skip)."""
    print("Looking for 下一步 after layout...", flush=True)
    deadline = time.time() + max_wait
    last = {"ok": False}
    while time.time() < deadline:
        found = _js_find_by_texts(driver, ["下一步"], pick="bottom")
        if found.get("ok"):
            _human_pause("排版后点击「下一步」前")
            last = _js_click_by_texts(driver, ["下一步"], pick="bottom")
            steps.append({"click_下一步_after_layout": last})
            print("Click 下一步 (after layout):", json.dumps(last, ensure_ascii=False), flush=True)
            if last.get("ok"):
                _human_pause("排版后点击「下一步」后")
                return True, last
        if _preview_strict(driver):
            print("Strict preview visible (下一步 not needed).", flush=True)
            return True, last
        _human_pause("等待「下一步」出现")
        time.sleep(2)
    return False, last


def _wait_generating_done(driver, timeout=90):
    print("Waiting for image generation banner to clear...", flush=True)
    deadline = time.time() + timeout
    while time.time() < deadline:
        st = _preview_state(driver)
        if not st.get("generating_visible"):
            return True
        time.sleep(2)
    print("WARN: generating banner still visible.", flush=True)
    return False


def _wait_preview_after_next(driver, next_clicked, timeout=120):
    """After 下一步: wait generating done, then ce-btn footer or strict preview."""
    _wait_generating_done(driver, timeout=min(90, timeout))
    _human_pause("图片生成/预览渲染")
    print("Waiting for preview footer (xhs-publish-btn)...", flush=True)
    deadline = time.time() + timeout
    last_log = 0.0
    relaxed_since = None
    while time.time() < deadline:
        st = _preview_state(driver)
        if _preview_strict(driver):
            print(
                "Preview strict OK (ce_deep=%s publish_ready=%s)."
                % (st.get("ce_btn_deep_count"), st.get("publish_ready")),
                flush=True,
            )
            return True, "strict"
        if st.get("xhs_publish_btn") or st.get("publish_ready"):
            print(
                "Preview xhs-publish-btn ready (submit=%s disabled=%s)."
                % (st.get("submit_text"), st.get("submit_disabled")),
                flush=True,
            )
            return True, "xhs_publish_btn"
        if next_clicked and not st.get("generating_visible"):
            if relaxed_since is None:
                relaxed_since = time.time()
            elif time.time() - relaxed_since >= 18:
                print(
                    "Preview relaxed ready (下一步已点, generating=false, DOM 仍少按钮)."
                , flush=True)
                return True, "relaxed"
        else:
            relaxed_since = None
        now = time.time()
        if now - last_log >= 12:
            last_log = now
            dbg = _debug_publish_page(driver)
            dbg["active_url"] = (driver.current_url or "")[:100]
            print("  preview wait:", json.dumps(dbg, ensure_ascii=False), flush=True)
        time.sleep(2)
    print("Preview wait timeout:", json.dumps(_debug_publish_page(driver), ensure_ascii=False), flush=True)
    return False, "timeout"


def _publish_click_by_coordinates(driver):
    """Fallback: click bottom-right 发布 when Vue footer is visible but not in querySelectorAll."""
    size = driver.execute_script(
        "return {w: window.innerWidth, h: window.innerHeight};"
    ) or {"w": 1200, "h": 800}
    w, h = float(size.get("w", 1200)), float(size.get("h", 800))
    points = [
        (w * 0.82, h - 52, "发布-右下"),
        (w * 0.5, h - 52, "发布-中下"),
        (w * 0.72, h - 58, "发布-偏右"),
    ]
    for x, y, label in points:
        _human_pause("坐标点击 %s" % label)
        hit = driver.execute_script(
            _JS_XHS_PUBLISH_HELPERS + r"""
            var x = arguments[0], y = arguments[1];
            var el = document.elementFromPoint(x, y);
            if (!el) return {ok: false};
            var node = el;
            for (var i = 0; i < 10 && node; i++) {
              var t = xhsNorm(node.innerText || node.textContent);
              var cls = String(node.className || '');
              if (xhsIsPublishLabel(t) || cls.indexOf('bg-red') >= 0) {
                var r = node.getBoundingClientRect();
                var cx = r.left + r.width/2, cy = r.top + r.height/2;
                ['mouseover','mousedown','mouseup','click'].forEach(function(tp) {
                  node.dispatchEvent(new MouseEvent(tp, {bubbles:true, cancelable:true,
                    view:window, clientX:cx, clientY:cy}));
                });
                if (typeof node.click === 'function') node.click();
                return {ok: true, text: t || '发布', via: 'coord-js', x: Math.round(x), y: Math.round(y)};
              }
              node = node.parentElement;
            }
            return {ok: false, tag: el.tagName};
            """,
            x,
            y,
        )
        if hit and hit.get("ok"):
            return hit
        native = _cdp_click_viewport_point(driver, x, y)
        if native.get("ok"):
            native["text"] = "发布"
            native["via"] = "coord-cdp-" + label
            return native
    return {"ok": False, "error": "coord_publish_failed"}


def _wait_preview_page_entered(driver, timeout=30):
    """Short poll after a 下一步 click (used internally by _advance_to_preview)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        st = _preview_state(driver)
        if st.get("preview_entered") or _selenium_preview_entered(driver):
            return True
        time.sleep(1.5)
    return False


def _wait_preview_publish_ready(driver, timeout=90):
    print("Waiting for final 发布 button (max %ss)..." % timeout, flush=True)
    deadline = time.time() + timeout
    last = {}
    while time.time() < deadline:
        last = _preview_state(driver)
        if last.get("publish_ready"):
            print(
                "Final 发布 found: via=%s bottom=%s generating=%s"
                % (last.get("via"), last.get("picked_bottom"), last.get("generating_visible")),
                flush=True,
            )
            return True
        time.sleep(2)
    print("Publish button wait timeout:", json.dumps(last, ensure_ascii=False), flush=True)
    print("Debug:", json.dumps(_debug_publish_page(driver), ensure_ascii=False), flush=True)
    return False


def _publish_confirm_state(driver, url_before=""):
    """Snapshot for publish confirmation (preview may linger after real success)."""
    try:
        return driver.execute_script(_JS_XHS_PUBLISH_HELPERS + r"""
            var body = document.body.innerText || '';
            var href = (location.href || '').toLowerCase();
            var success = body.indexOf('发布成功') >= 0
                || body.indexOf('发表成功') >= 0
                || body.indexOf('笔记发布成功') >= 0
                || body.indexOf('发布完成') >= 0
                || body.indexOf('提交成功') >= 0
                || body.indexOf('笔记已发布') >= 0
                || body.indexOf('继续发布') >= 0
                || body.indexOf('再发一篇') >= 0
                || body.indexOf('查看笔记') >= 0;
            var hasConfirmDialog = body.indexOf('确认发布') >= 0
                || body.indexOf('确定发布') >= 0
                || body.indexOf('是否发布') >= 0;
            var pb = xhsFindPublishSubmitBtn(document);
            var strict = xhsPreviewStrictEntered();
            var publishing = false;
            if (pb && (pb.getAttribute('submit-disabled') || '').toString() === 'true') {
              publishing = true;
            }
            var still_preview = pb ? xhsPublishBtnReady(pb) : false;
            return {
              success: success,
              has_confirm_dialog: hasConfirmDialog,
              publishing: publishing,
              still_on_preview: still_preview,
              preview_strict: strict,
              btn_gone: !pb,
              url: href
            };
        """)
    except Exception as e:
        return {"error": str(e)}


def _publish_confirmed_longform(driver, url_before):
    """True when publish succeeded (toast, URL change, left preview, or publishing state)."""
    info = _publish_confirm_state(driver, url_before) or {}
    if info.get("error"):
        return False

    if info.get("success") or info.get("publishing") or info.get("btn_gone"):
        return True
    if not info.get("preview_strict") and not info.get("has_confirm_dialog"):
        return True

    url = (info.get("url") or (driver.current_url or "").lower())
    url_before_l = (url_before or "").lower()
    if "login" in url:
        return False
    if info.get("has_confirm_dialog"):
        return False
    if "note-manager" in url or "/notes" in url or "success" in url:
        return True
    if url != url_before_l and "publish/publish" not in url:
        return True
    return False


def _publish_dialog_visible(driver):
    try:
        return bool(driver.execute_script(_JS_XHS_PUBLISH_HELPERS + r"""
          var b = document.body.innerText || '';
          return b.indexOf('确认发布') >= 0 || b.indexOf('确定发布') >= 0
            || b.indexOf('是否发布') >= 0 || b.indexOf('确认要发布') >= 0;
        """))
    except Exception:
        return False


def _publish_click_had_effect(driver, url_before=None):
    """True when the page reacted after 发布 click."""
    if _publish_dialog_visible(driver):
        return True, "confirm_dialog"
    try:
        eff = driver.execute_script(_JS_XHS_PUBLISH_HELPERS + r"""
          var body = document.body.innerText || '';
          if (body.indexOf('发布成功') >= 0 || body.indexOf('发表成功') >= 0
              || body.indexOf('发布中') >= 0 || body.indexOf('提交成功') >= 0) {
            return {ok: true, reason: 'success_copy'};
          }
          var pb = xhsFindPublishSubmitBtn(document);
          if (!pb) return {ok: true, reason: 'btn_gone'};
          if ((pb.getAttribute('submit-disabled') || '').toString() === 'true') {
            return {ok: true, reason: 'submit_disabled'};
          }
          return {ok: false, reason: 'still_on_preview'};
        """)
        if eff and eff.get("ok"):
            return True, eff.get("reason") or "js"
    except Exception:
        pass
    url = (driver.current_url or "").lower()
    before = (url_before or "").lower()
    if before and url != before and "login" not in url:
        return True, "url_changed"
    return False, "no_effect"


def _click_publish_confirm_dialog(driver):
    """Second-step confirm after 发布 (if platform shows a dialog)."""
    for labels in (["确认发布", "确定发布", "确认", "确定"], ["发布"]):
        r = _js_click_by_texts(driver, labels, pick="bottom", partial=True)
        if r.get("ok"):
            return r
    return {"ok": False}


def _log_publish_click_coords(driver, el):
    """Print viewport coords for manual debugging (trusted mouse)."""
    try:
        info = driver.execute_script(
            """
            var el = arguments[0];
            var r = el.getBoundingClientRect();
            return {
              left: Math.round(r.left), top: Math.round(r.top),
              width: Math.round(r.width), height: Math.round(r.height),
              x88: Math.round(r.left + r.width * 0.88),
              y50: Math.round(r.top + r.height * 0.5)
            };
            """,
            el,
        )
        print(
            "CDP click target (xhs-publish-btn red area) viewport (x=%s, y=%s). "
            "submit-disabled=%s"
            % (info.get("x88"), info.get("y50"), el.get_attribute("submit-disabled")),
            flush=True,
        )
        return info
    except Exception:
        return {}


def _after_final_publish_click(driver, hit):
    """Wait briefly and try confirm dialog after 发布 pointer event."""
    _human_pause("发布后等待")
    for _ in range(10):
        if _publish_dialog_visible(driver):
            hit["dialog_visible"] = True
            dlg = _click_publish_confirm_dialog(driver)
            hit["confirm_dialog"] = dlg
            if dlg.get("ok"):
                print("Confirm dialog:", json.dumps(dlg, ensure_ascii=False), flush=True)
            break
        time.sleep(1.0)
    return hit


def _wait_publish_confirmed_longform(driver, url_before, timeout_sec=90):
    """Poll until publish success; retry confirm dialog while on preview."""
    deadline = time.time() + timeout_sec
    last_state = {}
    retried_publish = False
    while time.time() < deadline:
        if _publish_dialog_visible(driver):
            dlg = _click_publish_confirm_dialog(driver)
            if dlg.get("ok"):
                print("Confirm dialog (wait loop):", json.dumps(dlg, ensure_ascii=False), flush=True)
        if _publish_confirmed_longform(driver, url_before):
            return True, last_state
        last_state = _publish_confirm_state(driver, url_before) or {}
        elapsed = int(timeout_sec - (deadline - time.time()))
        if (
            not retried_publish
            and elapsed >= 8
            and last_state.get("still_on_preview")
            and not last_state.get("has_confirm_dialog")
        ):
            retried_publish = True
            print(
                "WARN: still on preview — dismiss browser prompts and retry 发布",
                flush=True,
            )
            _dismiss_creator_browser_prompts(driver)
            el = _find_xhs_publish_submit_btn(driver)
            if el and (el.get_attribute("submit-disabled") or "").lower() != "true":
                hit_r = _js_click_publish_submit(driver)
                if not hit_r.get("ok"):
                    hit_r = _selenium_click_publish_host(driver, el, 0.82)
                if not hit_r.get("ok"):
                    hit_r = _cdp_click_xhs_publish_btn(driver, el, x_ratio=0.65)
                had_effect, _ = _publish_click_had_effect(driver)
                if not had_effect:
                    hit_r = _screen_click_publish_btn(driver, el)
                _after_final_publish_click(driver, hit_r or {"ok": False})
        if elapsed > 0 and elapsed % 10 == 0:
            print(
                "Still waiting publish confirm (%ss): %s"
                % (elapsed, json.dumps(last_state, ensure_ascii=False)),
                flush=True,
            )
        time.sleep(1.5)
    return False, last_state


def _cdp_click_xhs_publish_btn(driver, el, x_ratio=0.88):
    """CDP trusted click on xhs-publish-btn red area (resolution-independent)."""
    try:
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center',inline:'nearest'});", el
        )
        rect = driver.execute_script(
            """
            var r = arguments[0].getBoundingClientRect();
            return {x: r.left, y: r.top, w: r.width, h: r.height};
            """,
            el,
        )
        if not rect or rect.get("w", 0) < 10:
            return {"ok": False, "error": "bad_rect"}
        x = float(rect["x"]) + float(rect["w"]) * x_ratio
        y = float(rect["y"]) + float(rect["h"]) * 0.5
        hit = _cdp_click_viewport_point(driver, x, y, click_count=1)
        if hit.get("ok"):
            hit["text"] = "发布"
            hit["via"] = "cdp-xhs-publish-btn-%.0f%%" % (x_ratio * 100)
        return hit
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _cdp_click_publish_bottom_center(driver):
    """Fallback: fixed footer coords (brittle on layout change — use after element click)."""
    size = driver.execute_script(
        "return {w: window.innerWidth, h: window.innerHeight};"
    ) or {"w": 1200, "h": 800}
    cx = float(size.get("w", 1200)) * 0.5
    cy = float(size.get("h", 800)) - 58
    hit = _cdp_click_viewport_point(driver, cx, cy, click_count=1)
    if hit.get("ok"):
        hit["text"] = "发布"
        hit["via"] = "cdp-bottom-center-fallback"
    return hit


def _cdp_bring_to_front(driver):
    try:
        driver.execute_cdp_cmd("Page.bringToFront", {})
    except Exception:
        pass


def _cdp_set_permission(driver, name, setting, origin=XHS_CREATOR_ORIGIN):
    """Chrome native permission bar (e.g. geolocation) blocks page clicks until dismissed."""
    try:
        driver.execute_cdp_cmd(
            "Browser.setPermission",
            {
                "permission": {"name": name},
                "setting": setting,
                "origin": origin,
            },
        )
        return True
    except Exception as exc:
        print(
            "WARN: Browser.setPermission %s=%s @%s: %s"
            % (name, setting, origin, exc),
            flush=True,
        )
        return False


def _dismiss_creator_browser_prompts(driver):
    """
    Clear Chrome geolocation bar so page clicks reach xhs-publish-btn.
    Grant once (dismisses active prompt), then deny for later visits.
    """
    try:
        driver.execute_cdp_cmd(
            "Browser.grantPermissions",
            {
                "origin": XHS_CREATOR_ORIGIN,
                "permissions": ["geolocation"],
            },
        )
    except Exception:
        pass
    for origin in (XHS_CREATOR_ORIGIN, "https://www.xiaohongshu.com"):
        for perm in ("geolocation", "notifications"):
            _cdp_set_permission(driver, perm, "denied", origin=origin)
    _cdp_bring_to_front(driver)
    try:
        _cdp_dispatch_key(driver, "rawKeyDown", "Escape", "Escape", virtual_key_code=27)
        time.sleep(0.05)
        _cdp_dispatch_key(driver, "keyUp", "Escape", "Escape", virtual_key_code=27)
    except Exception:
        pass
    time.sleep(0.25)


def _read_publish_viewport_metrics(driver):
    """Best-effort viewport metrics for zoom / screen-click debugging."""
    out = {}
    try:
        out.update(
            driver.execute_script(
                """
                return {
                  inner_w: window.innerWidth,
                  inner_h: window.innerHeight,
                  outer_w: window.outerWidth,
                  outer_h: window.outerHeight,
                  screen_x: window.screenX,
                  screen_y: window.screenY,
                  chrome_h: Math.max(0, window.outerHeight - window.innerHeight),
                  dpr: window.devicePixelRatio
                };
                """
            )
            or {}
        )
    except Exception:
        pass
    try:
        metrics = driver.execute_cdp_cmd("Page.getLayoutMetrics", {}) or {}
        vv = metrics.get("visualViewport") or {}
        if vv.get("scale") is not None:
            out["visual_scale"] = vv.get("scale")
    except Exception:
        pass
    return out


def _cdp_dispatch_key(driver, event_type, key, code=None, modifiers=0, virtual_key_code=None):
    payload = {"type": event_type, "key": key, "modifiers": int(modifiers)}
    if code:
        payload["code"] = code
    if virtual_key_code is not None:
        payload["windowsVirtualKeyCode"] = int(virtual_key_code)
        payload["nativeVirtualKeyCode"] = int(virtual_key_code)
    driver.execute_cdp_cmd("Input.dispatchKeyEvent", payload)


def _cdp_reset_zoom_100(driver):
    """Reset page scale via CDP Emulation only (no Cmd/Ctrl+0 — macOS may open Settings)."""
    try:
        _cdp_bring_to_front(driver)
        for cmd in ("Emulation.clearDeviceMetricsOverride", "Emulation.resetPageScaleFactor"):
            try:
                driver.execute_cdp_cmd(cmd, {})
            except Exception:
                pass
        time.sleep(0.15)
        return True
    except Exception as e:
        print("WARN: reset zoom via CDP Emulation failed: %s" % e, flush=True)
        return False


def _ensure_zoom_100_for_publish(driver, enabled=False):
    """Optional CDP scale reset before publish click (off by default)."""
    if not enabled:
        return {"skipped": True, "reason": "default_off"}
    before = _read_publish_viewport_metrics(driver)
    ok = _cdp_reset_zoom_100(driver)
    after = _read_publish_viewport_metrics(driver)
    info = {"ok": ok, "method": "cdp-emulation", "before": before, "after": after}
    print("Browser zoom reset (CDP): %s" % json.dumps(info, ensure_ascii=False), flush=True)
    return info


def _cdp_click_viewport_point(driver, x, y, click_count=1):
    """Chrome DevTools Protocol: inject real mouse down/up at viewport (x,y)."""
    try:
        _cdp_bring_to_front(driver)
        for typ, delay in (
            ("mouseMoved", 0),
            ("mousePressed", 0.05),
            ("mouseReleased", 0.05),
        ):
            driver.execute_cdp_cmd(
                "Input.dispatchMouseEvent",
                {
                    "type": typ,
                    "x": float(x),
                    "y": float(y),
                    "button": "left",
                    "clickCount": click_count,
                },
            )
            if delay:
                time.sleep(delay)
        return {"ok": True, "via": "cdp-native", "x": int(x), "y": int(y)}
    except Exception as e:
        return {"ok": False, "error": "cdp_native:" + str(e)}


def _js_click_publish_submit(driver):
    try:
        return driver.execute_script(_JS_CLICK_FINAL_PUBLISH) or {"ok": False}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def _selenium_click_publish_host(driver, el, x_ratio=0.82):
    """Real pointer via WebDriver on xhs-publish-btn (works when CDP misses shadow)."""
    from selenium.webdriver.common.action_chains import ActionChains

    try:
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center',inline:'nearest'});", el
        )
        time.sleep(0.25)
        w = max(int(el.size.get("width", 200) or 200), 40)
        h = max(int(el.size.get("height", 36) or 36), 20)
        ox = int(w * x_ratio)
        oy = int(h * 0.5)
        ActionChains(driver).move_to_element_with_offset(el, ox, oy).pause(0.15).click().perform()
        return {"ok": True, "via": "selenium-offset", "ox": ox, "oy": oy}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def _selenium_native_click_element(driver, el):
    try:
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center',inline:'nearest'});", el
        )
        time.sleep(0.2)
        el.click()
        return {"ok": True, "via": "selenium-native-click"}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def _screen_click_disabled():
    """Opt-out only: export XHS_DISABLE_SCREEN_CLICK=1 to skip pyautogui fallback."""
    return os.environ.get("XHS_DISABLE_SCREEN_CLICK", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )


def _screen_click_viewport(driver, x, y):
    """OS-level click (pyautogui). Auto fallback when browser clicks miss; safe if not installed."""
    if _screen_click_disabled():
        return {"ok": False, "skipped": True, "reason": "XHS_DISABLE_SCREEN_CLICK"}
    try:
        import pyautogui
    except ImportError:
        return {"ok": False, "skipped": True, "reason": "pyautogui_not_installed"}
    except Exception as exc:
        return {
            "ok": False,
            "skipped": True,
            "reason": "pyautogui_import_error",
            "error": str(exc),
        }

    m = _read_publish_viewport_metrics(driver)
    sx = int(m.get("screen_x", 0) + float(x))
    sy = int(m.get("screen_y", 0) + float(m.get("chrome_h", 90)) + float(y))
    try:
        try:
            pyautogui.FAILSAFE = False
        except Exception:
            pass
        pyautogui.click(sx, sy)
        return {
            "ok": True,
            "via": "pyautogui",
            "screen_x": sx,
            "screen_y": sy,
            "viewport_x": int(x),
            "viewport_y": int(y),
        }
    except Exception as exc:
        return {"ok": False, "error": "pyautogui_click:" + str(exc)}


def _screen_click_publish_btn(driver, el):
    """pyautogui on xhs-publish-btn (65% then 82% — same ratios as successful CDP clicks)."""
    if _screen_click_disabled():
        return {"ok": False, "skipped": True, "reason": "XHS_DISABLE_SCREEN_CLICK"}
    try:
        rect = driver.execute_script(
            "var r=arguments[0].getBoundingClientRect();"
            "return {x:r.left,y:r.top,w:r.width,h:r.height};",
            el,
        ) or {}
    except Exception as exc:
        return {"ok": False, "error": "rect:" + str(exc)}
    if not rect or float(rect.get("w", 0)) < 10:
        return {"ok": False, "error": "bad_publish_btn_rect"}

    last = {"ok": False, "error": "pyautogui_publish_failed"}
    for ratio, label in ((0.65, "65%"), (0.82, "82%")):
        vx = float(rect["x"]) + float(rect["w"]) * ratio
        vy = float(rect["y"]) + float(rect["h"]) * 0.5
        hit = _screen_click_viewport(driver, vx, vy)
        if hit.get("skipped") and hit.get("reason") == "pyautogui_not_installed":
            print("WARN: pyautogui not installed — screen click fallback skipped", flush=True)
            return hit
        if hit.get("ok"):
            hit["via"] = "pyautogui-" + label
            return hit
        last = hit
    return last


def _try_click_final_publish(driver, wait_timeout=90, reset_zoom=False):
    """Preview 发布：JS/Selenium 点组件内红钮优先，CDP/屏幕坐标兜底。"""
    focus_best_tab(driver, prefer_creator=True)
    _dismiss_creator_browser_prompts(driver)
    print("URL before 发布 click: %s" % ((driver.current_url or "")[:110]), flush=True)
    _wait_generating_done(driver, timeout=60)
    _wait_preview_publish_ready(driver, timeout=wait_timeout)
    st = _preview_state(driver)
    strict = _preview_strict(driver)
    if not strict and not st.get("publish_ready") and not st.get("xhs_publish_btn"):
        print(
            "Cannot find 发布. State: %s"
            % json.dumps(_debug_publish_page(driver), ensure_ascii=False),
            flush=True,
        )
        return {"ok": False, "error": "preview_page_not_entered"}

    el = _find_xhs_publish_submit_btn(driver)
    if not el:
        return {"ok": False, "error": "xhs_publish_submit_btn_not_found"}
    if (el.get_attribute("submit-disabled") or "").lower() == "true":
        return {"ok": False, "error": "submit_disabled"}
    _log_publish_click_coords(driver, el)
    probe = driver.execute_script(
        _JS_XHS_PUBLISH_HELPERS + "return xhsProbePublishBtn();"
    )
    print("Publish btn probe:", json.dumps(probe, ensure_ascii=False), flush=True)

    zoom_info = _ensure_zoom_100_for_publish(driver, enabled=reset_zoom)
    last = {"ok": False, "error": "publish_click_failed", "zoom_reset": zoom_info}

    rect = driver.execute_script(
        "var r=arguments[0].getBoundingClientRect();"
        "return {x:r.left,y:r.top,w:r.width,h:r.height};",
        el,
    ) or {}
    strategies = [
        ("JS inner 发布", lambda: _js_click_publish_submit(driver)),
        ("Selenium native", lambda: _selenium_native_click_element(driver, el)),
        ("Selenium offset", lambda: _selenium_click_publish_host(driver, el, 0.82)),
        ("CDP 65%", lambda: _cdp_click_xhs_publish_btn(driver, el, x_ratio=0.65)),
        ("CDP 88%", lambda: _cdp_click_xhs_publish_btn(driver, el, x_ratio=0.88)),
        ("CDP bottom", lambda: _cdp_click_publish_bottom_center(driver)),
        (
            "JS elementFromPoint",
            lambda: driver.execute_script(_JS_CDP_CLICK_BOTTOM_PUBLISH) or {"ok": False},
        ),
        (
            "pyautogui (VNC)",
            lambda: _screen_click_publish_btn(driver, el),
        ),
    ]

    for idx, (label, fn) in enumerate(strategies, 1):
        _dismiss_creator_browser_prompts(driver)
        _human_pause("发布 %d/%d: %s" % (idx, len(strategies), label))
        try:
            hit = fn() or {"ok": False}
        except Exception as exc:
            hit = {"ok": False, "error": str(exc)}
        print("Publish try:", json.dumps(hit, ensure_ascii=False), flush=True)
        if hit.get("skipped"):
            if hit.get("reason") == "pyautogui_not_installed":
                print(
                    "WARN: pyautogui not installed — install with: pip3 install pyautogui",
                    flush=True,
                )
            continue
        if not hit.get("ok"):
            continue
        last = _after_final_publish_click(driver, hit)
        last["zoom_reset"] = zoom_info
        had_effect, effect_reason = _publish_click_had_effect(driver)
        last["click_effect"] = effect_reason
        if had_effect:
            last["strategy"] = label
            return last
        print("WARN: %s — no page effect (%s)" % (label, effect_reason), flush=True)

    last["zoom_reset"] = zoom_info
    print("Final 发布: all strategies exhausted.", flush=True)
    print("Debug:", json.dumps(_debug_publish_page(driver), ensure_ascii=False), flush=True)
    print(
        "TIP: In VNC click Never allow on location bar; optional: pip3 install pyautogui",
        flush=True,
    )
    return last


def run_publish(
    driver, title, body, tags=None, image_path=None, submit=False, emit_json=False,
    reset_zoom=False,
):
    """Long-form publish: 写长文 -> 新的创作 -> fill -> 一键排版 -> 下一步 -> 发布."""
    if image_path:
        print("NOTE: --image-file is ignored for long-form (写长文) mode.", file=sys.stderr)

    url_before = driver.current_url or ""
    steps = []
    submit_error = None

    _dismiss_creator_browser_prompts(driver)
    ok_enter, enter_err, enter_steps = _enter_longform_editor(driver)
    steps.extend(enter_steps)
    print("Editor URL:", driver.current_url)

    if not ok_enter:
        if emit_json:
            print(json.dumps({
                "ok": False, "mode": "longform", "error": enter_err,
                "published": False, "steps": steps,
            }, ensure_ascii=False))
        return 1

    body_text = _append_tags_to_body(body, tags or [])
    fill = _fill_longform_fields(driver, title, body_text)
    if not fill.get("filled_body") and body_text.strip():
        print("WARN: body fill missed — wait for editor and retry once", flush=True)
        if _wait_longform_body_editor(driver, timeout=20):
            fill = _fill_longform_fields(driver, title, body_text)
    filled_title = fill.get("filled_title")
    filled_body = fill.get("filled_body")
    print("Fill title:", filled_title, "| Fill body:", filled_body, flush=True)
    steps.append({"fill": fill})
    if not filled_title or not filled_body:
        print(
            "WARN: title/body field not found — 一键排版可能一直转圈直到 layout_timeout（请在 VNC 确认正文）",
            file=sys.stderr,
            flush=True,
        )

    r_layout = _human_click_retry(driver, ["一键排版"], timeout=20, pick="bottom")
    steps.append({"click_一键排版": r_layout})
    print("Click 一键排版:", json.dumps(r_layout, ensure_ascii=False))
    if not r_layout.get("ok"):
        submit_error = "click_一键排版_failed"
    else:
        _human_pause("等待 AI 排版开始")
        print("Waiting for AI layout (up to %ss)..." % LONGFORM_LAYOUT_WAIT_SEC)
        layout_ready = _wait_longform_layout_ready(driver)
        steps.append({"layout_ready": layout_ready})
        if not layout_ready:
            submit_error = "layout_timeout"
        else:
            _human_pause("排版完成，准备选版式/下一步")
            tpl = _click_first_layout_template(driver)
            steps.append({"click_template": tpl})
            if tpl.get("ok"):
                _human_pause("选中版式后")
            focus_best_tab(driver, prefer_creator=True, log=False)
            clicked_next, next_r = _click_next_step_after_layout(driver, steps, max_wait=90)
            steps.append({"next_clicked": clicked_next})
            if not clicked_next:
                print("WARN: 下一步 not clicked after layout.", flush=True)
            preview_ok, preview_mode = _wait_preview_after_next(
                driver, next_clicked=clicked_next, timeout=120,
            )
            steps.append({"preview_wait_mode": preview_mode})
            if not preview_ok:
                submit_error = "preview_page_not_entered"
            else:
                print("Reached preview (mode=%s)." % preview_mode, flush=True)

    shot = None
    submit_clicked = False
    published = False
    publish_click = None

    if submit and not submit_error:
        _human_pause("进入预览后，准备发布")
        url_before_submit = driver.current_url or ""
        publish_click = _try_click_final_publish(driver, wait_timeout=90, reset_zoom=reset_zoom)
        steps.append({"click_final_发布": publish_click})
        submit_clicked = bool((publish_click or {}).get("ok"))
        if not submit_clicked:
            submit_error = (publish_click or {}).get("error") or "final_publish_button_not_found"
        else:
            sec = random.uniform(1.0, 2.0)
            print("Wait %.1fs — 点击发布后截图" % round(sec, 1), flush=True)
            time.sleep(sec)
            shot = _save_screenshot(driver, "xhs_longform_after_publish_click")
            steps.append({"screenshot_after_publish_click": shot})
            print("Waiting for publish confirmation (up to 90s)...", flush=True)
            published, confirm_state = _wait_publish_confirmed_longform(
                driver, url_before_submit, timeout_sec=90,
            )
            if publish_click is not None:
                publish_click["confirm_state"] = confirm_state
            if published:
                print("Publish confirmed.", flush=True)
            else:
                submit_error = "publish_not_confirmed"
                print(
                    "Publish not confirmed. url=%s state=%s"
                    % (
                        (driver.current_url or "")[:100],
                        json.dumps(confirm_state, ensure_ascii=False),
                    ),
                    flush=True,
                )
    elif not submit and not submit_error:
        print("DRY-RUN: no --submit (stopped before final 发布)")
        shot = _save_screenshot(driver, "xhs_longform")

    if emit_json:
        ok = not submit_error
        if submit:
            ok = ok and submit_clicked and published
        print(json.dumps({
            "ok": ok,
            "mode": "longform",
            "submitted": submit_clicked,
            "published": published,
            "publish_button_text": (publish_click or {}).get("text"),
            "publish_via": (publish_click or {}).get("via"),
            "dry_run": not submit,
            "url": driver.current_url,
            "screenshot": shot,
            "filled_title": filled_title,
            "filled_body": filled_body,
            "error": submit_error,
            "steps": steps,
        }, ensure_ascii=False))
    if submit:
        return 0 if not submit_error and submit_clicked and published else 1
    return 0 if not submit_error else 1


def main():
    parser = argparse.ArgumentParser(description="Xiaohongshu publish via Chrome attach")
    parser.add_argument("--debug-address", default=DEFAULT_DEBUG_ADDRESS)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--check-creator",
        action="store_true",
        help="Also verify creator.xiaohongshu.com publish access (separate login)",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Long-form flow: 写长文 -> 新的创作 -> fill -> 一键排版 -> 下一步",
    )
    parser.add_argument("--title", default="")
    parser.add_argument("--body", default="")
    parser.add_argument("--body-file", default=None)
    parser.add_argument("--tags", default="", help="Comma-separated hashtags without #")
    parser.add_argument(
        "--image-file",
        default=None,
        help="Ignored for long-form (写长文); kept for CLI compatibility",
    )
    parser.add_argument("--submit", action="store_true")
    parser.add_argument(
        "--reset-zoom",
        action="store_true",
        help="Optional CDP Emulation scale reset before 发布 (default off; does not use Cmd+0)",
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--quit-browser", action="store_true")
    args = parser.parse_args()

    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as f:
            args.body = f.read()

    debug_url = "http://" + args.debug_address
    try:
        info = check_debug_port(debug_url)
        print("Connected:", info.get("Browser", info))
    except ConnectionError as e:
        print(e, file=sys.stderr)
        return 2

    if not args.check and not args.publish:
        parser.print_help()
        return 0

    print("Attaching to Chrome (%s) ..." % args.debug_address)
    driver = attach_chrome(args.debug_address)
    focus_best_tab(driver, prefer_creator=bool(args.publish))
    exit_code = 0
    try:
        if args.check:
            if args.check_creator:
                result = check_creator_ready(driver)
            else:
                result = check_login(driver, check_creator=False)
            if args.json:
                print(json.dumps({
                    "ok": result.get("api_ok") and (result.get("creator_ok", True) is not False),
                    "logged_in": result.get("api_ok"),
                    "creator_ok": result.get("creator_ok"),
                    "user_name": result.get("user_name"),
                    "user_id": result.get("user_id"),
                    "method": result.get("method"),
                    "error": result.get("error"),
                }, ensure_ascii=False))
            elif not result.get("api_ok"):
                print("Not logged in:", result.get("error"), file=sys.stderr)
                exit_code = 1
            else:
                print("Logged in as:", result.get("user_name"))
        if args.publish:
            api = check_creator_ready(driver)
            if not api.get("creator_ok"):
                print(
                    "Log in to creator center in Chrome first:",
                    api.get("error"),
                    file=sys.stderr,
                )
                exit_code = 1
            else:
                if args.submit:
                    print("WARNING: --submit will publish a REAL XHS note.")
                tags = _normalize_tags(args.tags)
                rc = run_publish(
                    driver, args.title, args.body, tags=tags,
                    image_path=args.image_file, submit=args.submit, emit_json=args.json,
                    reset_zoom=args.reset_zoom,
                )
                if rc != 0:
                    exit_code = rc
    finally:
        if args.quit_browser:
            driver.quit()
        else:
            try:
                focus_best_tab(driver, prefer_creator=True, log=False)
            except Exception:
                pass
    return exit_code


if __name__ == "__main__":
    sys.exit(main() or 0)
