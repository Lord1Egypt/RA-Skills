---
name: security-analyst
description: "Use when the user wants a security audit, penetration test, threat model, vulnerability hunt, security fix plan, SBOM, compliance mapping, privacy assessment, or security posture comparison between runs."
always: false
---

# Security Analyst

**Repository:** https://github.com/paixaop/security-analyst

Comprehensive security analysis suite that identifies vulnerabilities, assesses exploitability, and generates actionable remediation plans. Coordinates specialized agents through a multi-phase pipeline — built for developers and security researchers who want depth, not checkbox compliance.

## When to Use

- Before deploying to production or after major feature work
- When a security audit or penetration test is requested
- After a vulnerability is reported, to find unpatched variants
- To generate a threat model for compliance or planning
- To create a fix plan from an existing security report
- To generate a Software Bill of Materials (SBOM) for compliance
- To map findings against SOC 2, ISO 27001, PCI DSS, HIPAA, or GDPR controls
- To compare security posture between two analysis runs (delta/regression tracking)
- To conduct a privacy and data protection assessment (PII flows, consent, data subject rights)

## Available Commands

| Command | Purpose | Agents | Output |
|---------|---------|--------|--------|
| `/security-analyst` | Interactive — choose scope and output mode | Varies | Varies |
| `/security-analyst:full` | All 9 phases, all attack surfaces | 23+ | Full run directory |
| `/security-analyst:focused [component]` | Target a specific area (e.g., authentication, data pipeline) | 3-6 | Inline findings |
| `/security-analyst:recon` | Phase 0 only — codebase security map | 14 (parallel) | Recon index + step files |
| `/security-analyst:threat-model` | Recon + STRIDE analysis + attack trees | 1+ | Threat model doc |
| `/security-analyst:variant-hunt [vuln]` | Find all unpatched variants of a known vulnerability | 2-6 | Variant findings |
| `/security-analyst:fix-plan [run-dir]` | Generate implementation plan from existing report | 1 | Fix plan |
| `/security-analyst:sbom` | Software Bill of Materials — recon + dependency audit only | 15 | SBOM report |
| `/security-analyst:diff [run-a] [run-b]` | Compare two runs — new, resolved, persistent findings | 1 | Delta report |
| `/security-analyst:compliance [framework]` | Map findings to SOC 2 / ISO 27001 / PCI DSS / HIPAA / GDPR | 1 | Compliance report |
| `/security-analyst:privacy` | Privacy assessment — PII flows, consent, data subject rights | 15+ | Privacy report |

## How It Works

### Group-Based Pipeline

Analysis runs in dependency-ordered execution groups. Each group's findings feed the next. Groups are execution-order groupings of phases. Finding IDs use category prefixes (HTTP, INJ, DEP, etc.).

```
Recon: Reconnaissance (14 agents, all parallel — 2 waves)
  └─ Wave A (12 agents, batch-spawned): metadata, docs, HTTP, boundaries, crown jewels, auth, integrations, secrets, security work, config, frontend, deps
  └─ Wave B (2 agents, batch-spawned): data flows, scope notes (depend on Wave A)
  └─ Assembly: orchestrator builds recon/index.md from LOD-0+1 returns

Surface: Attack Surface + Git History + Dependencies + Config (up to 16 agents, batch-spawned in parallel)
  ├─ HTTP entry points, authz rules, integrations, frontend
  ├─ LLM/AI security (OWASP Top 10 for LLM Applications)
  ├─ API schema validation (OpenAPI, GraphQL, gRPC)
  ├─ WebSocket / SSE real-time security
  ├─ File upload security
  ├─ Injection/auth/SSRF/data-exposure variant hunting via git history
  ├─ Dependency audit (npm audit, supply chain)
  ├─ Infrastructure config, secrets, KMS, IAM
  ├─ CI/CD pipeline security (GitHub Actions, GitLab CI)
  └─ Container security (Docker, Kubernetes)

┌─ SBOM Assembly (orchestrator, no agent — runs in parallel with logic stage)
│
Logic: Business Logic (4 agents batch-spawned, needs surface stage)
  ├─ Race conditions and TOCTOU
  ├─ Authorization escalation and IDOR
  ├─ Pipeline exploitation (input → AI → decision → action)
  └─ DoS and resource exhaustion

Tracing: Data Flow Tracing (up to 4 agents batch-spawned, needs surface + logic)
  └─ End-to-end trace of critical data flows with sanitization gap analysis

Exploits: Exploit Development (1 agent, needs all findings)
  └─ Develops complete exploits with PoCs, CVSS scores, CWE/ATT&CK IDs, chains

Validation: Finding Validation (1 critic agent)
  └─ Adversarial review — catches false positives, validates fixes, adjusts severity

Reporting: Final Report (1 agent)
  └─ Executive summary, risk dashboard, remediation roadmap

Remediation: Fix Plan (1 agent)
  └─ Actionable tasks with fix code, regression tests, effort estimates
```

### Finding Format

Every Medium+ finding includes: CVSS 3.1 score, CWE ID, MITRE ATT&CK technique, exploit scoring (exploitability/blast radius/detectability/remediation ROI), attack steps, proof-of-concept, concrete fix code, and regression test.

### Output Directory

Full runs write to `docs/security/runs/{YYYY-MM-DD-HHMMSS}/`:

| File | Content |
|------|---------|
| `recon/index.md` | Recon LOD-0 + LOD-1 index |
| `recon/step-*.md` | 14 atomic LOD-2 recon section files |
| `findings/` | Atomic LOD-2 finding files + index |
| `reports/surface.md` | Attack surface, git history, deps, config |
| `reports/sbom.md` | Software Bill of Materials (deps, licenses, supply chain) |
| `reports/logic.md` | Business logic exploitation |
| `reports/tracing.md` | Data flow tracing |
| `reports/exploits.md` | Exploit catalog with PoCs |
| `reports/validation.md` | Validated findings |
| `reports/final.md` | Complete security report |
| `reports/fix-plan.md` | Implementation plan |
| `reports/compliance.md` | Compliance mapping (when requested) |
| `reports/delta.md` | Delta between two runs (when requested) |
| `reports/privacy.md` | Privacy & data protection assessment (when requested) |

## Command Details

### Full Analysis

Runs all 9 phases with no prompts. Most thorough — spawns up to 28+ agents across 6 execution groups. Expect significant processing time.

```
/security-analyst:full
```

### Focused Analysis

Analyzes a specific component with only relevant agents. Faster (3-6 agents) but still thorough within scope. Findings presented inline — no separate report.

```
/security-analyst:focused authentication
/security-analyst:focused data processing pipeline
/security-analyst:focused frontend
/security-analyst:focused database rules
/security-analyst:focused AI integration
/security-analyst:focused CI/CD
/security-analyst:focused containers
/security-analyst:focused API
/security-analyst:focused real-time
/security-analyst:focused file uploads
```

### Reconnaissance Only

Quick security map without vulnerability analysis. Good for orientation before a full audit or for manual review planning.

```
/security-analyst:recon
```

### Threat Model

Recon plus STRIDE analysis on each trust boundary, attack trees for each crown jewel, and a risk matrix. Useful for compliance (SOC 2, ISO 27001) and security planning.

```
/security-analyst:threat-model
```

### Variant Hunt

Given a known vulnerability (commit hash, CVE, or description), systematically finds all unpatched variants using git history mining and pattern analysis.

```
/security-analyst:variant-hunt 6dc9bb7
/security-analyst:variant-hunt OData injection
/security-analyst:variant-hunt CVE-2024-XXXX
```

### Software Bill of Materials

Generates a compliance-ready SBOM covering all languages, frameworks, direct and transitive dependencies, licenses, and supply chain health indicators. Runs recon plus the dependency audit agent only — no exploitation or attack surface analysis.

```
/security-analyst:sbom
```

### Delta Report

Compares two security analysis runs to highlight new, resolved, and persistent findings. Tracks dependency changes, attack surface evolution, and fix plan progress. Auto-detects the two most recent runs or accepts specific run directories.

```
/security-analyst:diff
/security-analyst:diff docs/security/runs/2025-06-01-100000 docs/security/runs/2025-06-15-143022
```

### Compliance Mapping

Maps findings from an existing security run to a compliance framework. Assesses each control as Pass/Partial/Fail/N/A and produces a compliance score with gap analysis.

```
/security-analyst:compliance soc2
/security-analyst:compliance iso27001
/security-analyst:compliance pci-dss
/security-analyst:compliance hipaa
/security-analyst:compliance gdpr
```

### Privacy Assessment

Traces all PII data flows, evaluates consent mechanisms, checks data subject rights implementation (access, erasure, portability), reviews data retention and deletion, and assesses cross-border transfers. Can run standalone or enrich an existing security run.

```
/security-analyst:privacy
```

### Fix Plan

Generates an implementation plan from an existing security report. Auto-detects the latest run or accepts a specific run directory. Tasks are prioritized: Quick Wins, Immediate, Short-term, Medium-term, Backlog.

```
/security-analyst:fix-plan
/security-analyst:fix-plan docs/security/runs/2025-06-15-143022
```

## Architecture

For detailed architecture reference (directory structure, agent design, LOD architecture, customization), see [references/architecture.md](references/architecture.md). For all constants (paths, filenames, agent registry, placeholders), see [references/constants.md](references/constants.md). **For platform-specific tool mapping (Cursor vs Claude Code vs Codex) and hang prevention, see [references/platform-tools.md](references/platform-tools.md).**

**Key concepts:**
- **LOD system**: Three-tier Level of Detail (LOD-0/1/2) saves 80-96% of prompt tokens for downstream agents while preserving full detail on disk
- **Group discipline**: Later groups depend on earlier findings; never start a group early
- **Dynamic scoping**: Recon determines which agents to skip
- **Framework plugins**: 16 auto-detected plugins inject framework-specific checks into agent prompts. See [references/plugins/README.md](references/plugins/README.md)
- **Critic validation**: Adversarial review catches false positives before the final report

## Before You Install

This skill performs comprehensive security analysis. It instructs agents to read large portions of your repository (including environment and secrets files), run dependency auditors, mine git history, and write proof-of-concept reproductions and reports to disk. Before installing or running it:

1. **Only run on codebases you control** — You must have explicit permission to perform security testing on the target project and environment.
2. **Use an isolated workspace** — Run inside a disposable environment, not a production system or a workspace containing real credentials. If you must analyze a production codebase, clone it into a sandboxed directory first.
3. **Expect persistent artifacts** — Generated PoCs, exploit chains, and fix code are written to `docs/security/runs/` by default. Choose a safe output directory (configurable in `references/constants.md`), review artifacts promptly, and delete or secure them after triage.
4. **Verify tooling availability** — The skill requires `git` and benefits from `npm audit`, `pip-audit`, `govulncheck`, and other ecosystem tools. See [Requirements](#requirements) for the full list and fallback behavior.
5. **Run supervised first** — If you are unsure about scope or safety, do not enable autonomous invocation. Run a manual, supervised test on a throwaway repository before trusting it on a real codebase. The `/security-analyst:recon` command is a good low-risk starting point — it maps the codebase without producing exploits.

## Installation

Copy or symlink this skill folder to your skills directory:

```bash
# Claude Code
cp -r . ~/.claude/skills/security-analyst

# Cursor
cp -r . ~/.cursor/skills/security-analyst

# OpenAI Codex (if applicable)
cp -r . $CODEX_HOME/skills/security-analyst
```

## Requirements

### Workspace Access

The skill requires **read access** to the project codebase and **write access** to the project directory. Agents use Read, Grep, and Glob to analyze source files, and full runs write output to `docs/security/runs/{YYYY-MM-DD-HHMMSS}/` inside the project workspace. The project being analyzed must be the current working directory.

### Platform Tools

All agents are spawned as `generalPurpose` subagents via the **Task** tool and require:

| Tool | Purpose |
|------|---------|
| **Task** | Spawn and coordinate subagents (Claude Code, Cursor, Codex) |
| **Bash / Shell** | Run git commands, dependency auditors, and inline scripts |
| **Read** | Read source files, configs, lockfiles, and prior-stage outputs |
| **Grep** | Search for patterns across the codebase |
| **Glob** | Find files by name/extension patterns |
| **Write** | Write findings, reports, and recon step files to the run directory |

See [references/platform-tools.md](references/platform-tools.md) for platform-specific availability (Cursor vs Claude Code vs Codex).

### Required: `git`

Git is a **hard dependency**. Four agents mine git history (`git log`, `git diff`, `git show`, `git blame`) to find unpatched vulnerability variants. The dependency audit agent uses `git ls-files` to verify lockfile integrity. The variant-hunt command relies entirely on git history analysis. If the project is not a git repository, history-based agents will produce no findings and the variant-hunt command will not function.

### Language-Specific Auditors (used when available)

The dependency audit agent attempts to run vulnerability scanners for detected package ecosystems. These tools are **not required** — if unavailable, the agent falls back to static analysis of manifest and lockfiles, but automated CVE detection will be less thorough.

| Ecosystem | Tool | Invocation | Fallback |
|-----------|------|------------|----------|
| Node.js | `npm` | `npm audit --json` | Parse `package.json` + `package-lock.json` directly |
| Python | `pip-audit` | `pip-audit --json` | Parse `requirements.txt` / `pyproject.toml` directly |
| Go | `govulncheck` | `govulncheck ./...` | Parse `go.mod` / `go.sum` directly |

The agent also runs inline Node.js scripts (via `node -e`) to extract license data from `node_modules/` when present. No global npm packages are installed — only project-local tooling is used.

### SBOM Export Tools (optional)

The SBOM report template references machine-readable export tools. These are **documentation-only recommendations** — the skill does not attempt to run them automatically. The SBOM report is always generated from the dependency audit agent's static analysis regardless of whether these tools are installed.

| Format | Tool |
|--------|------|
| CycloneDX | `npx @cyclonedx/cyclonedx-npm`, `cyclonedx-py`, `cyclonedx-gomod` |
| SPDX | `spdx-sbom-generator`, `syft` |

### Credentials

No credentials, API keys, or authentication tokens are required. All analysis is performed locally against the project source code and git history. The compliance and privacy commands assess implementation by reading code — they do not connect to external compliance platforms.

## Security & Safety Considerations

This skill performs deep security analysis. By design, it reads broadly, looks for weaknesses, and produces proof-of-concept reproductions. The following sections describe the data and safety surfaces so users can make an informed decision before running it.

### Instruction Scope — Broad Read Access

Agents are instructed to read **all files** in the project workspace, including source code, configuration, environment files, lockfiles, CI/CD pipelines, Dockerfiles, and infrastructure-as-code. This is inherent to security analysis — the skill cannot find vulnerabilities in code it cannot read. Specific high-sensitivity reads include:

- **Secret scanning**: Agents grep for patterns like `API_KEY=`, `SECRET=`, `PASSWORD=`, and read `.env*` files, `credentials*` files, and config files to identify hardcoded secrets. The config-infrastructure agent is explicitly instructed to `redact the actual secret` in findings — only file paths and pattern types are reported, not secret values.
- **Git history mining**: Four agents run `git log`, `git diff`, and `git show` to find previously-fixed vulnerabilities and check for incomplete remediation. This can surface deleted secrets that persist in git history.
- **Absolute file paths with line numbers**: Recon agents record exact file locations so downstream agents can `Read` specific code without re-scanning. This is an efficiency optimization, not a privilege escalation — agents already have workspace-wide read access via the platform's Read/Grep/Glob tools.

**The scope is the project workspace only.** Agents do not read files outside the current working directory, do not access the network, and do not read host system files.

### Install Mechanism — Instruction Only

This skill contains no executable code, install scripts, or downloaded binaries. It consists entirely of markdown instruction files (prompts, templates, references) that are read by the orchestrator and injected into agent prompts. The risk surface is in what the instructions ask agents to do at runtime, not in installation.

### Credential Discovery vs. Credential Use

The skill instructs agents to **discover and report on** credentials found in the codebase as part of the security audit. It does **not** use, exfiltrate, or test discovered credentials against external services. Specifically:

| What agents do | What agents do NOT do |
|----------------|----------------------|
| Grep for secret patterns in source and config files | Use discovered secrets to authenticate to any service |
| Read `.env` files to check if they are gitignored | Send secret values to external endpoints |
| Check git history for accidentally committed secrets | Store raw secret values in findings |
| Report the file path and pattern type of exposed secrets | Execute discovered credentials |
| Assess whether secret management (Vault, KMS, etc.) is used | Access cloud metadata endpoints or secret managers |

The config-infrastructure agent prompt (line 115) explicitly mandates: *"Plaintext secret findings are automatically High severity — include the file path (redact the actual secret)."* However, since agents interpret these instructions at runtime, redaction is best-effort. Users handling highly sensitive codebases should review the `findings/` directory after a run and before sharing reports.

### Persistent Artifacts — Exploit PoCs on Disk

Full analysis runs write output to `docs/security/runs/{YYYY-MM-DD-HHMMSS}/` containing:

- **Exploit PoCs**: The finding template requires Medium+ findings to include "concrete exploit code, curl command, or crafted payload" sufficient to reproduce the vulnerability.
- **Exploit chains**: The exploit developer agent produces multi-step attack chains combining individual findings.
- **Fix code**: Each finding includes concrete remediation code and regression tests.

These are **text-based descriptions and code snippets in markdown files**, not standalone executable scripts. They are no more executable than a security advisory with sample payloads. Nevertheless, they represent sensitive security knowledge about the analyzed project.

**Recommendations for managing run artifacts:**

1. **Add to `.gitignore`** — Consider adding `docs/security/runs/` to `.gitignore` to prevent accidental commits of security findings to shared repositories.
2. **Restrict access** — Treat run directories with the same access controls as penetration test reports. Share on a need-to-know basis.
3. **Clean up after review** — Delete run directories after findings have been triaged, remediated, and verified. The `/security-analyst:diff` command can compare runs before cleanup to confirm resolution.
4. **Custom output directory** — The output path is defined in `references/constants.md` (`RUN_DIR`). Change it to write outside the project tree if preferred (e.g., to a directory not tracked by version control).

### Activation

The skill sets `always: false` in its frontmatter. It only activates when the user explicitly requests a security audit, penetration test, threat model, vulnerability scan, SBOM, compliance mapping, or privacy assessment. It does not run automatically on every conversation.

## Troubleshooting

**Skill doesn't trigger on security-related requests**
- Ensure the description includes your trigger phrase. Try: "run a security audit", "penetration test", "threat model", "vulnerability scan", "SBOM", "compliance mapping"

**Analysis hangs / model waits forever**
- On **Cursor**: the orchestrator may be trying to call TaskList or TaskCreate — these don't exist on Cursor. Read `references/platform-tools.md` for the correct flow.
- On **Claude Code / Codex**: each Task call should block until the agent returns. If it hangs, check that agent prompts include "Return your LOD-0 + LOD-1 summary in your final message."

**MCP or subagent connection fails during analysis**
- Verify the environment supports subagent spawning (Claude Code Task tool, Cursor Task tool)
- Check that the project being analyzed is the current workspace so recon agents can Read/Glob the codebase

**Findings seem generic or lack concrete exploits**
- The skill expects findings to include attack steps and PoC. If outputs are shallow, re-run with a focused scope (e.g., `/security-analyst:focused authentication`) for deeper analysis
