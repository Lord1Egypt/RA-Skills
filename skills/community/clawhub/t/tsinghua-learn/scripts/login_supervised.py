#!/usr/bin/env python3
"""
login_supervised.py
清华网络学堂 - 有人值守登录脚本
======================================
先尝试 headless 自动登录，检测到 2FA 才弹浏览器。
"""
import sys, os, json, time, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import load_credentials, get_state_file, get_fp_file, get_profile_dir

STATE_FILE       = get_state_file()
FINGERPRINT_FILE = get_fp_file()
PROFILE_DIR      = get_profile_dir()

try:
    _creds = load_credentials()
    USER = _creds.get("username", "")
    PASS = _creds.get("password", "")
    if not USER or not PASS:
        raise ValueError("username 或 password 为空")
except Exception as e:
    print(e)
    raise SystemExit(1)

CAS_URL = "https://id.tsinghua.edu.cn/do/off/ui/auth/login/form/bb5df85216504820be7bba2b0ae1535b/0"

try:
    fp = json.load(open(FINGERPRINT_FILE, encoding="utf-8"))
except FileNotFoundError:
    fp = {}
    print("fingerprint 文件缺失，自动填充可能不完整。", flush=True)
os.makedirs(PROFILE_DIR, exist_ok=True)


def save_state(ctx, page_url, csrf):
    learn_jsession = None
    learn_token    = None
    for c in ctx.cookies():
        if "learn.tsinghua" in c["domain"]:
            if c["name"] == "JSESSIONID": learn_jsession = c["value"]
            elif c["name"] == "XSRF-TOKEN": learn_token = c["value"]
    state = {
        "learn_jsession": learn_jsession,
        "learn_token":    learn_token,
        "csrf":           csrf,
        "timestamp":      time.time(),
        "url":            page_url,
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"Session 已保存: {STATE_FILE}")
    return state


def _try_login(headless):
    """尝试登录，返回 (success, needs_2fa, page, ctx)"""
    ctx = pw.chromium.launch_persistent_context(
        PROFILE_DIR,
        headless=headless,
        viewport={"width": 1280, "height": 900},
        args=["--no-sandbox", "--disable-dev-shm-usage",
              "--disable-blink-features=AutomationControlled"],
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto(CAS_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)

    if fp and "fingerPrint" in fp:
        page.evaluate(
            "localStorage.setItem('fingerPrint', '" + fp["fingerPrint"] + "');"
            "localStorage.setItem('fingerGenPrint', '" + fp.get("fingerGenPrint","") + "');"
            "localStorage.setItem('fingerGenPrint3', '" + fp.get("fingerGenPrint3","") + "');"
        )
        time.sleep(1)

    page.fill("#i_user", USER)
    page.fill("#i_pass", PASS)
    page.evaluate("doLogin()")
    time.sleep(3)

    title = page.title()
    body  = page.inner_text("body")[:300]

    if "二次认证" in title or "二次验证" in body:
        if headless:
            ctx.close()
            return False, True, None, None
        print("需要二次验证。请在浏览器窗口中完成验证。", flush=True)
        try:
            page.wait_for_url("**://learn.tsinghua.edu.cn/**", timeout=120000)
            print("验证完成", flush=True)
        except Exception:
            print("二次验证超时。请重新运行并关注浏览器窗口。", flush=True)
            sys.exit(1)
    else:
        try:
            page.wait_for_url("**://learn.tsinghua.edu.cn/**", timeout=60000)
        except Exception:
            pass

    time.sleep(2)
    csrf = None
    if "_csrf" in page.url:
        for p2 in page.url.split("?")[1].split("&"):
            if p2.startswith("_csrf="): csrf = p2.split("=")[1]
    if not csrf:
        m = re.search(r'_csrf=([a-f0-9\-]{32,})', page.content())
        if m: csrf = m.group(1)
    state = save_state(ctx, page.url, csrf)
    print(f"JSESSIONID: {state.get('learn_jsession','?')[:10]}...")
    ctx.close()
    return True, False, None, None


pw = sync_playwright().start()

# 先试 headless
print("尝试 headless 登录...", flush=True)
ok, needs_2fa, _, _ = _try_login(headless=True)
if ok:
    print("headless 登录成功")
    pw.stop()
    sys.exit(0)

# headless 遇到 2FA，弹浏览器
print("检测到二次验证，弹出浏览器...", flush=True)
_try_login(headless=False)
pw.stop()
print("完成！以后运行 login_auto.py 即可无人值守登录。")