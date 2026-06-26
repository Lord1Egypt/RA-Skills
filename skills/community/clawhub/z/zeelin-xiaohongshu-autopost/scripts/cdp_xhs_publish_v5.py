#!/usr/bin/env python3
"""
Xiaohongshu creator — fill title + body via CDP, including content inside iframes.

- Walks Page.getFrameTree, uses Page.createIsolatedWorld + Runtime.evaluate per frame.
- After focus, uses Input.insertText (focus must be in the target frame).
- Does NOT click「发布」unless env XHS_AUTO_PUBLISH=1 (avoid accidental live posts).
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request

import websocket


SIGNATURE = "\n\n本推文由Auto Ops自动发布"


def port() -> int:
    return int(os.environ.get("OPENCLAW_CDP_PORT", "9222"))


def list_tabs(p: int):
    with urllib.request.urlopen(f"http://127.0.0.1:{p}/json", timeout=8) as r:
        return json.loads(r.read())


def activate(p: int, tid: str):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{p}/json/activate/{tid}", timeout=5)
    except Exception:
        pass


def find_xhs(p: int):
    for t in list_tabs(p):
        if t.get("type") == "page" and "xiaohongshu.com" in t.get("url", ""):
            return t
    return None


def connect_ws(ws_url: str, p: int):
    return websocket.create_connection(ws_url, timeout=15, origin=f"http://127.0.0.1:{p}")


def cdp_send(ws, method: str, params=None, timeout=25):
    msg_id = int(time.time() * 1000) % 1_000_000_000
    ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    deadline = time.time() + timeout
    while time.time() < deadline:
        ws.settimeout(max(0.5, deadline - time.time()))
        try:
            raw = ws.recv()
        except websocket.WebSocketTimeoutException:
            continue
        data = json.loads(raw)
        if data.get("id") == msg_id:
            if "error" in data:
                raise RuntimeError(str(data["error"]))
            return data.get("result", {})
    raise TimeoutError(method)


def collect_frame_ids(tree: dict) -> list[str]:
    out: list[str] = []
    frame = tree.get("frame") or {}
    fid = frame.get("id")
    if fid:
        out.append(fid)
    for child in tree.get("childFrames") or []:
        out.extend(collect_frame_ids(child))
    return out


def create_ctx(ws, frame_id: str) -> int:
    r = cdp_send(
        ws,
        "Page.createIsolatedWorld",
        {
            "frameId": frame_id,
            "worldName": "__openclaw_xhs__",
            "grantUniverseAccess": True,
        },
    )
    return int(r["executionContextId"])


def js_eval_ctx(ws, execution_context_id: int, expr: str, timeout=20):
    r = cdp_send(
        ws,
        "Runtime.evaluate",
        {
            "expression": expr,
            "returnByValue": True,
            "awaitPromise": False,
            "executionContextId": execution_context_id,
        },
        timeout=timeout,
    )
    res = r.get("result", {})
    if res.get("type") == "string":
        return res.get("value", "")
    if res.get("type") == "boolean":
        return res.get("value", False)
    if res.get("type") == "number":
        return res.get("value", 0)
    return res.get("value", "")


def js_eval(ws, expr: str, timeout=20):
    r = cdp_send(
        ws,
        "Runtime.evaluate",
        {"expression": expr, "returnByValue": True, "awaitPromise": False},
        timeout=timeout,
    )
    res = r.get("result", {})
    if res.get("type") == "string":
        return res.get("value", "")
    if res.get("type") == "boolean":
        return res.get("value", False)
    if res.get("type") == "number":
        return res.get("value", 0)
    return res.get("value", "")


PROBE_JS = """
(() => {
    const inputs = document.querySelectorAll('input, textarea');
    const ce = document.querySelectorAll('[contenteditable="true"]');
    let titleLike = 0;
    for (const i of inputs) {
        const ph = (i.placeholder || '') + (i.getAttribute('aria-label') || '');
        if (/标题|topic|title/i.test(ph) || i.maxLength === 20) titleLike++;
    }
    return JSON.stringify({
        inputs: inputs.length,
        ce: ce.length,
        titleLike: titleLike,
        path: location.pathname,
        href: location.href.substring(0, 80)
    });
})()
"""

FOCUS_TITLE_JS = """
(() => {
    const bad = new Set(['hidden', 'file', 'checkbox', 'radio', 'submit']);
    const sels = [
        'textarea[placeholder*="输入标题"]',
        'textarea[placeholder*="标题"]',
        'textarea.d-text[maxlength="64"]',
        'textarea.d-text',
        '.rich-editor-title textarea',
        'input[placeholder*="标题"]',
        'input[maxlength="20"]',
    ];
    for (const s of sels) {
        for (const el of document.querySelectorAll(s)) {
            if (!el.offsetParent) continue;
            if (el.tagName === 'INPUT' && bad.has(el.type)) continue;
            el.focus();
            el.click();
            return "OK_TITLE:" + s;
        }
    }
    const vis = [...document.querySelectorAll("textarea, input")].filter(
        i => i.offsetParent && !bad.has(i.type) && i.type !== 'file');
    if (vis[0]) {
        vis[0].focus();
        vis[0].click();
        return "OK_TITLE:first-visible";
    }
    return "ERROR:NO_TITLE";
})()
"""

FOCUS_BODY_JS = """
(() => {
    const sels = [
        '.tiptap.ProseMirror',
        '.ProseMirror[contenteditable="true"]',
        '.ql-editor',
        '.note-editor [contenteditable="true"]',
        '[data-placeholder*="正文"]',
        '[data-placeholder*="分享"]',
        'div.d-input-editor [contenteditable="true"]',
        '[contenteditable="true"]',
        'textarea'
    ];
    for (const s of sels) {
        for (const el of document.querySelectorAll(s)) {
            if (!el.offsetParent) continue;
            const h = el.getBoundingClientRect().height;
            if (s === '[contenteditable="true"]' && h < 30) continue;
            el.focus();
            el.click();
            return "OK_BODY:" + s;
        }
    }
    return "ERROR:NO_BODY";
})()
"""

CLICK_FORMAT_JS = """
(() => {
    for (const b of document.querySelectorAll('button')) {
        const t = (b.textContent || '').trim();
        if (t === '一键排版' && b.offsetParent) { b.click(); return 'CLICK'; }
    }
    return 'MISS';
})()
"""

CLICK_NEXT_JS = """
(() => {
    for (const b of document.querySelectorAll('button')) {
        const t = (b.textContent || '').trim();
        if (t === '下一步' && b.offsetParent) { b.click(); return 'CLICK'; }
    }
    return 'MISS';
})()
"""

PUBLISH_JS = """
(() => {
    // Only match exact "发布" button, NOT sidebar "发布笔记"
    for (const n of document.querySelectorAll('button')) {
        if (!n.offsetParent) continue;
        const t = (n.textContent || '').trim();
        if (t === '发布') {
            n.click();
            return 'CLICK:发布';
        }
    }
    return 'SKIP';
})()
"""

CONFIRM_DIALOG_JS = """
(() => {
    const labels = ['确认发布', '确认', '继续发布', '确定发布', '确定', '立即发布'];
    for (const n of document.querySelectorAll('button, [role="button"], div[class*="btn"], span[class*="btn"]')) {
        if (!n.offsetParent) continue;
        const t = (n.textContent || '').trim();
        for (const lb of labels) {
            if (t === lb) {
                n.click();
                return 'CONFIRM:' + t;
            }
        }
    }
    for (const n of document.querySelectorAll('button, [role="button"], div[class*="btn"], span[class*="btn"]')) {
        if (!n.offsetParent) continue;
        const t = (n.textContent || '').trim();
        for (const lb of labels) {
            if (t.includes(lb)) {
                n.click();
                return 'CONFIRM_PARTIAL:' + t;
            }
        }
    }
    return 'NO_DIALOG';
})()
"""

CHECK_SUCCESS_JS = """
(() => {
    const text = document.body.innerText || '';
    if (/发布成功|笔记已发布|审核中|内容已提交|已发布/.test(text)) return 'SUCCESS';
    const url = location.href;
    if (/\/notes|\/published|note-manage/.test(url)) return 'SUCCESS_URL';
    return 'STILL_ON_PAGE';
})()
"""


def score_probe(probe_str: str) -> int:
    try:
        o = json.loads(probe_str)
        return int(o.get("ce", 0)) * 10 + int(o.get("titleLike", 0)) * 5 + int(o.get("inputs", 0))
    except Exception:
        return 0


def best_frame_for_editor(ws) -> str | None:
    """Returns frame_id for the subtree that looks most like the editor."""
    tree = cdp_send(ws, "Page.getFrameTree", {})
    frame_tree = tree.get("frameTree", {})
    ids = collect_frame_ids(frame_tree)
    cdp_send(ws, "Runtime.enable", {})

    best_score = -1
    best_fid: str | None = None

    for fid in ids:
        try:
            ctx = create_ctx(ws, fid)
            probe = js_eval_ctx(ws, ctx, PROBE_JS)
            sc = score_probe(probe)
            if sc > best_score:
                best_score = sc
                best_fid = fid
        except Exception:
            continue

    if best_fid is None or best_score < 1:
        return None
    return best_fid


CLICK_NEW_ARTICLE_JS = """
(() => {
    // Prefer the <button> with exact text
    for (const n of document.querySelectorAll('button')) {
        const t = (n.textContent || '').trim();
        if (t === '新的创作' && n.offsetParent) { n.click(); return 'CLICK_BTN'; }
    }
    // Fallback: any clickable with exact match
    for (const n of document.querySelectorAll('div,span,a')) {
        const t = (n.textContent || '').trim();
        if (t === '新的创作' && n.offsetParent) { n.click(); return 'CLICK_OTHER'; }
    }
    return 'MISS';
})()
"""

def prepare_page(ws):
    """Navigate to the XHS long-article editor: publish page → '写长文' tab → '新的创作'."""
    cdp_send(
        ws,
        "Page.navigate",
        {"url": "https://creator.xiaohongshu.com/publish/publish?source=official&from=menu&target=article"},
    )
    time.sleep(3)
    cdp_send(ws, "Page.reload", {})
    time.sleep(6)
    print("Nav to article page:", js_eval(ws, "location.href"))

    # Click 新的创作 (with retry)
    for attempt in range(4):
        r = js_eval(ws, CLICK_NEW_ARTICLE_JS)
        print(f"Click 新的创作 (attempt {attempt+1}):", r)
        if "CLICK" in str(r):
            break
        time.sleep(3)

    time.sleep(4)
    probe = js_eval(ws, PROBE_JS)
    print("Editor probe:", probe)


def type_into_focused(ws, text: str):
    cdp_send(ws, "Input.dispatchKeyEvent", {"type": "keyDown", "key": "a", "code": "KeyA", "modifiers": 2})
    cdp_send(ws, "Input.dispatchKeyEvent", {"type": "keyUp", "key": "a", "code": "KeyA", "modifiers": 2})
    cdp_send(ws, "Input.dispatchKeyEvent", {"type": "keyDown", "key": "Backspace", "code": "Backspace"})
    cdp_send(ws, "Input.dispatchKeyEvent", {"type": "keyUp", "key": "Backspace", "code": "Backspace"})
    time.sleep(0.12)
    cdp_send(ws, "Input.insertText", {"text": text})
    js_eval(ws, """
    (() => {
        const el = document.activeElement;
        if (el) {
            el.dispatchEvent(new Event('input', {bubbles:true}));
            el.dispatchEvent(new Event('change', {bubbles:true}));
        }
    })()
    """)


def fill_in_context(ws, ctx_id: int, title: str, body: str) -> bool:
    r1 = js_eval_ctx(ws, ctx_id, FOCUS_TITLE_JS)
    print("(iframe) Title focus:", r1)
    if "OK" not in str(r1):
        return False
    type_into_focused(ws, title)
    time.sleep(0.4)

    r2 = js_eval_ctx(ws, ctx_id, FOCUS_BODY_JS)
    print("(iframe) Body focus:", r2)
    if "OK" not in str(r2):
        return False
    type_into_focused(ws, body)
    return True


def fill_in_main(ws, title: str, body: str) -> bool:
    r1 = js_eval(ws, FOCUS_TITLE_JS)
    print("Title focus:", r1)
    if "OK" not in str(r1):
        return False
    type_into_focused(ws, title)
    time.sleep(0.4)
    r2 = js_eval(ws, FOCUS_BODY_JS)
    print("Body focus:", r2)
    if "OK" not in str(r2):
        return False
    type_into_focused(ws, body)
    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: cdp_xhs_ops.py <title> <body>", file=sys.stderr)
        sys.exit(1)

    title = sys.argv[1]
    body = (sys.argv[2] or "").strip()
    p = port()
    tab = find_xhs(p)
    if not tab:
        print("ERROR: No xiaohongshu.com tab in CDP Chrome.", file=sys.stderr)
        sys.exit(1)

    activate(p, tab["id"])
    time.sleep(0.3)
    ws = connect_ws(tab["webSocketDebuggerUrl"], p)
    try:
        cdp_send(ws, "Page.enable", {})
        prepare_page(ws)

        ok = fill_in_main(ws, title, body)
        if not ok:
            print("Main frame incomplete, trying iframe contexts...")
            fid = best_frame_for_editor(ws)
            if fid:
                print(f"Using iframe frameId={fid[:16]}...")
                ctx_id = create_ctx(ws, fid)
                ok = fill_in_context(ws, ctx_id, title, body)
            if not ok:
                print("ERROR: Could not fill title/body.", file=sys.stderr)
                sys.exit(1)

        time.sleep(0.8)
        no_publish = os.environ.get("XHS_NO_PUBLISH", "").strip() in ("1", "true", "yes")
        if no_publish:
            print("XHS: content filled. Skipping live Ops (XHS_NO_PUBLISH=1).")
        else:
            # Step 1: 一键排版 → template selection
            fmt_r = js_eval(ws, CLICK_FORMAT_JS)
            print("一键排版:", fmt_r)
            time.sleep(8)

            # Step 2: 下一步 → publish settings (with retry)
            for step_try in range(5):
                js_eval(ws, "(function(){window.scrollTo(0,document.body.scrollHeight);return 1;})()")
                time.sleep(1)
                next_r = js_eval(ws, CLICK_NEXT_JS)
                print(f"下一步 (attempt {step_try+1}):", next_r)
                if "CLICK" in str(next_r):
                    break
                time.sleep(3)
            time.sleep(5)

            # Step 3: 发布
            js_eval(ws, "(function(){window.scrollTo(0,document.body.scrollHeight);return 'SCROLLED';})()")
            time.sleep(1)
            r3 = js_eval(ws, PUBLISH_JS)
            print("Submit click (platform UI 发布):", r3)

            success = False
            for attempt in range(5):
                time.sleep(3)
                confirm_r = js_eval(ws, CONFIRM_DIALOG_JS)
                print(f"  Confirm dialog (attempt {attempt+1}):", confirm_r)
                if "CONFIRM" in str(confirm_r):
                    time.sleep(3)

                check_r = js_eval(ws, CHECK_SUCCESS_JS)
                print(f"  Status:", check_r)
                if "SUCCESS" in str(check_r):
                    success = True
                    break

                if "STILL_ON_PAGE" in str(check_r) and attempt < 4:
                    js_eval(ws, PUBLISH_JS)
                    time.sleep(1)
                    js_eval(ws, CONFIRM_DIALOG_JS)
                    print(f"  Retry submit+confirm (attempt {attempt+2})")

            if success:
                print("Xiaohongshu Ops SUCCESS.")
            else:
                print("WARN: Ops may not have completed. Check creator center.", file=sys.stderr)
        print("Xiaohongshu Ops flow completed.")
    finally:
        ws.close()


if __name__ == "__main__":
    main()
