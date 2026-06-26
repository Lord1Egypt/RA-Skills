# CODEX Security Audit Report

**Repository:** `normieclaw-trainer-buddy-pro`  
**Audit Date:** 2026-03-08  
**Auditor:** Codex (GPT-5)

## Scope
Audited all repository files (excluding `.git/*` internals) for:
1. Hardcoded secrets or credential-like strings
2. Shell script safety issues
3. Path traversal risks
4. Data exfiltration risks
5. File permission issues
6. Prompt injection defense in `SKILL.md`
7. JSON config safety

## Method
- Enumerated all files with `rg --files` and `find . -type f`
- Manual line-by-line review of every repo file
- Secret-pattern scan via `rg` for common key/token formats
- Shell script static review and syntax check (`bash -n`)
- Permission inspection via `stat`

## Summary Counts
- Critical: **0**
- High: **1** (**1 fixed**)
- Medium: **2**
- Low: **2**
- Informational: **4**

## Detailed Findings

### 1) Unsafe backup cleanup pipeline could delete unintended paths (Fixed)
- **Severity:** High
- **File:** `scripts/backup-workout-data.sh` (previously cleanup block at end of file)
- **Description:** Old logic used `ls ... | head ... | xargs rm -rf`. This pattern is unsafe with whitespace/newlines in directory names and is generally brittle for destructive operations.
- **Fix:** Replaced with safe directory enumeration + bounded loop + `rm -rf -- "$old_backup"`; added `umask 077`; removed unsafe `xargs` path handling.
- **Status:** Fixed in current code (`scripts/backup-workout-data.sh:7`, `:79-86`).

### 2) Setup command used `xargs dirname` path parsing (Fixed)
- **Severity:** Low
- **File:** `SETUP-PROMPT.md:9-16`
- **Description:** Old install snippet used `... | xargs dirname`, which can break on whitespace and produce incorrect source path resolution.
- **Fix:** Replaced with `find ... -print -quit` and safe `dirname` expansion in shell variables.
- **Status:** Fixed.

### 3) Security claims conflict with repository content
- **Severity:** Medium
- **File:** `SECURITY.md:12-15`, `SECURITY.md:33`
- **Description:** Document states “NO external data transmission” and “No `rm -rf`”, but repository includes optional dashboard cloud sync guidance (`dashboard-kit/DASHBOARD-SPEC.md`) and backup cleanup uses controlled `rm -rf`.
- **Fix:** Update `SECURITY.md` claims to reflect reality: local-only by default, optional cloud sync exists, and controlled cleanup deletion exists.
- **Status:** Open.

### 4) Dashboard sync scope may include sensitive injury/profile data without minimization controls
- **Severity:** Medium
- **File:** `dashboard-kit/manifest.json:19`
- **Description:** `"source_files": ["trainer-buddy-pro/data/"]` can sync full local data directory (including injury and profile data) if downstream sync is enabled. No built-in data-minimization allowlist in this config.
- **Fix:** Restrict to explicit file allowlist (e.g., workout-only datasets), add opt-in gate and redaction guidance for sensitive fields.
- **Status:** Open.

### 5) Package file permissions are mostly world-readable
- **Severity:** Low
- **File:** `README.md`, `SKILL.md`, `SETUP-PROMPT.md`, `SECURITY.md`, `config/trainer-config.json`, examples (current mode `644`)
- **Description:** Current repo modes are broadly readable. This is usually fine for a distributed skill package, but it conflicts with stricter privacy posture described in docs for runtime data/config.
- **Fix:** Keep package docs readable, but enforce runtime-generated `data/*` at `600` and `data/` at `700`; optionally set packaged config to `600` in release artifacts.
- **Status:** Open (documentation/operational hardening item).

## Informational Checks
- **Hardcoded secrets:** No credential-like strings detected by pattern scan.
- **Path traversal:** No direct user-input-to-path concatenation found in scripts/config.
- **Prompt injection defense:** `SKILL.md` contains explicit and strong defense rules (`SKILL.md:17-25`).
- **JSON safety:** JSON files are syntactically valid and static; no executable expressions.

## Re-Audit After Fixes
Re-ran checks after patching shell safety items:
- `bash -n scripts/backup-workout-data.sh` passed
- Secret scan returned no matches
- Unsafe `xargs rm -rf` pattern no longer present

## Final Verdict
**PASS**

No unresolved Critical/High vulnerabilities remain after remediation. Medium/Low hardening items should be addressed in a follow-up documentation/config tightening pass.
