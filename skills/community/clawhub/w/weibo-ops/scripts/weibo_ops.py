#!/usr/bin/env python3
"""
Weibo operations via DrissionPage + CDP.
Connects to a real Chrome instance with --remote-debugging-port.

Usage:
  python3 weibo_ops.py --port 19334 --action post --text "hello"
  python3 weibo_ops.py --port 19334 --action delete_all
  python3 weibo_ops.py --port 19334 --action delete_one --index 0
  python3 weibo_ops.py --port 19334 --action repost --post_id QAjCW9m6h --text "转发语"
  python3 weibo_ops.py --port 19334 --action comment --post_id QAjCW9m6h --text "评论"
  python3 weibo_ops.py --port 19334 --action like --post_id QAjCW9m6h
  python3 weibo_ops.py --port 19334 --action count

Prerequisites:
  Chrome running with --remote-debugging-port=19334 --user-data-dir=<custom_profile>
  Already logged into weibo.com in that Chrome profile.
  pip install DrissionPage
"""

import argparse
import json
import sys
import time

from DrissionPage import Chromium

DEFAULT_PORT = 19334


def get_browser(port=DEFAULT_PORT):
    browser = Chromium(addr_or_opts=f'127.0.0.1:{port}')
    return browser, browser.latest_tab


def ensure_login(tab, uid):
    tab.get(f'https://weibo.com/u/{uid}')
    time.sleep(6)
    if 'login' in tab.url or 'visitor' in tab.url:
        print(f"ERROR: Not logged in. URL: {tab.url}")
        sys.exit(1)
    tab.run_js('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')


def find_more_buttons(tab):
    result = tab.run_js('''
    var items = document.querySelectorAll("[class*=_more_1v5ao]");
    var results = [];
    for (var i = 0; i < items.length; i++) {
        var r = items[i].getBoundingClientRect();
        if (r.width > 0 && r.height > 0) {
            results.push({x: r.x + r.width/2, y: r.y + r.height/2});
        }
    }
    return JSON.stringify(results);
    ''')
    return json.loads(result) if result and result != '[]' else []


def js_click(tab, x, y):
    """Click at coordinates via CDP mouse events."""
    tab.run_cdp('Input.dispatchMouseEvent', type='mousePressed', x=x, y=y, button='left', clickCount=1)
    time.sleep(0.05)
    tab.run_cdp('Input.dispatchMouseEvent', type='mouseReleased', x=x, y=y, button='left', clickCount=1)


def delete_one_post(tab):
    """Delete first visible post on profile page. Returns True if deleted."""
    btns = find_more_buttons(tab)
    if not btns:
        return False

    # Click 更多
    js_click(tab, btns[0]['x'], btns[0]['y'])
    time.sleep(2.5)

    # Click 删除 in popup
    del_result = tab.run_js('''
    var items = document.querySelectorAll("div[class*=pop-item-main]");
    for (var i = 0; i < items.length; i++) {
        if (items[i].textContent.trim() === "删除") {
            var r = items[i].getBoundingClientRect();
            if (r.width > 0) { items[i].click(); return true; }
        }
    }
    return false;
    ''')
    time.sleep(2)

    if del_result:
        # Click 确定 in confirm dialog (find inside woo-dialog)
        tab.run_js('''
        var btns = document.querySelectorAll("button");
        for (var i = 0; i < btns.length; i++) {
            if (btns[i].textContent.trim() === "确定") {
                var r = btns[i].getBoundingClientRect();
                if (r.width > 0 && r.height > 0 && btns[i].closest("[class*=dialog]")) {
                    btns[i].click(); return;
                }
            }
        }
        ''')
        time.sleep(2)
        return True

    # Dismiss popup
    js_click(tab, 100, 100)
    time.sleep(0.5)
    return False


# === Actions ===

def action_count(tab, uid):
    tab.get(f'https://weibo.com/u/{uid}')
    time.sleep(5)
    count = tab.run_js('''
    var text = document.body.innerText;
    var match = text.match(/全部微博（(\\d+)）/);
    return match ? match[1] : "unknown";
    ''')
    print(f'Current posts: {count}')
    return count


def action_post(tab, text):
    tab.get('https://weibo.com')
    time.sleep(5)

    # Click 写微博 via JS
    tab.run_js('''
    var btns = document.querySelectorAll("button");
    for (var i = 0; i < btns.length; i++) {
        if (btns[i].textContent.trim().includes("写微博")) {
            btns[i].click(); return;
        }
    }
    ''')
    time.sleep(2)

    # Set text via Vue-compatible native setter
    tab.run_js('''
    var ta = document.querySelectorAll("textarea");
    for (var i = 0; i < ta.length; i++) {
        var r = ta[i].getBoundingClientRect();
        if (r.width > 100 && r.y < 300 && r.height > 20) {
            ta[i].focus();
            var setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
            setter.call(ta[i], arguments[0]);
            ta[i].dispatchEvent(new Event("input", {bubbles: true}));
            return;
        }
    }
    ''', text)
    time.sleep(1)

    # Click 发送 via JS
    send = tab.run_js('''
    var btns = document.querySelectorAll("button");
    for (var i = 0; i < btns.length; i++) {
        var r = btns[i].getBoundingClientRect();
        if (r.width > 0 && r.y < 300 && btns[i].textContent.trim() === "发送" && !btns[i].disabled) {
            btns[i].click(); return "ok";
        }
    }
    return null;
    ''')
    time.sleep(3)
    if send:
        print("Post published!")
        return True
    print("ERROR: Cannot find '发送' button")
    return False


def action_delete_all(tab, uid):
    total = 0
    for _ in range(20):
        tab.get(f'https://weibo.com/u/{uid}')
        time.sleep(6)
        if not find_more_buttons(tab):
            break
        if delete_one_post(tab):
            total += 1
            print(f'  Deleted #{total}')
        else:
            break
    print(f'Total deleted: {total}')
    return total


def action_delete_one(tab, uid, index=0):
    tab.get(f'https://weibo.com/u/{uid}')
    time.sleep(6)
    btns = find_more_buttons(tab)
    if index >= len(btns):
        print(f"ERROR: Only {len(btns)} posts")
        return False
    # For index > 0, need to click the specific button
    # (current delete_one_post only handles first)
    js_click(tab, btns[index]['x'], btns[index]['y'])
    time.sleep(2.5)
    del_result = tab.run_js('''
    var items = document.querySelectorAll("div[class*=pop-item-main]");
    for (var i = 0; i < items.length; i++) {
        if (items[i].textContent.trim() === "删除") {
            if (items[i].getBoundingClientRect().width > 0) { items[i].click(); return true; }
        }
    }
    return false;
    ''')
    if del_result:
        time.sleep(2)
        tab.run_js('''
        var btns = document.querySelectorAll("button");
        for (var i = 0; i < btns.length; i++) {
            if (btns[i].textContent.trim() === "确定" && btns[i].getBoundingClientRect().width > 0 && btns[i].closest("[class*=dialog]")) {
                btns[i].click(); return;
            }
        }
        ''')
        time.sleep(2)
        print(f'Deleted post #{index}')
        return True
    return False


def action_repost(tab, uid, post_id, text=""):
    tab.get(f'https://weibo.com/{uid}/{post_id}')
    time.sleep(6)

    # Click 转发
    tab.run_js('''
    var divs = document.querySelectorAll("div");
    for (var i = 0; i < divs.length; i++) {
        if (divs[i].textContent.trim() === "转发") {
            var r = divs[i].getBoundingClientRect();
            if (r.width > 0 && r.width < 200 && r.y > 200) { divs[i].click(); return; }
        }
    }
    ''')
    time.sleep(2)

    if text:
        tab.run_js('''
        var ta = document.querySelectorAll("textarea");
        for (var i = 0; i < ta.length; i++) {
            var r = ta[i].getBoundingClientRect();
            if (r.width > 100 && r.height > 20) {
                ta[i].focus();
                var setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
                setter.call(ta[i], arguments[0]);
                ta[i].dispatchEvent(new Event("input", {bubbles: true}));
                return;
            }
        }
        ''', text)
        time.sleep(1)

    send = tab.run_js('''
    var btns = document.querySelectorAll("button");
    for (var i = 0; i < btns.length; i++) {
        if (btns[i].textContent.trim() === "发送" && !btns[i].disabled) {
            var r = btns[i].getBoundingClientRect();
            if (r.width > 0) { btns[i].click(); return "ok"; }
        }
    }
    return null;
    ''')
    time.sleep(3)
    if send:
        print("Reposted!")
        return True
    print("ERROR: Repost failed")
    return False


def action_comment(tab, uid, post_id, text):
    tab.get(f'https://weibo.com/{uid}/{post_id}')
    time.sleep(6)

    # Click 评论
    tab.run_js('''
    var divs = document.querySelectorAll("div");
    for (var i = 0; i < divs.length; i++) {
        if (divs[i].textContent.trim() === "评论") {
            var r = divs[i].getBoundingClientRect();
            if (r.width > 0 && r.width < 200 && r.y > 200) { divs[i].click(); return; }
        }
    }
    ''')
    time.sleep(1)

    # Type comment
    tab.run_js('''
    var ta = document.querySelectorAll("textarea");
    for (var i = 0; i < ta.length; i++) {
        var r = ta[i].getBoundingClientRect();
        if (r.width > 100 && r.height > 20) {
            ta[i].focus();
            var setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
            setter.call(ta[i], arguments[0]);
            ta[i].dispatchEvent(new Event("input", {bubbles: true}));
            return;
        }
    }
    ''', text)
    time.sleep(1)

    send = tab.run_js('''
    var btns = document.querySelectorAll("button");
    for (var i = 0; i < btns.length; i++) {
        var t = btns[i].textContent.trim();
        if ((t === "发送" || t === "评论") && !btns[i].disabled) {
            var r = btns[i].getBoundingClientRect();
            if (r.width > 0) { btns[i].click(); return "ok"; }
        }
    }
    return null;
    ''')
    time.sleep(3)
    if send:
        print("Comment posted!")
        return True
    print("ERROR: Comment failed")
    return False


def action_like(tab, uid, post_id):
    tab.get(f'https://weibo.com/{uid}/{post_id}')
    time.sleep(6)

    result = tab.run_js('''
    var btns = document.querySelectorAll("button[class*=like],[class*=woo-like]");
    for (var i = 0; i < btns.length; i++) {
        var r = btns[i].getBoundingClientRect();
        if (r.width > 0) { btns[i].click(); return "ok"; }
    }
    // Fallback
    var divs = document.querySelectorAll("div");
    for (var i = 0; i < divs.length; i++) {
        if (divs[i].textContent.trim() === "赞") {
            var r = divs[i].getBoundingClientRect();
            if (r.width > 0 && r.width < 200 && r.y > 200) { divs[i].click(); return "ok"; }
        }
    }
    return null;
    ''')
    time.sleep(1)
    if result:
        print("Liked!")
        return True
    print("ERROR: Like failed")
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('--uid', type=str, default='6331761230')
    parser.add_argument('--action', required=True,
                        choices=['post', 'delete_all', 'delete_one', 'repost', 'comment', 'like', 'count'])
    parser.add_argument('--text', type=str, default='')
    parser.add_argument('--post_id', type=str, default='')
    parser.add_argument('--index', type=int, default=0)
    parser.add_argument('--keep-open', action='store_true')
    args = parser.parse_args()

    browser, tab = get_browser(port=args.port)
    try:
        if args.action == 'count':
            action_count(tab, args.uid)
        elif args.action == 'post':
            ensure_login(tab, args.uid)
            action_post(tab, args.text)
        elif args.action == 'delete_all':
            ensure_login(tab, args.uid)
            action_delete_all(tab, args.uid)
        elif args.action == 'delete_one':
            ensure_login(tab, args.uid)
            action_delete_one(tab, args.uid, args.index)
        elif args.action == 'repost':
            action_repost(tab, args.uid, args.post_id, args.text)
        elif args.action == 'comment':
            action_comment(tab, args.uid, args.post_id, args.text)
        elif args.action == 'like':
            action_like(tab, args.uid, args.post_id)
    finally:
        if not args.keep_open:
            try: browser.quit()
            except: pass


if __name__ == '__main__':
    main()
