#!/usr/bin/env python3
"""
verify_helpers.py - Ground truth verification (no agent involvement)

These functions read REAL values from the page/system.
The agent cannot fake these - either the value exists or it doesn't.
"""

import hashlib
import os
import time
from typing import Optional, Tuple

def screen_hash(ctrl) -> str:
    """Hash the current screen. Used to detect if anything changed."""
    path = "/tmp/_hash_check.png"
    ctrl.screenshot(path)
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def screen_changed(ctrl, hash_before: str, settle: float = 1.5) -> bool:
    """Returns True if screen changed since hash_before was taken."""
    time.sleep(settle)
    hash_after = screen_hash(ctrl)
    changed = hash_before != hash_after
    if not changed:
        print(" ⚠️ SCREEN DID NOT CHANGE — agent likely did nothing")
    return changed


def dom_value(ctrl, selector: str, prop: str = "value") -> str:
    """
    Read actual DOM value — cannot be faked by agent.
    prop: 'value' for inputs, 'innerText' for divs, 'href' for links
    """
    result = ctrl.js(f"""
    (function() {{
        const el = document.querySelector('{selector}');
        if (!el) return '__NOT_FOUND__';
        return el.{prop} || el.getAttribute('{prop}') || '';
    }})()
    """)
    return str(result) if result else ""


def dom_exists(ctrl, selector: str) -> bool:
    """Check if element exists on page."""
    result = ctrl.js(f"""
    document.querySelector('{selector}') !== null
    """)
    return result is True


def current_url(ctrl) -> str:
    """Get current page URL."""
    return ctrl.js("window.location.href") or ""


def page_title(ctrl) -> str:
    """Get page title."""
    return ctrl.js("document.title") or ""


def page_contains_text(ctrl, text: str) -> bool:
    """Check if visible page text contains a string."""
    body = ctrl.js("document.body.innerText") or ""
    return text.lower() in body.lower()


def get_scroll_position(ctrl) -> int:
    """Get current vertical scroll position."""
    result = ctrl.js("window.scrollY")
    return int(result) if result else 0


def assert_dom_value(ctrl, selector: str, expected: str, prop: str = "value"):
    """Assert DOM value matches expected. Raises on failure."""
    actual = dom_value(ctrl, selector, prop)
    if actual == "__NOT_FOUND__":
        raise AssertionError(
            f"FAIL: element '{selector}' not found on page\n"
            f" → Element doesn't exist in DOM"
        )
    if expected.lower() not in actual.lower():
        raise AssertionError(
            f"FAIL: DOM check failed\n"
            f" selector  : {selector}\n"
            f" expected  : '{expected}'\n"
            f" actual    : '{actual}'\n"
            f" → Agent claimed success but DOM proves otherwise"
        )
    print(f" ✅ DOM verified: '{selector}' = '{actual[:60]}'")


def assert_url_contains(ctrl, expected: str):
    """Assert current URL contains expected string."""
    actual = current_url(ctrl)
    if expected.lower() not in actual.lower():
        raise AssertionError(
            f"FAIL: URL check failed\n"
            f" expected : '{expected}'\n"
            f" actual   : '{actual}'\n"
            f" → Agent claimed navigation but URL proves otherwise"
        )
    print(f" ✅ URL verified: '{actual[:80]}'")


def assert_page_has_text(ctrl, text: str):
    """Assert page body contains text."""
    if not page_contains_text(ctrl, text):
        raise AssertionError(
            f"FAIL: page text check failed\n"
            f" expected text : '{text}'\n"
            f" → Not found in page body\n"
            f" → Agent claimed to see it but page proves otherwise"
        )
    print(f" ✅ Page text verified: found '{text}'")


def assert_screen_changed(hash_before: str, hash_after: str):
    """Assert screen hash changed."""
    if hash_before == hash_after:
        raise AssertionError(
            "FAIL: screen did not change\n"
            " → Agent reported actions but screen is identical\n"
            " → Classic hallucination pattern"
        )
    print(" ✅ Screen diff verified: screen changed")


def assert_scroll_changed(scroll_before: int, scroll_after: int):
    """Assert scroll position changed."""
    if scroll_after <= scroll_before:
        raise AssertionError(
            f"FAIL: scroll position did not change\n"
            f" before: {scroll_before}px\n"
            f" after:  {scroll_after}px\n"
            f" → Agent claimed to scroll but window.scrollY proves otherwise"
        )
    print(f" ✅ Scroll verified: {scroll_before}px → {scroll_after}px")


def save_evidence(ctrl, test_name: str) -> str:
    """Save screenshot as evidence when test fails."""
    path = f"/tmp/EVIDENCE_{test_name}.png"
    ctrl.screenshot(path)
    print(f" 📸 Evidence saved: {path}")
    return path


def test_result(test_name: str, passed: bool, message: str = ""):
    """Print test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"\n{status}: {test_name}")
    if message:
        print(f" {message}")
    return passed


# ============================================================================
# BUG FIX 1: Google Search Box Selector (Textarea vs Input)
# ============================================================================

def google_search_box(ctrl):
    """
    Find Google's search box regardless of element type.
    Google uses textarea on homepage, input on results page.
    """
    sel = ctrl.js("""
    (function() {
        if (document.querySelector('textarea[name="q"]'))
            return 'textarea[name="q"]';
        if (document.querySelector('input[name="q"]'))
            return 'input[name="q"]';
        if (document.querySelector('[aria-label="Search"]'))
            return '[aria-label="Search"]';
        if (document.querySelector('input[type="search"]'))
            return 'input[type="search"]';
        return null;
    })()
    """)
    if not sel:
        raise RuntimeError(
            "Google search box not found on page.\n"
            "Check screenshot — may not be on Google."
        )
    return sel


def type_in_google_search(ctrl, text):
    """Click Google search box and type text."""
    sel = google_search_box(ctrl)
    ctrl.click_selector(sel)
    time.sleep(0.3)
    ctrl.type_into_focused(text)
    print(f" ✅ typed into Google search box (selector: {sel})")


# ============================================================================
# BUG FIX 4: Desktop Screenshot (DISPLAY=:0 not :99)
# ============================================================================

import subprocess

def desktop_screenshot(path="/tmp/desktop_screenshot.png"):
    """
    Screenshot the REAL desktop (:0), not Xvfb (:99).
    Use this for desktop app tests (G.1, G.2).
    """
    # Try scrot on :0
    result = subprocess.run(
        ["scrot", "-o", path],
        env={**os.environ, "DISPLAY": ":0"},
        capture_output=True
    )
    if result.returncode != 0:
        # Try gnome-screenshot fallback
        subprocess.run(
            ["gnome-screenshot", "-f", path],
            env={**os.environ, "DISPLAY": ":0"},
            capture_output=True
        )

    if not os.path.exists(path):
        raise RuntimeError(f"Desktop screenshot failed: {path}")

    size = os.path.getsize(path)
    print(f" [desktop] screenshot: {path} ({size} bytes)")

    if size < 100000:
        raise RuntimeError(
            f"Desktop screenshot too small ({size}b) — likely blank\n"
            f" Check DISPLAY=:0 is the real desktop\n"
            f" Path: {path}"
        )
    return path, size


# ============================================================================
# V6 FIX 4: Google Search Submission
# ============================================================================

def google_search(ctrl, query, wait=3.0):
    """
    Search Google reliably.
    Types query, then clicks the Search button directly.
    Falls back to Return key if button not found.
    """
    # Find search box
    sel = ctrl.js("""
    (function() {
        if (document.querySelector('textarea[name="q"]'))
            return 'textarea[name="q"]';
        if (document.querySelector('input[name="q"]'))
            return 'input[name="q"]';
        return null;
    })()
    """)
    assert sel, "Google search box not found"

    # Clear and type
    ctrl.click_selector(sel)
    time.sleep(0.3)
    ctrl.js(f"document.querySelector('{sel}').value = ''")
    ctrl._send("Input.insertText", {"text": query})
    time.sleep(0.5)

    # Verify typed
    val = ctrl.js(f"document.querySelector('{sel}').value")
    print(f" [google] typed: '{val}'")
    assert query in str(val), f"Typing failed: '{val}'"

    # Try to submit via button click first (most reliable)
    btn_found = ctrl.js("""
    (function() {
        const btns = Array.from(document.querySelectorAll(
            'input[type="submit"], button[type="submit"], [role="button"]'
        ));
        for (const b of btns) {
            const text = (b.value || b.innerText || b.textContent || '').toLowerCase();
            if (text.includes('search') || text.includes('google')) {
                b.click();
                return true;
            }
        }
        return false;
    })()
    """)

    if not btn_found:
        # Fallback: Return key or form submit
        ctrl.js("document.querySelector('[name=\"q\"]')?.closest('form')?.submit()")

    time.sleep(wait)

    url = ctrl.js("window.location.href")
    print(f" [google] after search url: {url[:60]}")
    return url
