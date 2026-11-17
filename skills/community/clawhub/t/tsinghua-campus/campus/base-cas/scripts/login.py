"""login.py — 清华 CAS 统一登录（浏览器即用即退 + 两阶段验证码）

核心架构：保留的是【cookie/session 文件 + profile 指纹】，不是浏览器进程。
浏览器一律即用即退 —— 仅 2FA 流程内保持打开等待用户填码，完成后即关闭。

- 信任机制：THU 通过浏览器指纹（profile）判断是否二次验证。首次登录走
  saveFinger 信任 → 指纹存服务端 + 本地 profile，后续同 profile 重启免 2FA。
- 会话复用：登录成功提取 session（含完整 cookie 快照）落地 sessions/*.json；
  下次任务先验证 cookie 有效性，有效直接用，无效 fall back 重新登录。

两阶段:
  阶段1: login.py --system <name> --ensure
     → session 有效 → 立即成功退出（浏览器不保留）
     → 否则启动/连接 CDP 浏览器 → CAS 登录 → 触发 2FA 发短信
       → 浏览器保持打开（仅此阶段）→ 立即返回 {"needs":"2fa_code","pending":"<token>"}
  阶段2: login.py --submit-code <token> <code>
     → CDP 连接【同一浏览器】→ 填码 → 信任确认 → 提取 session
     → 关闭 CDP 浏览器 → 写正式 session → 退出

支持的系统:
  learn → https://learn.tsinghua.edu.cn
  info  → https://info.tsinghua.edu.cn
  seat  → https://seat.lib.tsinghua.edu.cn
"""
import sys
import os
import json
import time
import uuid
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "creds", "scripts"))
import common
import vault
import session
import browser

CAS_URL = "https://id.tsinghua.edu.cn/do/off/ui/auth/login/form/bb5df85216504820be7bba2b0ae1535b/0"

# webvpn 编码前缀（Wengine: wrdvpnisthebest! + 域名编码），已实测确认
WEBVPN_BASE = "https://webvpn.tsinghua.edu.cn"
WEBVPN_PREFIX = "77726476706e69737468656265737421"  # wrdvpnisthebest!
WV_CODES = {
    "learn": "fcf2408e297e7c4377068ea48d546d30ca8cc97bcc",  # learn.tsinghua.edu.cn
    "info": "f9f9479369247b59700f81b9991b2631506205de",     # info.tsinghua.edu.cn
}

SYSTEMS = {
    # access: direct = 直连域名；webvpn = 走 webvpn 前缀
    "learn": {"target": "https://learn.tsinghua.edu.cn", "home": "/f/wlxt/index/course/student/", "access": "direct"},
    "info": {"target": "https://info.tsinghua.edu.cn", "home": "/", "access": "webvpn"},
    "seat": {"target": "https://seat.lib.tsinghua.edu.cn", "home": "/home/web/f_second", "access": "webvpn"},
}


def _system_url(system, path=None):
    """返回系统访问 URL。direct 直连；webvpn 走编码前缀。"""
    cfg = SYSTEMS[system]
    if cfg.get("access") == "webvpn":
        code = WV_CODES.get(system)
        if not code:
            raise RuntimeError(f"系统 {system} 缺少 webvpn 编码")
        base = f"{WEBVPN_BASE}/https/{WEBVPN_PREFIX}{code}"
    else:
        base = cfg["target"]
    return base + (path if path is not None else cfg.get("home", "/"))

CREDS_FILE = str(common.runtime_dir("credentials.json"))

PENDING_TTL = 300  # 验证码等待超时（秒）
RESULT_WAIT = 90   # submit-code 后等待登录完成上限


def _get_cred(key):
    """从凭据保险箱取明文（统一走 vault.vault_get）。"""
    return vault.vault_get(key)


def _pending_path(token):
    return os.path.join(str(common.pending_dir()), f"2fa_{token}.json")


def _code_path(token):
    return os.path.join(str(common.pending_dir()), f"2fa_{token}.code")


def _read_pending(token):
    p = _pending_path(token)
    if not os.path.exists(p):
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _write_pending(token, data):
    os.makedirs(str(common.pending_dir()), exist_ok=True)
    with open(_pending_path(token), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _fill_cas(page, user, pwd):
    """填 CAS 表单（i_user/i_pass/doLogin）。

    若已登录（信任浏览器直接跳转，无 #i_user 表单）则跳过填表。
    """
    try:
        # 先快速检测是否已是登录态（信任浏览器直接跳转，不显示表单）
        if page.locator("#i_user").count() == 0:
            common.log("[login] CAS 表单未出现（可能已是登录态/信任浏览器），跳过填表")
            return
        page.wait_for_selector("#i_user", timeout=15000)
    except Exception:
        common.log("[login] CAS 表单未出现，跳过填表")
        return
    try:
        page.fill("#i_user", user)
        page.fill("#i_pass", pwd)
        try:
            page.evaluate("doLogin()")
        except Exception:
            try:
                page.click("button:has-text('登录'), #logBtn, input[type=submit]", timeout=5000)
            except Exception:
                pass
    except Exception as e:
        common.log(f"[login] CAS 填表异常: {e}")


def _select_sms_and_send(page):
    """在 2FA 页选短信(mobile)并点发送。返回 True 若成功触发。"""
    try:
        page.wait_for_selector("input[name=type][value=mobile]", timeout=10000)
        try:
            page.check("input[name=type][value=mobile]")
        except Exception:
            page.evaluate("document.querySelector('input[name=type][value=mobile]').click()")
        time.sleep(1)
        try:
            page.click("button:has-text('确定')")
        except Exception:
            pass
        return True
    except Exception as e:
        common.log(f"[login] 选择短信方式失败: {e}")
        return False


def _fill_code_and_submit(page, code):
    """填验证码并提交。2FA 页验证码输入框为 #vericode（name=vericode）。"""
    selectors = ["input[name=vericode]", "#vericode", "input[name=captcha]", "input[name=code]",
                 "input[placeholder*='验证码']", "input[type=text]"]
    filled = False
    for sel in selectors:
        try:
            if page.locator(sel).count() > 0:
                page.fill(sel, code)
                filled = True
                break
        except Exception:
            continue
    if not filled:
        common.log("[login] 未找到验证码输入框")
        return False
    time.sleep(1)
    try:
        page.click("button:has-text('确定')")
    except Exception:
        try:
            page.click("input[type=submit]")
        except Exception:
            pass
    return True


def _click_trust(page):
    """完成 CAS 信任确认：选'是'（信任）+ 真实点击'确定'。

    信任浏览器是必要的（否则每次都要 2FA）。若 saveFinger 返回
    '信任浏览器数量已达到上限'，需引导用户清理旧信任设备（本函数只提交，
    错误处理在 submit_code 中基于 saveFinger 响应完成）。
    """
    try:
        if "login/check" not in page.url or page.locator("input[name=type]").count() == 0:
            return False
        try:
            page.check("input[name=type][value=是]")
        except Exception:
            page.evaluate("document.querySelector('input[name=type][value=是]').checked = true")
        time.sleep(0.5)
        clicked = False
        for sel in ["button:has-text('确定')", "button.btn-info", "input[type=submit]"]:
            try:
                if page.locator(sel).count() > 0:
                    page.locator(sel).first.click(timeout=5000)
                    clicked = True
                    common.log(f"[login] 已点击信任'确定': {sel}")
                    break
            except Exception:
                continue
        if not clicked:
            page.evaluate("""() => {
                const btns = [...document.querySelectorAll('button,input[type=button],input[type=submit]')];
                const b = btns.find(b => /确定/.test(b.innerText||b.value||''));
                if (b) b.click();
            }""")
            common.log("[login] JS 触发信任'确定'按钮")
        return True
    except Exception as e:
        common.log(f"[login] 信任提交失败: {e}")
        return False


def _save_session_cookies(system, context):
    """保存系统完整 cookie 快照（跨进程复用）。"""
    try:
        ck = context.cookies()
        data = session.load_session(system) or {}
        data["_cookies"] = ck
        session.save_session(system, data)
        common.log(f"[login] {system} cookie 快照已保存（{len(ck)} 条）")
    except Exception as e:
        common.log(f"[login] {system} 保存 cookie 失败: {e}")


def ensure_login(system, page, context, home_url=None, logged_in_check=None, trigger_js=None,
                 fill_timeout=20, captcha_handler=None):
    """统一的页面登录（整页 CAS + iframe CAS），带 cookie 复用。

    ⚠️ **所有子 SKILL 的登录必须走此函数，不得自己实现 CAS 填表。**

    流程：
      1. 注入 session 里保存的 cookie（`_cookies`）
      2. 导航 home_url
      3. 已登录（logged_in_check 为真，或默认：URL 在系统域且 body 无登录文案）→ 存 cookie 返回 True
      4. 出现 CAS 表单（整页 `#i_user` 或 iframe `id.tsinghua`）→ 填表 → 存 cookie 返回 True
      5. 失败返回 False

    参数：
      home_url: 系统主页（导航 + 判断登录态）
      logged_in_check: 可选 JS 表达式（返回 bool）判断是否已登录
      trigger_js: 可选 JS，触发登录入口（如 seat 需点"登录"才出现 CAS iframe）
      fill_timeout: CAS 填表后等待登录成功的轮数（每轮 3s）
    """
    user = _get_cred("cas_username")
    pwd = _get_cred("cas_password")

    def _logged_in():
        if logged_in_check:
            try:
                return bool(page.evaluate(logged_in_check))
            except Exception:
                return False
        try:
            host = home_url.split("/")[2] if home_url else ""
            if not host or host not in page.url:
                return False
            body = page.inner_text("body")
            return not any(m in body for m in ("用户密码登录", "二次认证", "二次验证"))
        except Exception:
            return False

    def _fill_cas():
        """填 CAS 表单（整页或 iframe）。返回是否已填。"""
        # 整页 CAS
        try:
            if "id.tsinghua" in page.url and page.locator("#i_user").count() > 0:
                for _ in range(8):
                    try:
                        if page.evaluate("() => typeof window.doLogin === 'function'"):
                            break
                    except Exception:
                        pass
                    time.sleep(1)
                page.fill("#i_user", user)
                page.fill("#i_pass", pwd)
                page.evaluate("doLogin()")
                common.log(f"[login] {system} 整页 CAS 已填表")
                return True
        except SystemExit:
            raise
        except Exception:
            pass
        # iframe CAS
        for fr in page.frames:
            try:
                if "id.tsinghua" in fr.url:
                    for _ in range(8):
                        try:
                            if fr.evaluate("() => typeof window.doLogin === 'function'"):
                                break
                        except Exception:
                            pass
                        time.sleep(1)
                    fr.fill("#i_user", user)
                    fr.fill("#i_pass", pwd)
                    fr.evaluate("doLogin()")
                    common.log(f"[login] {system} iframe CAS 已填表")
                    return True
            except Exception:
                pass
        return False

    # 1. 注入已保存 cookie（跨进程复用）
    n = session.inject_cookies(context, system)
    common.log(f"[login] {system} 注入 cookie {n} 条")
    if home_url:
        try:
            page.goto(home_url, wait_until="domcontentloaded", timeout=45000)
        except Exception:
            pass
        time.sleep(4)
    # 2. 已登录？（cookie 有效 → 免登录）
    for _ in range(4):
        if _logged_in():
            _save_session_cookies(system, context)
            return True
        time.sleep(2)
    # 3. 触发登录入口（如 seat 需点"登录"才出现 CAS iframe）
    if trigger_js:
        try:
            page.evaluate(trigger_js)
            time.sleep(4)
        except Exception:
            pass
    # 4. 未登录 → CAS 填表
    filled = False
    for _ in range(fill_timeout):
        # 图形验证码（可选回调）：CAS 表单验证码【可见】时才需要，由调用方填码或 exit(2) 返回 pending
        if captcha_handler is not None:
            has_cap = False
            try:
                loc = page.locator("input[name=captcha], #captcha, input[placeholder*='验证码']")
                for k in range(loc.count()):
                    if loc.nth(k).is_visible():
                        has_cap = True
                        break
            except Exception:
                has_cap = False
            if has_cap:
                try:
                    captcha_handler(page, context, system)
                except SystemExit:
                    raise
                except Exception:
                    pass
                filled = False  # 含验证码 → 需重新填表
        if not filled:
            filled = _fill_cas()
        # 信任确认页（login/check）
        try:
            if "login/check" in page.url:
                _click_trust(page)
        except Exception:
            pass
        if filled and _logged_in():
            _save_session_cookies(system, context)
            return True
        time.sleep(3)
    # 5. 再等一轮
    for _ in range(5):
        time.sleep(3)
        if _logged_in():
            _save_session_cookies(system, context)
            return True
    return False


# 向后兼容别名
ensure_iframe_cas = ensure_login


def _extract_session(system, browser_obj, page, context=None):
    """按系统提取会话。

    - learn（direct）: 提取 learn 域 JSESSIONID + XSRF-TOKEN（CSRF）
    - webvpn 类系统: 提取 webvpn 域 wengine_vpn_ticket

    同时附加完整 cookie 快照（`_cookies`），供后续复用（浏览器即用即退后，
    跨进程的信任态靠此 cookie + profile 指纹恢复）。
    """
    cookies = context.cookies() if context is not None else []
    cfg = SYSTEMS.get(system, {})
    access = cfg.get("access", "direct")

    if access == "webvpn":
        ticket = None
        for c in cookies:
            if "webvpn" in c["domain"] and c["name"] == "wengine_vpn_ticket":
                ticket = c["value"]
        result = {"ticket": ticket}
    else:
        # direct: learn 类（JSESSIONID + XSRF-TOKEN）
        jsession = None
        xsrf = None
        for c in cookies:
            if cfg["target"].replace("https://", "") in c["domain"]:
                if c["name"] == "JSESSIONID":
                    jsession = c["value"]
                elif c["name"] == "XSRF-TOKEN":
                    xsrf = c["value"]
        csrf = xsrf or ""
        if not csrf and "_csrf" in page.url:
            for p in page.url.split("?")[1].split("&"):
                if p.startswith("_csrf="):
                    csrf = p.split("=")[1]
        if not csrf:
            import re
            m = re.search(r'_csrf=([a-f0-9\-]{32,})', page.content())
            if m:
                csrf = m.group(1)
        result = {"jsession": jsession, "csrf": csrf}
    result["_cookies"] = [
        {"name": c["name"], "value": c["value"], "domain": c["domain"], "path": c.get("path", "/")}
        for c in cookies
    ]
    return result


def _close_browser(pw=None):
    """优雅关闭 CDP 浏览器：先断开 playwright 连接（避免 node EPIPE），再杀进程。"""
    if pw is not None:
        try:
            pw.stop()
        except Exception:
            pass
    browser.stop_cdp()


def ensure_apps_service(page, app_name="", max_wait=45):
    """确保 info 门户【应用导航页（学生工作台）】的 CAS service 会话已建立。

    背景：webvpn 根路径（info 门户首页）与应用导航页（/f/info/portal_fg/student/yyfwxxindex）
    是**两个独立的 CAS service**。base-cas 登录只建立 webvpn 根的 ticket；直接访问应用导航页
    会被重定向到 CAS 登录表单（提示"您即将登录 清华大学信息门户"），需完成该 service 的
    登录（信任浏览器通常免密，headless 偶发图形验证码但实测可绕过）。

    返回 (ok: bool, message: str)。调用方应先 goto 应用导航页，再调用本函数。
    """
    user = _get_cred("cas_username")
    pwd = _get_cred("cas_password")
    # 等 doLogin / 表单就绪（最多 max_wait 秒）
    t0 = time.time()
    while time.time() - t0 < max_wait:
        if "id.tsinghua" not in page.url:
            return True, "已登录（应用导航页正常访问）"
        try:
            ready = page.evaluate("() => typeof window.doLogin === 'function'") or page.locator("#i_user").count() > 0
            if ready:
                break
        except Exception:
            pass
        time.sleep(2)
    if "id.tsinghua" not in page.url:
        return True, "已登录"
    # 已登录态（表单未出现）→ 成功
    try:
        if page.locator("#i_user").count() == 0:
            return True, "CAS 表单未出现（信任浏览器自动完成）"
    except Exception:
        pass
    # 填表登录
    try:
        page.wait_for_selector("#i_user", timeout=10000)
        page.type("#i_user", user, delay=30)
        page.type("#i_pass", pwd, delay=30)
        page.evaluate("doLogin()")
        common.log("[login] 应用导航页 CAS 已填表（service 登录）")
    except Exception as e:
        return False, f"应用导航页 CAS 填表异常: {str(e)[:80]}"
    # 等跳转（含信任确认）
    for i in range(20):
        time.sleep(2)
        cur = page.url
        if "login/check" in cur:
            try:
                _click_trust(page)
            except Exception:
                pass
        if "id.tsinghua" not in cur:
            # 回跳成功：可能是应用导航页或门户工作台
            time.sleep(3)
            return True, "应用导航页 service 登录成功"
    # 超时：不能再谎报"可能已建立"——明确验证页面是否真的离开认证域
    try:
        final_url = page.url
        if "id.tsinghua" not in final_url:
            time.sleep(3)
            return True, "应用导航页已离开认证域（超时后确认）"
        return False, f"应用导航页 CAS 登录超时（仍停在认证域 {final_url[:80]}）"
    except Exception as e:
        return False, f"应用导航页登录确认异常: {str(e)[:80]}"


def _open_cas_login(system):
    """连接 CDP 浏览器，导航到登录入口并填表。

    - direct 系统（learn）: 直接 goto CAS 登录页（learn 的 service），
      learn 首页不自动跳 CAS（显示"登录失效"需点登录），须从 CAS_URL 进入
    - webvpn 系统: goto 系统 URL（webvpn→CAS 自动跳转）

    返回 (pw, browser, context, page)。
    """
    pw, b, ctx, page = browser.connect_cdp()
    # 自动接受弹窗（confirm/alert）
    page.on("dialog", lambda d: d.accept())
    cfg = SYSTEMS.get(system, {})
    if cfg.get("access") == "webvpn":
        page.goto(_system_url(system), wait_until="domcontentloaded", timeout=30000)
    else:
        page.goto(CAS_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)
    # 若在 CAS 登录页，填表
    if "id.tsinghua.edu.cn" in page.url:
        user = _get_cred("cas_username")
        pwd = _get_cred("cas_password")
        _fill_cas(page, user, pwd)
    return pw, b, ctx, page


def _learn_session_real_valid(data=None):
    """learn 会话真实验证。data 传入时用该会话验证（不经 session 文件）；
    否则读 session 文件。learn 会话会过期，字段检查不足。"""
    try:
        if data:
            # 用传入的 jsession/csrf 直接验证
            jsession = data.get("jsession") or data.get("learn_jsession")
            csrf = data.get("csrf")
            if not jsession or not csrf:
                return False
            import requests
            h = {
                "Accept": "application/json, */*",
                "Referer": "https://learn.tsinghua.edu.cn/f/wlxt/index/course/student/",
                "X-XSRF-TOKEN": csrf,
                "Cookie": f"JSESSIONID={jsession}; XSRF-TOKEN={csrf}",
            }
            r = requests.get(
                "https://learn.tsinghua.edu.cn/b/wlxt/kczy/zy/student/index/zyListWj?wlkcid=&size=1",
                headers=h, timeout=10)
            return r.status_code == 200 and "location.href" not in r.text[:500]
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "learn", "scripts"))
        import learn_api
        api = learn_api.LearnAPI()
        return api.reload_session()
    except Exception:
        return False


def _info_session_real_valid(data=None):
    """info 会话真实验证（webvpn）。

    ⚠️ info.json 里的 ticket 是登录时的快照，webvpn 每次访问都会滚动换发
    （旧 ticket 随即作废），因此不能像 learn 那样用 requests 带旧 ticket 探测
    （必然失败）。真正的会话在浏览器的 cookie + profile 信任指纹里。

    做法：启动一个【临时】CDP 浏览器（同 profile，信任指纹复用）访问 info
    门户根路径。若被重定向回 id.tsinghua（CAS）则会话已失效；若停留在
    webvpn 域则有效，并顺手把换发后的最新 ticket 写回 session 文件。
    探测完成后立即关闭浏览器（即用即退，不保留进程）。

    data 传入时仅做字段检查（与 learn 签名对称），探测始终走浏览器。
    浏览器不可用 → 无法验证 → 视为失效（login_ensure 会重新登录）。
    """
    if data is not None:
        return bool(data.get("ticket"))
    browser.start_cdp(headed=False)
    pw = None
    try:
        pw, b, ctx, page = browser.connect_cdp()
        page.on("dialog", lambda d: d.accept())
        page.goto(_system_url("info"), wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        url = page.url
        valid = "id.tsinghua.edu.cn" not in url
        if valid:
            # 更新滚动换发后的 ticket（快照 → 最新）
            data = _extract_session("info", b, page, context=ctx)
            if data.get("ticket"):
                data["url"] = page.url
                session.save_session("info", data)
        return valid
    except Exception:
        return False
    finally:
        _close_browser(pw)


def login_ensure(system, headed=False):
    """阶段1：确保 session；否则触发 2FA，浏览器保持打开，立即返回 pending。"""
    if system not in SYSTEMS:
        common.output_json({"status": "error", "message": f"未知系统 {system}", "systems": list(SYSTEMS.keys())})
        sys.exit(1)
    if session.session_valid(system):
        # learn/info 会话会过期，字段存在不代表有效 → 真实验证
        real_valid = True
        if system == "learn" and not _learn_session_real_valid():
            real_valid = False
        elif system == "info" and not _info_session_real_valid():
            real_valid = False
        if not real_valid:
            common.log(f"[login] {system} session 字段存在但已失效，重新登录")
            session.clear_session(system)
        else:
            s = session.load_session(system)
            common.output_json({"status": "ok", "system": system, "session_valid": True,
                                "session": {k: (v[:12] + "…" if isinstance(v, str) and len(v) > 12 else v) for k, v in s.items() if k != "_updated"}})
            return
    user = _get_cred("cas_username")
    pwd = _get_cred("cas_password")
    if not user or not pwd:
        common.output_json({"status": "error", "message": "CAS 凭据未配置", "needs": "creds", "run": "creds.py guide cas_username"})
        sys.exit(1)

    # 启动/复用 CDP 常驻浏览器
    browser.start_cdp(headed=headed)
    pw, b, ctx, page = _open_cas_login(system)

    # 等离开认证域 或 出现 2FA（最多 ~30s，带进度日志避免误判卡死）
    jumped = False
    is_webvpn = SYSTEMS[system].get("access") == "webvpn"
    for i in range(20):
        time.sleep(1.5)
        cur = page.url
        try:
            body = page.inner_text("body")[:200] if page.url else ""
        except Exception:
            body = ""
        common.log(f"[login] 等待认证跳转 ({i+1}/20) url={cur[:60]}")
        if is_webvpn:
            # webvpn 系统：登录后回到 webvpn 的 <system> URL 即算成功
            if "id.tsinghua.edu.cn" not in cur and "oauth.tsinghua.edu.cn" not in cur:
                jumped = True
                break
        else:
            if "id.tsinghua.edu.cn" not in cur and "oauth.tsinghua.edu.cn" not in cur and "webvpn.tsinghua.edu.cn" not in cur:
                jumped = True
                break  # 已登录（信任浏览器，直接成功）
        # 凭据错误 / 锁定等 CAS 报错，立即返回明确错误（不等超时）
        if "用户名或密码不正确" in body or "密码错误" in body or "账号被锁定" in body or "登录失败" in body:
            _close_browser(pw)
            common.output_json({"status": "error", "error": "cas_credential",
                                "message": "CAS 用户名或密码不正确（或账号异常）。请用 creds.py 重新配置 cas_username / cas_password 后重试。"})
            sys.exit(1)
        if "二次认证" in body or "二次验证" in body or "验证码" in body:
            token = uuid.uuid4().hex[:12]
            pending = {
                "token": token,
                "system": system,
                "created": time.time(),
                "status": "awaiting_code",
                "message": "已触发二次验证，浏览器保持打开等待验证码",
            }
            _write_pending(token, pending)
            sms_ok = _select_sms_and_send(page)
            if not sms_ok:
                _close_browser(pw)
                common.output_json({"status": "error", "error": "sms_failed",
                                    "message": "2FA 页面结构异常，未能选择短信验证方式。请手动在浏览器中操作或稍后重试。"})
                sys.exit(1)
            common.output_json({
                "status": "pending",
                "needs": "2fa_code",
                "pending": token,
                "message": "已向登记手机发送短信验证码。请让用户提供验证码，然后调用 login.py --submit-code <token> <code>（浏览器已保持打开，验证码不会失效）",
            })
            # 关闭 playwright 连接但保持 CDP 浏览器进程存活
            try:
                pw.stop()
            except Exception:
                pass
            sys.exit(2)

    # 循环耗尽仍停在认证域 → 明确报错（避免误判）
    if not jumped and "id.tsinghua.edu.cn" in page.url:
        _close_browser(pw)
        common.output_json({"status": "error", "error": "login_timeout",
                            "message": f"CAS 登录 30 秒内未完成跳转（停在 {page.url[:80]}），可能是图形验证码/网络问题。请重试 --ensure 或手动检查浏览器。"})
        sys.exit(1)

    # 未触发 2FA 直接成功（信任浏览器）：提取 session
    # 跳转到系统目标页（direct 直连 / webvpn 前缀），确保会话在目标域
    target_url = _system_url(system)
    if "/f/login" in page.url or "webvpn.tsinghua" in page.url:
        page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
    # 稳定等待：learn 会话在跳转后建立，稍等让 cookie 落定
    if system == "learn":
        time.sleep(2)
        # 重试提取：首次提取可能拿到跳转前的临时 JSESSIONID
        valid = False
        for _try in range(3):
            data = _extract_session(system, b, page, context=ctx)
            if data.get("jsession") and _learn_session_real_valid(data):
                valid = True
                break
            common.log(f"[login] learn session 提取重试 {_try+1}/3")
            time.sleep(2)
        if not valid:
            _close_browser(pw)
            common.output_json({
                "status": "error", "error": "session_invalid",
                "message": "learn 登录后 session 无效（信任浏览器复用可能未建立 learn 会话）。请删除 cdp_profile 或走完整 2FA 登录。",
            })
            sys.exit(1)
    else:
        data = _extract_session(system, b, page, context=ctx)
    if system == "learn" and (not data["jsession"] or not data["csrf"]):
        _close_browser(pw)
        common.output_json({"status": "error", "message": f"登录后未提取到 learn session，停在 {page.url}"})
        sys.exit(1)
    if system == "info" and not data["ticket"]:
        _close_browser(pw)
        common.output_json({"status": "error", "message": f"登录后未提取到 webvpn 会话，停在 {page.url}"})
        sys.exit(1)
    data["url"] = page.url
    session.save_session(system, data)
    _close_browser(pw)
    common.output_json({"status": "ok", "system": system, "session_valid": True,
                        "browser_closed": True,
                        "session": {k: (v[:12] + "…" if isinstance(v, str) and len(v) > 12 else v) for k, v in data.items() if k != "_cookies"}})


def submit_code(token, code, headed=False):
    """阶段2：CDP 连接【同一浏览器】填验证码完成登录（不重开浏览器）。"""
    pending = _read_pending(token)
    if not pending:
        common.output_json({"status": "error", "message": f"pending 不存在或已过期: {token}"})
        sys.exit(1)
    system = pending["system"]

    if not browser.is_running():
        common.output_json({"status": "error", "message": "CDP 浏览器已退出（验证码会话丢失），请重新执行 --ensure"})
        sys.exit(1)

    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    # 当前页面应是 2FA 验证码页
    try:
        page.wait_for_selector("#vericode, input[name=vericode]", timeout=10000)
    except Exception:
        pass
    common.log(f"[login] 填码提交 {code[:3]}***（{time.strftime('%H:%M:%S')}）")
    _fill_code_and_submit(page, code)

    # 等信任确认页出现（radio name=type），15s 内；出现则点击信任（真实按钮）
    # 同时用 expect_response 可靠捕获 saveFinger 响应（不能靠事件回调里读 body）
    trust_submitted = False
    sf_body = ""
    try:
        page.wait_for_selector("input[name=type]", timeout=15000)
        body = page.inner_text("body")[:200]
        if "信任" in body:
            common.log("[login] 检测到信任确认页，立即提交信任")
            with page.expect_response(lambda r: "saveFinger" in r.url, timeout=15000) as sf_resp:
                trust_submitted = _click_trust(page)
            try:
                sf_body = sf_resp.value.text() or ""
            except Exception:
                sf_body = ""
    except Exception:
        pass

    # 检查 saveFinger 是否返回信任上限错误
    if "信任浏览器数量已达到上限" in sf_body:
        common.log("[login] saveFinger: 信任浏览器数量已达到上限")
        common.output_json({
            "status": "error",
            "error": "trust_limit",
            "message": (
                "信任浏览器数量已达上限（约 15 个），无法将本浏览器加入信任列表。\n"
                "请打开浏览器登录 https://id.tsinghua.edu.cn 后，进入「账号设置 → 多因子认证 → 信任浏览器数量 维护」"
                "，删除 1-2 个旧设备（直接入口: https://id.tsinghua.edu.cn/f/account/trustDeviceIndex），"
                "然后重新执行登录。"
            ),
        })
        _close_browser(pw)
        sys.exit(3)

    # 检查验证码是否填错（页面停在 2FA 且报错）
    if not trust_submitted:
        try:
            body2 = page.inner_text("body")[:300]
            if "不正确" in body2 or "错误" in body2 or "验证码" in body2:
                common.log("[login] 验证码可能错误或已过期")
                common.output_json({
                    "status": "error",
                    "error": "code_invalid",
                    "message": "验证码可能错误或已过期（或信任确认页未出现）。请重新执行 --ensure 获取新验证码后重试。",
                })
                _close_browser(pw)
                sys.exit(4)
        except Exception:
            pass

    # 等跳转目标系统（信任已提交 → JS 跳转）
    try:
        page.wait_for_url(f"**{SYSTEMS[system]['target'].replace('https://','')}**", timeout=30000)
    except Exception:
        pass

    if "/f/login" in page.url or "webvpn.tsinghua" in page.url:
        page.goto(_system_url(system), wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
    data = _extract_session(system, b, page, context=ctx)
    if system == "learn" and (not data["jsession"] or not data["csrf"]):
        _close_browser(pw)
        common.output_json({"status": "error", "message": f"未提取到 learn session，停在 {page.url}"})
        sys.exit(1)
    if system == "info" and not data["ticket"]:
        _close_browser(pw)
        common.output_json({"status": "error", "message": f"未提取到 webvpn 会话，停在 {page.url}"})
        sys.exit(1)
    data["url"] = page.url
    session.save_session(system, data)
    _close_browser(pw)
    try:
        os.remove(_pending_path(token))
        os.remove(_code_path(token))
    except Exception:
        pass
    common.output_json({"status": "ok", "system": system, "session_valid": True,
                        "browser_closed": True,
                        "session": {k: (v[:12] + "…" if isinstance(v, str) and len(v) > 12 else v) for k, v in data.items() if k != "_cookies"}})


def cmd_reset():
    """【CAS 系统重置】清空 CAS 登录态：CAS 凭据 + session + profile + browser 残留。

    职责边界（与 creds.py reset 分工）:
      - creds.py reset <system>  = 只清某系统的【凭据】（keyring），不动登录态
      - login.py --reset        = 只清【CAS 系统】：CAS 凭据 + learn/info session
                                  + CDP profile（浏览器 cookies）+ browser 残留
    文献/mail/llm 等其他系统的凭据不受影响（它们不属于 CAS，用 creds.py reset 管理）。

    覆盖:
      - CAS 凭据（cas_username/cas_password/student_id/student_name）文件+keyring
      - sessions/*.json + pending/
      - profiles/cdp_profile + profiles/default_profile（浏览器 cookies/设置）
      - browser/cdp.pid + cdp.port
    保留: logs/ screenshots/ downloads/ uploads/ submissions/（历史排错与用户数据）
    """
    import shutil

    CAS_CRED_KEYS = ("cas_username", "cas_password", "student_id", "student_name")

    # 1. 关闭 CDP 浏览器（先停进程，避免 profile 文件被锁）
    try:
        browser.stop_cdp()
    except Exception:
        pass

    cleared = []

    # 2. 仅清 CAS 凭据（文件 + keyring），其他系统凭据保留
    if os.path.exists(CREDS_FILE):
        try:
            stored = _load_creds()
            for key in list(stored.keys()):
                if key not in CAS_CRED_KEYS:
                    continue
                ref = stored[key]
                if isinstance(ref, str) and ref.startswith("keyring:"):
                    acct = ref[len("keyring:"):]
                    try:
                        import keyring
                        keyring.delete_password("campus-skill", acct)
                    except Exception:
                        pass
                del stored[key]
                cleared.append("cred:" + key)
            if not stored:
                os.remove(CREDS_FILE)
            else:
                with open(CREDS_FILE, "w", encoding="utf-8") as f:
                    json.dump(stored, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # 3. sessions + pending
    sd = str(common.session_dir())
    if os.path.isdir(sd):
        for f in os.listdir(sd):
            p = os.path.join(sd, f)
            try:
                if os.path.isdir(p):
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    os.remove(p)
                cleared.append("session:" + f)
            except Exception:
                pass

    # 4. profiles（浏览器设置/cookies）
    pd = str(common.runtime_dir("profiles"))
    if os.path.isdir(pd):
        for name in os.listdir(pd):
            p = os.path.join(pd, name)
            try:
                shutil.rmtree(p, ignore_errors=True)
                cleared.append("profile:" + name)
            except Exception:
                pass

    # 5. browser 残留（pid/port 文件）
    bd = str(common.runtime_dir("browser"))
    if os.path.isdir(bd):
        for name in os.listdir(bd):
            p = os.path.join(bd, name)
            try:
                if os.path.isfile(p):
                    os.remove(p)
            except Exception:
                pass

    common.output_json({"status": "ok", "cleared": cleared,
                        "message": "已重置 CAS 系统（凭据+会话+浏览器 profile）。文献/邮件/LLM 凭据不受影响；如需重置它们用 creds.py reset <system>"})


def main():
    ap = argparse.ArgumentParser(description="清华 CAS 统一登录（CDP 常驻浏览器 + 两阶段）")
    ap.add_argument("--system", default="learn", choices=list(SYSTEMS.keys()), help="目标系统")
    ap.add_argument("--ensure", action="store_true", help="阶段1：触发 2FA（浏览器保持打开）")
    ap.add_argument("--submit-code", nargs=2, metavar=("TOKEN", "CODE"), help="阶段2：填验证码完成登录")
    ap.add_argument("--headed", action="store_true", help="（已废弃，恒 headless——产品决策全部无头模式）")
    ap.add_argument("--stop", action="store_true", help="关闭 CDP 浏览器")
    ap.add_argument("--reset", action="store_true", help="[CAS 系统重置] 清 CAS 凭据+learn/info session+浏览器 profile（不碰文献/邮件/LLM 凭据）")
    args = ap.parse_args()

    if args.reset:
        cmd_reset()
        return
    if args.stop:
        browser.stop_cdp()
        common.output_json({"status": "ok", "message": "CDP 浏览器已关闭"})
        return
    if args.submit_code:
        submit_code(args.submit_code[0], args.submit_code[1], headed=args.headed)
        return
    if args.ensure:
        login_ensure(args.system, headed=args.headed)
        return
    common.output_json({"status": "error", "message": "需要 --ensure 或 --submit-code", "usage": "login.py --system learn --ensure"})


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        # 兜底：任何未捕获异常输出 JSON（不产生 traceback 到 stderr）
        common.log(f"[login] 未捕获异常: {e}")
        common.output_json({"status": "error", "error": "unexpected",
                            "message": f"脚本异常: {str(e)[:200]}。请重试或查看 runtime/logs/campus.log。"})
        sys.exit(1)
