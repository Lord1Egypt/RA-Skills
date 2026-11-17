# -*- coding: utf-8 -*-
"""QA：逐条把原帖与案例文本对照（打印数字上下文），人工确认没有失真。

原版把两个 tid 和要查的数字硬编码在脚本里（换话题就 KeyError，踩过两次）。
现在遍历全部入选帖，默认对「4 位以上数字」在原文里的每一次出现打上下文——
长帖会刷屏，所以支持 argv 过滤：`python3 qa_08_source_diff_per_case.py <tid前缀或账号名>`。

注意：对齐用的是入选池里的 text（由 00_prep_qa.py 从原始记录回填），不是 xlsx 单元格，
所以这里看到的就是原帖原文本身。
"""
import json, re, sys

sel = json.load(open('/tmp/cb_sel.json', encoding='utf-8'))
rows = sel if isinstance(sel, list) else sel.get('rows', sel)
only = sys.argv[1] if len(sys.argv) > 1 else ''
PAT = re.compile(r'\d[\d,]{3,}|\d+(?:\.\d+)?\s?%|[\$€£]\s?\d[\d,\.]*')

shown = 0
for r in rows:
    tid = str(r.get('tid', ''))
    sn = r.get('sn', '?')
    if only and only not in tid and only.lower() not in str(sn).lower():
        continue
    t = r.get('text', '') or ''
    print('=' * 20, tid, '@' + str(sn))
    for m in PAT.finditer(t):
        seg = t[max(0, m.start() - 90):m.end() + 90].replace('\n', ' ')
        print('   [%s] …%s…' % (m.group(0).strip(), seg))
        shown += 1
print('共打印 %d 处数字上下文（对照案例文本逐条确认；可用 argv 指定 tid/账号只看一条）' % shown)
