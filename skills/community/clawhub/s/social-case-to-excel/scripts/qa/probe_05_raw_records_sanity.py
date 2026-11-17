# -*- coding: utf-8 -*-
"""probe 05：media 类型分布 —— 有多少条是 photo / video / 空，用来预估配图条数。

用法：python3 probe_05_raw_records_sanity.py ['/tmp/bf/bf*_all.json'] [入选池.json]
"""
import glob, json, os, sys
from collections import Counter

RAW_GLOB = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get('QA_RAW_GLOB')) or '/tmp/cb*_all.json'
SEL = (sys.argv[2] if len(sys.argv) > 2 else os.environ.get('QA_SEL')) or '/tmp/cb_sel.json'
paths = sorted(glob.glob(RAW_GLOB))
if not paths:
    sys.exit('没匹配到原始抓取文件：%s' % RAW_GLOB)

recs = {}
for p in paths:
    d = json.load(open(p, encoding='utf-8'))
    for lb, blk in (d.items() if isinstance(d, dict) else []):
        for t in (blk or {}).get('tweets', []):
            tid = str(t.get('tweet_id') or '')
            if tid:
                recs.setdefault(tid, t)

ids = list(recs)
if os.path.exists(SEL):
    d = json.load(open(SEL, encoding='utf-8'))
    rows = d if isinstance(d, list) else d.get('rows', d)
    ids = [str(r['tid']) for r in rows]
    print('按入选池 %d 条统计' % len(ids))
else:
    print('入选池不存在（%s），按全部 %d 条统计' % (SEL, len(ids)))

kinds, imgs = Counter(), 0
for tid in ids:
    m = (recs.get(tid) or {}).get('media')
    if isinstance(m, dict) and m:
        k = tuple(sorted(m.keys()))
        kinds[k] += 1
        imgs += sum(len(v) for v in m.values() if isinstance(v, list))
    elif isinstance(m, list) and m:
        kinds[('LIST', len(m))] += 1
        imgs += len(m)
    else:
        kinds[('EMPTY',)] += 1
for k, v in kinds.most_common():
    print('  %-22s %d' % (str(k), v))
print('可下载图片总数（含视频封面）：约 %d 张；无图 %d 条（正常）' % (imgs, kinds.get(('EMPTY',), 0)))
