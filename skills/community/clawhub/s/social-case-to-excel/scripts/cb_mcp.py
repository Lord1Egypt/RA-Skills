#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cb_mcp.py —— 社媒案例库的默认数据源客户端：Reddit MCP（claudebaby 通道）。

零依赖（stdlib urllib），既当命令行工具用，也被 01~04_fetch*.py `import` 调用。

服务端只暴露 3 个工具（2026-09-24 实测）：
  reddit_search_posts     在**指定 subreddit 内**按关键词 + 相对天数窗搜帖（required: subreddit, query）
  reddit_get_thread       取单个帖的评论树（required: post_id；top_n 可选）
  reddit_search_comments  按关键词搜评论 —— **实测恒空，按不可用处理**（评论走 posts → thread 逐帖）

凭证不在本文件里。解析顺序：
  1. 环境变量 REDDIT_MCP_URL / REDDIT_MCP_TOKEN
  2. ~/.clacky/mcp.json → mcpServers.claudebaby-reddit（url + headers.Authorization）

用法（PTY 友好，单行）：
  python3 cb_mcp.py tools                              # 列工具与参数
  python3 cb_mcp.py ping                               # 连通性自检
  python3 cb_mcp.py posts --subreddit AmazonFBA --query "case study" --days 365 --limit 300 --out /tmp/p.json
  python3 cb_mcp.py thread --post-id 1nqx17e --top-n 200 --out /tmp/t.json
  python3 cb_mcp.py call reddit_search_posts '{"subreddit":"ecommerce","query":"revenue","days":30,"limit":5}'

硬约束（改抓取脚本前必读，全部是实测踩出来的）：
  * 返回形状**统一为对象**：{"endpoint":…, "rows":[…], "count":N, "cursor":null}。
    数据只认 `rows`；`count` 是本次返回条数、**不是**总命中数；`cursor` 恒为 null →
    **服务端没有可用分页**，一个 (subreddit, query, days) 组合一次最多 `limit` 条，超了就丢。
  * `limit` 合法区间 1–300（>300 报 invalid_request）→ 本脚本自动截断并告警。
  * 排序 = **oldest first**。要"取最近 N 条"必须把 limit 放大到覆盖窗口内**全部**命中，
    否则会静默丢掉最新那段。命中触顶（rows == limit）时本脚本在落盘里打 `truncated: true`。
  * 时间参数**只有相对 `days`**，没有 after/before 绝对日期。
  * **本机代理约 30s 硬超时，且是静默失败**：返回 HTTP 200 + 空 body，或
    {"error":"Request timed out"}；服务端仍在后台跑完并落缓存 → 正确姿势是
    **原样重发同一请求一次**（缓存预热，通常 1–2s 返回）。**不要改参数**，改任何参数都是
    新的 cache key，会重新冷跑再超时。
  * `post_id` 传错**不报错**，会拿到 id 空间邻近帖的评论 → get_thread 的结果必须校验
    `row.link_id == "t3_"+post_id`（本脚本 norm_comment 已做；调用方可再核一次）。
  * `subreddit:"all"` 不报错但恒空（**无全站搜索**）；不存在的 subreddit 不报错、直接挂到超时。
  * **"0 条"有两种含义，必须看 status 区分**：status=error 是**取数失败，不是"无数据"**，
    照原样重试；status=ok + 0 条才是真的没命中。
  * 错误一律 HTTP 200 + result.isError + **纯文本**（upstream_unavailable / invalid_request /
    pydantic 校验 / 代理超时）→ 本脚本把纯文本当 error，不当成 0 条。

归一化：fetch 脚本落盘前必须调 `norm_post()`，把 Reddit 记录补成下游（05_screen / 07_media /
00_prep_qa / 08_build_xlsx）认的规范字段（`tweet_id` / `text` / `screen_name` / `favorites` /
`replies` / `created_at` / `post_url` / `media`）。合规形状见 `harvest_round()` 的落盘结构。
"""
import datetime
import glob
import html
import json
import os
import pathlib
import random
import re
import sys
import time
import urllib.error
import urllib.request
import urllib.parse

TIMEOUT = 120            # 单次 HTTP 等待；代理侧约 30s 已超时，这里给足余量
RETRIES = 3              # 常规重试（网络 / 5xx）
COLD_RETRY_SLEEP = 1.5   # 空 body / 超时 → 原样重发前的等待（等缓存预热）
DEFAULT_SLEEP = 1.0      # 相邻调用节流（服务端页间自述有数秒节流）
LIMIT_MAX = 300

SERVER = 'claudebaby-reddit'
RETRYABLE = ('temporarily unavailable', 'upstream_unavailable', 'timed out', 'timeout')


# ---------------------------------------------------------------- 凭证 / 连接

def _cfg_entry():
    cfg = pathlib.Path.home() / '.clacky' / 'mcp.json'
    if not cfg.exists():
        return {}
    try:
        data = json.loads(cfg.read_text(encoding='utf-8'))
        return (data.get('mcpServers') or {}).get(SERVER) or {}
    except Exception:
        return {}


def validate_url(url):
    parsed = urllib.parse.urlsplit(url)
    host = parsed.hostname or ''
    if parsed.scheme != 'https' or not (host == 'claudebaby.cn' or host.endswith('.claudebaby.cn')) or parsed.username or parsed.password:
        raise SystemExit('只允许 ClaudeBaby 官方域名的 HTTPS MCP 地址；请检查控制台配置。')
    if parsed.query or parsed.fragment:
        raise SystemExit('MCP 地址不能含查询凭据或 fragment；认证请使用 Bearer token。')
    return url


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise SystemExit('MCP 请求重定向已阻止，请使用控制台给出的直接地址。')


def resolve_url():
    url = os.environ.get('CLAUDEBABY_MCP_URL') or os.environ.get('REDDIT_MCP_URL')
    if url:
        return validate_url(url)
    entry = _cfg_entry()
    if entry.get('url'):
        return validate_url(entry['url'])
    sys.exit('未找到数据源地址：请设置 REDDIT_MCP_URL，或确认 ~/.clacky/mcp.json 内有 '
             'mcpServers.%s.url。' % SERVER)


def resolve_token():
    tok = os.environ.get('CLAUDEBABY_MCP_TOKEN') or os.environ.get('REDDIT_MCP_TOKEN')
    if tok:
        return tok
    headers = _cfg_entry().get('headers') or {}
    auth = headers.get('Authorization') or headers.get('authorization') or ''
    if auth.lower().startswith('bearer '):
        return auth[7:].strip()
    if auth:
        return auth.strip()
    sys.exit('未找到数据源凭证：请设置 REDDIT_MCP_TOKEN，或确认 ~/.clacky/mcp.json 内有 '
             'mcpServers.%s.headers.Authorization。' % SERVER)


def _rpc(method, params, rid=1):
    """JSON-RPC 一次调用；空 body / 网络错在内部重试。"""
    payload = json.dumps({'jsonrpc': '2.0', 'id': rid, 'method': method,
                          'params': params}).encode('utf-8')
    req = urllib.request.Request(
        resolve_url(), data=payload,
        headers={'Content-Type': 'application/json',
                 'Accept': 'application/json, text/event-stream',
                 'Authorization': 'Bearer ' + resolve_token()})
    last = None
    for attempt in range(RETRIES):
        try:
            with urllib.request.build_opener(_NoRedirect()).open(req, timeout=TIMEOUT) as resp:
                raw = resp.read().decode('utf-8', errors='replace')
            if not raw.strip():
                last = '空响应（代理超时，服务端可能仍在跑）'
                time.sleep(COLD_RETRY_SLEEP)
                continue
            return _parse(raw)
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')[:200]
            last = 'HTTP %s: %s' % (e.code, body)
            if e.code not in (429, 500, 502, 503, 504):
                raise SystemExit(last)
        except Exception as e:
            last = repr(e)
        time.sleep(COLD_RETRY_SLEEP * (2 ** attempt) + random.random())
    raise SystemExit('调用失败（已重试 %d 次）：%s' % (RETRIES, last))


def _parse(raw):
    """拆 SSE 帧 → 取最后一个 data: 行 → JSON。"""
    lines = [l[5:].strip() for l in raw.splitlines() if l.startswith('data:')]
    if not lines:
        raw = raw.strip()
        if not raw:
            raise SystemExit('空响应')
        return json.loads(raw)
    return json.loads(lines[-1])


def _retryable(text):
    low = str(text).lower()
    return any(t in low for t in RETRYABLE)


CALL_ATTEMPTS = 3


def call_tool(name, arguments):
    """→ (status, payload)。status ∈ ok|empty|error。

    三类**可重发**失败一律"原样重发同一请求"（不改参数，否则命中新 cache key 再冷跑）：
    空 body（代理约 30s 静默超时）/ {"error":"Request timed out"} /
    `upstream_unavailable: The data source is temporarily unavailable.`
    """
    body = None
    for attempt in range(CALL_ATTEMPTS):
        resp = _rpc('tools/call', {'name': name, 'arguments': arguments})
        if resp.get('error') and not resp.get('result'):
            body = resp['error']
        else:
            result = resp.get('result') or {}
            blocks = result.get('content') or []
            text = (blocks[0].get('text', '') if blocks else '') or ''
            body = text
            if result.get('isError'):
                if _retryable(text):
                    time.sleep(COLD_RETRY_SLEEP * (attempt + 1))
                    continue
                return 'error', text.strip()
            text = text.strip()
            if not text:
                time.sleep(COLD_RETRY_SLEEP * (attempt + 1))
                continue
            if not text.startswith('{') and not text.startswith('['):
                if _retryable(text):
                    time.sleep(COLD_RETRY_SLEEP * (attempt + 1))
                    continue
                return 'error', text          # 纯文本 = 服务端错误（不是 0 条）
            try:
                return 'ok', json.loads(text)
            except Exception:
                return 'error', text[:400]
        time.sleep(COLD_RETRY_SLEEP * (attempt + 1))
    if isinstance(body, str) and body.strip() and not body.strip().startswith('{'):
        return 'error', body.strip()
    return 'empty', ''


def rows_of(payload):
    """搜帖/评论树的行数组一律在 payload['rows']（兼容 items/list/data）。"""
    if isinstance(payload, dict):
        for k in ('rows', 'items', 'list', 'data', 'result'):
            if isinstance(payload.get(k), list):
                return payload[k]
    if isinstance(payload, list):
        return payload
    return []


# ---------------------------------------------------------------- 归一化

_IMG_EXT = re.compile(r'\.(jpg|jpeg|png|gif|webp)(\?|$)', re.I)


def _reddit_media(o):
    """把 Reddit 的 media_metadata / preview / 直链图 统一成
    {'photo': [{'media_url_https': url}]}（X 形状），喂给 07_media.py 的通用取图逻辑。

    Reddit 的 media 字段结构与 X 完全不同：X 是「值是列表的字典」，Reddit 则散在
    media_metadata（图集）/ preview.images（首图预览）/ url_overridden_by_dest（直链图帖）三处。
    07_media.py 只认 media_url_https，所以在这里统一，别留给下游猜。
    """
    urls = []

    mm = o.get('media_metadata')
    if isinstance(mm, dict):
        for _k, v in mm.items():
            if not isinstance(v, dict):
                continue
            u = (v.get('s') or {}).get('u') or ''
            if not u:
                ps = v.get('p')
                if isinstance(ps, list) and ps and isinstance(ps[-1], dict):
                    u = ps[-1].get('u') or ''
            if u:
                urls.append(html.unescape(u))

    pv = (o.get('preview') or {}).get('images')
    if isinstance(pv, list):
        for it in pv:
            if isinstance(it, dict):
                u = (it.get('source') or {}).get('url') or ''
                if u:
                    urls.append(html.unescape(u))

    dest = o.get('url_overridden_by_dest') or o.get('url') or ''
    if isinstance(dest, str) and _IMG_EXT.search(dest):
        urls.append(html.unescape(dest))

    seen, out = set(), []
    for u in urls:
        if u and u not in seen:
            seen.add(u)
            out.append({'media_url_https': u})
    return {'photo': out} if out else {}


def _iso_utc(v):
    """created_utc（秒，可能是 float/str）→ 'YYYY-MM-DD HH:MM:SS'（UTC）。"""
    if v in (None, ''):
        return ''
    try:
        return datetime.datetime.fromtimestamp(float(v), datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return str(v)


def norm_post(o, subreddit=None):
    """把一条原始记录归一成下游认的规范字段（**保留原始键**，只补规范键）。

    规范键：tweet_id / text / screen_name / favorites / replies / created_at /
            post_url / url / lang / media / subreddit / platform

    为什么必须在 fetch 阶段做而不是留给下游：`05_screen.py` 数的是 `favorites`、
    `08_build_xlsx.py` 拼的是 `t.get('url')`、`00_prep_qa.py` 只认 `tweet_id`+`text`。
    Reddit 那套字段（id / title+selftext / score / num_comments / author / created_utc /
    permalink）直接喂下去会**条条落空而且不报错**（筛出的候选池是 0 条、总表数字全 0）。
    """
    if not isinstance(o, dict):
        return None

    tid = o.get('tweet_id') or o.get('id') or o.get('name') or ''
    if isinstance(tid, str) and tid.startswith('t3_'):
        tid = tid[3:]
    if not tid:
        return None
    tid = str(tid)

    text = o.get('text')
    if text is None:
        title = o.get('title') or ''
        body = o.get('selftext') or o.get('body') or o.get('desc_full') or o.get('desc') or ''
        text = ('%s\n\n%s' % (title, body)).strip() if (title or body) else ''
    # 删帖的 Reddit 正文是 '[removed]' / '[deleted]'，只有一个标题时不要把它当真内容
    if (o.get('selftext') or '') in ('[removed]', '[deleted]'):
        text = (o.get('title') or '').strip()

    perm = o.get('permalink') or ''
    raw_url = o.get('url') if isinstance(o.get('url'), str) else ''
    if perm.startswith('/'):
        post_url = 'https://www.reddit.com' + perm
    elif perm.startswith('http'):
        post_url = perm
    elif raw_url.startswith('http') and 'reddit.com' in raw_url:
        # 实测 reddit_search_posts 的 rows 里没有 permalink，只有 url（就是帖子页，带 slug）
        post_url = raw_url
    else:
        post_url = ('https://www.reddit.com/comments/%s' % tid) if o.get('subreddit') else ''

    d = dict(o)
    d.update({
        'tweet_id': tid,
        'text': text,
        'screen_name': o.get('screen_name') or o.get('author') or '',
        # Reddit 的赞是 score（含踩的净值），转发/浏览没有对应字段 → 留空，
        # 总表那两列填「—」而不是 0（见 references/pipeline.md 6.0.2 第③条）
        'favorites': o.get('favorites') if o.get('favorites') is not None else o.get('score'),
        'replies': o.get('replies') if o.get('replies') is not None else o.get('num_comments'),
        'created_at': o.get('created_at') or _iso_utc(o.get('created_utc')),
        'lang': o.get('lang') or '',
        'url': post_url or (o.get('url') if isinstance(o.get('url'), str) and 'reddit.com' in (o.get('url') or '') else ''),
        'post_url': post_url,
        'subreddit': subreddit or o.get('subreddit') or '',
        'platform': o.get('platform') or ('reddit' if o.get('subreddit') else ''),
    })
    # media：X 形状是「值是列表的字典」，原样保留；Reddit 形状则归一成 X 形状
    if not isinstance(o.get('media'), (dict, list)):
        m = _reddit_media(o)
        if m:
            d['media'] = m
    return d


def norm_comment(o, post_id=None):
    """评论树里按 link_id 过滤（post_id 传错会静默返回邻近帖的评论）。"""
    if not isinstance(o, dict):
        return None
    lib = o.get('link_id') or ''
    if post_id:
        want = 't3_' + str(post_id)
        if lib and lib != want:
            return None
    if not post_id and lib.startswith('t3_'):
        post_id = lib[3:]        # 没显式传 post_id 时，用 link_id 反推（t3_ 前缀剥掉）
    d = dict(o)
    d['tweet_id'] = str(o.get('tweet_id') or o.get('id') or '')
    d['text'] = o.get('text') if o.get('text') is not None else (o.get('body') or '')
    d['screen_name'] = o.get('screen_name') or o.get('author') or ''
    d['favorites'] = o.get('favorites') if o.get('favorites') is not None else o.get('score')
    d['created_at'] = o.get('created_at') or _iso_utc(o.get('created_utc'))
    d['_post_id'] = str(post_id) if post_id else ''
    return d


def dump(path, payload):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding='utf-8')
    return p


# ---------------------------------------------------------------- 一轮抓取

def harvest_round(specs, out_path, limit=LIMIT_MAX, sleep=DEFAULT_SLEEP, per_label_files=None):
    """跑一组检索式并落成**标准形状** `{label: {keyword, subreddit, days, tweets: [...]}}`。

    标准形状是契约（`00_prep_qa.py` / probe / `05_screen.py` 都按它读），所以抓完立刻归一化，
    不要留 Reddit 的原始字段给下游。specs 每条：{label, subreddit, query, days}。

    status=error 的组合**不算 0 条**：记进返回值的 `errors`，并在打印里标 [ERR]，
    让调用方决定是否原样重跑（多数是代理瞬时超时，参数不变才能吃服务端缓存）。
    """
    limit = max(1, min(int(limit), LIMIT_MAX))
    out, tot, errors, truncated = {}, 0, [], []
    for sp in specs:
        lb = sp['label']
        arg = {'subreddit': sp['subreddit'], 'query': sp['query'],
               'days': int(sp.get('days', 365)), 'limit': limit}
        t0 = time.time()
        st, pl = call_tool('reddit_search_posts', arg)
        if st == 'error':
            st, pl = call_tool('reddit_search_posts', arg)   # 原样再试一次
        rows = rows_of(pl) if st == 'ok' else []
        tweets = [t for t in (norm_post(r, sp['subreddit']) for r in rows) if t]
        trunc = len(rows) >= limit
        out[lb] = {'keyword': sp['query'], 'subreddit': sp['subreddit'],
                   'days': arg['days'], 'limit': limit, 'truncated': trunc,
                   'status': st, 'tweets': tweets}
        tot += len(tweets)
        if st != 'ok':
            # 记全 spec（subreddit/query/days）——04_fetch_round4.py 要拿它**原样**重跑，
            # 只记 label + err 的话下一轮就重放不出来了。
            errors.append({'label': lb, 'subreddit': sp['subreddit'], 'query': sp['query'],
                           'days': arg['days'], 'err': str(pl)[:160]})
        if trunc:
            truncated.append(lb)
        print('%-16s r/%-20s n=%3d %s %.1fs%s' % (
            lb, sp['subreddit'], len(tweets), st, time.time() - t0,
            ' [TRUNC]' if trunc else ''))
        if per_label_files:
            dump(per_label_files % lb, out[lb])
        time.sleep(sleep)
    dump(out_path, out)
    print('saved %s | total %d' % (out_path, tot))
    if truncated:
        print('[warn] 触顶（rows==limit=%d）的组合：%s' % (limit, truncated))
        print('       oldest-first 排序下**最新命中会丢**，需按更细的词/更短 days 拆分重取')
    if errors:
        print('[warn] %d 个组合取数失败（**不是 0 条**，需原样重跑）：%s'
              % (len(errors), [e['label'] for e in errors]))
        # 失败组合另存一份，供「原样重跑」。命名兜住两种路径：既支持约定的 xxx_all.json，
        # 也支持任意名字 —— 否则 replace 落空时会把 errors **覆盖写到主文件上**（好数据被冲掉）。
        ep = str(out_path)
        ep = ep.replace('_all.json', '_errors.json') if '_all.json' in ep \
            else (ep[:-5] + '_errors.json' if ep.endswith('.json') else ep + '_errors.json')
        if ep != str(out_path):
            dump(ep, errors)
    return out


# ---------------------------------------------------------------- CLI

# 离线兜底：上游不可达时 `tools` 至少还能把可用工具/参数印出来（真值以此为准，实测校准过）
KNOWN_TOOLS = [
    ('reddit_search_posts', 'reddit_search_posts',
     {'subreddit': 'string（必填，社区名，不带 r/；**不支持 all**）',
      'query': 'string（必填，社区内关键词，无 X 语法糖）',
      'days': 'int（必填，相对天数，越大越慢）',
      'limit': 'int 1-300（上限 300，超过报 invalid_request）'},
     '社区内按关键词检索帖子，**按时间先后（oldest-first）**返回，cursor 恒为 null。'),
    ('reddit_get_thread', 'reddit_get_thread',
     {'post_id': 'string（必填，帖子 id，不带 t3_）',
      'top_n': 'int（可选，取前 N 条评论）'},
     '取单帖详情 + 评论树；post_id 写错会**静默**返回邻近帖的评论，'
     '必须校验 link_id == "t3_"+post_id。'),
    ('reddit_search_comments', 'reddit_search_comments',
     {'subreddit': 'string', 'query': 'string', 'days': 'int', 'limit': 'int'},
     '**实测恒空，按不可用处理**：评论只能走 posts → 逐帖 thread。'),
]


def cmd_tools(_args):
    try:
        resp = _rpc('tools/list', {})
    except (SystemExit, Exception) as e:                          # noqa: BLE001
        print('[warn] 上游不可达（%s），以下是本地校准过的工具清单：\n' % str(e)[:120])
        for _n, name, args, desc in KNOWN_TOOLS:
            print('%s' % name)
            for k, v in args.items():
                print('    %-10s %s' % (k, v))
            print('    -> %s' % desc)
        print('\n共 %d 个工具（离线清单）' % len(KNOWN_TOOLS))
        return 0
    tools = (resp.get('result') or {}).get('tools') or []
    for t in tools:
        props = ((t.get('inputSchema') or {}).get('properties') or {})
        req = ((t.get('inputSchema') or {}).get('required') or [])
        desc = (t.get('description') or '').replace('\n', ' ')[:100]
        print('%-26s required=%-18s args=%s' % (t['name'], ','.join(req), ','.join(props)))
        print('%-26s %s' % ('', desc))
    print('\n共 %d 个工具' % len(tools))
    print('注意：reddit_search_comments 实测恒空，按不可用处理（评论走 posts → thread 逐帖）。')
    return 0


def cmd_ping(_args):
    st, pl = call_tool('reddit_search_posts',
                       {'subreddit': 'ecommerce', 'query': 'revenue', 'days': 30, 'limit': 3})
    rows = rows_of(pl) if st == 'ok' else []
    print('reddit_search_posts: status=%s rows=%d' % (st, len(rows)))
    if st == 'error':
        print('error:', str(pl)[:200])
        return 1
    if rows:
        r = rows[0]
        print('sample:', {k: r.get(k) for k in ('id', 'subreddit', 'title', 'score', 'created_utc')})
    return 0


def cmd_posts(args):
    limit = max(1, min(int(args.limit), LIMIT_MAX))
    if int(args.limit) > LIMIT_MAX:
        print('[warn] limit 上限 %d，已截断为 %d（服务端报 invalid_request）' % (LIMIT_MAX, limit))
    arg = {'subreddit': args.subreddit, 'query': args.query, 'days': int(args.days), 'limit': limit}
    t0 = time.time()
    st, pl = call_tool('reddit_search_posts', arg)
    rows = rows_of(pl) if st == 'ok' else []
    print('status=%s rows=%d %.1fs' % (st, len(rows), time.time() - t0))
    if st == 'error':
        print('error:', str(pl)[:200])
        return 1
    if len(rows) >= limit:
        print('[warn] 命中触顶（rows == limit=%d）：oldest-first 排序下**最新命中会丢**' % limit)
    norm = [t for t in (norm_post(r, args.subreddit) for r in rows) if t]
    payload = {'endpoint': (pl or {}).get('endpoint', 'posts.search'), 'request': arg,
               'count': len(norm), 'truncated': len(rows) >= limit, 'rows': norm}
    if args.out:
        print('已落盘', dump(args.out, payload))
    else:
        print(json.dumps([{k: v.get(k) for k in ('tweet_id', 'screen_name', 'favorites', 'created_at')}
                          for v in norm[:3]], ensure_ascii=False, indent=1)[:800])
    return 0


def cmd_thread(args):
    arg = {'post_id': args.post_id}
    if args.top_n:
        arg['top_n'] = int(args.top_n)
    st, pl = call_tool('reddit_get_thread', arg)
    rows = rows_of(pl) if st == 'ok' else []
    if st == 'error':
        print('status=error rows=0')
        print('error:', str(pl)[:200])
        return 1
    good = [c for c in (norm_comment(r, args.post_id) for r in rows) if c]
    bad = len(rows) - len(good)
    print('status=%s rows=%d kept=%d rejected=%d' % (st, len(rows), len(good), bad))
    if bad:
        print('[warn] link_id 校验丢弃 %d 行（≠ t3_%s）：post_id 传错会静默返回邻近帖评论'
              % (bad, args.post_id))
    payload = {'endpoint': 'comments.thread', 'request': arg, 'count': len(good),
               'rejected_link_id_mismatch': bad, 'rows': good}
    if args.out:
        print('已落盘', dump(args.out, payload))
    return 0


def cmd_call(args):
    try:
        arguments = json.loads(args.arguments) if args.arguments else {}
    except Exception as e:
        raise SystemExit('arguments 必须是合法 JSON：%s' % e)
    st, pl = call_tool(args.tool, arguments)
    print('status=', st)
    print(json.dumps(pl, ensure_ascii=False)[:2000])
    return 0 if st == 'ok' else 1


def cmd_norm(args):
    """把任意形状的原始记录文件过一遍 norm_post，用于排障（看归一化后长什么样）。"""
    paths = sorted(glob.glob(args.path))
    if not paths:
        raise SystemExit('没匹配到文件：%s' % args.path)
    n = 0
    for p in paths:
        d = json.load(open(p, encoding='utf-8'))

        def eat(o):
            nonlocal n
            if isinstance(o, dict):
                r = norm_post(o)
                if r:
                    n += 1
                    if n <= args.show:
                        print(json.dumps({k: r.get(k) for k in
                                          ('tweet_id', 'subreddit', 'screen_name', 'favorites',
                                           'replies', 'created_at', 'url', 'media')},
                                         ensure_ascii=False)[:400])
                    return
                for v in o.values():
                    eat(v)
            elif isinstance(o, list):
                for v in o:
                    eat(v)
        eat(d)
    print('%d 条可归一化记录' % n)
    return 0


def main():
    import argparse
    ap = argparse.ArgumentParser(description='社媒案例库数据源客户端（Reddit MCP）')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('tools', help='列工具与参数'); p.set_defaults(fn=cmd_tools)
    p = sub.add_parser('ping', help='连通性自检'); p.set_defaults(fn=cmd_ping)

    p = sub.add_parser('posts', help='按 subreddit + 关键词搜帖')
    p.add_argument('--subreddit', required=True)
    p.add_argument('--query', required=True)
    p.add_argument('--days', type=int, default=365)
    p.add_argument('--limit', type=int, default=LIMIT_MAX)
    p.add_argument('--out')
    p.set_defaults(fn=cmd_posts)

    p = sub.add_parser('thread', help='取单帖评论树')
    p.add_argument('--post-id', required=True, dest='post_id')
    p.add_argument('--top-n', type=int, dest='top_n')
    p.add_argument('--out')
    p.set_defaults(fn=cmd_thread)

    p = sub.add_parser('call', help='直接调一个工具')
    p.add_argument('tool')
    p.add_argument('arguments', nargs='?', default='')
    p.set_defaults(fn=cmd_call)

    p = sub.add_parser('norm', help='排障：把原始记录归一化后打印前几条')
    p.add_argument('path')
    p.add_argument('--show', type=int, default=3)
    p.set_defaults(fn=cmd_norm)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == '__main__':
    sys.exit(main() or 0)
