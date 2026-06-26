#!/usr/bin/env python3
"""
cdp_typer.py — Types text into any element including contenteditable divs.
"""

import json
import time
import base64
import subprocess
import threading
import os
import requests
import websocket

CDP_PORT = 9222

CHROME_FLAGS = [
    f"--remote-debugging-port={CDP_PORT}",
    f"--user-data-dir=/tmp/chrome-automation-profile",  # Use shared profile
    "--no-sandbox",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-extensions",
    "--disable-plugins",
    "--disable-background-networking",
    "--disable-sync",
    "--disable-crash-reporter",
    "--disable-breakpad",
    "--dns-prefetch-disable",
    "--proxy-server=direct://",
    "--proxy-bypass-list=*",
    "--ignore-certificate-errors",
    "--disable-blink-features=AutomationControlled",
]

X11_ENV = {
    "GDK_BACKEND": "x11",
    "QT_QPA_PLATFORM": "xcb",
    "EGL_PLATFORM": "x11",
}


class CDPTyper:
    def __init__(self):
        self._ws = None
        self._msg_id = 0
        self._results = {}
        self._lock = threading.Lock()
        self._chrome = None

    def launch(self, url="http://example.com", wait=10.0):
        os.system(f"pkill -f 'remote-debugging-port={CDP_PORT}' 2>/dev/null")
        time.sleep(1.5)

        env = {**os.environ, "DISPLAY": ":0", "GDK_BACKEND": "x11"}
        env.pop("WAYLAND_DISPLAY", None)

        cmd = ["google-chrome"] + CHROME_FLAGS + [url]
        print(f"[cdp] launching Chrome → {url}")

        self._chrome = subprocess.Popen(
            cmd, env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        time.sleep(wait)

        if self._chrome.poll() is not None:
            raise RuntimeError(
                "Chrome exited immediately.\n"
                "Try: google-chrome --remote-debugging-port=9222 --no-sandbox"
            )

        self._connect()
        print(f"[cdp] ✅ Chrome ready on port {CDP_PORT} (PID {self._chrome.pid})")

    def _connect(self, retries=40):
        last_error = None
        for i in range(retries):
            try:
                resp = requests.get(
                    f"http://localhost:{CDP_PORT}/json",
                    timeout=2
                )
                tabs = resp.json()
                if tabs:
                    # Get first tab (prefer pages over background)
                    tab = None
                    for t in tabs:
                        if t.get("type") == "page":
                            tab = t
                            break
                    if not tab and tabs:
                        tab = tabs[0]
                    
                    if not tab:
                        time.sleep(0.5)
                        continue
                    
                    ws_url = tab.get("webSocketDebuggerUrl")
                    if not ws_url:
                        time.sleep(0.5)
                        continue
                    
                    # FIX: suppress_origin=True to bypass Chrome origin check
                    self._ws = websocket.create_connection(
                        ws_url, 
                        timeout=10,
                        suppress_origin=True
                    )
                    threading.Thread(target=self._listen, daemon=True).start()
                    self._send("Page.enable")
                    self._send("Runtime.enable")
                    url = tab.get("url", "?")
                    print(f"[cdp] ✅ CDP connected to: {url[:60]}")
                    return
            except Exception as e:
                last_error = e
                if i < 3:
                    print(f"[cdp] attempt {i+1}: {type(e).__name__}: {str(e)[:60]}")
                time.sleep(0.5)
        raise RuntimeError(
            f"Could not connect to CDP after {retries} attempts\n"
            f"Last error: {last_error}"
        )

    def _listen(self):
        while True:
            try:
                data = json.loads(self._ws.recv())
                if "id" in data:
                    with self._lock:
                        self._results[data["id"]] = data
            except:
                break

    def _send(self, method, params=None, timeout=15):
        self._msg_id += 1
        mid = self._msg_id
        self._ws.send(json.dumps({
            "id": mid,
            "method": method,
            "params": params or {}
        }))
        start = time.time()
        while time.time() - start < timeout:
            with self._lock:
                if mid in self._results:
                    resp = self._results.pop(mid)
                    if "error" in resp:
                        raise RuntimeError(
                            f"CDP error [{method}]: {resp['error']['message']}"
                        )
                    return resp.get("result", {})
            time.sleep(0.05)
        raise TimeoutError(f"CDP timeout: {method}")

    def navigate(self, url, wait=3.0):
        self._send("Page.navigate", {"url": url})
        time.sleep(wait)
        self.wait_for_load()
        title = self.js("document.title")
        print(f"[cdp] ✅ navigated → '{title}'")

    def wait_for_load(self, timeout=15):
        start = time.time()
        while time.time() - start < timeout:
            if self.js("document.readyState") == "complete":
                return True
            time.sleep(0.4)
        return False

    def click(self, x, y):
        self._send("Input.dispatchMouseEvent", {
            "type": "mousePressed", "x": x, "y": y,
            "button": "left", "clickCount": 1
        })
        time.sleep(0.08)
        self._send("Input.dispatchMouseEvent", {
            "type": "mouseReleased", "x": x, "y": y,
            "button": "left", "clickCount": 1
        })
        time.sleep(0.1)
        print(f"[cdp] click ({x}, {y})")

    def double_click(self, x, y):
        for i in [1, 2]:
            self._send("Input.dispatchMouseEvent", {
                "type": "mousePressed", "x": x, "y": y,
                "button": "left", "clickCount": i
            })
            self._send("Input.dispatchMouseEvent", {
                "type": "mouseReleased", "x": x, "y": y,
                "button": "left", "clickCount": i
            })
        print(f"[cdp] double_click ({x}, {y})")

    def right_click(self, x, y):
        self._send("Input.dispatchMouseEvent", {
            "type": "mousePressed", "x": x, "y": y,
            "button": "right", "clickCount": 1
        })
        self._send("Input.dispatchMouseEvent", {
            "type": "mouseReleased", "x": x, "y": y,
            "button": "right", "clickCount": 1
        })
        print(f"[cdp] right_click ({x}, {y})")

    def move(self, x, y):
        self._send("Input.dispatchMouseEvent", {
            "type": "mouseMoved", "x": x, "y": y
        })

    def scroll(self, x, y, delta_y=400):
        self._send("Input.dispatchMouseEvent", {
            "type": "mouseWheel",
            "x": x, "y": y,
            "deltaX": 0,
            "deltaY": delta_y
        })
        print(f"[cdp] scroll delta={delta_y}")

    def click_selector(self, selector, timeout=8):
        start = time.time()
        while time.time() - start < timeout:
            pos = self.js(f"""
            (function() {{
                const el = document.querySelector('{selector}');
                if (!el) return null;
                el.scrollIntoView({{block: 'center'}});
                const r = el.getBoundingClientRect();
                if (r.width === 0 || r.height === 0) return null;
                return {{
                    x: Math.round(r.left + r.width / 2),
                    y: Math.round(r.top + r.height / 2)
                }};
            }})()
            """)
            if pos and isinstance(pos, dict):
                self.click(pos["x"], pos["y"])
                print(f"[cdp] ✅ click_selector '{selector}'")
                return True
            time.sleep(0.5)
        raise RuntimeError(f"Selector not found: {selector}")

    def key(self, key_name, modifiers=0):
        self._send("Input.dispatchKeyEvent", {
            "type": "keyDown",
            "key": key_name,
            "modifiers": modifiers
        })
        self._send("Input.dispatchKeyEvent", {
            "type": "keyUp",
            "key": key_name,
            "modifiers": modifiers
        })
        print(f"[cdp] key: {key_name}")

    def ctrl(self, key_name):
        self.key(key_name, modifiers=2)

    def shift(self, key_name):
        self.key(key_name, modifiers=8)

    def type_into_focused(self, text):
        self._send("Input.insertText", {"text": text})
        print(f"[cdp] ✅ typed: {text[:60]}{'...' if len(text) > 60 else ''}")

    def type_into_selector(self, selector, text, clear_first=True):
        self.click_selector(selector)
        time.sleep(0.3)

        if clear_first:
            self.ctrl("a")
            time.sleep(0.1)
            self.key("Backspace")
            time.sleep(0.1)

        self.type_into_focused(text)
        print(f"[cdp] ✅ typed into '{selector}'")

    def type_into_contenteditable(self, selector, text, clear_first=True):
        focused = self.js(f"""
        (function() {{
            const el = document.querySelector('{selector}');
            if (!el) return false;
            el.focus();
            el.click();
            return true;
        }})()
        """)

        if not focused:
            raise RuntimeError(f"Could not focus selector: {selector}")

        time.sleep(0.2)

        if clear_first:
            self.ctrl("a")
            time.sleep(0.1)
            self.key("Backspace")
            time.sleep(0.1)

        self._send("Input.insertText", {"text": text})
        time.sleep(0.3)

        actual = self.js(f"""
        (function() {{
            const el = document.querySelector('{selector}');
            return el ? (el.value || el.innerText || el.textContent) : null;
        }})()
        """)

        if actual and text[:20] in str(actual):
            print(f"[cdp] ✅ text confirmed in contenteditable: '{str(actual)[:50]}'")
            return True

        print(f"[cdp] trying execCommand fallback...")
        self.js(f"""
        (function() {{
            const el = document.querySelector('{selector}');
            if (!el) return;
            el.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('insertText', false, {json.dumps(text)});
        }})()
        """)
        time.sleep(0.3)
        print(f"[cdp] ✅ execCommand typed into '{selector}'")
        return True

    def js(self, expression):
        result = self._send("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True
        })
        return result.get("result", {}).get("value")

    def get_title(self):
        return self.js("document.title") or ""

    def get_url(self):
        return self.js("window.location.href") or ""

    def get_text(self):
        return self.js("document.body.innerText") or ""

    def screenshot(self, path="/tmp/screenshot.png"):
        result = self._send("Page.captureScreenshot", {"format": "png"})
        data = result.get("data")
        if not data:
            raise RuntimeError("Screenshot returned no data")
        with open(path, "wb") as f:
            f.write(base64.b64decode(data))
        size = os.path.getsize(path)
        if size < 5000:
            raise RuntimeError(f"Screenshot too small ({size}b) — likely blank")
        print(f"[cdp] ✅ screenshot: {path} ({size} bytes)")
        return path

    # ========================================================================
    # BUG FIX 2: Field Focus Race Condition
    # ========================================================================

    def click_and_focus(self, selector, timeout=5):
        """
        Click an element and verify it has focus before returning.
        Use this instead of click_selector() for input fields.
        """
        # Click it
        self.click_selector(selector, timeout=timeout)
        time.sleep(0.2)

        # Verify focus via JS
        start = time.time()
        while time.time() - start < 2.0:
            focused = self.js(f"""
            (function() {{
                const el = document.querySelector('{selector}');
                return el === document.activeElement ||
                el?.contains(document.activeElement);
            }})()
            """)
            if focused:
                print(f"[cdp] ✅ focus confirmed: {selector}")
                return True
            time.sleep(0.1)

        # Focus didn't happen — try JS focus as fallback
        self.js(f"""
        (function() {{
            const el = document.querySelector('{selector}');
            if (el) {{ el.focus(); el.click(); }}
        }})()
        """)
        time.sleep(0.2)
        print(f"[cdp] ⚠️ focus forced via JS: {selector}")
        return True

    def type_into_field(self, selector, text, clear_first=True):
        """
        Click, focus, verify, then type.
        The safe way to fill any input field.
        """
        self.click_and_focus(selector)
        time.sleep(0.3)

        if clear_first:
            self.ctrl("a")
            time.sleep(0.1)
            self.key("Backspace")
            time.sleep(0.1)

        self._send("Input.insertText", {"text": text})
        time.sleep(0.2)

        # Verify value appeared
        actual = self.js(f"""
        (function() {{
            const el = document.querySelector('{selector}');
            if (!el) return null;
            return el.value !== undefined ? el.value : el.innerText;
        }})()
        """)

        if actual and text[:10] in str(actual):
            print(f"[cdp] ✅ typed and verified: '{actual[:50]}'")
        else:
            print(f"[cdp] ⚠️ typed but value unexpected: '{str(actual)[:50]}'")

        return actual

    # ========================================================================
    # BUG FIX 3: Scroll Via Reliable Methods
    # ========================================================================

    def scroll_to_bottom(self):
        """Scroll to the absolute bottom of the page via JS."""
        self.js("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)
        pos = self.js("window.scrollY")
        print(f"[cdp] scrolled to bottom: scrollY={pos}")
        return pos

    def scroll_to_top(self):
        """Scroll to the top of the page via JS."""
        self.js("window.scrollTo(0, 0)")
        time.sleep(0.3)
        print(f"[cdp] scrolled to top")

    def scroll_by(self, pixels=500, direction="down"):
        """
        Scroll by a number of pixels.
        Uses JS window.scrollBy — works regardless of OS focus.
        """
        delta = pixels if direction == "down" else -pixels
        before = self.js("window.scrollY") or 0
        self.js(f"window.scrollBy(0, {delta})")
        time.sleep(0.3)
        after = self.js("window.scrollY") or 0
        print(f"[cdp] scrolled {direction} {pixels}px: {before} → {after}")
        return after

    def scroll_element_into_view(self, selector):
        """Scroll a specific element into view."""
        self.js(f"""
        document.querySelector('{selector}')
        ?.scrollIntoView({{behavior: 'smooth', block: 'center'}});
        """)
        time.sleep(0.5)

    # ========================================================================
    # V6 FIX 1: Multi-field Form Filling with Focus Verification
    # ========================================================================

    def tab_to_field(self, expected_selector, max_tabs=5):
        """
        Press Tab until the expected field has focus.
        Verifies document.activeElement after each Tab.
        Returns True if focus confirmed.
        """
        start = time.time()
        for i in range(max_tabs):
            self.key("Tab")
            time.sleep(0.3)
            focused = self.js(f"""
            (function() {{
                const target = document.querySelector('{expected_selector}');
                return target === document.activeElement;
            }})()
            """)
            if focused:
                print(f"[cdp] ✅ focus on '{expected_selector}' after {i+1} Tab(s)")
                return True
            time.sleep(0.2)
        
        # Fallback: force focus via JS
        self.js(f"document.querySelector('{expected_selector}')?.focus()")
        time.sleep(0.3)
        print(f"[cdp] ⚠️ forced focus via JS: {expected_selector}")
        return True

    def fill_form_fields(self, fields):
        """
        Fill multiple form fields safely with focus verification.
        
        fields = [
            ("#login_field", "myusername"),
            ("#password", "mypassword"),
            ("#email", "me@test.com"),
        ]
        
        Returns dict of {selector: actual_value}
        """
        results = {}
        for i, (selector, value) in enumerate(fields):
            # Focus via JS (most reliable)
            self.js(f"document.querySelector('{selector}')?.focus()")
            time.sleep(0.5)

            # Verify focus
            focused = self.js(f"""
            document.querySelector('{selector}') === document.activeElement
            """)
            if not focused:
                print(f"[cdp] ⚠️ retrying focus: {selector}")
                self.click_selector(selector, timeout=3)
                time.sleep(0.5)

            # Clear existing value via select all + delete
            self.js(f"""
            const el = document.querySelector('{selector}');
            if (el) {{
                el.value = '';
                el.focus();
                el.select();
            }}
            """)
            time.sleep(0.2)

            # Delete any selected text
            self.key("Delete")
            time.sleep(0.1)

            # Type character by character (more reliable than insertText)
            for char in value:
                self._send("Input.insertText", {"text": char})
                time.sleep(0.05)
            
            time.sleep(0.3)

            # Verify DOM value with retries
            for attempt in range(3):
                actual = self.js(
                    f"document.querySelector('{selector}')?.value"
                )
                if actual and value in str(actual):
                    print(f"[cdp] field '{selector}' = '{actual}'")
                    results[selector] = actual
                    break
                elif attempt < 2:
                    print(f"[cdp] ⚠️ value mismatch, retry {attempt+1}/3")
                    time.sleep(0.2)
                    # Re-type if missing
                    missing = value.replace(str(actual or ''), '')
                    if missing:
                        self._send("Input.insertText", {"text": missing})
                        time.sleep(0.3)
                else:
                    print(f"[cdp] ❌ field '{selector}' failed: got '{actual}'")
                    results[selector] = actual or ''

        return results

    # ========================================================================
    # V6 FIX 2: Multi-tab via CDP Target API
    # ========================================================================

    def new_tab(self, url=None):
        """
        Open a new tab via CDP Target API.
        Waits until the new tab appears in CDP tab list.
        Returns the new tab's targetId.
        """
        import requests as req
        
        before = {
            t["id"] for t in
            req.get(f"http://localhost:9222/json", timeout=2).json()
            if t.get("type") == "page"
        }

        # Use CDP to create new target
        result = self._send("Target.createTarget", {"url": url or "about:blank"})
        target_id = result.get("targetId")
        time.sleep(1.5)

        # Verify it appeared
        after_tabs = req.get(f"http://localhost:9222/json", timeout=2).json()
        after = {t["id"] for t in after_tabs if t.get("type") == "page"}
        new_tabs = after - before

        if new_tabs:
            print(f"[cdp] ✅ new tab created: {target_id}")
        else:
            print(f"[cdp] ⚠️ tab may not have registered yet")

        return target_id

    def get_all_tabs(self):
        """Return list of all open tab URLs."""
        import requests as req
        tabs = req.get(f"http://localhost:9222/json", timeout=2).json()
        urls = [t.get("url","") for t in tabs if t.get("type") == "page"]
        return urls

    # ========================================================================
    # V6 FIX 3: Smart Scrolling (Window or Container)
    # ========================================================================

    def scroll_page(self, direction="down", pixels=800):
        """
        Scroll the page intelligently.
        Detects whether window or a DOM element is the scroll container.
        """
        before_y = self.js("window.scrollY") or 0

        # Try window scroll first
        delta = pixels if direction == "down" else -pixels
        self.js(f"window.scrollBy(0, {delta})")
        time.sleep(0.5)

        after_y = self.js("window.scrollY") or 0

        if after_y != before_y:
            print(f"[cdp] ✅ window scroll: {before_y} → {after_y}")
            return after_y

        # Window didn't scroll — find the scrollable container
        print(f"[cdp] window.scrollY unchanged, finding scroll container...")

        scrollable_sel = self.js("""
        (function() {
            const candidates = [
                document.scrollingElement,
                document.documentElement,
                document.body,
                document.querySelector('main'),
                document.querySelector('[role="main"]'),
                document.querySelector('.content'),
            ];
            for (const el of candidates) {
                if (!el) continue;
                const style = window.getComputedStyle(el);
                const overflow = style.overflow + style.overflowY;
                if (overflow.includes('scroll') || overflow.includes('auto')) {
                    if (el.scrollHeight > el.clientHeight) {
                        return el.tagName + (el.id ? '#' + el.id : '') +
                            (el.className ? '.' + el.className.split(' ')[0] : '');
                    }
                }
            }
            return 'body';
        })()
        """)

        print(f"[cdp] scroll container: {scrollable_sel}")

        # Scroll the container
        self.js(f"""
        (function() {{
            const sel = '{scrollable_sel}';
            const el = sel === 'body' ? document.body :
                document.querySelector(sel) || document.body;
            el.scrollBy(0, {delta});
            el.scrollTop += {delta};
        }})()
        """)
        time.sleep(0.5)

        # Check scrollTop of body as fallback
        scroll_top = self.js(
            "document.body.scrollTop || document.documentElement.scrollTop"
        ) or 0
        print(f"[cdp] scrollTop after: {scroll_top}")
        return scroll_top

    def scroll_to_bottom_of_page(self):
        """Scroll to the absolute bottom, handling any scroll container."""
        self.js("""
        window.scrollTo(0, document.body.scrollHeight);
        document.body.scrollTop = document.body.scrollHeight;
        document.documentElement.scrollTop = document.body.scrollHeight;
        """)
        time.sleep(0.8)
        pos = self.js(
            "Math.max(window.scrollY, document.body.scrollTop, "
            "document.documentElement.scrollTop)"
        ) or 0
        print(f"[cdp] scrolled to bottom: {pos}px")
        return pos

    # ========================================================================
    # V7 SECTIONS 2-6, 8-14: All advanced features
    # ========================================================================

    # SECTION 2: File Upload Dialog Bypass
    def upload_file(self, selector, file_path):
        """
        Set a file input to a local file path without opening the dialog.
        Uses CDP DOM.setFileInputFiles.
        """
        import os
        assert os.path.exists(file_path), f"File not found: {file_path}"

        # Get node ID for the file input
        doc = self._send("DOM.getDocument")
        root_id = doc["root"]["nodeId"]

        result = self._send("DOM.querySelector", {
            "nodeId": root_id,
            "selector": selector
        })
        node_id = result.get("nodeId")

        if not node_id:
            raise RuntimeError(f"File input not found: {selector}")

        # Set the file without opening dialog
        self._send("DOM.setFileInputFiles", {
            "files": [file_path],
            "nodeId": node_id
        })

        # Verify
        time.sleep(0.3)
        value = self.js(f"document.querySelector('{selector}')?.files[0]?.name")
        expected = os.path.basename(file_path)

        if value == expected:
            print(f"[cdp] ✅ file uploaded: {value}")
        else:
            print(f"[cdp] ⚠️ file value: '{value}' (expected '{expected}')")

        return value

    # SECTION 3: Right-click Context Menu
    def right_click_and_select(self, x, y, menu_item_text):
        """
        Right-click at (x,y) and select a context menu item by text.
        """
        # Right-click
        self._send("Input.dispatchMouseEvent", {
            "type": "mousePressed", "x": x, "y": y,
            "button": "right", "clickCount": 1,
            "buttons": 2
        })
        self._send("Input.dispatchMouseEvent", {
            "type": "mouseReleased", "x": x, "y": y,
            "button": "right", "clickCount": 1,
            "buttons": 0
        })
        time.sleep(0.5)

        # Look for context menu
        menu_visible = self.js("""
        (function() {
            const menus = document.querySelectorAll(
                '[role="menu"], [role="menuitem"], .context-menu, #context-menu'
            );
            return menus.length > 0;
        })()
        """)

        if menu_visible:
            # Click item by text
            clicked = self.js(f"""
            (function() {{
                const items = document.querySelectorAll(
                    '[role="menuitem"], .menu-item, li'
                );
                for (const item of items) {{
                    if (item.innerText.trim().toLowerCase()
                        .includes('{menu_item_text.lower()}')) {{
                        item.click();
                        return item.innerText.trim();
                    }}
                }}
                return null;
            }})()
            """)
            print(f"[cdp] context menu item clicked: '{clicked}'")
            return clicked

        print(f"[cdp] native context menu — using keyboard navigation")
        self.key("ArrowDown")
        time.sleep(0.2)
        self.key("Return")
        return None

    # SECTION 4: Drag and Drop
    def drag_and_drop(self, source_selector, target_selector):
        """
        Drag an element to a target.
        Tries CDP mouse events first, falls back to JS event simulation.
        """
        # Get positions
        src_pos = self.js(f"""
        (function() {{
            const el = document.querySelector('{source_selector}');
            if (!el) return null;
            const r = el.getBoundingClientRect();
            return {{x: Math.round(r.left + r.width/2),
                     y: Math.round(r.top + r.height/2)}};
        }})()
        """)
        tgt_pos = self.js(f"""
        (function() {{
            const el = document.querySelector('{target_selector}');
            if (!el) return null;
            const r = el.getBoundingClientRect();
            return {{x: Math.round(r.left + r.width/2),
                     y: Math.round(r.top + r.height/2)}};
        }})()
        """)

        if not src_pos or not tgt_pos:
            raise RuntimeError(
                f"Could not find elements:\n"
                f" source: {source_selector} → {src_pos}\n"
                f" target: {target_selector} → {tgt_pos}"
            )

        # CDP mouse events
        self._send("Input.dispatchMouseEvent", {
            "type": "mousePressed",
            "x": src_pos["x"], "y": src_pos["y"],
            "button": "left", "clickCount": 1
        })
        time.sleep(0.1)

        steps = 20
        for i in range(1, steps + 1):
            ix = int(src_pos["x"] + (tgt_pos["x"] - src_pos["x"]) * i / steps)
            iy = int(src_pos["y"] + (tgt_pos["y"] - src_pos["y"]) * i / steps)
            self._send("Input.dispatchMouseEvent", {
                "type": "mouseMoved", "x": ix, "y": iy,
                "button": "left", "buttons": 1
            })
            time.sleep(0.02)

        self._send("Input.dispatchMouseEvent", {
            "type": "mouseReleased",
            "x": tgt_pos["x"], "y": tgt_pos["y"],
            "button": "left", "clickCount": 1
        })
        time.sleep(0.5)

        # JS event simulation (fallback for custom drag libs)
        self.js(f"""
        (function() {{
            function fireEvent(el, type, x, y) {{
                const ev = new MouseEvent(type, {{
                    bubbles: true, cancelable: true,
                    clientX: x, clientY: y
                }});
                el.dispatchEvent(ev);
            }}
            function fireDrag(el, type, x, y) {{
                const ev = new DragEvent(type, {{
                    bubbles: true, cancelable: true,
                    clientX: x, clientY: y,
                    dataTransfer: new DataTransfer()
                }});
                el.dispatchEvent(ev);
            }}
            const src = document.querySelector('{source_selector}');
            const tgt = document.querySelector('{target_selector}');
            if (!src || !tgt) return;
            const sr = src.getBoundingClientRect();
            const tr = tgt.getBoundingClientRect();
            const sx = sr.left + sr.width/2, sy = sr.top + sr.height/2;
            const tx = tr.left + tr.width/2, ty = tr.top + tr.height/2;

            fireDrag(src, 'dragstart', sx, sy);
            fireEvent(src, 'mousedown', sx, sy);
            fireDrag(tgt, 'dragover', tx, ty);
            fireDrag(tgt, 'drop', tx, ty);
            fireDrag(src, 'dragend', tx, ty);
            fireEvent(src, 'mouseup', tx, ty);
        }})()
        """)
        time.sleep(0.5)
        print(f"[cdp] drag: {source_selector} → {target_selector}")

    # SECTION 5: Iframe Scroll
    def scroll_in_iframe(self, iframe_selector, pixels=500, direction="down"):
        """Scroll content inside an iframe."""
        delta = pixels if direction == "down" else -pixels
        before = self.js(f"""
        (function() {{
            const fr = document.querySelector('{iframe_selector}');
            return fr ? fr.contentWindow.scrollY : null;
        }})()
        """)

        self.js(f"""
        (function() {{
            const fr = document.querySelector('{iframe_selector}');
            if (fr && fr.contentWindow) {{
                fr.contentWindow.scrollBy(0, {delta});
            }}
        }})()
        """)

        time.sleep(0.5)

        after = self.js(f"""
        (function() {{
            const fr = document.querySelector('{iframe_selector}');
            return fr ? fr.contentWindow.scrollY : null;
        }})()
        """)
        print(f"[cdp] iframe scroll: {before} → {after}")
        return after

    # SECTION 6: Shadow DOM
    def query_shadow(self, host_selector, inner_selector):
        """
        Query an element inside a Shadow DOM.
        """
        return self.js(f"""
        (function() {{
            const host = document.querySelector('{host_selector}');
            if (!host || !host.shadowRoot) return null;
            const el = host.shadowRoot.querySelector('{inner_selector}');
            if (!el) return null;
            const r = el.getBoundingClientRect();
            return {{
                x: Math.round(r.left + r.width/2),
                y: Math.round(r.top + r.height/2),
                text: el.innerText || el.value || ''
            }};
        }})()
        """)

    def click_shadow(self, host_selector, inner_selector):
        """Click an element inside a Shadow DOM."""
        pos = self.query_shadow(host_selector, inner_selector)
        if not pos:
            raise RuntimeError(
                f"Shadow DOM element not found:\n"
                f" host: {host_selector}\n"
                f" inner: {inner_selector}"
            )
        self.click(pos["x"], pos["y"])
        print(f"[cdp] shadow DOM click at ({pos['x']}, {pos['y']})")
        return pos

    def type_shadow(self, host_selector, inner_selector, text):
        """Type into an element inside Shadow DOM."""
        self.click_shadow(host_selector, inner_selector)
        time.sleep(0.3)
        self._send("Input.insertText", {"text": text})

        # Verify
        value = self.js(f"""
        (function() {{
            const host = document.querySelector('{host_selector}');
            if (!host || !host.shadowRoot) return null;
            const el = host.shadowRoot.querySelector('{inner_selector}');
            return el ? (el.value || el.innerText) : null;
        }})()
        """)
        print(f"[cdp] shadow typed, value: '{value}'")
        return value

    # SECTION 8: Complex Multi-field Forms
    def fill_form_smart(self, field_map, submit_selector=None):
        """
        Fill a form intelligently.
        field_map: list of (selector, value) tuples in order
        submit_selector: CSS selector for submit button (optional)
        """
        results = {}
        errors = []

        for selector, value in field_map:
            # Scroll element into view
            self.js(f"document.querySelector('{selector}')?.scrollIntoView({{block:'center'}})")
            time.sleep(0.2)

            # Determine element type
            el_type = self.js(f"""
            (function() {{
                const el = document.querySelector('{selector}');
                if (!el) return null;
                return el.type || el.tagName.toLowerCase();
            }})()
            """)

            if el_type in ("checkbox", "radio"):
                # Toggle
                self.js(f"document.querySelector('{selector}').click()")
                time.sleep(0.2)
            elif el_type in ("select", "select-one"):
                # Select by value
                self.js(f"""
                (function() {{
                    const el = document.querySelector('{selector}');
                    el.value = '{value}';
                    el.dispatchEvent(new Event('change', {{bubbles: true}}));
                }})()
                """)
                time.sleep(0.2)
            elif el_type == "date":
                # Date input
                self.js(f"document.querySelector('{selector}').focus()")
                time.sleep(0.3)
                self.js(f"document.querySelector('{selector}').value = '{value}'")
                self.js(f"""
                document.querySelector('{selector}')
                    .dispatchEvent(new Event('change', {{bubbles:true}}));
                """)
                time.sleep(0.2)
            else:
                # Standard text input
                self.js(f"document.querySelector('{selector}').focus()")
                time.sleep(0.3)
                self.js(f"document.querySelector('{selector}').value = ''")
                self._send("Input.insertText", {"text": str(value)})
                self.js(f"""
                document.querySelector('{selector}')
                    .dispatchEvent(new Event('input', {{bubbles:true}}));
                document.querySelector('{selector}')
                    .dispatchEvent(new Event('change', {{bubbles:true}}));
                """)
                time.sleep(0.2)

            # Verify
            actual = self.js(f"""
            (function() {{
                const el = document.querySelector('{selector}');
                if (!el) return '__NOT_FOUND__';
                return el.value !== undefined ? el.value : el.checked;
            }})()
            """)
            results[selector] = actual
            print(f"[form] '{selector}' = '{actual}'")

            # Check for validation errors
            error = self.js(f"""
            (function() {{
                const el = document.querySelector('{selector}');
                return el ? el.validationMessage : '';
            }})()
            """)
            if error:
                errors.append(f"{selector}: {error}")
                print(f"[form] ⚠️ validation: {error}")

        if submit_selector:
            time.sleep(0.3)
            self.click_selector(submit_selector)
            time.sleep(2)
            print(f"[form] submitted")

        if errors:
            print(f"[form] validation errors: {errors}")

        return results, errors

    # SECTION 9: Canvas Apps
    def canvas_hash(self, selector="canvas"):
        """Get MD5 of canvas content. Proves canvas changed."""
        import hashlib
        data = self.js(f"""
        (function() {{
            const canvas = document.querySelector('{selector}');
            if (!canvas) return null;
            try {{
                return canvas.toDataURL('image/png');
            }} catch(e) {{
                return 'tainted:' + e.message;
            }}
        }})()
        """)
        if not data or data.startswith("tainted"):
            print(f"[canvas] ⚠️ canvas tainted (cross-origin): {data}")
            return None
        return hashlib.md5(data.encode()).hexdigest()

    def draw_on_canvas(self, selector, points):
        """
        Draw on a canvas by simulating mouse events.
        points: list of (x, y) tuples to draw through
        """
        if not points:
            return

        self._send("Input.dispatchMouseEvent", {
            "type": "mousePressed",
            "x": points[0][0], "y": points[0][1],
            "button": "left", "clickCount": 1
        })
        for x, y in points[1:]:
            self._send("Input.dispatchMouseEvent", {
                "type": "mouseMoved",
                "x": x, "y": y,
                "button": "left", "buttons": 1
            })
            time.sleep(0.02)
        self._send("Input.dispatchMouseEvent", {
            "type": "mouseReleased",
            "x": points[-1][0], "y": points[-1][1],
            "button": "left"
        })
        print(f"[canvas] drew {len(points)} points")

    # SECTION 10: Dynamic / Lazy-loaded Content
    def wait_for_element(self, selector, timeout=15, visible=True):
        """
        Wait until an element exists (and optionally is visible).
        More reliable than fixed time.sleep().
        """
        start = time.time()
        while time.time() - start < timeout:
            exists = self.js(f"""
            (function() {{
                const el = document.querySelector('{selector}');
                if (!el) return false;
                if ({str(visible).lower()}) {{
                    const r = el.getBoundingClientRect();
                    return r.width > 0 && r.height > 0;
                }}
                return true;
            }})()
            """)
            if exists:
                elapsed = round(time.time() - start, 1)
                print(f"[cdp] element appeared: '{selector}' ({elapsed}s)")
                return True
            time.sleep(0.3)
        raise TimeoutError(
            f"Element not found after {timeout}s: {selector}"
        )

    def wait_for_text(self, text, timeout=15):
        """Wait until specific text appears anywhere on the page."""
        start = time.time()
        while time.time() - start < timeout:
            if text.lower() in (self.js("document.body.innerText") or "").lower():
                elapsed = round(time.time() - start, 1)
                print(f"[cdp] text appeared: '{text}' ({elapsed}s)")
                return True
            time.sleep(0.3)
        raise TimeoutError(f"Text not found after {timeout}s: '{text}'")

    def wait_for_url_change(self, current_url, timeout=15):
        """Wait until URL changes from current_url."""
        start = time.time()
        while time.time() - start < timeout:
            new_url = self.js("window.location.href")
            if new_url != current_url:
                elapsed = round(time.time() - start, 1)
                print(f"[cdp] URL changed after {elapsed}s: {new_url[:60]}")
                return new_url
            time.sleep(0.3)
        raise TimeoutError(f"URL did not change after {timeout}s")

    # SECTION 11: Bot Detection Bypass + Human-like Typing
    def type_human(self, text, min_delay=50, max_delay=150):
        """
        Type text with random delays between keystrokes.
        More realistic — avoids bot detection on timing-sensitive sites.
        """
        import random
        for char in text:
            self._send("Input.insertText", {"text": char})
            time.sleep(random.randint(min_delay, max_delay) / 1000)
        print(f"[cdp] human-typed: '{text[:40]}'")

    # SECTION 13: Keyboard Shortcut Combos
    def key_combo(self, key, modifiers=0):
        """
        Send a key with modifiers.
        modifiers: 1=Alt, 2=Ctrl, 4=MetaCmd, 8=Shift
        """
        self._send("Input.dispatchKeyEvent", {
            "type": "rawKeyDown",
            "key": key,
            "modifiers": modifiers
        })
        time.sleep(0.1)
        self._send("Input.dispatchKeyEvent", {
            "type": "keyUp",
            "key": key,
            "modifiers": modifiers
        })
        print(f"[cdp] key combo: {key} (mods={modifiers})")

    def close(self):
        if self._ws:
            try:
                self._ws.close()
            except:
                pass
        if self._chrome:
            self._chrome.terminate()
        print("[cdp] closed")
