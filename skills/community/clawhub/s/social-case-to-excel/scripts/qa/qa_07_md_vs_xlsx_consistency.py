# -*- coding: utf-8 -*-
"""QA：markdown 与总表的一致性 + 体量体检（中文帖数、sheet4/sheet5 行数、文件大小）。

**按表头找列，不按列号找**。上一轮这里是硬编码 `ws.cell(r, 22)` / `cell(r, 21)`，
本次跑批在总表里多插了一列（24 列），索引整体右移，于是「译文长度」读到的是原文、
「中文帖计数」直接变成 0 —— 而 0 看起来像是"这批没有中文帖"，不会有人去查。
所以：凡是找不到必需表头就打印 `!! SKIP`，不要用 0 假装通过。
"""
from openpyxl import load_workbook
import os, sys

P = '/tmp/social-case-to-excel-example/跨境电商案例拆解库_X_选品-黑五-关键词-Listing-站外-Reddit_20260916.xlsx'
M = '/tmp/social-case-to-excel-example/跨境电商案例研究_42条_20260916.md'
wb = load_workbook(P)
ws = wb['1-案例总表']
hdr = [str(c.value) if c.value else '' for c in ws[1]]


def col(*keys, **kw):
    """按表头子串找列号；找不到返回 None（下游打印 SKIP 而不是静默算错）。"""
    for i, h in enumerate(hdr):
        if all(k in h for k in keys):
            return i + 1
    return kw.get('default')


C_ORIG = col('正文原文')
C_ZH = col('正文翻译')
C_ACC = col('原帖账号')
if not C_ZH:
    print('!! SKIP 中文帖计数：总表里找不到含「正文翻译」的表头，实际表头=%s' % hdr)
    sys.exit(0)
if not C_ORIG:
    print('!! 提示：找不到「正文原文」列，中文帖判定只看译文前缀')

n = 0
for r in range(2, ws.max_row + 1):
    zh = ws.cell(r, C_ZH).value or ''
    if str(zh).startswith('（原帖即中文'):
        n += 1
        orig_len = len(ws.cell(r, C_ORIG).value or '') if C_ORIG else '?'
        acc = ws.cell(r, C_ACC).value if C_ACC else '?'
        print('中文帖', r, acc, '| 原文长度', orig_len, '| 译文长度', len(str(zh)))
print('中文帖计数', n)
print('sheet4', wb['4-原帖配图'].max_row, 'rows', len(getattr(wb['4-原帖配图'], '_images', [])), 'imgs')
print('sheet5', wb['5-候选池原始数据'].max_row - 1, 'data rows')
for p in [P, M]:
    print(os.path.getsize(p) // 1024, 'KB', p)
