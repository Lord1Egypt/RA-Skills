# CODEX Security Audit Report

Date: 2026-03-08
Repository: `/private/tmp/normieclaw-tutor-buddy-pro`
Scope: Entire repository content excluding `.git/` internals

## Files Reviewed
- `README.md`
- `SECURITY.md`
- `SETUP-PROMPT.md`
- `SKILL.md`
- `config/tutor-config.json`
- `dashboard-kit/DASHBOARD-SPEC.md`
- `dashboard-kit/manifest.json`
- `examples/quiz-mode.md`
- `examples/study-plan.md`
- `examples/tutoring-session.md`
- `scripts/generate-progress-report.sh`
- `CODEX-SECURITY-AUDIT.md`

## Method
- Manual line-by-line review of all repository files.
- Secret pattern scan for API keys, tokens, credentials, private keys, and connection strings.
- Shell safety review: quoting, injection, temp file handling, filesystem write scope.
- Path traversal and file write boundary review.
- Data exfiltration behavior review (network-capable flows and script behavior).
- Prompt injection defense review in `SKILL.md`.
- JSON validation and safety review for config/manifest.

## Summary Counts
- Critical: 0
- High: 0 open (1 fixed)
- Medium: 1
- Low: 2
- Info: 3

## Detailed Findings

### 1) HTML Injection in Progress Report Renderer (Fixed)
- Severity: High (Fixed)
- File: `scripts/generate-progress-report.sh`
- Description: User-controlled values from `data/learner-profile.json` and `data/quiz-history.json` were inserted directly into HTML. A crafted value (for example in learner name/topic) could inject HTML/JS during Playwright rendering, enabling outbound requests and potential data exfiltration.
- Fix: Added strict output encoding and numeric sanitization in embedded Python:
  - `html.escape(...)` for text fields.
  - `safe_int(...)` with type coercion and bounds for numeric fields.
  - Type guards for dictionary/list structures before rendering.

### 2) Arbitrary Output Path Write Risk (Fixed)
- Severity: High (Fixed)
- File: `scripts/generate-progress-report.sh`
- Description: Script previously accepted arbitrary output paths, allowing writes outside workspace boundaries if called with absolute paths or traversal-style arguments.
- Fix: Restricted output to `WORKSPACE_ROOT/reports/` and normalized user input to basename-only (`OUTPUT_NAME="$(basename "$1")"`).

### 3) Setup Prompt Path Resolution Can Mis-handle Multiple Matches
- Severity: Medium
- File: `SETUP-PROMPT.md` (Step 5)
- Description: `SKILL_DIR=$(find . -path "*/skills/tutor-buddy-pro/SKILL.md" -exec dirname {} \;)` can return multiple lines or empty output; downstream recursive `find "$SKILL_DIR" ... chmod ...` may fail or target unintended paths.
- Fix: Resolve one path deterministically and validate before chmod. Example:
  - `SKILL_DIR=$(find ... | head -1)`
  - `[ -n "$SKILL_DIR" ] && [ -d "$SKILL_DIR" ] || exit 1`

### 4) Permission Policy/Reality Mismatch
- Severity: Low
- File: `SECURITY.md`, repository file modes
- Description: `SECURITY.md` asserts `config/tutor-config.json` should be `600`, but current repository mode is `644` in this checkout. This is a policy mismatch and can confuse operators.
- Fix: Add explicit note that secure permissions are enforced during setup/runtime (not guaranteed by repository checkout), and include a verification script/check step.

### 5) Future Sync Path Is a Potential Exfiltration Surface (Design-Level)
- Severity: Low
- File: `dashboard-kit/DASHBOARD-SPEC.md`
- Description: Spec documents `/api/sync` ingestion from local JSON. While no executable sync code exists here, future implementation introduces exfiltration risk if enabled without strict controls.
- Fix: Require explicit opt-in, authenticated transport, schema validation, and data minimization when implemented.

### 6) Hardcoded Secrets Scan
- Severity: Info
- File: Repository-wide
- Description: No hardcoded API keys, access tokens, passwords, private keys, or credential-like connection strings found.
- Fix: No action required.

### 7) Prompt Injection Defense Review
- Severity: Info
- File: `SKILL.md`
- Description: Prompt injection defenses are explicit and strong: untrusted OCR/text/web content treated as data, command-like text ignored, and sensitive learner data protected.
- Fix: No action required.

### 8) JSON Config Safety Review
- Severity: Info
- File: `config/tutor-config.json`, `dashboard-kit/manifest.json`
- Description: JSON is syntactically valid (`jq empty`), contains no secrets, and does not include dynamic code execution hooks.
- Fix: No action required.

## Re-Audit After Fixes
- Re-ran shell syntax check: `bash -n scripts/generate-progress-report.sh` (pass).
- Re-ran secret scan patterns (no credential findings).
- Re-checked JSON validity (`jq empty`) for both JSON files (pass).
- Confirmed High findings are remediated in current code.

## Final Verdict
PASS

Rationale: No unresolved Critical or High findings remain. One Medium and two Low hardening items remain as follow-up recommendations.
