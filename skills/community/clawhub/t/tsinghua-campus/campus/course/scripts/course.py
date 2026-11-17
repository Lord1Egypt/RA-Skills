"""course.py — 选课系统查询子 SKILL 统一入口

通过选课系统（zhjwxk）查询开课信息（任课老师）、学生推荐度、已选课程。
选课系统走 webvpn http 编码 + 二次 CAS 认证（信任浏览器免 2FA，偶发图形验证码）。

流程:
  1. 确保 webvpn/info 会话
  2. CDP 访问 xklogin.do（webvpn 编码）→ 触发 CAS
  3. 填 CAS 凭据 → doLogin（偶发图形验证码 → 两阶段）
  4. 进入选课系统 → 访问业务页取数据

用法:
  course.py teacher [--query <关键词>]    # 开课信息（任课老师）
  course.py recommend                     # 学生推荐度
  course.py enrolled                      # 已选课程（退课查询）
  course.py --submit-captcha <token> <code>  # 图形验证码两阶段
"""
import sys
import os
import json
import time
import uuid
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "base-cas", "scripts"))
import common
import browser
import login

INFO_BASE = "https://webvpn.tsinghua.edu.cn/https/77726476706e69737468656265737421f9f9479369247b59700f81b9991b2631506205de"
APPS_URL = INFO_BASE + "/f/info/portal_fg/student/yyfwxxindex"
COURSE_YYFWID = "A7298655396722EF78BA5B5FB0B5482A"
BASE = ("https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b2653770bc7b88b5c2d320506b1aec738590a49ba")
XKLOGIN = BASE + "/xklogin.do"
CURRENT_TERM = "2026-2027-1"

CAPTCHA_TTL = 300
_KEEP_BROWSER = False


def _ensure_session():
    """确保 webvpn/info 会话。"""
    sess_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "runtime", "sessions", "info.json")
    if os.path.exists(sess_path):
        try:
            data = json.load(open(sess_path, encoding="utf-8"))
            age = time.time() - data.get("_updated", 0)
            if data.get("ticket") and age < 3600 * 4:
                common.log(f"[course] info 会话可用（age={int(age/60)}min），跳过登录")
                return {"status": "ok"}
        except Exception:
            pass
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "base-cas", "scripts", "login.py"),
                        "--system", "info", "--ensure"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    try:
        out = json.loads(r.stdout or "{}")
    except Exception:
        out = {"status": "error", "raw": r.stdout[:200]}
    if out.get("needs") == "2fa_code":
        return {"status": "pending", "needs": "2fa_code", "pending": out.get("pending")}
    if not out.get("session_valid"):
        return {"status": "error", "message": "info 登录失败"}
    return {"status": "ok"}


def _captcha_path(token):
    return os.path.join(str(common.runtime_dir("captcha")), f"captcha_{token}.png")


def _pending_path(token):
    return os.path.join(str(common.pending_dir()), f"captcha_{token}.json")


def _write_pending(token, data):
    os.makedirs(str(common.pending_dir()), exist_ok=True)
    with open(_pending_path(token), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _read_pending(token):
    p = _pending_path(token)
    if not os.path.exists(p):
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _save_captcha(page, token):
    """保存 CAS 图形验证码截图。"""
    import io
    common.runtime_dir("captcha").mkdir(parents=True, exist_ok=True)
    try:
        # 优先截【可见】的验证码图区域（#captcha 常驻但仅需要时才可见）
        el = None
        for sel in ("#captcha", "img[src*='captcha']", "img[src*='Captcha']", ".captcha"):
            for h in page.query_selector_all(sel):
                try:
                    if h.is_visible():
                        el = h
                        break
                except Exception:
                    pass
            if el is not None:
                break
        if el is not None:
            el.screenshot(path=_captcha_path(token))
        else:
            page.screenshot(path=_captcha_path(token), full_page=False)
    except Exception:
        try:
            page.screenshot(path=_captcha_path(token), full_page=False)
        except Exception:
            return None
    return _captcha_path(token)


def _check_captcha(page):
    """检测 CAS 登录页是否出现图形验证码（精确：必须有验证码输入框或图片）。"""
    try:
        has = page.evaluate("""() => {
            const hasInput = !!document.querySelector('input[name=captcha], input[id=captcha], input[placeholder*="验证码"]');
            const hasImg = !!document.querySelector('img[src*="captcha"], img[src*="Captcha"]');
            return hasInput || hasImg;
        }""")
        return bool(has)
    except Exception:
        return False


def _auth(page, ctx, captcha_token=None, captcha_code=None):
    """选课系统 CAS 认证 —— 统一走 base-cas 会话复用；图形验证码走 captcha_handler。

    captcha_token/code 提供时填入图形验证码后登录。
    """
    def _captcha(pg, context, system):
        if captcha_token is None:
            token = uuid.uuid4().hex[:12]
            img = _save_captcha(pg, token)
            _write_pending(token, {"token": token, "system": "course", "created": time.time(),
                                   "captcha_image": img})
            global _KEEP_BROWSER
            _KEEP_BROWSER = True
            common.output_json({
                "status": "pending", "needs": "captcha", "pending": token,
                "captcha_image": img,
                "message": "选课系统 CAS 需图形验证码。浏览器已保持打开，请查看验证码图片后调用 course.py --submit-captcha <token> <code>",
            })
            sys.exit(2)
        else:
            try:
                pg.fill("input[name=captcha], #captcha, input[placeholder*='验证码']", captcha_code)
            except Exception:
                pass

    ok = login.ensure_login("course", page, ctx, home_url=XKLOGIN,
                            logged_in_check="() => location.href.indexOf('id.tsinghua') < 0",
                            captcha_handler=_captcha)
    if ok:
        return True, {}
    return False, {"message": "选课系统认证失败（可能验证码错误或系统不稳定）"}


def _submit_captcha(token, code):
    """阶段2：连接【同一浏览器】填图形验证码完成登录（复用 _auth / ensure_login）。"""
    pending = _read_pending(token)
    if not pending:
        common.output_json({"status": "error", "message": f"pending 不存在或已过期: {token}"})
        sys.exit(1)
    if not browser.is_running():
        common.output_json({"status": "error", "message": "CDP 浏览器已退出（验证码会话丢失），请重新执行查询命令"})
        sys.exit(1)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    ok, err = _auth(page, ctx, captcha_token=token, captcha_code=code)
    if not ok:
        common.output_json({"status": "error", "message": err.get("message", "验证码登录失败")})
        try:
            pw.stop()
        except Exception:
            pass
        sys.exit(1)
    common.log("[course] 验证码登录成功")
    try:
        os.remove(_pending_path(token))
    except Exception:
        pass
    common.output_json({"status": "ok", "message": "选课系统认证成功！请重新执行查询命令（如 course.py teacher --query 数学）"})
    try:
        pw.stop()
    except Exception:
        pass
    sys.exit(0)


def _goto_biz(page, path):
    """访问选课系统业务页。"""
    url = BASE + path
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
    except Exception:
        return []
    time.sleep(12)
    rows = []
    for fr in page.frames:
        try:
            txt = fr.inner_text("body")
            if txt and len(txt) > 20:
                # 解析表格
                trows = fr.evaluate("""() => {
                    const out = [];
                    document.querySelectorAll('table').forEach(t => {
                        const rows = [...t.querySelectorAll('tr')].map(tr =>
                            [...tr.querySelectorAll('td,th')].map(td => (td.innerText||'').trim()));
                        if (rows.length >= 1 && rows[0].length > 2) out.push(rows);
                    });
                    return out;
                }""")
                if trows:
                    rows = trows
                    break
        except Exception:
            pass
    return rows


def cmd_teacher(query=""):
    sess = _ensure_session()
    if sess.get("status") == "pending":
        common.output_json(sess); sys.exit(2)
    if sess.get("status") != "ok":
        common.output_json(sess); sys.exit(1)
    user = login._get_cred("cas_username")
    pwd = login._get_cred("cas_password")
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    keep_browser = False
    try:
        ok, err = _auth(page, ctx)
        if not ok:
            common.output_json({"status": "error", "message": err.get("message", "认证失败")})
            sys.exit(1)
        common.log("[course] 选课系统认证成功")
        # 开课信息（一级课）
        path = "/xkBks.vxkBksJxjhBs.do?m=kkxxSearch"
        if query:
            path += "&p_kcm=" + query
        tables = _goto_biz(page, path)
        common.output_json({"status": "ok", "type": "teacher", "query": query, "tables": tables})
    except SystemExit:
        raise
    finally:
        try:
            global _KEEP_BROWSER
            if not _KEEP_BROWSER:
                browser.stop_cdp()
        except Exception:
            pass


def cmd_enrolled():
    sess = _ensure_session()
    if sess.get("status") == "pending":
        common.output_json(sess); sys.exit(2)
    if sess.get("status") != "ok":
        common.output_json(sess); sys.exit(1)
    user = login._get_cred("cas_username")
    pwd = login._get_cred("cas_password")
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        ok, err = _auth(page, ctx)
        if not ok:
            common.output_json({"status": "error", "message": err.get("message", "认证失败")})
            sys.exit(1)
        common.log("[course] 选课系统认证成功")
        path = f"/xkBks.vxkBksTkbBs.do?m=tkSearchSingle&p_xnxq={CURRENT_TERM}&pathContent=退课查询"
        tables = _goto_biz(page, path)
        common.output_json({"status": "ok", "type": "enrolled", "tables": tables})
    except SystemExit:
        raise
    finally:
        try:
            global _KEEP_BROWSER
            if not _KEEP_BROWSER:
                browser.stop_cdp()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser(description="选课系统查询（只读）")
    ap.add_argument("cmd", nargs="?", default="enrolled", choices=["teacher", "enrolled", "recommend"])
    ap.add_argument("--query", default="", help="teacher 查询关键词（课程名）")
    ap.add_argument("--submit-captcha", nargs=2, metavar=("TOKEN", "CODE"), help="图形验证码两阶段")
    args = ap.parse_args()
    if args.submit_captcha:
        _submit_captcha(*args.submit_captcha)
    if args.cmd == "teacher":
        cmd_teacher(args.query)
    elif args.cmd == "recommend":
        common.output_json({"status": "ok", "message": "学生推荐度查询开发中，先用 teacher 查任课老师"})
    else:
        cmd_enrolled()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        common.log(f"[course] 未捕获异常: {e}")
        common.output_json({"status": "error", "error": "unexpected", "message": f"脚本异常: {str(e)[:200]}"})
        sys.exit(1)
