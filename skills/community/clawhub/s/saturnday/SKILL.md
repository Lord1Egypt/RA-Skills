---
name: saturnday
version: 1.8.0
description: Governed AI software execution — 48+ deterministic governance checks for Python with additional checks for TypeScript, DevOps, and project metadata. LLM-powered security triage to filter false positives. Build projects from a brief with per-commit governance, produce governed documents, inspect release artefacts, or auto-fix findings. Six backends — Claude Code, Codex, OpenClaude, Cursor, OpenAI API, Anthropic API. Requires pip install saturnday.
homepage: https://www.saturnday.dev
source: https://github.com/honouralexwill/saturnday
license: MIT
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - git
    optional_bins:
      - node
    optional_env:
      - ANTHROPIC_API_KEY
      - OPENAI_API_KEY
      - OPENCLAUDE_API_KEY
      - CURSOR_API_KEY
    install:
      - cmd: pip install saturnday
      - cmd: echo "Saturnday installed. Run 'saturnday version' to verify."
    notes: >
      Scan mode requires only python3 and git. Guard mode requires python3, git, and optionally node for TypeScript checks.
      Run mode requires python3, git, and at least one AI backend API key or CLI tool (claude, codex, openclaude, or cursor).
      All API keys are optional — set only the one for your chosen backend.
      Run and Guard modes modify the target repository (git commits, evidence directories).
      Run mode transmits repository contents to the chosen AI backend for code generation.
---

# Saturnday

Govern AI-built software from scan to build to repair — all from the terminal. Saturnday runs 48+ deterministic governance checks on Python projects (with additional checks for TypeScript, DevOps files, and project metadata), builds projects from a brief with ticketed execution and per-commit governance, produces governed documents, inspects release artefacts, and auto-fixes findings with evidence.

**Requires:** `pip install saturnday` (Python 3.10+)

Verify installation:
```bash
saturnday version
```

If saturnday is not installed, run:
```bash
pip install saturnday
```

---

## Three Modes

Saturnday has three core modes plus document and release modes. Choose based on the task:

| Mode | When to use | Command |
|------|-------------|---------|
| **Scan** | Check a skill or repo for issues | `python scripts/scan.py <path>` |
| **Guard** | Full governance on a git repo | `python scripts/guard.py <path>` |
| **Run** | Build a project from a brief | `python scripts/run.py <path> --brief "..."` |
| **Document** | Produce a governed document | `saturnday start --document --doc-spec spec.yaml` |
| **Release** | Inspect artefacts before publishing | `saturnday release-preflight --repo <path>` |

---

## Mode 1: Scan

**Use when:** checking an OpenClaw skill for security risks, hallucinated imports, fake tests, or quality issues before installing or publishing.

```bash
python scripts/scan.py <skill-directory-path>
```

Or directly:
```bash
saturnday scan --skill <skill-directory-path> --output /tmp/scan-results --format both
```

### What it checks
- 19 Python security checks (SQL injection, auth bypass, CSRF, XSS, hardcoded secrets)
- 19 TypeScript security checks
- Hallucinated import detection (packages that don't exist)
- No-assert and fake test detection
- Dead code (cross-file analysis)
- Dependency declaration verification
- Project hygiene (README, LICENSE)
- Dockerfile checks (unpinned images, root user, secrets in build, missing dockerignore)
- GitHub Actions (SHA pinning, broad permissions, pull_request_target, plaintext secrets)
- GitLab CI (secrets in YAML, docker-in-docker patterns)
- Jenkins (hardcoded credentials)
- Terraform (hardcoded credentials, public CIDR)
- Kubernetes (privileged containers, unpinned images, secrets in manifests)
- Optional Trivy integration for deep IaC analysis

### Output
```
Disposition: PASS or FAIL
Findings: list with check name, severity, file, line, description
Evidence: timestamped directory with full results
```

---

## Mode 2: Guard

**Use when:** running full governance on any git repository — before merging, before deploying, or for audit.

```bash
python scripts/guard.py <repo-path>
```

For staged changes only (pre-commit):
```bash
python scripts/guard.py <repo-path> --staged
```

Or directly:
```bash
saturnday governance --repo <path> --full
```

### What it checks
48+ deterministic checks for Python projects: security (SQL injection, XSS, CSRF, auth bypass, hardcoded secrets, WebSocket security, OAuth, token handling, rate limiting, IDOR, user enumeration, cookie security), AI-specific (hallucinated imports, fake tests, dead code, placeholders), quality (syntax, dependencies, Python version compat, code quality, blast radius, project hygiene, typosquat detection). Additional checks activate for DevOps files (Dockerfile, GitHub Actions, GitLab CI, Jenkins, Terraform, Kubernetes, config security) and TypeScript/JavaScript code.

### Ratchet baselines
Prevent regressions:
```bash
saturnday baseline generate --repo <path>
```

### Policy exemptions
Create `.saturnday-policy.yaml`:
```yaml
expected_findings:
  - declared_not_installed
  - package_not_importable
```

---

## Mode 3: Run

**Use when:** building a project from a description. This is the full governed execution pipeline.

```bash
python scripts/run.py <project-directory> --brief "build a REST API with auth and tests" --backend anthropic
```

Or interactively:
```bash
cd <project-directory>
saturnday start
```

### Backends

| Backend | Value | Auth |
|---------|-------|------|
| Claude Code CLI | `claude-cli` | Claude Pro subscription |
| Codex CLI | `codex-cli` | OpenAI subscription |
| OpenClaude | `openclaude` | OpenClaude CLI |
| Cursor CLI | `cursor-cli` | Cursor |
| OpenAI API | `openai` | OPENAI_API_KEY |
| Anthropic API | `anthropic` | ANTHROPIC_API_KEY |

### What happens during a run

1. **Security triage** — LLM-powered data flow analysis filters false positives from security findings so you only review what matters
2. **Brief enrichment** — vague briefs are auto-enriched with technical detail before planning
2. **Planning** — 3-stage planner generates tickets with acceptance criteria and scope constraints
3. **Execution** — each ticket executed sequentially, governance checks after every commit
4. **Auto-install** — dependencies are automatically installed between tickets when pyproject.toml or package.json changes
5. **Retry** — if governance fails, revert, feed findings back, retry (up to 3 attempts)
6. **Ungoverned commit** — if a ticket still fails after retries and auto-repair, the code is committed with a `[GOVERNANCE: review required]` tag so the project stays complete
7. **Auto-repair** — after all tickets, ungoverned and failed tickets go through the repair pipeline again
8. **Definition of done** — evaluates whether plan goals are met
9. **Review report** — for ungoverned tickets: `review-required.md` with findings, remediation tips, and copy-paste fix prompts for each ticket
10. **Progress log** — live `saturnday-progress.log` with ticket outcomes, governance results, and counterfactual messages showing what ungoverned AI coders would have done wrong
11. **Evidence** — timestamped directory with per-ticket results, governance evidence, analytics

### Resume interrupted runs

Saturnday auto-detects prior runs. If you restart `saturnday run` on a project that already has a ledger, tickets that already passed are skipped automatically. You can also resume explicitly:

```bash
saturnday resume --repo <path> --backend anthropic
```

---

## Document Mode

**Use when:** producing governed documents (specs, reports, audits) with section-level checks and cross-section consistency validation.

```bash
saturnday start --document --doc-spec doc-spec.yaml --backend claude-cli
```

The pipeline: parse spec, plan sections, generate each section, run section-level checks (structure, placeholders, citations, evidence coverage), retry failures, run cross-section consistency checks, and produce a signed-off evidence pack.

---

## Release Preflight

**Use when:** inspecting built artefacts (wheels, sdists, npm tarballs, OCI images) before publishing.

```bash
saturnday release-preflight --repo <path> --type python
saturnday release-preflight --wheel dist/mypackage-1.0-py3-none-any.whl
```

Runs 5 release-security checks: source map blocking, secrets in artefact, internal file blocking, allowlist manifest validation, and release diff comparison. Separate from code governance.

---

## When to Use Each Mode

- **"Scan this skill before I install it"** → Scan
- **"Check this repo for security issues"** → Guard
- **"Build me a project from this description"** → Run
- **"Audit this codebase"** → Guard
- **"Produce a governed document"** → Document mode
- **"Check this wheel before publishing"** → Release preflight
- **"Fix the findings"** → use `saturnday repair --repo <path>` directly

## Prerequisites

- `pip install saturnday` (Python 3.10+)
- Node.js 18+ (for TypeScript checks)
- Git (for Guard and Run modes)
- At least one AI coder backend for Run mode
