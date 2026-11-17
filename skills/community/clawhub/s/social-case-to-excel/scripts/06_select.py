# -*- coding: utf-8 -*-
"""第 3 步：把候选池过一遍，定最终案例清单 → `/tmp/cb_sel.json`（后面所有步骤的对齐基准）。

**这一步是人工/AI 判断，脚本只做搬运。** 先读 `/tmp/cbx_new.txt`（`05_screen.py` 产出的
可读清单），按下面的口径挑，再把挑中的 (主题, 序号, 作者) 填进 `SEL`。

判断口径（按重要性排序）：
  1. 有具体数字：金额、百分比、件数、转化率。没有数字的经验帖降级或剔除。
  2. 有可复制方法：能拆成 ①②③ 的步骤，而不是「坚持就会成功」这类结论。
  3. 主体明确：谁做的（账号/店铺/品牌）、做什么类目、多久。
  4. 排重：同一作者、同一爆款、同一事件的多个帖子只留信息量最大的那条。

Reddit 特有的两条：
  * **案例帖普遍比 X 长**（复盘体），所以 `text` 动辄几千字符——入选后「方法拆解」的提炼工作量
    比 X 大，别按 X 的习惯估工期。
  * **r/ 发帖常有配图**（后台截图、GSC/Ads 面板），这些图里的数字是重要事实来源，
    第 4 步要用 OCR 读出来（见 `ocr.swift`）。

优先级 S/A/B/C 在这一步就分好，**不要留空档**（44 条全落 A/B、S=0 会让「口径与说明」
自打脸，也说明分档没起作用）。升档会改变线内排序与编号，所以必须在 QA 之前做。
"""
import json, os, re

SHORT2 = '/tmp/cbx_short2.json'
SHORT1 = '/tmp/cbx_short.json'
POOL = ['/tmp/cbx1_all.json', '/tmp/cbx2_all.json', '/tmp/cbx3_all.json', '/tmp/cbx4_all.json']

# ---- 入选清单（每批重写这一段）--------------------------------------------------
# ('主题', 'o<n>' 或 'n<n>', '作者')  o<n> = cbx_short.json 的第 n 条（上一批）
#                                    n<n> = cbx_short2.json 的新增条目第 n 条
# 推荐做法：先跑一次本脚本（SEL 留空）只生成 cbx_new.txt 供挑选，填完再跑一次。
SEL = [
    # ('选品',      'n3',  'some_author'),
    # ('黑五营销',  'n7',  'another_author'),
]
# --------------------------------------------------------------------------------


def flatten(paths):
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


short2 = json.load(open(SHORT2))
old_rows = json.load(open(SHORT1)) if os.path.exists(SHORT1) else []
old = {r['tid'] for r in old_rows}
new = [r for r in short2 if r['tid'] not in old]
by_tid = {r['tid']: r for r in short2}

if not SEL:
    print('SEL 为空 —— 本次只生成挑选用的清单，不产出入选池。')
    print('候选池：short2=%d 条（其中新增 %d 条）' % (len(short2), len(new)))
    print('阅读 /tmp/cbx_new.txt，把 (主题, 序号, 作者) 填回本脚本的 SEL 再跑一次。')
    raise SystemExit(0)

picked, miss = [], []
for theme, key, sn in SEL:
    arr, idx = (old_rows, int(key[1:])) if key[0] == 'o' else (new, int(key[1:]))
    if idx >= len(arr):
        miss.append((theme, key, sn, 'INDEX-OUT-OF-RANGE'))
        continue
    r = arr[idx]
    if r['sn'] != sn:
        miss.append((theme, key, sn, r['sn']))     # 序号漂了，别硬跑——图会错位
    r = dict(r); r['theme_sel'] = theme
    picked.append(r)
print('picked', len(picked), 'mismatch', miss)
if miss:
    print('!! 有作者对不上的条目：说明 cbx_new.txt 的序号与本脚本读的不是同一份候选池，'
          '先重新生成候选池再挑，不要带着 mismatch 往下走（图片与案例会错位）。')
json.dump(picked, open('/tmp/cb_sel.json', 'w'), ensure_ascii=False, indent=1)

# 完整原始正文（含 media）——人工读案例时用
recs = flatten(POOL)
L = []
for i, r in enumerate(picked):
    t = recs.get(r['tid']) or {}
    txt = (t.get('text') or '')
    L.append('=' * 70)
    L.append('[%02d] %s | %s | r/%s | %s | theme=%s | score=%s comments=%s' % (
        i + 1, r['tid'], r['sn'], t.get('subreddit') or r.get('sub') or '',
        (r.get('created') or '')[:16], r['theme_sel'], r.get('fav'), r.get('rp')))
    L.append(txt)
    med = (t.get('media') or {})
    # media 是「值是列表的字典」（X 形状）：{"photo": [{...}], "video": [{...}]}；
    # Reddit 的图在 norm_post() 里已被归一化进 photo。不要按 photos/images/urls 取键。
    if isinstance(med, dict):
        flat = []
        for k, arr in med.items():
            for it in (arr if isinstance(arr, list) else []):
                flat.append(it)
        med = flat
    if med:
        L.append('--- media: %d' % len(med))
        for m in med:
            u = m if isinstance(m, str) else (m.get('media_url_https') or m.get('url') or m.get('media_url') or '')
            if u:
                L.append('    %s' % u)
    if t.get('post_url'):
        L.append('url: %s' % t['post_url'])
    L.append('len(text)=%d' % len(txt))
open('/tmp/cb_sel.txt', 'w').write('\n'.join(L))
print('-> /tmp/cb_sel.txt', len('\n'.join(L)))
