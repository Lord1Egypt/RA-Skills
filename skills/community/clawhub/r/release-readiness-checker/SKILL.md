---
name: release-readiness-checker
description: Pre-release checklist for shipping software — verify tests pass, changelog updated, version bumped, no debug code, dependencies clean, docs current, no secrets committed, CI green. Blocks releases that aren't ready.
---

# Release Readiness Checker

Run a comprehensive pre-release audit before cutting a release. Checks code quality, documentation, dependencies, CI status, and common release blockers. Produces a go/no-go report.

Use when: "are we ready to release", "pre-release check", "release audit", "can we ship this", "release checklist", or before tagging a version.

## Commands

### 1. `check` — Full Release Readiness Audit

Run all checks and produce a go/no-go verdict.

#### Check 1: Version Bumped

```bash
# Check current version
if [ -f "package.json" ]; then
  CURRENT=$(python3 -c "import json; print(json.load(open('package.json')).get('version','none'))" 2>/dev/null)
  echo "Current version: $CURRENT"

  # Compare with latest git tag
  LATEST_TAG=$(git tag --sort=-version:refname 2>/dev/null | head -1)
  echo "Latest tag: ${LATEST_TAG:-none}"

  if [ "$CURRENT" = "${LATEST_TAG#v}" ] || [ "v$CURRENT" = "$LATEST_TAG" ]; then
    echo "⚠️  Version matches latest tag — did you forget to bump?"
  fi
fi

# Check for version in other files
for f in pyproject.toml Cargo.toml setup.py setup.cfg version.txt VERSION; do
  if [ -f "$f" ]; then
    grep -i "version" "$f" | head -3
  fi
done
```

#### Check 2: Changelog Updated

```bash
# Check CHANGELOG exists and has recent entry
for f in CHANGELOG.md CHANGELOG CHANGES.md HISTORY.md; do
  if [ -f "$f" ]; then
    echo "Found: $f"
    # Check if top entry matches current version or is Unreleased
    head -20 "$f"

    # Check if there's content under Unreleased
    UNRELEASED=$(sed -n '/\[Unreleased\]/,/\[/p' "$f" 2>/dev/null | wc -l)
    if [ "$UNRELEASED" -le 2 ]; then
      echo "⚠️  Unreleased section appears empty"
    fi
    break
  fi
done

# If no changelog found
if [ ! -f "CHANGELOG.md" ] && [ ! -f "CHANGELOG" ] && [ ! -f "CHANGES.md" ]; then
  echo "⚠️  No CHANGELOG file found"
fi
```

#### Check 3: No Debug Code

```bash
# Common debug artifacts
echo "=== Debug Code Check ==="
rg -n "console\.log|console\.debug|console\.warn|debugger;" \
  -g '!node_modules' -g '!vendor' -g '!dist' -g '!build' -g '!*.test.*' -g '!*.spec.*' \
  -g '*.{js,ts,jsx,tsx}' --stats 2>&1 | tail -5

rg -n "print\(|breakpoint\(\)|pdb\.set_trace|import pdb|import ipdb" \
  -g '!vendor' -g '!dist' -g '*.py' -g '!*test*' --stats 2>&1 | tail -5

rg -n "fmt\.Print|log\.Print" \
  -g '*.go' -g '!*_test.go' --stats 2>&1 | tail -5

# TODO/FIXME in critical paths (not tests)
CRITICAL_TODOS=$(rg -c "TODO|FIXME|HACK|XXX" \
  -g '!node_modules' -g '!vendor' -g '!dist' -g '!*.test.*' -g '!*.spec.*' \
  --type-not binary 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
echo "TODO/FIXME count (non-test): $CRITICAL_TODOS"
```

#### Check 4: Tests Pass

```bash
echo "=== Test Check ==="
# Detect test runner
if [ -f "package.json" ]; then
  HAS_TEST=$(python3 -c "import json; d=json.load(open('package.json')); print('yes' if d.get('scripts',{}).get('test','') not in ['','echo \"Error: no test specified\" && exit 1'] else 'no')" 2>/dev/null)
  if [ "$HAS_TEST" = "yes" ]; then
    echo "Test command: npm test"
    echo "(Run 'npm test' to verify — not running automatically to avoid side effects)"
  else
    echo "⚠️  No test script configured in package.json"
  fi
fi

if [ -f "pytest.ini" ] || [ -f "setup.cfg" ] || [ -f "pyproject.toml" ]; then
  if python3 -c "import pytest" 2>/dev/null; then
    echo "Test runner: pytest detected"
  fi
fi

# Check if tests exist at all
TEST_COUNT=$(find . -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" -o -name "*_test.*" \) \
  -not -path '*/node_modules/*' -not -path '*/vendor/*' 2>/dev/null | wc -l)
echo "Test files found: $TEST_COUNT"
if [ "$TEST_COUNT" -eq 0 ]; then
  echo "❌ No test files found"
fi
```

#### Check 5: Dependencies Clean

```bash
echo "=== Dependency Check ==="
# Check for outdated (major versions)
if [ -f "package-lock.json" ] || [ -f "yarn.lock" ] || [ -f "pnpm-lock.yaml" ]; then
  npm outdated 2>/dev/null | head -15 || true

  # Check for known vulnerabilities
  npm audit --json 2>/dev/null | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    vulns = d.get('metadata', {}).get('vulnerabilities', {})
    crit = vulns.get('critical', 0)
    high = vulns.get('high', 0)
    if crit > 0: print(f'❌ {crit} critical vulnerabilities')
    elif high > 0: print(f'⚠️  {high} high vulnerabilities')
    else: print('✅ No critical/high vulnerabilities')
except: print('Could not parse npm audit output')
" 2>/dev/null
fi

# Lockfile freshness
if [ -f "package-lock.json" ]; then
  LOCK_AGE=$(git log -1 --format="%ar" -- package-lock.json 2>/dev/null)
  echo "Lock file last updated: ${LOCK_AGE:-unknown}"
fi
```

#### Check 6: No Secrets Committed

```bash
echo "=== Secrets Check ==="
# Common secret patterns
rg -n "(PRIVATE_KEY|SECRET_KEY|API_KEY|ACCESS_TOKEN|password\s*=\s*['\"][^'\"]+['\"])" \
  -g '!node_modules' -g '!vendor' -g '!dist' -g '!*.lock' -g '!*.test.*' \
  --type-not binary -i 2>/dev/null | \
  grep -v "process\.env\|os\.environ\|os\.getenv\|\.env\|example\|sample\|template\|test\|mock\|fake\|dummy" | head -10

# Check .env files are gitignored
if [ -f ".env" ]; then
  if git check-ignore .env >/dev/null 2>&1; then
    echo "✅ .env is gitignored"
  else
    echo "❌ .env is NOT gitignored — potential secret exposure"
  fi
fi

# Check for committed .env files
git ls-files '*.env' '.env*' 2>/dev/null | grep -v '.env.example\|.env.sample\|.env.template' | while read f; do
  echo "⚠️  Committed env file: $f"
done
```

#### Check 7: CI Status

```bash
echo "=== CI Check ==="
# Check GitHub Actions status for current branch
BRANCH=$(git branch --show-current 2>/dev/null)
if command -v gh &>/dev/null; then
  gh run list --branch "$BRANCH" --limit 3 2>/dev/null || echo "Could not fetch CI status (gh not configured)"
else
  echo "gh CLI not available — check CI manually"
fi

# Check if CI config exists
for f in .github/workflows/*.yml .github/workflows/*.yaml .gitlab-ci.yml Jenkinsfile .circleci/config.yml; do
  if ls $f 2>/dev/null | head -1 >/dev/null; then
    echo "CI config found: $f"
  fi
done 2>/dev/null
```

#### Check 8: Documentation Current

```bash
echo "=== Documentation Check ==="
# README exists and is non-trivial
if [ -f "README.md" ]; then
  LINES=$(wc -l < README.md)
  echo "README.md: $LINES lines"
  if [ "$LINES" -lt 10 ]; then
    echo "⚠️  README.md seems sparse"
  fi
else
  echo "⚠️  No README.md found"
fi

# API docs if relevant
for f in docs/ doc/ api-docs/ API.md; do
  if [ -e "$f" ]; then
    echo "Docs found: $f"
  fi
done

# Check if README references current version
if [ -f "README.md" ] && [ -n "$CURRENT" ]; then
  if grep -q "$CURRENT" README.md 2>/dev/null; then
    echo "✅ README references current version ($CURRENT)"
  fi
fi
```

#### Check 9: Git Status Clean

```bash
echo "=== Git Status ==="
UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$UNCOMMITTED" -gt 0 ]; then
  echo "⚠️  $UNCOMMITTED uncommitted changes"
  git status --short 2>/dev/null | head -10
else
  echo "✅ Working tree clean"
fi

# Check if current branch is ahead/behind
BRANCH=$(git branch --show-current 2>/dev/null)
AHEAD=$(git rev-list --count origin/$BRANCH..$BRANCH 2>/dev/null || echo "?")
BEHIND=$(git rev-list --count $BRANCH..origin/$BRANCH 2>/dev/null || echo "?")
echo "Branch: $BRANCH (ahead: $AHEAD, behind: $BEHIND)"
if [ "$BEHIND" != "0" ] && [ "$BEHIND" != "?" ]; then
  echo "⚠️  Branch is behind remote — pull before releasing"
fi
```

### 2. `verdict` — Go/No-Go Summary

After running all checks, produce a verdict:

```markdown
# Release Readiness Report
Project: [name] | Version: [version] | Date: [date]

## Verdict: 🟢 GO / 🟡 CAUTION / 🔴 NO-GO

### Blockers (must fix before release)
- ❌ 3 critical vulnerabilities in dependencies
- ❌ .env file committed to repository

### Warnings (should fix, won't block)
- ⚠️  Version not bumped from last tag
- ⚠️  12 TODO/FIXME comments in source
- ⚠️  5 uncommitted changes

### Passing
- ✅ Changelog updated
- ✅ Tests exist (47 test files)
- ✅ No debug code detected
- ✅ README current (89 lines)
- ✅ CI config present
```

Verdict rules:
- **NO-GO**: Any critical vulnerability, committed secrets, or no tests
- **CAUTION**: Uncommitted changes, outdated deps (major), sparse docs, debug code found
- **GO**: All checks pass or only minor warnings

### 3. `checklist` — Interactive Checklist

Generate a markdown checklist for manual review:

```markdown
## Pre-Release Checklist

### Automated (run `check` to verify)
- [ ] Version bumped
- [ ] Changelog updated
- [ ] No debug code (console.log, debugger, etc.)
- [ ] Tests pass
- [ ] Dependencies clean (no critical vulns)
- [ ] No secrets committed
- [ ] CI green
- [ ] Docs updated
- [ ] Git status clean

### Manual Review
- [ ] Breaking changes documented
- [ ] Migration guide written (if needed)
- [ ] API deprecation notices sent
- [ ] Performance regression check
- [ ] Security review completed
- [ ] Stakeholders notified
- [ ] Release notes drafted
- [ ] Rollback plan documented
```

### 4. `compare` — Compare with Previous Release

Show what changed since the last tagged release:

```bash
LATEST_TAG=$(git tag --sort=-version:refname 2>/dev/null | head -1)
if [ -n "$LATEST_TAG" ]; then
  echo "Changes since $LATEST_TAG:"
  echo ""
  echo "=== Commits ==="
  git log "$LATEST_TAG"..HEAD --oneline 2>/dev/null | head -30

  echo ""
  echo "=== File Stats ==="
  git diff --stat "$LATEST_TAG"..HEAD 2>/dev/null | tail -5

  echo ""
  echo "=== New Files ==="
  git diff --name-only --diff-filter=A "$LATEST_TAG"..HEAD 2>/dev/null | head -20

  echo ""
  echo "=== Deleted Files ==="
  git diff --name-only --diff-filter=D "$LATEST_TAG"..HEAD 2>/dev/null | head -20

  echo ""
  echo "=== Contributors ==="
  git log "$LATEST_TAG"..HEAD --format="%an" 2>/dev/null | sort -u
fi
```

## Output Formats

- **text** (default): Human-readable with status icons
- **json**: Machine-readable `{version, verdict, blockers: [], warnings: [], passing: [], checks: {name: {status, details}}}`
- **markdown**: PR/wiki-ready report with tables and checklist

## CI Integration

Exit codes:
- 0: GO (all checks pass)
- 1: NO-GO (blockers found)
- 2: CAUTION (warnings only)

```yaml
# Block release on failure
- name: Release readiness check
  run: |
    # Agent runs: release-readiness-checker check
    # Exits 1 if blockers found

# As PR comment
- name: Post readiness report
  run: |
    # Agent runs: release-readiness-checker verdict --format markdown > report.md
    gh pr comment $PR_NUMBER --body-file report.md
```

## Notes

- Does not run tests automatically (to avoid side effects) — reports whether test infrastructure exists and suggests running them
- Secrets detection uses pattern matching — may have false positives (review flagged items)
- Git history required for version comparison and branch status
- CI status check requires `gh` CLI with authentication
- Adapts to project type: detects Node.js, Python, Go, Rust from config files
- Customizable: add `.release-readiness.json` to adjust thresholds (max TODOs, required docs, etc.)
