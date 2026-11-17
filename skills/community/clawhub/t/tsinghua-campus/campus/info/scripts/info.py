"""info.py — 信息查询子 SKILL 统一入口

查询校内通知（info 门户）。登录走 base-cas info（webvpn，信任浏览器免 2FA）。
JSON 输出。

CLI:
  info.py notices [--category <分类>] [--limit N]  → 通知列表
  info.py read --xxid <id>                         → 通知详情

分类: 重要公告 / 办公通知 / 综合信息 / 教务通知 / 科研通知 / 招标招租
"""
import sys
import os
import json
import time
import argparse
import urllib.request
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "base-cas", "scripts"))
import common
import browser
import login

INFO_BASE = "https://webvpn.tsinghua.edu.cn/https/77726476706e69737468656265737421f9f9479369247b59700f81b9991b2631506205de"

# 通知分类 lmid
LMIDS = {
    "重要公告": "LM_XJ_ZYGG_UNION",
    "办公通知": "LM_XJ_BGTZ",
    "综合信息": "LM_XJ_ZHXX",
    "教务通知": "LM_XJ_JWTZ",
    "科研通知": "LM_XJ_KYTZ",
    "招标招租": "LM_XJ_ZBZZ",
}


def _ensure_login(page, ctx):
    """info 登录 —— 统一走 base-cas 会话复用（cookie 有效则免登录，失效才 CAS 填表）。"""
    return login.ensure_login("info", page, ctx, home_url=INFO_BASE)


def cmd_notices(category, limit):
    user = login._get_cred("cas_username")
    pwd = login._get_cred("cas_password")
    if not user or not pwd:
        common.output_json({"status": "error", "message": "CAS 凭据未配置"})
        sys.exit(1)
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        if not _ensure_login(page, ctx):
            common.output_json({"status": "error", "message": "info 登录失败"})
            sys.exit(1)
        common.log("[info] info 登录成功")
        # 通知列表
        lmid = LMIDS.get(category, LMIDS["重要公告"])
        page.goto(INFO_BASE + f"/f/info/xxfb_fg/xnzx/template/more?lmid={lmid}", wait_until="domcontentloaded", timeout=45000)


        data = page.evaluate("""() => {
            const out = [];
            document.querySelectorAll('a').forEach(a => {
                const href = a.getAttribute('href') || '';
                const m = href.match(/xxid=([a-f0-9]+)/);
                if (m) {
                    const t = (a.innerText||'').trim().replace(/\\s+/g,' ').slice(0, 60);
                    if (t && t.length > 4) out.push({xxid: m[1], title: t, url: href.slice(0, 130)});
                }
            });
            // 去重
            const seen = new Set(); const uniq = [];
            for (const o of out) { if (!seen.has(o.xxid)) { seen.add(o.xxid); uniq.push(o); } }
            return uniq;
        }""")
        # 过滤分类（列表页含多个分类）
        if category and category in LMIDS:
            # more 页可能只显示该分类，但保留过滤
            pass
        common.output_json({"status": "ok", "type": "notices", "category": category,
                            "notices": data[:limit]})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


def cmd_read(xxid):
    user = login._get_cred("cas_username")
    pwd = login._get_cred("cas_password")
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        if not _ensure_login(page, ctx):
            common.output_json({"status": "error", "message": "info 登录失败"})
            sys.exit(1)
        page.goto(INFO_BASE + f"/f/info/xxfb_fg/xnzx/template/detail?xxid={xxid}", wait_until="domcontentloaded", timeout=45000)


        body = page.inner_text("body")
        # 提取标题 + 正文（清理多余空白）
        import re
        text = re.sub(r'\s+', ' ', body).strip()
        common.output_json({"status": "ok", "type": "read", "xxid": xxid,
                            "text": text[:5000]})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


def cmd_search(query, limit):
    """水木搜索（馆藏检索）。公开，无需登录。

    水木搜索 = Primo explore（tsinghua-primo.hosted.exlibrisgroup.com.cn）。
    检索 API: /primo_library/libweb/webservices/rest/primo-explore/v1/pnxs
    （手动 fetch 403，需真实浏览器导航触发，捕获响应解析）。
    """
    PRIMO = "https://tsinghua-primo.hosted.exlibrisgroup.com.cn/primo-explore/search?vid=86THU"
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    page.set_viewport_size({"width": 1280, "height": 900})
    try:
        page.goto(PRIMO, wait_until="load", timeout=45000)


        with page.expect_response(lambda r: "pnxs" in r.url and "rest" in r.url, timeout=25000) as resp_info:
            page.fill("input[placeholder*='检索']", query)
            page.keyboard.press("Enter")
        resp = resp_info.value
        if resp.status != 200:
            common.output_json({"status": "error", "message": f"水木搜索失败（HTTP {resp.status}）"})
            sys.exit(1)
        d = json.loads(resp.text())
        docs = d.get("docs", [])[:limit]
        results = []
        for doc in docs:
            disp = doc.get("pnx", {}).get("display", {})
            title = disp.get("title", "")
            if isinstance(title, list):
                title = " | ".join(title)
            creator = disp.get("creator", "")
            if isinstance(creator, list):
                creator = " | ".join(creator)
            results.append({"title": title, "creator": creator,
                            "type": disp.get("type", ""), "date": disp.get("creationdate", "")})
        common.output_json({"status": "ok", "type": "search", "query": query,
                            "results": results})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser(description="信息查询（校内通知 + 水木搜索）")
    ap.add_argument("cmd", choices=["notices", "read", "search"])
    ap.add_argument("--category", default="重要公告", help="通知分类")
    ap.add_argument("--limit", type=int, default=10, help="列表条数")
    ap.add_argument("--xxid", default="", help="read: 通知 xxid")
    ap.add_argument("--query", default="", help="search: 检索词")
    args = ap.parse_args()
    if args.cmd == "notices":
        cmd_notices(args.category, args.limit)
    elif args.cmd == "read":
        if not args.xxid:
            common.output_json({"status": "error", "message": "read 需要 --xxid"})
            sys.exit(1)
        cmd_read(args.xxid)
    elif args.cmd == "search":
        if not args.query:
            common.output_json({"status": "error", "message": "search 需要 --query"})
            sys.exit(1)
        cmd_search(args.query, args.limit)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        common.log(f"[info] 未捕获异常: {e}")
        common.output_json({"status": "error", "error": "unexpected", "message": f"脚本异常: {str(e)[:200]}"})
        sys.exit(1)
