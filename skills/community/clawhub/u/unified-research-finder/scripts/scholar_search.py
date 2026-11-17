#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scholar_search.py - Google Scholar 与大陆镜像站 统一检索。

数据源（auto 模式按优先级依次尝试）：
  1. kiphub     KipHub学术        https://www.kiphub.com/search          -> 自定义 HTML（paper-summary-wrapper 容器）
  2. lanfanshu  烂番薯学术搜索     https://scholar.lanfanshu.cn/          -> 经典 Scholar HTML（gs_rt/gs_a/gs_rs）
  3. scholar_pro 学术搜索Pro       https://www.googlescholar.pro/         -> 自定义 HTML（card-title/card-meta/card-text）
  4. dotaindex  灯塔学术搜索       https://www.dotaindex.com/scholar     -> JSON API（/api/scholar/search，最快最稳最省内存）
  5. hk         Google Scholar 香港镜像  https://scholar.google.com.hk/   -> 经典 HTML
  6. google     Google Scholar 官方站    https://scholar.google.com/       -> 经典 HTML

设计目标：低内存、速度快。默认走纯 HTTPS（仅用标准库 urllib），不依赖任何第三方包。
当目标站点对纯 HTTP 做了拦截 / 验证码时，可用 --browser 切换到 Playwright 无头浏览器兜底
（需自行 `pip install playwright && playwright install chromium`，仅在必要时启用，避免常驻重进程）。

输出：stdout 打印 JSON。
  {"ok": true, "source": "dotaindex", "query": "...", "count": N,
   "results": [ {title, url, authors, year, venue, snippet, citations, pdf_url} ],
   "note": "..."}
所有结果字段必须来自真实响应，绝不编造。
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html import unescape

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# 各源的检索基址 + 类型 + 参数名约定
# 字段说明：
#   label       中文名
#   type        数据格式：json / html / html_custom（非经典 Scholar 标记）
#   search_url  检索接口（不含查询字符串）
#   query_param 查询关键词的参数名（默认 "q"）
#   extra_params 固定追加的参数（如反爬需要的 hl/as_sdt/btnG）
#   referer     请求时携带的 Referer 头
SOURCES = {
    "kiphub": {
        "label": "KipHub学术",
        "type": "html_custom",
        "search_url": "https://www.kiphub.com/search?",
        "query_param": "wd",
        "extra_params": {},
        "referer": "https://www.kiphub.com/",
    },
    "lanfanshu": {
        "label": "烂番薯学术搜索",
        "type": "html",
        "search_url": "https://scholar.lanfanshu.cn/scholar?",
        "extra_params": {"hl": "zh-CN", "as_sdt": "0,5", "btnG": ""},
        "referer": "https://scholar.lanfanshu.cn/",
    },
    "scholar_pro": {
        "label": "学术搜索Pro",
        "type": "html_custom",
        "search_url": "https://www.googlescholar.pro/search_results.php?",
        "referer": "https://www.googlescholar.pro/",
    },
    "dotaindex": {
        "label": "灯塔学术搜索",
        "type": "json",
        "search_url": "https://www.dotaindex.com/api/scholar/search?",
        "referer": "https://www.dotaindex.com/scholar",
    },
    "hk": {
        "label": "Google Scholar 香港镜像",
        "type": "html",
        "search_url": "https://scholar.google.com.hk/scholar?",
        "referer": "https://scholar.google.com.hk/",
    },
    "google": {
        "label": "Google Scholar 官方站",
        "type": "html",
        "search_url": "https://scholar.google.com/scholar?",
        "referer": "https://scholar.google.com/",
    },
}
PRIORITY = ["kiphub", "lanfanshu", "scholar_pro", "dotaindex", "hk", "google"]

MONTH_ABBR = {"jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05",
              "jun": "06", "jul": "07", "aug": "08", "sep": "09", "oct": "10",
              "nov": "11", "dec": "12"}


# ---------------------------------------------------------------------------
# 通用工具
# ---------------------------------------------------------------------------
def clean_html(text):
    """去除 HTML 标签并反转义实体。"""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def http_get(url, headers, timeout=25, retries=2):
    """GET 请求，带退避重试。失败时抛 RuntimeError。"""
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.reason}"
            if e.code in (429, 403):
                # 403/429 多为拦截，直接放弃重试
                raise RuntimeError(f"被目标站点拦截（{last_err}）")
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = str(e)
        time.sleep(1.2 * (attempt + 1))
    raise RuntimeError(f"请求失败（{retries} 次）：{last_err}")


def build_params(query, start, sort, ylo, hl, cfg=None):
    # 使用源配置中的 query_param（默认 "q"），并合并 extra_params
    qp = (cfg or {}).get("query_param", "q")
    params = {qp: query, "hl": hl}
    if cfg and cfg.get("extra_params"):
        params.update(cfg["extra_params"])
    if start:
        params["start"] = start
    if ylo:
        params["as_ylo"] = ylo
    if sort == "date":
        params["scisbd"] = "1"
    return params


# ---------------------------------------------------------------------------
# 经典 Scholar HTML 解析（烂番薯 / 香港 / 官方 通用）
# ---------------------------------------------------------------------------
def parse_scholar_html(html):
    """解析经典 Scholar 结果页，返回标准化结果列表。"""
    rt_idxs = [m.start() for m in re.finditer(r'<h3 class=["\']gs_rt', html)]
    gs_r_idxs = [m.start() for m in re.finditer(r'<div class=["\']gs_r', html)]
    results = []
    for rt in rt_idxs:
        start = max([s for s in gs_r_idxs if s < rt], default=rt)
        end = min([s for s in gs_r_idxs if s > rt], default=rt + 6000)
        results.append(_parse_html_block(html[start:end]))
    return [r for r in results if r]


def _parse_html_block(block):
    # 标题 + 链接（class 顺序无关，使用模糊匹配）
    m = re.search(r'<h3 class="[^"]*gs_rt[^"]*"[^>]*>\s*<a[^>]*?href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
                  block, re.S)
    if m:
        url, title = m.group(1), clean_html(m.group(2))
    else:
        m2 = re.search(r'<h3 class="[^"]*gs_rt[^"]*"[^>]*>(.*?)</h3>', block, re.S)
        if not m2:
            return None
        title = clean_html(m2.group(1))
        url = ""

    # 作者 / 来源 / 年份（gs_a）
    authors, year, venue = "", "", ""
    ma = re.search(r'<div class="[^"]*gs_a[^"]*"[^>]*>(.*?)</div>', block, re.S)
    if ma:
        authors, year, venue = _parse_gs_a(clean_html(ma.group(1)))

    # 摘要片段（gs_rs）；标记名/顺序不确定时，取 gs_a 与 gs_fl 之间的文本兜底
    ms = re.search(r'<div class="[^"]*gs_rs[^"]*"[^>]*>(.*?)</div>', block, re.S)
    if ms:
        snippet = clean_html(ms.group(1))
    else:
        ia = block.find('<div class="gs_a')
        ifl = block.find('<div class="gs_fl')
        if ia != -1 and ifl != -1 and ifl > ia:
            sub = block[ia:ifl]
            ja = sub.find("</div>")
            if ja != -1:
                sub = sub[ja + 6:]
            snippet = clean_html(sub)
        else:
            snippet = ""

    # 被引次数（兼容 中文/英文 多种写法）
    mc = re.search(r'(?:被引用次数|引用次数|被引|Cited by|被引用)\D{0,40}(\d[\d,]*)',
                   block, re.I)
    if not mc:
        mc = re.search(r'cites=[^"\'>\s]+["\'][^>]*>\D*(\d[\d,]*)', block)
    citations = int(re.sub(r"[^\d]", "", mc.group(1))) if mc else 0

    # PDF 全文链接：[PDF] 之后的 href，或 gs_ggs 区域内的 href
    mp = re.search(r'\[PDF\][\s\S]*?href=["\']([^"\']+)', block)
    if not mp:
        mp = re.search(r'class="[^"]*gs_ggs[^"]*"[\s\S]*?href=["\']([^"\']+)', block)
    pdf_url = mp.group(1) if mp else ""

    return {
        "title": title,
        "url": url,
        "authors": authors,
        "year": year,
        "venue": venue,
        "snippet": snippet,
        "citations": citations,
        "pdf_url": pdf_url,
    }


def _parse_gs_a(text):
    authors, year, venue = text, "", ""
    my = re.search(r'\b(19|20)\d{2}\b', text)
    if my:
        year = my.group(0)
        before = text[:my.start()].strip().rstrip(",").strip()
        if " - " in before:
            venue = before.split(" - ", 1)[1].strip()
    if " - " in text:
        authors = text.split(" - ", 1)[0].strip()
    return authors, year, venue


def html_is_blocked(html):
    low = html.lower()
    markers = ["unusual traffic", "我们的系统检测到", "enter the characters you see",
               "please show you", "captcha", "why did this happen", "rate limit"]
    return any(m in low for m in markers)


# ---------------------------------------------------------------------------
# 灯塔 JSON API 解析
# ---------------------------------------------------------------------------
def parse_dotaindex_json(data):
    results = []
    for r in data.get("results", []):
        th = r.get("titleHtml", "")
        m = re.search(r'href=["\']([^"\']+)["\']', th)
        url = m.group(1) if m else r.get("url", "")
        title = clean_html(th) or r.get("url", "")
        cit_s = str(r.get("citationCount", "0") or "0")
        citations = int(re.sub(r"\D", "", cit_s) or 0)
        pdf = r.get("openAccessUrl", "") or ""
        if not pdf and isinstance(r.get("accessLinks"), list) and r["accessLinks"]:
            pdf = r["accessLinks"][0].get("url", "")
        results.append({
            "title": title,
            "url": url,
            "authors": r.get("author", ""),
            "year": str(r.get("year", "")),
            "venue": r.get("journal", "") or r.get("publisher", ""),
            "snippet": clean_html(r.get("abstractHtml", "")),
            "citations": citations,
            "pdf_url": pdf,
        })
    return results


# ---------------------------------------------------------------------------
# KipHub 自定义 HTML 解析（paper-summary-wrapper 容器）
# ---------------------------------------------------------------------------
def parse_kiphub_html(html_text):
    """解析 kiphub.com 的搜索结果页。"""
    results = []
    blocks = re.findall(
        r'<div class="paper-summary-wrapper[^>]*>(.*?)'
        r'(?=<div class="paper-summary-wrapper|$)', html_text, re.S)
    for blk in blocks:
        # 标题 + 链接（pp-title div 内有 img 等元素，匹配第一个 <a>）
        tm = re.search(r'class="pp-title[^"]*"[^>]*>(.*?)</div>', blk, re.S)
        if tm:
            lm = re.search(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', tm.group(1), re.S)
            title = clean_html(lm.group(2)) if lm else ""
            url = lm.group(1) if lm else ""
        else:
            title, url = "", ""

        # 作者 / 期刊 / 年份（.pp-info .author 内的文本）
        mm = re.search(r'class="author"[^>]*>(.*?)</div>', blk, re.S)
        meta_text = clean_html(mm.group(1)) if mm else ""
        authors, year, venue = _parse_gs_a(meta_text)

        results.append({
            "title": title,
            "url": url,
            "authors": authors,
            "year": year,
            "venue": venue,
            "snippet": "",
            "citations": 0,
            "pdf_url": "",
        })
    return [r for r in results if r.get("title")]


# ---------------------------------------------------------------------------
# 学术搜索Pro 自定义 HTML 解析（card 容器）
# ---------------------------------------------------------------------------
def parse_scholarpro_html(html_text):
    """解析 googlescholar.pro 的搜索结果页（card-title/card-meta/card-text）。"""
    results = []
    cards = re.findall(
        r'<div class="card"[^>]*>.*?<h3 class="card-title">(.*?)'
        r'(?=<div class="card"[^>]*>.*?<h3 class="card-title"|$)', html_text, re.S)
    for card in cards:
        # 标题 + 链接
        tm = re.search(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', card, re.S)
        title = clean_html(tm.group(2)) if tm else ""
        url = tm.group(1) if tm else ""

        # 元信息（card-meta）
        mm = re.search(r'class="card-meta"[^>]*>(.*?)</div>', card, re.S)
        meta_text = clean_html(mm.group(1)) if mm else ""
        authors, year, venue = _parse_gs_a(meta_text)

        # 摘要（card-text）
        sm = re.search(r'class="card-text"[^>]*>(.*?)</div>', card, re.S)
        snippet = clean_html(sm.group(1)) if sm else ""

        # 被引次数（从 card-actions / card-side-links 区域找 "被引用次数" "Cited by"）
        cm = re.search(r'(?:被引用次数|Cited by)\D*(\d[\d,]*)', card, re.I)
        citations = int(re.sub(r"[^\d]", "", cm.group(1))) if cm else 0

        # PDF（card-side-links 区域的 [PDF] 链接）
        pm = re.search(r'\[PDF\]\s*<a[^>]*href="([^"]+)"', card)
        if not pm:
            pm = re.search(r'class="card-side-links[^"]*"[^>]*>\s*<a[^>]*href="([^"]+)"', card)
        pdf_url = pm.group(1) if pm else ""

        results.append({
            "title": title,
            "url": url,
            "authors": authors,
            "year": year,
            "venue": venue,
            "snippet": snippet,
            "citations": citations,
            "pdf_url": pdf_url,
        })
    return [r for r in results if r.get("title")]


# ---------------------------------------------------------------------------
# 单源检索（含分页）
# ---------------------------------------------------------------------------
def search_source(key, query, num, sort, ylo, hl, use_browser):
    cfg = SOURCES[key]
    out_results = []
    start = 0
    pages = 0
    blocked = False
    note = ""
    while len(out_results) < num and pages < 5:
        params = build_params(query, start, sort, ylo, hl, cfg)
        url = cfg["search_url"] + urllib.parse.urlencode(params)

        if cfg["type"] == "json":
            # 灯塔是 JSON，无需浏览器；偶发限流会返回空 results，做一次短暂退避重试
            page = []
            total = None
            for attempt in range(2):
                try:
                    body = http_get(url, {
                        "User-Agent": UA,
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Referer": cfg["referer"],
                    })
                    data = json.loads(body)
                except RuntimeError as e:
                    blocked = True
                    note = f"{cfg['label']} 访问失败：{e}"
                    break
                if isinstance(data, dict) and "results" in data:
                    page = parse_dotaindex_json(data)
                    total = data.get("total")
                    if page or attempt == 1:
                        break
                    time.sleep(1.5)  # 疑似限流，退避后重试一次
                    continue
                else:
                    blocked = True
                    note = f"{cfg['label']} 返回异常：{str(data)[:120]}"
                    break
            if blocked:
                break
            out_results.extend(page)
            if not page:
                break
        else:
            # HTML / HTML 自定义源
            content = ""
            if use_browser:
                content, berr, bnote = fetch_via_browser(url)
                if berr:
                    blocked = True
                    note = bnote
                    break
            else:
                try:
                    content = http_get(url, {
                        "User-Agent": UA,
                        "Accept": "text/html,application/xhtml+xml,*/*",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Referer": cfg["referer"],
                        "Connection": "keep-alive",
                    })
                except RuntimeError as e:
                    blocked = True
                    note = f"{cfg['label']} 访问失败：{e}"
                    break
            # 按源类型选择解析器
            if cfg["type"] == "html_custom":
                if key == "kiphub":
                    page = parse_kiphub_html(content)
                elif key == "scholar_pro":
                    page = parse_scholarpro_html(content)
                else:
                    page = parse_scholar_html(content)
            else:
                page = parse_scholar_html(content)
                if not page and html_is_blocked(content):
                    blocked = True
                    note = f"{cfg['label']} 触发验证码/流量限制，需切换 --browser 模式或换源"
                    break
            if not page:
                break
            out_results.extend(page)

        start += 10
        pages += 1
        time.sleep(0.3)  # 轻量礼貌间隔

    out_results = out_results[:num]
    return out_results, blocked, note


def fetch_via_browser(url):
    """Playwright 兜底：仅 HTML 源、且用户显式开启 --browser 时调用。"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None, True, ("Playwright 未安装。请先执行：\n"
                            "  pip install playwright && playwright install chromium\n"
                            "然后重新运行并加 --browser 参数。")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            page.wait_for_timeout(2500)
            content = page.content()
            browser.close()
        return content, False, ""
    except Exception as e:  # noqa: BLE001
        return None, True, f"Playwright 渲染失败：{e}"


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Google Scholar + 镜像站统一检索")
    ap.add_argument("--query", required=True, help="检索词")
    ap.add_argument("--source", default="auto",
                    choices=["auto"] + list(SOURCES.keys()),
                    help="指定数据源；默认 auto 按优先级回退")
    ap.add_argument("--num", type=int, default=10, help="返回条数（默认 10）")
    ap.add_argument("--start", type=int, default=0, help="起始偏移")
    ap.add_argument("--sort", default="relevance", choices=["relevance", "date"],
                    help="排序：relevance 相关度 / date 日期")
    ap.add_argument("--ylo", help="起始年份（如 2020），按年份下限过滤")
    ap.add_argument("--lang", default="zh-CN", help="界面语言，默认 zh-CN")
    ap.add_argument("--browser", action="store_true",
                    help="被拦截时改用 Playwright 无头浏览器兜底（需已安装）")
    args = ap.parse_args()

    num = max(1, min(args.num, 50))
    order = [args.source] if args.source != "auto" else PRIORITY

    out = {"ok": True, "source": "", "query": args.query,
           "count": 0, "results": [], "note": ""}
    tried = []
    for key in order:
        results, blocked, note = search_source(
            key, args.query, num, args.sort, args.ylo, args.lang, args.browser)
        tried.append(SOURCES[key]["label"])
        if results:
            out["ok"] = True
            out["source"] = key
            out["results"] = results
            out["count"] = len(results)
            if key != PRIORITY[0] and args.source == "auto":
                out["note"] = (f"已在 {SOURCES[key]['label']} 取得结果"
                               f"（前序源：{', '.join(tried[:-1])} 未返回可用结果）。")
            else:
                out["note"] = note or f"数据来源：{SOURCES[key]['label']}。"
            break
        if blocked:
            out["note"] = note
            # 被拦截则继续尝试下一源
            continue
        # 未拦截但 0 结果：也尝试下一源，碰碰运气
        continue
    else:
        # 所有源都未产出结果（可能全部被拦截或全部为空）
        out["ok"] = bool(out["results"])
        fallback_hint = (
            "所有 Scholar 数据源均不可达。"
            "当前中国 Scholar 镜像（灯塔/烂番薯/panda985/gfsoso 等）已全面启用反爬/验证码，"
            "纯 HTTP 请求难以穿透。"
        )
        if not args.browser:
            fallback_hint += (
                " 如安装了 Playwright，可用 --browser 模式通过无头浏览器绕过验证码："
                " pip install playwright && playwright install chromium，"
                "然后重新运行并加 --browser。"
            )
        else:
            fallback_hint += " Playwright 模式也已尝试，仍无法获取结果。"
        out["note"] = out.get("note") or fallback_hint

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
