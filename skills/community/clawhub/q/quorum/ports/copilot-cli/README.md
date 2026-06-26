# Quorum — Copilot CLI Skill

Multi-critic quality validation for code, configs, and documentation.

## Install

```bash
git clone https://github.com/SharedIntellect/quorum
cp -r quorum/ports/copilot-cli ~/.copilot/skills/quorum
```

## Usage

### Full validation (all critics)
"Run Quorum validation on this file"
"Validate api_handler.py with Quorum"

### Single critic
"Run the security critic on auth.py"
"Check this config for completeness"

### Cross-artifact consistency
"Check if implementation.py matches spec.md"

## What It Checks
- **Correctness** — Logic errors, contradictions, false claims
- **Completeness** — Missing sections, edge cases, broken promises
- **Security** — OWASP ASVS 5.0, CWE Top 25, framework-grounded
- **Code Hygiene** — ISO 25010/5055, structural quality beyond linting
- **Cross-Consistency** — Spec/impl, docs/code, schema contracts

## Verdict Scale
- **PASS** — No issues found
- **PASS_WITH_NOTES** — Minor issues only (MEDIUM/LOW)
- **REVISE** — HIGH severity issues requiring rework
- **REJECT** — CRITICAL issues found

## Requirements
- GitHub Copilot CLI with skill support
- Python 3.10+ (for pre-screen script)
- No additional dependencies

## Skill Structure

```
~/.copilot/skills/quorum/
├── SKILL.md                    # Orchestration (Copilot reads this)
├── quorum-prescreen.py         # Stdlib-only pre-screen script
├── rubrics/
│   ├── python-code.json        # 25 criteria for Python code
│   ├── research-synthesis.json # Research report criteria
│   └── agent-config.json       # Config/YAML criteria
└── critics/
    ├── correctness.agent.md    # Direct single-critic invocation
    ├── completeness.agent.md
    ├── security.agent.md
    ├── code-hygiene.agent.md
    └── cross-consistency.agent.md
```

## What Changes vs Reference Implementation
- LiteLLM provider -> Copilot `task` tool for parallel dispatch
- ThreadPoolExecutor -> Copilot parallel `task` calls
- CLI arguments -> natural language invocation
- Config YAML depth profiles -> SKILL.md instructions
- Python package -> file-based skill (SKILL.md + scripts + rubrics)
- Pydantic models -> plain JSON (in prescreen script)

## What Stays Identical
- Rubric schema and criteria content
- Finding JSON schema (FINDINGS_SCHEMA)
- Pre-screen check IDs (PS-001 through PS-010)
- Verdict taxonomy (PASS / PASS_WITH_NOTES / REVISE / REJECT)
- Severity levels (CRITICAL / HIGH / MEDIUM / LOW / INFO)
- Evidence grounding requirement
- Critic system prompts (verbatim)

## What Is NOT Included in This Port
- **Tester (Phase 3)** — verification requires filesystem access patterns that differ in Copilot
- **Fix loops** — Copilot's edit model differs from file-write patterns
- **Learning memory** — future enhancement
- **Batch mode** — Copilot invocations are per-file

## References
- [Reference Implementation](../../reference-implementation/)
- [Architecture Mapping](ARCHITECTURE.md)
