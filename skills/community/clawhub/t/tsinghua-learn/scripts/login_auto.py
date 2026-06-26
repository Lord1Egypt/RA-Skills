#!/usr/bin/env python3
"""
login_auto.py
清华网络学堂 - 无人值守自动登录脚本（双脚本方案·第二套）
==========================================================
【什么时候用】
  日常调用。Session 失效时自动重新登录，无需人工介入。

【工作流程】
  1. 检查 sessions/learn_session.json 里的 Session 是否有效
  2. 有效 → 直接返回（不登录）
  3. 无效 → 复用固定 Profile 的 cookies 自动走 CAS 登录（无 2FA）
  4. 登录成功后保存 Session

【核心原则】
  固定 profile 路径：profiles/learn_profile/
  账号密码从 credentials.json 统一读取（禁止硬编码）
"""
import sys, os, json, time, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
import requests

# ====== 账号密码（从 credentials.json 统一加载）=======
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


def check_session_valid(state):
    """用轻量 API 检查 Session 是否有效"""
    if not state.get("learn_jsession") or not state.get("csrf"):
        return False
    h = {
        "Accept": "application/json, */*",
        "Referer": "https://learn.tsinghua.edu.cn/f/wlxt/index/course/student/",
        "X-XSRF-TOKEN": state["csrf"],
        "Cookie": f"JSESSIONID={state['learn_jsession']}; XSRF-TOKEN={state['csrf']}",
    }
    try:
        r = requests.get(
            "https://learn.tsinghua.edu.cn/b/wlxt/kczy/zy/student/index/zyListWj?wlkcid=&size=1",
            headers=h, timeout=10
        )
        return not ("location.href" in r.text and r.status_code == 200)
    except:
        return False


def save_state(ctx, page_url, csrf):
    """提取并保存 Session"""
    learn_jsession = None
    for c in ctx.cookies():
        if "learn.tsinghua" in c["domain"] and c["name"] == "JSESSIONID":
            learn_jsession = c["value"]

    state = {
        "learn_jsession": learn_jsession,
        "learn_token":    None,
        "csrf":           csrf,
        "timestamp":      time.time(),
        "url":            page_url,
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"✅ Session 已保存")
    return state


def auto_login():
    """用固定 profile 的 cookies 自动登录（无 2FA）"""
    fp = json.load(open(FINGERPRINT_FILE, encoding="utf-8"))
    pw = sync_playwright().start()
    ctx = None
    try:
        ctx = pw.chromium.launch_persistent_context(
            PROFILE_DIR,
            headless=True,
            viewport={"width": 1280, "height": 900},
            args=["--no-sandbox", "--disable-dev-shm-usage",
                  "--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(CAS_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(2)

        page.evaluate(
            "localStorage.setItem('fingerPrint', '" + fp["fingerPrint"] + "');"
            "localStorage.setItem('fingerGenPrint', '" + fp.get("fingerGenPrint","") + "');"
            "localStorage.setItem('fingerGenPrint3', '" + fp.get("fingerGenPrint3","") + "');"
        )
        time.sleep(1)

        page.fill("#i_user", USER)
        page.fill("#i_pass", PASS)
        page.evaluate("doLogin()")

        page.wait_for_url("**://learn.tsinghua.edu.cn/**", timeout=30000)
        time.sleep(2)

        csrf = None
        if "_csrf" in page.url:
            for p2 in page.url.split("?")[1].split("&"):
                if p2.startswith("_csrf="): csrf = p2.split("=")[1]
        if not csrf:
            m = re.search(r'_csrf=([a-f0-9\-]{32,})', page.content())
            if m: csrf = m.group(1)

        return save_state(ctx, page.url, csrf)

    finally:
        if ctx: ctx.close()
        pw.stop()


# ========== 主流程 ==========
if os.path.exists(STATE_FILE):
    state = json.load(open(STATE_FILE, encoding="utf-8"))
    age_h = (time.time() - state.get("timestamp", 0)) / 3600
    print(f"Session 存在，age={age_h:.1f}h")

    if check_session_valid(state):
        print("✅ Session 有效，无需重新登录")
    else:
        print("⚠️ Session 失效，自动重新登录...")
        state = auto_login()
        print(f"JSESSIONID: {state.get('learn_jsession','?')[:10]}...")
else:
    print("⚠️ Session 文件不存在，运行 login_supervised.py 建立")
    print("   python scripts/login_supervised.py")
    sys.exit(1)