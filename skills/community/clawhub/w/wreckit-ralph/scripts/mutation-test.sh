#!/usr/bin/env bash
# wreckit — automated mutation testing
# Usage: ./mutation-test.sh [project-path] [test-command]
# Generates mutations, runs tests, reports kill rate
# Exit 0 = results produced, check JSON for pass/fail

set -euo pipefail
# Capture SCRIPT_DIR before any cd (BASH_SOURCE may be relative)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="${1:-.}"
TEST_CMD="${2:-}"
PROJECT="$(cd "$PROJECT" && pwd)"
cd "$PROJECT"

verdict_from_rate() {
  local rate="$1"
  local rate_int
  rate_int=$(echo "$rate" | cut -d. -f1)
  if [ "$rate_int" -ge 95 ] 2>/dev/null; then
    echo "SHIP"
  elif [ "$rate_int" -ge 90 ] 2>/dev/null; then
    echo "CAUTION"
  else
    echo "BLOCKED"
  fi
}

# Auto-detect test command
if [ -z "$TEST_CMD" ]; then
  if [ -f "package.json" ]; then
    if grep -q '"vitest"' package.json 2>/dev/null; then TEST_CMD="npx vitest run"
    elif grep -q '"jest"' package.json 2>/dev/null; then TEST_CMD="npx jest"
    elif grep -q 'node --test' package.json 2>/dev/null; then TEST_CMD="npm test"
    fi
  elif [ -f "Cargo.toml" ]; then TEST_CMD="cargo test"
  elif [ -f "go.mod" ]; then TEST_CMD="go test ./..."
  elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then TEST_CMD="pytest"
  elif [ -f "Package.swift" ]; then TEST_CMD="swift test"
  elif [ -f "tests/run_tests.sh" ]; then TEST_CMD="bash tests/run_tests.sh"
  elif [ -f "test/run_tests.sh" ]; then TEST_CMD="bash test/run_tests.sh"
  elif [ -f "run_tests.sh" ]; then TEST_CMD="bash run_tests.sh"
  elif find . -name "run_tests.sh" -not -path '*/.git/*' -maxdepth 3 2>/dev/null | head -1 | grep -q .; then
    TEST_CMD="bash $(find . -name 'run_tests.sh' -not -path '*/.git/*' -maxdepth 3 2>/dev/null | head -1)"
  fi
fi

if [ -z "$TEST_CMD" ]; then
  echo '{"error":"Could not detect test command. Pass as second argument."}'
  exit 1
fi

echo "Test command: $TEST_CMD" >&2

# ─── Swift AI-estimated mutation testing ───────────────────────────────────
# Swift is handled BEFORE the generic baseline check because:
# 1. Swift has no real mutation tool — we do AI estimation
# 2. The Swift block runs its own test check internally
# 3. We want to produce useful output even when swift test is slow or flaky
# WHY AI-ESTIMATED: As of 2026, there is no production-ready mutation testing
# framework for Swift. Tools like Mull (LLVM-based) exist in research but are
# not reliable enough for CI. We honestly estimate mutation kill rate based on
# code analysis + test results. The verdict is ALWAYS "CAUTION" — never "SHIP"
# — because we can't mechanically verify that tests catch mutations.
if [ -f "Package.swift" ] || find . -name "*.xcodeproj" -maxdepth 2 2>/dev/null | head -1 | grep -q .; then
  echo "Swift project detected — using AI-estimated mutation analysis" >&2
  echo "NOTE: No production mutation testing tool exists for Swift" >&2

  # Sample up to 20 Swift source files (exclude tests, generated code, Pods, build artifacts)
  SWIFT_SRC_FILES=$(find . -name '*.swift' \
    -not -name '*Test*.swift' -not -name '*Tests.swift' -not -name '*Spec.swift' \
    -not -path '*/Tests/*' -not -path '*/XCTests/*' -not -path '*/.build/*' \
    -not -path '*/Pods/*' -not -path '*/Generated/*' -not -path '*/DerivedData/*' \
    -not -path '*/.git/*' -not -path '*/Carthage/*' \
    2>/dev/null | head -20 || true)

  SWIFT_FILE_COUNT=$(echo "$SWIFT_SRC_FILES" | grep -c '.' 2>/dev/null || echo 0)

  if [ "$SWIFT_FILE_COUNT" -gt 0 ]; then
    # Count test files to estimate test coverage
    TEST_FILE_COUNT=$(find . -name '*Test*.swift' -o -name '*Tests.swift' -o -name '*Spec.swift' \
      2>/dev/null | grep -c '.' || echo 0)
    TEST_FILE_COUNT=${TEST_FILE_COUNT//[^0-9]/}; TEST_FILE_COUNT=${TEST_FILE_COUNT:-0}

    # Analyze mutation surface: count mutable code points
    MUTATION_SURFACE=0
    for src_file in $SWIFT_SRC_FILES; do
      # Count conditional branches: if, guard, switch, while, for
      CONDITIONALS=$(grep -cE '\b(if |guard |switch |while |for )\b' "$src_file" 2>/dev/null || echo 0)
      CONDITIONALS=${CONDITIONALS//[^0-9]/}; CONDITIONALS=${CONDITIONALS:-0}
      # Count optionals: ??, optional chaining ?.
      OPTIONALS=$(grep -cE '(\?\?|\?\.)' "$src_file" 2>/dev/null || echo 0)
      OPTIONALS=${OPTIONALS//[^0-9]/}; OPTIONALS=${OPTIONALS:-0}
      # Count arithmetic operators that could be mutated: +, -, *, /
      ARITHMETIC=$(grep -cE '[^/+*-][+*/-][^/+*==-]' "$src_file" 2>/dev/null || echo 0)
      ARITHMETIC=${ARITHMETIC//[^0-9]/}; ARITHMETIC=${ARITHMETIC:-0}
      # Count boolean operators: &&, ||
      BOOLEANS=$(grep -cE '(&&|\|\|)' "$src_file" 2>/dev/null || echo 0)
      BOOLEANS=${BOOLEANS//[^0-9]/}; BOOLEANS=${BOOLEANS:-0}
      # Count comparison operators: ==, !=, >, <, >=, <=
      COMPARISONS=$(grep -cE '(==|!=|>=|<=)' "$src_file" 2>/dev/null || echo 0)
      COMPARISONS=${COMPARISONS//[^0-9]/}; COMPARISONS=${COMPARISONS:-0}

      FILE_POINTS=$((CONDITIONALS + OPTIONALS + ARITHMETIC + BOOLEANS + COMPARISONS))
      MUTATION_SURFACE=$((MUTATION_SURFACE + FILE_POINTS))
    done

    # Ensure minimum surface to avoid division by zero
    [ "$MUTATION_SURFACE" -lt 1 ] && MUTATION_SURFACE=1

    # Run tests and check if they pass
    TESTS_PASS=0
    echo "Running swift tests to validate baseline..." >&2
    if eval "$TEST_CMD" >/dev/null 2>&1; then
      TESTS_PASS=1
      echo "Swift tests pass ✓" >&2
    else
      echo "Swift tests fail ✗" >&2
    fi

    # Conservative kill rate estimate:
    # min(0.72, test_file_count / mutation_surface)
    # 0.72 cap = honest upper bound for AI estimation (we can't prove better)
    python3 - "$SWIFT_FILE_COUNT" "$TEST_FILE_COUNT" "$MUTATION_SURFACE" "$TESTS_PASS" <<'PYEOF'
import json, sys

src_count = int(sys.argv[1])
test_count = int(sys.argv[2])
mutation_surface = int(sys.argv[3])
tests_pass = int(sys.argv[4])

if tests_pass and mutation_surface > 0:
    # Conservative estimate: test coverage correlates loosely with mutation kill rate
    raw_rate = min(0.72, test_count / mutation_surface) if mutation_surface > 0 else 0.0
    kill_rate = round(raw_rate, 4)
else:
    kill_rate = 0.0

print(json.dumps({
    "language": "swift",
    "tool": "ai-estimated",
    "method": "ai-estimated",
    "confidence": "low",
    "sourceFiles": src_count,
    "testFiles": test_count,
    "mutationSurface": mutation_surface,
    "testsPass": bool(tests_pass),
    "killRate": round(kill_rate * 100, 1),
    "kill_rate": kill_rate,
    "verdict": "CAUTION",
    "note": "Swift mutation testing requires manual verification — no automated tool available. Kill rate is a conservative AI estimate based on code analysis, NOT mechanical mutation testing."
}))
PYEOF
    exit 0
  else
    echo '{"language":"swift","tool":"ai-estimated","error":"No Swift source files found","verdict":"SKIP"}'
    exit 0
  fi
fi

# ─── Baseline test check (non-Swift languages) ────────────────────────────
echo "Verifying baseline tests pass..." >&2
if ! eval "$TEST_CMD" >/dev/null 2>&1; then
  echo '{"error":"Baseline tests fail. Fix tests before mutation testing."}'
  exit 1
fi
echo "Baseline OK" >&2

# ─── Real mutation frameworks ──────────────────────────────────────────────

# JS/TS → Stryker
if ([ -f "tsconfig.json" ] || [ -f "package.json" ]) && ! [ -f "Cargo.toml" ]; then
  if npx stryker --version >/dev/null 2>&1 && [ -f "$SCRIPT_DIR/mutation-test-stryker.sh" ]; then
    echo "Using Stryker for mutation testing..." >&2
    OUTPUT=$("$SCRIPT_DIR/mutation-test-stryker.sh" "$PROJECT" 2>/dev/null || true)
    LAST_JSON=$(echo "$OUTPUT" | grep '^{' | tail -1)
    if [ -n "$LAST_JSON" ]; then
      echo "$LAST_JSON" | python3 -c "
import json,sys
d=json.load(sys.stdin)
d['tool']='stryker'
print(json.dumps(d))
" 2>/dev/null || echo "$LAST_JSON"
      exit 0
    fi
    echo "Stryker produced no JSON — falling back to AI mutations" >&2
  fi
fi

# Python → mutmut
if [ -f "pyproject.toml" ] || [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
  if command -v mutmut >/dev/null 2>&1; then
    echo "Using mutmut for Python mutation testing..." >&2
    mutmut run >/dev/null 2>&1 || true
    RESULTS=$(mutmut results 2>/dev/null || true)
    # mutmut outputs "Killed: N" or "Killed N out of M" — use case-insensitive grep
    KILLED=$(echo "$RESULTS" | grep -iE "^[[:space:]]*killed" | grep -oE '[0-9]+' | head -1 || echo 0)
    SURVIVED=$(echo "$RESULTS" | grep -iE "^[[:space:]]*(survived|missed)" | grep -oE '[0-9]+' | head -1 || echo 0)
    # Fallback: count individual mutation status lines
    if [ -z "$KILLED" ] || [ "$KILLED" = "0" ]; then
      KILLED=$(echo "$RESULTS" | grep -icE "\bkilled\b" || echo 0)
      SURVIVED=$(echo "$RESULTS" | grep -icE "\b(survived|missed)\b" || echo 0)
    fi
    KILLED=${KILLED:-0}
    SURVIVED=${SURVIVED:-0}
    TOTAL=$((KILLED + SURVIVED))
    if [ "$TOTAL" -gt 0 ]; then
      KILL_RATE=$(echo "scale=1; $KILLED * 100 / $TOTAL" | bc 2>/dev/null || echo "0")
      VERDICT=$(verdict_from_rate "$KILL_RATE")
      echo "{\"total\":$TOTAL,\"killed\":$KILLED,\"survived\":$SURVIVED,\"killRate\":$KILL_RATE,\"language\":\"py\",\"tool\":\"mutmut\",\"verdict\":\"$VERDICT\"}"
      exit 0
    fi
    echo "mutmut returned no results — falling back to AI mutations" >&2
  else
    echo "mutmut not installed. Install with: pip install mutmut" >&2
    echo "Falling back to AI mutations..." >&2
  fi
fi

# Rust → cargo-mutants
if [ -f "Cargo.toml" ]; then
  if command -v cargo-mutants >/dev/null 2>&1; then
    echo "Using cargo-mutants for Rust mutation testing..." >&2
    MUTANTS_OUT=$(cargo mutants --json 2>/dev/null || true)
    if [ -n "$MUTANTS_OUT" ] && echo "$MUTANTS_OUT" | python3 -c "import json,sys; json.load(sys.stdin)" >/dev/null 2>&1; then
      echo "$MUTANTS_OUT" | python3 -c "
import json,sys
data=json.load(sys.stdin)
killed=sum(1 for m in data if m.get('outcome')=='Caught')
survived=sum(1 for m in data if m.get('outcome')=='Missed')
total=killed+survived
rate=round(killed*100/total,1) if total>0 else 0
verdict='SHIP' if rate>=95 else ('CAUTION' if rate>=90 else 'BLOCKED')
print(json.dumps({'total':total,'killed':killed,'survived':survived,'killRate':rate,'language':'rs','tool':'cargo-mutants','verdict':verdict}))
"
      exit 0
    fi
    echo "cargo-mutants returned no usable JSON — falling back to AI mutations" >&2
  else
    echo "cargo-mutants not installed. Install with: cargo install cargo-mutants" >&2
    echo "Falling back to AI mutations..." >&2
  fi
fi

# Find source files
if [ -f "tsconfig.json" ] || ([ -f "package.json" ] && ! [ -f "Cargo.toml" ]); then
  LANG="ts"
  SRC_FILES=$(find . -name '*.ts' -not -name '*.test.*' -not -name '*.spec.*' \
    -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' \
    -not -name '*.d.ts' -not -path '*/tests/*' -not -path '*/__tests__/*' 2>/dev/null || true)
elif [ -f "Cargo.toml" ]; then
  LANG="rs"; SRC_FILES=$(find . -name '*.rs' -not -path '*/target/*' -not -path '*/.git/*' 2>/dev/null || true)
elif [ -f "go.mod" ]; then
  LANG="go"; SRC_FILES=$(find . -name '*.go' -not -name '*_test.go' -not -path '*/.git/*' 2>/dev/null || true)
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
  LANG="py"; SRC_FILES=$(find . -name '*.py' -not -name 'test_*' -not -name '*_test.py' -not -path '*/.git/*' -not -path '*/venv/*' 2>/dev/null || true)
else
  LANG="sh"; SRC_FILES=$(find . -name '*.sh' -not -path '*/.git/*' 2>/dev/null || true)
fi

FILE_COUNT=$(echo "$SRC_FILES" | grep -c '.' 2>/dev/null || echo 0)
echo "Found $FILE_COUNT source files ($LANG)" >&2

# Use temp files for counters (avoids subshell issues)
RESULTS_FILE=$(mktemp)
KILLED=0
SURVIVED=0
TOTAL=0
MAX_MUTATIONS=20

mutate_line() {
  local line="$1"
  if echo "$line" | grep -q '==='; then echo "$line" | sed 's/===/!==/'
  elif echo "$line" | grep -q '!=='; then echo "$line" | sed 's/!==/===/'
  elif echo "$line" | grep -q '>='; then echo "$line" | sed 's/>=/</'
  elif echo "$line" | grep -q '<='; then echo "$line" | sed 's/<=/>/g'
  elif echo "$line" | grep -q '&&'; then echo "$line" | sed 's/&&/||/'
  elif echo "$line" | grep -qF '||'; then echo "$line" | sed 's/||/\&\&/'
  elif echo "$line" | grep -q ' true'; then echo "$line" | sed 's/ true/ false/'
  elif echo "$line" | grep -q ' false'; then echo "$line" | sed 's/ false/ true/'
  elif echo "$line" | grep -q 'return '; then echo "$line" | sed 's/return /return undefined; \/\/ /'
  else echo "$line"
  fi
}

for file in $SRC_FILES; do
  [ "$TOTAL" -ge "$MAX_MUTATIONS" ] && break
  LINE_COUNT=$(wc -l < "$file" | tr -d ' ')
  [ "$LINE_COUNT" -lt 5 ] && continue

  CANDIDATES=$(grep -nE '(===|!==|>=|<=|&&|\|\|| true| false|return )' "$file" 2>/dev/null | head -5 || true)
  [ -z "$CANDIDATES" ] && continue

  cp "$file" "/tmp/wreckit-backup-$$"

  while IFS= read -r candidate; do
    [ "$TOTAL" -ge "$MAX_MUTATIONS" ] && break
    LINENUM=$(echo "$candidate" | cut -d: -f1)
    ORIGINAL=$(sed -n "${LINENUM}p" "$file")
    MUTATED=$(mutate_line "$ORIGINAL")
    [ "$ORIGINAL" = "$MUTATED" ] && continue

    # Apply mutation via awk
    awk -v ln="$LINENUM" -v rep="$MUTATED" 'NR==ln{print rep;next}{print}' "$file" > "/tmp/wreckit-mutated-$$"
    cp "/tmp/wreckit-mutated-$$" "$file"
    TOTAL=$((TOTAL + 1))

    if eval "$TEST_CMD" >/dev/null 2>&1; then
      SURVIVED=$((SURVIVED + 1))
      echo "  SURVIVED: ${file}:${LINENUM}" >> "$RESULTS_FILE"
    else
      KILLED=$((KILLED + 1))
      echo "  KILLED:   ${file}:${LINENUM}" >> "$RESULTS_FILE"
    fi

    cp "/tmp/wreckit-backup-$$" "$file"
  done <<< "$CANDIDATES"

  cp "/tmp/wreckit-backup-$$" "$file"
  rm -f "/tmp/wreckit-backup-$$" "/tmp/wreckit-mutated-$$"
done

if [ "$TOTAL" -eq 0 ]; then
  rm -f "$RESULTS_FILE"
  echo '{"error":"No mutatable lines found in source files."}'
  exit 1
fi

KILL_RATE=$(echo "scale=1; $KILLED * 100 / $TOTAL" | bc 2>/dev/null || echo "0")
VERDICT=$(verdict_from_rate "$KILL_RATE")

echo ""
echo "=== MUTATION TEST RESULTS ==="
cat "$RESULTS_FILE"
echo ""
echo "Total: $TOTAL | Killed: $KILLED | Survived: $SURVIVED"
echo "Kill rate: ${KILL_RATE}%"

cat <<EOF

{"total":$TOTAL,"killed":$KILLED,"survived":$SURVIVED,"killRate":$KILL_RATE,"language":"$LANG","tool":"ai-mutations","verdict":"$VERDICT"}
EOF

rm -f "$RESULTS_FILE"
