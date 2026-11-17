#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
required=(SKILL.md manifest.yaml agents/openai.yaml README.md README.en.md LICENSE icon-512.png assets/promo-1600x900.png fixtures/success-input.md fixtures/success-output.md fixtures/failure-input.md fixtures/failure-output.md)
for file in "${required[@]}"; do test -s "$file" || { echo "missing or empty: $file" >&2; exit 1; }; done
grep -q '^name: video-overloaded-shot-split-cn$' SKILL.md
grep -q '^name: video-overloaded-shot-split-cn$' manifest.yaml
grep -q '^slug: video-overloaded-shot-split-cn$' manifest.yaml
grep -q '^icon: icon-512.png$' manifest.yaml
grep -q 'allow_implicit_invocation: true' agents/openai.yaml
grep -q '成功样例' README.md
grep -q 'npx skills add xxjrq/video-overloaded-shot-split-cn' README.md
grep -q '不补充存储卡的藏放位置、状态或持拿方式' fixtures/success-output.md
grep -q '不设定追兵人数、距离或装备' fixtures/success-output.md
grep -q '不补充追兵后续位置或主路环境细节' fixtures/success-output.md
grep -q '^补充模板：$' fixtures/failure-output.md
if rg -q '样本的尺寸|出口位置|追赶者|左手|外套内袋|湿漉漉|右手|车灯|两名追兵|八码|巷右|被留在巷内' fixtures/success-output.md fixtures/failure-output.md; then
  echo 'fixtures contain unsupported facts or optional advice' >&2
  exit 1
fi
python3 - <<'PY'
import struct
for path, expected in [('icon-512.png', (512, 512)), ('assets/promo-1600x900.png', (1600, 900))]:
    with open(path, 'rb') as f:
        assert f.read(8) == b'\x89PNG\r\n\x1a\n', f'{path}: not PNG'
        assert f.read(4) == b'\x00\x00\x00\r', f'{path}: invalid IHDR length'
        assert f.read(4) == b'IHDR', f'{path}: missing IHDR'
        w, h = struct.unpack('>II', f.read(8))
    assert (w, h) == expected, f'{path}: got {w}x{h}, expected {expected}'
print('self-test passed')
PY
