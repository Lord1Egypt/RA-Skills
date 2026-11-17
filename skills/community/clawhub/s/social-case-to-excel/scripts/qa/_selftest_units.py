import re, sys
UNIT = {'兆': 1e12, '万亿': 1e12, '亿': 1e8, '千万': 1e7, '百万': 1e6, '十万': 1e5,
        '万': 1e4, '千': 1e3,
        'k': 1e3, 'K': 1e3, 'M': 1e6, 'MM': 1e6, 'mm': 1e6, 'm': 1e6,
        'B': 1e9, 'b': 1e9, 'billion': 1e9, 'million': 1e6, 'bn': 1e9}
NUM_RE = re.compile(
    r'(\d[\d,]*(?:\.\d+)?)'
    r'(?:[ \t]*(万亿|兆|千万|百万|十万|亿|万|千))?'
    r'(?:(billion|million|MM|mm|bn|[kKMBmb])(?![A-Za-z]))?'
    r'(?![\d])')


def nums(t):
    out = set()
    for m in NUM_RE.finditer(t):
        core = m.group(1).replace(',', '').rstrip('.')
        if not re.fullmatch(r'\d+(\.\d+)?', core):
            continue
        out.add(round(float(core) * UNIT.get(m.group(2) or m.group(3) or '', 1), 4))
    return out


CASES = [
    ('$3,800\nMonth', {3800.0}, 'Month 的 M 不应算百万（旧版报 3.8e9）'),
    ('3. KD<10', {3.0, 10.0}, 'KD 的 K 不应算千（旧版报 3000）'),
    ('500 keywords', {500.0}, 'keywords 的 k 不应算千'),
    ('$7.5mm', {7.5e6}, '小写 mm 应算百万（旧版只认 M）'),
    ('$1.1m', {1.1e6}, '小写 m 应算百万（旧版漏认）'),
    ('3bn', {3e9}, 'bn 应算十亿'),
    ('12.2 万亿', {12.2e12}, '万亿 不再被切成 万（旧版报 12.2 万）'),
    ('500k 曝光 / 1.06M', {500e3, 1.06e6}, '正常单位'),
    ('7. Most of the time', {7.0}, '序号不应算百万'),
]
fail = 0
for txt, want, note in CASES:
    got = nums(txt)
    ok = got == want
    fail += 0 if ok else 1
    print('%s  %-22r %-22s %s | %s' % ('PASS' if ok else 'FAIL', txt, sorted(got), sorted(want), note))
print('FAILED', fail, '/', len(CASES))
sys.exit(1 if fail else 0)
