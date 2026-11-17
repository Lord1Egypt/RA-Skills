# -*- coding: utf-8 -*-
"""probe 03：原始抓取记录体检 —— 字段覆盖、去重后的总数、media/entities 结构。

原版把四个原始文件路径硬编码成 list 字面量，多轮抓取（8 个文件）时会崩。
现在用 glob（可用 argv / QA_RAW_GLOB 覆盖），并对原始文件为空的 key 做兜底。

用法：python3 probe_03_raw_records_sanity.py ['/tmp/bf/bf*_all.json']
"""
import glob, json, os, sys
from collections import Counter

RAW_GLOB = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get('QA_RAW_GLOB')) or '/tmp/cb*_all.json'
paths = sorted(glob.glob(RAW_GLOB))
if not paths:
    sys.exit('没匹配到原始抓取文件：%s（用 argv 或 QA_RAW_GLOB 指定）' % RAW_GLOB)

recs, per_file, keys = {}, [], Counter()
for p in paths:
    d = json.load(open(p, encoding='utf-8'))
    n = 0
    # 结构兼容：X 的 {label: {tweets: [...]}}，以及 ClaudeBaby Reddit 返回这类「文件本身就是帖子 list」
    # 或 {label: [...]}。以前只认 blk['tweets']，换数据源后每文件都数成 0 条，
    # 探针看着「通过」其实什么都没检查——所以下面同时清点、并在 0 条时显式告警。
    def eat(obj):
        global n
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == 'tweets' and isinstance(v, list):
                    for t in v:
                        take(t)
                else:
                    eat(v)
        elif isinstance(obj, list):
            for v in obj:
                if isinstance(v, dict) and (v.get('tweet_id') or v.get('id') or v.get('name')):
                    take(v)
                else:
                    eat(v)

    def take(t):
        global n
        tid = str(t.get('tweet_id') or t.get('id') or t.get('name') or '')
        if not tid:
            return
        n += 1
        keys.update(t.keys())
        recs.setdefault(tid, t)

    eat(d)
    per_file.append((os.path.basename(p), n))
print('原始文件 %d 个，抓取记录 %d 条，去重后唯一 %d 条' % (len(paths), sum(x[1] for x in per_file), len(recs)))
if sum(x[1] for x in per_file) == 0:
    print('!! 所有原始文件都摊平出 0 条 —— 本探针的结论无意义。')
print('每文件：%s' % per_file)
print('字段覆盖（出现次数 / 总记录）：%s' % {k: v for k, v in keys.most_common()})
with_media = sum(1 for t in recs.values() if t.get('media'))
print('有 media 字段且非空：%d / %d（media 为空是正常的，不要当 bug 修）' % (with_media, len(recs)))
print('语种分布：%s' % dict(Counter(t.get('lang') or '?' for t in recs.values()).most_common(6)))
