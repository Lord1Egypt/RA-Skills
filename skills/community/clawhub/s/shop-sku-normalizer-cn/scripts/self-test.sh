#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

required=(SKILL.md manifest.yaml agents/openai.yaml README.md README.en.md LICENSE icon-512.png assets/promo-1600x900.png fixtures/success-products.txt fixtures/failure-missing-field.txt scripts/self-test.sh)
for path in "${required[@]}"; do
  [[ -f "$path" ]] || { echo "FAIL: missing $path" >&2; exit 1; }
done

grep -qx 'name: shop-sku-normalizer-cn' manifest.yaml
grep -qx 'display_name: 商品规格与SKU整理' manifest.yaml
grep -qx 'repository: https://github.com/xxjrq/shop-sku-normalizer-cn' manifest.yaml
grep -qx 'self_test: bash scripts/self-test.sh' manifest.yaml
grep -q '^  - ecommerce$' manifest.yaml
grep -q '^  - sku$' manifest.yaml
grep -q '^  - product-data$' manifest.yaml
grep -q '^  - chinese$' manifest.yaml
grep -q '^  - 商品规格整理$' manifest.yaml
grep -q '^name: shop-sku-normalizer-cn$' SKILL.md
grep -q '缺少必填列或关键值' SKILL.md
grep -q '重复组中的\*\*每一行\*\*均标为“待确认”' SKILL.md
grep -q '商品名称,颜色,尺寸,型号,建议统一名称,状态,待确认原因' SKILL.md
grep -q '商品规格与SKU整理' agents/openai.yaml

python3 - <<'PY'
from pathlib import Path
import struct

def png_size(path):
    data = Path(path).read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', f'{path} is not a PNG'
    return struct.unpack('>II', data[16:24])

assert png_size('icon-512.png') == (512, 512), 'icon must be 512x512'
assert png_size('assets/promo-1600x900.png') == (1600, 900), 'promo must be 1600x900'

def rows(path):
    return Path(path).read_text(encoding='utf-8').splitlines()

ok = rows('fixtures/success-products.txt')
bad = rows('fixtures/failure-missing-field.txt')
assert len(ok) == 5 and all(len(r.split('\t')) == 4 for r in ok), 'success fixture shape'
assert len(bad) == 2 and bad[1].split('\t')[1] == '', 'failure fixture must have missing color'
assert ok[1] == ok[2], 'success fixture must contain a duplicate group for review handling'
print('PASS: structure and fixtures validated')
print('NOTE: this self-test validates package structure and sample shape only; real behavior is performed by the Markdown workflow at use time.')
PY
