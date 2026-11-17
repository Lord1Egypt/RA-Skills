# -*- coding: utf-8 -*-
import json
sel = json.load(open('/tmp/cb_sel.json', encoding='utf-8'))
rows = sel if isinstance(sel, list) else sel.get('rows', sel)
MAN, POST = {}, {}
for f in ['/tmp/tcb%d.py' % i for i in range(1, 7)]:
    ns = {}
    exec(open(f, encoding='utf-8').read(), ns)
    MAN.update(ns.get('MAN', {}))
    POST.update(ns.get('POST', {}))
print('cases', len(rows), 'MAN', len(MAN), 'POST', len(POST))
miss_m, miss_p = [], []
for r in rows:
    t = r['tid']
    th = r.get('theme')
    th = '/'.join(th) if isinstance(th, list) else str(th)
    txt = r.get('text', '') or ''
    cjk = sum(1 for ch in txt if '\u4e00' <= ch <= '\u9fff')
    zh = cjk > len(txt) * 0.15
    if t not in MAN and not zh:
        miss_m.append((th, t, (r.get('line') or '')[:30]))
    if t not in POST:
        miss_p.append((th, t, (r.get('line') or '')[:30]))
print('MISSING MAN:', miss_m)
print('MISSING POST:', miss_p)
print('avg POST len', sum(len(POST.get(t, '')) for t in [r['tid'] for r in rows]) // len(rows))
