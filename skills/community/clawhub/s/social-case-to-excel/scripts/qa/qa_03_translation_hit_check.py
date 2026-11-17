# -*- coding: utf-8 -*-
"""QA：按关键词/年份定位上下文，逐条人工核对译文是否失真。

原版把某个 tid 硬编码在脚本里，换话题就 KeyError（踩过）。现在遍历全部入选帖：
给一个正则（默认年份 202x，可用 argv[1] 换），打印命中处的上下文，用来确认
「原帖里的 2024」确实被当成年份、而不是被当成业务数字写进案例文本。
"""
import json, re, sys

sel = json.load(open('/tmp/cb_sel.json', encoding='utf-8'))
rows = sel if isinstance(sel, list) else sel.get('rows', sel)
T = {r['tid']: (r.get('text', '') or '') for r in rows}
PAT = sys.argv[1] if len(sys.argv) > 1 else r'(?<![\d])20(?:2[0-6])(?![\d])'
money = re.compile(r'[\$€£]\s?\d|\d+\s?(?:bn|million|billion|%|K|M|B)\b')

n = 0
for r in rows:
    t = T.get(r['tid'], '')
    for m in re.finditer(PAT, t):
        seg = t[max(0, m.start() - 70):m.end() + 70].replace('\n', ' ')
        # 只在「年份与金额同现」时打印，避免刷屏
        if PAT == r'(?<![\d])20(?:2[0-6])(?![\d])' and not money.search(seg):
            continue
        n += 1
        print('@%-17s | …%s…' % (r.get('sn', '?'), seg))
print('命中 %d 处（默认口径只打印年份与金额同现的位置，属正常语境）' % n)
