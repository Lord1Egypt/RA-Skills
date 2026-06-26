# skill-evolver

[English](README.md) | [中文](README.zh-CN.md)

> Solve first. Materialize later.

`skill-evolver` is a spec-driven skill lifecycle manager for Claude Code, Codex, and OpenClaw-style runtimes. It helps an agent find the right skills, verify whether they are safe, decide whether to orchestrate or fuse them, and preserve successful workflows as reusable capabilities.

## Problem

Most AI coding workflows break down before execution:

- **Skill discovery is fragmented**: useful skills are scattered across local folders, registries, and personal repos.
- **Trust is unclear**: installing a skill from a public source without auditing it is a real risk.
- **Composition is underspecified**: sometimes one skill is enough, sometimes you need orchestration, and sometimes only deep fusion works.
- **Reuse is inconsistent**: strong one-off workflows often disappear instead of becoming reusable skills.

## Solution

`skill-evolver` turns skill usage into a deliberate workflow instead of ad hoc trial and error:

- **Analyze the task first** to clarify what the user actually needs.
- **Search across local and remote sources** including installed skills, `skills.sh`, and ClawHub.
- **Inspect and audit candidates** before using or installing them.
- **Let the LLM choose the right path**: native execution, orchestration, or fusion.
- **Add human checkpoints** where the decision carries product or security risk.
- **Materialize proven workflows** into reusable skills only after they have demonstrated value.

## What You Get

- **Safer skill adoption** with verification and security audit built into the workflow.
- **Clear decision points** for choosing between native execution, orchestration, and fusion.
- **A complete lifecycle** from discovery to execution to optional skill creation.
- **Cross-ecosystem coverage** for Claude Code, Codex, and OpenClaw-style runtimes.
- **Repeatable outputs** through templates, scripts, and documented phase artifacts.

## How It Works

```text
Phase 0: Setup Output Directory
Phase 1: Intent Analysis
Phase 2: Skill Search (local + skills.sh + ClawHub)
Phase 3: Deep Inspection
Checkpoint: Approach Decision
Phase 3.5: Skill Fusion (conditional)
Phase 4: Orchestration
Checkpoint: Plan Confirmation
Phase 5: Execution
Checkpoint: Materialization Decision
```

## Core Capabilities

- **Dual-track search**: query local skills and remote registries in one workflow.
- **Security audit**: detect destructive commands, remote execution patterns, credential exfiltration, and privilege escalation risks.
- **LLM-guided decision making**: evaluate fit and recommend native execution, orchestration, or fusion.
- **Skill fusion**: combine multiple partial-fit skills into a more coherent capability.
- **Workflow preservation**: turn a successful execution path into a reusable skill when it proves repeat value.

## Installation

**Recommended (via skills.sh):**
```bash
npx skills add ClawSkill/skill-evolver -g -y
```

**Manual:**
```bash
# Clone the repo
git clone https://github.com/ClawSkill/skill-evolver.git

# Copy to your skills directory
# macOS / Linux
cp -r skill-evolver/* ~/.claude/skills/skill-evolver/

# Windows (PowerShell)
Copy-Item -Recurse skill-evolver/* $env:USERPROFILE\.claude\skills\skill-evolver\
```

### Optional prerequisites

Install CLI tools for remote skill search:

```bash
# Skills.sh (Vercel) - No installation needed, runs directly via npx
# Usage: npx skills find <query>
#        npx skills add <source> -g -y
# Docs: https://github.com/vercel-labs/skills

# ClawHub (OpenClaw) - Requires global installation
npm i -g clawhub
# Usage: clawhub search "<query>"
#        clawhub install <slug>
# Docs: https://docs.openclaw.ai/zh-CN/tools/clawhub
```

## Repository Structure

```text
.
|-- SKILL.md
|-- README.md
|-- scripts/
|   |-- search_skills.py
|   |-- audit_skill.py
|   `-- verify_skill.py
`-- references/
    |-- skill-search.md
    |-- skill-fusion.md
    |-- skill-inspector.md
    `-- templates/
        |-- 01-intent.md
        |-- 02-candidates.md
        |-- 03-inspection.md
        |-- 03b-fusion-spec.md
        `-- 04-orchestration.md
```

## License

This project is licensed under the [MIT License](LICENSE).
