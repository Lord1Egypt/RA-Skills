# -*- coding: utf-8 -*-
"""gate_02 人工闸门②：我们自己的写作列里没有第二人称/教程口吻。

检查范围**只有我们自己撰写的列**：方法拆解(steps) / 可迁移到我们(transfer) / 案例研究推文(post)。
**不检查译文列(zh)** —— 译文里原帖本人说的「你」是原文口吻，必须保留；把它一起改会把原帖改坏。

白名单：引号内的原帖原话、建议照抄给读者的问卷题目（如「你是怎么知道我们的」）——
问卷题必须用第二人称才成立。脚本按「是否落在引号内」自动分流：引号内的命中单独打印，不计入失败。
另有**假朋友词**白名单（FALSE_FRIENDS）：中文里含「你」但完全不是第二人称的词，
典型是「迷你」（mini，如「迷你墓碑摆件」「迷你摊位」）。这类命中会被单独计数，不计入失败。

用法：
    python3 gate_02_second_person.py <cases_final.json>
    python3 gate_02_second_person.py <file.md>
退出码 0 = 干净（或只剩引号内/假朋友词命中），1 = 有引号外的第二人称。

修法：写一个 fix_voice.py 做精确字符串替换（一条条列 old→new），别用正则全局替换。
改完必须**重建 xlsx+md 再复跑本脚本**——本脚本读构建产出的中间 json，不重建会读到旧数据。"""
import os, re, sys, json, glob

RX_PRON = re.compile(r'[你您]')
QUOTE_CHARS = '「」“”"\''
# 假朋友词：含「你」但不是第二人称。命中位置落在这些词里就跳过（避免把正常内容判成违规）。
FALSE_FRIENDS = ['迷你']          # mini
COLS = [('方法拆解', 'steps'), ('可迁移到我们', 'transfer'), ('案例研究推文', 'post')]


def in_false_friend(txt, pos):
    """pos 处的「你」是否属于「迷你」这类非第二人称词。"""
    for w in FALSE_FRIENDS:
        i = w.find('你')
        if i == -1:
            continue
        start = pos - i
        if start >= 0 and txt[start:start + len(w)] == w:
            return True
    return False


def in_quote(txt, pos):
    """判断 pos 位置是否落在成对的引号内（粗略：往前数最近的成对引号）。"""
    for a, b in (('「', '」'), ('“', '”')):
        before = txt.rfind(a, 0, pos)
        if before != -1:
            close = txt.find(b, before)
            if close > pos:
                return True
    return False


def scan(rows):
    outside, inside, friends = [], [], []
    for i, c in enumerate(rows, 1):
        for label, key in COLS:
            txt = c.get(key, '') or ''
            for m in RX_PRON.finditer(txt):
                seg = txt[max(0, m.start() - 45):m.start() + 45].replace('\n', ' ')
                line = '%d %s | …%s…' % (i, label, seg)
                if in_false_friend(txt, m.start()):
                    friends.append(line)
                elif in_quote(txt, m.start()):
                    inside.append(line)
                else:
                    outside.append(line)
    return outside, inside, friends


def main(argv):
    p = os.path.expanduser(argv[0]) if argv else ''
    if not p or not os.path.isfile(p):
        print('用法：python3 gate_02_second_person.py <cases_final.json|file.md>')
        return 2
    if p.endswith('.json'):
        data = json.load(open(p, encoding='utf-8'))
        rows = data if isinstance(data, list) else data.get('cases', [])
    else:
        txt = open(p, encoding='utf-8', errors='ignore').read()
        rows = [{'post': txt}]          # markdown 整体当一列扫
    outside, inside, friends = scan(rows)
    print('=== 引号外的第二人称（需要修）: %d ===' % len(outside))
    for x in outside[:40]:
        print(' ', x[:200])
    print('=== 引号内的引用（可保留）: %d ===' % len(inside))
    for x in inside[:20]:
        print(' ', x[:200])
    if friends:
        print('=== 假朋友词（如「迷你」，可保留）: %d ===' % len(friends))
        for x in friends[:10]:
            print(' ', x[:200])
    if not outside:
        print('结论：闸门② 通过（我们自己的写作列无第二人称教程口吻）')
        return 0
    print('结论：闸门② 未通过 —— 改完请重建 xlsx+md 再复跑本脚本')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
