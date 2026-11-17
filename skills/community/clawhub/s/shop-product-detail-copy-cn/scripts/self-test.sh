#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

for file in SKILL.md manifest.yaml agents/openai.yaml README.md README.en.md LICENSE icon-512.png assets/promo-1600x900.png fixtures/success.json fixtures/failure-missing-fields.json; do
  [[ -f "$file" ]] || { echo "missing required file: $file" >&2; exit 1; }
done

python3 - <<'PY'
import json, struct
from pathlib import Path

root = Path('.')
manifest = (root / 'manifest.yaml').read_text(encoding='utf-8')
for key in ('name:', 'slug: shop-product-detail-copy-cn', 'short_description:', 'repository: https://github.com/xxjrq/shop-product-detail-copy-cn', 'self_test: bash scripts/self-test.sh'):
    assert key in manifest, f'manifest field missing: {key}'
assert 25 <= len(next(line.split(': ', 1)[1] for line in manifest.splitlines() if line.startswith('short_description:'))) <= 64
assert manifest.count('\n  - ') >= 7, 'expected tags, triggers, and trigger words'
assert 'browserId' not in (root / 'SKILL.md').read_text(encoding='utf-8')

def png_size(path):
    raw = path.read_bytes()
    assert raw[:8] == b'\x89PNG\r\n\x1a\n', f'not PNG: {path}'
    return struct.unpack('>II', raw[16:24])

assert png_size(root / 'icon-512.png') == (512, 512), 'icon must be 512x512'
assert png_size(root / 'assets/promo-1600x900.png') == (1600, 900), 'promo must be 1600x900'

required = {'product_name', 'specifications', 'image_notes', 'target_audience'}
success = json.loads((root / 'fixtures/success.json').read_text(encoding='utf-8'))
failure = json.loads((root / 'fixtures/failure-missing-fields.json').read_text(encoding='utf-8'))
assert required <= success.keys(), 'success fixture lacks required fields'
assert isinstance(success['specifications'], dict) and success['specifications']
assert isinstance(success['image_notes'], list) and success['image_notes']
expected = success.get('expected_behavior')
assert isinstance(expected, dict), 'success fixture must declare expected behavior'
expected_modules = {
    '模块 1：首屏价值主张', '模块 2：核心卖点与证据', '模块 3：规格与选购信息',
    '模块 4：图片搭配文案', '模块 5：适用场景与温和提醒', 'FAQ', '事实与建议边界'
}
assert expected_modules <= set(expected.get('required_modules', [])), 'success fixture must require every fixed output module'
selling_points = expected.get('selling_points', {})
assert selling_points.get('count_range') == [3, 5], 'success fixture must require 3–5 selling points'
assert '证据：' in selling_points.get('each_requires', ''), 'success fixture must require evidence per selling point'
assert expected.get('faq'), 'success fixture must define FAQ expectation'
boundary = expected.get('fact_suggestion_boundary', {})
assert boundary.get('known_facts_must_preserve'), 'success fixture must state facts to preserve'
assert boundary.get('suggestions_must_be_labeled'), 'success fixture must state suggestions to label'
assert any('目标客群' in item and '易清洁' in item for item in boundary.get('must_not_claim', [])), (
    'success fixture must prevent audience preference from becoming a product claim'
)
missing = required - failure.get('input', {}).keys()
assert missing == set(failure['expected_missing_fields']), 'failure fixture must state exactly its missing fields'
print('PASS: repository structure and manifest fields')
print('PASS: icon and promo dimensions')
print('PASS: success fixture expected modules, evidence, FAQ, and fact/suggestion boundary')
print('PASS: missing-field fixture structure')
print('NOTE: this self-test validates packaging and fixture structure only; it does not claim to validate generated copy quality.')
PY
