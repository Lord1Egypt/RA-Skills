#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
联想扩散机检器 —— research-first skill 配套
判的不是「结论对不对」，是「你有没有偷懒只查一个方向」。

用法: python check_expansion.py <纪要.md>

期望纪要里有一个表：
    ### 联想扩散（D1–D9）
    | # | 方向 | 状态 | 检索词 | 找到了什么 |
    |---|---|---|---|---|
    | D1 | 术语邻居 | ✅ | ... | ... |
    | D5 | 反面/失败 | ❌未查 | — | — |

退出码: 0 = 全部方向都有交代（含显式标"未查"） / 1 = 有方向被漏掉 / 2 = 解析失败
⚠️ 标 ❌ 是合法的；要修的是「不标」。
"""
import sys
import os
import re
import importlib.util

# 复用 check_journal 的 strip_fences（⛔ 路径必须用 __file__ 推导，不能用 sys.path[0].replace，
# 那个写法会拼出错误路径然后被 except 静默吞掉 —— 静默降级必须告警）
_HERE = os.path.dirname(os.path.abspath(__file__))
try:
    _spec = importlib.util.spec_from_file_location('cj', os.path.join(_HERE, 'check_journal.py'))
    _cj = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_cj)
except Exception as e:
    print(f'⚠️ 未能复用 check_journal.strip_fences（{e}）→ 改用本文件内置的等价实现')
    _cj = None

DIRECTIONS = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9']
NAMES = {'D1': '术语邻居', 'D2': '权威源头', 'D3': '利益相关', 'D4': '前置依赖',
         'D5': '反面/失败', 'D6': '量化参数', 'D7': '同类替代',
         'D8': '跨域差异', 'D9': '原始材料'}
# 状态判定：**只认开头的标记符**，⛔ 不用子串匹配
# （2026-10-18 实测踩坑：原实现用 any(t in status)，
#  结果「⚠️ 被动」「⚠️ 部分」这类中间态既不命中已查也不命中未查 ⇒ 被误判成「状态列空着」。
#  与 check_journal 那次 `'结论' in line` 是同一个病：**判类别要匹配标记符本身，不要用子串**。）
def classify(status):
    """→ 'done' / 'partial' / 'notdone' / 'blank'"""
    s = status.strip()
    if s.startswith(('✅', '✔', '☑')):
        return 'done'
    if s.startswith(('⚠', '△')):
        return 'partial'      # 部分查到 / 被动撞见 —— 合法，但要单独统计
    if s.startswith(('❌', '✗', '☒')):
        return 'notdone'
    if any(t in s for t in ('未查', '没查', '未做', '跳过', '未检索')):
        return 'notdone'
    return 'blank'             # ⛔ 空白 = 等于没交代，最贵的漏检


def die(msg, code=2):
    print(f'⛔ {msg}')
    sys.exit(code)


def split_row(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def load_lines(path):
    with open(path, encoding='utf-8') as f:
        raw = f.read().splitlines()
    if _cj is not None:
        return _cj.strip_fences(raw)
    out, fence = [], False
    for i, ln in enumerate(raw, 1):
        if ln.lstrip().startswith('```'):
            fence = not fence
            continue
        if not fence:
            out.append((i, ln))
    return out


def main(path):
    try:
        lines = load_lines(path)
    except OSError as e:
        die(f'读不了文件: {e}')

    # 找含 D 编号的表头（'方向' 且 '状态'）
    rows = []
    for idx, (lineno, ln) in enumerate(lines):
        if not ln.lstrip().startswith('|'):
            continue
        cells = split_row(ln)
        norm = [c.replace('**', '').replace('*', '').replace('`', '').strip() for c in cells]
        if '方向' in norm and '状态' in norm:
            j = idx + 1
            if j < len(lines) and re.match(r'^\s*\|[\s:\-|]+\|\s*$', lines[j][1]):
                j += 1
            while j < len(lines) and lines[j][1].lstrip().startswith('|'):
                c2 = split_row(lines[j][1])
                if len(c2) >= 3:
                    rows.append((lines[j][0], c2))
                j += 1
            if rows:
                break

    if not rows:
        die('解析到 0 条联想方向 —— 判据空过。\n'
            '   纪要里必须有表头含「方向」与「状态」的表格，见 references/纪要模板.md。')

    seen, tally = {}, {'done': 0, 'partial': 0, 'notdone': 0, 'blank': 0}
    for lineno, c in rows:
        code = None
        for cell in c[:2]:
            m = re.match(r'^\**\s*(D[1-9])\s*\**$', cell.strip())
            if m:
                code = m.group(1)
                break
        if not code:
            continue
        status = c[2] if len(c) > 2 else ''
        seen[code] = (lineno, status, classify(status))
        tally[seen[code][2]] += 1

    LABEL = {'done': '✅ 已主动查', 'partial': '⚠️ 部分/被动撞见（合法，需跟进）',
             'notdone': '⛔ 明确标了「未查」', 'blank': '⛔ 状态列空白 —— 等于没交代'}
    print(f'\n联想扩散机检 —— {path}')
    print(f'声明了 {len(seen)}/9 个方向\n' + '-' * 62)
    for d in DIRECTIONS:
        if d not in seen:
            print(f'⛔ {d} {NAMES[d]:<8}: ⛔ 整个方向都没声明 —— 这是最贵的漏检')
            tally['blank'] += 1
        else:
            lineno, status, kind = seen[d]
            print(f'{"✅" if kind in ("done", "partial") else "⛔"} '
                  f'{d} {NAMES[d]:<8}: {LABEL[kind]}（行 {lineno}）')

    print('-' * 62)
    fails = tally['notdone'] + tally['blank']
    print(f'✅ 已查 {tally["done"]}｜⚠️ 部分 {tally["partial"]}｜'
          f'⛔ 标未查 {tally["notdone"]}｜⛔ 空白 {tally["blank"]} ⇒ {fails} 个方向未过关')
    if fails:
        print('❌ 联想面存在漏检 —— 继续 research，或把这些缺口写进「未决」')
    else:
        print(f'✅ 九个方向都有交代'
              + (f'（⚠️ 其中 {tally["partial"]} 个只是部分/被动，须跟进）' if tally['partial'] else ''))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('用法: python check_expansion.py <纪要.md>')
        sys.exit(2)
    main(sys.argv[1])
