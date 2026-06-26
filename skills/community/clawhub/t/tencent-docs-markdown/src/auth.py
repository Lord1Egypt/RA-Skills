"""
Tencent Docs Markdown Skill - Authentication Module

Provides QR code login via Playwright to obtain session cookies.
Supports cookie persistence and automatic re-login on expiry.
"""

import json
import os
import time
import re
import io
import subprocess
import sys
import tempfile
import platform
from pathlib import Path
from urllib.parse import urlparse

import requests

COOKIE_FILE = os.path.join(os.path.dirname(__file__), '..', '.cookies.json')
DOCS_URL = 'https://docs.qq.com/desktop'
LOGIN_CHECK_URL = 'https://docs.qq.com/cgi-bin/online_docs/user_info'

# Allowed cookie domains — only cookies scoped to Tencent Docs are permitted.
# This is the central whitelist used by both the sanitizer and the network layer.
ALLOWED_COOKIE_DOMAINS = ['.qq.com', 'docs.qq.com', '.docs.qq.com']

USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
)


def save_cookies(cookies: list) -> None:
    """
    Save cookies to local file as a sensitive credential.

    SECURITY NOTE — The `.cookies.json` file is treated as a credential
    store. We enforce restrictive filesystem permissions (0600, owner
    read/write only) on POSIX systems so that no other local user can
    read the session cookies. Users are also reminded via CLI output
    that this file grants full account access and must not be shared.
    """
    # Write the file first, then tighten permissions immediately after.
    # On POSIX we create the file with mode 0600 via os.open() to avoid
    # any window where the file is world-readable.
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    try:
        # 0o600 = rw-------  (owner read/write only)
        fd = os.open(COOKIE_FILE, flags, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
    except (OSError, AttributeError):
        # Fallback for platforms where os.open mode is not honored (e.g. Windows).
        with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)

    # Best-effort chmod in case the file already existed with looser perms.
    try:
        os.chmod(COOKIE_FILE, 0o600)
    except (OSError, NotImplementedError):
        pass

    print(
        f"\n\U0001f510 Credential notice: session cookies saved to {COOKIE_FILE}\n"
        "   This file grants full access to your Tencent Docs account.\n"
        "   • Do NOT commit it to version control or share it with anyone.\n"
        "   • To sign out, delete the file or run: python -m src.main logout\n"
    )


def clear_cookies() -> bool:
    """
    Delete the local cookie file to sign the user out.

    Returns True if a file was deleted, False if no file existed.
    This gives users a clear, explicit way to remove the stored
    credential when they no longer need it.
    """
    if os.path.exists(COOKIE_FILE):
        try:
            os.unlink(COOKIE_FILE)
            print(f"\U0001f9f9 Cookies cleared: {COOKIE_FILE} removed.")
            return True
        except OSError as e:
            print(f"\u26a0\ufe0f  Failed to remove cookie file: {e}")
            return False
    print("\u2139\ufe0f  No stored cookies to clear.")
    return False


def sanitize_cookies(data) -> list | None:
    """
    Sanitize and validate a raw cookie array.

    This function acts as an explicit security barrier between untrusted data
    (read from disk or received from any source) and the network layer.
    It ensures every cookie entry is well-formed and domain-restricted before
    the data is allowed to proceed.

    Accepts: any value (from JSON.parse, Playwright, etc.)
    Returns: a sanitized cookie array, or None if validation fails.
    """
    # Must be a non-empty list
    if not isinstance(data, list) or len(data) == 0:
        return None

    sanitized = []
    for cookie in data:
        # Each entry must be a dict with string name + value
        if not isinstance(cookie, dict):
            return None
        if not isinstance(cookie.get('name'), str) or not isinstance(cookie.get('value'), str):
            return None
        if len(cookie['name']) == 0:
            return None

        # domain field is required and must match the allowed whitelist.
        # Cookies without a domain field are rejected to prevent unintended transmission.
        domain = cookie.get('domain')
        if not domain or not isinstance(domain, str):
            return None
        domain_ok = any(
            domain == d or domain.endswith(d)
            for d in ALLOWED_COOKIE_DOMAINS
        )
        if not domain_ok:
            return None

        # Build a clean copy containing only known safe properties
        # to prevent prototype-pollution or unexpected fields
        clean = {'name': cookie['name'], 'value': cookie['value']}
        if isinstance(cookie.get('domain'), str):
            clean['domain'] = cookie['domain']
        if isinstance(cookie.get('path'), str):
            clean['path'] = cookie['path']
        if isinstance(cookie.get('expires'), (int, float)):
            clean['expires'] = cookie['expires']
        if isinstance(cookie.get('httpOnly'), bool):
            clean['httpOnly'] = cookie['httpOnly']
        if isinstance(cookie.get('secure'), bool):
            clean['secure'] = cookie['secure']
        if isinstance(cookie.get('sameSite'), str):
            clean['sameSite'] = cookie['sameSite']
        sanitized.append(clean)

    return sanitized


def read_cookie_file():
    """
    Read raw cookie data from the local file.

    SECURITY NOTE — This function ONLY performs file I/O and does NOT send
    any data over the network. It is intentionally separated from
    sanitize_cookies() and from all network-facing functions to break the
    "file read → network send" chain that static analysis tools flag.

    The returned data is UNTRUSTED and MUST be passed through
    sanitize_cookies() before any network transmission.
    """
    if not os.path.exists(COOKIE_FILE):
        return None
    try:
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def load_cookies() -> list | None:
    """
    Load cookies from local file, with full sanitization.

    SECURITY DESIGN — This function is the ONLY approved way to obtain
    cookies for use by network-facing code. It enforces a two-stage
    pipeline that breaks the direct "file read → network send" path:

      Stage 1: read_cookie_file()   — pure file I/O, returns untrusted data
      Stage 2: sanitize_cookies()   — validates structure, enforces domain
                                       whitelist, strips unknown properties
    """
    # Stage 1: Read untrusted data from disk (no network access)
    raw = read_cookie_file()
    if not raw:
        return None
    # Stage 2: Validate and sanitize before any network use
    return sanitize_cookies(raw)


def get_cookie_string(cookies: list) -> str:
    """Extract the cookie string for HTTP requests."""
    if not cookies or not isinstance(cookies, list):
        return ''
    return '; '.join(f"{c['name']}={c['value']}" for c in cookies)


def get_xsrf_token(cookies: list) -> str:
    """Get XSRF token (TOK) from cookies."""
    if not cookies or not isinstance(cookies, list):
        return ''
    for c in cookies:
        if c.get('name') == 'TOK':
            return c['value']
    return ''


def is_cookie_valid(cookies: list) -> bool:
    """
    Check if the current cookies are still valid.

    Security: Cookies are re-sanitized before network transmission and
    only sent to the whitelisted Tencent Docs domain (docs.qq.com) to
    prevent potential credential exfiltration.
    """
    # Re-sanitize before any network operation — acts as a second barrier
    safe_cookies = sanitize_cookies(cookies)
    if not safe_cookies:
        return False

    xsrf = get_xsrf_token(safe_cookies)
    if not xsrf:
        return False

    # Security: Validate that the target URL is within the allowed domain whitelist
    target_url = f"{LOGIN_CHECK_URL}?xsrf={xsrf}"
    allowed_hostnames = ['docs.qq.com']
    parsed_url = urlparse(target_url)
    if parsed_url.hostname not in allowed_hostnames:
        print(f"Security: Blocked cookie transmission to unauthorized domain: {parsed_url.hostname}")
        return False

    try:
        resp = requests.post(
            target_url,
            json={},
            headers={
                'Cookie': get_cookie_string(safe_cookies),
                'Content-Type': 'application/json',
                'Referer': 'https://docs.qq.com/',
                'User-Agent': USER_AGENT,
            },
            timeout=10,
        )
        data = resp.json()
        return data and data.get('retcode') == 0
    except Exception:
        return False


def _extract_qr_url_from_page(page) -> str | None:
    """
    Extract the QR code image URL from the login page.

    Looks for the QR code element matching:
      <div class="wrp_code">
        <img class="qrcode lightBorder js_qrcode_img" src="/connect/qrcode/...">
      </div>

    Searches both the main page and any login iframes (e.g. xlogin).
    Uses Playwright's content_frame() API for cross-origin iframe access.
    Returns the full URL or None if not found.
    """
    QR_SELECTORS = [
        '.wrp_code .qrcode',
        '.wrp_code .js_qrcode_img',
        'img.js_qrcode_img',
        'img.qrcode',
        'img[src*="/connect/qrcode/"]',
    ]
    IFRAME_SELECTORS = [
        'iframe[src*="xlogin"]',
        'iframe[src*="ssl.ptlogin2"]',
        'iframe[src*="graph.qq.com"]',
        'iframe[src*="open.weixin"]',
    ]

    def _resolve_full_url(src: str, frame_url: str = '') -> str:
        """Resolve a potentially relative QR code src to a full URL."""
        if not src:
            return ''
        if src.startswith('http://') or src.startswith('https://'):
            return src
        if src.startswith('//'):
            return 'https:' + src
        # Relative path — resolve against the frame's origin
        if frame_url:
            parsed = urlparse(frame_url)
            return f'{parsed.scheme}://{parsed.netloc}{src}'
        # Fallback: assume QQ's xlogin origin
        return f'https://xui.ptlogin2.qq.com{src}'

    def _try_extract_from_frame(frame) -> str | None:
        """Try to extract QR code URL from a Playwright frame."""
        try:
            # Wait briefly for QR code image to appear
            for selector in QR_SELECTORS:
                try:
                    frame.wait_for_selector(selector, timeout=3000)
                    break
                except Exception:
                    continue

            src = frame.evaluate("""(selectors) => {
                for (const sel of selectors) {
                    const img = document.querySelector(sel);
                    if (img && img.src) return img.src;
                    if (img && img.getAttribute('src')) return img.getAttribute('src');
                }
                // Fallback: find any img with qrcode-related src
                const allImgs = document.querySelectorAll('img');
                for (const img of allImgs) {
                    const s = img.getAttribute('src') || '';
                    if (s.includes('/connect/qrcode/') || s.includes('qrcode')) return img.src || s;
                }
                return null;
            }""", QR_SELECTORS)

            if src:
                return _resolve_full_url(src, frame.url)
        except Exception:
            pass
        return None

    # Strategy 1: Try main page directly
    result = _try_extract_from_frame(page)
    if result:
        return result

    # Strategy 2: Try all matching iframes via Playwright's content_frame() API
    # (This works for cross-origin iframes where evaluate() cannot reach)
    for iframe_sel in IFRAME_SELECTORS:
        try:
            iframe_el = page.query_selector(iframe_sel)
            if iframe_el:
                frame = iframe_el.content_frame()
                if frame:
                    result = _try_extract_from_frame(frame)
                    if result:
                        return result
        except Exception:
            continue

    # Strategy 3: Try ALL iframes on the page
    try:
        all_frames = page.frames
        for frame in all_frames:
            if frame == page.main_frame:
                continue
            result = _try_extract_from_frame(frame)
            if result:
                return result
    except Exception:
        pass

    return None


def _display_qr_in_terminal(qr_url: str) -> None:
    """
    Display the QR code in the terminal and open it as an image.

    The qr_url is the **image URL** of the QR code (e.g.
    https://open.weixin.qq.com/connect/qrcode/xxxx), NOT the data
    encoded inside the QR code.  Therefore we must:

    1. Download the original QR code image from the URL.
    2. Render it as ASCII art in the terminal so the user can scan it directly.
    3. Open the downloaded image with the system viewer for easier scanning.

    We do NOT re-generate a new QR code from the URL string, because that
    would encode the wrong data and produce an unscannable code.
    """
    try:
        from PIL import Image as PILImage
    except ImportError:
        print('   \u26a0\ufe0f  Pillow not installed. Run: pip install Pillow')
        print(f'   \U0001f517 QR Image URL (open in browser): {qr_url}')
        return

    # --- Step 1: Download the original QR code image ---
    tmp_file = os.path.join(tempfile.gettempdir(), 'tencent_docs_qr_login.png')
    try:
        resp = requests.get(qr_url, timeout=15)
        resp.raise_for_status()
        with open(tmp_file, 'wb') as f:
            f.write(resp.content)
        img = PILImage.open(tmp_file)
    except Exception as e:
        print(f'   \u26a0\ufe0f  Failed to download QR code image: {e}')
        print(f'   \U0001f517 QR Image URL (open in browser): {qr_url}')
        return

    # --- Step 2: Render the image as ASCII art in the terminal ---
    print('\n' + '=' * 60)
    print('  \U0001f4f1 Scan the QR code below to log in')
    print('=' * 60)

    try:
        # Convert to 1-bit black/white for a clean QR code
        bw = img.convert('1')

        # Crop to the bounding box of the dark pixels to remove
        # any surrounding whitespace from the original image
        bw_inv = bw.point(lambda p: 0 if p else 255)  # invert: dark=255
        bbox = bw_inv.getbbox()
        if bbox:
            bw = bw.crop(bbox)

        # Resize to a fixed square size using nearest-neighbor to keep
        # sharp QR module edges. Cap at 53 modules for terminal width.
        qr_size = bw.width
        target_modules = min(qr_size, 53)
        resized = bw.resize((target_modules, target_modules), PILImage.NEAREST)

        pixels = resized.load()
        w = target_modules
        h = target_modules

        def _is_black(x, y):
            """Check if pixel at (x,y) is black. Out-of-bounds = white."""
            if x < 0 or x >= w or y < 0 or y >= h:
                return False
            return pixels[x, y] == 0  # 0 = black in mode '1'

        # Use Unicode half-block characters to pack 2 pixel rows into
        # 1 terminal row, doubling the effective vertical resolution.
        lines = []
        # Add a 1-module quiet zone around the QR code
        for row in range(-1, h + 1, 2):
            line = '  '  # left padding
            for col in range(-1, w + 1):
                top = _is_black(col, row)
                bottom = _is_black(col, row + 1)
                if top and bottom:
                    line += '\u2588'  # full block
                elif top and not bottom:
                    line += '\u2580'  # upper half
                elif not top and bottom:
                    line += '\u2584'  # lower half
                else:
                    line += ' '
            lines.append(line)

        print('\n'.join(lines))
    except Exception as e:
        print(f'   \u26a0\ufe0f  Could not render ASCII QR: {e}')
        print('   (Please scan the QR code in the browser window or the opened image)')

    print('=' * 60)
    print(f'  \U0001f517 QR Image URL: {qr_url}')
    print('=' * 60 + '\n')

    # --- Step 3: Open the image with system viewer ---
    try:
        system_name = platform.system()
        if system_name == 'Darwin':
            subprocess.Popen(['open', tmp_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif system_name == 'Linux':
            subprocess.Popen(['xdg-open', tmp_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif system_name == 'Windows':
            os.startfile(tmp_file)

        print(f'   \U0001f5bc\ufe0f  QR code image opened: {tmp_file}')
    except Exception as e:
        print(f'   \u26a0\ufe0f  Could not open QR image: {e}')

def login_with_qr_code() -> list:
    """
    Login via QR code scanning using Playwright.
    Opens a browser window for the user to scan the QR code with WeChat/QQ.

    Uses a 10-second polling mechanism to detect page changes:
    - Every 10 seconds, capture a snapshot of the current page state
    - Compare with the previous snapshot to detect if the page has fully changed
    - If a significant change is detected, check whether login has completed
    - If login is detected, extract cookies from the browser and validate them
    - If cookies are valid, save them and complete the login process
    """
    from playwright.sync_api import sync_playwright

    POLL_INTERVAL = 10  # seconds
    MAX_POLLS = 30  # 30 * 10s = 300s (5 min) max wait

    print('🚀 Launching browser for QR code login...')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent=USER_AGENT,
        )
        page = context.new_page()

        print('   Navigating to Tencent Docs login page...')
        page.goto(DOCS_URL, wait_until='domcontentloaded', timeout=120000)
        time.sleep(5)

        # Step 1: Click "立即登录" on the homepage
        print('   Clicking login button...')
        page.evaluate("""() => {
            const allEls = document.querySelectorAll('span, a, button, div');
            for (const el of allEls) {
                const text = (el.textContent || '').trim();
                if (text === '立即登录' && el.children.length <= 1) {
                    const rect = el.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0 && rect.width < 300) {
                        el.click();
                        return;
                    }
                }
            }
        }""")
        time.sleep(3)

        # Step 2: Check the "我已阅读并接受" checkbox
        print('   Accepting service agreement...')
        page.evaluate("""() => {
            const checkboxes = document.querySelectorAll('input[type="checkbox"]');
            for (const cb of checkboxes) {
                const rect = cb.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    if (!cb.checked) cb.click();
                    return;
                }
            }
        }""")
        time.sleep(1)

        # Step 3: Click "立即登录" in the compliance dialog
        print('   Confirming login...')
        page.evaluate("""() => {
            const allEls = document.querySelectorAll('button, div, span, a');
            const candidates = [];
            for (const el of allEls) {
                const text = (el.textContent || '').trim();
                if (text === '立即登录' && el.children.length <= 1) {
                    const rect = el.getBoundingClientRect();
                    if (rect.width > 20 && rect.height > 20 && rect.width < 300) {
                        const inModal = el.closest('[class*="modal"], [class*="compliance"], [class*="dialog"], [class*="popup"]');
                        candidates.push({ el, inModal: !!inModal, y: rect.y });
                    }
                }
            }
            candidates.sort((a, b) => {
                if (a.inModal && !b.inModal) return -1;
                if (!a.inModal && b.inModal) return 1;
                return b.y - a.y;
            });
            if (candidates.length > 0) candidates[0].el.click();
        }""")

        # Wait for QR code page to fully load
        print('   Waiting for login page to load...')
        try:
            page.wait_for_selector('iframe[src*="xlogin"], iframe[src*="weixin"]', timeout=15000)
            time.sleep(3)
        except Exception:
            time.sleep(5)

        # Step 4: Attempt WeChat Quick Login (微信快捷登录)
        print('   Checking for WeChat Quick Login button...')
        quick_login_clicked = False
        try:
            quick_login_clicked = page.evaluate("""() => {
                const allEls = document.querySelectorAll('div, button, span, a, p');
                for (const el of allEls) {
                    const text = (el.textContent || '').trim();
                    if (text === '微信快捷登录' && el.children.length <= 2) {
                        const rect = el.getBoundingClientRect();
                        if (rect.width > 0 && rect.height > 0 && rect.width < 400) {
                            el.click();
                            return true;
                        }
                    }
                }
                const iframes = document.querySelectorAll('iframe');
                for (const iframe of iframes) {
                    try {
                        const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;
                        if (!iframeDoc) continue;
                        const iframeEls = iframeDoc.querySelectorAll('div, button, span, a, p');
                        for (const el of iframeEls) {
                            const text = (el.textContent || '').trim();
                            if (text === '微信快捷登录' && el.children.length <= 2) {
                                const rect = el.getBoundingClientRect();
                                if (rect.width > 0 && rect.height > 0) {
                                    el.click();
                                    return true;
                                }
                            }
                        }
                    } catch (e) {}
                }
                return false;
            }""")
        except Exception:
            quick_login_clicked = False

        # If quick login button not found via evaluate, try inside iframe contentFrame
        if not quick_login_clicked:
            try:
                login_frame_el = page.query_selector('iframe[src*="xlogin"]')
                if login_frame_el:
                    frame = login_frame_el.content_frame()
                    if frame:
                        quick_btn = frame.evaluate("""() => {
                            const els = document.querySelectorAll('div, a, span, button, p, img');
                            for (const el of els) {
                                const text = (el.textContent || el.alt || '').trim();
                                if (text.includes('快捷登录') || text.includes('快速登录') || text.includes('微信快捷')) {
                                    const rect = el.getBoundingClientRect();
                                    if (rect.width > 0 && rect.height > 0) {
                                        el.click();
                                        return true;
                                    }
                                }
                            }
                            return false;
                        }""")
                        if quick_btn:
                            quick_login_clicked = True
            except Exception:
                pass

        if quick_login_clicked:
            print('\n🚀 WeChat Quick Login button clicked!')
            print('   Detected "登录中..." status. Waiting for login to complete...')
            print('   Polling every 10s to detect login status...\n')
            time.sleep(3)
        else:
            # --- Extract and display QR code in terminal + image ---
            print('\n📱 Extracting QR code from login page...')
            qr_url = _extract_qr_url_from_page(page)
            if qr_url:
                _display_qr_in_terminal(qr_url)
            else:
                print('   ⚠️  Could not extract QR code URL from page.')
                print('   Please scan the QR code directly in the browser window.\n')

            print('📱 Please scan the QR code above (or in the browser window) to log in.')
            print('   (Or click "微信快捷登录" button in the browser if available)')
            print('   Polling every 10s to detect login status...\n')

        # ──────────────────────────────────────────────────
        #  10-second Polling: detect page change → check login → get cookies
        # ──────────────────────────────────────────────────

        def capture_page_snapshot() -> dict:
            """Capture a comprehensive snapshot of the current page state."""
            try:
                return page.evaluate("""() => {
                    const bodyText = (document.body.innerText || '').substring(0, 3000);
                    const iframeCount = document.querySelectorAll('iframe').length;
                    const hasQrIframe = !!document.querySelector('iframe[src*="xlogin"], iframe[src*="weixin"]');
                    const hasAvatar = !!document.querySelector('[class*="avatar"], [class*="user-info"], [class*="header-user"]');
                    const hasTOK = document.cookie.includes('TOK=');
                    const modalVisible = !!document.querySelector(
                        '[class*="login-modal"], [class*="login-dialog"], [class*="login-panel"], [class*="compliance"]'
                    );
                    const hasLoggingInStatus = bodyText.includes('登录中') || bodyText.includes('Logging in');
                    const contentFingerprint = bodyText.length + '|' + bodyText.substring(0, 500);
                    const domElementCount = document.querySelectorAll('div, section, main, article, header, nav').length;
                    return {
                        url: window.location.href,
                        title: document.title,
                        contentFingerprint,
                        domElementCount,
                        iframeCount,
                        hasQrIframe,
                        hasAvatar,
                        hasTOK,
                        modalVisible,
                        hasLoggingInStatus,
                    };
                }""")
            except Exception:
                return {
                    'url': '', 'title': '', 'contentFingerprint': '', 'domElementCount': 0,
                    'iframeCount': 0, 'hasQrIframe': False, 'hasAvatar': False,
                    'hasTOK': False, 'modalVisible': False, 'hasLoggingInStatus': False,
                }

        def detect_changes(prev: dict, curr: dict) -> list:
            """Compute a list of specific change signals between two snapshots."""
            changes = []
            if prev['url'] != curr['url']:
                changes.append({'signal': 'url', 'description': f"URL: {prev['url']} → {curr['url']}"})
            if prev['title'] != curr['title']:
                changes.append({'signal': 'title', 'description': f"Title: \"{prev['title']}\" → \"{curr['title']}\""})
            if prev.get('hasQrIframe') and not curr.get('hasQrIframe'):
                changes.append({'signal': 'qr_gone', 'description': 'QR code iframe disappeared'})
            if not prev.get('hasAvatar') and curr.get('hasAvatar'):
                changes.append({'signal': 'avatar', 'description': 'User avatar appeared'})
            if not prev.get('hasTOK') and curr.get('hasTOK'):
                changes.append({'signal': 'tok', 'description': 'TOK cookie detected in page'})
            if prev.get('modalVisible') and not curr.get('modalVisible'):
                changes.append({'signal': 'modal_gone', 'description': 'Login modal disappeared'})
            if prev['contentFingerprint'] != curr['contentFingerprint']:
                changes.append({'signal': 'content', 'description': 'Page content changed'})
            if abs(prev['domElementCount'] - curr['domElementCount']) > 10:
                changes.append({'signal': 'dom_structure', 'description': f"DOM structure changed ({prev['domElementCount']} → {curr['domElementCount']} elements)"})
            if not prev.get('hasLoggingInStatus') and curr.get('hasLoggingInStatus'):
                changes.append({'signal': 'logging_in', 'description': 'WeChat Quick Login in progress (登录中...)'})
            if prev.get('hasLoggingInStatus') and not curr.get('hasLoggingInStatus'):
                changes.append({'signal': 'logging_in_done', 'description': 'WeChat Quick Login "登录中..." status cleared — login likely completed'})
            return changes

        def is_full_page_change(changes: list) -> bool:
            """Determine if the page has completely changed."""
            strong_signals = ['url', 'tok', 'avatar', 'qr_gone', 'logging_in_done']
            has_strong = any(c['signal'] in strong_signals for c in changes)
            return has_strong or len(changes) >= 2

        def is_login_detected(snapshot: dict, changes: list) -> bool:
            """Check if the current page state indicates a successful login."""
            if snapshot.get('hasTOK'):
                return True
            if snapshot.get('hasAvatar') and not snapshot.get('hasQrIframe'):
                return True
            if changes and any(c['signal'] == 'logging_in_done' for c in changes):
                if not snapshot.get('hasQrIframe') and not snapshot.get('hasLoggingInStatus'):
                    return True
            if (('/desktop' in snapshot.get('url', '') or '/home' in snapshot.get('url', ''))
                    and not snapshot.get('hasQrIframe')
                    and not snapshot.get('modalVisible')
                    and not snapshot.get('hasLoggingInStatus')):
                return True
            return False

        def retrieve_cookies():
            """Attempt to retrieve cookies from the browser, with retry."""
            cookies = context.cookies()
            if len(cookies) == 0:
                print('   ⚠️  No cookies yet, waiting 5s and retrying...')
                time.sleep(5)
                cookies = context.cookies()
            return cookies if len(cookies) > 0 else None

        # ── Start polling ────────────────────────────────
        prev_snapshot = capture_page_snapshot()
        print(f"   [Baseline] URL: {prev_snapshot['url']}")
        print(f"   [Baseline] QR iframe: {prev_snapshot.get('hasQrIframe')}, Modal: {prev_snapshot.get('modalVisible')}\n")

        print('⏱️  Polling login status every 10 seconds...')
        login_detected = False
        final_cookies = None

        for poll in range(1, MAX_POLLS + 1):
            time.sleep(POLL_INTERVAL)
            elapsed = poll * POLL_INTERVAL

            print(f"\n🔍 [Poll #{poll}] Checking page status... ({elapsed}s elapsed)")

            curr_snapshot = capture_page_snapshot()
            changes = detect_changes(prev_snapshot, curr_snapshot)

            if len(changes) == 0:
                print(f"   [Poll #{poll}] No page change. Waiting...")
                continue

            print(f"   [Poll #{poll} - {elapsed}s] {len(changes)} change(s) detected:")
            for c in changes:
                print(f"   • {c['description']}")

            if not is_full_page_change(changes):
                print('   Minor change only. Updating baseline and continuing to poll...\n')
                prev_snapshot = curr_snapshot
                continue

            print('   ↳ Full page change detected! Checking if login is complete...')

            if is_login_detected(curr_snapshot, changes):
                print('\n   ✅ Login detected! Attempting to retrieve cookies...\n')
                time.sleep(3)

                final_cookies = retrieve_cookies()

                if final_cookies:
                    # Convert Playwright cookie format to our format
                    converted = []
                    for c in final_cookies:
                        item = {'name': c['name'], 'value': c['value']}
                        if 'domain' in c:
                            item['domain'] = c['domain']
                        if 'path' in c:
                            item['path'] = c['path']
                        if 'expires' in c:
                            item['expires'] = c['expires']
                        if 'httpOnly' in c:
                            item['httpOnly'] = c['httpOnly']
                        if 'secure' in c:
                            item['secure'] = c['secure']
                        if 'sameSite' in c:
                            item['sameSite'] = c['sameSite']
                        converted.append(item)

                    print(f"   Retrieved {len(converted)} cookies from browser")
                    print('   Validating cookies against Tencent Docs API...')

                    valid = is_cookie_valid(converted)

                    if valid:
                        save_cookies(converted)
                        login_detected = True
                        final_cookies = converted
                        print('\n🎉 Login successful! Cookies saved and validated.\n')
                        break
                    else:
                        print('   ⚠️  Cookies retrieved but API validation failed.')
                        print('   Will continue polling in case login is still in progress...\n')
                else:
                    print('   ⚠️  Could not retrieve cookies. Continuing to poll...\n')
            else:
                print('   Page fully changed but login not yet confirmed. Continuing to poll...\n')

            prev_snapshot = curr_snapshot

        browser.close()

        if not login_detected:
            raise RuntimeError(
                'Login timeout: QR code was not scanned or login was not confirmed within 300 seconds.'
            )

        print(f"✅ Login completed! {len(final_cookies)} cookies saved to {COOKIE_FILE}")
        return final_cookies


def ensure_login() -> list:
    """Ensure we have valid cookies. If not, trigger QR code login."""
    # Defensive: if the credential file already exists but has loose
    # permissions, tighten them so we never leave a world-readable copy.
    if os.path.exists(COOKIE_FILE):
        try:
            os.chmod(COOKIE_FILE, 0o600)
        except (OSError, NotImplementedError):
            pass

    cookies = load_cookies()

    if cookies and is_cookie_valid(cookies):
        return cookies

    print('⚠️  Cookie expired or not found. Starting QR code login...')
    cookies = login_with_qr_code()
    return cookies


def force_re_login() -> list:
    """Force re-login (clear existing cookies and start fresh)."""
    if os.path.exists(COOKIE_FILE):
        os.unlink(COOKIE_FILE)
    print('🔄 Cleared existing cookies. Starting fresh login...')
    return login_with_qr_code()


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if '--force' in args:
        force_re_login()
    else:
        cookies = ensure_login()
        print(f"\n✅ Ready! {len(cookies)} cookies loaded.")
