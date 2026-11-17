# -*- coding: utf-8 -*-
"""把交付用的 markdown 按案例切成单篇（发飞书/单独给客户时用）。

用法：
  python3 09_split_md.py <markdown 路径> [输出目录] [案例号,案例号,...]
默认输出目录 /tmp/cb_split，不指定案例号则全切。
"""
import os, re, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else '<交付用 markdown 路径>'
OUT = sys.argv[2] if len(sys.argv) > 2 else '/tmp/cb_split'
WANT = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 and sys.argv[3] else []

lines = open(SRC, encoding='utf-8').read().split('\n')
idx = []
for i, l in enumerate(lines):
    m = re.match(r'^## 案例 (\d+)｜', l)
    if m:
        idx.append((int(m.group(1)), i))
os.makedirs(OUT, exist_ok=True)
n = 0
for k, (no, i) in enumerate(idx):
    if WANT and no not in WANT:
        continue
    end = idx[k + 1][1] if k + 1 < len(idx) else len(lines)
    body = '\n'.join(lines[i:end]).rstrip()
    open(os.path.join(OUT, 'md_%d.md' % no), 'w', encoding='utf-8').write(body)
    print('md_%d.md' % no, len(body))
    n += 1
print('done:', n, 'files ->', OUT)
