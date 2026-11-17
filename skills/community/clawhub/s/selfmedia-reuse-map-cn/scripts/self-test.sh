#!/usr/bin/env bash
set -euo pipefail
root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$root"
fail=0
note() { printf '%s\n' "$1"; }
check() { if "$@"; then note "PASS: $*"; else note "FAIL: $*"; fail=1; fi; }
check test -f SKILL.md
check test -f manifest.yaml
check test -f agents/openai.yaml
check test -f fixtures/success.json
check test -f fixtures/failure-missing-summary.json
check test -f README.md
check test -f README.en.md
check test -f README.zh-CN.md
check test -f LICENSE
check test -f icon-512.png
check test -f assets/icon-512.png
check test -f assets/promo-1600x900.png
if command -v python3 >/dev/null; then
  python3 - <<'PY' || fail=1
from pathlib import Path
import json, re, struct
root=Path('.')
skill=root.joinpath('SKILL.md').read_text()
assert re.search(r'^name: selfmedia-reuse-map-cn$', skill, re.M)
skill_description=re.search(r'^description: (.+)$', skill, re.M).group(1)
assert 80 <= len(skill_description) <= 240
manifest=root.joinpath('manifest.yaml').read_text()
for item in ('name: selfmedia-reuse-map-cn','slug: selfmedia-reuse-map-cn','repository: https://github.com/xxjrq/selfmedia-reuse-map-cn','self_test: ./scripts/self-test.sh'):
    assert item in manifest, item
manifest_description=re.search(r'^description: (.+)$', manifest, re.M).group(1)
assert 80 <= len(manifest_description) <= 240
assert len(re.search(r'^  short_description: (.+)$', manifest, re.M).group(1)) in range(25,65)
assert manifest.count('  - ') >= 7, 'expected tags, triggers, and sources'
assert re.search(r'^icon: icon-512.png$', manifest, re.M), 'manifest root icon'
agent=root.joinpath('agents/openai.yaml').read_text()
assert 'allow_implicit_invocation: true' in agent
for field in ['icon_small', 'icon_large']:
    match = re.search(r'^  '+field+r': (.+)$', agent, re.M)
    assert match is not None and (root / match.group(1).strip('"')).is_file(), f'{field} must refer to a real icon'
assert len(re.search(r'^  short_description: (.+)$', agent, re.M).group(1)) in range(25,65)
success=json.loads((root/'fixtures'/'success.json').read_text())
failure=json.loads((root/'fixtures'/'failure-missing-summary.json').read_text())
required=('id','title','published_at','platform','summary')
success_items=success['input']['content_items']
assert success_items and all(all(k in x for k in required) for x in success_items)
success_output=success['expected_output']
success_md=success_output['markdown']
success_semantics=success_output['semantic_expectations']
assert '## 资料核对' in success_md and '## 二次利用清单' in success_md and '## 新角度' in success_md
assert success_semantics['inference_marker'] == '推断' and success_semantics['known_vs_inference_boundary'] == '已知资料依据'
for item_id in success_semantics['update_item_ids']:
    assert item_id in success_md and '更新' in success_md
for item_id in success_semantics['split_item_ids']:
    assert item_id in success_md and '拆分' in success_md
for item_id in success_semantics['bundle_item_ids']:
    assert item_id in success_md and '合集' in success_md
assert '评论中多次询问小包装选择' in success_md, 'update priority must retain supplied evidence'
assert '两篇标题均聚焦咖啡豆' in success_md, 'bundle basis must be explicit'
failure_item=failure['input']['content_items'][0]
assert 'summary' not in failure_item and failure_item['id'] == 'novel-03'
failure_output=failure['expected_output']
failure_md=failure_output['markdown']
failure_semantics=failure_output['semantic_expectations']
assert '`novel-03` 缺少 `summary`' in failure_md
assert failure_semantics['missing_item_id'] == 'novel-03'
assert failure_semantics['missing_field'] == 'summary'
assert failure_semantics['stopped_item_ids'] == ['novel-03']
assert failure_semantics['recommendations_for_stopped_items'] == []
assert '不对 `novel-03` 给出更新、拆分、合集或新角度建议' in failure_md
for name, dims in [('icon-512.png',(512,512)), ('assets/icon-512.png',(512,512)), ('assets/promo-1600x900.png',(1600,900))]:
    p=root/name
    if not p.exists(): raise AssertionError(f'missing visual asset: {p}')
    b=p.read_bytes(); assert b[:8]==b'\x89PNG\r\n\x1a\n', f'not png: {p}'
    w,h=struct.unpack('>II',b[16:24]); assert (w,h)==dims, f'{p}: {(w,h)} != {dims}'
print('PASS: metadata, fixtures, fixture semantics, and asset dimensions')
PY
else
  note 'FAIL: python3 is required for JSON and PNG structural checks'; fail=1
fi
note 'INFO: Structural checks validate package fields and asset dimensions; fixture-semantic checks validate documented expected outputs and boundaries.'
note 'INFO: No recommendation engine is simulated: apply SKILL.md to the included input/expected-output examples to verify real behavior.'
exit "$fail"
