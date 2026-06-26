---
name: repository-health-score
description: Score a repository's health across 8 dimensions — code quality, testing, documentation, CI/CD, security, dependencies, community, and maintainability. Produces a letter grade (A-F) with specific improvement suggestions.
---

# Repository Health Score

Rate any repository on a 0-100 scale across 8 dimensions. Like a credit score for code — quick assessment of project maturity, maintenance quality, and risk level.

Use when: "how healthy is this repo", "rate this codebase", "project quality audit", "is this repo well-maintained", "should we adopt this library", "repository assessment", or during due diligence on open-source dependencies.

## Commands

### 1. `score` — Full Health Assessment

Run all dimension checks and produce a composite score.

#### Dimension 1: Documentation (15 points)

```bash
echo "=== Documentation ==="
SCORE=0

# README quality
if [ -f "README.md" ]; then
  LINES=$(wc -l < README.md)
  if [ "$LINES" -gt 50 ]; then SCORE=$((SCORE + 3))
  elif [ "$LINES" -gt 20 ]; then SCORE=$((SCORE + 2))
  elif [ "$LINES" -gt 5 ]; then SCORE=$((SCORE + 1)); fi

  # Check for key sections
  grep -qi "install" README.md && SCORE=$((SCORE + 1))
  grep -qi "usage\|getting started\|quick start" README.md && SCORE=$((SCORE + 1))
  grep -qi "api\|reference\|documentation" README.md && SCORE=$((SCORE + 1))
  grep -qi "contribut" README.md && SCORE=$((SCORE + 1))
  grep -qi "license" README.md && SCORE=$((SCORE + 1))
else
  echo "❌ No README.md"
fi

# Additional docs
[ -f "CONTRIBUTING.md" ] && SCORE=$((SCORE + 2))
[ -f "CHANGELOG.md" ] || [ -f "CHANGES.md" ] && SCORE=$((SCORE + 2))
[ -d "docs" ] || [ -d "doc" ] && SCORE=$((SCORE + 2))
[ -f "LICENSE" ] || [ -f "LICENSE.md" ] && SCORE=$((SCORE + 1))

echo "Documentation score: $SCORE/15"
```

#### Dimension 2: Testing (15 points)

```bash
echo "=== Testing ==="
SCORE=0

# Test files exist
TEST_COUNT=$(find . -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" -o -name "*_test.*" \) \
  -not -path '*/node_modules/*' -not -path '*/vendor/*' 2>/dev/null | wc -l)
SRC_COUNT=$(find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" \) \
  -not -path '*/node_modules/*' -not -path '*/vendor/*' -not -path '*/dist/*' \
  -not -name '*.test.*' -not -name '*.spec.*' 2>/dev/null | wc -l)

if [ "$TEST_COUNT" -gt 0 ]; then
  RATIO=$(echo "scale=0; $TEST_COUNT * 100 / ($SRC_COUNT + 1)" | bc)
  if [ "$RATIO" -gt 80 ]; then SCORE=$((SCORE + 5))
  elif [ "$RATIO" -gt 50 ]; then SCORE=$((SCORE + 4))
  elif [ "$RATIO" -gt 30 ]; then SCORE=$((SCORE + 3))
  elif [ "$RATIO" -gt 10 ]; then SCORE=$((SCORE + 2))
  else SCORE=$((SCORE + 1)); fi
  echo "Test ratio: ${RATIO}% ($TEST_COUNT tests / $SRC_COUNT sources)"
fi

# Test runner configured
if [ -f "package.json" ]; then
  HAS_TEST=$(python3 -c "import json; d=json.load(open('package.json')); s=d.get('scripts',{}).get('test',''); print('yes' if s and 'no test' not in s else 'no')" 2>/dev/null)
  [ "$HAS_TEST" = "yes" ] && SCORE=$((SCORE + 2))
fi
[ -f "pytest.ini" ] || [ -f "conftest.py" ] && SCORE=$((SCORE + 2))
[ -f "jest.config.js" ] || [ -f "jest.config.ts" ] || [ -f "vitest.config.ts" ] && SCORE=$((SCORE + 2))

# Coverage config
rg -l "coverage|istanbul|c8|nyc" package.json .nycrc jest.config.* vitest.config.* pyproject.toml 2>/dev/null | head -1 && SCORE=$((SCORE + 3))

# E2E tests
find . -path "*/e2e/*" -o -path "*/cypress/*" -o -path "*/playwright/*" 2>/dev/null | head -1 && SCORE=$((SCORE + 3))

echo "Testing score: $SCORE/15"
```

#### Dimension 3: CI/CD (12 points)

```bash
echo "=== CI/CD ==="
SCORE=0

# CI config exists
[ -d ".github/workflows" ] && SCORE=$((SCORE + 3))
[ -f ".gitlab-ci.yml" ] && SCORE=$((SCORE + 3))
[ -f ".circleci/config.yml" ] && SCORE=$((SCORE + 3))
[ -f "Jenkinsfile" ] && SCORE=$((SCORE + 3))

# Multiple workflows (build + test + deploy)
if [ -d ".github/workflows" ]; then
  WF_COUNT=$(ls .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null | wc -l)
  [ "$WF_COUNT" -ge 3 ] && SCORE=$((SCORE + 3))
  [ "$WF_COUNT" -ge 2 ] && SCORE=$((SCORE + 2)) || true

  # Quality gates
  rg -l "lint\|format\|type-check\|typecheck" .github/workflows/ 2>/dev/null | head -1 && SCORE=$((SCORE + 2))
  rg -l "deploy\|release\|publish" .github/workflows/ 2>/dev/null | head -1 && SCORE=$((SCORE + 2))
fi

# Branch protection indicators
[ -f ".github/branch-protection.yml" ] || [ -f "CODEOWNERS" ] || [ -f ".github/CODEOWNERS" ] && SCORE=$((SCORE + 2))

echo "CI/CD score: $SCORE/12"
```

#### Dimension 4: Security (12 points)

```bash
echo "=== Security ==="
SCORE=0

# .gitignore quality
if [ -f ".gitignore" ]; then
  SCORE=$((SCORE + 1))
  grep -q "\.env" .gitignore && SCORE=$((SCORE + 1))
  grep -q "node_modules\|vendor\|__pycache__" .gitignore && SCORE=$((SCORE + 1))
fi

# No secrets in repo
SECRET_HITS=$(rg -c "(PRIVATE_KEY|SECRET_KEY|sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|password\s*=\s*['\"][^'\"]{8,})" \
  -g '!node_modules' -g '!vendor' -g '!*.lock' -g '!*.test.*' -g '!*.example*' \
  --type-not binary 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
if [ "$SECRET_HITS" -eq 0 ]; then SCORE=$((SCORE + 3))
elif [ "$SECRET_HITS" -lt 3 ]; then SCORE=$((SCORE + 1)); fi

# Security policy
[ -f "SECURITY.md" ] || [ -f ".github/SECURITY.md" ] && SCORE=$((SCORE + 2))

# Dependency scanning
rg -l "dependabot\|renovate\|snyk\|socket" .github/ 2>/dev/null | head -1 && SCORE=$((SCORE + 2))

# Lock file committed
([ -f "package-lock.json" ] || [ -f "yarn.lock" ] || [ -f "pnpm-lock.yaml" ] || [ -f "Cargo.lock" ] || [ -f "go.sum" ]) && SCORE=$((SCORE + 2))

echo "Security score: $SCORE/12"
```

#### Dimension 5: Code Quality (12 points)

```bash
echo "=== Code Quality ==="
SCORE=0

# Linting configured
([ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ] || [ -f "eslint.config.js" ] || [ -f "biome.json" ] || [ -f ".flake8" ] || [ -f "ruff.toml" ] || [ -f ".golangci.yml" ]) && SCORE=$((SCORE + 3))

# Formatting configured
([ -f ".prettierrc" ] || [ -f ".prettierrc.json" ] || [ -f "biome.json" ] || [ -f ".editorconfig" ]) && SCORE=$((SCORE + 2))

# Type checking (TypeScript, mypy, etc.)
([ -f "tsconfig.json" ] || rg -l "mypy\|pyright" pyproject.toml setup.cfg 2>/dev/null | head -1) && SCORE=$((SCORE + 3))

# Low TODO/FIXME density
TODO_COUNT=$(rg -c "TODO|FIXME|HACK|XXX" -g '!node_modules' -g '!vendor' --type-not binary 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
if [ "$TODO_COUNT" -lt 5 ]; then SCORE=$((SCORE + 2))
elif [ "$TODO_COUNT" -lt 20 ]; then SCORE=$((SCORE + 1)); fi

# Pre-commit hooks
([ -f ".husky/pre-commit" ] || [ -f ".pre-commit-config.yaml" ] || [ -d ".lefthook" ]) && SCORE=$((SCORE + 2))

echo "Code quality score: $SCORE/12"
```

#### Dimension 6: Dependencies (10 points)

```bash
echo "=== Dependencies ==="
SCORE=0

# Dependency count is reasonable
if [ -f "package.json" ]; then
  DEP_COUNT=$(python3 -c "import json; d=json.load(open('package.json')); print(len(d.get('dependencies',{})))" 2>/dev/null)
  if [ "$DEP_COUNT" -lt 20 ]; then SCORE=$((SCORE + 3))
  elif [ "$DEP_COUNT" -lt 50 ]; then SCORE=$((SCORE + 2))
  elif [ "$DEP_COUNT" -lt 100 ]; then SCORE=$((SCORE + 1)); fi
fi

# No deprecated dependencies
DEPRECATED=$(python3 -c "
import json
d = json.load(open('package.json'))
deps = {**d.get('dependencies',{}), **d.get('devDependencies',{})}
deprecated = ['request','node-uuid','nomnom','optimist','jade','istanbul','coffee-script','bower','grunt','moment']
found = [p for p in deprecated if p in deps]
print(len(found))
" 2>/dev/null || echo "0")
[ "$DEPRECATED" -eq 0 ] && SCORE=$((SCORE + 3))

# Engine constraints specified
python3 -c "import json; d=json.load(open('package.json')); print('yes' if 'engines' in d else 'no')" 2>/dev/null | grep -q "yes" && SCORE=$((SCORE + 2))

# Peer dependency aware
python3 -c "import json; d=json.load(open('package.json')); print('yes' if 'peerDependencies' in d else 'na')" 2>/dev/null | grep -q "yes" && SCORE=$((SCORE + 2))

echo "Dependencies score: $SCORE/10"
```

#### Dimension 7: Maintainability (12 points)

```bash
echo "=== Maintainability ==="
SCORE=0

# Consistent project structure
([ -d "src" ] || [ -d "lib" ] || [ -d "pkg" ] || [ -d "internal" ]) && SCORE=$((SCORE + 2))

# No god files (>1000 lines)
GOD_FILES=$(find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" \) \
  -not -path '*/node_modules/*' -not -path '*/vendor/*' -not -path '*/dist/*' 2>/dev/null | \
  xargs wc -l 2>/dev/null | awk '$1 > 1000 {count++} END {print count+0}')
if [ "$GOD_FILES" -eq 0 ]; then SCORE=$((SCORE + 3))
elif [ "$GOD_FILES" -lt 3 ]; then SCORE=$((SCORE + 2))
elif [ "$GOD_FILES" -lt 5 ]; then SCORE=$((SCORE + 1)); fi

# Recent activity (commits in last 90 days)
RECENT=$(git log --since="90 days ago" --oneline 2>/dev/null | wc -l)
if [ "$RECENT" -gt 20 ]; then SCORE=$((SCORE + 3))
elif [ "$RECENT" -gt 5 ]; then SCORE=$((SCORE + 2))
elif [ "$RECENT" -gt 0 ]; then SCORE=$((SCORE + 1)); fi

# Issue/PR templates
([ -f ".github/ISSUE_TEMPLATE/bug_report.md" ] || [ -d ".github/ISSUE_TEMPLATE" ] || [ -f ".github/pull_request_template.md" ]) && SCORE=$((SCORE + 2))

# Multiple contributors
CONTRIBUTORS=$(git log --format="%an" 2>/dev/null | sort -u | wc -l)
[ "$CONTRIBUTORS" -gt 3 ] && SCORE=$((SCORE + 2))

echo "Maintainability score: $SCORE/12"
```

#### Dimension 8: Community (12 points)

```bash
echo "=== Community ==="
SCORE=0

# Contributing guide
[ -f "CONTRIBUTING.md" ] && SCORE=$((SCORE + 3))

# Code of conduct
[ -f "CODE_OF_CONDUCT.md" ] && SCORE=$((SCORE + 2))

# Issue templates
[ -d ".github/ISSUE_TEMPLATE" ] && SCORE=$((SCORE + 2))

# PR template
[ -f ".github/pull_request_template.md" ] && SCORE=$((SCORE + 2))

# GitHub features
if command -v gh &>/dev/null; then
  STARS=$(gh repo view --json stargazerCount -q '.stargazerCount' 2>/dev/null || echo "0")
  FORKS=$(gh repo view --json forkCount -q '.forkCount' 2>/dev/null || echo "0")
  [ "$STARS" -gt 100 ] && SCORE=$((SCORE + 1))
  [ "$FORKS" -gt 10 ] && SCORE=$((SCORE + 1))
fi

# Badges in README (community engagement indicator)
if [ -f "README.md" ]; then
  BADGES=$(grep -c "!\[" README.md 2>/dev/null || echo "0")
  [ "$BADGES" -gt 3 ] && SCORE=$((SCORE + 1))
fi

echo "Community score: $SCORE/12"
```

### Composite Score

Sum all dimensions (max 100) and assign a letter grade:

| Score | Grade | Assessment |
|-------|-------|-----------|
| 90-100 | A | Excellent — production-ready, well-maintained |
| 80-89 | B | Good — solid project with minor gaps |
| 70-79 | C | Fair — functional but needs attention |
| 60-69 | D | Below average — significant gaps |
| <60 | F | Poor — high risk, needs major investment |

### 2. `compare` — Compare Two Repositories

Run `score` on two repos and produce a side-by-side comparison. Useful for choosing between competing libraries.

### 3. `improve` — Top 5 Improvements

Based on the score breakdown, suggest the 5 highest-impact improvements with AI reasoning:

```markdown
## Top 5 Improvements (by score impact)

1. **Add tests** (+8 points) — No test files found. Start with unit tests for core modules.
   Effort: M | Impact: Testing 0→8/15

2. **Configure CI** (+6 points) — No CI pipeline. Add GitHub Actions with lint+test+build.
   Effort: S | Impact: CI/CD 0→6/12

3. **Add CHANGELOG.md** (+2 points) — No changelog. Start with Keep a Changelog format.
   Effort: XS | Impact: Documentation 11→13/15

4. **Set up Dependabot** (+2 points) — No dependency automation.
   Effort: XS | Impact: Security 8→10/12

5. **Add CONTRIBUTING.md** (+3 points) — No contributor guide.
   Effort: S | Impact: Community 4→7/12
```

## Output Formats

- **text** (default): Human-readable scorecard with bar chart
- **json**: `{total, grade, dimensions: {name: {score, max, details: []}}, improvements: []}`
- **markdown**: Report card format with tables and grade badges
- **badge**: Shield.io badge URL for README: `![Health Score](https://img.shields.io/badge/health-B%2083%25-green)`

## Notes

- Works on any git repository — adapts to language/framework automatically
- Does not execute code or install dependencies — purely static analysis
- Community dimension requires `gh` CLI for GitHub metrics (optional)
- Scores are relative — a CLI tool and a web app have different baselines
- Run periodically to track improvement trends
