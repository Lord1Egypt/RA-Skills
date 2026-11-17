# -*- coding: utf-8 -*-
"""gate_01 人工闸门①：中文列无残留英文段落。

只扫「我们自己写的中文」这几列，命中 = 疑似整段英文没翻译 / 没改写（连续 5 个以上英文单词）。

用法：
    python3 gate_01_no_english_leftover.py <cases_final.json>       # 构建产出的中间文件
    python3 gate_01_no_english_leftover.py <file.xlsx>              # 也可以直接扫交付物
    python3 gate_01_no_english_leftover.py <file.md>
退出码 0 = 干净，1 = 有命中。

例外（属正常，不用改）：品牌名/产品名/平台名/行业术语（offer、campaign、ROI、UGC、Buy Box、
take rate…）、译文列里的专有名词与英文原句引用。
【注意】译文列（zh）里出现大段英文同样要报——中文原帖免译时译文列会是中文，
英文原帖的译文列若还是英文，说明这条忘了翻译。"""
import os, re, sys, json, glob, html, zipfile

RX = re.compile(r"(?:[A-Za-z][A-Za-z'\-]+[ ,]+){5,}")
COLS = [('方法拆解', 'steps'), ('可迁移到我们', 'transfer'),
        ('案例研究推文', 'post'), ('正文翻译(中文)', 'zh')]
ALLOW_SUBSTR = ('offer', 'campaign', 'ROI', 'UGC', 'Buy Box', 'take rate')


def scan_text(txt, tag):
    out = []
    for m in RX.finditer(txt or ''):
        seg = m.group(0).strip()
        if any(a.lower() in seg.lower() for a in ALLOW_SUBSTR):
            continue
        a, b = max(0, m.start() - 40), min(len(txt), m.end() + 40)
        out.append('%s: …%s…' % (tag, txt[a:b].replace('\n', ' ')))
    return out


def from_json(p):
    data = json.load(open(p, encoding='utf-8'))
    rows = data if isinstance(data, list) else data.get('cases', [])
    hit = []
    for i, c in enumerate(rows, 1):
        for label, key in COLS:
            hit += scan_text(c.get(key, ''), '%d %s' % (i, label))
    return hit


def from_xlsx(p):
    z = zipfile.ZipFile(p)
    t = ''
    for n in z.namelist():
        if n.startswith('xl/') and n.endswith('.xml'):
            t += re.sub(r'<[^>]+>', ' ', html.unescape(z.read(n).decode('utf-8', 'ignore')))
    return scan_text(t, 'xlsx')


def from_md(p):
    return scan_text(open(p, encoding='utf-8', errors='ignore').read(), 'md')


def main(argv):
    targets = []
    for a in argv:
        a = os.path.expanduser(a)
        if os.path.isdir(a):
            targets += sorted(glob.glob(os.path.join(a, '*.xlsx'))) + sorted(glob.glob(os.path.join(a, '*.md')))
        else:
            targets.append(a)
    if not targets:
        print('用法：python3 gate_01_no_english_leftover.py <cases_final.json|xlsx|md> [...]')
        return 2
    bad = 0
    for p in targets:
        if not os.path.isfile(p):
            print('!! 跳过（不存在）：%s' % p)
            continue
        if p.endswith('.json'):
            f = from_json(p)
        elif p.lower().endswith('.xlsx'):
            f = from_xlsx(p)
        else:
            f = from_md(p)
        if f:
            bad += 1
            print('❌ %s —— %d 处疑似残留英文段落' % (os.path.basename(p), len(f)))
            for x in f[:15]:
                print('    ', x[:200])
        else:
            print('✅ %s —— 0 命中，闸门① 通过' % os.path.basename(p))
    print('结论：%d 个文件未通过闸门①' % bad)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
