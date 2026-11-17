"""sources/its.py — its.tsinghua.edu.cn 信息化服务搜索（Lucene 站内搜索）

接口（已实测确认）:
  POST https://its.tsinghua.edu.cn/search.jsp?wbtreeid=1001
    参数: lucenenewssearchkey=<关键词> & _lucenesearchtype=1 & searchScope=0

its 是清华信息化用户服务平台（校园网络/邮箱/VPN/账号密码等服务说明）。
"""
import sys
import os
import re
import json
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "shared", "scripts"))
import common

SOURCE_NAME = "its"
BASE = "https://its.tsinghua.edu.cn"
SEARCH_URL = BASE + "/search.jsp?wbtreeid=1001"


def _cas_login(page, ctx, base_cas_dir):
    """its service 登录 —— 统一走 base-cas 会话复用（cookie 有效则免登录）。"""
    sys.path.insert(0, base_cas_dir)
    import login as _login
    return _login.ensure_login("its", page, ctx, home_url=BASE)


def _fetch(query):
    """POST 搜索请求。优先用运行中的 base-cas CDP 浏览器；
    无浏览器会话时启动临时浏览器（复用 profile 信任态），用完即退；
    若 its 需登录则用 CAS 凭据完成 service 登录。
    urllib 直连仅作最后兜底（本机受限可能返回空）。"""
    import urllib.parse

    base_cas_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "base-cas", "scripts")
    result = None
    pw = None
    owned = False
    try:
        sys.path.insert(0, base_cas_dir)
        import browser as _browser
        if _browser.is_running():
            pw, b, ctx, page = _browser.connect_cdp()
        else:
            # 即用即退：临时启动浏览器（复用 profile 指纹 + 落盘 cookie），用完关闭
            _browser.start_cdp(headed=False)
            owned = True
            pw, b, ctx, page = _browser.connect_cdp()
        page.on("dialog", lambda d: d.accept())
        # 统一走 base-cas 登录（导航 + cookie 复用 + 失效才填表）
        if not _cas_login(page, ctx, base_cas_dir):
            common.log("[its] CAS 登录失败，搜索返回空")
            return None
        # 在浏览器页面里 fetch its 搜索（带 cookie）
        result = page.evaluate("""async (q) => {
            const r = await fetch('/search.jsp?wbtreeid=1001', {
                method: 'POST',
                credentials: 'include',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: 'lucenenewssearchkey=' + encodeURIComponent(q) +
                      '&_lucenesearchtype=1&searchScope=0&showkeycode=' + encodeURIComponent(q)
            });
            return await r.text();
        }""", query)
        return result
    except Exception as e:
        common.log(f"[its] CDP 搜索失败: {e}")
        result = None
    finally:
        # 即用即退：自己启动的浏览器必须关闭（不碰运行中的外部浏览器）
        try:
            if owned:
                import browser as _browser
                _browser.stop_cdp()
            if pw is not None and not owned:
                pw.stop()
        except Exception:
            pass

    import urllib.request

    data = urllib.parse.urlencode({
        "lucenenewssearchkey": query,
        "_lucenesearchtype": "1",
        "searchScope": "0",
        "showkeycode": query,
    }).encode("utf-8")
    req = urllib.request.Request(SEARCH_URL, data=data, headers={
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    return urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="replace")


def _is_junk(href, title):
    """判断是否非内容链接（页脚导航/联系方式/资源文件等噪声）。"""
    if not href or href.startswith("javascript") or href in ("#", ""):
        return True
    if "TreeTempUrl" in href or "void(0)" in href or "index.jsp" in href:
        return True
    if href.startswith("tel:") or href.startswith("mailto:"):
        return True
    # 纯资源文件（PDF 说明书等非搜索目标）
    low = href.lower()
    if any(low.endswith(ext) for ext in (".pdf", ".zip", ".doc", ".docx", ".xls", ".xlsx", ".png", ".jpg")):
        return True
    # 纯数字/邮箱/链接文本（联系方式）
    if re.fullmatch(r"[\d\-—\s]+", title) or "@" in title:
        return True
    return False


def search(query, limit=5):
    """执行 its 搜索，返回 [{source, title, url, snippet}]。"""
    common.log(f"[its] 搜索: {query}")
    html = _fetch(query)
    if not html:
        common.log("[its] 无搜索结果页（登录失败或空响应）")
        return []

    # 解析结果：泛微 OA 搜索结果 = <a href="1wzcycejdh_content.jsp?...">标题</a> + 发表时间
    results = []
    seen = set()
    for m in re.finditer(r'<a[^>]*href="([^"]*content\.jsp[^"]*)"[^>]*>(.*?)</a>', html, re.S):
        href, inner = m.group(1), m.group(2)
        title = re.sub(r"<[^>]+>", "", inner).strip()
        if not title or title in seen or len(title) < 3 or _is_junk(href, title):
            continue
        seen.add(title)
        url = href if href.startswith("http") else BASE + "/" + href
        results.append({"source": SOURCE_NAME, "title": title, "url": url, "snippet": ""})
        if len(results) >= limit:
            break

    # 兜底：过滤掉导航类链接，取内容页
    if not results:
        for m in re.finditer(r'<a[^>]*href="([^"]*)"[^>]*>([^<]{3,80})</a>', html):
            href, title = m.group(1), m.group(2).strip()
            if _is_junk(href, title) or title in seen:
                continue
            seen.add(title)
            url = href if href.startswith("http") else BASE + "/" + href
            results.append({"source": SOURCE_NAME, "title": title, "url": url, "snippet": ""})
            if len(results) >= limit:
                break

    common.log(f"[its] 结果 {len(results)} 条")
    return results


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "VPN"
    common.output_json(search(q))
