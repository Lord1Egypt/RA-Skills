#!/usr/bin/env python3
"""知乎数据抓取工具 - 走 API 路径,不渲染浏览器

跟 keepalive.py 配合使用: 本脚本读 cookies.txt,负责抓数据.
keepalive.py 负责管理 ab daemon + cookie 续期.

为什么是 API 而不是 ab?
- ab open 一个问题页 -> ~1-3 MB HTML (含 CSS/侧栏/推荐/广告)
- ab eval innerText  -> ~50-200 KB 纯文本,但含导航/版权/无关评论
- API answers       -> ~30-50 KB JSON,纯结构化答案

ab 仅在需要看渲染效果 / 过验证码 / 操作 UI 时才用.

用法:
  zhihu-fetch.py search <关键词> [--limit 25] [--type question|column|people|topic|zvideo]
  zhihu-fetch.py answers <qid> [--top 10]
  zhihu-fetch.py batch-search <关键词> [<关键词> ...] [--limit 25]
  zhihu-fetch.py extract <answers.json> [--top 3] [--md-out PATH]
  zhihu-fetch.py qa-batch <qid>:<title> [<qid>:<title> ...] [--top 3] [--md-out PATH]
  zhihu-fetch.py article <url_or_id>              # 抓专栏文章正文 (SPA HTML 解析)
  zhihu-fetch.py hotlist [--limit 30]             # 看热榜
"""
import argparse
import html
import json
import re
import subprocess
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# ===== 路径 (从 paths.py 读,支持自包含部署) =====
from paths import (
    DATA_DIR, COOKIE_FILE, ANSWERS_DIR, ARTICLES_DIR, COLUMNS_DIR, COMMENTS_DIR, report
)

# ===== 常量 =====
HOME = Path.home()
SEARCH_API = "https://www.zhihu.com/api/v4/search_v3"
ANSWER_API = "https://www.zhihu.com/api/v4/questions/{qid}/answers"
HOTLIST_API = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
COLUMN_API = "https://www.zhihu.com/api/v4/columns/{c_id}/articles"
COMMENTS_API = "https://www.zhihu.com/api/v4/answers/{aid}/comments"  # 绕开 comment_v5 的反爬
ZHUANLAN_URL = "https://zhuanlan.zhihu.com/p/{aid}"
UA = "Mozilla/5.0"

# ===== 底层 =====
def load_cookie() -> str:
    if not COOKIE_FILE.exists():
        sys.exit(f"✗ {COOKIE_FILE} 不存在,先用 keepalive.py setup 注入 cookie\n\n当前路径配置:\n{report()}")
    return COOKIE_FILE.read_text().strip()

def curl_json(url: str, cookie: str) -> dict:
    r = subprocess.run(
        ["curl", "-sL", "-A", UA, "-H", f"Cookie: {cookie}", url],
        capture_output=True, text=True, timeout=30
    )
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError as e:
        sys.exit(f"✗ 非 JSON 响应 (可能 cookie 失效): {e}\n  body 前 200 字: {r.stdout[:200]}")

def curl_text(url: str, cookie: str, timeout: int = 30) -> str:
    r = subprocess.run(
        ["curl", "-sL", "-A", UA, "-H", f"Cookie: {cookie}", url],
        capture_output=True, text=True, timeout=timeout
    )
    return r.stdout

# ===== HTML 清洗 =====
def strip_html(s: str) -> str:
    """知乎答案 HTML -> markdown-ish 纯文本"""
    if not s:
        return ""
    s = re.sub(r'</p>\s*<p[^>]*>', '\n\n', s)
    s = re.sub(r'<li[^>]*>', '\n- ', s)
    s = re.sub(r'<h([1-6])[^>]*>', lambda m: '\n\n' + '#' * int(m.group(1)) + ' ', s)
    s = re.sub(r'</h[1-6]>', '\n', s)
    s = re.sub(r'<(strong|b)[^>]*>', '**', s)
    s = re.sub(r'</(strong|b)>', '**', s)
    s = re.sub(r'<(em|i)[^>]*>', '*', s)
    s = re.sub(r'</(em|i)>', '*', s)
    s = re.sub(r'<code[^>]*>', '`', s)
    s = re.sub(r'</code>', '`', s)
    s = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>([^<]*)</a>', r'[\2](\1)', s)
    s = re.sub(r'<img[^>]*>', '[图]', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

def make_summary(text: str, head: int = 800, tail: int = 400) -> str:
    """截取核心:前 head 字符 + 后 tail 字符 (有些答案末尾有结论)"""
    if len(text) <= head + tail:
        return text
    return text[:head] + "\n\n...(中略)...\n\n" + text[-tail:]

# ===== 命令 =====
def cmd_search(args):
    """单个关键词搜索"""
    cookie = load_cookie()
    q = urllib.parse.quote(args.keyword)
    t = args.type
    limit = args.limit
    d = curl_json(f"{SEARCH_API}?t={t}&q={q}&limit={limit}&offset=0", cookie)
    data = d.get("data", [])
    print(f"# 搜索: {args.keyword}  (type={t}, 命中 {len(data)} 条)")
    for it in data:
        obj = it.get("object", {})
        otype = obj.get("type", "?")
        # 去除 <em> 高亮标签
        def clean(s): return (s or "").replace("<em>", "").replace("</em>", "")

        if otype == "question":
            qid = obj.get("id")
            print(f"  [Q {obj.get('answer_count',0)}答 {obj.get('follower_count',0)}关] {clean(obj.get('title'))[:60]}")
            print(f"    https://www.zhihu.com/question/{qid}")
        elif otype == "column":
            cid = obj.get("id")
            print(f"  [专栏 {obj.get('articles_count','?')}篇] {clean(obj.get('title'))[:50]}")
            print(f"    https://www.zhihu.com/column/{cid}  (描述: {clean(obj.get('description',''))[:50]})")
        elif otype == "people":
            uid = obj.get("id")
            utok = obj.get("url_token")
            print(f"  [人 {obj.get('follower_count',0)}粉 {obj.get('answer_count',0)}答] {clean(obj.get('name'))} (@{utok})")
            print(f"    https://www.zhihu.com/people/{utok or uid}")
        elif otype == "topic":
            tid = obj.get("id")
            print(f"  [话题 {obj.get('follower_count','?')}关] {clean(obj.get('name'))}")
            print(f"    https://www.zhihu.com/topic/{tid}")
        elif otype == "zvideo":
            zid = obj.get("id")
            print(f"  [视频 {obj.get('voteup_count',0)}赞 {obj.get('comment_count',0)}评] {clean(obj.get('title'))[:55]}")
            print(f"    https://www.zhihu.com/zvideo/{zid}")
        else:
            print(f"  [{otype}] {clean(obj.get('title') or obj.get('name') or obj.get('description',''))[:60]}")

def cmd_batch_search(args):
    """多关键词并发搜索,合并去重"""
    cookie = load_cookie()
    keywords = args.keyword
    limit = args.limit
    print(f"# 批量搜索 {len(keywords)} 个关键词,每关键词 {limit} 条 ...")

    def fetch(kw):
        q = urllib.parse.quote(kw)
        d = curl_json(f"{SEARCH_API}?t=question&q={q}&limit={limit}&offset=0", cookie)
        return kw, d.get("data", [])

    raw = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for kw, data in ex.map(fetch, keywords):
            raw[kw] = data
            print(f"  [{kw}] {len(data)} 条")

    # 去重 + 汇总
    seen = {}
    for kw, items in raw.items():
        for it in items:
            obj = it.get("object", {})
            if obj.get("type") != "question":
                continue
            qid = str(obj.get("id", ""))
            if not qid:
                continue
            if qid not in seen:
                seen[qid] = {
                    "id": qid,
                    "url": f"https://www.zhihu.com/question/{qid}",
                    "title": obj.get("title", "").replace("<em>", "").replace("</em>", ""),
                    "answer_count": obj.get("answer_count", 0),
                    "follower_count": obj.get("follower_count", 0),
                    "visit_count": obj.get("visits_count", 0),
                    "keywords_hit": []
                }
            if kw not in seen[qid]["keywords_hit"]:
                seen[qid]["keywords_hit"].append(kw)

    ranked = sorted(
        seen.values(),
        key=lambda x: (len(x["keywords_hit"]), x["visit_count"], x["follower_count"]),
        reverse=True
    )

    # 输出文件
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "raw-search.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2))
    (DATA_DIR / "ranked.json").write_text(json.dumps(ranked, ensure_ascii=False, indent=2))
    print(f"\n去重后 {len(ranked)} 个问题 -> raw-search.json + ranked.json")
    print(f"\nTOP 10:")
    for r in ranked[:10]:
        hits = ",".join(r["keywords_hit"][:4])
        if len(r["keywords_hit"]) > 4:
            hits += f" +{len(r['keywords_hit'])-4}"
        print(f"  [{len(r['keywords_hit']):>2}kw|{r['visit_count']:>8}v|{r['answer_count']:>4}a] {r['title'][:60]}")

def cmd_answers(args):
    """抓单个问题的高赞答案 -> JSON"""
    cookie = load_cookie()
    qid = args.qid
    limit = args.limit
    url = ANSWER_API.format(qid=qid) + f"?include=data%5B*%5D.content%2Cvoteup_count%2Ccomment_count%2Cauthor.name%2Cauthor.headline&limit={limit}&offset=0&order=default"
    d = curl_json(url, cookie)

    # 排序 + 输出 JSON
    answers = sorted(d.get("data", []), key=lambda x: x.get("voteup_count", 0), reverse=True)
    out_path = ANSWERS_DIR / f"{qid}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(d, ensure_ascii=False, indent=2))

    totals = d.get("paging", {}).get("totals", "?")
    print(f"# 问题 {qid} 共 {totals} 答, 取 top {len(answers)} ({out_path})")
    for a in answers[:5]:
        author = a.get("author", {}).get("name", "?")
        votes = a.get("voteup_count", 0)
        print(f"  {votes:>5} 赞 | @{author} | len={len(a.get('content',''))}")

def cmd_extract(args):
    """answers JSON -> markdown 摘要"""
    raw = json.load(open(args.file))
    answers = raw.get("data", [])
    answers.sort(key=lambda x: x.get("voteup_count", 0), reverse=True)
    top = args.top
    head_n = 300 if args.compact else 800
    tail_n = 100 if args.compact else 400

    md = []
    for i, a in enumerate(answers[:top], 1):
        author = a.get("author", {}).get("name", "?")
        votes = a.get("voteup_count", 0)
        comments = a.get("comment_count", 0)
        content = strip_html(a.get("content", ""))
        md.append(f"\n## 第 {i} 高赞 ({votes} 赞 / {comments} 评论) — @{author}\n")
        md.append(make_summary(content, head=head_n, tail=tail_n))
        md.append("")

    text = "\n".join(md)
    if args.md_out:
        Path(args.md_out).write_text(text)
        print(f"✓ 写入 {args.md_out} ({len(text)//1024} KB, top {top} 答{', compact' if args.compact else ''})")
    else:
        print(text)

def cmd_article(args):
    """抓专栏文章正文 - 走 SPA HTML 解析 (知乎 article API 现在拒,10003 错误)"""
    cookie = load_cookie()
    # 接受 https://zhuanlan.zhihu.com/p/xxx 或纯数字 id
    spec = args.spec
    m = re.search(r'/p/(\d+)', spec)
    aid = m.group(1) if m else spec.strip()
    if not aid.isdigit():
        sys.exit(f"✗ 无法识别 article id: {spec}")

    url = ZHUANLAN_URL.format(aid=aid)
    print(f"# 抓专栏: {url}")
    html_text = curl_text(url, cookie, timeout=45)
    if len(html_text) < 5000:
        sys.exit(f"✗ HTML 太小 ({len(html_text)} 字节),可能 cookie 失效或文章不存在")

    # 提取 <script id="js-initialData"> 里的 JSON
    m = re.search(r'<script[^>]*id="js-initialData"[^>]*>(.+?)</script>', html_text, re.DOTALL)
    if not m:
        sys.exit("✗ 未找到 js-initialData script tag, 可能页面结构已变")

    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        sys.exit(f"✗ js-initialData JSON 解析失败: {e}")

    # 递归找 article (带 title + 长 content 的对象)
    def find_article(obj, depth=0):
        if depth > 8: return None
        if isinstance(obj, dict):
            content = obj.get('content')
            if isinstance(content, str) and len(content) > 200 and 'title' in obj:
                return obj
            for v in obj.values():
                r = find_article(v, depth+1)
                if r: return r
        elif isinstance(obj, list):
            for x in obj:
                r = find_article(x, depth+1)
                if r: return r
        return None

    art = find_article(data)
    if not art:
        sys.exit("✗ 在 js-initialData 里找不到 article 对象")

    # 输出 JSON
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    (ARTICLES_DIR / f"{aid}.json").write_text(json.dumps(art, ensure_ascii=False, indent=2))

    # 输出 markdown 摘要
    title = art.get('title', '(无标题)')
    author = art.get('author', {}).get('name', '?') if isinstance(art.get('author'), dict) else '?'
    voteup = art.get('voteupCount', 0)
    excerpt_raw = art.get('excerptTitle') or art.get('excerpt', '')
    excerpt = strip_html(excerpt_raw)[:300]
    content_md = strip_html(art.get('content', ''))

    md = [
        f"# {title}\n",
        f"作者: @{author} | 点赞: {voteup} | 文章ID: {aid}",
        f"原文: https://zhuanlan.zhihu.com/p/{aid}",
        f"\n## 摘要\n{excerpt}\n" if excerpt else "",
        f"\n## 正文 ({len(content_md)} 字)\n",
        make_summary(content_md, head=1500, tail=600),
    ]
    md_text = "\n".join(x for x in md if x)
    print(md_text)
    (ARTICLES_DIR / f"{aid}.md").write_text(md_text)
    print(f"\n✓ 写入 {ARTICLES_DIR}/{aid}.json + {aid}.md")

def cmd_hotlist(args):
    """知乎热榜"""
    cookie = load_cookie()
    url = f"{HOTLIST_API}?limit={args.limit}&desktop=true"
    d = curl_json(url, cookie)
    items = d.get("data", [])
    rows = []
    for i, x in enumerate(items, 1):
        t = x.get("target", {})
        qid = t.get("id")
        title = t.get("title", "")
        url = f"https://www.zhihu.com/question/{qid}"
        heat = x.get("detail_text", "")
        excerpt = t.get("excerpt", "")[:100]
        ans = t.get("answer_count", 0)
        rows.append({
            "rank": i, "qid": qid, "title": title, "url": url,
            "heat": heat, "answer_count": ans, "excerpt": excerpt,
            "type": t.get("type", "question")
        })

    # JSON 落盘总是执行 (方便后续 grep). 写到 data/ 不污染项目 CWD.
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "hotlist.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2))

    # 紧凑模式: 只打表格到 stdout / md-out
    if args.compact:
        lines = [f"# 知乎热榜 Top {len(rows)}\n"]
        lines.append("| 排名 | 热度 | 标题 | 回答 |")
        lines.append("|---|---|---|---|")
        for r in rows[:args.limit]:
            lines.append(f"| {r['rank']} | {r['heat']} | [{r['title'][:60]}]({r['url']}) | {r['answer_count']} |")
        text = "\n".join(lines)
        if args.md_out:
            Path(args.md_out).write_text(text)
            print(f"✓ {args.md_out} ({len(rows)} 条, compact)", file=sys.stderr)
        else:
            print(text)
            print(f"\n(完整摘要见 hotlist.json)", file=sys.stderr)
        return

    # 默认模式: 表格 + 详情列表
    print(f"# 知乎热榜 (共 {len(items)} 条)\n")
    print("| 排名 | 热度 | 标题 | 回答 |")
    print("|---|---|---|---|")
    for r in rows[:args.limit]:
        print(f"| {r['rank']} | {r['heat']} | [{r['title'][:55]}]({r['url']}) | {r['answer_count']} |")

    print(f"\n## 详情\n")
    for r in rows:
        if r["excerpt"]:
            print(f"**{r['rank']}. {r['title']}** ({r['heat']})")
            print(f"   {r['excerpt']}...")
            print(f"   {r['url']}\n")

    if args.md_out:
        # 把 stdout 重定向到文件很难，这里写一份等价的精简版
        md_text = f"# 知乎热榜 (共 {len(items)} 条)\n\n"
        md_text += "| 排名 | 热度 | 标题 | 回答 |\n|---|---|---|---|\n"
        for r in rows[:args.limit]:
            md_text += f"| {r['rank']} | {r['heat']} | [{r['title'][:60]}]({r['url']}) | {r['answer_count']} |\n"
        Path(args.md_out).write_text(md_text)
        print(f"✓ {args.md_out}", file=sys.stderr)
    else:
        print(f"\n✓ 落盘 {DATA_DIR}/hotlist.json", file=sys.stderr)

def cmd_quick(args):
    """一键: 多关键词搜索 + 去重 + 抓 top 答案 -> 单个紧凑 markdown

    这是为 LLM agent 设计的快捷命令, 一次调用拿到主题摘要.
    默认: 多关键词搜索 -> 去重排序 -> 抓 top 问题 -> 输出 markdown.
    """
    cookie = load_cookie()
    topic = args.topic
    keywords = args.keywords if args.keywords else [topic, f"{topic} 资讯", f"{topic} 新闻"]

    limit = args.limit
    top_q = args.top_q
    per_q = args.per_q
    compact = args.compact

    head_n = 300 if compact else 800
    tail_n = 100 if compact else 400

    print(f"[1/3] 批量搜索 {len(keywords)} 关键词, 每词 {limit} 条 ...", file=sys.stderr)

    # 1. 批量搜索
    raw = {}
    def fetch_kw(kw):
        q = urllib.parse.quote(kw)
        d = curl_json(f"{SEARCH_API}?t=question&q={q}&limit={limit}&offset=0", cookie)
        return kw, d.get("data", [])

    with ThreadPoolExecutor(max_workers=8) as ex:
        for kw, data in ex.map(fetch_kw, keywords):
            raw[kw] = data
            print(f"    [{kw}] {len(data)} 条", file=sys.stderr)

    # 2. 去重排序
    seen = {}
    for kw, items in raw.items():
        for it in items:
            obj = it.get("object", {})
            if obj.get("type") != "question":
                continue
            qid = str(obj.get("id", ""))
            if not qid:
                continue
            if qid not in seen:
                seen[qid] = {
                    "id": qid,
                    "title": obj.get("title", "").replace("<em>", "").replace("</em>", ""),
                    "answer_count": obj.get("answer_count", 0),
                    "visit_count": obj.get("visits_count", 0),
                    "follower_count": obj.get("follower_count", 0),
                    "keywords_hit": [],
                }
            if kw not in seen[qid]["keywords_hit"]:
                seen[qid]["keywords_hit"].append(kw)

    ranked = sorted(
        seen.values(),
        key=lambda x: (len(x["keywords_hit"]), x["visit_count"]),
        reverse=True,
    )
    top_questions = ranked[:top_q]
    print(f"[2/3] {len(ranked)} 个候选 -> 取 top {top_q}", file=sys.stderr)

    # 3. 抓 top 答案
    (ANSWERS_DIR).mkdir(parents=True, exist_ok=True)

    def fetch_q(qinfo):
        qid = qinfo["id"]
        url = ANSWER_API.format(qid=qid) + f"?include=data%5B*%5D.content%2Cvoteup_count%2Ccomment_count%2Cauthor.name&limit=20&offset=0&order=default"
        d = curl_json(url, cookie)
        return qinfo, d

    results = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for qinfo, d in ex.map(fetch_q, top_questions):
            results.append((qinfo, d))
            totals = d.get("paging", {}).get("totals", "?")
            print(f"    {qinfo['id']} -> {totals} 答", file=sys.stderr)

    # 4. 合并 markdown
    print(f"[3/3] 生成 markdown ...", file=sys.stderr)

    log = []
    log.append(f"# Quick 摘要: {topic}\n")
    log.append(f"关键词: {', '.join(keywords)}")
    log.append(f"参数: top {top_q} 问题 × top {per_q} 答 ({'紧凑' if compact else '完整'}模式)\n")

    for qinfo, d in results:
        answers = sorted(d.get("data", []), key=lambda x: x.get("voteup_count", 0), reverse=True)
        log.append(f"\n## {qinfo['title']}")
        log.append(f"https://www.zhihu.com/question/{qinfo['id']} | {qinfo['answer_count']}答 | 命中 {len(qinfo['keywords_hit'])}kw\n")
        for i, a in enumerate(answers[:per_q], 1):
            author = a.get("author", {}).get("name", "?")
            votes = a.get("voteup_count", 0)
            comments = a.get("comment_count", 0)
            content = strip_html(a.get("content", ""))
            log.append(f"\n### [{i}] @{author} ({votes}赞 / {comments}评)")
            log.append(make_summary(content, head=head_n, tail=tail_n))
            log.append("")

    text = "\n".join(log)

    if args.md_out:
        Path(args.md_out).write_text(text)
        print(f"\n✓ {args.md_out}: {len(text)} chars ({len(text)//1024} KB)", file=sys.stderr)
        if not args.quiet:
            # 仅打印前 1500 字 + 提示
            preview = text[:1500]
            tail_hint = f"\n\n...(完整 {len(text)} chars 见 {args.md_out})" if len(text) > 1500 else ""
            print(preview + tail_hint)
    else:
        print(text)


def cmd_qa_batch(args):
    """批量:抓多个问题的答案 + 各自 top N,合并成一个 markdown"""
    cookie = load_cookie()
    (ANSWERS_DIR).mkdir(parents=True, exist_ok=True)

    items = []
    for spec in args.qid:
        if ":" in spec:
            qid, title = spec.split(":", 1)
        else:
            qid, title = spec, ""
        items.append((qid, title))

    def fetch(item):
        qid, _ = item
        url = ANSWER_API.format(qid=qid) + f"?include=data%5B*%5D.content%2Cvoteup_count%2Ccomment_count%2Cauthor.name%2Cauthor.headline&limit=20&offset=0&order=default"
        d = curl_json(url, cookie)
        (ANSWERS_DIR / f"{qid}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2))
        return item, d

    print(f"# 批量抓 {len(items)} 个问题的答案 ...")
    results = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for item, d in ex.map(fetch, items):
            results.append((item, d))
            totals = d.get("paging", {}).get("totals", "?")
            print(f"  {item[0]} -> {totals} 答")

    # 合并 markdown
    head_n = 300 if args.compact else 800
    tail_n = 100 if args.compact else 400
    md = []
    for (qid, qtitle), d in results:
        answers = sorted(d.get("data", []), key=lambda x: x.get("voteup_count", 0), reverse=True)
        totals = d.get("paging", {}).get("totals", "?")
        md.append(f"\n# {qtitle or '(无标题)'}\n")
        md.append(f"问题链接: https://www.zhihu.com/question/{qid} (共 {totals} 答)\n")
        md.append("=" * 70 + "\n")
        for i, a in enumerate(answers[:args.top], 1):
            author = a.get("author", {}).get("name", "?")
            votes = a.get("voteup_count", 0)
            comments = a.get("comment_count", 0)
            content = strip_html(a.get("content", ""))
            md.append(f"\n## 第 {i} 高赞 ({votes} 赞 / {comments} 评论) — @{author}\n")
            md.append(make_summary(content, head=head_n, tail=tail_n))
            md.append("\n")
        md.append("\n" + "=" * 70 + "\n")

    text = "\n".join(md)
    if args.md_out:
        Path(args.md_out).write_text(text)
        print(f"\n✓ 写入 {args.md_out} ({len(text)//1024} KB)")
    else:
        print(text)

def cmd_column_articles(args):
    """抓专栏内的文章列表 (走 API 拿到结构化数据)"""
    cookie = load_cookie()
    c_id = args.c_id
    limit = args.limit
    offset = args.offset
    url = COLUMN_API.format(c_id=c_id) + f"?limit={limit}&offset={offset}"
    d = curl_json(url, cookie)
    items = d.get("data", [])
    totals = d.get("paging", {}).get("totals", "?")

    # 落盘
    (COLUMNS_DIR).mkdir(parents=True, exist_ok=True)
    (COLUMNS_DIR / f"{c_id}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2))

    print(f"# 专栏 {c_id} 共 {totals} 篇, 取 {len(items)} 篇\n")
    print("| ID | 标题 | 更新时间 | 摘要 |")
    print("|---|---|---|---|")
    from datetime import datetime
    for a in items:
        aid = a.get("id", "?")
        title = a.get("title", "(无标题)")
        upd = a.get("updated", 0)
        upd_str = datetime.fromtimestamp(upd).strftime("%Y-%m-%d") if upd else "?"
        excerpt = (a.get("excerpt") or "").replace("\n", " ").replace("|", "\\|")[:80]
        print(f"| {aid} | [{title[:50]}](https://zhuanlan.zhihu.com/p/{aid}) | {upd_str} | {excerpt}... |")

    print(f"\n✓ 落盘 {COLUMNS_DIR}/{c_id}.json")
    print(f"\n下一步: 抓某篇全文 → python3 {Path(__file__).name} article {items[0].get('id', '?')}")

def cmd_comments(args):
    """抓答案的评论列表 (走老 API 端点, 绕开 comment_v5 反爬)"""
    cookie = load_cookie()
    aid = args.aid
    limit = args.limit
    offset = args.offset
    order = args.order  # normal | score | ts
    url = COMMENTS_API.format(aid=aid) + f"?limit={limit}&offset={offset}&order={order}&status=open"
    d = curl_json(url, cookie)

    comments = d.get("data", [])
    totals = d.get("common_counts", 0)

    # 落盘
    (COMMENTS_DIR).mkdir(parents=True, exist_ok=True)
    (COMMENTS_DIR / f"{aid}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2))

    print(f"# 答案 {aid} 共 {totals} 评 (order={order}), 取 {len(comments)} 条\n")

    for i, c in enumerate(comments, 1):
        # author 结构: {"role": "normal", "member": {"name": ...}}
        author_obj = c.get("author", {})
        if isinstance(author_obj, dict):
            author = author_obj.get("member", {}).get("name", "?") if isinstance(author_obj.get("member"), dict) else "匿名"
        else:
            author = "匿名"
        cid = c.get("id", "?")
        likes = c.get("vote_count", 0)
        content = strip_html(c.get("content", ""))
        child_n = c.get("child_comment_count", 0)
        created = c.get("created_time", 0)
        from datetime import datetime
        ts = datetime.fromtimestamp(created).strftime("%m-%d %H:%M") if created else "?"
        print(f"### [{i}] @{author} ({likes}赞 · {ts})")
        print(content)
        if child_n:
            print(f"\n└─ {child_n} 条子评论 (API 不下钻,需浏览器抓)")
        print(f"\n   链接: https://www.zhihu.com/comment/{cid}\n")
        print("---\n")

    print(f"✓ 落盘 {COMMENTS_DIR}/{aid}.json")
    if args.md_out:
        # 简化为表格写入
        md = [f"# 答案 {aid} 评论 ({totals} 条, order={order})\n"]
        md.append("| # | 作者 | 赞 | 时间 | 内容摘要 |")
        md.append("|---|---|---|---|---|")
        from datetime import datetime
        for i, c in enumerate(comments, 1):
            author_obj = c.get("author", {})
            if isinstance(author_obj, dict):
                author = author_obj.get("member", {}).get("name", "?") if isinstance(author_obj.get("member"), dict) else "匿名"
            else:
                author = "匿名"
            likes = c.get("vote_count", 0)
            content = strip_html(c.get("content", "")).replace("\n", " ").replace("|", "\\|")[:60]
            ts = datetime.fromtimestamp(c.get("created_time", 0)).strftime("%m-%d %H:%M") if c.get("created_time") else "?"
            md.append(f"| {i} | {author} | {likes} | {ts} | {content}... |")
        Path(args.md_out).write_text("\n".join(md))
        print(f"✓ 表格写入 {args.md_out}")

# ===== CLI =====
def main():
    p = argparse.ArgumentParser(description="知乎数据抓取 (API 路径, 不渲染浏览器)")
    sub = p.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("search", help="单关键词搜索")
    p1.add_argument("keyword")
    p1.add_argument("--limit", type=int, default=25)
    p1.add_argument("--type", default="question",
                    choices=["question", "column", "people", "topic", "zvideo"],
                    help="搜索类型 (article 在知乎用 column)")
    p1.set_defaults(func=cmd_search)

    p2 = sub.add_parser("batch-search", help="多关键词并发搜索 + 去重汇总")
    p2.add_argument("keyword", nargs="+")
    p2.add_argument("--limit", type=int, default=25)
    p2.set_defaults(func=cmd_batch_search)

    p3 = sub.add_parser("answers", help="抓单个问题的答案 -> JSON")
    p3.add_argument("qid")
    p3.add_argument("--limit", type=int, default=20)
    p3.set_defaults(func=cmd_answers)

    p4 = sub.add_parser("extract", help="answers JSON -> markdown")
    p4.add_argument("file")
    p4.add_argument("--top", type=int, default=3)
    p4.add_argument("--compact", action="store_true", help="紧凑模式 (head=300/tail=100)")
    p4.add_argument("--md-out")
    p4.set_defaults(func=cmd_extract)

    p5 = sub.add_parser("qa-batch", help="批量: 多问题 + 各自 top N -> 单个 markdown")
    p5.add_argument("qid", nargs="+", help="格式: qid 或 qid:title")
    p5.add_argument("--top", type=int, default=3)
    p5.add_argument("--compact", action="store_true", help="紧凑模式 (head=300/tail=100)")
    p5.add_argument("--md-out", default="qa-summary.md")
    p5.set_defaults(func=cmd_qa_batch)

    p_quick = sub.add_parser("quick", help="⭐ 一键: 多关键词搜索 + 去重 + 抓 top 答案 -> markdown (为 LLM 设计)")
    p_quick.add_argument("topic", help="主题/话题名 (用作默认关键词 + 文件名)")
    p_quick.add_argument("--keywords", nargs="+", help="自定义关键词列表 (默认: 主题 + 主题+资讯 + 主题+新闻)")
    p_quick.add_argument("--top-q", type=int, default=5, help="取 top N 问题 (默认5)")
    p_quick.add_argument("--per-q", type=int, default=3, help="每个问题取 top N 答 (默认3)")
    p_quick.add_argument("--limit", type=int, default=15, help="每关键词搜索条数 (默认15)")
    p_quick.add_argument("--compact", action="store_true", help="紧凑模式 (head=300/tail=100, 约 70%% token 节省)")
    p_quick.add_argument("--md-out", help="输出到文件 (推荐: 避免 context bloat)")
    p_quick.add_argument("--quiet", action="store_true", help="只写文件, 不打印正文")
    p_quick.set_defaults(func=cmd_quick)

    p6 = sub.add_parser("article", help="抓专栏文章正文 (SPA HTML 解析)")
    p6.add_argument("spec", help="完整 URL (https://zhuanlan.zhihu.com/p/xxx) 或纯 article id")
    p6.set_defaults(func=cmd_article)

    p7 = sub.add_parser("hotlist", help="知乎热榜")
    p7.add_argument("--limit", type=int, default=30, help="取前 N 条 (默认30)")
    p7.add_argument("--compact", action="store_true", help="紧凑模式: 仅标题表格, 不打摘要")
    p7.add_argument("--md-out", help="输出到文件 (默认 hotlist.json)")
    p7.set_defaults(func=cmd_hotlist)

    p8 = sub.add_parser("column-articles", help="抓专栏内文章列表 (API)")
    p8.add_argument("c_id", help="专栏 id (如 c_1297485212247425024)")
    p8.add_argument("--limit", type=int, default=20, help="取前 N 篇 (默认20)")
    p8.add_argument("--offset", type=int, default=0, help="分页偏移 (默认0)")
    p8.set_defaults(func=cmd_column_articles)

    p9 = sub.add_parser("comments", help="抓答案的评论 (API, 绕开 comment_v5 反爬)")
    p9.add_argument("aid", help="答案 id (如 2050463219832164626)")
    p9.add_argument("--limit", type=int, default=20, help="取前 N 条评论 (默认20)")
    p9.add_argument("--offset", type=int, default=0, help="分页偏移 (默认0)")
    p9.add_argument("--order", default="score", choices=["normal", "score", "ts"],
                    help="排序: score(默认) / ts(时间) / normal")
    p9.add_argument("--md-out", help="输出简洁表格到文件")
    p9.set_defaults(func=cmd_comments)

    p_paths = sub.add_parser("paths", help="打印当前 skill 的路径配置 (含 data 目录, cookies 路径)")
    p_paths.set_defaults(func=lambda a: print(report()))

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()