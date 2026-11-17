#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yun-zhi-seo-skill / seo_audit.py
零依赖（仅 Python 标准库）的网站 SEO 体检与打分工具。

覆盖维度（与 SKILL.md 流水线一一对应）：
  关键词分析 / Title分析 / Description分析 / Heading分析 /
  URL分析 / Internal Link分析 / Schema分析 / Indexability分析 / 页面分析

用法:
  # 整站爬取并分析（默认最多 50 页、深度 3）
  python seo_audit.py audit --url https://example.com --max-pages 50 --out report.json

  # 单页分析（可来自本地文件，用于离线分析页面源码）
  python seo_audit.py page --url https://example.com/about --file about.html --out page.json

  # 基于已有报告重新计算 SEO Score（不改抓取，仅重算评分/建议）
  python seo_audit.py score --report report.json --out scored.json

输出: JSON 报告，含 各维度评分、整站 SEO Score、按风险分级(low/high)的优化建议。

已知限制:
  - 不执行 JavaScript，仅分析服务端返回的 HTML（SPA 站需先渲染或提供源码）。
  - 中文分词未引入 jieba（保持零依赖），中文关键词密度以「字符级 bigram 词频」作为代理信号。
  - 爬取遵守 robots.txt 与 polite delay（相邻请求最小间隔 2 秒）；默认仅抓同域名内链。
"""

import sys
import os
import re
import json
import time
import argparse
import urllib.parse
import urllib.request
import urllib.error
import urllib.robotparser
from collections import Counter
from html.parser import HTMLParser

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

UA = "Mozilla/5.0 (compatible; YunZhiSEO/1.0)"

# 抓取频率下限：相邻两次请求最小间隔（秒），防止对目标站点造成压力
MIN_DELAY = 2.0

# 维度权重（合计 100，与 SKILL.md 流水线对应）
WEIGHTS = {
    "keyword": 10,        # 关键词分析
    "title": 15,          # Title分析
    "description": 10,    # Description分析
    "heading": 10,        # Heading分析
    "url": 10,            # URL分析
    "internal_link": 10,  # Internal Link分析
    "schema": 10,         # Schema分析
    "indexability": 20,   # Indexability分析
    "page": 5,            # 页面分析
}

# 英文停用词（用于词频统计）
STOPWORDS = set("""
a an the and or but if while of to in on at by for with from as is are was were be been being
this that these those it its it's he she they we you your our their my me him her them us
not no nor so than too very can will just dont don't into over under again about up down out
i'm im you're we're they're he's she's there's what's who's how's here's where's
of is do does did has have had would could should may might must shall will
""".split())

# 通用锚文本（内部链接质量惩罚）
GENERIC_ANCHORS = {
    "click here", "here", "more", "read more", "learn more", "详情", "点击",
    "更多", "点击查看", "点击这里", "阅读更多", "查看详情", "more...", "here.",
}

# 理想区间（字符数）
TITLE_IDEAL = (30, 60)
DESC_IDEAL = (70, 160)


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def clamp(x, lo=0, hi=100):
    return max(lo, min(hi, x))


def normalize_url(u):
    """规范化 URL：去 fragment、去尾斜杠、小写 scheme/host、剔除 utm_* 跟踪参数。"""
    p = urllib.parse.urlparse(u)
    path = p.path or "/"
    if path.endswith("/") and path != "/":
        path = path[:-1]
    q = p.query
    if q:
        params = urllib.parse.parse_qs(q, keep_blank_values=True)
        keep = {k: v for k, v in params.items() if not k.lower().startswith("utm_")}
        q = urllib.parse.urlencode(keep, doseq=True)
    return urllib.parse.urlunparse(
        (p.scheme.lower(), p.netloc.lower(), path, "", q, "")
    )


def is_internal(url, base_netloc):
    try:
        return urllib.parse.urlparse(url).netloc == base_netloc
    except Exception:
        return False


def is_home(url):
    p = urllib.parse.urlparse(url)
    return (p.path in ("", "/")) and not p.query


def is_html(headers, html_head):
    ctype = (headers.get("Content-Type") or headers.get("content-type") or "").lower()
    if "text/html" in ctype:
        return True
    head = html_head[:200].lower()
    return ("<html" in head) or ("<!doctype" in head)


# ---------------------------------------------------------------------------
# HTML 解析器
# ---------------------------------------------------------------------------

class SEOParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.title = None
        self._in_title = False

        self.meta_name = {}
        self.meta_property = {}
        self.charset = None
        self.canonical = None
        self.viewport = None
        self.lang = None

        self.headings = []          # [(level, text)]
        self._heading_level = None
        self._heading_text = []

        self.links = []             # [(href, text)]
        self._in_a = False
        self._a_href = None
        self._link_text = []

        self.images = []            # [(src, alt)]
        self.jsonld = []            # [raw_json_string]
        self.microdata = False

        self._in_jsonld = False
        self._jsonld_buf = []
        self._skip_depth = 0        # 在 <script>/<style> 内

        self.text_parts = []

    # -- starttag --
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "html":
            self.lang = d.get("lang") or d.get("xml:lang")
        if tag in ("script", "style"):
            self._skip_depth += 1
            if (d.get("type") or "").lower() == "application/ld+json":
                self._in_jsonld = True
                self._jsonld_buf = []
            return
        if self._skip_depth > 0:
            return
        if tag == "title":
            self._in_title = True
            return
        if tag == "meta":
            self._handle_meta(d)
            return
        if tag == "link" and (d.get("rel") or "").lower() == "canonical":
            self.canonical = d.get("href")
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading_level = int(tag[1])
            self._heading_text = []
            return
        if tag == "a":
            href = d.get("href")
            if href:
                self._in_a = True
                self._a_href = href
                self._link_text = []
            return
        if tag == "img":
            self.images.append((d.get("src"), d.get("alt")))
            return
        if tag in ("div", "span", "section", "article", "li", "ul", "ol"):
            if d.get("itemscope") is not None or d.get("itemtype"):
                self.microdata = True

    def _handle_meta(self, d):
        name = (d.get("name") or "").lower()
        prop = (d.get("property") or d.get("itemprop") or "").lower()
        content = d.get("content")
        charset = d.get("charset")
        httpeq = (d.get("http-equiv") or "").lower()
        if charset:
            self.charset = charset
        if httpeq == "content-type" and content:
            m = re.search(r"charset=([\w-]+)", content, re.I)
            if m:
                self.charset = m.group(1)
        if name == "description":
            self.meta_name["description"] = content
        elif name == "keywords":
            self.meta_name["keywords"] = content
        elif name == "robots":
            self.meta_name["robots"] = content
        elif name == "viewport":
            self.viewport = content
        elif name:
            self.meta_name[name] = content
        if prop:
            self.meta_property[prop] = content

    # -- data --
    def handle_data(self, data):
        if self._skip_depth > 0:
            if self._in_jsonld:
                self._jsonld_buf.append(data)
            return
        if self._in_title:
            self.title = (self.title or "") + data
            return
        if self._heading_level is not None:
            self._heading_text.append(data)
            return
        if self._in_a:
            self._link_text.append(data)
            return
        self.text_parts.append(data)

    # -- endtag --
    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            if self._in_jsonld and tag == "script":
                raw = "".join(self._jsonld_buf).strip()
                if raw:
                    self.jsonld.append(raw)
                self._in_jsonld = False
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth > 0:
            return
        if tag == "title":
            self._in_title = False
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            text = " ".join(self._heading_text).strip()
            self.headings.append((self._heading_level, text))
            self._heading_level = None
            self._heading_text = []
            return
        if tag == "a":
            self.links.append((self._a_href, " ".join(self._link_text).strip()))
            self._in_a = False
            self._a_href = None
            self._link_text = []


# ---------------------------------------------------------------------------
# 文本 / 关键词分析
# ---------------------------------------------------------------------------

def extract_focus_keywords(parser):
    """从 meta keywords / title 推断关注关键词（最多 5 个）。"""
    focus = []
    kw = parser.meta_name.get("keywords")
    if kw:
        focus += [k.strip() for k in kw.split(",") if k.strip()]
    if not focus:
        for w in re.findall(r"[A-Za-z]{3,}", (parser.title or "").lower()):
            if w not in STOPWORDS:
                focus.append(w)
    return focus[:5]


def word_frequency(text):
    """英文词频（去停用词）+ 中文 bigram 词频。返回 (en_counter, zh_bigram_counter, word_count)。"""
    lower = text.lower()
    en_words = [w for w in re.findall(r"[a-z][a-z'-]*", lower) if w not in STOPWORDS]
    en_counter = Counter(en_words)

    # 中文：按连续 CJK 段切分，生成 bigram
    zh_bigrams = Counter()
    for seg in re.findall(r"[\u4e00-\u9fff]+", text):
        for i in range(len(seg) - 1):
            zh_bigrams[seg[i:i + 2]] += 1
    zh_bigrams = Counter({k: v for k, v in zh_bigrams.items() if v >= 2})

    word_count = len(en_words) + sum(zh_bigrams.values())
    return en_counter, zh_bigrams, word_count


def keyword_coverage(parser, focus, text_lower, slug_lower):
    """返回每个关注词在 [title, desc, h1, url, headings] 的出现情况与正文密度。"""
    title = (parser.title or "").lower()
    desc = (parser.meta_name.get("description") or "").lower()
    h1 = " ".join(t for _, t in parser.headings if t).lower()
    headings_all = " ".join(t for _, t in parser.headings).lower()

    coverage = {}
    for kw in focus:
        k = kw.lower()
        loc = {
            "title": k in title,
            "description": k in desc,
            "h1": k in h1,
            "url": k in slug_lower,
            "heading": k in headings_all,
        }
        # 正文密度（近似）
        if " " in k or not re.match(r"^[a-z]", k):
            occ = text_lower.count(k)
        else:
            occ = len(re.findall(r"\b" + re.escape(k) + r"\b", text_lower))
        coverage[kw] = {"locations": loc, "body_occurrences": occ}
    return coverage


# ---------------------------------------------------------------------------
# 单页指标提取
# ---------------------------------------------------------------------------

def analyze_html(html, base_url):
    parser = SEOParser(base_url)
    parser.feed(html)
    parser.close()

    text = " ".join(parser.text_parts)
    text_lower = text.lower()
    en_counter, zh_bigrams, word_count = word_frequency(text)

    netloc = urllib.parse.urlparse(base_url).netloc
    slug = urllib.parse.urlparse(base_url).path.lower()

    # 链接分析
    internal_links = 0
    external_links = 0
    generic_anchor = 0
    total_anchors = 0
    out_internal = []
    for href, t in parser.links:
        if not href or href.startswith("#") or href.lower().startswith("javascript:"):
            continue
        absurl = urllib.parse.urljoin(base_url, href)
        total_anchors += 1
        if is_internal(absurl, netloc):
            internal_links += 1
            out_internal.append(normalize_url(absurl))
        else:
            external_links += 1
        if t.strip().lower() in GENERIC_ANCHORS:
            generic_anchor += 1

    # 图片 alt
    images_total = len(parser.images)
    images_missing_alt = sum(1 for _, alt in parser.images if not alt or not alt.strip())

    # Schema 校验
    jsonld_valid = 0
    jsonld_total = len(parser.jsonld)
    for raw in parser.jsonld:
        try:
            json.loads(raw)
            jsonld_valid += 1
        except Exception:
            pass

    focus = extract_focus_keywords(parser)
    coverage = keyword_coverage(parser, focus, text_lower, slug)

    h1_list = [t for lvl, t in parser.headings if lvl == 1]
    h_levels = [lvl for lvl, _ in parser.headings]

    page = {
        "url": base_url,
        "title": (parser.title or "").strip(),
        "description": (parser.meta_name.get("description") or "").strip(),
        "keywords_meta": (parser.meta_name.get("keywords") or "").strip(),
        "robots_meta": (parser.meta_name.get("robots") or "").strip().lower(),
        "x_robots": None,                       # 由 fetch 层填充
        "charset": (parser.charset or "").lower(),
        "viewport": parser.viewport,
        "lang": parser.lang,
        "canonical": parser.canonical,
        "h1_count": len(h1_list),
        "headings": [{"level": l, "text": t} for l, t in parser.headings],
        "heading_levels": h_levels,
        "internal_links": internal_links,
        "external_links": external_links,
        "generic_anchor": generic_anchor,
        "total_anchors": total_anchors,
        "out_internal": sorted(set(out_internal)),
        "images_total": images_total,
        "images_missing_alt": images_missing_alt,
        "jsonld_count": jsonld_total,
        "jsonld_valid": jsonld_valid,
        "microdata": parser.microdata,
        "word_count": word_count,
        "https": base_url.lower().startswith("https"),
        "focus_keywords": focus,
        "keyword_coverage": coverage,
        "top_en_words": en_counter.most_common(20),
        "top_zh_bigrams": zh_bigrams.most_common(20),
        "status": 200,
    }
    return page


# ---------------------------------------------------------------------------
# 评分（每个维度 0-100）
# ---------------------------------------------------------------------------

def _len_score(length, ideal, soft_low, soft_high):
    lo, hi = ideal
    if length == 0:
        return 0
    if lo <= length <= hi:
        return 100
    if soft_low <= length < lo:
        return int(60 + 40 * (length - soft_low) / max(1, (lo - soft_low)))
    if hi < length <= soft_high:
        return int(100 - 40 * (length - hi) / max(1, (soft_high - hi)))
    if length < soft_low:
        return clamp(int(40 * length / max(1, soft_low)))
    return clamp(int(60 - 40 * (length - soft_high) / max(1, (soft_high * 1.5 - soft_high))))


def score_title(p):
    t = p["title"]
    L = len(t)
    if L == 0:
        return 0
    len_s = _len_score(L, TITLE_IDEAL, 20, 90)
    kw_s = 100 if (p["focus_keywords"] and
                   any(c["locations"]["title"] for c in p["keyword_coverage"].values())) else 55
    return clamp(int(0.7 * len_s + 0.3 * kw_s))


def score_description(p):
    d = p["description"]
    L = len(d)
    if L == 0:
        return 0
    len_s = _len_score(L, DESC_IDEAL, 40, 220)
    kw_s = 100 if (p["focus_keywords"] and
                   any(c["locations"]["description"] for c in p["keyword_coverage"].values())) else 55
    return clamp(int(0.7 * len_s + 0.3 * kw_s))


def score_heading(p):
    if p["h1_count"] == 0:
        return 30
    base = 100 if p["h1_count"] == 1 else 70
    # 跳级检测：如 h1 后直接 h3
    levels = [l for l in p["heading_levels"]]
    skipped = False
    prev = 0
    for l in levels:
        if prev and l > prev + 1:
            skipped = True
            break
        prev = l
    if skipped:
        base -= 15
    if p["focus_keywords"] and not any(c["locations"]["h1"] or c["locations"]["heading"]
                                       for c in p["keyword_coverage"].values()):
        base -= 10
    return clamp(base)


def score_url(p):
    if is_home(p["url"]):
        return 100
    path = urllib.parse.urlparse(p["url"]).path.lower()
    s = 100
    if "?" in p["url"]:
        s -= 20
    if "_" in path:
        s -= 10
    if any(c.isupper() for c in path):
        s -= 10
    if len(path) > 80:
        s -= 10
    if p["focus_keywords"]:
        slug = path
        if not any(kw.lower() in slug for kw in p["focus_keywords"]):
            s -= 15
    return clamp(s)


def score_schema(p):
    if p["jsonld_count"] > 0:
        return 100 if p["jsonld_valid"] == p["jsonld_count"] else 50
    if p["microdata"]:
        return 70
    return 0


def score_indexability(p):
    s = 100
    rm = p.get("robots_meta") or ""
    xr = p.get("x_robots") or ""
    if "noindex" in rm or "noindex" in xr:
        return 0
    if p.get("robots_allowed") is False:
        s -= 60
    if p.get("status") != 200:
        s -= 40
    if not p["https"]:
        s -= 15
    if p["canonical"]:
        if p["canonical"] != p["url"] and normalize_url(p["canonical"]) != normalize_url(p["url"]):
            s -= 10
    else:
        s -= 10
    return clamp(s)


def score_page(p):
    s = 100
    wc = p["word_count"]
    if wc < 150:
        s -= 40
    elif wc < 300:
        s -= 25
    if p["images_total"] > 0 and p["images_missing_alt"] / p["images_total"] > 0.3:
        s -= 20
    if not p["viewport"]:
        s -= 15
    if not p["lang"]:
        s -= 5
    if p["charset"] and p["charset"] not in ("utf-8", "utf8"):
        s -= 5
    return clamp(s)


def score_keyword(p):
    if not p["focus_keywords"]:
        return 65
    cov = p["keyword_coverage"]
    # 覆盖位置占比（title/desc/h1/url/heading 5 个位置）
    ratios = []
    for c in cov.values():
        loc = c["locations"]
        hit = sum([loc["title"], loc["description"], loc["h1"], loc["url"], loc["heading"]])
        ratios.append(hit / 5.0)
    coverage_ratio = sum(ratios) / len(ratios)
    # 密度
    total_occ = sum(c["body_occurrences"] for c in cov.values())
    density = (total_occ / p["word_count"] * 100) if p["word_count"] else 0
    if density == 0:
        dens_s = 20
    elif density <= 0.3:
        dens_s = 50
    elif density <= 2:
        dens_s = 100
    elif density <= 3:
        dens_s = 80
    else:
        dens_s = 50
    return clamp(int(0.6 * coverage_ratio * 100 + 0.4 * dens_s))


def score_internal_link(pages):
    if len(pages) <= 1:
        return None  # 单页无法评估
    s = 100
    inbounds = Counter()
    # 过滤抓取失败/非 HTML 页面（与 aggregate 其它维度口径一致）
    pages = [p for p in pages if "error" not in p]
    if len(pages) <= 1:
        return None
    for p in pages:
        for t in p.get("out_internal", []):
            inbounds[t] += 1
    orphan = 0
    for p in pages:
        if not is_home(p["url"]) and inbounds.get(normalize_url(p["url"]), 0) == 0:
            orphan += 1
    s -= orphan * 10
    avg_int = sum(p["internal_links"] for p in pages) / len(pages)
    if avg_int < 3:
        s -= (3 - avg_int) * 5
    total_anchor = sum(p["total_anchors"] for p in pages)
    total_generic = sum(p["generic_anchor"] for p in pages)
    if total_anchor > 0:
        gr = total_generic / total_anchor
        if gr > 0.3:
            s -= (gr - 0.3) * 100
    return clamp(s)


# ---------------------------------------------------------------------------
# 建议生成（按风险分级）
# ---------------------------------------------------------------------------

def build_suggestions(pages):
    sug = []
    n = 0
    # 过滤抓取失败/非 HTML 页面（与 aggregate 口径一致），避免访问缺失字段
    pages = [p for p in pages if "error" not in p]

    def add(dimension, risk, issue, recommendation, affected, fix=None):
        nonlocal n
        n += 1
        sug.append({
            "id": "S%03d" % n,
            "dimension": dimension,
            "risk": risk,
            "issue": issue,
            "recommendation": recommendation,
            "pages": affected,
            "fix": fix or {},
        })

    for p in pages:
        u = p["url"]
        # Title
        if not p["title"]:
            add("title", "low", "页面缺少 <title>", "补充能概括页面主题、含核心关键词的标题（30-60 字符）。",
                [u], {"type": "meta_title", "value": p["focus_keywords"][0] if p["focus_keywords"] else u})
        elif not (TITLE_IDEAL[0] <= len(p["title"]) <= TITLE_IDEAL[1]):
            add("title", "low", "标题长度 %d 字符，不在理想区间 30-60" % len(p["title"]),
                "精简或扩展标题至 30-60 字符，并前置核心关键词。", [u],
                {"type": "meta_title", "value": p["title"][:60]})
        # Description
        if not p["description"]:
            add("description", "low", "页面缺少 meta description", "补充 70-160 字符的描述，含核心关键词与行动号召。",
                [u], {"type": "meta_description", "value": ""})
        elif not (DESC_IDEAL[0] <= len(p["description"]) <= DESC_IDEAL[1]):
            add("description", "low", "描述长度 %d 字符，不在理想区间 70-160" % len(p["description"]),
                "调整描述至 70-160 字符。", [u], {"type": "meta_description", "value": p["description"][:160]})
        # Heading（高风险：结构改动影响布局）
        if p["h1_count"] == 0:
            add("heading", "high", "页面缺少 H1 标题", "新增一个概括页面主题的 H1（含核心关键词），会影响页面结构需确认。",
                [u], {"type": "add_h1", "value": p["focus_keywords"][0] if p["focus_keywords"] else "主标题"})
        elif p["h1_count"] > 1:
            add("heading", "high", "页面存在 %d 个 H1（应仅 1 个）" % p["h1_count"],
                "保留一个主 H1，其余改为 H2/H3，改动较大需确认。", [u], {"type": "fix_h1", "value": ""})
        # Schema（低风险：追加 JSON-LD）
        if p["jsonld_count"] == 0 and not p["microdata"]:
            add("schema", "low", "页面缺少结构化数据(JSON-LD)", "按页面类型注入 schema.org JSON-LD（如 Organization/Product/Article/BreadcrumbList）。",
                [u], {"type": "add_jsonld", "value": "{}"})
        # Indexability
        if "noindex" in (p.get("robots_meta") or ""):
            add("indexability", "high", "页面 meta robots 含 noindex", "确认是否应被收录；若要收录需移除 noindex（影响索引，需确认）。",
                [u], {"type": "remove_noindex", "value": ""})
        if not p["canonical"]:
            add("indexability", "low", "页面缺少 canonical", "补充指向自身规范 URL 的 <link rel=canonical>。",
                [u], {"type": "add_canonical", "value": u})
        if not p["https"]:
            add("indexability", "high", "页面未使用 HTTPS", "全站启用 HTTPS 并配置 301 跳转（基础设施改动，需确认）。",
                [u], {"type": "enable_https", "value": ""})
        # 页面
        if p["images_total"] > 0 and p["images_missing_alt"] / p["images_total"] > 0.3:
            add("page", "low", "超过 30% 图片缺少 alt 文本", "为图片补充描述性 alt（含相关关键词，勿堆砌）。",
                [u], {"type": "add_alt", "value": ""})
        if not p["viewport"]:
            add("page", "low", "缺少 viewport 元标签（移动端不友好）", "补充 <meta name=viewport content=\"width=device-width,initial-scale=1\">。",
                [u], {"type": "add_viewport", "value": "width=device-width,initial-scale=1"})
        if not p["lang"]:
            add("page", "low", "html 缺少 lang 属性", "为 <html> 设置 lang（如 zh-CN / en）。",
                [u], {"type": "add_lang", "value": "zh-CN"})
        if p["word_count"] < 300:
            add("page", "high", "正文内容偏薄（约 %d 词）" % p["word_count"],
                "扩充原创、有价值的内容至 300+ 词，自然融入关键词（内容重写需确认）。", [u],
                {"type": "expand_content", "value": ""})
        # 关键词
        if p["focus_keywords"] and p["keyword_coverage"]:
            for kw, c in p["keyword_coverage"].items():
                if not (c["locations"]["title"] or c["locations"]["h1"] or c["locations"]["heading"]):
                    add("keyword", "high", "关注词「%s」未出现在标题/H1/Heading" % kw,
                        "在标题与 H1 中自然融入该关键词（改动标题/标题层级需确认）。", [u],
                        {"type": "inject_keyword", "value": kw})

    # Internal Link（站点级）
    if len(pages) > 1:
        inbounds = Counter()
        for p in pages:
            for t in p.get("out_internal", []):
                inbounds[normalize_url(t)] += 1
        orphans = [p["url"] for p in pages if not is_home(p["url"])
                   and inbounds.get(normalize_url(p["url"]), 0) == 0]
        if orphans:
            add("internal_link", "high", "存在 %d 个未被内部链接的孤岛页面" % len(orphans),
                "在相关页面增加指向这些页面的内部链接，提升抓取与权重传递（结构改动需确认）。",
                orphans, {"type": "add_internal_links", "value": ""})

    return sug


# ---------------------------------------------------------------------------
# 聚合与总分
# ---------------------------------------------------------------------------

def aggregate(pages):
    dim_scores = {}
    for dim, fn in (("title", score_title), ("description", score_description),
                    ("heading", score_heading), ("url", score_url),
                    ("schema", score_schema), ("indexability", score_indexability),
                    ("page", score_page), ("keyword", score_keyword)):
        vals = [fn(p) for p in pages if "error" not in p]
        dim_scores[dim] = round(sum(vals) / len(vals)) if vals else 0
    il = score_internal_link(pages)
    if il is not None:
        dim_scores["internal_link"] = round(il)
    else:
        dim_scores["internal_link"] = None  # 单页不评估

    # 总分：internal_link 为 None 时把其权重摊到其余维度
    total_w = sum(WEIGHTS[d] for d in WEIGHTS if dim_scores.get(d) is not None)
    total = sum(dim_scores[d] * WEIGHTS[d] for d in WEIGHTS if dim_scores.get(d) is not None)
    seo_score = round(total / total_w) if total_w else 0

    return dim_scores, seo_score


# ---------------------------------------------------------------------------
# 抓取
# ---------------------------------------------------------------------------

def fetch_url(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            final = resp.geturl()
            status = resp.status
            headers = dict(resp.headers)
            enc = resp.headers.get_content_charset() or "utf-8"
            raw = resp.read()
    except urllib.error.HTTPError as e:
        headers = dict(e.headers) if e.headers else {}
        enc = (e.headers.get_content_charset() if e.headers else None) or "utf-8"
        try:
            raw = e.read()
        except Exception:
            raw = b""
        return e.code, headers, raw.decode(enc, "replace"), url
    except Exception as e:
        return 0, {}, "", url
    return status, headers, raw.decode(enc, "replace"), final


def fetch_site_meta(start_url):
    """抓取 robots.txt 与 sitemap，供全站分析使用。"""
    netloc = urllib.parse.urlparse(start_url).netloc
    base = "%s://%s" % (urllib.parse.urlparse(start_url).scheme, netloc)
    meta = {"robots_allowed": True, "sitemap_urls": [], "rp": None}

    # robots.txt
    try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(urllib.parse.urljoin(base + "/", "robots.txt"))
        rp.read()
        meta["rp"] = rp
        meta["robots_allowed"] = rp.can_fetch(UA, start_url)
    except Exception:
        meta["rp"] = None

    # sitemap
    for cand in ("/sitemap.xml", "/sitemap_index.xml"):
        try:
            s, h, body, _ = fetch_url(base + cand)
            if s == 200 and "<" in body:
                locs = re.findall(r"<loc>(.*?)</loc>", body, re.S)
                meta["sitemap_urls"].extend([x.strip() for x in locs])
        except Exception:
            pass
    return meta


def crawl(start_url, max_pages=50, max_depth=3, delay=MIN_DELAY):
    # 强制最小抓取间隔：无论传入什么值，相邻请求间隔不得低于 MIN_DELAY（2 秒）
    delay = max(float(delay), MIN_DELAY)
    pages = []
    visited = set()
    base_netloc = urllib.parse.urlparse(start_url).netloc
    site_meta = fetch_site_meta(start_url)
    rp = site_meta.get("rp")
    sitemap_set = set(site_meta.get("sitemap_urls", []))

    queue = [(start_url, 0)]
    while queue and len([p for p in pages if "error" not in p]) < max_pages:
        url, depth = queue.pop(0)
        norm = normalize_url(url)
        if norm in visited or depth > max_depth:
            continue
        visited.add(norm)

        status, headers, html, final = fetch_url(url)
        if status != 200 or not is_html(headers, html):
            pages.append({"url": url, "status": status, "error": "non-200/non-html"})
            continue

        p = analyze_html(html, final)
        p["status"] = status
        p["x_robots"] = (headers.get("X-Robots-Tag") or headers.get("x-robots-tag") or "").lower()
        if rp is not None:
            try:
                p["robots_allowed"] = rp.can_fetch(UA, final)
            except Exception:
                p["robots_allowed"] = True
        else:
            p["robots_allowed"] = True
        p["in_sitemap"] = normalize_url(final) in sitemap_set

        pages.append(p)

        # 入队内链
        for t in p["out_internal"]:
            if t not in visited and depth + 1 <= max_depth:
                queue.append((t, depth + 1))

        if delay:
            time.sleep(delay)

    return pages, site_meta


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def run_audit(args):
    pages, site_meta = crawl(args.url, args.max_pages, args.depth, args.delay)
    dim, score = aggregate(pages)
    sug = build_suggestions(pages)
    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "mode": "audit",
        "start_url": args.url,
        "site": {
            "domain": urllib.parse.urlparse(args.url).netloc,
            "crawled_pages": len([p for p in pages if "error" not in p]),
            "robots_allowed": site_meta.get("robots_allowed"),
            "sitemap_count": len(site_meta.get("sitemap_urls", [])),
        },
        "dimension_scores": dim,
        "seo_score": score,
        "suggestions": sug,
        "pages": pages,
    }
    _dump(report, args.out)
    print("抓取 %d 页，SEO Score = %d" % (report["site"]["crawled_pages"], score))
    _print_summary(dim, score, sug)


def run_page(args):
    if args.file:
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
        base_url = args.url or ("file://" + os.path.abspath(args.file))
    else:
        status, headers, html, final = fetch_url(args.url)
        base_url = final
    p = analyze_html(html, base_url)
    p["url"] = base_url
    p["x_robots"] = ""
    p["robots_allowed"] = True
    p["in_sitemap"] = False
    dim, score = aggregate([p])
    sug = build_suggestions([p])
    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "mode": "page",
        "start_url": base_url,
        "site": {"domain": urllib.parse.urlparse(base_url).netloc, "crawled_pages": 1},
        "dimension_scores": dim,
        "seo_score": score,
        "suggestions": sug,
        "pages": [p],
    }
    _dump(report, args.out)
    print("单页分析完成，SEO Score = %d" % score)
    _print_summary(dim, score, sug)


def run_score(args):
    with open(args.report, "r", encoding="utf-8") as f:
        report = json.load(f)
    pages = report.get("pages", [])
    dim, score = aggregate(pages)
    sug = build_suggestions(pages)
    report["dimension_scores"] = dim
    report["seo_score"] = score
    report["suggestions"] = sug
    _dump(report, args.out)
    print("重算完成，SEO Score = %d" % score)
    _print_summary(dim, score, sug)


def _dump(report, out):
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print("报告已写入: %s" % out)
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))


def _print_summary(dim, score, sug):
    print("\n=== 维度评分 ===")
    for d, v in dim.items():
        print("  %-14s : %s" % (d, "N/A(单页)" if v is None else v))
    print("  %-14s : %d" % ("SEO Score", score))
    low = [s for s in sug if s["risk"] == "low"]
    high = [s for s in sug if s["risk"] == "high"]
    print("  建议: 低风险 %d 项 / 高风险 %d 项" % (len(low), len(high)))


def main():
    ap = argparse.ArgumentParser(description="yun-zhi-seo-skill SEO 体检工具")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a_audit = sub.add_parser("audit", help="整站爬取分析")
    a_audit.add_argument("--url", required=True)
    a_audit.add_argument("--max-pages", type=int, default=50)
    a_audit.add_argument("--depth", type=int, default=3)
    a_audit.add_argument("--delay", type=float, default=MIN_DELAY,
                         help="相邻请求最小间隔秒数（下限 2 秒，传更小值也会被强制提升到 2）")
    a_audit.add_argument("--out")
    a_audit.set_defaults(func=run_audit)

    a_page = sub.add_parser("page", help="单页分析（可来自本地文件）")
    a_page.add_argument("--url", required=True, help="页面 URL（用于链接解析/URL 分析上下文）")
    a_page.add_argument("--file", help="本地 HTML 文件路径（离线分析源码）")
    a_page.add_argument("--out")
    a_page.set_defaults(func=run_page)

    a_score = sub.add_parser("score", help="基于已有报告重算评分")
    a_score.add_argument("--report", required=True)
    a_score.add_argument("--out")
    a_score.set_defaults(func=run_score)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
