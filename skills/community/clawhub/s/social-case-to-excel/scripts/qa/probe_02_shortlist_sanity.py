# -*- coding: utf-8 -*-
"""probe_02：shortlist（05_screen 产出） sanity —— 本轮新增/覆盖了哪些条目。

用法：
  python3 probe_02_shortlist_sanity.py [short2.json] [short.json]

默认读 /tmp/cbx_short2.json（05_screen 的产出）与 /tmp/cbx_short.json（上一轮的产出，
不存在就当作空）。只做展示：把"本轮新增"的条目按序打印出来，方便人眼扫一遍有没有
明显跑偏的（标题党、纯求助帖、无关赛道）。

注意：早期版本这里硬编码了一批 X 账号名（某批交付的"目标账号"）去筛，换数据源/换话题
就完全失效还容易误导。现在改成平台无关——只按 fav 降序列出新增条目的
`subreddit / 作者 / 赞 / 正文开头`，具体该留意什么由读的人判断。
"""
import json
import os
import sys

S2 = sys.argv[1] if len(sys.argv) > 1 else '/tmp/cbx_short2.json'
S1 = sys.argv[2] if len(sys.argv) > 2 else '/tmp/cbx_short.json'

s2 = json.load(open(S2, encoding='utf-8'))
old = set()
if os.path.exists(S1):
    old = {r['tid'] for r in json.load(open(S1, encoding='utf-8'))}
new = [r for r in s2 if r['tid'] not in old]
print('short2 %d 条 | 上一版 %d 条 | 本轮新增 %d 条' % (len(s2), len(old), len(new)))

for i, r in enumerate(sorted(new, key=lambda x: -x.get('fav', 0))[:40]):
    print('[%2d] f%-6s r/%-18s %-20s %s' % (
        i, r.get('fav'), (r.get('sub') or '')[:18], (r.get('sn') or '')[:20],
        (r.get('text') or '')[:70].replace('\n', ' ')))
print('\n主题分布：')
dist = {}
for r in s2:
    for t in (r.get('theme') or ['(无)']):
        dist[t] = dist.get(t, 0) + 1
for k, v in sorted(dist.items(), key=lambda kv: -kv[1]):
    print('  %-14s %d' % (k, v))
