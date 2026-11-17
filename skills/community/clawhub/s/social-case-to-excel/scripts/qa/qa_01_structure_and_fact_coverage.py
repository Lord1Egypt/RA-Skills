# -*- coding: utf-8 -*-
"""QA：结构 + 数字级事实覆盖"""
import json, re, glob
from openpyxl import load_workbook

sel = json.load(open('/tmp/cb_sel.json', encoding='utf-8'))
rows = sel if isinstance(sel, list) else sel.get('rows', sel)
bytid = {r['tid']: r for r in rows}

MAN, POST = {}, {}
for f in ['/tmp/tcb%d.py' % i for i in range(1, 7)]:
    ns = {}
    exec(open(f, encoding='utf-8').read(), ns)
    MAN.update(ns.get('MAN', {}))
    POST.update(ns.get('POST', {}))

XLSX = '/tmp/social-case-to-excel-example/跨境电商案例拆解库_X_选品-黑五-关键词-Listing-站外-Reddit_20260916.xlsx'
MD = '/tmp/social-case-to-excel-example/跨境电商案例研究_42条_20260916.md'
wb = load_workbook(XLSX)
print('--- sheets ---')
for ws in wb.worksheets:
    print(ws.title, ws.max_row, 'x', ws.max_column, '| freeze', ws.freeze_panes, '| filter', bool(ws.auto_filter.ref))
ws1 = wb['1-案例总表']
print('--- sheet1 header ---')
hdr = [c.value for c in ws1[1]]
print(len(hdr), hdr)
print('--- 优先级/所属线/编号 分布 ---')
from collections import Counter
pr, th = Counter(), Counter()
nums = []
bad = []
for r in range(2, ws1.max_row + 1):
    pr[ws1.cell(r, 2).value] += 1
    th[ws1.cell(r, 3).value] += 1
    nums.append(ws1.cell(r, 1).value)
    for c in range(1, 24):
        v = ws1.cell(r, c).value
        if c in (20, 21):
            continue
        if v is None or (isinstance(v, str) and not v.strip()):
            bad.append((r, hdr[c-1]))
print('优先级', dict(pr))
print('所属线', dict(th))
print('编号', nums[:5], '...', nums[-3:], 'unique', len(set(nums)))
print('空单元格(非图片列):', len(bad), bad[:8])
print('图片数 sheet1:', len(getattr(ws1, '_images', [])))

# 数字级事实覆盖（正向 = 原帖数字有没有写进中文写作列）。
#
# 按「数值」比，不按「字符串」比：5x 与 5 倍、500k 与 50 万、4.1x 与 4.1 倍是同一个事实。
# 按字符串比会报大量格式假差异——上一轮 70 条"缺失"里 69 条是这种，剩下 1 条是短链里的数字，
# 结果是审查者要花几十分钟逐条排除，真正漏写的反而不容易看见。
#
# 过滤规则（都是实测出来的噪音源）：短链 t.co/… 与 @handle 里的数字不是业务数字；年限
# 1900–2100 的裸整数是年份；1000 以下的裸整数多半是序号（「7. Most…」）。带单位或 % 的
# 数字则全部保留——它们才是这条案例的价值所在。
#
# 单位必须紧贴数字：文本里的「1. Mapped the…」「2. Built…」「2 MONTHS」「500 keywords」
# 都会被宽松的正则读成 1M / 2B / 2M / 500k —— 上一轮 7 条假报里有 6 条是这么来的。
# 中文单位（万/亿）允许有空格，英文的 k/K/M/B 不允许。
#
# 反向核对（中文里出现、原帖却没有的数字，用来抓写错量级/张冠李戴）在 qa_09。
UNIT = {'亿': 1e8, '千万': 1e7, '百万': 1e6, '十万': 1e5, '万': 1e4, '千': 1e3,
        'k': 1e3, 'K': 1e3, 'M': 1e6, 'B': 1e9, 'billion': 1e9, 'million': 1e6, 'bn': 1e9}
NRE = re.compile(r'(?<![\d,.])(\d[\d,]*(?:\.\d+)?)'
                 r'(?:\s*(亿|千万|百万|十万|万|千)|(million|billion|bn|[kKMB])(?![A-Za-z]))?')
NOISE = re.compile(r'https?://\S+|t\.co/\S+|@\w+')
CJK = re.compile(r'[\u4e00-\u9fff]')


def values(t):
    """→ 绝对值集合；带单位/百分号的都收，裸大数收 1000+（排除年份）。"""
    out = set()
    clean = NOISE.sub(' ', t)
    for m in NRE.finditer(clean):
        core = m.group(1).replace(',', '')
        if not re.fullmatch(r'\d+(\.\d+)?', core):
            continue
        f = float(core)
        suf = (m.group(2) or m.group(3) or '')
        if clean[m.end():m.end() + 1] == '%':      # 百分号写在同一 token 后面的情况
            if f >= 1:
                out.add(round(f, 4))
            continue
        if suf:
            out.add(round(f * UNIT[suf], 4))
            continue
        if f >= 1000 and not (1900 <= f <= 2100 and f == int(f)):
            out.add(round(f, 4))
    return out


def hit(v, pool):
    return any(abs(v - h) <= max(1e-9, 0.01 * max(abs(v), abs(h))) for h in pool)


miss_report = []
tot_miss = 0
zh_orig = 0                                     # 原帖即中文的条数（中文列就是原文）
for c in rows:
    tid = c['tid']
    orig = c.get('text', '') or ''
    have = (MAN.get(tid, '') or '') + '\n' + (POST.get(tid, '') or '')
    # 中文原帖没有译文，中文写作列就是原帖本身 —— 不把原文算进来会把它的数字全报成缺失
    if len(CJK.findall(orig)) > len(orig) * 0.15:
        zh_orig += 1
        have += '\n' + orig
    pool = values(have)
    miss = sorted(v for v in values(orig) if not hit(v, pool))
    if miss:
        tot_miss += len(miss)
        miss_report.append((tid, c.get('line') if isinstance(c.get('line'), str) else '', miss[:12]))
print('--- 数字覆盖（正向，按数值比 · 1% 容差；反向核对看 qa_09）---')
print('原文即中文、已按原文核对：%d 条' % zh_orig)
print('缺失总数', tot_miss, '/ 案例数', len(miss_report))
for tid, line, miss in miss_report[:15]:
    print(' ', tid, line[:24], miss)
md = open(MD, encoding='utf-8').read()
print('--- markdown ---', len(md), 'chars | 案例数', md.count('\n## 案例 '))
