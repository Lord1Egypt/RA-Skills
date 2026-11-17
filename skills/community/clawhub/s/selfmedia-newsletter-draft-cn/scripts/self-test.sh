#!/usr/bin/env bash
set -euo pipefail

root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$root"

for required in SKILL.md manifest.yaml agents/openai.yaml README.md README.en.md LICENSE icon-512.png assets/promo-1600x900.png fixtures/success-input.md fixtures/success-output.md fixtures/failure-input.md fixtures/failure-output.md; do
  [[ -f "$required" ]] || { echo "missing: $required" >&2; exit 1; }
done

python3 - <<'PY'
from pathlib import Path
import re, struct

root = Path('.')
skill = (root / 'SKILL.md').read_text()
manifest = (root / 'manifest.yaml').read_text()
agent = (root / 'agents/openai.yaml').read_text()
assert re.search(r'^name: selfmedia-newsletter-draft-cn$', skill, re.M)
assert re.search(r'^name: selfmedia-newsletter-draft-cn$', manifest, re.M)
assert re.search(r'^slug: selfmedia-newsletter-draft-cn$', manifest, re.M)
assert re.search(r'^icon: icon-512.png$', manifest, re.M)
assert re.search(r'^  allow_implicit_invocation: (true|false)$', agent, re.M)
for content in (manifest, agent):
    short = re.search(r'^  short_description: (.+)$', content, re.M)
    assert short and 25 <= len(short.group(1)) <= 64
for phrase in ('https://example.com/idea-cards', '待补资料'):
    assert phrase in ''.join(p.read_text() for p in (root / 'fixtures').glob('*.md'))
for filename, dimensions in [('icon-512.png', (512, 512)), ('assets/promo-1600x900.png', (1600, 900))]:
    raw = (root / filename).read_bytes()
    assert raw[:8] == b'\x89PNG\r\n\x1a\n', f'{filename} is not PNG'
    actual = struct.unpack('>II', raw[16:24])
    assert actual == dimensions, f'{filename}: {actual}, expected {dimensions}'
print('self-test passed')
PY
