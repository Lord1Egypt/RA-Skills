#!/usr/bin/env python3
"""v20.41 学术 / 代码检索 - 简化版 (curl subprocess)"""
import subprocess, json, asyncio, re, urllib.parse
from concurrent.futures import ThreadPoolExecutor

_executor = ThreadPoolExecutor(max_workers=4)

def _curl(url, headers=None, timeout=5):
    cmd = ['curl', '-sS', '-m', str(timeout), '--max-redirs', '3']
    if headers:
        for h in headers.items():
            cmd += ['-H', f'{h[0]}: {h[1]}']
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout+1)
        # v20.47: SSE chunked stream 即使 timeout (rc=28) 也有数据, 不检查 returncode
        if r.stdout:
            try:
                return r.stdout.decode('utf-8', errors='ignore')
            except Exception:
                return r.stdout.decode('latin-1', errors='ignore')
    except Exception:
        pass
    return ''

async def _curl_async(url, headers=None, timeout=5):
    """v20.41 v2: 真正支持 timeout (wait_for 包裹 executor task)"""
    loop = asyncio.get_event_loop()
    try:
        task = loop.run_in_executor(_executor, _curl, url, headers, timeout)
        return await asyncio.wait_for(task, timeout=timeout + 0.5)
    except asyncio.TimeoutError:
        return ''
    except Exception:
        return 

def _strip_html(s):
    return re.sub(r'<[^>]+>', ' ', s).strip()

async def search_scholar(query, num=10):
    url = f"https://scholar.google.com/scholar?q={urllib.parse.quote(query)}&hl=zh-CN&num={num}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/<server-ip> Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    html = await _curl_async(url, headers, timeout=4)
    if not html:
        return []
    results = []
    pattern = r'<h3[^>]*class="gs_rt"[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
    for m in re.finditer(pattern, html, re.DOTALL):
        url = m.group(1)
        title = _strip_html(m.group(2))[:120]
        if not title or len(title) < 5 or 'javascript' in url:
            continue
        results.append({
            'title': title,
            'url': url if url.startswith('http') else 'https://scholar.google.com' + url,
            'summary': '',
            'engine': 'scholar',
            'category': 'scholar',
            'date': '',
        })
        if len(results) >= num:
            break
    return results

async def search_semantic_scholar(query, num=10):
    # v20.47: 加 x-api-key header 解限流 (官方 1 req/s 无限流, 无 token 5 req/5min 限流)
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(query)}&limit={num}&fields=title,abstract,authors,year,url,citationCount"
    headers = {'x-api-key': _SS_TOKEN} if _SS_TOKEN else None
    text = await _curl_async(url, headers=headers, timeout=4)
    if not text:
        return []
    try:
        data = json.loads(text)
    except Exception:
        return []
    results = []
    for p in data.get('data', []):
        title = p.get('title', '')
        abstract = p.get('abstract', '') or ''
        year = p.get('year', '')
        authors = ', '.join([a.get('name', '') for a in (p.get('authors') or [])[:3]])
        if not title:
            continue
        summary = f"{authors} ({year}) | cited: {p.get('citationCount', 0)}"
        if abstract:
            summary += f" | {abstract[:150]}"
        results.append({
            'title': title,
            'url': p.get('url') or f"https://www.semanticscholar.org/paper/{p.get('paperId', '')}",
            'summary': summary,
            'engine': 'semantic_scholar',
            'category': 'semantic_scholar',
            'date': str(year) if year else '',
        })
    return results



async def search_openalex(query, num=10):
    """v20.104: OpenAlex 免密钥学术搜索 (覆盖 200M+ 论文, 按引用量排序)"""
    url = f"https://api.openalex.org/works?search={urllib.parse.quote(query)}&per_page={num}"
    headers = {
        'User-Agent': 'star-search/1.0 (mailto:lizhe@users.noreply.github.com)',
        'Accept': 'application/json',
    }
    text = await _curl_async(url, headers=headers, timeout=8)
    if not text: return []
    try: data = json.loads(text)
    except: return []
    results = []
    for w in data.get('results', []) or []:
        title = w.get('title') or w.get('display_name') or ''
        if not title: continue
        pub_date = w.get('publication_date') or ''
        year = pub_date[:4] if pub_date else ''
        authors = ', '.join([
            (a.get('author', {}) or {}).get('display_name') or '?'
            for a in (w.get('authorships') or [])[:3]
        ])
        cited = w.get('cited_by_count', 0)
        doi = w.get('doi') or ''
        primary_loc = (w.get('primary_location') or {}).get('source') or {}
        url_out = primary_loc.get('homepage_url') or doi or w.get('id', '')
        oa = w.get('open_access') or {}
        oa_url = oa.get('oa_url') if isinstance(oa, dict) else None
        if oa_url: url_out = oa_url
        elif not url_out: url_out = w.get('id', '')
        summary = f'{authors} ({year}) | cited: {cited}'
        aii = w.get('abstract_inverted_index') or {}
        if aii:
            pos2w = {}
            for wd, pns in aii.items():
                for p in pns:
                    pos2w[p] = wd
            if pos2w:
                abstr = ' '.join(pos2w[k] for k in sorted(pos2w.keys()))
                if abstr: summary += f' | {abstr[:180]}'
        results.append({
            'title': title[:120],
            'url': url_out,
            'summary': summary,
            'engine': 'openalex',
            'category': 'openalex',
            'date': pub_date,
        })
    return results


async def search_crossref(query, num=10):
    """v20.104: CrossRef 免密钥学术搜索 (覆盖期刊 DOI, 按相关度排序)"""
    url = f"https://api.crossref.org/works?query={urllib.parse.quote(query)}&rows={num}"
    headers = {
        'User-Agent': 'star-search/1.0 (mailto:lizhe@users.noreply.github.com)',
        'Accept': 'application/json',
    }
    text = await _curl_async(url, headers=headers, timeout=8)
    if not text: return []
    try: data = json.loads(text)
    except: return []
    items = (data.get('message') or {}).get('items', []) or []
    results = []
    for w in items:
        title = (w.get('title') or [''])[0] or ''
        if not title: continue
        date_parts = ((w.get('issued') or {}).get('date-parts') or [[None]])[0]
        year = date_parts[0] if date_parts else None
        authors = ', '.join([
            (a.get('family', '?') + ' ' + (a.get('given', '?')[:1] + '.'))
            for a in (w.get('author') or [])[:3]
        ])
        cited = w.get('is-referenced-by-count', 0)
        doi = w.get('DOI', '')
        url_out = w.get('URL', '') or (f'https://doi.org/{doi}' if doi else '')
        summary = f'{authors} ({year}) | cited: {cited}'
        abstr = w.get('abstract', '') or ''
        if abstr:
            abstr_clean = re.sub(r'<[^>]+>', '', abstr).strip()
            if abstr_clean: summary += f' | {abstr_clean[:180]}'
        results.append({
            'title': title[:120],
            'url': url_out,
            'summary': summary,
            'engine': 'crossref',
            'category': 'crossref',
            'date': str(year) if year else '',
        })
    return results

async def search_grep_app(query, num=10):
    url = f"https://grep.app/api/search?q={urllib.parse.quote(query)}"
    text = await _curl_async(url, timeout=4)
    if not text:
        return []
    try:
        data = json.loads(text)
    except Exception:
        return []
    results = []
    for hit in (data.get('hits') or {}).get('nodes', [])[:num]:
        repo = hit.get('repo', {})
        repo_raw = repo.get('raw', '/')
        path = hit.get('path', {}).get('raw', '/')
        content = hit.get('content', {}).get('raw', '')[:200]
        results.append({
            'title': f"{repo_raw.split('/')[-1]}/{path}",
            'url': f"https://grep.app/search?q={urllib.parse.quote(query)}",
            'summary': content,
            'engine': 'grep_app',
            'category': 'grep_app',
            'date': '',
        })
    return results

async def search_sourcegraph(query, num=10):
    # v20.47: GET 真实返回 SSE (POST 404), matchCount 在 progress 事件
    url = f"https://sourcegraph.com/.api/search/stream?q={urllib.parse.quote(query)}&v=V3"
    headers = {'User-Agent': 'Mozilla/5.0'}
    text = await _curl_async(url, headers, timeout=6)
    if not text:
        return []
    results = []
    # v20.47: SSE 格式 = "event: TYPE\ndata: [JSON]\n\n"
    # 解析: 找到所有 'data: ' 行, 剥前缀, json.loads
    data_lines = []
    for line in text.split('\n'):
        if line.startswith('data: '):
            data_lines.append(line[6:])  # 剥 'data: ' 前缀
    for data_str in data_lines:
        try:
            d = json.loads(data_str)
        except Exception:
            continue
        # v20.47: 取所有含 'repository' 字段的 dict
        # filters array / progress dict / matches array of dict
        if isinstance(d, list):
            for item in d:
                if isinstance(item, dict) and item.get('repository'):
                    line_matches = item.get('lineMatches') or []
                    if line_matches:
                        content = line_matches[0].get('line', '')[:200]
                    else:
                        content = item.get('content', '')[:200]
                    repo = item.get('repository', '')
                    path = item.get('path', '')
                    results.append({
                        'title': f"{repo.split('/')[-1]}/{path}" if repo and path else repo or path,
                        'url': f"https://sourcegraph.com/{repo}/-/blob/{path}" if repo and path else '',
                        'summary': content,
                        'engine': 'sourcegraph',
                        'category': 'sourcegraph',
                        'date': '',
                    })
                    if len(results) >= num:
                        return results
        elif isinstance(d, dict) and d.get('repository'):
            line_matches = d.get('lineMatches') or []
            content = line_matches[0].get('line', '')[:200] if line_matches else d.get('content', '')[:200]
            repo = d.get('repository', '')
            path = d.get('path', '')
            results.append({
                'title': f"{repo.split('/')[-1]}/{path}" if repo and path else repo or path,
                'url': f"https://sourcegraph.com/{repo}/-/blob/{path}" if repo and path else '',
                'summary': content,
                'engine': 'sourcegraph',
                'category': 'sourcegraph',
                'date': '',
            })
            if len(results) >= num:
                return results
    return results

ACADEMIC_KW = ['paper', '论文', '研究', 'research', 'arxiv', 'scholar', 'journal', '会议', 'proceedings', 'survey', 'review', 'study']
CODE_KW = ['code', '代码', 'function', '函数', 'class', 'method', 'implementation', 'source', '开源', 'github', 'git', '如何实现', 'how to implement']

def detect_query_mode(query):
    q_lower = query.lower()
    academic_score = sum(1 for kw in ACADEMIC_KW if kw in q_lower)
    code_score = sum(1 for kw in CODE_KW if kw in q_lower)
    if academic_score > code_score and academic_score >= 1:
        return 'academic'
    if code_score > academic_score and code_score >= 1:
        return 'code'
    return 'general'

async def run_academic(query, num=10):
    """shi-zhan 104: add openalex + crossref, 4 engines parallel + dedup"""
    tasks = [
        search_scholar(query, num),
        search_semantic_scholar(query, num),
        search_openalex(query, num),
        search_crossref(query, num),
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    out = []
    seen = set()
    for r in results:
        if isinstance(r, list):
            for item in r:
                key = (item.get("title", "") or "")[:60].lower().strip()
                if key and key in seen:
                    continue
                if key:
                    seen.add(key)
                out.append(item)
    return out


async def run_code(query, num=10):
    tasks = [search_grep_app(query, num), search_sourcegraph(query, num)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    out = []
    for r in results:
        if isinstance(r, list):
            out.extend(r)
    return out
