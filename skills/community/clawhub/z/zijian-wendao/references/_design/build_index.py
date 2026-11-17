# -*- coding: utf-8 -*-
import os, re, collections

BASE = '/sandbox/workspace/skills/资鉴问道/references'
CASES = os.path.join(BASE, 'cases')
files = sorted(os.listdir(CASES))

cases = []          # (title, tags, srcfile, groupname)
for f in files:
    txt = open(os.path.join(CASES, f), encoding='utf-8').read()
    group = txt.split('\n', 1)[0].lstrip('# ').strip()
    blocks = re.split(r'^## ', txt, flags=re.M)[1:]
    for b in blocks:
        lines = b.split('\n')
        title = lines[0].strip()
        tags = []
        for l in lines[1:4]:
            m = re.search(r'标签\*\*：(.*)', l)
            if m:
                tags = re.findall(r'#([^\s#]+)', m.group(1))
                break
        cases.append((title, tags, f, group))

# 主题索引
bytag = collections.defaultdict(list)
for title, tags, f, g in cases:
    for t in tags:
        bytag[t].append((title, f))

idx = ['# 「资鉴问道」抉择案例·主题索引\n',
       f'共收录 **{len(cases)}** 个历史抉择案例，覆盖《史记》《资治通鉴》。按主题标签归类如下；点开任一案例可读全文（情境／选项／结果／显隐性代价／原文出处／决策要点）。\n']
order = sorted(bytag.keys(), key=lambda k: -len(bytag[k]))
for t in order:
    idx.append(f'\n## #{t}（{len(bytag[t])}）\n')
    for title, f in bytag[t]:
        idx.append(f'- {title}　〔{f[:-3]}〕')

# 按出处总目录
comp = ['\n\n---\n\n# 案例总目录（按出处）\n']
for f in files:
    grp = [c for c in cases if c[2] == f]
    comp.append(f'\n## {f[:-3]}（{len(grp)}）\n')
    for title, tags, _, _ in grp:
        comp.append(f'- {title}　#' + ' #'.join(tags))

open(os.path.join(BASE, '案例索引.md'), 'w', encoding='utf-8').write('\n'.join(idx + comp))
print('案例总数:', len(cases))
print('标签数:', len(bytag))
print('Top标签:', [(t, len(bytag[t])) for t in order[:12]])
