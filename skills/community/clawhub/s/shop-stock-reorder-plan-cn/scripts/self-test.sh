#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
python3 - <<'PY'
import json, pathlib, re, struct

root = pathlib.Path('.')
required = ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'LICENSE', 'icon-512.png', 'assets/promo-1600x900.png', 'fixtures/success.json', 'fixtures/failure-missing-fields.json']
for name in required:
    assert (root / name).is_file(), f'missing file: {name}'

skill = (root / 'SKILL.md').read_text(encoding='utf-8')
manifest = (root / 'manifest.yaml').read_text(encoding='utf-8')
agent = (root / 'agents/openai.yaml').read_text(encoding='utf-8')
assert re.search(r'^name: shop-stock-reorder-plan-cn$', skill, re.M)
assert 'name: "shop-stock-reorder-plan-cn"' in manifest and 'slug: "shop-stock-reorder-plan-cn"' in manifest
assert 'allow_implicit_invocation: true' in agent
for text in (manifest, agent):
    assert 'display_name: "库存补货清单"' in text

def png_size(path):
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', f'not PNG: {path}'
    return struct.unpack('>II', data[16:24])

assert png_size(root / 'icon-512.png') == (512, 512)
assert png_size(root / 'assets/promo-1600x900.png') == (1600, 900)

need = {'sku', 'current_stock', 'recent_sales', 'sales_days', 'lead_time_days', 'target_stock'}
success_fixture = json.loads((root / 'fixtures/success.json').read_text(encoding='utf-8'))
failure_fixture = json.loads((root / 'fixtures/failure-missing-fields.json').read_text(encoding='utf-8'))
success = success_fixture['items']
failure = failure_fixture['items']

# Structure checks: inputs are bounded and success inputs contain every required field.
assert 1 <= len(success) <= 100 and all(need <= set(row) for row in success)
assert all(isinstance(row['sales_days'], (int, float)) and row['sales_days'] > 0 for row in success)

# Fixture behavior checks: expected outputs document the Markdown workflow's business semantics.
success_expected = success_fixture['expected']
assert success_expected['reorder_quantities'] == {
    'NOTEBOOK-A5': 32, 'BOOKMARK-SET': 30, 'COFFEE-DRIP': 0,
}
assert success_expected['lead_time_stockout_risks'] == ['NOTEBOOK-A5', 'BOOKMARK-SET']
assert success_expected['unprocessed'] == []

failure_expected = failure_fixture['expected']
assert failure_expected['unprocessed'] == {
    'MISSING-LEAD': ['lead_time_days'],
    'MISSING-STOCK': ['current_stock'],
}
assert failure_expected['no_reorder_recommendations_for'] == ['MISSING-LEAD', 'MISSING-STOCK']
for row in failure:
    missing = need - set(row)
    assert missing == set(failure_expected['unprocessed'][row['sku']])

print('PASS: package structure and fixture field contracts are valid.')
print('PASS: fixture behavior assertions cover reorder quantities, lead-time risks, missing fields, and no-recommendation cases.')
print('NOTE: this self-test validates packaged fixture expectations; it does not execute a replenishment engine.')
PY
