"""sources/info.py — info.tsinghua.edu.cn 信息门户搜索

info 直连（校园网可用）；本机（机房 IP）会跳 webvpn，需登录态。
实现:
  1. 通知分类列表浏览（lmid 参数，公开可用）
  2. 站内全文搜索（typeahead 接口，需登录态，校园网验证）

注意: 搜索接口在 webvpn 代理下 JS 会被替换，用户校园网环境直连可用。
"""
import sys
import os
import re
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "shared", "scripts"))
import common

SOURCE_NAME = "info"
BASE = "https://info.tsinghua.edu.cn"
# webvpn 前缀（wrdvpnisthebest! + info 域编码）
WEBVPN_BASE = "https://webvpn.tsinghua.edu.cn/https/77726476706e69737468656265737421f9f9479369247b59700f81b9991b2631506205de"

# 通知分类（lmid）
LMIDS = {
    "重要公告": "LM_XJ_ZYGG_UNION",
    "办公通知": "LM_XJ_BGTZ",
    "综合信息": "LM_XJ_ZHXX",
}


def _fetch_browser(path, params=None):
    """用 base-cas CDP 浏览器带登录态访问 info（webvpn 前缀，cookie 由 profile/session 提供）。

    本机（机房 IP）直连 info.tsinghua.edu.cn 会被 webvpn/CAS 拦截，必须经
    webvpn 前缀 + 登录态。复用 base-cas 的 profile 指纹 + 落盘 cookie 快照
    （session.py inject_cookies），即用即退。
    返回 (html, ok)。
    注意：通知列表是 JS 动态渲染，需 goto + networkidle 后用 inner_text 提取。"""
    import urllib.parse
    base_cas_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "base-cas", "scripts")
    sys.path.insert(0, base_cas_dir)
    try:
        import browser as _browser
        import session as _session
        pw = None
        owned = False
        try:
            if _browser.is_running():
                pw, b, ctx, page = _browser.connect_cdp()
            else:
                _browser.start_cdp(headed=False)
                owned = True
                pw, b, ctx, page = _browser.connect_cdp()
            page.on("dialog", lambda d: d.accept())
            # 注入 info session 的 cookie 快照（webvpn ticket 等），恢复信任态
            n = _session.inject_cookies(ctx, "info")
            common.log(f"[info] 注入 info cookie {n} 条")
            q = urllib.parse.urlencode(params or {})
            path_q = path + ("?" + q if q else "")
            # 先访问 webvpn 根（建立 webvpn 会话/消费换发 ticket），再 goto 目标页
            page.goto(WEBVPN_BASE, wait_until="domcontentloaded", timeout=25000)
            if "id.tsinghua" in page.url:
                common.log("[info] info 会话失效（跳 CAS），无法站内搜索")
                return [], False
            page.goto(WEBVPN_BASE + path_q, wait_until="networkidle", timeout=30000)
            # 提取渲染后的所有通知链接（JS 列表已展开）
            links = page.eval_on_selector_all(
                "a", "els => els.map(e => ({href: e.href, text: (e.innerText||'').trim().slice(0,120)}))")
            return links, True
        finally:
            if owned:
                try:
                    _browser.stop_cdp()
                except Exception:
                    pass
            if pw is not None and not owned:
                try:
                    pw.stop()
                except Exception:
                    pass
    except Exception as e:
        common.log(f"[info] CDP 访问失败: {e}")
        return [], False


def _fetch(path, params=None):
    """获取 info 页面（直连 info.tsinghua.edu.cn，校园网可用）。

    注意: 本机测试（机房 IP）会被重定向到 webvpn/CAS，返回跳转页导致空结果。
    校园网内 info.tsinghua.edu.cn 直连可用。搜索接口需登录态（CDP 会话）。"""
    import urllib.request
    import urllib.parse
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="replace")


def _parse_notices(html, limit):
    """解析通知列表页，提取标题+链接。"""
    results = []
    seen = set()
    # 通知链接常见: /f/info/xxfb_fg/xnzx/template/detail?xxid=...
    for m in re.finditer(r'<a[^>]*href="([^"]*detail\?xxid=[^"]*)"[^>]*>([^<]{4,100})</a>', html):
        href, title = m.group(1), m.group(2).strip()
        if title in seen or len(title) < 4:
            continue
        seen.add(title)
        url = href if href.startswith("http") else BASE + href
        results.append({"source": SOURCE_NAME, "title": title, "url": url, "snippet": ""})
        if len(results) >= limit:
            break
    return results


def search(query, limit=5):
    """info 搜索：在通知分类里匹配关键词（含站内全文搜索接口说明）。"""
    common.log(f"[info] 搜索: {query}")
    results = []
    # 方式1: 浏览器带登录态（webvpn）+ 渲染后链接，匹配关键词（本机可用，JS 列表）
    try:
        links, ok = _fetch_browser("/f/info/xxfb_fg/xnzx/stu/index")
        common.log(f"[info] 浏览器返回 ok={ok} links={len(links)} sample={links[0] if links else None} xxid_in_module={sum(1 for l in links if 'xxid' in str(l.get('href','')))}")
        # 调试：打印所有 xxid 标题（检查是否有"选课"）
        xids = [l.get("text","").strip() for l in links if "xxid" in str(l.get("href",""))]
        common.log(f"[info] xxid 标题样例: {xids[:5]} | 含选课: {sum(1 for t in xids if '选课' in t)} | 含安排: {sum(1 for t in xids if '安排' in t)}")
        if ok and links:
            seen = set()
            # 关键词 2 字词拆分（处理"选课、退课安排" vs "选课安排"这类标点差异）
            words = [q for q in (query[i:i+2] for i in range(0, len(query), 2)) if q] if len(query) >= 2 else [query]
            for l in links:
                if "xxid" not in l.get("href", ""):
                    continue
                title = l.get("text", "").strip()
                if not title or len(title) < 4 or title in seen:
                    continue
                hit = query in title or all(w in title for w in words)
                if hit:
                    seen.add(title)
                    results.append({"source": SOURCE_NAME, "title": title,
                                    "url": l["href"], "snippet": "[学生版首页]"})
            common.log(f"[info] 浏览器 xxid 候选 {len(seen)} 条，命中 {len(results)} 条")
            if results:
                common.log(f"[info] 浏览器渲染匹配 {len(results)} 条")
                return results
    except Exception as e:
        common.log(f"[info] 浏览器搜索失败: {e}")

    # 方式2: 站内全文搜索接口（需登录态；校园网环境验证）
    try:
        html = _fetch("/f/info/xxfb_fg/xnzx/template/more", params={"searchText": query})
        if query in html or "detail?xxid" in html:
            res = _parse_notices(html, limit)
            if res:
                results.extend(res)
                common.log(f"[info] 全文搜索命中 {len(res)} 条")
                return results
    except Exception as e:
        common.log(f"[info] 全文搜索失败(可能需登录): {e}")

    # 方式3: 分类列表 + 标题过滤（公开可用）
    for cat, lmid in LMIDS.items():
        try:
            html = _fetch("/f/info/xxfb_fg/xnzx/template/more", params={"lmid": lmid})
            for m in re.finditer(r'<a[^>]*href="([^"]*detail\?xxid=[^"]*)"[^>]*>([^<]{4,100})</a>', html):
                href, title = m.group(1), m.group(2).strip()
                if query in title:
                    url = href if href.startswith("http") else BASE + href
                    results.append({"source": SOURCE_NAME, "title": title, "url": url, "snippet": f"[{cat}]"})
        except Exception:
            continue
        if len(results) >= limit:
            break

    common.log(f"[info] 分类匹配 {len(results)} 条")
    return results


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "奖学金"
    common.output_json(search(q))
