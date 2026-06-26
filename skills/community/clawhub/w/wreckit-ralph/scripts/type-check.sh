#!/usr/bin/env bash
# wreckit — Type Check gate
# Detects and runs the type checker for the project
# Usage: ./type-check.sh [project-path]
# Output: JSON with status PASS/FAIL/ERROR

set -euo pipefail
PROJECT="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="$(cd "$PROJECT" && pwd)"
cd "$PROJECT"

STACK_JSON=$("$SCRIPT_DIR/detect-stack.sh" "$PROJECT" 2>/dev/null || true)
TYPE_CMD=$(echo "$STACK_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('commands',{}).get('typeCheck','none'))" 2>/dev/null || echo "none")
TYPE_CHECKER=$(echo "$STACK_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('typeChecker','none'))" 2>/dev/null || echo "none")
DETECTED_LANG=$(echo "$STACK_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('language','unknown'))" 2>/dev/null || echo "unknown")

# ─── Swift-specific type checking ────────────────────────────────────────────
# Swift's compiler IS the type checker — `swift build` or `xcodebuild` catches
# all type errors, missing imports, protocol conformance issues, etc.
if [ "$DETECTED_LANG" = "swift" ]; then
  # Check if Swift toolchain is available
  if ! command -v swift >/dev/null 2>&1 && ! command -v xcodebuild >/dev/null 2>&1; then
    python3 -c "
import json
print(json.dumps({
    'lang': 'swift',
    'error': 'swift toolchain not installed',
    'verdict': 'SKIP',
    'tool': 'none',
    'status': 'SKIP'
}))
"
    exit 0
  fi

  BUILD_SYSTEM=$(echo "$STACK_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('buildSystem','unknown'))" 2>/dev/null || echo "unknown")

  SWIFT_TOOL=""
  SWIFT_EXIT=0
  SWIFT_OUTPUT=""

  if [ -f "Package.swift" ] && command -v swift >/dev/null 2>&1; then
    # SPM project — swift build is the type checker
    SWIFT_TOOL="swift build"
    SWIFT_OUTPUT=$(swift build 2>&1) || SWIFT_EXIT=$?
  elif command -v xcodebuild >/dev/null 2>&1; then
    # Xcode project — use xcodebuild with scheme detection
    SWIFT_TOOL="xcodebuild"
    SCHEME=$(xcodebuild -list 2>/dev/null | sed -n '/Schemes:/,/^$/p' | grep -m1 '^\s' | xargs 2>/dev/null || echo "")
    if [ -n "$SCHEME" ]; then
      SWIFT_OUTPUT=$(xcodebuild build -scheme "$SCHEME" -quiet 2>&1) || SWIFT_EXIT=$?
    else
      # Fallback: try without specifying scheme
      SWIFT_OUTPUT=$(xcodebuild build -quiet 2>&1) || SWIFT_EXIT=$?
    fi
  else
    python3 -c "
import json
print(json.dumps({
    'lang': 'swift',
    'error': 'No suitable build tool found for this project layout',
    'verdict': 'SKIP',
    'tool': 'none',
    'status': 'SKIP'
}))
"
    exit 0
  fi

  # Count errors and warnings from Swift/Xcode output
  ERRORS=$(echo "$SWIFT_OUTPUT" | { grep -ciE '\berror:' 2>/dev/null || true; })
  ERRORS=${ERRORS:-0}
  WARNINGS=$(echo "$SWIFT_OUTPUT" | { grep -ciE '\bwarning:' 2>/dev/null || true; })
  WARNINGS=${WARNINGS:-0}

  if [ "$SWIFT_EXIT" -eq 0 ]; then
    VERDICT="PASS"
  else
    VERDICT="FAIL"
  fi

  python3 - "$VERDICT" "$SWIFT_TOOL" "$ERRORS" "$WARNINGS" "$BUILD_SYSTEM" <<'PYEOF'
import json, sys
verdict, tool, errors, warnings, build_system = sys.argv[1:]
raw = sys.stdin.read()
if len(raw) > 4000:
    raw = raw[:4000] + "\n...truncated..."
print(json.dumps({
    "lang": "swift",
    "tool": tool,
    "errors": int(errors),
    "warnings": int(warnings),
    "verdict": verdict,
    "status": verdict,
    "buildSystem": build_system,
    "raw_output": raw,
    "confidence": 1.0 if int(errors) > 0 or verdict == "PASS" else 0.5
}))
PYEOF
  exit 0
fi

# ─── Generic type checking (non-Swift languages) ────────────────────────────
if [ -z "$TYPE_CMD" ] || [ "$TYPE_CMD" = "none" ]; then
  python3 - <<'PYEOF'
import json
print(json.dumps({
  "status": "ERROR",
  "tool": "none",
  "errors": 0,
  "warnings": 0,
  "output": "No type checker detected.",
  "confidence": 0.5
}))
PYEOF
  exit 1
fi

TOOL="$TYPE_CHECKER"
case "$TYPE_CHECKER" in
  rustc) TOOL="cargo check" ;;
  go) TOOL="go vet" ;;
  tsc|pyright|mypy) TOOL="$TYPE_CHECKER" ;;
  *) TOOL="$TYPE_CHECKER" ;;
esac

TYPE_EXIT=0
OUTPUT=$(eval "$TYPE_CMD" 2>&1) || TYPE_EXIT=$?
OUTPUT=${OUTPUT:-}

ERRORS=$(echo "$OUTPUT" | { grep -ciE '\berror\b' 2>/dev/null || true; })
ERRORS=${ERRORS:-0}
WARNINGS=$(echo "$OUTPUT" | { grep -ciE '\bwarn(ing)?\b' 2>/dev/null || true; })
WARNINGS=${WARNINGS:-0}

STATUS="PASS"
if [ -z "$OUTPUT" ]; then
  STATUS="PASS"
elif [ "$TYPE_EXIT" -ne 0 ] && [ "$ERRORS" -gt 0 ]; then
  STATUS="FAIL"
elif [ "$TYPE_EXIT" -ne 0 ] && [ "$ERRORS" -eq 0 ]; then
  STATUS="WARN"
else
  STATUS="PASS"
fi

CONFIDENCE="0.0"
if [ "$ERRORS" -gt 0 ] 2>/dev/null; then
  CONFIDENCE="1.0"
elif [ "$TYPE_EXIT" -ne 0 ] 2>/dev/null; then
  CONFIDENCE="0.5"
fi

python3 - "$STATUS" "$TOOL" "$ERRORS" "$WARNINGS" "$CONFIDENCE" <<'PYEOF'
import json, sys
status, tool, errors, warnings, confidence = sys.argv[1:]
output = sys.stdin.read()
if len(output) > 4000:
    output = output[:4000] + "\n...truncated..."
print(json.dumps({
  "status": status,
  "tool": tool,
  "errors": int(errors),
  "warnings": int(warnings),
  "output": output,
  "confidence": float(confidence)
}))
PYEOF
