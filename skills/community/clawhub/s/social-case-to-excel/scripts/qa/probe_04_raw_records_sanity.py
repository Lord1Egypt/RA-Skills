# -*- coding: utf-8 -*-
"""probe 04：media 结构确认 —— 打印若干条真实样本，确认是「值是列表的字典」。

这一步的意义：抽图前先看清结构（photo / video / 空），否则容易写出
`media.get('photos')` 这种取不到图、但也不报错的代码（踩过）。
用法：python3 probe_04_raw_records_sanity.py ['/tmp/bf/bf*_all.json'] [条数]
"""
import glob, json, os, sys

RAW_GLOB = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get('QA_RAW_GLOB')) or '/tmp/cb*_all.json'
N = int(sys.argv[2]) if len(sys.argv) > 2 else 4
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
shown = 0
for tid, t in recs.items():
    m = t.get('media')
    if not m:
        continue
    print('@%-17s %s' % (t.get('screen_name'), json.dumps(m, ensure_ascii=False)[:400]))
    shown += 1
    if shown >= N:
        break
print('（结构形如 {"photo": [{media_url_https, id, sizes}]} 或 {"video": [{media_url_https: 封面, variants: [...]}]}）')
