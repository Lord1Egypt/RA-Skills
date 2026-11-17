#!/usr/bin/env sh
set -eu
base=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
actual=$(mktemp "${TMPDIR:-/tmp}/picklist-success.XXXXXX")
trap 'rm -f "$actual"' EXIT
python3 "$base/scripts/generate_picklist.py" "$base/fixtures/success-input.json" > "$actual"
diff -u "$base/fixtures/success-expected.md" "$actual"
python3 "$base/scripts/generate_picklist.py" "$base/fixtures/failure-input.json" > "$actual"
diff -u "$base/fixtures/failure-expected.md" "$actual"
python3 "$base/scripts/generate_picklist.py" "$base/fixtures/conservative-input.json" > "$actual"
diff -u "$base/fixtures/conservative-expected.md" "$actual"
python3 "$base/scripts/generate_picklist.py" "$base/fixtures/gift-missing-unit-input.json" > "$actual"
diff -u "$base/fixtures/gift-missing-unit-expected.md" "$actual"
python3 "$base/scripts/generate_picklist.py" "$base/fixtures/gift-same-unit-input.json" > "$actual"
diff -u "$base/fixtures/gift-same-unit-expected.md" "$actual"
python3 "$base/scripts/generate_picklist.py" "$base/fixtures/mixed-units-input.json" > "$actual"
diff -u "$base/fixtures/mixed-units-expected.md" "$actual"
summary=$(awk '/^## 拆套后组件汇总/{inside=1; next} /^## /{inside=0} inside' "$actual")
if printf '%s\n' "$summary" | grep -Eq 'BEANS|GIFT|EXTRA' || ! printf '%s\n' "$summary" | grep -q 'STRAP × 1 条'; then
  echo "component summary must contain kit parts only" >&2
  exit 1
fi
python3 "$base/scripts/generate_picklist.py" "$base/fixtures/gift-same-unit-input.json" > "$actual"
summary=$(awk '/^## 拆套后组件汇总/{inside=1; next} /^## /{inside=0} inside' "$actual")
if printf '%s\n' "$summary" | grep -q 'GIFT'; then
  echo "gift must not be mixed into kit-component summary" >&2
  exit 1
fi
python3 - "$base/scripts/generate_picklist.py" <<'PY'
import json, subprocess, sys, tempfile
from pathlib import Path
script = sys.argv[1]
kit = {"K": [{"sku":"P", "quantity":1, "unit":"个"}]}
payload = {"kits":kit,"orders":[{"id":"cap","items":[{"sku":"K","quantity":1,"unit":"套"} for _ in range(60)]}]}
with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as f:
    json.dump(payload, f); f.flush()
    r = subprocess.run([sys.executable, script, f.name], capture_output=True, text=True)
    if r.returncode == 0 or "100 条" not in r.stderr: raise SystemExit("60 kit parents plus 60 parts must exceed the 100-row cap")
payload = {"kits":{"K":[{"sku":"P","quantity":1,"unit":"   "}]},"orders":[{"id":"1","items":[{"sku":"K","quantity":1,"unit":"套"}]}]}
with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as f:
    json.dump(payload, f); f.flush()
    r = subprocess.run([sys.executable, script, f.name], capture_output=True, text=True)
    if r.returncode or "组件资料不完整" not in r.stdout or "- [ ] K" in r.stdout or "- [ ] P" in r.stdout or "P ×" in r.stdout.split("## 拆套后组件汇总", 1)[1].split("## 待确认项", 1)[0]: raise SystemExit("blank kit component unit must not create executable rows or a component total")
payload = {"orders":[{"id":"1","items":[{"sku":"A","quantity":1,"unit":"   "}]}]}
with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as f:
    json.dump(payload, f); f.flush()
    r = subprocess.run([sys.executable, script, f.name], capture_output=True, text=True)
    if r.returncode or "缺少单位" not in r.stdout or "- [ ] A" in r.stdout: raise SystemExit("blank item unit must be reported, not made executable")
PY
echo "self-test passed: success, conservative missing-data, valid same-unit gift, missing-unit, and mixed-unit gift-threshold fixtures rendered safely"
