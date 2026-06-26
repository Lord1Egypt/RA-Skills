# Security Analyst

[![GitHub](https://img.shields.io/github/stars/paixaop/security-analyst?style=social)](https://github.com/paixaop/security-analyst)

Comprehensive security analysis skill for Claude Code, Cursor, and Codex. Identifies vulnerabilities, assesses exploitability, and generates actionable remediation plans. Coordinates specialized agents through a multi-phase pipeline — built for developers and security researchers who want depth, not checkbox compliance.

**Repository:** https://github.com/paixaop/security-analyst

## When to Use

- **Before deploying** or after major feature work
- **On demand** for security audits, penetration tests, threat models
- **After a vulnerability** is reported, to find unpatched variants
- **For compliance** — SBOM, SOC 2, ISO 27001, PCI DSS, HIPAA, GDPR
- **For tracking** — compare security posture between runs (delta/regression)

## Quick Start

| Command | Purpose |
|---------|---------|
| `/security-analyst` | Interactive — choose scope and output mode |
| `/security-analyst:full` | All phases, all attack surfaces |
| `/security-analyst:focused [component]` | Target one area (auth, API, frontend, etc.) |
| `/security-analyst:recon` | Reconnaissance only — codebase security map |
| `/security-analyst:threat-model` | STRIDE, attack trees, risk matrix |
| `/security-analyst:variant-hunt [vuln]` | Find unpatched variants of a known vuln |
| `/security-analyst:fix-plan [run-dir]` | Implementation plan from existing report |
| `/security-analyst:sbom` | Software Bill of Materials |
| `/security-analyst:diff [run-a] [run-b]` | Compare two runs — new, resolved, persistent |
| `/security-analyst:compliance [framework]` | Map findings to compliance controls |
| `/security-analyst:privacy` | PII flows, consent, data subject rights |

## Installation

Copy or symlink this skill to your skills directory:

```bash
# Claude Code
cp -r . ~/.claude/skills/security-analyst

# Cursor
cp -r . ~/.cursor/skills/security-analyst
```

## Output

Full runs write to `docs/security/runs/{YYYY-MM-DD-HHMMSS}/`:

| Path | Content |
|------|---------|
| `recon/index.md` | Recon index (LOD-0 + LOD-1) |
| `recon/step-*.md` | 14 atomic recon section files |
| `findings/` | Atomic finding files + index |
| `reports/surface.md` | Attack surface, git history, deps, config |
| `reports/sbom.md` | Software Bill of Materials |
| `reports/logic.md` | Business logic exploitation |
| `reports/tracing.md` | Data flow tracing |
| `reports/exploits.md` | Exploit catalog with PoCs |
| `reports/validation.md` | Validated findings |
| `reports/final.md` | Complete security report |
| `reports/fix-plan.md` | Implementation plan |
| `reports/compliance.md` | Compliance mapping (when requested) |
| `reports/delta.md` | Delta between runs (when requested) |
| `reports/privacy.md` | Privacy assessment (when requested) |

## Pipeline Overview

```
Recon (14 agents, parallel)
    ↓
Surface (≤16 agents) — HTTP, auth, integrations, frontend, LLM, API, deps, config, CI/CD, containers
    ↓
Logic (4 agents) — race conditions, authz escalation, pipeline exploitation, DoS
    ↓
Tracing (≤4 agents) — data flow + sanitization gaps
    ↓
Exploits (1) → Validation (1 critic) → Reporting (1) → Remediation (1 fix plan)
```

- **LOD system**: Three tiers reduce prompt tokens while keeping full detail on disk
- **Framework plugins**: 16 auto-detected plugins (Firebase, React, Django, etc.) inject framework-specific checks
- **Critic validation**: Adversarial review before final report

## Project Structure

```
security-analyst/
├── SKILL.md
├── README.md (this file)
├── references/
│   ├── architecture.md    # Architecture reference
│   ├── constants.md       # Paths, agent registry, templates
│   ├── commands/          # Entry points
│   ├── prompts/           # Agent prompt templates
│   └── plugins/           # Framework-specific checks (16 plugins)
└── assets/
    └── templates/         # Output format templates
```

## Troubleshooting

**Skill doesn't trigger**
- Use phrases like "run a security audit", "penetration test", "threat model", "SBOM", "compliance mapping"

**Analysis hangs / model waits forever**
- On Cursor: the orchestrator may be calling TaskList/TaskCreate which don't exist. See `references/platform-tools.md` for the correct flow.

**Subagent fails**
- Verify the environment supports the Task tool for subagent spawning
- Ensure the project being analyzed is the current workspace

**Findings seem generic**
- Re-run with a focused scope: `/security-analyst:focused authentication`

## References

- [references/architecture.md](references/architecture.md) — Architecture, LOD system, agent design
- [references/constants.md](references/constants.md) — Paths, filenames, agent registry
- [references/plugins/README.md](references/plugins/README.md) — Plugin format and detection
