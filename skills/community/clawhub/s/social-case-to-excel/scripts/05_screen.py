# -*- coding: utf-8 -*-
"""第 2 步：合并去重 + 筛「真案例 vs 农场噪音」+ 自动打主题标签。

数据源是 Reddit（`cb_mcp.py` 抓），记录在抓取时已归一化，所以这里读的是规范字段：
`tweet_id` / `text` / `favorites`（Reddit 的 score）/ `replies`（num_comments）/
`screen_name`（作者）/ `created_at` / `subreddit`。

三个 Reddit 特有的注意点：
  * **点赞就是 score**（含踩的净值，可能为负）；没有转发/浏览字段 → 判门槛只看 score。
  * **主题可以先用 subreddit 兜底**：Reddit 的正文常常很长而主题词不在标题里，
    垂类社区本身（r/AmazonFBA = 选品/Listing、r/SEO = 关键词、r/PPC = 广告）信息量很大，
    所以 `theme()` 同时看正文与 subreddit。
  * **`text` 已经是「标题 + \\n\\n + 正文」**（`norm_post()` 干的），不要再只拿 selftext。
"""
import json, os, re

POOL = ['/tmp/cbx1_all.json', '/tmp/cbx2_all.json', '/tmp/cbx3_all.json', '/tmp/cbx4_all.json']

# subreddit → 主题兜底（正文里主题词不明显时用）
SUB_THEME = {
    'amazonfba': '选品', 'fulfillmentbyamazon': '选品', 'amazonseller': 'Listing运营',
    'ecommerce': '选品', 'shopify': 'Listing运营', 'dropship': '选品', 'dropshipping': '选品',
    'etsysellers': 'Listing运营', 'etsy': 'Listing运营', 'printondemand': '选品',
    'seo': '关键词', 'bigseo': '关键词', 'blogging': '关键词', 'analytics': '关键词',
    'ppc': '站外运营', 'adwords': '站外运营', 'facebookads': '站外运营',
    'emailmarketing': '站外运营', 'socialmedia': '站外运营', 'growthhacking': '站外运营',
    'affiliatemarketing': '站外运营', 'marketing': '黑五营销', 'tiktokshop': '站外运营',
}


def flatten(paths):
    """把若干原始抓取 JSON 摊平成 {帖子ID: record}，兼容三种落盘形状。

    为什么非要容错：自建平台抓取脚本常把结果落成「键=帖子 ID 的 dict」
    （`{bvid: {...}}` / `{note_id: {...}}`），而 fetch 模板落的是
    `{label: {keyword, tweets: [...]}}`。下游要是假设"一定是 list"或者
    "一定是 {label: {tweets}}" 就直接炸在
    `TypeError: string indices must be integers`——因为对 dict 做 `for t in d`
    迭代出来的是字符串键，`t['text']` 自然报错。所以读取端统一走这里，
    判定靠"这条记录里有没有 ID 字段 + 正文"，不靠文件名也不靠猜。
    """
    recs = {}

    def tid_of(o):
        for k in ('tweet_id', 'tid', 'id', 'note_id', 'bvid', 'aweme_id', 'video_id'):
            if o.get(k):
                return str(o[k])
        return ''

    def eat(o):
        if isinstance(o, dict):
            t = tid_of(o)
            if t and (o.get('text') is not None or o.get('desc') is not None or o.get('title') is not None):
                recs.setdefault(t, o)
                return
            for v in o.values():
                eat(v)
        elif isinstance(o, list):
            for v in o:
                eat(v)

    for p in POOL:
        if not os.path.exists(p):
            continue
        eat(json.load(open(p, encoding='utf-8')))
    return recs


def fav_of(t):
    for k in ('favorites', 'score', 'ups'):
        v = t.get(k)
        if v is not None:
            try:
                return int(float(v))
            except Exception:
                return 0
    return 0


def sn_of(t):
    return t.get('screen_name') or t.get('author') or ''


def created_of(t):
    return t.get('created_at') or t.get('created') or ''


recs = flatten(POOL)
print('unique posts', len(recs))

HARD = ['amazon', 'shopify', 'etsy', 'tiktok shop', 'tiktokshop', 'dropship', 'fba', 'private label',
        'dtc', 'd2c', 'ecommerce', 'e-com', 'ecom', 'listing', 'black friday', 'bfcm', 'cyber monday',
        'product research', 'roas', 'acos', 'klaviyo', 'product page', 'sku', 'alibaba', 'aliexpress',
        '独立站', '跨境电商', '亚马逊', '选品', '出海', 'amazon seller', 'conversion rate', 'cvr',
        'supplier', 'a+ content', 'search terms', 'search volume', 'keyword', 'reddit', 'ugc', 'affiliate']
KILL = ['claude code', 'crypto', 'bitcoin', 'airdrop', 'shitcoin', 'stock', 'stocks', 'options trading',
        'nifty', 'cpi', 'nvidia', 'nasdaq', 'lpa', 'resume', 'leetcode', 'faceless', 'info product',
        'youtube automation', 'smma', 'ghostwriter', 'webinar', 'cold email', 'salary',
        # Reddit 专属噪音：泛创业社区里占比很高
        'onlyfans', 'nsfw', 'dating', 'casino', 'betting', 'gambling', 'karma farm']
NUM = re.compile(r'(\$\s?[\d,\.]+\s?[KMBkmb]?|\d+(?:\.\d+)?\s?%|\b\d[\d,]{2,}\b)', re.I)


def theme(t, sub=''):
    low = (t or '').lower()
    s = set()
    if re.search(r'black friday|bfcm|cyber monday|holiday|双11|黑五|旺季|q4', low):
        s.add('黑五营销')
    if re.search(r'keyword|search term|search volume|indexing|rank\b|seo|关键词', low):
        s.add('关键词')
    if re.search(r'listing|main image|a\+ content|product page|ppc|sponsored products|acos|review|详情页|主图|评价', low):
        s.add('Listing运营')
    if re.search(r'reddit|r/', low):
        s.add('Reddit营销')
    if re.search(r'influencer|ugc|creator|affiliate|tiktok|instagram|youtube|email|klaviyo|sms|google ads|meta ads|站外|达人', low):
        s.add('站外运营')
    if re.search(r'product research|winning product|sourcing|supplier|niche|选品|测品', low):
        s.add('选品')
    # subreddit 兜底：垂类社区本身就是很强的主题信号
    s.add(SUB_THEME.get((sub or '').lower()) or '')
    s.discard('')
    return s


rows = []
for tid, t in recs.items():
    txt = re.sub(r'https?://\S+', '', t.get('text') or '').strip()
    if len(txt) < 150:
        continue
    low = txt.lower()
    dom = [s for s in HARD if s in low]
    kill = [k for k in KILL if k in low]
    if not dom:
        continue
    if len(kill) >= 1 and len(dom) <= 1:
        continue
    if len(kill) >= 3:
        continue
    nnum = len(NUM.findall(txt))
    fav = fav_of(t)
    if nnum < 3 and fav < 120:
        continue
    # 缺失的平台指标写「—」不写 0：Reddit 没有转发/浏览字段，写 0 会被读成"真的为 0"
    def dash(v):
        return v if v not in (None, '') else '—'

    _u = t.get('url') or ''
    rows.append({'tid': tid, 'sn': sn_of(t), 'sub': t.get('subreddit') or '', 'fav': fav,
                 'rt': dash(t.get('retweets')), 'rp': dash(t.get('replies')),
                 'views': dash(t.get('views')),
                 'url': t.get('post_url') or (_u if str(_u).startswith('http') else ''),
                 'lang': t.get('lang'), 'created': created_of(t), 'nnum': nnum, 'len': len(txt),
                 'score': nnum * 3 + (1 if fav >= 200 else 0) + (1 if len(txt) > 500 else 0),
                 'text': txt, 'dom': dom[:6], 'theme': sorted(theme(txt, t.get('subreddit') or ''))})
rows.sort(key=lambda r: -(r['score'] + 2 * len(r['dom'])))
json.dump(rows, open('/tmp/cbx_short2.json', 'w'), ensure_ascii=False)
print('shortlist2', len(rows))

old = set()
if os.path.exists('/tmp/cbx_short.json'):
    old = {r['tid'] for r in json.load(open('/tmp/cbx_short.json'))}
new = [r for r in rows if r['tid'] not in old]
print('new entries', len(new))
L = []
for i, r in enumerate(new):
    L.append('[%3d] f%-5s r/%-18s %-17s %-24s %s' % (
        i, r['fav'], r['sub'][:18], r['sn'][:17], ','.join(r['theme'])[:24], r['created'][:16]))
    L.append('      ' + r['text'][:400].replace('\n', ' '))
open('/tmp/cbx_new.txt', 'w').write('\n'.join(L))
print('-> /tmp/cbx_new.txt')
