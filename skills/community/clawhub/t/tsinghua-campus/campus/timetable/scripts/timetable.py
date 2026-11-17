"""timetable.py — 课表查询子 SKILL 统一入口

通过 info 门户应用导航进入教务系统获取课表。JSON 输出。

流程:
  1. 确保 webvpn/info 会话（base-cas --system info --ensure）
  2. CDP 打开 info 应用导航页
  3. 点击"课表"应用（yyfwid），onlineAppRedirect 跳转教务
  4. 解析 portal3rd.do 课表数据（星期×节次表格）

用法:
  timetable.py [--semester auto]   # 当前学期课表
"""
import sys
import os
import json
import time
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "base-cas", "scripts"))
import common
import browser

INFO_BASE = "https://webvpn.tsinghua.edu.cn/https/77726476706e69737468656265737421f9f9479369247b59700f81b9991b2631506205de"
APPS_URL = INFO_BASE + "/f/info/portal_fg/student/yyfwxxindex"
KB_YYFWID = "287C0C6D90ABB364CD5FDF1495199962"
KB_URL = "https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b69336153301c9aa596522b20bc86e6e559a9b290/portal3rd.do?url=/portal3rd.do&m=bks_yjkbSearch"


def _ensure_session():
    """确保 webvpn/info 会话；无有效会话时才登录（避免每次重登）。"""
    import os
    sess_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "runtime", "sessions", "info.json")
    if os.path.exists(sess_path):
        try:
            import time as _t
            data = json.load(open(sess_path, encoding="utf-8"))
            age = _t.time() - data.get("_updated", 0)
            if data.get("ticket") and age < 3600:  # webvpn ticket 实际有效期短，1h 内才信任
                common.log(f"[timetable] info 会话可用（age={int(age/60)}min），跳过登录")
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


def _click_app(page, yyfwid, app_name):
    """在应用导航页点击指定应用（真实点击，触发 Vue 事件）。"""
    try:
        page.click(f"[yyfwid='{yyfwid}']", timeout=8000)
        common.log(f"[timetable] 点击应用 {app_name}")
        time.sleep(12)
        return
    except Exception:
        pass
    # 备选：文本点击
    try:
        page.click(f"text={app_name}", timeout=8000)
        time.sleep(12)
        return
    except Exception:
        pass
    # 最后：JS 点击（旧应用导航可能 JS 绑定）
    page.evaluate("""(yyfwid) => {
        const els = [...document.querySelectorAll('[yyfwid], a, li, div')];
        const target = els.find(el =>
            el.getAttribute('yyfwid') === yyfwid ||
            (el.getAttribute('onclick')||'').includes(yyfwid)
        );
        if (target) {
            const real = target.closest('[yyfwid]') || target.closest('[onclick]') || target;
            real.click();
        }
    }""", yyfwid)
    time.sleep(12)


def _parse_timetable(page):
    """解析课表表格。"""
    data = page.evaluate("""() => {
        const out = {schedule: [], unplaced: []};
        const tables = document.querySelectorAll('table');
        if (tables.length > 0) {
            const t = tables[0];
            const headers = [...t.querySelectorAll('tr:first-child td, tr:first-child th')]
                .map(td => (td.innerText||'').trim());
            t.querySelectorAll('tr').forEach((tr, ri) => {
                if (ri === 0) return;
                const cells = [...tr.querySelectorAll('td,th')].map(td => (td.innerText||'').trim());
                if (cells.length > 1) out.schedule.push({period: cells[0], days: cells.slice(1)});
            });
        }
        if (tables.length > 1) {
            const t2 = tables[1];
            t2.querySelectorAll('tr').forEach((tr, ri) => {
                if (ri === 0) return;
                const cells = [...tr.querySelectorAll('td')].map(td => (td.innerText||'').trim());
                if (cells.length >= 3) out.unplaced.push({code: cells[0], seq: cells[1], name: cells[2]});
            });
        }
        return out;
    }""")
    return data


def cmd_timetable():
    sess = _ensure_session()
    if sess.get("status") == "pending":
        common.output_json({"status": "pending", "needs": "2fa_code", "pending": sess.get("pending"),
                            "message": "需要二次验证。请提供验证码后调用 base-cas login.py --submit-code"})
        sys.exit(2)
    if sess.get("status") != "ok":
        common.output_json(sess)
        sys.exit(1)

    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        # 打开应用导航
        page.goto(APPS_URL, wait_until="domcontentloaded", timeout=30000)

        common.log("[timetable] 应用导航页已打开")
        # 检测登录态（webvpn ticket 可能已过期但文件年龄未超）
        body0 = page.inner_text("body")
        if "退出" not in body0 and "登录" in body0:
            # 应用导航页是独立 CAS service，跳 CAS 时自动登录
            import login as _login
            ok, msg = _login.ensure_apps_service(page, "课表")
            if not ok:
                common.output_json({"status": "error", "message": f"info 门户登录失败: {msg}"})
                sys.exit(1)
            common.log(f"[timetable] {msg}")
            page.goto(APPS_URL, wait_until="domcontentloaded", timeout=30000)
            time.sleep(8)
            body0 = page.inner_text("body")
            if "退出" not in body0 and "登录" in body0:
                common.output_json({"status": "error", "message": "info 会话仍无效（应用导航页显示未登录）。请稍后重试。"})
                sys.exit(1)
        # 点击课表
        _click_app(page, KB_YYFWID, "课表")
        common.log(f"[timetable] 点击后 pages={len(ctx.pages)}")
        # 直接 goto 课表 URL（onlineAppRedirect 已建立 zhjw 教务会话）
        page.goto(KB_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(6)
        common.log(f"[timetable] 课表 URL 加载: {page.url[:120]}")
        data = _parse_timetable(page)
        if not data["schedule"]:
            body = page.inner_text("body")[:150]
            common.output_json({"status": "error", "message": "未解析到课表数据", "page": body})
            sys.exit(1)
        common.output_json({"status": "ok", "timetable": data})
    finally:
        # 保留浏览器常驻：信任会话是 session cookie，杀进程即丢失
        try:
            pw.stop()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser(description="课表查询")
    ap.add_argument("--semester", default="auto")
    args = ap.parse_args()
    cmd_timetable()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        common.log(f"[timetable] 未捕获异常: {e}")
        common.output_json({"status": "error", "error": "unexpected", "message": f"脚本异常: {str(e)[:200]}"})
        sys.exit(1)
