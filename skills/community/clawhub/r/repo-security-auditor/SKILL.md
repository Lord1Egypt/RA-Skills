---
name: repo-security-auditor
description: |
  Audit GitHub repositories for security vulnerabilities, malicious code patterns,
  and suspicious behavior. Clone repos, analyze code for backdoors, data exfiltration,
  obfuscation, dependency risks, and license compliance. Generate a security report
  and optionally scaffold a clean reimplementation if the repo passes safety checks.
  Use when: user wants to "review a GitHub repo for security", "check if code is safe",
  "audit repository for malicious code", "analyze repo before using", "scan dependencies",
  "recreate this repo safely", or any request involving security analysis of third-party code.
  Do NOT use for: repos you own and trust, general code review without security focus,
  or when user only wants a feature summary without security checks.
---

# Repo Security Auditor

## Overview

This skill performs comprehensive security audits on GitHub repositories before you adopt,
modify, or reimplement them. It clones the repo, analyzes code for malicious patterns,
checks dependencies for vulnerabilities, verifies license compatibility, and produces
a detailed security report with a PASS/FAIL verdict.

If the repo passes safety checks, the skill can scaffold a clean reimplementation
with the same features but without any inherited risks.

## When to Use

- **Before adopting third-party code**: "Is this library safe to use?"
- **Before forking**: "Audit this repo before I fork it"
- **Dependency risk assessment**: "Check if these dependencies are malicious"
- **Reimplementation planning**: "Recreate this safely as our own"
- **Supply chain security**: "Scan this repo for backdoors or exfiltration"

## Quick Reference

| Situation | Action |
|-----------|--------|
| User provides GitHub URL | Clone → security scan → report → if safe, scaffold clean reimplementation |
| Repo has suspicious patterns | Document findings, recommend against use, suggest alternatives |
| Dependencies have CVEs | Report severity, suggest updates or replacements |
| License is incompatible | Note restrictions, check against intended use |
| Repo passes all checks | Scaffold clean reimplementation with feature extraction |
| Large repo (100k+ lines) | Sample key files, prioritize entry points and network code |

## Step 1: Clone and Inventory

Clone the repository and create a file inventory:

```bash
# Clone to temp directory
REPO_URL="https://github.com/owner/repo"
REPO_NAME=$(basename "$REPO_URL" .git)
WORKDIR="/tmp/repo-audit-$REPO_NAME-$(date +%s)"
git clone --depth 1 "$REPO_URL" "$WORKDIR"
cd "$WORKDIR"

# Create inventory
echo "=== File Inventory ===" > inventory.txt
find . -type f -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" -o -name "*.c" -o -name "*.cpp" | head -100 >> inventory.txt
echo "=== Dependencies ===" >> inventory.txt
cat package.json 2>/dev/null || cat requirements.txt 2>/dev/null || cat Cargo.toml 2>/dev/null || cat go.mod 2>/dev/null >> inventory.txt
```

## Step 2: Security Analysis Pipeline

Run these checks in parallel where possible:

### 2.1 Static Code Analysis (Nefarious Patterns)

Search for suspicious patterns:

```bash
# Network exfiltration patterns
grep -rE "(fetch|axios|request|http|socket).*\.(post|send|write)" --include="*.js" --include="*.ts" . | head -20 > suspicious-network.txt

# Dynamic code execution
grep -rE "(eval|Function|setTimeout|setInterval).*\(" --include="*.js" --include="*.ts" . | head -20 > suspicious-dynamic.txt

# Obfuscation patterns
grep -rE "(\\x[0-9a-f]{2}|\\u[0-9a-f]{4}|String\.fromCharCode|atob|btoa)" --include="*.js" --include="*.ts" . | head -20 > suspicious-obfuscation.txt

# Environment variable access
grep -rE "process\.env|env\[" --include="*.js" --include="*.ts" --include="*.py" . | head -20 > env-access.txt

# Shell execution
grep -rE "(exec|spawn|execSync|child_process)" --include="*.js" --include="*.ts" . | head -20 > shell-execution.txt

# Cryptocurrency/mining patterns
grep -riE "(bitcoin|ethereum|monero|mining|crypto|wallet|blockchain)" --include="*.js" --include="*.ts" --include="*.py" . | head -10 > crypto-patterns.txt
```

### 2.2 Dependency Vulnerability Scan

```bash
# JavaScript/TypeScript
npm audit --json 2>/dev/null > npm-audit.json || echo "No npm audit available"

# Python
pip install safety 2>/dev/null && safety check -r requirements.txt --json 2>/dev/null > safety-report.json || echo "No safety check available"

# Use GitHub Advisory Database via CLI if available
gh api repos/:owner/:repo/dependency-graph/sbom 2>/dev/null > sbom.json || echo "No SBOM available"
```

### 2.3 License Compliance Check

```bash
# Check license file
LICENSE_FILE=$(find . -maxdepth 2 -iname "license*" -o -iname "copying*" | head -1)
if [ -n "$LICENSE_FILE" ]; then
    cat "$LICENSE_FILE" > license-content.txt
fi

# Package.json license field
grep -A2 '"license"' package.json 2>/dev/null > license-package.txt
```

### 2.4 Supply Chain Risk Assessment

```bash
# Check for unpublished or scoped packages with low downloads
echo "Checking package registry visibility..."
npm ls --depth=0 --json 2>/dev/null | jq -r '.dependencies | keys[]' 2>/dev/null | head -20 > package-list.txt
```

## Step 3: Risk Assessment & Scoring

Score each category 0-10 (10 = highest risk):

| Category | Weight | Findings | Score |
|----------|--------|----------|-------|
| Network exfiltration | 25% | Suspicious outbound calls | 0-10 |
| Dynamic code execution | 20% | eval(), new Function(), etc. | 0-10 |
| Obfuscation | 15% | Encoded strings, packed code | 0-10 |
| Dependency vulnerabilities | 20% | Known CVEs in deps | 0-10 |
| License risk | 10% | GPL, proprietary conflicts | 0-10 |
| Supply chain | 10% | Unpublished packages, typosquats | 0-10 |

**Verdict thresholds:**
- **0-3**: Safe to use — proceed with clean reimplementation
- **4-6**: Caution — review flagged items, may proceed with modifications
- **7-10**: High risk — do not use, recommend alternatives

## Step 4: Security Report Generation

Generate a comprehensive markdown report:

```markdown
# Security Audit Report: [REPO_NAME]
**URL:** [GITHUB_URL]
**Audit Date:** [DATE]
**Auditor:** Repo Security Auditor Skill

## Executive Summary
**Overall Risk Score:** [X.X]/10 ([SAFE|CAUTION|HIGH RISK])
**Recommendation:** [PROCEED WITH CAUTION|DO NOT USE|SAFE TO REIMPLEMENT]

## Risk Breakdown

### 🔴 Network Exfiltration Risk: [SCORE]/10
**Findings:**
- [List suspicious network calls]
- [Document data transmission patterns]

**Assessment:** [Explanation]

### 🔴 Dynamic Code Execution Risk: [SCORE]/10
**Findings:**
- [List eval/new Function usage]
- [Document dynamic import patterns]

**Assessment:** [Explanation]

### 🟡 Obfuscation Risk: [SCORE]/10
**Findings:**
- [List encoded strings, packed code]
- [Document minification patterns]

**Assessment:** [Explanation]

### 🔴 Dependency Vulnerabilities: [SCORE]/10
**Findings:**
- [CVE-XXXX-XXXX: Description]
- [Severity levels]

**Assessment:** [Explanation]

### 🟡 License Risk: [SCORE]/10
**License:** [LICENSE_TYPE]
**Compatibility:** [COMPATIBLE|INCOMPATIBLE]
**Restrictions:** [Any commercial/use restrictions]

### 🟡 Supply Chain Risk: [SCORE]/10
**Findings:**
- [Unpublished packages]
- [Low-download dependencies]
- [Typosquatting candidates]

## Detailed Findings

### High Priority Issues
1. **[Issue title]**
   - Location: `file:line`
   - Evidence: [code snippet]
   - Risk: [Description]
   - Mitigation: [How to address]

### Medium Priority Issues
...

### Low Priority Issues
...

## Clean Reimplementation Assessment

**Eligible:** [YES|NO - explain why]

If YES, include:
- Core features to preserve
- Architecture to replicate
- Security improvements to make
- Dependencies to update/replace
```

## Step 5: Clean Reimplementation (If Safe)

If overall score ≤ 3.0, scaffold a clean reimplementation:

### 5.1 Feature Extraction

Analyze the repo and extract:
- **Core functionality**: What does this code do?
- **Public API**: Classes, functions, exports
- **Data models**: Types, schemas, interfaces
- **Key algorithms**: Unique logic worth preserving

### 5.2 Scaffold Generation

Create a new clean project structure:

```
clean-reimplementation/
├── README.md                 # Feature documentation
├── LICENSE                   # Your preferred license
├── package.json              # Clean dependency manifest
├── src/
│   ├── index.ts             # Clean entry point
│   ├── [feature-modules]/   # Modular architecture
│   └── utils/               # Clean utilities
├── tests/
│   └── [test-files].test.ts # Comprehensive tests
└── docs/
    └── ARCHITECTURE.md       # Design decisions
```

### 5.3 Security Improvements to Make

When reimplementing, always:
- Use latest dependency versions
- Remove any dynamic code execution
- Add input validation at all boundaries
- Use dependency scanning in CI/CD
- Add security headers/cors config
- Implement proper error handling (no info leakage)
- Use least-privilege permissions

## Anti-Patterns to Avoid

**Don't just grep and report** — analyze context. `eval()` in a test file for a parser is different from `eval()` in production handling user input.

**Don't flag minified code as malicious** — Check if it's a legitimate build artifact vs. intentionally obfuscated source.

**Don't ignore test files** — But weight them lower; test utilities often use "dangerous" patterns legitimately.

**Don't trust package download counts alone** — New packages can be safe; old packages can be compromised.

**Don't skip manual review** — Automated scans catch patterns, not intent. Always review findings in context.

## Scripts Reference

Use bundled scripts for deterministic analysis:

```bash
# Run full security audit
bash scripts/audit-repo.sh [GITHUB_URL]

# Generate SBOM and vulnerability report
bash scripts/dependency-scan.sh [REPO_PATH]

# Extract features for reimplementation
bash scripts/extract-features.sh [REPO_PATH]
```

## Output Files

Always save to `~/repo-audits/[repo-name]-[date]/`:
- `security-report.md` — Full audit report
- `risk-assessment.json` — Machine-readable scores
- `inventory.txt` — File and dependency inventory
- `suspicious-*.txt` — Raw grep findings
- `clean-scaffold/` — Reimplementation scaffold (if safe)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-05-15 | Initial skill creation for Chibitek Labs |
