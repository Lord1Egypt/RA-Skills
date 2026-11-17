# -*- coding: utf-8 -*-
"""QA2：数字核心（数值）覆盖，容忍格式差异。

**这一关是「字面包含」检查，不是数值检查**：把原文里每个数字 token 去掉逗号/空格后，
直接看它在「正文翻译 + 案例研究推文」里作为字符串出现过没有。所以它会把**中文惯用写法**
判成缺失，属已知假报，不要为它改内容：
  - 原文 "30K" 写成「3 万」→ 报缺 30（正确写法见下）
  - 原文 "$50k" 写成「五万美元」→ 报缺 50
  - 原文 "9 times out of 10" 写成「十次有九次」→ 报缺 9 / 10
  - 原文 "1.5k" 写成「1,500」→ 报缺 1500（两边其实等价）
  - 原文 "300,000" 写成「30 万」→ 报缺 300,000
  - URL 片段（?s=21&t=…）、电话/WhatsApp 号（+82 10-2688-3795）、「360° 拍摄」
权威的正向检查是 qa_01（数值归一化 + 容差）——先看 qa_01 的结论，再用本关兜底。

写数字的统一约定（同时满足 qa_01 与 qa_02）：
  1) 大额整数照原文写成阿拉伯数字带千分位：写 30,000 / 300,000，不写「3 万」「30 万」；
  2) 金额保留原帖符号与量级：写 $50k，不写「5 万美元」；原文写 5 万时照抄 5 万；
  3) 原作者笔误照抄并标注：写「$1000k+（原文如此）」，不要自行改成 $1,000；
  4) 由我们算出来的差值/比率要标注来源：写「差价 $15K（$40K−$25K，自算）」；
  5) 习惯语（9 out of 10）保留中文说法，但把数字带进去：写「10 次里有 9 次顾客看不到」。
"""
import json, re
sel = json.load(open('/tmp/cb_sel.json', encoding='utf-8'))
rows = sel if isinstance(sel, list) else sel.get('rows', sel)
MAN, POST = {}, {}
for f in ['/tmp/tcb%d.py' % i for i in range(1, 7)]:
    ns = {}
    exec(open(f, encoding='utf-8').read(), ns)
    MAN.update(ns.get('MAN', {}))
    POST.update(ns.get('POST', {}))

TOK = re.compile(r'\d[\d,\.]*')
def cores(t):
    out = {}
    for m in TOK.finditer(t):
        s = m.group(0).rstrip('.')
        digits = s.replace(',', '')
        try:
            f = float(digits)
        except Exception:
            continue
        out[digits + '|' + ('%' if t[m.end():m.end()+1] == '%' else '')] = s
    return out
def norm(s):
    return re.sub(r'[,\s]', '', s)
tot = 0
rep = []
for c in rows:
    tid = c['tid']
    orig = c.get('text', '') or ''
    have = norm((MAN.get(tid, '') or '') + '\n' + (POST.get(tid, '') or ''))
    miss = []
    for k, s in cores(orig).items():
        core = k.split('|')[0]
        if len(core) < 2 and float(core) < 3:
            continue
        if norm(s) not in have:
            miss.append(s)
    if miss:
        tot += len(miss)
        rep.append((tid, miss))
print('缺失数字项总数', tot, '涉及案例', len(rep))
for tid, miss in rep:
    print(' ', tid, miss[:14])
