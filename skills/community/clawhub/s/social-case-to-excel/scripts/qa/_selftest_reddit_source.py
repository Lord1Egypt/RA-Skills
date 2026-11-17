# -*- coding: utf-8 -*-
"""数据源离线自检（不联网）：归一化 / 重试 / 落盘形状 / 缺值语义。

为什么单独一个文件：`cb_mcp.py` 里最容易悄悄改坏的三处 —— ①原始字段→内部字段的映射、
②代理 30s 静默超时时「原样重发」的重试、③`status=error` 与「0 条」的区分 —— 只有真跑
上游才暴露，而上游随时可能不可达（claudebaby.cn 就整段挂过）。这份自检用**离线桩**把
这三件事钉住：改 `cb_mcp.py` 后先跑它，再跑真实取数。

用法：python3 scripts/qa/_selftest_reddit_source.py
退出码：0 = 全通过；非 0 = 有 FAIL（不要开始取数）。
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SC = os.path.dirname(HERE)
sys.path.insert(0, SC)
import cb_mcp  # noqa: E402

OK, FAIL = [], []


def chk(name, cond, extra=''):
    (OK if cond else FAIL).append(name)
    print('%s %s%s' % ('  PASS' if cond else '  FAIL', name, ('  ' + str(extra)) if extra else ''))


# ---------------------------------------------------------------- 1. SSE 拆帧
print('=== 1. SSE 拆帧（data: 行取最后一条）===')
inner = {'endpoint': 'posts.search', 'rows': [{'id': 'a1', 'title': 't'}], 'count': 1, 'cursor': None}
body = json.dumps({'ok': True, 'result': {'content': [{'text': json.dumps(inner)}]}})
sse = ('event: message\n'
       'data: {"jsonrpc":"2.0","id":1,"result":{"keep":"first"}}\n\n'
       'event: message\n'
       'data: %s\n\n' % body)
got = cb_mcp._parse(sse)
chk('取最后一条 data:（不是第一条）', got.get('ok') is True, list(got)[:3])
chk('纯 JSON body 也能吃下', cb_mcp._parse(body).get('ok') is True)
try:
    cb_mcp._parse('   ')
    chk('空 body 抛 SystemExit', False)
except SystemExit:
    chk('空 body 抛 SystemExit', True)

# ---------------------------------------------------------------- 2. 归一化
print('\n=== 2. norm_post：Reddit 原始字段 → 内部契约字段 ===')
raw = {'id': '1nqx17e', 'subreddit': 'AmazonFBA', 'author': 'Admirable_Sale3860',
       'title': 'My FBA results', 'selftext': 'Revenue $40k in 3 months.',
       'score': 512, 'num_comments': 214, 'created_utc': 1758879784,
       'link_flair_text': 'Case Study',
       'url': 'https://www.reddit.com/r/AmazonFBA/comments/1nqx17e/my_fba_results/'}
p = cb_mcp.norm_post(raw, raw['subreddit'])
chk('title+selftext → text', p['text'].startswith('My FBA results') and '$40k' in p['text'])
chk('score → favorites', p['favorites'] == 512)
chk('num_comments → replies', p['replies'] == 214)
chk('created_utc → ISO created_at', str(p['created_at'])[:4] == '2025', p['created_at'])
chk('author → screen_name', p['screen_name'] == 'Admirable_Sale3860')
chk('url → post_url（真实行没有 permalink 字段）', 'reddit.com' in p['post_url'], p['post_url'])
chk('platform=reddit', p['platform'] == 'reddit')
chk('原始键保留（下游做图片/主题兜底要用）', 'selftext' in p and 'score' in p)

print('\n=== 3. 边界：删帖 / 缺指标 / 无 url / t3_ 前缀 ===')
r = cb_mcp.norm_post({'id': 'abc', 'title': 'Only a title', 'selftext': '[removed]', 'subreddit': 'x'})
chk('[removed] 不污染 text', r['text'] == 'Only a title', repr(r['text']))
chk('缺 score → favorites=None（落表写「—」，不写 0）', r['favorites'] is None, r['favorites'])
chk('缺 num_comments → replies=None', r['replies'] is None)
chk('无 url → 回退 /comments/<id>', r['post_url'].endswith('/comments/abc'), r['post_url'])
chk('id 上的 t3_ 前缀剥掉', cb_mcp.norm_post({'id': 't3_zzz', 'title': 'x'})['tweet_id'] == 'zzz')
chk('无 id → None（不产脏记录）', cb_mcp.norm_post({'title': 'no id'}) is None)

print('\n=== 4. norm_comment：link_id 守卫（post_id 写错会静默返回邻近帖的评论）===')
good = cb_mcp.norm_comment({'id': 'c1', 'link_id': 't3_1nqx17e', 'body': 'nice',
                            'score': 7, 'author': 'u2'}, post_id='1nqx17e')
chk('link_id 匹配 → 保留', bool(good) and good['text'] == 'nice')
chk('score → favorites', good['favorites'] == 7)
chk('author → screen_name', good['screen_name'] == 'u2')
chk('link_id 不匹配 → 丢弃（None）',
    cb_mcp.norm_comment({'id': 'c2', 'link_id': 't3_OTHER', 'body': 'x'}, post_id='1nqx17e') is None)
chk('没传 post_id 时用 link_id 反推 _post_id',
    cb_mcp.norm_comment({'id': 'c3', 'link_id': 't3_1nqx17e', 'body': 'x'})['_post_id'] == '1nqx17e')

# ---------------------------------------------------------------- 5. 重试
print('\n=== 5. call_tool：30s 静默超时（HTTP 200 + 空 body）必须原样重发 ===')
seq = []


def fake_rpc(method, params, rid=1):
    seq.append(json.dumps(params, sort_keys=True))
    if len(seq) == 1:
        return {}                                  # 空 body：代理超时
    if len(seq) == 2:
        return {'error': {'message': 'upstream_unavailable'}}
    return {'result': {'content': [{'text': json.dumps(inner)}]}, 'ok': True}


_real, cb_mcp._rpc_orig = cb_mcp._rpc, cb_mcp._rpc
cb_mcp._rpc = fake_rpc
try:
    st, pl = cb_mcp.call_tool('reddit_search_posts',
                              {'subreddit': 'AmazonFBA', 'query': 'case study', 'days': 730, 'limit': 300})
finally:
    cb_mcp._rpc = _real
chk('重试 3 次后成功', st == 'ok', 'status=%s calls=%d' % (st, len(seq)))
chk('重试参数逐次完全一致（换参数=新缓存键=又要冷跑一次）', len(set(seq)) == 1, len(set(seq)))
chk('至少发了 3 次', len(seq) >= 3, len(seq))
chk('rows_of 能取到 rows', len(cb_mcp.rows_of(pl)) == 1)

cb_mcp._rpc = lambda m, p, rid=1: {'result': {'isError': True,
                                              'content': [{'text': 'invalid_request: limit>300'}]}}
try:
    st2, pl2 = cb_mcp.call_tool('reddit_search_posts', {'limit': 999})
finally:
    cb_mcp._rpc = _real
chk('isError → status=error 且带原文', st2 == 'error' and 'invalid_request' in str(pl2), st2)
chk('error 时 rows_of 返回空（但**不等于 0 条**）', cb_mcp.rows_of(pl2) == [])

# ---------------------------------------------------------------- 6. 落盘形状
print('\n=== 6. harvest_round 落盘形状（00_prep_qa / 05_screen 的读入口）===')
specs = [{'label': 'L1', 'subreddit': 'AmazonFBA', 'query': 'case study', 'days': 730},
         {'label': 'L2', 'subreddit': 'AmazonFBA', 'query': 'invalid', 'days': 730}]


def fake_tool(name, arg, *a, **k):
    if arg.get('query') == 'invalid':
        return 'error', 'invalid_request: bad query'
    rows = [raw, dict(raw, id='second', score=3, num_comments=1)]
    return 'ok', {'endpoint': 'posts.search', 'rows': rows, 'count': len(rows), 'cursor': None}


_rt = cb_mcp.call_tool
cb_mcp.call_tool = fake_tool
out_path = '/tmp/cbx_selftest_all.json'
try:
    out = cb_mcp.harvest_round(specs, out_path, limit=300, sleep=0)
finally:
    cb_mcp.call_tool = _rt
dumped = json.load(open(out_path, encoding='utf-8'))
top = dumped['L1']
chk('顶层按 label 分桶', set(dumped) == {'L1', 'L2'}, sorted(dumped))
chk('桶里有 keyword/subreddit/days/limit/status/tweets（标准形状）',
    set(('keyword', 'subreddit', 'days', 'limit', 'truncated', 'status', 'tweets')) <= set(top), sorted(top))
chk('tweets 已归一（不是 Reddit 原始行）', 'favorites' in top['tweets'][0] and 'tweet_id' in top['tweets'][0])
chk('未触顶 → truncated=False', top['truncated'] is False)
chk('失败组合 status=error（不是 0 条）', dumped['L2']['status'] == 'error', dumped['L2']['status'])
errs = json.load(open('/tmp/cbx_selftest_errors.json', encoding='utf-8')) \
    if os.path.exists('/tmp/cbx_selftest_errors.json') else []
chk('失败组合另存 errors 文件（方便原样重跑）', any(e['label'] == 'L2' for e in errs), [e['label'] for e in errs])
chk('errors 文件没有覆盖主文件（主文件仍是分桶 dict）', isinstance(dumped, dict))
for p_ in (out_path, '/tmp/cbx_selftest_errors.json'):
    if os.path.exists(p_):
        os.remove(p_)

# ---------------------------------------------------------------- 7. 下游能吃
print('\n=== 7. 05_screen 能读标准形状并筛出案例（不破坏真实中间产物）===')
case = dict(raw, title='How I scaled to $40k/mo in 3 months',
            selftext='Revenue $40k in 3 months. I tested 12 products and here is what worked. '
                     'The full breakdown: ads spend $8k, profit $12k, ROAS 3.2. '
                     'What I would do differently next time: start with the 3 winners only.',
            score=512, num_comments=214)
noise = dict(raw, id='n1', title='Is this a good buy?', selftext='beginner here', score=1, num_comments=0)
short = dict(raw, id='s1', title='hi', selftext='', score=2, num_comments=0)
d = {'L1': {'keyword': 'case study', 'subreddit': 'AmazonFBA', 'days': 730, 'limit': 300,
            'truncated': False, 'status': 'ok',
            'tweets': [cb_mcp.norm_post(x, 'AmazonFBA') for x in (case, noise, short)]}}

# 05_screen 的入参/出参路径是硬编码的，跑它会把同名中间产物写掉 —— 先备份再还原。
GUARD = ['/tmp/cbx1_all.json', '/tmp/cbx_short2.json', '/tmp/cbx_new.txt']
backup = {}
for p_ in GUARD:
    if os.path.exists(p_):
        backup[p_] = open(p_, 'rb').read()
json.dump(d, open('/tmp/cbx1_all.json', 'w', encoding='utf-8'), ensure_ascii=False)

cwd = os.getcwd()
os.chdir('/tmp')
sys.argv = ['05_screen.py']
buf = io.StringIO()
try:
    import contextlib
    with contextlib.redirect_stdout(buf):
        exec(compile(open(os.path.join(SC, '05_screen.py'), encoding='utf-8').read(), '05', 'exec'),
             {'__name__': 'not_main'})
    chk('05_screen 跑完并出了候选池', os.path.exists('/tmp/cbx_short2.json'))
except Exception as e:                                        # noqa: BLE001
    chk('05_screen 跑完并出了候选池', False, repr(e))
finally:
    os.chdir(cwd)

try:
    sh = json.load(open('/tmp/cbx_short2.json', encoding='utf-8'))
    ids = [r.get('tid') for r in sh]
    chk('真案例进池（标题带数字 + 有指标）', raw['id'] in ids, ids)
    chk('纯噪音被筛掉', 'n1' not in ids)
    chk('过短/无数字的帖子被筛掉', 's1' not in ids)
    rec = [r for r in sh if r.get('tid') == raw['id']]
    chk('候选池用紧凑键（tid/fav/rp），下游照此读',
        bool(rec) and set(('tid', 'fav', 'rp', 'url', 'theme', 'text')) <= set(rec[0]), sorted(rec[0]) if rec else None)
    chk('点赞=score、评论=num_comments 映射正确', bool(rec) and rec[0]['fav'] == 512 and rec[0]['rp'] == 214)
    chk('Reddit 没有的转发/浏览 → 候选池里就是「—」（不是 0）',
        bool(rec) and rec[0]['rt'] == '—' and rec[0]['views'] == '—', (rec[0]['rt'], rec[0]['views']) if rec else None)
    chk('subreddit 兜底出主题（正文没主题词时靠社区）', bool(rec) and rec[0]['theme'] == ['选品'], rec[0]['theme'] if rec else None)
    chk('帖子链接保留（Reddit 帖子页，不是 X 状态页）', bool(rec) and 'reddit.com' in rec[0]['url'])
except Exception as e:                                        # noqa: BLE001
    chk('候选池可读', False, repr(e))

# 还原被 05_screen 写掉的中间产物
for p_ in GUARD:
    if p_ in backup:
        open(p_, 'wb').write(backup[p_])
    elif os.path.exists(p_):
        os.remove(p_)

print('\n=========== 结果 ===========')
print('PASS %d / FAIL %d' % (len(OK), len(FAIL)))
for f in FAIL:
    print('  !! ' + f)
sys.exit(1 if FAIL else 0)
