"""program.py — 培养方案查询子 SKILL 统一入口

通过 info 门户应用导航进入教务系统获取培养方案完成情况。JSON 输出。

流程:
  1. 确保 webvpn/info 会话（base-cas --system info --ensure）
  2. CDP 打开 info 应用导航页
  3. 点击"培养方案完成情况"应用（yyfwid），onlineAppRedirect 建立教务会话
  4. goto 培养方案业务 URL jhBks.by_fascjgmxb_gr.do → 解析摘要 + 课组 + 方案外课程

用法:
  program.py                       # 培养方案完成情况
  program.py --summary-only        # 仅摘要
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
PROG_YYFWID = "EF49444CB7D13C2AA029B911B0833CEE"
PROG_URL = ("https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b69336153301c9aa596522b20bc86e6e559a9b290"
            "/jhBks.by_fascjgmxb_gr.do?url=/jhBks.by_fascjgmxb_gr.do&xsViewFlag=pyfa&m=queryFaScjgmx_gr")


def _ensure_session():
    """确保 webvpn/info 会话；无有效会话时才登录（避免每次重登）。"""
    sess_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "runtime", "sessions", "info.json")
    if os.path.exists(sess_path):
        try:
            data = json.load(open(sess_path, encoding="utf-8"))
            age = time.time() - data.get("_updated", 0)
            if data.get("ticket") and age < 3600:
                common.log(f"[program] info 会话可用（age={int(age/60)}min），跳过登录")
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
        common.log(f"[program] 未找到应用 {app_name}，尝试文本点击")
        page.click(f"text={app_name}", timeout=5000)
    time.sleep(12)


def _parse_program(page):
    """解析培养方案页面（摘要 + 课组 + 方案外课程）。"""
    data = page.evaluate("""() => {
        const out = {summary: '', groups: [], outside: []};
        const body = document.body.innerText || '';
        // 摘要：取"本科生培养方案完成情况"段落的文本
        const m = body.match(/本科生培养方案完成情况[\\s\\S]*?课程属性/);
        if (m) out.summary = m[0].replace(/\\s+/g, ' ').replace('课程属性', '').trim().slice(0, 400);

        const tables = document.querySelectorAll('table');
        let curAttr = '', curGroup = '';
        tables.forEach(t => {
            const txt = t.innerText || '';
            const rows = [...t.querySelectorAll('tr')].map(tr =>
                [...tr.querySelectorAll('td,th')].map(td => (td.innerText||'').trim()));
            if (!rows.length) return;
            // 方案内课组表（表头含 应修学分+课程属性）——只取第一张，后续重复 view 跳过
            if (rows[0].includes('应修学分') && rows[0].includes('课程属性')) {
                if (out._groupsDone) return;
                out._groupsDone = 1;
                rows.slice(1).forEach(r => {
                    const isCourseRow =
                        (r.length >= 12 && /^[0-9]{5,9}$/.test(r[2]))
                        || (r.length === 11 && /^[0-9]{5,9}$/.test(r[1]))
                        || (r.length >= 5 && /^[0-9]{5,9}$/.test(r[0]));
                    if (!isCourseRow) return;
                    const codeIdx = r.length >= 12 ? 2 : (r.length >= 11 ? 1 : 0);
                    const code = r[codeIdx] || '';
                    if (!code) return;
                    const key = code + '|' + (r[codeIdx+1] || '');
                    if (out._gk && out._gk[key]) return;
                    out._gk = out._gk || {};
                    out._gk[key] = 1;
                    if (r.length >= 12) {
                        curAttr = r[0]; curGroup = r[1];
                        out.groups.push({
                            attr: curAttr, group: curGroup,
                            code: r[2], name: r[3], credit: r[4], grade: r[5], gpa: r[6],
                            need: r[7]||'', done: r[8]||'', needCnt: r[9]||'', doneCnt: r[10]||'', complete: r[11]||''
                        });
                    } else if (r.length >= 11) {
                        curGroup = r[0];
                        out.groups.push({
                            attr: curAttr, group: curGroup,
                            code: r[1], name: r[2], credit: r[3], grade: r[4], gpa: r[5],
                            need: r[6]||'', done: r[7]||'', needCnt: r[8]||'', doneCnt: r[9]||'', complete: r[10]||''
                        });
                    } else {
                        out.groups.push({
                            attr: curAttr, group: curGroup,
                            code: r[0], name: r[1], credit: r[2], grade: r[3], gpa: r[4]||'',
                            need: '', done: '', needCnt: '', doneCnt: '', complete: ''
                        });
                    }
                });
                return;
            }
            // 方案外课程表（表头含 学时+考试时间）
            if (rows[0].includes('学时') && rows[0].includes('考试时间')) {
                rows.slice(1).forEach(r => {
                    if (r.length >= 10 && r[0] && /^[0-9]{5,9}$/.test(r[0])) {
                        const key = r[0] + '|' + r[1] + '|' + r[2] + '|' + r[8];
                        if (out._ok && out._ok[key]) return;
                        out._ok = out._ok || {};
                        out._ok[key] = 1;
                        out.outside.push({
                            code: r[0], seq: r[1], name: r[2], credit: r[3], hours: r[4],
                            grade: r[5], gpa: r[6], attr: r[7], term: r[8], exam: r[9]
                        });
                    }
                });
            }
        });
        delete out._ok; delete out._gk;
        return out;
    }""")
    return data


def cmd_program(summary_only=False):
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
        page.goto(APPS_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(8)
        common.log("[program] 应用导航页已打开")
        body0 = page.inner_text("body")
        if "退出" not in body0 and "登录" in body0:
            # 应用导航页是独立 CAS service，跳 CAS 时自动登录
            import login as _login
            ok, msg = _login.ensure_apps_service(page, "培养方案完成情况")
            if not ok:
                common.output_json({"status": "error", "message": f"info 门户登录失败: {msg}"})
                sys.exit(1)
            common.log(f"[program] {msg}")
            page.goto(APPS_URL, wait_until="domcontentloaded", timeout=30000)
            time.sleep(8)
            body0 = page.inner_text("body")
            if "退出" not in body0 and "登录" in body0:
                common.output_json({"status": "error", "message": "info 会话仍无效（应用导航页显示未登录）。请稍后重试。"})
                sys.exit(1)
        _click_app(page, PROG_YYFWID, "培养方案完成情况")
        page.goto(PROG_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(6)
        common.log(f"[program] 培养方案 URL 加载: {page.url[:120]}")
        data = _parse_program(page)
        if not data["groups"]:
            body = page.inner_text("body")[:150]
            common.output_json({"status": "error", "message": "未解析到培养方案数据", "page": body})
            sys.exit(1)
        if summary_only:
            common.output_json({"status": "ok", "summary": data["summary"]})
            sys.exit(0)
        common.output_json({"status": "ok", "program": data})
    finally:
        # 即用即退：杀浏览器进程（会话信任靠落盘的 session cookie + profile 指纹恢复）
        try:
            browser.stop_cdp()
        except Exception:
            pass
        try:
            pw.stop()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser(description="培养方案查询")
    ap.add_argument("--summary-only", action="store_true", help="仅输出摘要")
    args = ap.parse_args()
    cmd_program(summary_only=args.summary_only)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        common.log(f"[program] 未捕获异常: {e}")
        common.output_json({"status": "error", "error": "unexpected", "message": f"脚本异常: {str(e)[:200]}"})
        sys.exit(1)
