#!/usr/bin/env bash
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 - <<'PY'
import json, re, struct
from pathlib import Path
r=Path.cwd()
need=['SKILL.md','manifest.yaml','agents/openai.yaml','scripts/self-test.sh','fixtures/success-input.json','fixtures/success-output.md','fixtures/failure-input.json','fixtures/failure-output.md','README.md','README.zh-CN.md','icon-512.png','assets/promo-1600x900.png','LICENSE']
assert not [x for x in need if not (r/x).is_file()]
s=(r/'SKILL.md').read_text();m=(r/'manifest.yaml').read_text();a=(r/'agents/openai.yaml').read_text()
assert re.search(r'^name: selfmedia-content-calendar-cn$',s,re.M)
assert re.search(r'^name: selfmedia-content-calendar-cn$',m,re.M) and re.search(r'^slug: selfmedia-content-calendar-cn$',m,re.M)
assert 'https://github.com/xxjrq/selfmedia-content-calendar-cn' in m
assert len(re.search(r'^description: (.+)$',m,re.M).group(1)) in range(80,241)
assert 25<=len(re.search(r'^  short_description: (.+)$',a,re.M).group(1))<=64
assert 'policy:\n  allow_implicit_invocation: true' in a
for f,wh in [('icon-512.png',(512,512)),('assets/promo-1600x900.png',(1600,900))]:
 d=(r/f).read_bytes();assert d[:8]==b'\x89PNG\r\n\x1a\n';assert struct.unpack('>II',d[16:24])==wh
good=json.loads((r/'fixtures/success-input.json').read_text());bad=json.loads((r/'fixtures/failure-input.json').read_text())
assert set(good)=={'账号定位','素材清单','产能','已确定主题'} and set(bad)!=set(good)
o=(r/'fixtures/success-output.md').read_text();assert all(f'第{n}天' in o for n in range(1,15))
assert all(x in o for x in ('### 已知事实','### 建议与待确认','### 边界'))
# Fixture behavior check: confirmed weekly themes and stated capacity are met.
rows=[x for x in o.splitlines() if x.startswith('| 第')]
assert len(rows)==14
week1,week2=rows[:7],rows[7:]
for week in (week1,week2):
 assert sum('| 图文' in x for x in week)==2
 assert sum('| 短视频' in x for x in week)==1
 assert sum('2小时：' in x for x in week)==2
 assert sum('3小时：' in x for x in week)==1
 assert sum('0小时' in x for x in week)==4
 for day,row in enumerate(week,1):
  if day not in (2,4,6):assert '0小时，不安排制作' in row
assert '缺少' in (r/'fixtures/failure-output.md').read_text() or '资料缺失' in (r/'fixtures/failure-output.md').read_text()
print('PASS: package structure and metadata')
print('PASS: success and failure fixture structure and stated example constraints')
print('NOTE: validates structure/examples; real Markdown planning behavior requires user input.')
PY
