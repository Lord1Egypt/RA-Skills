#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

for file in SKILL.md manifest.yaml agents/openai.yaml README.md README.en.md LICENSE icon-512.png assets/promo-1600x900.png fixtures/success-input.md fixtures/success-output.md fixtures/failure-input.md fixtures/failure-output.md; do
  test -f "$file" || { echo "Missing $file" >&2; exit 1; }
done
grep -q '^name: selfmedia-interview-quote-index-cn$' SKILL.md
grep -q '^name: selfmedia-interview-quote-index-cn$' manifest.yaml
grep -q '^slug: selfmedia-interview-quote-index-cn$' manifest.yaml
grep -q '^icon: icon-512.png$' manifest.yaml
grep -q 'allow_implicit_invocation: true' agents/openai.yaml
grep -q 'npx skills add xxjrq/selfmedia-interview-quote-index-cn' README.md
python3 - <<'PY'
import struct
for path, want in [('icon-512.png', (512, 512)), ('assets/promo-1600x900.png', (1600, 900))]:
    with open(path, 'rb') as f:
        sig = f.read(8)
        assert sig == b'\x89PNG\r\n\x1a\n', f'{path}: not PNG'
        length = struct.unpack('>I', f.read(4))[0]
        assert f.read(4) == b'IHDR' and length == 13, f'{path}: invalid IHDR'
        width, height = struct.unpack('>II', f.read(8))
        assert (width, height) == want, f'{path}: got {width}x{height}, want {want}'
PY
node scripts/verify-fixtures.mjs
echo 'self-test passed'
