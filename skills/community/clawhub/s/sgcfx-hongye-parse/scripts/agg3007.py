# -*- coding: utf-8 -*-
"""SGCFX 3007 工料机汇总表 聚合器 v2（去硬编码 / 去敏）

相对旧版的关键修复：
1. 不再硬编码单位工程目录 ID 与工程名（旧版写死了某个具体项目的结构，换项目即失效）
2. 自动发现 <root>/<ver>/*/3007，覆盖任意项目
3. 分组标签一律用通用名「单位工程<目录ID>」，不猜测、不编造、不含真实项目名
4. 额外导出 Tree 中解析到的名称清单，供人工核对映射（tree_names.txt）

用法:
  python3 agg3007.py <root>[:ver1,ver2] [<root>[:ver...]] [-o out.csv] [--tree-out tree_names.txt]
示例:
  python3 agg3007.py /tmp/sgcfx_new:3,4 /tmp/sgcfx_old:2,3 -o materials_3007.csv
"""
import os
import sys
import csv
import re
import argparse
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p3007 import rows, tlv  # noqa: E402


def tree_names(root):
    """尝试从 Tree 提取可读名称清单，失败返回空列表（不保证顺序即目录顺序）。"""
    p = os.path.join(root, 'Tree')
    if not os.path.exists(p):
        return []
    try:
        strs = [s.strip() for _, s in tlv(p)]
    except Exception:
        return []
    seen, out = set(), []
    for s in strs:
        if 2 <= len(s) <= 40 and s not in seen and not re.fullmatch(r'[\d\.\-_/\s]+', s):
            seen.add(s)
            out.append(s)
    return out


def discover(root, ver):
    """返回 [(目录ID, 3007文件路径)]，按数字序排列。"""
    vdir = os.path.join(root, ver)
    if not os.path.isdir(vdir):
        return []
    items = []
    for name in sorted(os.listdir(vdir), key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else x)):
        f = os.path.join(vdir, name, '3007')
        if os.path.isfile(f):
            items.append((name, f))
    return items




# --- 防电子表格公式注入（CWE-1236）：Excel 打开 CSV 时求值 =/+/−/@ 开头单元格 ---

def _csv_safe(v):
    if isinstance(v, str) and v[:1] in ('=', '+', '-', '@', '\t'):
        return "'" + v
    return v


def main():
    ap = argparse.ArgumentParser(description='聚合 SGCFX 工料机汇总表（3007）')
    ap.add_argument('roots', nargs='+', help='解包根目录，可用 root:3,4 指定版本')
    ap.add_argument('-o', '--out', default='materials_3007.csv')
    ap.add_argument('--tree-out', default='tree_names.txt')
    args = ap.parse_args()

    allr, trees = [], {}
    for spec in args.roots:
        root, _, vs = spec.partition(':')
        root = root.rstrip('/')
        if not os.path.isdir(root):
            print(f'[跳过] 目录不存在: {root}')
            continue
        vers = vs.split(',') if vs else [d for d in sorted(os.listdir(root)) if d.isdigit()]
        trees[root] = tree_names(root)
        for v in vers:
            for uid, f in discover(root, v):
                for x in rows(f):
                    if x['qty'] is None:
                        continue
                    allr.append(dict(
                        root=os.path.basename(root), ver=v, unit=f'单位工程{uid}',
                        code=x['code'], name=x['name'], spec=x['spec'], u=x['unit'],
                        qty=x['qty'], price=x['price'], amt=x['amt'], src=x['src'],
                    ))

    with open(args.out, 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=['root', 'ver', 'unit', 'code', 'name', 'spec', 'unit2', 'qty', 'price', 'amt', 'src'])
        w.writeheader()
        for r in allr:
            w.writerow({k: _csv_safe(x) for k, x in dict(root=r['root'], ver=r['ver'], unit=r['unit'], code=r['code'],
                            name=r['name'], spec=r['spec'], unit2=r['u'], qty=r['qty'], price=r['price'], amt=r['amt'], src=r['src']).items()})

    with open(args.tree_out, 'w', encoding='utf-8') as fh:
        for root, ns in trees.items():
            fh.write(f'# {os.path.basename(root)}\n')
            for n in ns:
                fh.write(n + '\n')

    print(f'总行数 {len(allr)} -> {args.out}；Tree 名称清单 -> {args.tree_out}')
    c = Counter((r['root'], r['ver'], r['unit']) for r in allr)
    for k in sorted(c):
        print(k, c[k])


if __name__ == '__main__':
    main()
