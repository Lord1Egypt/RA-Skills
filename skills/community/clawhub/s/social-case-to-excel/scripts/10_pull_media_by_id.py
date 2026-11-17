# -*- coding: utf-8 -*-
"""第 4 步 · 按 post id 重拉配图（推荐用这个，而不是 07 的首次下载）。

**为什么要有第二次拉图**：首次下载用的是"当时的筛选顺序"，一旦案例编号/入选顺序变了，
图片就会与案例错位（踩过：把 A 案例的截图当成 B 案例的配图）。所以规矩是
**图片一律以 post id 为键**，并在交付前用 id 再拉一遍核对。

本脚本还会做一件重要的事：把**入选池顺序**与**markdown 案例顺序**对齐核验
（`--md` 给 markdown 路径时），不一致就报出来——顺序漂了会让「编号」与「配图」对不上。

用法：
  python3 10_pull_media_by_id.py                                  # 重拉入选池全部
  python3 10_pull_media_by_id.py --md '/path/案例研究_40条.md'      # 顺带核验顺序
  python3 10_pull_media_by_id.py --tids 1nqx17e,2abcd3            # 只拉指定的几个 id
"""
import argparse, glob, json, os, re, subprocess, sys, time

PROXY = os.environ.get('MEDIA_PROXY', 'http://127.0.0.1:7897')
USE_PROXY_FIRST = os.environ.get('NO_PROXY') != '1'
POOL = ['/tmp/cbx1_all.json', '/tmp/cbx2_all.json', '/tmp/cbx3_all.json', '/tmp/cbx4_all.json']
OUTDIR = '/tmp/cb_imgs_byid'
IMG_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.webp')


def flatten(paths):
    """摊平原始抓取 JSON 成 {帖子ID: record}，兼容 list / {label:{tweets}} / {id:record}。

    自建平台抓取脚本常把结果落成「键=帖子 ID 的 dict」，对 dict 直接迭代会拿到字符串键，
    紧接着 `t.get(...)` 就报 `TypeError: string indices must be integers`。
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


def media_urls(t):
    m = t.get('media') or {}
    urls = []
    if isinstance(m, dict):
        for _k, arr in m.items():
            for it in (arr if isinstance(arr, list) else []):
                u = it if isinstance(it, str) else (it.get('media_url_https') or it.get('url') or '')
                if u:
                    urls.append(u)
    elif isinstance(m, list):
        for it in m:
            u = it if isinstance(it, str) else (it.get('media_url_https') or it.get('url') or '')
            if u:
                urls.append(u)
    if not urls:
        for it in ((t.get('preview') or {}).get('images') or []):
            u = (it.get('source') or {}).get('url')
            if u:
                urls.append(u)
        u = t.get('url_overridden_by_dest') or ''
        if isinstance(u, str) and u.lower().split('?')[0].endswith(IMG_EXT):
            urls.append(u)
    return urls


def prep_url(u):
    low = u.lower()
    if 'redd.it' in low or 'reddit' in low or 'imgur' in low:
        return u
    return u.split('?')[0] + '?format=jpg&name=large'


CHANNEL_HINT = {}  # host -> 'proxy' / 'direct'：记住这个域名走哪条通道，别每次从头试


def pull(url, out_path):
    """先代理后直连地下图；按域名记住哪条通道能用。

    X 的图床（pbs.twimg.com）直连必然超时，而 curl 的 --max-time 是硬等的：一条 45 秒，
    一批 50 张就能白等半小时。所以这里做两件事——(1) 同一个域名首次成功后记下通道并优先后用，
    (2) 备选通道给短超时（12 秒），它基本不会成功，不值得陪它等满 45 秒。
    同一通道内重试 2 轮：代理偶发 000/空包，一次失败就记 FAIL 会在交付里留下「这帖没配图」的假洞。
    """
    host = url.split('//')[-1].split('/')[0]
    hint = CHANNEL_HINT.get(host)
    proxy, direct = ['-x', PROXY], []
    if hint == 'direct' or not USE_PROXY_FIRST:
        order = [(direct, 45), (proxy, 12)]
    elif hint == 'proxy':
        order = [(proxy, 45), (direct, 12)]
    else:
        order = [(proxy, 45), (direct, 12)]
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sel', default='/tmp/cb_sel.json')
    ap.add_argument('--md', default='', help='markdown 交付物路径，用来核验案例顺序')
    ap.add_argument('--tids', default='', help='逗号分隔的 id 子集；默认重拉入选池全部')
    ap.add_argument('--outdir', default=OUTDIR)
    ap.add_argument('--pool', default='',
                    help='原始抓取 JSON，逗号分隔或 glob（如 "/tmp/cm/cm*_all.json"）；'
                         '不给就用 Reddit 跑批的默认 4 个 /tmp/cbx*_all.json。'
                         '换平台跑批时务必显式给这一项，否则会对着上一次的池子拉图。')
    a = ap.parse_args()
    pool = ([p for chunk in a.pool.split(',') for p in (glob.glob(chunk.strip()) or [chunk.strip()])
             if p] if a.pool else POOL)

    sel = json.load(open(a.sel, encoding='utf-8'))
    rows = sel if isinstance(sel, list) else sel.get('rows', sel)

    if a.md and os.path.exists(a.md):
        md = open(a.md, encoding='utf-8').read()
        order = re.findall(r'^## 案例 (\d+)｜.*?comments/([A-Za-z0-9]+)', md, re.M) \
            or re.findall(r'^## 案例 (\d+)｜.*?status/(\d+)', md, re.M)
        mismatch = [(no, tid, rows[i]['tid']) for i, (no, tid) in enumerate(order)
                    if i < len(rows) and str(rows[i]['tid']) != str(tid)]
        print('markdown cases:', len(order), 'sel rows:', len(rows), 'mismatch:', len(mismatch))
        if mismatch:
            print('!! 顺序不一致（编号 vs 配图会错位）：', mismatch[:6])
    elif a.md:
        print('（--md 不存在，跳过顺序核验）', a.md)

    tids = [x.strip() for x in a.tids.split(',') if x.strip()] or [str(r['tid']) for r in rows]
    recs = flatten(pool)
    print('pool:', len(pool), 'files | recs', len(recs), '| 待拉', len(tids))

    # 覆盖率先行：0 覆盖要往「取数端字段形状」上查，而不是先怀疑数据源不给图
    # （踩过：X 的 media 是 {photo:[…], video:[…], animated_gif:[…]} 的字典，
    #   把它当 list 迭代就得到 0 张，于是误判「这个数据源拿不到配图」。）
    with_media = [t for t in tids if media_urls(recs.get(t) or {})]
    no_rec = [t for t in tids if t not in recs]
    print('media coverage: %d/%d 条有配图 | 原始池里查不到记录 %d 条%s' % (
        len(with_media), len(tids) - len(no_rec), len(no_rec),
        ('（如：%s…）' % ','.join(no_rec[:3])) if no_rec else ''))
    if no_rec:
        print('!! 有 tid 在原始池里查不到：多半是 --pool 给少了（只喂了本次抓取的一部分），'
              '这些帖子会静默变成 NO-REC、交付时配图少几行。')
    if tids and not with_media:
        print('!! 0 覆盖：先检查取数端是否保留了 media 字段（键名可能是 media / photos / '
              'extended_entities），再怀疑图床可达性；不要直接断定「本批未抓取配图」。')
    os.makedirs(a.outdir, exist_ok=True)

    report, ok_n = [], 0
    for tid in tids:
        t = recs.get(tid)
        if not t:
            report.append((tid, 'NO-REC'))
            continue
        urls = media_urls(t)[:2]
        if not urls:
            report.append((tid, 'NO-MEDIA'))
            continue
        got = []
        for j, u in enumerate(urls):
            f = os.path.join(a.outdir, '%s_%d.jpg' % (tid, j + 1))
            ok, info = pull(prep_url(u), f)
            got.append((f, info, ok))
            ok_n += 1 if ok else 0
        report.append((tid, got))
    for r in report:
        print(r)
    print('本次成功下载 %d 张 → %s' % (ok_n, a.outdir))
    if ok_n == 0 and with_media:
        print('!! 有图 URL 但一张都没下来：先确认代理通不通（MEDIA_PROXY=%s，'
              'X 的图床必须走代理，直连会 000）；代理正常再去看要不要加 UA/Referer。' % PROXY)
    print('提示：文件名以 post id 为键，交付前用它对一遍 sheet4 的「原图链接」列。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
