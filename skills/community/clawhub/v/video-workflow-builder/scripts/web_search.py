#!/usr/bin/env python3
"""通过 qianfan web search 网关做联网搜索。

本技能（及其生成的产物 skill）做联网研究时，统一走这个自建网关，而不是直接用
Claude Code / Codex 各自内置的 WebSearch。好处是搜索源可控、结果结构统一、
不同 agent 环境行为一致。

用法:
    python3 web_search.py "英伟达最新财报"
    python3 web_search.py "抖音职场号爆款打法" --top 15 --json
    python3 web_search.py "小红书美食探店" --source baidu_search_v2
    python3 web_search.py "英伟达 logo" --images          # 搜图片（封面/配图选材用）
    python3 web_search.py "赛博朋克 城市 夜景" --images --top 8 --json
    python3 web_search.py "https://www.163.com/dy/article/xxx.html" --full   # 抓正文全文

API key 读取顺序:
    1. 环境变量 QIANFAN_WEBSEARCH_API_KEY
    2. skill 目录下 .env 里的 QIANFAN_WEBSEARCH_API_KEY=xxx
    未配置则报错退出——不静默降级、不返回空结果。

网关地址（必填）:
    环境变量 QIANFAN_WEBSEARCH_API_BASE 或 .env 里的同名项，指向你自己的搜索网关。
    未配置则报错退出——不内置任何默认网关地址。

铁律：搜不到就报错，绝不返回缓存/编造的结果。联网研究的价值全在"实时"二字，
拿旧数据或空结果冒充搜索结果，比明说搜不到更有害。
"""
import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error

DEFAULT_SEARCH_SOURCE = "baidu_search_v2"
DEFAULT_TOP_K = 10
DEFAULT_TIMEOUT = 20


def _load_env_value(name):
    """按优先级读取配置：环境变量 > skill 目录 .env。找不到返回 None。"""
    val = os.environ.get(name)
    if val:
        return val.strip()
    env_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                if key.strip() == name:
                    return value.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return None


def _load_api_key():
    return _load_env_value("QIANFAN_WEBSEARCH_API_KEY")


def _load_api_base():
    base = _load_env_value("QIANFAN_WEBSEARCH_API_BASE")
    if not base:
        raise RuntimeError(
            "未配置 QIANFAN_WEBSEARCH_API_BASE。请把搜索网关地址写进环境变量，"
            "或 skill 目录下被 .gitignore 排除的 .env 文件："
            "QIANFAN_WEBSEARCH_API_BASE=https://你的搜索网关/v2/ai_search/web_search")
    return base.rstrip("/")


def _fetch_references(query, res_type, top, source, timeout, api_key, api_base):
    """调用网关一次，返回原始 references 列表。web/image 共用这段。

    失败抛异常，绝不吞掉、绝不返回空列表冒充"无结果"。
    """
    api_key = api_key or _load_api_key()
    if not api_key:
        raise RuntimeError(
            "未配置 QIANFAN_WEBSEARCH_API_KEY。请把网关密钥写进环境变量，"
            "或 skill 目录下被 .gitignore 排除的 .env 文件："
            "QIANFAN_WEBSEARCH_API_KEY=your-key-here")
    api_base = api_base or _load_api_base()

    body = json.dumps({
        "search_source": source,
        "resource_type_filter": [{"type": res_type, "top_k": top}],
        "messages": [{"content": query, "role": "user"}],
    }).encode("utf-8")
    req = urllib.request.Request(
        api_base, data=body, method="POST",
        headers={
            "Authorization": "Bearer %s" % api_key,
            "Content-Type": "application/json; charset=utf-8",
        })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    refs = payload.get("references")
    if not isinstance(refs, list):
        raise RuntimeError("搜索网关返回异常：无 references 数组（%r）"
                           % payload.get("request_id"))
    return refs


def search(query, top=DEFAULT_TOP_K, source=DEFAULT_SEARCH_SOURCE,
           timeout=DEFAULT_TIMEOUT, api_key=None, api_base=None):
    """网页搜索。每条结果字段：title / url / snippet / content / date / website。"""
    refs = _fetch_references(query, "web", top, source, timeout, api_key, api_base)
    results = []
    for r in refs:
        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("snippet", "") or r.get("web_anchor", ""),
            "content": r.get("content", ""),
            "date": r.get("date", ""),
            "website": r.get("website", ""),
        })
    return results


def search_images(query, top=DEFAULT_TOP_K, source=DEFAULT_SEARCH_SOURCE,
                  timeout=DEFAULT_TIMEOUT, api_key=None, api_base=None):
    """图片搜索（封面/配图选材用）。走同一网关，只是资源类型换成 image。

    每条结果字段：title / image_url / width / height / source_url / website。
    image_url 是图片本身的直链，source_url 是图片所在的网页。失败抛异常。
    """
    refs = _fetch_references(query, "image", top, source, timeout, api_key, api_base)
    results = []
    for r in refs:
        img = r.get("image") or {}
        results.append({
            "title": r.get("title", ""),
            "image_url": img.get("url", ""),
            "width": img.get("width", ""),
            "height": img.get("height", ""),
            "source_url": r.get("url", ""),
            "website": r.get("website", ""),
        })
    return results


_PAGE_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36")
# 抓正文前先剥掉这些整块噪声（脚本/样式/导航等），再抽 <p> 文本。
_STRIP_BLOCKS_RE = re.compile(
    r"<(script|style|noscript|template|svg)\b[^>]*>.*?</\1>", re.S | re.I)
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"[ \t\r\f\v]+")
_BLANKLINES_RE = re.compile(r"\n\s*\n\s*\n+")


def _html_to_text(html):
    """把 HTML 粗提纯成正文纯文本：剥噪声块 → 抽 <p> 段落 → 去标签 → 规整空白。

    不追求完美排版，只求把可读正文尽量完整地捞出来（网关 content 只给约两成，
    深读要靠这个补全）。抽不到 <p> 时退化为整页去标签，避免返回空。
    """
    # 只在 <body> 内提取，避免 <head> 里的 title/meta 泄漏进正文。
    body_m = re.search(r"<body\b[^>]*>(.*?)</body>", html, re.S | re.I)
    scope = body_m.group(1) if body_m else html
    cleaned = _STRIP_BLOCKS_RE.sub(" ", scope)
    paras = re.findall(r"<p\b[^>]*>(.*?)</p>", cleaned, re.S | re.I)
    if paras:
        chunks = []
        for p in paras:
            t = _WS_RE.sub(" ", _TAG_RE.sub("", p)).strip()
            if t:
                chunks.append(t)
        text = "\n\n".join(chunks)
    else:
        text = _WS_RE.sub(" ", _TAG_RE.sub("", cleaned))
    return _BLANKLINES_RE.sub("\n\n", text).strip()


def _extract_title(html):
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    return _WS_RE.sub(" ", _TAG_RE.sub("", m.group(1))).strip() if m else ""


def fetch_page(url, timeout=DEFAULT_TIMEOUT, max_chars=0):
    """本机直抓网页正文并提纯成纯文本。

    存在的理由：WebFetch 跑在 claude.ai 云端，对国内站（163/百家号/东财等）
    系统性报"无法确认域名安全"而失败；本机 urllib 抓同样的 URL 没问题。所以
    深读正文统一走这里，不依赖 agent 自带的 WebFetch。

    返回 {url, title, text, chars}。max_chars>0 时截断正文（并标注）。
    抓取失败抛异常，绝不返回空正文冒充"抓到了"。
    """
    req = urllib.request.Request(url, headers={"User-Agent": _PAGE_UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
    html = raw.decode(charset, "ignore")
    text = _html_to_text(html)
    if not text:
        raise RuntimeError("抓到网页但未能提取到正文文本：%s" % url)
    truncated = False
    if max_chars and len(text) > max_chars:
        text = text[:max_chars]
        truncated = True
    return {
        "url": url,
        "title": _extract_title(html),
        "text": text + ("\n\n…（已截断）" if truncated else ""),
        "chars": len(text),
    }


def _print_page(page):
    if page["title"]:
        print("【正文】%s" % page["title"])
    print("来源: %s（%d 字）\n" % (page["url"], page["chars"]))
    print(page["text"])


def _print_human(query, results):
    print("【搜索】%s（%d 条）" % (query, len(results)))
    for i, r in enumerate(results, 1):
        date_s = " · %s" % r["date"] if r["date"] else ""
        site_s = "[%s] " % r["website"] if r["website"] else ""
        print("\n%2d. %s%s%s" % (i, site_s, r["title"], date_s))
        print("    %s" % r["url"])
        snippet = (r["snippet"] or r["content"] or "").strip().replace("\n", " ")
        if snippet:
            print("    %s" % (snippet[:200] + ("…" if len(snippet) > 200 else "")))


def _print_images(query, results):
    print("【图片搜索】%s（%d 条）" % (query, len(results)))
    for i, r in enumerate(results, 1):
        site_s = "[%s] " % r["website"] if r["website"] else ""
        size_s = ""
        if r["width"] and r["height"]:
            size_s = " (%sx%s)" % (r["width"], r["height"])
        print("\n%2d. %s%s%s" % (i, site_s, r["title"], size_s))
        print("    图片直链: %s" % r["image_url"])
        if r["source_url"]:
            print("    来源页面: %s" % r["source_url"])


def main(argv):
    p = argparse.ArgumentParser(
        description="通过 qianfan web search 网关做联网搜索")
    p.add_argument("query", help="搜索关键词/问题；--full 模式下传网页 URL")
    p.add_argument("--top", type=int, default=DEFAULT_TOP_K, help="返回前 N 条")
    p.add_argument("--source", default=DEFAULT_SEARCH_SOURCE, help="搜索源")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    p.add_argument("--images", action="store_true",
                   help="搜图片而非网页（封面/配图选材用）")
    p.add_argument("--full", action="store_true",
                   help="把 query 当作 URL，本机直抓正文全文（绕开 WebFetch，国内站可靠）")
    p.add_argument("--max-chars", type=int, default=0,
                   help="--full 时截断正文到 N 字（0=不截断）")
    p.add_argument("--json", action="store_true", help="输出原始 JSON 而非人类可读格式")
    args = p.parse_args(argv)

    if args.full:
        try:
            page = fetch_page(args.query, timeout=args.timeout,
                              max_chars=args.max_chars)
        except (urllib.error.URLError, OSError) as e:
            print("抓取正文失败（网络/目标站不可达）：%s\n"
                  "本工具不返回缓存数据——换个源或稍后重试。" % e, file=sys.stderr)
            return 1
        except (ValueError, RuntimeError) as e:
            print("抓取正文失败：%s" % e, file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(page, ensure_ascii=False, indent=2))
        else:
            _print_page(page)
        return 0

    fn = search_images if args.images else search
    kind = "图片搜索" if args.images else "联网搜索"
    try:
        results = fn(args.query, top=args.top, source=args.source,
                     timeout=args.timeout)
    except (urllib.error.URLError, OSError) as e:
        print("%s失败（网络/网关不可达）：%s\n"
              "本工具不返回缓存数据——请修好网关或网络再重试，"
              "不要拿旧数据/空结果冒充搜索结果。" % (kind, e), file=sys.stderr)
        return 1
    except (ValueError, RuntimeError) as e:
        print("%s失败：%s" % (kind, e), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.images:
        _print_images(args.query, results)
    else:
        _print_human(args.query, results)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
