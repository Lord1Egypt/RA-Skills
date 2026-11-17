# -*- coding: utf-8 -*-
"""第 4 步 · 配图：从入选池抽 media 列表并下载（**文件名以 post id 为键**）。

两条平台差异（Reddit 与 X 不同，别照抄 X 的写法）：
  * **Reddit 的图片是直链**（i.redd.it / preview.redd.it），**不要**照 X 那样追加
    `?format=jpg&name=large` —— X 的 pbs.twimg.com 需要这个参数拿高清，
    Reddit 的预览链接自带 `?width=…&format=pjpg&s=…`，改查询串会 403/404 或拿到占位图。
    这里按域名分流。
  * **代理只是"需要时就带上"**：X 的图必须走本地代理；Reddit 的图很多直连也通。
    所以本脚本**先走代理、失败再直连**（`NO_PROXY=1` 可强制直连），别让一条通道的
    网络策略把另一条平台的图整批下成 0 张。
"""
import json, os, subprocess, time

CHANNEL_HINT = {}  # host -> 'proxy' / 'direct'：记住这个域名走哪条通道，别每次从头试

PROXY = os.environ.get('MEDIA_PROXY', 'http://127.0.0.1:7897')
USE_PROXY_FIRST = os.environ.get('NO_PROXY') != '1'
MAX_IMG = 4  # 每条帖最多下载几张（sheet1 每行只内嵌 2 张，sheet4 会列出全部，别在这里截太小）
POOL = ['/tmp/cbx1_all.json', '/tmp/cbx2_all.json', '/tmp/cbx3_all.json', '/tmp/cbx4_all.json']

IMG_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.webp')


def flatten(paths):
    """把原始抓取 JSON 摊平成 {帖子ID: record}，兼容 list / {label:{tweets}} / {id:record} 三种形状。

    多平台跑批时自建抓取脚本常落成「键=帖子 ID 的 dict」，直接 `for t in d` 迭代会拿到
    字符串键、随即 `TypeError: string indices must be integers`。读取端一律走这里。
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

    for p in paths:
        if os.path.exists(p):
            eat(json.load(open(p, encoding='utf-8')))
    return recs


def media_items(t):
    """从一条记录里取 (kind, url) 列表。兼容 X 的 media 字典与 Reddit 的散字段。"""
    m = t.get('media') or {}
    items = []
    if isinstance(m, dict):
        for k, arr in m.items():
            for it in (arr if isinstance(arr, list) else []):
                u = it if isinstance(it, str) else (
                    it.get('media_url_https') or it.get('media_url') or it.get('url') or '')
                if u:
                    items.append((k, u))
    elif isinstance(m, list):
        for it in m:
            u = it if isinstance(it, str) else (it.get('media_url_https') or it.get('url') or '')
            if u:
                items.append(('photo', u))
    if not items:
        # 兜底：原始记录没归一化过（media 为空但 Reddit 图在散字段里）
        for it in ((t.get('preview') or {}).get('images') or []):
            u = (it.get('source') or {}).get('url')
            if u:
                items.append(('photo', u))
        u = t.get('url_overridden_by_dest') or ''
        if isinstance(u, str) and u.lower().split('?')[0].endswith(IMG_EXT):
            items.append(('photo', u))
    return items


def prep_url(u):
    """按域名决定要不要追加 X 的高清参数。"""
    low = u.lower()
    if 'redd.it' in low or 'reddit' in low or 'imgur' in low:
        return u
    return u.split('?')[0] + '?format=jpg&name=large'


def pull(url, out_path):
    """先代理后直连地下一张图；返回 (ok, 说明)。"""
    host = url.split('//')[-1].split('/')[0]
    hint = CHANNEL_HINT.get(host)
    proxy, direct = ['-x', PROXY], []
    if hint == 'direct':
        order = [(direct, 45), (proxy, 12)]
    elif hint == 'proxy':
        order = [(proxy, 45), (direct, 12)]
    else:
        order = [(proxy, 45), (direct, 12)] if USE_PROXY_FIRST else [(direct, 45), (proxy, 12)]
    last = ''
    for extra, tmo in order:
        for attempt in range(2):
            p = subprocess.run(['curl', '-sS', '-L', *extra, '-o', out_path,
                                '-w', '%{http_code} %{size_download}', '--max-time', str(tmo), url],
                               capture_output=True, text=True)
            last = (p.stdout or '').strip() or (p.stderr or '')[:80]
            if last.startswith('200') and os.path.exists(out_path) and os.path.getsize(out_path) > 3000:
                CHANNEL_HINT[host] = 'proxy' if extra else 'direct'
                return True, last
            if attempt == 0:
                time.sleep(1.5)
    if os.path.exists(out_path):
        try:
            os.remove(out_path)
        except OSError:
            pass
    return False, last


recs = flatten(POOL)
sel = json.load(open('/tmp/cb_sel.json'))
os.makedirs('/tmp/cbx_imgs', exist_ok=True)
os.makedirs('/tmp/cbx_imgs_small', exist_ok=True)

out = {}
for i, r in enumerate(sel):
    items = media_items(recs.get(r['tid']) or {})[:MAX_IMG]
    got = []
    for j, (kind, u) in enumerate(items):
        # 文件名一律以 post id 为键（不要用选中顺序的序号）：案例编号会随筛选变化，
        # 序号命名会让图片与案例错位，而 tid 永远对得上。
        f = '/tmp/cbx_imgs/%s_%d.jpg' % (r['tid'], j + 1)
        s = '/tmp/cbx_imgs_small/%s_%d.jpg' % (r['tid'], j + 1)
        ok, info = pull(prep_url(u), f)
        if ok:
            subprocess.run(['sips', '-Z', '330', f, '--out', s], capture_output=True, text=True)
            got.append({'kind': kind, 'url': u, 'file': f, 'small': s})
        else:
            print('FAIL %s_%d %s %s' % (r['tid'], j + 1, info, u[:70]), flush=True)
    out[r['tid']] = got
    print('%02d %-17s %d' % (i + 1, r['sn'], len(got)), flush=True)
json.dump(out, open('/tmp/cbx_media.json', 'w'), ensure_ascii=False, indent=1)
posts_with_img = sum(1 for v in out.values() if v)
print('posts with image:', posts_with_img, 'files:', sum(len(v) for v in out.values()))
if out and not posts_with_img:
    print('!! 全池 0 张图：先回原始 JSON 里找 media 字段（X 是 {photo:[…],video:[…]} 字典，'
          'Reddit 在 preview.images / url_overridden_by_dest），确认是不是读取端形状没兼容；'
          '确认字段存在却下载失败，再去看图床是否需要代理（X 的 pbs.twimg.com 直连不通）。')
print('（Reddit 帖无图是正常的：讨论型帖子常不带图；有图的多是后台截图，OCR 里会有数字）')
