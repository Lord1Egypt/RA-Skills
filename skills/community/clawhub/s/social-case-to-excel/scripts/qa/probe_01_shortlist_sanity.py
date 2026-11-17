# -*- coding: utf-8 -*-
"""probe 01：候选池（shortlist）体检 —— 去重、文本完整度、入选是否都在池里。

原版硬编码了 old[69] / old[163] 这类下标，池子长度一变就 IndexError（踩过）。
现在只看统计，不依赖任何固定下标。

用法：python3 probe_01_shortlist_sanity.py [shortlist.json ...]
      不传参则用环境变量 QA_SHORT 或默认 /tmp/cbx_short.json
"""
import json, os, sys
from collections import Counter

SHORT = os.environ.get('QA_SHORT') or '/tmp/cbx_short.json'
paths = sys.argv[1:] or [SHORT]
for p in paths:
    if not os.path.exists(p):
        print('skip（不存在）：%s' % p)
        continue
    d = json.load(open(p, encoding='utf-8'))
    rows = d if isinstance(d, list) else d.get('rows', d)
    tids = [str(r.get('tid') or r.get('tweet_id') or '') for r in rows]
    dups = [k for k, v in Counter(tids).items() if v > 1]
    empty = [t for t, r in zip(tids, rows) if not (r.get('text') or '').strip()]
    short = [t for t, r in zip(tids, rows) if len(r.get('text') or '') < 120]
    print('%s：%d 条 | 唯一 tid %d | 重复 %d %s' % (p, len(rows), len(set(tids)), len(dups), dups[:5]))
    print('   空文本 %d | 短于 120 字 %d | 语种 %s' % (
        len(empty), len(short), dict(Counter(r.get('lang') or '?' for r in rows).most_common(5))))
    if rows:
        lens = sorted(len(r.get('text') or '') for r in rows)
        print('   文本长度 min/中位/max = %d / %d / %d' % (lens[0], lens[len(lens) // 2], lens[-1]))
        med = lens[len(lens) // 2]
        # 列表模式抓取（批量列表模式 这类）会把简介静默截断，落盘的 text 短得
        # 不像正文。这里不做判定，只把「短到可疑」的挑出来给人工确认——正文本身就短的
        # 帖子真实存在，误报成结论反而误导（详见 pipeline.md 6.0.4）。
        tiny = sorted(((str(r.get('tid') or r.get('tweet_id') or ''), len(r.get('text') or ''))
                       for r in rows if len(r.get('text') or '') < 300), key=lambda x: x[1])
        if tiny and med >= 600:
            print('   ?? 短文本 %d 条（<300 字，中位 %d）：逐条确认是「原文就短」还是「列表模式截断」；'
                  '若是截断，用详情（desc_full）回填 text 后重跑入选再进 QA。清单：%s'
                  % (len(tiny), med, tiny[:6]))
