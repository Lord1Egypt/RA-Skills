"""transcript.py — 成绩单查询子 SKILL 统一入口

通过 info 门户应用导航进入教务系统获取成绩。JSON 输出。

流程:
  1. 确保 webvpn/info 会话（base-cas --system info --ensure）
  2. CDP 打开 info 应用导航页
  3. 点击"全部成绩"应用（yyfwid），onlineAppRedirect 建立教务会话
  4. goto 成绩单业务 URL cj.cjCjbAll.do → 解析学生信息 + 课程成绩 + 汇总

用法:
  transcript.py                       # 全部成绩（当前学位）
  transcript.py --section 二学位       # 按分类（一学位/二学位/辅修）
  transcript.py --json                # 原始 JSON（默认）
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
SCORE_YYFWID = "0A4DFABA3A5876334F71F94654FCC4A8"
SCORE_URL = ("https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b69336153301c9aa596522b20bc86e6e559a9b290"
             "/cj.cjCjbAll.do?url=/cj.cjCjbAll.do&cjdlx=zw&m=bks_cjdcx")


def _ensure_session():
    """确保 webvpn/info 会话；由 login.py 做真实会话验证（非时间戳启发式）。

    info.json 的 ticket 是登录时快照，webvpn 滚动换发后即失效，本地
    时间戳判断不可靠 → 一律交给 login.py --system info --ensure 探测。
    """
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
    """在应用导航页点击指定应用。"""
    clicked = page.evaluate("""(yyfwid) => {
        const els = [...document.querySelectorAll('[yyfwid], [data-yyfwid], a, li, div')];
        const target = els.find(el =>
            el.getAttribute('yyfwid') === yyfwid ||
            el.getAttribute('data-yyfwid') === yyfwid ||
            ((el.getAttribute('onclick')||'').includes(yyfwid))
        );
        if (target) {
            const real = target.closest('[yyfwid]') || target.closest('[onclick]') || target;
            real.click();
            return true;
        }
        return false;
    }""", yyfwid)
    if not clicked:
        common.log(f"[transcript] 未找到应用 {app_name}，尝试文本点击")
        page.click(f"text={app_name}", timeout=5000)
    time.sleep(12)


def _parse_transcript(page):
    """解析成绩单页面（学生信息 + 课程成绩 + 汇总）。"""
    data = page.evaluate("""() => {
        const out = {student: {}, courses: [], summary: {}};
        const tables = document.querySelectorAll('table');
        tables.forEach((t, i) => {
            const rows = [...t.querySelectorAll('tr')].map(tr =>
                [...tr.querySelectorAll('td,th')].map(td => (td.innerText||'').trim()));
            // 学生信息表（含 姓名/学号）
            if (rows.some(r => r.some(c => c.includes('学号') || c.includes('姓名')))) {
                rows.forEach(r => {
                    const flat = r.filter(c => c && !/^[\\s\\u3000]*$/.test(c));
                    if (flat.length >= 2) {
                        for (let j = 0; j + 1 < flat.length; j += 2) {
                            const k = flat[j].replace(/[：:]/g,'').replace(/[\\s\\u3000]/g,'');
                            if (/^[\\u4e00-\\u9fa5]+$/.test(k)) out.student[k] = flat[j+1];
                        }
                    }
                });
            }
            // 课程成绩表（含 课程号 表头）
            if (rows.length > 1 && rows[0].includes('课程号')) {
                rows.slice(1).forEach(r => {
                    if (r.length >= 6 && r[0]) out.courses.push({
                        code: r[0], name: r[1], credit: r[2], grade: r[3], gpa: r[4], term: r[5]
                    });
                });
            }
            // 汇总表（含 总学分）
            if (rows.some(r => r.some(c => c.includes('总学分')))) {
                rows.forEach(r => {
                    for (let j = 0; j < r.length; j += 2) {
                        if (j + 1 < r.length) out.summary[r[j].replace(/\\s/g,'')] = r[j+1];
                    }
                });
            }
        });
        return out;
    }""")
    return data


def cmd_transcript():
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
    # 注入已保存的 info/webvpn cookie，恢复跨进程信任态（即用即退后凭此免重登）
    import session as _session
    _session.inject_cookies(ctx, "info")
    try:
        page.goto(APPS_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(8)
        common.log("[transcript] 应用导航页已打开")
        body0 = page.inner_text("body")
        if "退出" not in body0 and "登录" in body0:
            # 应用导航页是独立 CAS service，跳 CAS 时自动登录（信任浏览器免密/自动填表）
            import login as _login
            ok, msg = _login.ensure_apps_service(page, "全部成绩")
            if not ok:
                common.output_json({"status": "error", "message": f"info 门户登录失败: {msg}"})
                sys.exit(1)
            common.log(f"[transcript] {msg}")
            page.goto(APPS_URL, wait_until="domcontentloaded", timeout=30000)
            time.sleep(8)
            body0 = page.inner_text("body")
            if "退出" not in body0 and "登录" in body0:
                common.output_json({"status": "error", "message": "info 会话仍无效（应用导航页显示未登录）。请稍后重试。"})
                sys.exit(1)
        _click_app(page, SCORE_YYFWID, "全部成绩")
        page.goto(SCORE_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(6)
        common.log(f"[transcript] 成绩单 URL 加载: {page.url[:120]}")
        data = _parse_transcript(page)
        if not data["courses"]:
            body = page.inner_text("body")[:150]
            common.output_json({"status": "error", "message": "未解析到成绩数据", "page": body})
            sys.exit(1)
        common.output_json({"status": "ok", "transcript": data})
    finally:
        # 即用即退：浏览器用完即关。信任态靠 cookies/session 文件 + profile 指纹保留
        try:
            browser.stop_cdp()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser(description="成绩单查询")
    ap.add_argument("--section", default="", help="成绩分类（一学位/二学位/辅修）")
    args = ap.parse_args()
    cmd_transcript()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        common.log(f"[transcript] 未捕获异常: {e}")
        common.output_json({"status": "error", "error": "unexpected", "message": f"脚本异常: {str(e)[:200]}"})
        sys.exit(1)
