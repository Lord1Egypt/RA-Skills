#!/usr/bin/env python3
"""Star Search v11.0 - Hybrid HTTP + Playwright 多引擎搜索

架构：HTTP引擎(aiohttp)不需要浏览器，Playwright引擎保留给反爬严格的国内引擎。
- HTTP: Google, DuckDuckGo, Bing (国际)
- Playwright: 搜狗, 百度, 360, 微信

语言感知路由：中文查询优先国内引擎+Google，非中文查询走国际引擎。
"""
import json, re, sys, time, argparse, os, asyncio, sqlite3, hashlib
from urllib.parse import quote, urlparse
from datetime import datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    from playwright.async_api import async_playwright
    _PLAYWRIGHT_OK = True
except ImportError:
    async_playwright = None
    _PLAYWRIGHT_OK = False
    import sys
    print("⚠️  playwright 未安装 — 浏览器引擎 (sogou/baidu/360/weixin) 不可用；HTTP 引擎照常工作", file=sys.stderr)
import aiohttp

# ===== 配置 =====
STEALTH_JS = os.path.join(os.path.dirname(__file__), 'stealth.js')
CACHE_DB = os.path.join(os.path.dirname(__file__), '.search_cache.sqlite')
USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/131.0.0.0 Safari/537.36')
VIEWPORT = {'width': 1920, 'height': 1080}

# Playwright引擎（反爬严格，需要浏览器）
PW_BASE_URLS = {
    'sogou':  'https://www.sogou.com/web?query={q}&ie=utf8',
    'baidu':  'https://www.baidu.com/s?wd={q}',
    '360':    'https://www.so.com/s?q={q}',
    'weixin': 'https://weixin.sogou.com/weixin?type=2&query={q}&ie=utf8',
}

# HTTP引擎（aiohttp，不需要浏览器）
HTTP_BASE_URLS = {
    # 'sogou': v16 移除 — PW_PARSERS 有但 HTTP_PARSERS 无，会 KeyError。sogou 走 PW 即可
    'bing_cn':  'https://cn.bing.com/search?q={q}&setlang=zh-cn&count=15',
    # v16.1: bing_http 改动态 setlang（{lang} 占位符在 _search_http 替换）
    'bing_http': 'https://www.bing.com/search?q={q}&setlang={lang}&count=15',
    'github_issues': 'https://api.github.com/search/issues?q={q}+language:zh+archived:false&sort=updated&order=desc&per_page=15',
    # v15: 3个 site:bing 直搜代理 — 免反爬 <1秒
    'toutiao':  'https://cn.bing.com/search?q=site%3Atoutiao.com+{q}&setlang=zh-cn&count=15',
    'zhihu':    'https://cn.bing.com/search?q=site%3Azhihu.com+{q}&setlang=zh-cn&count=15',
    'weixin':   'https://cn.bing.com/search?q=site%3Amp.weixin.qq.com+{q}&setlang=zh-cn&count=15',
    # v15.1: 7个新增 site:bing 直搜代理（探测后确认有真实结果）
    'csdn':     'https://cn.bing.com/search?q=site%3Acsdn.net+{q}&setlang=zh-cn&count=15',
    'cnblogs':  'https://cn.bing.com/search?q=site%3Acnblogs.com+{q}&setlang=zh-cn&count=15',
    'eastmoney':'https://cn.bing.com/search?q=site%3Aeastmoney.com+{q}&setlang=zh-cn&count=15',
    'cls':      'https://cn.bing.com/search?q=site%3Acls.cn+{q}&setlang=zh-cn&count=15',
    'tencent_cloud': 'https://cn.bing.com/search?q=site%3Acloud.tencent.com+{q}&setlang=zh-cn&count=15',
    'sina_finance':  'https://cn.bing.com/search?q=site%3Afinance.sina.com.cn+{q}&setlang=zh-cn&count=15',
    'sohu':     'https://cn.bing.com/search?q=site%3Asohu.com+{q}&setlang=zh-cn&count=15',
    # v16.1: 5 个 RSS 引擎（不带 query — RSS endpoint 固定）
    # 注：RSS_BASE_URLS 在 _search_http 里特殊处理：q 占位符忽略
    'rss_ithome':  'https://www.ithome.com/rss/?q={q}',
    'rss_36kr':    'https://36kr.com/feed-newsflash?q={q}',
    'rss_sspai':   'https://sspai.com/feed?q={q}',
    'rss_oschina': 'https://www.oschina.net/news/rss?q={q}',
    'rss_woshipm': 'https://www.woshipm.com/feed?q={q}',
}

# ===== Playwright全局单例 =====
_pw = None; _browser = None; _browser_refcount = 0

async def _ensure_browser():
    global _pw, _browser, _browser_refcount
    if not _PLAYWRIGHT_OK:
        raise RuntimeError("playwright 未安装；浏览器引擎 (sogou/baidu/360/weixin) 不可用。请 pip install playwright + playwright install chromium")
    if _browser and _browser.is_connected():
        _browser_refcount += 1; return _browser
    _pw = await async_playwright().start()
    _browser = await _pw.chromium.launch(headless=True, args=[
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox', '--disable-setuid-sandbox',
        '--disable-infobars', '--window-size=1920,1080'])
    _browser_refcount = 1; return _browser

async def _release_browser():
    global _browser_refcount
    _browser_refcount -= 1

async def _cleanup_browser():
    global _pw, _browser, _browser_refcount
    if _browser_refcount > 0: return
    try:
        if _browser: await _browser.close()
    except: pass
    try:
        if _pw: await _pw.stop()
    except: pass
    _browser = _pw = None

_stealth_js = None
def _get_stealth():
    global _stealth_js
    if _stealth_js is None:
        try:
            with open(STEALTH_JS) as f: _stealth_js = f.read()
        except: _stealth_js = '/* stealth unavailable */'
    return _stealth_js

_stealth_context = None
async def _get_context(browser):
    global _stealth_context
    if _stealth_context and not _stealth_context.pages: return _stealth_context
    _stealth_context = await browser.new_context(
        user_agent=USER_AGENT, viewport=VIEWPORT,
        locale='zh-CN', timezone_id='Asia/Shanghai')
    await _stealth_context.add_init_script(_get_stealth())
    return _stealth_context

# ===== SQLite缓存 v13（分桶TTL + 归一化key + 命中率统计） =====
_cache_conn = None
_cache_stats = {'hits': 0, 'misses': 0, 'sets': 0}

# 模式 → TTL（秒）
# news/policy/stock 时效敏感 → 短TTL
# dev/global/deep 引擎组合稳定 → 长TTL
# quick 极速缓存（用户高频同查）→ 中TTL
MODE_TTL = {
    'news':    300,    # 5分钟
    'policy':  600,    # 10分钟
    'stock':   300,    # 5分钟
    'quick':   1800,   # 30分钟
    'dev':     3600,   # 1小时
    'global':  3600,   # 1小时
    'deep':    1800,   # 30分钟
}
DEFAULT_TTL = 1800    # 默认30分钟

def _get_cache_conn():
    global _cache_conn
    if _cache_conn: return _cache_conn
    _cache_conn = sqlite3.connect(CACHE_DB, check_same_thread=False)
    # v13: 加 ttl 列
    _cache_conn.execute('''CREATE TABLE IF NOT EXISTS search_cache (
        id TEXT PRIMARY KEY, created_at REAL NOT NULL,
        engine TEXT NOT NULL, result TEXT NOT NULL, ttl REAL NOT NULL DEFAULT 3600)''')
    _cache_conn.commit(); return _cache_conn

def _normalize_query(q):
    """v13 query归一化：去标点/停用词/空白 → 小写
    目的：让'Python教程'和'python 教程!'和'Python的教程'复用同一缓存
    """
    if not q: return ''
    q = q.lower().strip()
    q = re.sub(r'[\s\-—–_·…\'"，。、：；。！？,.!?;:()（）【】\[\]]+', ' ', q)
    q = re.sub(r'\s+', ' ', q).strip()
    return q

def _cache_key(q, engine, mode, recency, num):
    """v13 key: query归一化 + 不含 num（用大桶复用策略）
    num 单独记录在 result JSON 里（取前N即可）
    """
    qn = _normalize_query(q)
    raw = f"{qn}|{engine or ''}|{mode or ''}|{recency or ''}"
    return hashlib.md5(raw.encode()).hexdigest()

def _cache_get(q, engine, mode, recency, num):
    """v13 缓存读取：分桶TTL + 桶复用（num 不参与 key）"""
    conn = _get_cache_conn()
    key = _cache_key(q, engine, mode, recency, num)
    ttl = MODE_TTL.get(mode or 'deep', DEFAULT_TTL)
    cutoff = time.time() - ttl
    cur = conn.execute('SELECT result, created_at, ttl FROM search_cache WHERE id=? AND created_at>?', (key, cutoff))
    rows = cur.fetchall()
    if rows:
        results = json.loads(rows[0][0])
        results = results[:num]  # 桶复用：num=10 直接从 num=20 桶里取前 10
        age = int(time.time() - rows[0][1])
        _cache_stats['hits'] += 1
        print(f'  [cache] 命中{len(results)}条 (key={key[:8]}.. TTL={int(rows[0][2])}s 剩{age}s前)', file=sys.stderr)
        return results
    _cache_stats['misses'] += 1
    return None

def _cache_set(q, engine, mode, recency, num, results):
    """v13 缓存写入：分桶TTL + 放大 num 写入（max(num, 20)）"""
    if not results: return
    conn = _get_cache_conn()
    key = _cache_key(q, engine, mode, recency, num)
    ttl = MODE_TTL.get(mode or 'deep', DEFAULT_TTL)
    # 桶复用：永远存 max(请求num, 20) 条，让 num=5/8/10 都能复用
    results_to_store = results[:max(num, 20)]
    conn.execute('DELETE FROM search_cache WHERE id=?', (key,))
    conn.execute('INSERT INTO search_cache VALUES (?,?,?,?,?)',
                 (key, time.time(), mode or '_batch', json.dumps(results_to_store, ensure_ascii=False), ttl))
    conn.commit()
    _cache_stats['sets'] += 1
    # 清理过期
    oldest_allowed = time.time() - max(MODE_TTL.values())  # 用最长TTL作清理阈值（保守）
    conn.execute('DELETE FROM search_cache WHERE created_at<?', (oldest_allowed,))

def _cache_stats_report():
    """打印缓存命中率"""
    h, m, s = _cache_stats['hits'], _cache_stats['misses'], _cache_stats['sets']
    total = h + m
    if total == 0 and s == 0: return
    hit_rate = (h / total * 100) if total > 0 else 0
    print(f'  [cache] 命中率 {h}/{total} = {hit_rate:.0f}% · 写入 {s} 次', file=sys.stderr)

# ===== 日期提取 =====
def _extract_date(text):
    m = re.search(r'(\d{4})[年/-](\d{1,2})[月/-](\d{1,2})[日号]?', text)
    if m: return f"{int(m.group(1))}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    m = re.search(r'(\d{4})年(\d{1,2})月', text)
    if m: return f"{int(m.group(1))}-{int(m.group(2)):02d}"
    return ''

# ===== 结果分类 =====
CATEGORIES = {
    'baike.baidu.com':'📖百科','zh.wikipedia.org':'📖百科','wikipedia.org':'📖百科','baike.sogou.com':'📖百科',
    'apple.com':'🏢官方','google.com':'🏢官方','microsoft.com':'🏢官方',
    'gov.cn':'🏛️政府','edu.cn':'🏫教育',
    'zhidao.baidu.com':'💬问答','zhihu.com':'💬问答','quora.com':'💬问答','stackoverflow.com':'💻代码',
    'github.com':'💻代码','gitlab.com':'💻代码','pypi.org':'💻代码',
    'blog.csdn.net':'✍️博客','cnblogs.com':'✍️博客','medium.com':'✍️博客',
    'sina.com.cn':'📰新闻','sohu.com':'📰新闻','163.com':'📰新闻','qq.com':'📰新闻','thepaper.cn':'📰新闻',
    'xinhuanet.com':'📰新闻','people.com.cn':'📰新闻',
    'bilibili.com':'🎬视频','youtube.com':'🎬视频',
    'mp.weixin.qq.com':'💬社交','weixin.qq.com':'💬社交','weibo.com':'💬社交',
    'arxiv.org':'🎓学术','scholar.google.com':'🎓学术',
}

def _classify(r):
    url = r.get('url','').lower()
    for dom, cat in sorted(CATEGORIES.items(), key=lambda x:-len(x[0])):
        if dom in url: r['category']=cat; return cat
    t = r.get('title','')
    if '百科' in t: r['category']='📖百科';return '📖百科'
    if '官网' in t: r['category']='🏢官方';return '🏢官方'
    if '知乎' in t: r['category']='💬问答';return '💬问答'
    if 'GitHub' in t: r['category']='💻代码';return '💻代码'
    if '新闻' in t: r['category']='📰新闻';return '📰新闻'
    r['category']='🔗网页';return '🔗网页'

# ===== 摘要清洗 =====
_NAV_PAT = re.compile(r'[-‒–—]{3,}\s*(相关\w*|推荐|热点|阅读|资讯|链接|文章|新闻|话题|导航|标签)|<[^>]+>')
def _clean_summary(text, title=''):
    if not text: return ''
    text = re.sub(r'<[^>]+>',' ',text).replace('\xa0',' ').replace('\u200b','')
    text = _NAV_PAT.sub('',text)
    if title and len(title)>5:
        tc = re.sub(r'[\s\-—–_"\']','',title)[:20].lower()
        tx = re.sub(r'[\s\-—–_"\']','',text)[:len(tc)].lower()
        if tx.startswith(tc): text=text[len(title):]
        sep = re.search(r'[——\-]{2,}\s*',text)
        if sep and sep.end()<len(text)*0.4: text=text[sep.end():]
    text = re.sub(r'\s+',' ',text).strip()
    return text[:200] if len(text)>200 else text

# ===== HTTP引擎解析器 =====
def _parse_bing_http(html, engine='bing_http'):
    """解析Bing搜索结果（HTTP模式，国际版）"""
    results=[]
    if not BeautifulSoup: return results
    soup=BeautifulSoup(html,'lxml')
    for block in soup.select('li.b_algo, div.b_algo')[:15]:
        a=block.select_one('h2 a, h3 a')
        if not a: continue
        title=_clean_summary(a.get_text(strip=True))
        if len(title)<3: continue
        href=a.get('href','')
        if not href.startswith('http'): continue
        summary=''
        for sel in ['p.b_paratext','div.b_paractx','span.b_paractx']:
            s=block.select_one(sel)
            if s:
                raw=s.get_text()
                if len(raw.strip())>10: summary=_clean_summary(raw,title); break
        if not summary or len(summary)<10:
            texts=[t.strip() for t in block.find_all(string=True,recursive=True) if len(t.strip())>20
                   and t.strip()!=title and not t.strip().startswith('http')]
            for t in texts[:2]:
                cleaned=_clean_summary(t,title)
                if len(cleaned)>10: summary=cleaned; break
        date=_extract_date(title) or _extract_date(summary)
        r=dict(title=title,url=href,summary=summary,date=date,engine=engine,url_type='direct')
        _classify(r); results.append(r)
    return results

def _parse_bing_cn(html):
    """解析Bing中国版搜索结果"""
    return _parse_bing_http(html, engine='bing_cn')

def _parse_github_issues(html_or_json, engine='github_issues'):
    """解析GitHub Issues搜索结果（JSON API）

    GitHub API返回JSON，包含issue/PR混合结果。优先issue，过滤bot批量issue（Renovate等）。
    """
    import json as _json
    results = []
    try:
        data = _json.loads(html_or_json)
    except Exception:
        return results
    items = (data.get('items') or [])[:15]
    bot_logins = {'renovate[bot]','dependabot[bot]','github-actions[bot]','codecov[bot]','sonarcloud[bot]'}
    for it in items:
        user = (it.get('user') or {}).get('login','')
        # 过滤bot批量issue + PR（PR不算"问题讨论"）
        if user in bot_logins: continue
        if it.get('pull_request'): continue
        title = (it.get('title') or '').strip()
        if len(title) < 3: continue
        url = it.get('html_url') or ''
        if not url: continue
        # 摘要：body 截断 + repo 上下文
        body = (it.get('body') or '').strip()
        body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
        body = re.sub(r'\[!\[.*?\]\(.*?\)\]\(.*?\)', '', body)
        body = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', body)
        body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', body)
        body = re.sub(r'#+ ', '', body)
        body = re.sub(r'\s+', ' ', body).strip()
        repo = (it.get('repository_url') or '').rsplit('/', 1)[-1] or ''
        state = it.get('state', '')
        comments = it.get('comments', 0)
        summary = body[:200] if body else f"[{repo}] {state} · {comments} 评论"
        # 日期：updated_at
        date = (it.get('updated_at') or '')[:10]
        labels = [l.get('name','') for l in (it.get('labels') or [])][:3]
        if labels: summary = f"[{','.join(labels)}] {summary}" if summary else f"[{','.join(labels)}]"
        r = dict(
            title=f"[{repo}] {title}" if repo else title,
            url=url, summary=summary, date=date,
            engine=engine, url_type='direct')
        _classify(r)
        results.append(r)
    return results

# ===== HTTP引擎搜索 =====
HTTP_PARSERS = {
    'bing_cn': _parse_bing_cn,
    'bing_http': _parse_bing_http,
    'github_issues': _parse_github_issues,
    # v15: site: 代理复用 bing_cn 解析器（HTML 结构相同）
    'toutiao': _parse_bing_cn,
    'zhihu': _parse_bing_cn,
    'weixin': _parse_bing_cn,
    # v15.1: 7个新增复用 bing_cn 解析器
    'csdn': _parse_bing_cn,
    'cnblogs': _parse_bing_cn,
    'eastmoney': _parse_bing_cn,
    'cls': _parse_bing_cn,
    'tencent_cloud': _parse_bing_cn,
    'sina_finance': _parse_bing_cn,
    'sohu': _parse_bing_cn,
    # v16.1: 5 个 RSS 引擎（v15.1 探针确认 target>0）
    'rss_ithome':  lambda xml, engine='rss_ithome':  _parse_rss(xml, engine),
    'rss_36kr':    lambda xml, engine='rss_36kr':    _parse_rss(xml, engine),
    'rss_sspai':   lambda xml, engine='rss_sspai':   _parse_rss(xml, engine),
    'rss_oschina': lambda xml, engine='rss_oschina': _parse_rss(xml, engine),
    'rss_woshipm': lambda xml, engine='rss_woshipm': _parse_rss(xml, engine),
}

# v16.1: RSS 端点配置（site 字段用于 engine 标签真实）
RSS_ENDPOINTS = {
    'rss_ithome':  ('https://www.ithome.com/rss/',                      'ithome.com'),
    'rss_36kr':    ('https://36kr.com/feed-newsflash',                   '36kr.com'),
    'rss_sspai':   ('https://sspai.com/feed',                            'sspai.com'),
    'rss_oschina': ('https://www.oschina.net/news/rss',                  'oschina.net'),
    'rss_woshipm': ('https://www.woshipm.com/feed',                      'woshipm.com'),
}


def _parse_rss(xml, engine='rss'):
    """v16.1: 通用 RSS 2.0 解析器（无 feedparser 依赖）
    输入: RSS XML 字符串
    输出: [{title, url, summary, date, engine, url_type}, ...]
    限制: 不支持 Atom（这些站点都是 RSS 2.0）
    """
    results = []
    # 提取所有 <item>
    items = re.findall(r'<item[\s>](.*?)</item>', xml, re.DOTALL | re.IGNORECASE)
    site = RSS_ENDPOINTS.get(engine, ('', ''))[1] or ''
    for it in items[:15]:
        # title (支持 CDATA)
        tm = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', it, re.DOTALL)
        title = _clean_summary(tm.group(1).strip()) if tm else ''
        if len(title) < 3: continue
        # link
        lm = re.search(r'<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>', it, re.DOTALL)
        if not lm: lm = re.search(r'<link\s+[^>]*href=[\"\']*(.*?)[\"\']*\s*/?>', it, re.DOTALL)
        href = lm.group(1).strip() if lm else ''
        if href and not href.startswith('http'): continue
        # description / content
        dm = re.search(r'<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>', it, re.DOTALL)
        summary_raw = dm.group(1) if dm else ''
        # 转 HTML 到纯文本
        # 转 HTML 实体到纯文本（&lt; / &gt; / &amp; / &quot; / &#34; / &nbsp;）
        if summary_raw:
            summary_raw = (summary_raw.replace('&lt;', '<').replace('&gt;', '>')
                           .replace('&amp;', '&').replace('&quot;', '"').replace('&#34;', '"')
                           .replace('&nbsp;', ' ').replace('&#39;', "'"))
        summary = _clean_summary(summary_raw, title) if summary_raw else ''
        # pubDate
        pm = re.search(r'<pubDate>(.*?)</pubDate>', it, re.DOTALL)
        date_raw = pm.group(1).strip() if pm else ''
        date = _parse_rss_date(date_raw) or _extract_date(title) or _extract_date(summary)
        r = dict(title=title, url=href, summary=summary or '', date=date,
                 engine=engine, url_type='direct')
        _classify(r)
        # 强制 engine 标签为真实别名
        r['engine'] = engine
        results.append(r)
    return results


def _parse_rss_date(s):
    """RSS pubDate 解析（RFC 822: 'Tue, 03 Jun 2025 12:34:56 +0800'）"""
    if not s: return ''
    m = re.search(r'(\d{1,2})\s+(\w{3})\s+(\d{4})', s)
    if not m: return ''
    months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
              'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    day, mon, year = m.group(1), m.group(2), m.group(3)
    return f'{year}-{months.get(mon,"01")}-{int(day):02d}'

async def _search_http(engine, query, session):
    """单个HTTP引擎搜索（aiohttp，快速直链）"""
    # v16.1: RSS 引擎使用固定 endpoint（忽略 query 参数，只取最新条目后客户端过滤）
    if engine in RSS_ENDPOINTS:
        url = RSS_ENDPOINTS[engine][0]
    else:
        # v16.1: bing_http 按 query 语言动态 setlang；其他引擎无 {lang} 占位符
        lang = 'zh-cn' if re.search(r'[\u4e00-\u9fa5]', query) else 'en'
        if '{lang}' in HTTP_BASE_URLS[engine]:
            url = HTTP_BASE_URLS[engine].format(q=quote(query), lang=lang)
        else:
            url = HTTP_BASE_URLS[engine].format(q=quote(query))
    # GitHub API需要专属请求头（Accept版本 + UA）
    if engine == 'github_issues':
        headers = {
            'User-Agent': USER_AGENT,
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8',
        }
    else:
        headers = {
            'User-Agent': USER_AGENT,
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8',
        }
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15),
                               headers=headers) as resp:
            if resp.status != 200:
                print(f'  [{engine}] HTTP {resp.status}', file=sys.stderr); return engine, []
            # GitHub API返回JSON，其他引擎返回HTML
            if engine == 'github_issues':
                body = await resp.text()
            else:
                body = await resp.text()
            results = HTTP_PARSERS[engine](body)
            # v15: site: 代理过滤非目标域名（保证 engine 标签真实）
            if engine == 'toutiao':
                results = [r for r in results if 'toutiao.com' in r.get('url', '') or 'toutiao.com' in r.get('domain', '')]
                for r in results: r['engine'] = 'toutiao'
            elif engine == 'zhihu':
                results = [r for r in results if 'zhihu.com' in r.get('url', '') or 'zhihu.com' in r.get('domain', '')]
                for r in results: r['engine'] = 'zhihu'
            elif engine == 'weixin':
                results = [r for r in results if 'weixin' in r.get('url', '').lower() or 'mp.weixin.qq.com' in r.get('url', '').lower()]
                for r in results: r['engine'] = 'weixin_bing'  # 区分 weixin_pw
            # v15.1: 7个新增 site: 代理
            elif engine == 'csdn':
                results = [r for r in results if 'csdn.net' in r.get('url', '')]
                for r in results: r['engine'] = 'csdn'
            elif engine == 'cnblogs':
                results = [r for r in results if 'cnblogs.com' in r.get('url', '')]
                for r in results: r['engine'] = 'cnblogs'
            elif engine == 'eastmoney':
                results = [r for r in results if 'eastmoney.com' in r.get('url', '')]
                for r in results: r['engine'] = 'eastmoney'
            elif engine == 'cls':
                results = [r for r in results if 'cls.cn' in r.get('url', '')]
                for r in results: r['engine'] = 'cls'
            elif engine == 'tencent_cloud':
                results = [r for r in results if 'cloud.tencent.com' in r.get('url', '')]
                for r in results: r['engine'] = 'tencent_cloud'
            elif engine == 'sina_finance':
                results = [r for r in results if 'sina.com.cn' in r.get('url', '')]
                for r in results: r['engine'] = 'sina_finance'
            elif engine == 'sohu':
                results = [r for r in results if 'sohu.com' in r.get('url', '')]
                for r in results: r['engine'] = 'sohu'
            # v16.1: RSS 引擎客户端按 query 关键词过滤（RSS endpoint 不带 q）
            elif engine in RSS_ENDPOINTS:
                results = _filter_by_query(results, query, engine)
                for r in results: r['engine'] = engine
            print(f'  [{engine}] {len(results)} 条结果', file=sys.stderr)
            return engine, results
    except Exception as e:
        print(f'  [{engine}] 错误: {type(e).__name__}', file=sys.stderr); return engine, []


def _filter_by_query(results, query, engine):
    """v16.1: RSS 返回所有最新条目，按 query 关键词命中过滤
    策略: 提取 query 中的中英文关键词（去停用词），title/summary 命中任一即保留
    兜底: 关键词全部不命中时取前 5 条（保证 RSS 引擎总能返回结果）
    """
    if not results: return results
    # 中文 2-字 切词 + 英文 3+ 词
    cn = re.findall(r'[\u4e00-\u9fa5]{2,}', query)
    en = re.findall(r'[a-zA-Z]{3,}', query.lower())
    keywords = cn + en
    if not keywords: return results[:5]
    hits = [r for r in results if any(kw.lower() in (r.get('title','')+r.get('summary','')).lower() for kw in keywords)]
    return hits[:10] if hits else results[:5]

# ===== Playwright引擎搜索（保留v10.x的解析器） =====
def _parse_sogou(html):
    results=[]
    if not BeautifulSoup: return results
    soup=BeautifulSoup(html,'lxml')
    for block in soup.select('div.vrwrap')[:15]:
        el=block.select_one('h3.vr-title a, h3 a')
        if not el: continue
        title=_clean_summary(el.get_text(strip=True))
        if len(title)<3: continue
        href=el.get('href','')
        if href and not href.startswith('http'): href='https://www.sogou.com'+href
        summary=''
        for sel in ['p.str-info','div.str-text','div.str_text','div.star-wiki']:
            s=block.select_one(sel)
            if s:
                raw=s.get_text()
                if len(raw.strip())>10: summary=_clean_summary(raw,title); break
        date=_extract_date(title) or _extract_date(summary)
        url_type='redirect' if any(x in href for x in ['sogou.com/link','src=11','sogoucdn.com']) else 'direct'
        r=dict(title=title,url=href,summary=summary or '',date=date,engine='sogou',url_type=url_type)
        _classify(r); results.append(r)
    return results

def _parse_baidu(html):
    results=[]
    if not BeautifulSoup: return results
    soup=BeautifulSoup(html,'lxml')
    for a in soup.select('h3.t a')[:15]:
        title=_clean_summary(a.get_text(strip=True))
        if len(title)<3: continue
        href=a.get('href','')
        if href and not href.startswith('http'): href='https://www.baidu.com'+href
        parent=a.find_parent() or a.parent
        summary=''
        for sel in ['span.c-abstract','div.c-abstract','div.c-span-last']:
            s=parent.select_one(sel)
            if s:
                raw=s.get_text()
                if len(raw.strip())>5:
                    summary=_clean_summary(raw,title)
                    if len(summary)>10: break
        if not summary or len(summary)<10:
            texts=sorted([t.strip() for t in parent.find_all(string=True,recursive=True)
                         if t.strip() and len(t.strip())>15 and '{' not in str(t)
                         and str(t).strip()!=title and not str(t).strip().startswith('http')],
                        key=len,reverse=True)
            for t in texts[:3]:
                cleaned=_clean_summary(str(t),title)
                if len(cleaned)>10: summary=cleaned; break
        date=_extract_date(title) or _extract_date(summary)
        baidu_rp=['baidu.com/link','baidu.com/baidu.php','baidu.com/bbox','baidu.com/c?url','baidu.com/redirect']
        url_type='redirect' if any(p in href.lower() for p in baidu_rp) else 'direct'
        r=dict(title=title,url=href,summary=summary or '',date=date,engine='baidu',url_type=url_type)
        _classify(r); results.append(r)
    return results

def _parse_360(html):
    results=[]
    if not BeautifulSoup: return results
    soup=BeautifulSoup(html,'lxml')
    for block in soup.select('li.res-list, div.res-list, div.result')[:15]:
        a=block.select_one('h3 a, a')
        if not a: continue
        title=_clean_summary(a.get_text(strip=True))
        if len(title)<3: continue
        href=a.get('href','')
        if href and not href.startswith('http'): href='https://www.so.com'+href
        summary=''
        for sel in ['p.str-text','div.str-text','p.des']:
            s=block.select_one(sel)
            if s:
                raw=s.get_text()
                if len(raw.strip())>5: summary=_clean_summary(raw,title)
                if len(summary)>10: break
        if not summary or len(summary)<10:
            texts=sorted([t.strip() for t in block.find_all(string=True,recursive=True)
                         if t.strip() and len(t.strip())>15 and '{' not in str(t)
                         and str(t).strip()!=title and not str(t).strip().startswith('http')],
                        key=len,reverse=True)
            for t in texts[:3]:
                cleaned=_clean_summary(str(t),title)
                if len(cleaned)>10: summary=cleaned; break
        date=_extract_date(title)
        url_type='redirect' if 'so.com/link' in href else 'direct'
        r=dict(title=title,url=href,summary=summary or '',date=date,engine='360',url_type=url_type)
        _classify(r); results.append(r)
    return results

def _parse_weixin(html):
    results=[]
    if not BeautifulSoup: return results
    soup=BeautifulSoup(html,'lxml')
    for block in soup.select('div.txt-box')[:15]:
        h3=block.select_one('h3 a')
        if not h3: continue
        title=_clean_summary(h3.get_text(strip=True))
        if len(title)<3: continue
        href=str(h3.get('href',''))
        if href and not href.startswith('http'): href='https://weixin.sogou.com'+href
        desc=block.select_one('p.txt-info')
        summary=_clean_summary(desc.get_text(strip=True)) if desc else ''
        date_str=''
        date_elem=block.select_one('span.s2') or block.select_one('span[s]')
        if date_elem: date_str=date_elem.get_text(strip=True)
        r=dict(title=title,url=href,summary=summary,date=date_str,engine='weixin',url_type='direct')
        _classify(r); results.append(r)
    return results

PW_PARSERS = {
    'sogou': _parse_sogou, 'baidu': _parse_baidu, '360': _parse_360, 'weixin': _parse_weixin,
}
PW_ENGINE_CFG = {
    'sogou': {'weight': 100, 'captcha_check': lambda h,r: 'seccodeForm' in h or 'antispider' in h},
    'baidu': {'weight': 80, 'captcha_check': lambda h,r: '安全验证' in h or len(h)<10000},
    '360':   {'weight': 60, 'captcha_check': lambda h,r: '验证码' in h or len(h)<10000},
    'weixin':{'weight': 85, 'captcha_check': lambda h,r: '验证' in h or len(h)<3000},
}

async def _search_pw(engine, query, page):
    """单个Playwright引擎搜索"""
    cfg = PW_ENGINE_CFG[engine]
    url = PW_BASE_URLS[engine].format(q=quote(query))
    try:
        await page.goto(url, timeout=20000, wait_until='domcontentloaded')
        await asyncio.sleep(0.5)
        html = await page.content()
        results = PW_PARSERS[engine](html)
        if cfg['captcha_check'](html, results): return engine, []
        return engine, results
    except Exception as e:
        return engine, []

# ===== URL解析（Playwright跳转链） =====
async def _resolve_results(results):
    resolve_slice = results[:8]
    redirect_results = [(i, r) for i, r in enumerate(resolve_slice)
                       if r.get('url_type')=='redirect' and r.get('url')]
    if not redirect_results: return results
    try:
        browser = await _ensure_browser()
        ctx = await _get_context(browser)
        num_pages = min(3, len(redirect_results))
        pages = [await ctx.new_page() for _ in range(num_pages)]
        sem = asyncio.Semaphore(num_pages)
        async def resolve_one(iu):
            async with sem:
                idx, r = iu
                page = pages[idx % num_pages]
                try:
                    await page.goto(r['url'], wait_until='domcontentloaded', timeout=2000)
                    final = page.url
                    if final.startswith('http') and final != r['url']:
                        results[idx]['url'] = final
                        results[idx]['url_type'] = 'direct'
                        results[idx]['resolved'] = True
                except: pass
        await asyncio.gather(*[resolve_one(iu) for iu in redirect_results], return_exceptions=True)
        for p in pages:
            try: await p.close()
            except: pass
    except: pass
    return results

# ===== 语言检测 & 模式配置 =====
_CJK_PAT = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')

def _has_chinese(text):
    return bool(_CJK_PAT.search(text))

# 引擎组
CN_ENGINES = ['sogou', 'baidu', '360', 'weixin', 'bing_cn']
ALL_ENGINES = CN_ENGINES + ['bing_http', 'github_issues']
# v16.1: global mode 中文 query 走 bing_cn+bing_http 双源，英文 query 走纯国际
# 用 _pick_global_engines() 在 search_async 里按 query 动态选择
GLOBAL_ENGINES_ZH = ['bing_cn', 'bing_http']
GLOBAL_ENGINES_EN = ['bing_http']

def _pick_global_engines(query):
    """v16.1: global mode 按 query 语言动态选引擎
    含中文字符 → 加 bing_cn 双源（中文社区 GPT-4 讨论质量高）
    纯英文 → 只走 bing_http (国际)"""
    if re.search(r'[\u4e00-\u9fa5]', query):
        return GLOBAL_ENGINES_ZH
    return GLOBAL_ENGINES_EN

MODES = {
    'deep':    CN_ENGINES,             # 综合：国内+Bing CN
    'quick':   ['sogou'],              # 极速
    'news':    ['sogou', 'baidu', 'weixin', 'bing_cn'],  # 中文新闻+Bing
    'global':  GLOBAL_ENGINES_ZH,       # v16.1: 中文走双源；纯英文在 search_async 里再切
    'policy':  ['baidu', 'sogou', 'bing_cn'],  # 政策研究+Bing
    'stock':   ['sogou', 'baidu', 'weixin', 'bing_cn'],  # 财经+Bing
    'dev':     ['sogou', 'baidu', 'github_issues', 'bing_cn'],  # 开发者向：技术问答+官方源
    # v16.1: 4 个新组合 mode（v15.1 7 引擎 + v16.1 5 RSS 引擎）
    'dev_rss':   ['sogou', 'baidu', 'github_issues', 'bing_cn', 'cnblogs', 'csdn',
                  'rss_ithome', 'rss_36kr', 'rss_sspai', 'rss_oschina', 'rss_woshipm'],
    'tech_news': ['cnblogs', 'csdn', 'rss_ithome', 'rss_36kr', 'rss_sspai', 'rss_oschina'],
    'finance':   ['eastmoney', 'cls', 'sina_finance', 'sohu', 'baidu', 'weixin', 'bing_cn'],  # v16.2.4: 去 RSS, 加 baidu/weixin/bing_cn/sohu 兜底
    'weixin_agg':['weixin', 'sogou', 'cls', 'woshipm'],  # v16.1: weixin (PW+HTTP双源) + sogou + cls + woshipm
}

# HTTP引擎权重 & 权威性评分
HTTP_ENGINE_WEIGHTS = {'bing_cn': 85, 'bing_http': 70, 'github_issues': 80}
DOMAIN_AUTHORITY = {
    'gov.cn': 20, 'edu.cn': 20,
    'github.com': 15, 'arxiv.org': 20,
    'thepaper.cn': 15, 'xinhuanet.com': 18, 'people.com.cn': 18,
    'cctv.com': 18, 'news.cn': 18, 'sina.com.cn': 12,
    'sohu.com': 8, '163.com': 8, 'qq.com': 8,
    'stcn.com': 15, 'cls.cn': 15, 'eastmoney.com': 15,
    'zhihu.com': 10, 'bilibili.com': 8,
    'csdn.net': 8, 'cnblogs.com': 8, 'stackoverflow.com': 12,
    'medium.com': 10, 'wikipedia.org': 18,
    'mp.weixin.qq.com': 5,
}

def _get_domain_authority(url):
    url_l = url.lower().replace('https://','').replace('http://','')
    for dom, score in sorted(DOMAIN_AUTHORITY.items(), key=lambda x:-len(x[0])):
        if dom in url_l: return score
    return 0

def _normalize_title(s):
    """归一化标题：去标点/空白/括号内容（移除"官方"、"中文版"等噪声），统一小写"""
    s = s.lower()
    s = re.sub(r'[\(\[【][^\)\]】]*[\)\]】]', '', s)  # 去括号内容
    s = re.sub(r'[【】\[\]（）()《》<>「」『』]', '', s)
    s = re.sub(r'[\s\-—–_·…\'"，。、：；。！？,.!?;:]+', '', s)
    return s

# 中文停用词（去噪声，提高主题词权重）
_STOPWORDS = set('的了是在我你他她它这那和与及或而把被将从为对到于上下来年月日时秒万亿千百十个把被给让使由自从向朝着对于关于')

def _topic_key(s, n=8):
    """提取主题词key：归一化 → 去停用词 → 取前n字符
    例："5月25日A股三大指数集体高开超4400股上涨" → "5月25日a股三大指数集体高开超4400股"
    """
    s = _normalize_title(s)
    # 去停用词（按字符级）
    s = ''.join(c for c in s if c not in _STOPWORDS)
    return s[:n]

def _title_bigrams(s, n=2):
    """生成字符n-gram集合（用于Jaccard相似度）"""
    s = _normalize_title(s)
    if len(s) < n: return {s}
    return {s[i:i+n] for i in range(len(s)-n+1)}

def _title_similarity(a, b, n=2):
    """Jaccard相似度：基于字符n-gram"""
    ba, bb = _title_bigrams(a, n), _title_bigrams(b, n)
    if not ba or not bb: return 0.0
    return len(ba & bb) / len(ba | bb)

def _domain_of(url):
    """提取URL的注册域名（去www./子路径/query）"""
    try:
        from urllib.parse import urlparse
        u = urlparse(url if url.startswith('http') else 'http://'+url)
        host = u.netloc.lower()
        if host.startswith('www.'): host = host[4:]
        # 二级域名合并：xinhua.com.cn / news.cn 保留末两段
        parts = host.split('.')
        if len(parts) >= 2:
            return '.'.join(parts[-2:])
        return host
    except: return ''

def _dedup_v2(all_results, recency=None, sim_threshold=0.5):
    """v12.2 去重 + 排序智能：
    1. 主题词key合并（停用词过滤后前N字符，召回同一事件不同表述）
    2. Jaccard 二次校验（避免误合并）
    3. 跨源/跨引擎聚合（cross_verified加权）
    """
    weights = {}
    for e in PW_ENGINE_CFG: weights[e] = PW_ENGINE_CFG[e]['weight']
    for e in HTTP_ENGINE_WEIGHTS: weights[e] = HTTP_ENGINE_WEIGHTS[e]

    # 第一步：算基础分 + 主题key
    scored = []
    for r in all_results:
        score = weights.get(r['engine'], 50)
        score += _get_domain_authority(r.get('url',''))
        if r.get('summary'): score += 15
        if r.get('date'):
            score += 10
            try:
                dt = datetime.strptime(r['date'][:10], '%Y-%m-%d')
                days = (datetime.now() - dt).days
                if days <= 0: score += 20
                elif days <= 7: score += 20 - int((days/7)*15)
                elif days <= 30: score += 5
                elif days <= 90: score += 2
            except: pass
        r['score'] = score
        r['cross_verified'] = 0
        r['domain'] = _domain_of(r.get('url',''))
        r['topic_key'] = _topic_key(r.get('title',''), n=10)
        scored.append(r)

    # 第二步：合并 — 主题key完全相同 OR Jaccard > 阈值
    clusters = []  # [member_indices]
    used = [False] * len(scored)
    for i, r in enumerate(scored):
        if used[i]: continue
        cluster = [i]
        used[i] = True
        for j in range(i+1, len(scored)):
            if used[j]: continue
            # 条件1：主题key相同（精确合并同一事件）
            if r['topic_key'] and r['topic_key'] == scored[j]['topic_key']:
                cluster.append(j); used[j] = True
                continue
            # 条件2：Jaccard 相似（兜底）
            sim = _title_similarity(r['title'], scored[j]['title'])
            if sim >= sim_threshold:
                cluster.append(j); used[j] = True
        clusters.append(cluster)

    # 第三步：每个簇选代表 + 聚合
    unique = []
    cluster_id = 0
    for cluster in clusters:
        members = [scored[k] for k in cluster]
        members.sort(key=lambda x: -x['score'])
        rep = dict(members[0])
        domains = set(m['domain'] for m in members if m['domain'])
        engines = set(m['engine'] for m in members)
        rep['cross_verified'] = max(0, len(domains) - 1) + max(0, len(engines) - 1)
        rep['score'] += rep['cross_verified'] * 10
        if len(domains) >= 3: rep['score'] += 15
        elif len(domains) == 2: rep['score'] += 8
        # 摘要：保留最长的
        best_summary = max((m.get('summary','') for m in members), key=len)
        if best_summary: rep['summary'] = best_summary
        rep['source_count'] = len(domains)
        rep['source_engines'] = ','.join(sorted(engines))
        rep['cluster_size'] = len(members)
        rep['cluster_id'] = cluster_id
        cluster_id += 1
        unique.append(rep)

    unique.sort(key=lambda x: -x['score'])
    if recency:
        day_map = {'day':1,'week':7,'month':30,'year':365}
        max_d = day_map.get(recency, 30)
        unique = [r for r in unique if (not r.get('date') or _days_since(r['date'][:10]) <= max_d)]
    return unique

def _dedup(all_results, recency=None):
    weights = {}
    for e in PW_ENGINE_CFG: weights[e] = PW_ENGINE_CFG[e]['weight']
    for e in HTTP_ENGINE_WEIGHTS: weights[e] = HTTP_ENGINE_WEIGHTS[e]
    seen = set(); unique = []
    for r in all_results:
        key = re.sub(r'[\s\-—–_·…\'"，。、：；。！？【】（）()]+','',r['title'])[:25].lower()
        if key in seen: continue
        seen.add(key)
        score = weights.get(r['engine'], 50)
        score += _get_domain_authority(r.get('url',''))
        if r.get('summary'): score += 15
        if r.get('date'):
            score += 10
            try:
                dt = datetime.strptime(r['date'][:10], '%Y-%m-%d')
                days = (datetime.now() - dt).days
                if days <= 0: score += 20
                elif days <= 7: score += 20 - int((days/7)*15)
                elif days <= 30: score += 5
                elif days <= 90: score += 2
            except: pass
        r['cross_verified'] = 0; r['score'] = score; unique.append(r)
    unique.sort(key=lambda x:-x['score'])
    for i, a in enumerate(unique):
        for j, b in enumerate(unique):
            if i != j and a['engine'] != b['engine']:
                ka = re.sub(r'[\s\-—–]+','',a['title'])[:20].lower()
                kb = re.sub(r'[\s\-—–]+','',b['title'])[:20].lower()
                if ka == kb or (len(ka)>10 and ka in b['title'].lower()):
                    a['cross_verified'] += 1; a['score'] += 15
    unique.sort(key=lambda x:-x['score'])
    if recency:
        day_map = {'day':1,'week':7,'month':30,'year':365}
        max_d = day_map.get(recency, 30)
        unique = [r for r in unique if (not r.get('date') or _days_since(r['date'][:10]) <= max_d)]
    return unique

def _days_since(d):
    try: return (datetime.now() - datetime.strptime(d[:10],'%Y-%m-%d')).days
    except: return 999

# ===== 主搜索函数 =====
async def search_async(query, engine=None, num=10, mode='deep', resolve_urls=True, recency=None, exact=False, sources=None, force_refresh=False):
    # v17.2: 默认用原 query, 智能识别时改写
    query_for_search = query

    # v14 增量追加：force_refresh 绕过缓存，拿到新结果后由调用方合并
    if not force_refresh:
        cached = _cache_get(query_for_search, engine, mode, recency, num)
        if cached is not None:
            print(f'  [cache] 命中{len(cached)}条，跳过搜索', file=sys.stderr)
            return cached[:num]

    # v16.2.2: 智能识别 — query 含财经词自动用 finance 引擎 (优先于 mode)
    engines = CN_ENGINES  # 默认 fallback, 下面会覆盖
    if not engine and not sources:
        stock_kw = ('股票', '股价', '股市', 'A股', 'a股', '大盘', '上证', '深证', '沪深',
                    '港股', '美股', '纳斯达克', '道琼斯', '标普', '基金',
                    '行情', '涨停', '跌停', '个股', '板块',
                    '开盘', '收盘', '今日股价', '今日行情', '今天股票', '今天股市',
                    '基金净值', 'etf', 'ETF', '指数', '成份股', '龙虎榜',
                    '财经', '股价', '市值', '财报')
        if any(kw in query for kw in stock_kw):
            engines = MODES.get('finance', CN_ENGINES)  # v16.2.2: stock 实际是 news, 用 finance
            print(f'  [smart→finance] 命中财经关键词, 强制用 finance 引擎', file=sys.stderr)
            _used_smart = True
            # v17.2: 如果 query 没含"行情/股价"等, 追加 "行情" 让搜索引擎返回实时报价页而非新闻
            if not any(w in query for w in ('行情', '股价', '收盘', '开盘', '实时', '今日')):
                query_for_search = query + ' 行情'
            else:
                query_for_search = query
        else:
            _used_smart = False
            query_for_search = query
    else:
        _used_smart = False
        query_for_search = query

    # ... (下面要替换 search 用的 query 为 query_for_search)

    # 确定引擎列表
    if engine:
        engines = [engine]
    elif not _used_smart and mode:
        engines = MODES.get(mode, MODES['deep'])
        # v16.1: global mode 动态语言路由（中文加 bing_cn 双源；纯英文只 bing_http）
        if mode == 'global':
            engines = _pick_global_engines(query)
    elif not _used_smart and not mode:
        # 语言感知路由 (只有 _used_smart=False 才走这里)
        if _has_chinese(query):
            engines = CN_ENGINES  # 中文查询：国内+Bing CN（HTTP）
        else:
            engines = GLOBAL_ENGINES_EN  # v16.1: 纯国际（删 GLOBAL_ENGINES）
    # else: _used_smart=True, engines 已在上面 smart 分支设置好, 保留

    engines = [e for e in engines if e in PW_BASE_URLS or e in HTTP_BASE_URLS]
    pw_engines = [e for e in engines if e in PW_BASE_URLS]
    http_engines = [e for e in engines if e in HTTP_BASE_URLS]

    start = time.time()
    all_results = []

    # 1) HTTP引擎搜索（aiohttp，无需浏览器）
    if http_engines:
        async with aiohttp.ClientSession() as session:
            http_tasks = [_search_http(e, query_for_search, session) for e in http_engines]
            http_results = await asyncio.gather(*http_tasks, return_exceptions=True)
            for eng, results in http_results:
                if results:
                    all_results.extend(results)

    # 2) Playwright引擎搜索 (v16.2: 优雅降级 - 系统库缺失/lockfile 失败不阻断)
    browser = None
    ctx = None
    if pw_engines:
        try:
            browser = await _ensure_browser()
            ctx = await _get_context(browser)
        except Exception as e:
            print(f'  [pw] 浏览器启动失败: {e}，跳过 {len(pw_engines)} 个 playwright 引擎', file=sys.stderr)
            pw_engines = []  # 全部跳过
    if pw_engines and ctx is not None:
        # v14 fix: 容错 new_page 失败（context 偶发被 close）
        pw_pages = []
        for _ in pw_engines:
            try:
                pw_pages.append(await ctx.new_page())
            except Exception as e:
                print(f'  [pw] new_page 失败: {e}，跳过该引擎', file=sys.stderr)
                pw_pages.append(None)
        # 只对成功 new_page 的引擎跑任务
        active = [(e, p) for e, p in zip(pw_engines, pw_pages) if p is not None]
        pw_tasks = [_search_pw(e, query_for_search, p) for e, p in active]
        pw_results = await asyncio.gather(*pw_tasks, return_exceptions=True) if pw_tasks else []
        for p in pw_pages:
            if p is None: continue
            try: await p.close()
            except: pass
        for eng, results in pw_results:
            if results:
                print(f'  [{eng}] {len(results)} 条结果', file=sys.stderr)
                all_results.extend(results)
            elif results is not None:
                print(f'  [{eng}] 被拦截', file=sys.stderr)
        await _release_browser()
        await _cleanup_browser()

    results = all_results

    # v16.2.4: finance 模式兜底 — 如果 5 个 finance 引擎 < 3 条, 自动补 sogou/baidu/weixin (中文财经兜底)
    if _used_smart and len(results) < 3:
        print(f'  [finance-fallback] 触发: 当前 {len(results)} 条 < 3, 加跑 sogou/baidu/weixin/bing_cn', file=sys.stderr)
        async with aiohttp.ClientSession() as session:
            fb_engines = ('sogou', 'baidu', 'weixin', 'bing_cn')
            fb_tasks = [_search_http(e, query_for_search, session) for e in fb_engines]
            fb_raw = await asyncio.gather(*fb_tasks, return_exceptions=True)
            # type: ignore[union-attr]  # fb_raw elements are (str, list) or Exception
            for item in fb_raw:
                if isinstance(item, BaseException):
                    continue
                if not item:
                    continue
                eng, r = item  # type: ignore[misc]
                if r:
                    results.extend(r)
                    print(f'  [{eng}] 兜底 +{len(r)} 条', file=sys.stderr)

    # URL解析
    if resolve_urls:
        results = await _resolve_results(results)

    # 去重排序（v12.2: 智能去重 + 跨源聚合）
    results = _dedup_v2(results, recency)
    elapsed = time.time() - start
    print(f'  [{int(elapsed)}s] 合计{len(results)}条', file=sys.stderr)
    _cache_stats_report()  # v13 缓存命中率报告

    # 精确匹配
    if exact and query:
        q_l = query.lower()
        results = [r for r in results if q_l in r.get('title','').lower()]
    if sources:
        results = [r for r in results if r.get('engine') in sources]

    # v14 增量追加：force_refresh 模式 — 与历史 cache 合并
    if force_refresh and not engine:
        try:
            old = _cache_get(query, None, mode, recency, 30) or []
            if old:
                seen_urls = set()
                merged = []
                # 新结果在前（标 refresh=True），历史结果在后（标 refresh=False）
                for r in results:
                    u = r.get('url', '')
                    if u and u not in seen_urls:
                        seen_urls.add(u); r['refresh'] = True; merged.append(r)
                for r in old:
                    u = r.get('url', '')
                    if u and u not in seen_urls:
                        seen_urls.add(u); r['refresh'] = False; merged.append(r)
                results = merged[:max(num, 30)]
                new_count = sum(1 for r in results if r.get('refresh'))
                print(f'  [增量] 新{new_count}条 + 历史{len(results)-new_count}条 = {len(results)}条', file=sys.stderr)
        except Exception as e:
            print(f'  [增量] 合并失败: {e}', file=sys.stderr)

    _cache_set(query, engine, mode, recency, num, results)
    return results[:num]

# ===== CLI =====
def main():
    p = argparse.ArgumentParser(description='Star Search v11.0 - Hybrid HTTP+Playwright')
    all_engine_names = sorted(set(list(PW_BASE_URLS.keys()) + list(HTTP_BASE_URLS.keys())))
    p.add_argument('query', nargs='?', help='搜索关键词')
    p.add_argument('--engine', choices=all_engine_names)
    p.add_argument('--mode', choices=list(MODES.keys()) + ['gl'], default=None,
                   help='搜索模式（默认：语言感知自动路由）')
    p.add_argument('--recency', choices=['day','week','month','year'])
    p.add_argument('--exact', action='store_true', help='精确匹配')
    p.add_argument('--sources', type=str, help='逗号分隔限定来源引擎')
    p.add_argument('--json', action='store_true')
    p.add_argument('--top', type=int, default=10)
    p.add_argument('--list', action='store_true')
    p.add_argument('--no-resolve', action='store_true', help='禁用URL解析')
    p.add_argument('--explain', action='store_true', help='v16: 调试模式，显示每条结果的评分构成与跨源验证详情')
    args = p.parse_args()

    if args.list:
        print('引擎:', ', '.join(all_engine_names))
        print('HTTP:', ', '.join(HTTP_BASE_URLS.keys()))
        print('Playwright:', ', '.join(PW_BASE_URLS.keys()))
        print('模式:', ', '.join(MODES.keys()))
        return

    if not args.query:
        p.print_help(); return

    resolve = not args.no_resolve
    sources = None
    if args.sources:
        sources = [s.strip() for s in args.sources.split(',') if s.strip() in all_engine_names]
        if not sources:
            print('⚠️ --sources 无效，可用: ' + ', '.join(all_engine_names), file=sys.stderr); return
    results = asyncio.run(search_async(
        args.query, engine=args.engine, num=args.top,
        mode=args.mode, resolve_urls=resolve, recency=args.recency,
        exact=args.exact, sources=sources))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f'📊 {len(results)} 条结果')
        for i, r in enumerate(results, 1):
            d = f' [{r["date"]}]' if r.get('date') else ''
            e = f' ({r["engine"]})'
            c = f' {r.get("category","🔗网页")}'
            # v16: 质量标识 — 跨源/跨引擎越多越可信
            cv = r.get('cross_verified', 0) or 0
            if cv >= 3:   badge = ' 🌟🌟🌟'
            elif cv >= 2: badge = ' 🌟🌟'
            elif cv >= 1: badge = ' 🌟'
            else:         badge = ''
            cross = badge if cv > 0 else ''
            # v16: 总评分后缀（透明度）
            score = r.get('score')
            score_str = f' [score={score:.0f}]' if isinstance(score, (int, float)) else ''
            print(f'{i}. {r["title"]}{d}{e}{c}{cross}{score_str}')
            print(f'   {r["url"][:100]}')
            if r.get('summary'): print(f'   {r["summary"][:150]}')
            # v16: --explain 调试模式 — 显示评分构成
            if args.explain:
                expl_parts = []
                if r.get('date'):
                    expl_parts.append('date_score')
                if r.get('url_type') == 'direct':
                    expl_parts.append('direct_url')
                cv = r.get('cross_verified', 0) or 0
                if cv > 0:
                    expl_parts.append(f'cross_verified=+{cv*10}')
                da = _get_domain_authority(r.get('url',''))
                if da:
                    expl_parts.append(f'domain_auth=+{da}')
                expl_parts.append(f'total={r.get("score", 0):.0f}')
                if r.get('resolved'):
                    expl_parts.append('resolved=true')
                sep = ' · '
                print('   📊 ' + sep.join(expl_parts))

if __name__ == '__main__':
    main()
