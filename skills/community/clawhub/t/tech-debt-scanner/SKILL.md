---
name: tech-debt-scanner
description: Scan codebases for technical debt — TODO/FIXME comments, deprecated APIs, complexity hotspots, outdated patterns, missing tests, large files — then prioritize with AI reasoning and generate remediation plans.
---

# Tech Debt Scanner

Find, categorize, and prioritize technical debt in any codebase. Produces an actionable report with effort estimates, risk scores, and remediation suggestions — not just a list of problems.

Use when: "scan for tech debt", "find code smells", "audit code quality", "what should we refactor first", "technical debt report", or before sprint planning to identify cleanup candidates.

## Commands

### 1. `scan` — Full Tech Debt Audit

Run all detectors and produce a prioritized report.

#### Step 1: Detect TODO/FIXME/HACK Comments

```bash
# Find all debt markers with context
rg -n "TODO|FIXME|HACK|XXX|TEMP|WORKAROUND|DEPRECATED|NOCOMMIT" \
  --type-not binary \
  -g '!node_modules' -g '!vendor' -g '!dist' -g '!build' -g '!.git' \
  --stats 2>&1
```

Categorize each hit:
- **TODO**: Feature incomplete — low risk, track in backlog
- **FIXME**: Known bug — medium risk, prioritize
- **HACK/WORKAROUND**: Fragile code — high risk, refactor soon
- **DEPRECATED**: API sunset — high risk if external dependency
- **NOCOMMIT**: Should never have been merged — critical

Count totals per category. Flag any older than 6 months (check git blame):

```bash
# Age of oldest TODO/FIXME (sample first 10)
rg -l "TODO|FIXME|HACK" -g '!node_modules' -g '!vendor' | head -10 | while read f; do
  echo "=== $f ==="
  git log -1 --format="%ai %an" -- "$f" 2>/dev/null
done
```

#### Step 2: Detect Complexity Hotspots

```bash
# Largest source files (often the most complex)
find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" \) \
  -not -path '*/node_modules/*' -not -path '*/vendor/*' -not -path '*/dist/*' -not -path '*/.git/*' \
  -exec wc -l {} + 2>/dev/null | sort -rn | head -20

# Functions with high nesting (proxy for cyclomatic complexity)
rg -n "^\s{12,}(if|for|while|switch|case|catch)" \
  --type-not binary \
  -g '!node_modules' -g '!vendor' -g '!dist' \
  --stats 2>&1 | tail -5
```

Flag files >500 lines as candidates for splitting.
Flag functions with >4 levels of nesting as complexity hotspots.

#### Step 3: Detect Outdated Patterns

```bash
# JavaScript/TypeScript: var usage (should be let/const)
rg -c "^\s*var\s+" -g '*.{js,ts,jsx,tsx}' -g '!node_modules' 2>/dev/null | sort -t: -k2 -rn | head -10

# JavaScript: callback hell (nested callbacks)
rg -c "function\s*\(" -g '*.{js,ts}' -g '!node_modules' 2>/dev/null | sort -t: -k2 -rn | head -10

# Python: old-style string formatting
rg -c '% ["\x27(]' -g '*.py' -g '!vendor' 2>/dev/null | sort -t: -k2 -rn | head -10

# Python: bare except
rg -n "except:" -g '*.py' -g '!vendor' 2>/dev/null

# Deprecated React patterns
rg -n "componentWillMount|componentWillReceiveProps|componentWillUpdate|React\.createClass|mixins\s*:" \
  -g '*.{jsx,tsx,js,ts}' -g '!node_modules' 2>/dev/null
```

#### Step 4: Detect Missing or Weak Tests

```bash
# Test file ratio
SRC_COUNT=$(find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" \) \
  -not -path '*/node_modules/*' -not -path '*/vendor/*' -not -path '*/test*' -not -path '*/__test*' \
  -not -path '*/*.test.*' -not -path '*/*.spec.*' -not -path '*/dist/*' | wc -l)
TEST_COUNT=$(find . -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" -o -name "*_test.*" \) \
  -not -path '*/node_modules/*' | wc -l)
echo "Source files: $SRC_COUNT, Test files: $TEST_COUNT, Ratio: $(echo "scale=1; $TEST_COUNT * 100 / ($SRC_COUNT + 1)" | bc)%"

# Source files with no corresponding test
find . -type f -name "*.ts" -not -name "*.test.*" -not -name "*.spec.*" \
  -not -path '*/node_modules/*' -not -path '*/dist/*' | while read f; do
  BASE=$(basename "$f" .ts)
  if ! find . -type f \( -name "${BASE}.test.ts" -o -name "${BASE}.spec.ts" -o -name "test_${BASE}*" \) \
    -not -path '*/node_modules/*' 2>/dev/null | grep -q .; then
    echo "NO TEST: $f"
  fi
done | head -20
```

#### Step 5: Detect Dependency Issues

```bash
# Node.js: outdated dependencies
npm outdated 2>/dev/null || true
# Check for deprecated packages in package.json
cat package.json 2>/dev/null | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    deps = {**d.get('dependencies',{}), **d.get('devDependencies',{})}
    deprecated = ['request', 'node-uuid', 'nomnom', 'optimist', 'jade', 'istanbul', 'coffee-script', 'bower', 'grunt']
    for pkg in deprecated:
        if pkg in deps:
            print(f'DEPRECATED: {pkg}@{deps[pkg]}')
except: pass
"

# Python: check requirements age
cat requirements.txt 2>/dev/null | head -30
pip list --outdated 2>/dev/null | head -20

# Go: check go.sum for old versions
cat go.sum 2>/dev/null | wc -l
```

#### Step 6: Detect Code Duplication Indicators

```bash
# Find suspiciously similar file names (copy-paste indicators)
find . -type f -name "*.ts" -not -path '*/node_modules/*' -not -path '*/dist/*' | \
  xargs -I{} basename {} | sort | uniq -d

# Find repeated import patterns (same large import block = shared code candidate)
rg -c "^import" -g '*.{ts,js,tsx,jsx}' -g '!node_modules' 2>/dev/null | \
  sort -t: -k2 -rn | head -10

# Find files with very similar line counts (heuristic for copies)
find . -type f \( -name "*.ts" -o -name "*.js" \) \
  -not -path '*/node_modules/*' -not -path '*/dist/*' \
  -exec wc -l {} + 2>/dev/null | sort -n | awk '{print $1}' | uniq -d | head -5
```

#### Step 7: Generate Report

Analyze all findings with AI reasoning. For each debt item, assess:
- **Risk**: How likely is this to cause bugs, outages, or slow development?
- **Effort**: T-shirt size (XS/S/M/L/XL) to fix
- **Impact**: What improves when fixed? (velocity, reliability, onboarding, security)

Produce a prioritized report:

```markdown
# Tech Debt Report — [project name]
Generated: [date]

## Summary
- Total debt items: N
- Critical (fix now): N
- High (next sprint): N
- Medium (backlog): N
- Low (opportunistic): N

## Critical Items
1. [item] — Risk: critical | Effort: S | Impact: ...
   **Why:** [AI reasoning about the risk]
   **Fix:** [specific remediation steps]

## High Priority Items
...

## Metrics
- TODO/FIXME count: N (N are >6 months old)
- Test coverage ratio: N%
- Files >500 lines: N
- Deprecated dependencies: N
- Code duplication indicators: N hotspots
```

### 2. `hotspots` — Complexity Hotspot Map

Run Steps 2 and 6 only. Output the top 10 files that are:
- Largest by line count
- Most frequently changed (git churn)
- Most complex (deep nesting)

```bash
# Git churn — most frequently modified files in last 90 days
git log --since="90 days ago" --name-only --pretty=format: 2>/dev/null | \
  grep -v '^$' | sort | uniq -c | sort -rn | head -20
```

Cross-reference size × churn × nesting to find the "burning" hotspots — large, complex files that change often are the highest-ROI refactoring targets.

### 3. `todos` — TODO/FIXME Audit

Run Step 1 only. Group by file, show git blame age for each, flag ancient ones.

Output format:
```
[CRITICAL] path/to/file.ts:42 — HACK: workaround for API bug (author, 2024-03-15)
[MEDIUM]   path/to/file.ts:87 — TODO: add validation (author, 2025-11-02)
[LOW]      path/to/other.py:12 — TODO: optimize later (author, 2026-04-01)
```

### 4. `deps` — Dependency Health

Run Step 5 only. Show:
- Outdated packages with how far behind they are (major/minor/patch)
- Known deprecated packages
- Packages with known vulnerabilities (npm audit / pip-audit if available)

### 5. `tests` — Test Coverage Gaps

Run Step 4 only. List source files without corresponding tests, sorted by:
1. Size (larger untested files = higher risk)
2. Git churn (frequently changed untested files = highest risk)

## Output Formats

- **text** (default): Human-readable report with sections and bullet points
- **json**: Machine-readable for CI/CD integration, structured as `{summary, items: [{category, severity, file, line, message, effort, fix}]}`
- **markdown**: Formatted report suitable for PR comments or wiki pages

## CI Integration

Exit codes:
- 0: No critical or high debt items
- 1: Critical items found (fail the build)
- 2: High items exceed threshold

Use with `--max-critical 0 --max-high 10` to set thresholds.

## Notes

- Adapts detectors to the project's language (auto-detected from file extensions and config files)
- Git history required for churn and age analysis — works without git but reports are less useful
- Does not execute code or install dependencies — static analysis only
- Large monorepos: pass a subdirectory to scope the scan
