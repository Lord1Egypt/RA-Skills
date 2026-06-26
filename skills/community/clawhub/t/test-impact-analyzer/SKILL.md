---
name: test-impact-analyzer
description: Determine which tests need to run for a given code change — trace file dependencies, map source-to-test relationships, identify untested changes, and prioritize test execution order for faster CI feedback.
---

# Test Impact Analyzer

Don't run all tests for every change. Analyze which source files changed, trace their dependencies, find the corresponding tests, and produce a targeted test execution plan. Faster CI, focused testing, immediate feedback.

Use when: "which tests should I run", "what does this change affect", "test impact analysis", "optimize CI test time", "what tests cover this file", "skip unrelated tests", or speeding up CI pipelines.

## Commands

### 1. `affected` — Find Tests Affected by Changes

Given a set of changed files (from git diff), find all tests that should run.

```bash
# Get changed files (compared to main/master)
BASE_BRANCH="${1:-main}"
CHANGED_FILES=$(git diff --name-only "$BASE_BRANCH"...HEAD 2>/dev/null || git diff --name-only HEAD~1 2>/dev/null)

if [ -z "$CHANGED_FILES" ]; then
  echo "No changed files detected. Specify base branch or ensure you're on a feature branch."
  exit 0
fi

echo "Changed files:"
echo "$CHANGED_FILES" | sed 's/^/  /'
echo ""
```

#### Step 1: Direct Test Matches

```bash
echo "=== Direct Test Matches ==="
echo "$CHANGED_FILES" | while read f; do
  # Skip non-source files
  echo "$f" | grep -qE '\.(ts|js|tsx|jsx|py|go|rs|java)$' || continue
  # Skip test files themselves
  echo "$f" | grep -qE '\.(test|spec)\.' && continue

  BASE=$(basename "$f" | sed 's/\.[^.]*$//')
  DIR=$(dirname "$f")

  # Find corresponding test file
  for pattern in "${BASE}.test.ts" "${BASE}.test.js" "${BASE}.test.tsx" "${BASE}.test.jsx" \
                  "${BASE}.spec.ts" "${BASE}.spec.js" "${BASE}.spec.tsx" \
                  "test_${BASE}.py" "${BASE}_test.py" "${BASE}_test.go"; do
    FOUND=$(find "$DIR" -maxdepth 2 -name "$pattern" -not -path '*/node_modules/*' 2>/dev/null | head -1)
    if [ -n "$FOUND" ]; then
      echo "  $f → $FOUND"
      break
    fi
  done
done
```

#### Step 2: Import Chain Analysis

```bash
echo ""
echo "=== Import Chain (files that import changed files) ==="
echo "$CHANGED_FILES" | while read f; do
  echo "$f" | grep -qE '\.(ts|js|tsx|jsx)$' || continue
  echo "$f" | grep -qE '\.(test|spec)\.' && continue

  BASE=$(basename "$f" | sed 's/\.[^.]*$//')
  DIR=$(dirname "$f")

  # Find files that import this module
  # Match relative imports like: from './module' or from '../utils/module'
  IMPORTERS=$(rg -l "from ['\"]\..*/${BASE}['\"]|from ['\"]\./${BASE}['\"]|require\(['\"]\..*/${BASE}['\"]\)" \
    -g '*.{ts,js,tsx,jsx}' -g '!node_modules' -g '!dist' 2>/dev/null)

  if [ -n "$IMPORTERS" ]; then
    echo "  $f is imported by:"
    echo "$IMPORTERS" | while read imp; do
      IMP_BASE=$(basename "$imp" | sed 's/\.[^.]*$//')
      # Is the importer a test file?
      if echo "$imp" | grep -qE '\.(test|spec)\.'; then
        echo "    🧪 $imp (test — should run)"
      else
        # Check if the importer has its own test
        TEST=$(find "$(dirname "$imp")" -maxdepth 2 \
          -name "${IMP_BASE}.test.*" -o -name "${IMP_BASE}.spec.*" 2>/dev/null | head -1)
        if [ -n "$TEST" ]; then
          echo "    📄 $imp → 🧪 $TEST (transitive)"
        else
          echo "    📄 $imp (no test found)"
        fi
      fi
    done
  fi
done
```

#### Step 3: Collect All Tests to Run

```bash
echo ""
echo "=== Test Execution Plan ==="

# Collect unique test files
TESTS_TO_RUN=$(mktemp)

echo "$CHANGED_FILES" | while read f; do
  echo "$f" | grep -qE '\.(test|spec)\.' && echo "$f" >> "$TESTS_TO_RUN"

  BASE=$(basename "$f" | sed 's/\.[^.]*$//')
  DIR=$(dirname "$f")

  # Direct test matches
  find "$DIR" -maxdepth 2 \( -name "${BASE}.test.*" -o -name "${BASE}.spec.*" -o -name "test_${BASE}.*" -o -name "${BASE}_test.*" \) \
    -not -path '*/node_modules/*' 2>/dev/null >> "$TESTS_TO_RUN"

  # Tests from importers
  IMPORTERS=$(rg -l "from ['\"]\..*/${BASE}['\"]|from ['\"]\./${BASE}['\"]" \
    -g '*.{test.*,spec.*}' -g '!node_modules' 2>/dev/null)
  echo "$IMPORTERS" >> "$TESTS_TO_RUN" 2>/dev/null
done

UNIQUE_TESTS=$(sort -u "$TESTS_TO_RUN" | grep -v '^$')
TOTAL=$(echo "$UNIQUE_TESTS" | grep -c "." 2>/dev/null || echo "0")
ALL_TESTS=$(find . -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" \) \
  -not -path '*/node_modules/*' 2>/dev/null | wc -l)

echo "Tests to run: $TOTAL / $ALL_TESTS total ($(echo "scale=0; $TOTAL * 100 / ($ALL_TESTS + 1)" | bc)%)"
echo ""
echo "$UNIQUE_TESTS" | sed 's/^/  /'

rm -f "$TESTS_TO_RUN"
```

### 2. `map` — Source-to-Test Mapping

Build a complete map of which source files are covered by which tests.

```bash
echo "=== Source → Test Map ==="

find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.tsx" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" \) \
  -not -path '*/node_modules/*' -not -path '*/vendor/*' -not -path '*/dist/*' \
  -not -name '*.test.*' -not -name '*.spec.*' -not -name 'test_*' 2>/dev/null | sort | while read f; do
  BASE=$(basename "$f" | sed 's/\.[^.]*$//')
  DIR=$(dirname "$f")

  TEST=$(find "$DIR" -maxdepth 2 \( -name "${BASE}.test.*" -o -name "${BASE}.spec.*" -o -name "test_${BASE}.*" -o -name "${BASE}_test.*" \) \
    -not -path '*/node_modules/*' 2>/dev/null | head -1)

  if [ -n "$TEST" ]; then
    echo "✅ $f → $TEST"
  else
    echo "�� $f → (no test)"
  fi
done
```

Summary stats:
```
Coverage map: X/Y files have corresponding tests (Z%)
Untested critical files (by size):
  1. src/core/engine.ts (450 lines) — NO TEST
  2. src/api/handlers.ts (320 lines) — NO TEST
```

### 3. `gaps` — Find Untested Code Paths

Identify source files without tests, prioritized by risk.

```bash
echo "=== Untested Files (by risk) ==="

python3 -c "
import subprocess, os

# Get all source files
src = subprocess.run(
    ['find', '.', '-type', 'f', '(', '-name', '*.ts', '-o', '-name', '*.js', '-o', '-name', '*.py', ')',
     '-not', '-path', '*/node_modules/*', '-not', '-path', '*/dist/*',
     '-not', '-name', '*.test.*', '-not', '-name', '*.spec.*', '-not', '-name', 'test_*'],
    capture_output=True, text=True
).stdout.strip().split('\n')

untested = []
for f in src:
    if not f: continue
    base = os.path.splitext(os.path.basename(f))[0]
    d = os.path.dirname(f)

    # Check for test file
    has_test = False
    for pattern in [f'{base}.test', f'{base}.spec', f'test_{base}', f'{base}_test']:
        result = subprocess.run(
            ['find', d, '-maxdepth', '2', '-name', f'{pattern}.*'],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            has_test = True
            break

    if not has_test:
        # Get file size and git churn
        try:
            lines = sum(1 for _ in open(f))
        except:
            lines = 0

        try:
            churn = int(subprocess.run(
                ['git', 'log', '--since=90 days ago', '--oneline', '--', f],
                capture_output=True, text=True
            ).stdout.strip().count('\n')) + 1
        except:
            churn = 0

        risk = lines * 0.5 + churn * 10  # larger + more active = higher risk
        untested.append((risk, lines, churn, f))

untested.sort(reverse=True)
print(f'Untested files: {len(untested)} / {len(src)} ({len(untested)*100//max(len(src),1)}%)')
print()
print('Top 20 by risk (size × activity):')
for risk, lines, churn, f in untested[:20]:
    print(f'  [{lines:>4} lines, {churn:>2} commits] {f}')
" 2>/dev/null
```

### 4. `order` — Optimal Test Execution Order

Prioritize test execution for fastest feedback:

1. **Tests for changed files** — most likely to fail, run first
2. **Tests for files importing changed files** — transitive impact
3. **Integration/E2E tests** — broader coverage, run if unit tests pass
4. **Everything else** — only in full CI run

```bash
echo "=== Recommended Test Order ==="
echo ""
echo "Phase 1 — Direct (run immediately, ~seconds):"
# Changed files' tests
echo "Phase 2 — Transitive (if Phase 1 passes, ~minutes):"
# Tests that import changed modules
echo "Phase 3 ��� Integration (if Phase 2 passes, ~minutes):"
# E2E/integration tests in affected areas
echo "Phase 4 — Full suite (nightly/merge, ~minutes-hours):"
# Everything
```

### 5. `ci` — Generate CI Test Commands

Output the exact commands to run only affected tests.

```bash
# For Jest
JEST_TESTS=$(echo "$UNIQUE_TESTS" | grep -E '\.(test|spec)\.(ts|js|tsx|jsx)$' | tr '\n' ' ')
if [ -n "$JEST_TESTS" ]; then
  echo "Jest command:"
  echo "  npx jest --passWithNoTests $JEST_TESTS"
fi

# For pytest
PYTEST_TESTS=$(echo "$UNIQUE_TESTS" | grep -E '(test_.*\.py|.*_test\.py)$' | tr '\n' ' ')
if [ -n "$PYTEST_TESTS" ]; then
  echo "Pytest command:"
  echo "  pytest $PYTEST_TESTS"
fi

# For Go
GO_TESTS=$(echo "$UNIQUE_TESTS" | grep -E '_test\.go$' | xargs -I{} dirname {} | sort -u | tr '\n' ' ')
if [ -n "$GO_TESTS" ]; then
  echo "Go test command:"
  echo "  go test $GO_TESTS"
fi
```

## Output Formats

- **text** (default): Human-readable with file tree
- **json**: `{changed_files: [], affected_tests: [], untested_changes: [], execution_plan: {phases: []}}`
- **paths**: Plain list of test file paths (pipe to test runner)

## CI Integration

```yaml
# GitHub Actions — run only affected tests
- name: Find affected tests
  id: tests
  run: |
    # Agent runs: test-impact-analyzer affected ${{ github.event.pull_request.base.ref }} --format paths > affected-tests.txt
    echo "count=$(wc -l < affected-tests.txt)" >> $GITHUB_OUTPUT

- name: Run affected tests
  if: steps.tests.outputs.count > 0
  run: npx jest $(cat affected-tests.txt | tr '\n' ' ')

- name: Full test suite
  if: steps.tests.outputs.count == 0
  run: npm test
```

Exit codes:
- 0: All changed code has test coverage
- 1: Some changed code is untested (lists the files)
- 2: No tests found at all

## Notes

- Uses file naming conventions for test matching (file.test.ts, test_file.py, file_test.go)
- Import chain analysis is 1 level deep by default — use `--depth 2` for transitive imports
- Does not parse code ASTs — uses grep/ripgrep patterns for speed
- Works best when test files are co-located or follow naming conventions
- For monorepos: respects workspace boundaries when tracing imports
- Not a replacement for code coverage tools — this is pre-execution analysis, not runtime coverage
