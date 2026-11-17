# -*- coding: utf-8 -*-
"""source-doc-slimming 配套工具：体量分解 / 耦合侦察 / 零丢失证明。

用法
----
  # 1) 体量分解：Markdown 按 ## 切，JSON/YAML 按顶层键切（一律 UTF-8 字节）
  python slim.py breakdown <file>

  # 2) 耦合侦察：搬动之前先问「谁引用了它」
  python slim.py coupling <root_dir> <regex> [--ext .py,.md,.json,.yaml]

  # 3) 零丢失证明：原段落每一非空行必须逐行命中外置文件
  python slim.py verify <pre_file> <ref_file> --start "## 12." [--end "## Reference Files"]

退出码：0 = 通过 / 1 = 有未命中或读取失败。
"""
import io
import json
import os
import re
import sys

TEXT_EXT = ('.md', '.py', '.json', '.yaml', '.yml', '.txt', '.toml', '.cfg', '.ini')


def rd(p):
    return io.open(p, 'r', encoding='utf-8').read()


def blen(s):
    """字节数。len(str) 是字符数，中文文本两者相差 ~1.4 倍 —— 混用会算出互相矛盾的占比。"""
    return len(s.encode('utf-8'))


def walk(root, exts):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ('.git', '__pycache__', 'node_modules', '.venv', 'archive')]
        for f in fn:
            if f.endswith(exts):
                yield os.path.join(dp, f)


def try_load_json(p):
    return json.loads(rd(p))


def try_load_yaml(p):
    try:
        import yaml
    except ImportError:
        return None
    try:
        return yaml.safe_load(rd(p))
    except Exception:
        return None


def cmd_breakdown(path):
    raw = rd(path)
    total_b, total_c = blen(raw), len(raw)
    print('=' * 78)
    print('体量分解 — %s' % os.path.basename(path))
    print('=' * 78)
    print('  文件 %d B / %d chars（字节÷字符 = %.2f —— 中文越密比值越大）' % (
        total_b, total_c, total_b / max(total_c, 1)))
    rows = []
    if path.endswith(('.md', '.txt')):
        lines = raw.split('\n')
        idx = [(i, l) for i, l in enumerate(lines) if l.startswith('## ')]
        if not idx:
            idx = [(i, l) for i, l in enumerate(lines) if l.startswith('#')]
        for n, (i, l) in enumerate(idx):
            j = idx[n + 1][0] if n + 1 < len(idx) else len(lines)
            rows.append((blen('\n'.join(lines[i:j])), l))
    else:
        obj = try_load_json(path)
        if obj is None:
            obj = try_load_yaml(path)
        if not isinstance(obj, (dict, list)):
            print('  ❌ 无法解析为 dict / list')
            return 1
        items = obj.items() if isinstance(obj, dict) else [(str(i), v) for i, v in enumerate(obj)]
        for k, v in items:
            try:
                rows.append((blen(json.dumps(v, ensure_ascii=False, indent=2)), str(k)))
            except (TypeError, ValueError):
                rows.append((blen(str(v)), str(k)))
    rows.sort(reverse=True)
    tot = sum(r[0] for r in rows) or 1
    print('  分块 %d 个：' % len(rows))
    for n, label in rows:
        print('   %9d B  %5.1f%%  %s' % (n, n * 100.0 / tot, label[:66]))
    print('  ---- 分块合计 %d B（文件 %d B，差额 = 键名/缩进/分隔符开销）' % (tot, total_b))
    print('\n  下界提醒：**被代码/校验器实际读取**的分块删不得 —— 先跑 coupling 与 grep，再定目标。')
    print('  目标必须由算术下界导出，不能取整数字。')
    return 0


def cmd_coupling(root, pattern, exts):
    rx = re.compile(pattern)
    hits = 0
    print('=' * 78)
    print('耦合侦察 — %s ｜ pattern = %s' % (root, pattern))
    print('=' * 78)
    for p in sorted(walk(root, exts)):
        try:
            t = rd(p)
        except Exception:
            continue
        found = []
        for i, line in enumerate(t.split('\n'), 1):
            if rx.search(line):
                found.append((i, line.strip()[:130]))
        if found:
            hits += 1
            print('\n  --- %s ---' % os.path.relpath(p, root))
            for i, l in found[:12]:
                print('    %4d| %s' % (i, l))
            if len(found) > 12:
                print('    ... 共 %d 处' % len(found))
    print('\n  引用面：%d 个文件。**为零 → 搬动无运行耦合；不为零 → 逐个确认后再动。**' % hits)
    return 0


def cmd_verify(pre, ref, start, end):
    t, r = rd(pre), rd(ref)
    if t.count(start) != 1:
        print('❌ start 锚点在 pre_file 中出现 %d 次（应为 1）' % t.count(start))
        return 1
    i = t.index(start)
    if end:
        if t.count(end) != 1:
            print('❌ end 锚点在 pre_file 中出现 %d 次（应为 1）' % t.count(end))
            return 1
        j = t.index(end)
        if j <= i:
            print('❌ end 出现在 start 之前')
            return 1
    else:
        j = len(t)
    blk = t[i:j]
    lines = [l for l in blk.split('\n') if l.strip()]
    miss = [l for l in lines if l not in r]
    print('=' * 78)
    print('零丢失证明 — %s → %s' % (os.path.basename(pre), os.path.basename(ref)))
    print('=' * 78)
    print('  原段落 %d B ｜ 非空行 %d ｜ 未命中 %d' % (blen(blk), len(lines), len(miss)))
    for l in miss[:20]:
        print('    ❌ %s' % l[:120])
    if miss:
        print('\n  结论：❌ 有内容未落到外置文件 —— **不得删原文**，先补齐。')
        return 1
    print('  结论：✅ 逐行命中，外置完整（原文可安全替换为 digest + 指针）')
    return 0


def main():
    a = sys.argv[1:]
    if not a or a[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    if a[0] == 'breakdown' and len(a) >= 2:
        return cmd_breakdown(a[1])
    if a[0] == 'coupling' and len(a) >= 3:
        exts = TEXT_EXT
        if '--ext' in a:
            exts = tuple(x.strip() for x in a[a.index('--ext') + 1].split(',') if x.strip())
        return cmd_coupling(a[1], a[2], exts)
    if a[0] == 'verify' and len(a) >= 4:
        start = a[a.index('--start') + 1] if '--start' in a else None
        end = a[a.index('--end') + 1] if '--end' in a else None
        if not start:
            print('verify 需要 --start "<段落首行>"')
            return 1
        return cmd_verify(a[1], a[2], start, end)
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
