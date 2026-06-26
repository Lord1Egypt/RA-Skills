#!/usr/bin/env bash
# Demo of the current uniqc CLI workflow.

set -euo pipefail

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

run_uniqc() {
  if command -v uniqc >/dev/null 2>&1; then
    uniqc "$@"
  else
    python3 -m uniqc "$@"
  fi
}

cat >"$TMP_DIR/build_bell.py" <<'PY'
from uniqc.circuit_builder import Circuit

c = Circuit(2)
c.h(0)
c.cnot(0, 1)
c.measure(0, 1)

with open("bell.ir", "w", encoding="utf-8") as f:
    f.write(c.originir)
PY

echo "[1/4] Build a Bell circuit as OriginIR"
(cd "$TMP_DIR" && python3 build_bell.py)

echo
echo "[2/4] Show circuit info"
run_uniqc circuit "$TMP_DIR/bell.ir" --info

echo
echo "[3/4] Convert to OpenQASM 2.0"
run_uniqc circuit "$TMP_DIR/bell.ir" --format qasm -o "$TMP_DIR/bell.qasm"
sed -n '1,40p' "$TMP_DIR/bell.qasm"

echo
echo "[4/4] Try local simulation and dummy submission"
echo "These steps usually require unified-quantum[simulation]."

if run_uniqc simulate "$TMP_DIR/bell.ir" --shots 1024 --format json; then
  echo
  run_uniqc submit "$TMP_DIR/bell.ir" --platform dummy --wait --format json
else
  echo "Simulation failed. Install unified-quantum[simulation] and retry."
fi
