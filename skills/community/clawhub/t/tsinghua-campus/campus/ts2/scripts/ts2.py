"""ts2.py — 第二成绩单查询子 SKILL 统一入口

清华大学学生第二成绩单系统（transcript.student.tsinghua.edu.cn）。
记录本科生课外经历（社会工作/学术科研/竞赛/志愿公益/社会实践/体育/文艺等）。
登录走 CAS（信任浏览器免 2FA，无需 webvpn，全年可用）。JSON 输出。

用法:
  ts2.py status                    # 全部模块状态（已填/未填 + 学号）
  ts2.py list [模块]               # 某模块已填条目（省略=全部）
  ts2.py list --status 已通过       # 按状态筛选（已通过/审核中）
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
import login

TS_BASE = "https://transcript.student.tsinghua.edu.cn"

# 模块路径映射
MODULES = {
    "ay_innovations": ("创新训练", "学年填报"),
    "ay_research": ("科研项目", "学年填报"),
    "ay_contests": ("竞赛奖励", "学年填报"),
    "ay_arts": ("艺术比赛", "学年填报"),
    "ay_sports": ("体育比赛", "学年填报"),
    "ay_publications": ("学术论文", "学年填报"),
    "ay_creative": ("创作表演", "学年填报"),
    "ay_patents": ("专利授权", "学年填报"),
    "socialworks": ("社会工作", "信息填写"),
    "researches": ("学术科研", "信息填写"),
    "contests": ("竞赛比赛", "信息填写"),
    "innovations": ("创新创业", "信息填写"),
    "exchanges": ("海外研修及交换", "信息填写"),
    "volunteers": ("志愿公益", "信息填写"),
    "socials": ("社会实践", "信息填写"),
    "sports": ("体育表现", "信息填写"),
    "arts": ("文艺表现", "信息填写"),
    "projects": ("因材施教计划", "信息填写"),
    "unrecorded": ("其他", "信息填写"),
}


def _ensure_session():
    """确保 CAS 凭据存在（第二成绩单系统直连，走 CAS 登录）。"""
    user = login._get_cred("cas_username")
    pwd = login._get_cred("cas_password")
    if not user or not pwd:
        common.output_json({"status": "error", "needs": "creds", "message": "CAS 凭据未配置"})
        sys.exit(1)
    return {"status": "ok"}


def _auth(page, ctx):
    """CAS 登录第二成绩单系统 —— 统一走 base-cas 会话复用（cookie 有效则免登录）。"""
    ok = login.ensure_login("ts2", page, ctx, home_url=TS_BASE)
    return (True, {}) if ok else (False, {"message": "第二成绩单登录未完成（可能需要 2FA）"})


def _goto(page, path, settle=3):
    """导航到模块页。登录回跳后页面可能仍在导航，失败时等待重试。"""
    url = TS_BASE + path
    for attempt in range(3):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            break
        except Exception as e:
            if "interrupted" not in str(e) and "another navigation" not in str(e):
                raise
            common.log(f"[ts2] 导航被上次跳转打断，重试 {attempt + 1}")
            time.sleep(settle)
    # 等页面稳定（条件等待，替代固定 sleep(5)）
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass
    time.sleep(1)


def _parse_table(page):
    """解析模块页表格（序号/信息/状态/操作）。"""
    return page.evaluate("""() => {
        const out = {rows: [], explain: ''};
        const body = document.body.innerText || '';
        const ei = body.indexOf('填写说明');
        if (ei >= 0) out.explain = body.slice(ei, ei + 120).split('\\n')[0];
        document.querySelectorAll('table').forEach(t => {
            const rows = [...t.querySelectorAll('tr')].map(tr =>
                [...tr.querySelectorAll('td,th')].map(td => (td.innerText||'').trim()));
            if (rows.length > 1 && rows[0].includes('序号')) {
                rows.slice(1).forEach(r => {
                    if (r.length >= 3 && r[1]) out.rows.push({
                        info: r[1].replace(/\\n/g, ' | '),
                        status: r[2] || '',
                    });
                });
            }
        });
        return out;
    }""")


def _parse_status(page):
    """解析首页全部模块状态。"""
    return page.evaluate("""() => {
        const out = {student_id: '', modules: []};
        const body = document.body.innerText || '';
        const m = body.match(/^\\s*(20\\d{8})/);
        if (m) out.student_id = m[1];
        document.querySelectorAll('a[href]').forEach(a => {
            const href = a.getAttribute('href');
            const t = (a.innerText||'').trim().replace(/\\s+/g, ' ');
            if (href && href.startsWith('/') && t && (t.includes('已填') || t.includes('未填') || t.includes('（学年）') || t.includes('已通过'))) {
                const status = t.includes('已填') ? '已填' : (t.includes('未填') ? '未填' : '');
                out.modules.push({path: href.slice(1), label: t.replace(/已填|未填/g, '').trim(), status});
            }
        });
        return out;
    }""")


def cmd_status():
    sess = _ensure_session()
    if sess.get("status") != "ok":
        common.output_json(sess); sys.exit(1)
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        ok, err = _auth(page, ctx)
        if not ok:
            common.output_json({"status": "error", "message": err.get("message", "登录失败")})
            sys.exit(1)
        _goto(page, "/")
        data = _parse_status(page)
        common.output_json({"status": "ok", "type": "status", **data})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


def cmd_list(module="", status_filter=""):
    sess = _ensure_session()
    if sess.get("status") != "ok":
        common.output_json(sess); sys.exit(1)
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        ok, err = _auth(page, ctx)
        if not ok:
            common.output_json({"status": "error", "message": err.get("message", "登录失败")})
            sys.exit(1)
        # 先拿状态（学号 + 各模块已填/未填）
        _goto(page, "/")
        st = _parse_status(page)
        # 选择模块
        if module:
            paths = [module] if module in MODULES else [m for m, (label, cat) in MODULES.items() if label == module or m == module]
            if not paths:
                common.output_json({"status": "error", "message": f"未知模块 {module}。可选: {', '.join(list(MODULES.keys()) + [l for l,_ in MODULES.values()])}"})
                sys.exit(1)
            modules = {paths[0]: MODULES[paths[0]]}
        else:
            # 无参时只查已填模块，避免全遍历 19 个（每页导航+等待，太慢）
            filled = {m["path"] for m in st.get("modules", []) if m["status"] == "已填"}
            modules = {p: MODULES[p] for p, (label, cat) in MODULES.items() if p in filled}
            if not modules:
                common.log("[ts2] 无已填模块，仅返回状态")
        result = []
        for path, (label, cat) in modules.items():
            _goto(page, "/" + path)
            data = _parse_table(page)
            rows = data["rows"]
            if status_filter:
                rows = [r for r in rows if r["status"] == status_filter]
            result.append({"path": path, "label": label, "category": cat,
                           "count": len(rows), "rows": rows, "explain": data["explain"]})
        common.output_json({"status": "ok", "type": "list", "student_id": st.get("student_id", ""),
                            "modules": result, "module_status": st.get("modules", [])})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


def cmd_export(out_path=""):
    """导出第二成绩单 PDF（仅已通过条目）。"""
    sess = _ensure_session()
    if sess.get("status") != "ok":
        common.output_json(sess); sys.exit(1)
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        ok, err = _auth(page, ctx)
        if not ok:
            common.output_json({"status": "error", "message": err.get("message", "登录失败")})
            sys.exit(1)
        _goto(page, "/profile/export")
        result = page.evaluate("""async () => {
            const names = [...document.querySelectorAll('input[type=checkbox]')].map(c => c.name);
            const formData = new URLSearchParams();
            names.forEach(n => formData.append(n, 'on'));
            const resp = await fetch('/profile/export?_method=PUT', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: formData.toString(),
                credentials: 'include'
            });
            const buf = await resp.arrayBuffer();
            const ct = resp.headers.get('content-type') || '';
            let binary = '';
            const bytes = new Uint8Array(buf);
            for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
            return {status: resp.status, ct, b64: btoa(binary)};
        }""")
        if result["status"] != 200 or not result.get("b64"):
            common.output_json({"status": "error", "message": f"导出失败（HTTP {result['status']}）"})
            sys.exit(1)
        import base64
        pdf_bytes = base64.b64decode(result["b64"])
        if not out_path:
            out_path = os.path.join(str(common.runtime_dir("..")), "output", "ts2_export.pdf")
        out_path = os.path.abspath(out_path)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(pdf_bytes)
        common.output_json({"status": "ok", "type": "export", "size": len(pdf_bytes),
                            "saved_to": out_path, "message": "第二成绩单 PDF 已导出"})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser(description="第二成绩单查询")
    ap.add_argument("cmd", nargs="?", default="status", choices=["status", "list", "export"])
    ap.add_argument("module", nargs="?", default="", help="模块路径或中文名（list 用）")
    ap.add_argument("--status", default="", help="按状态筛选（已通过/审核中）")
    ap.add_argument("--out", default="", help="导出 PDF 保存路径（export 用）")
    args = ap.parse_args()
    if args.cmd == "status":
        cmd_status()
    elif args.cmd == "export":
        cmd_export(args.out)
    else:
        cmd_list(args.module, args.status)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        common.log(f"[ts2] 未捕获异常: {e}")
        common.output_json({"status": "error", "error": "unexpected", "message": f"脚本异常: {str(e)[:200]}"})
        sys.exit(1)
