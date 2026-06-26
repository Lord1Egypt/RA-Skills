# Skill Vetter v2

**Know what a skill does before you trust it.**

Skill Vetter v2 is a packaged safety-review skill for evaluating agent skills before installation or use. It preserves a local, review-first workflow and adds optional SettlementWitness verification for the finished report.

## Why this exists

Most agent skills are installed based on a short description and a guess.

That creates avoidable risk:
- hidden file access
- undisclosed network behavior
- silent trust in opaque external services
- credential exposure or workspace exfiltration

Skill Vetter v2 makes those risks visible before a skill is trusted.

## What it analyzes

Every target skill is reviewed across four areas:

### 1. Purpose and scope
Does the actual package match the stated purpose?

### 2. Install-time behavior
Does it write files, register hooks, install packages, or modify environment state?

### 3. Runtime behavior
Does it execute commands, access sensitive files, call external services, or handle data broadly?

### 4. Trust dependency
Does it rely on narrow and understandable external systems, or on opaque services that require blind trust?

## Output

The skill produces a structured report with:
- capability inventory
- install-time risk
- runtime risk
- trust dependency classification
- warnings and recommendations
- final verdict: `safe`, `caution`, or `unsafe`

## SettlementWitness integration

This skill does **not** delegate the safety decision.

Optional verification is used only after local review is complete.
It can validate that the final report matches a deterministic spec and provide receipt metadata for auditability.

Use it conservatively:
- send only structured report data
- never send secrets, credentials, personal data, or full private repositories
- treat PASS as evidence that the report matches the spec, not as a substitute for judgment

## Included package structure

```text
skill-vetter-v2/
├── SKILL.md
├── README.md
├── _meta.json
├── .learnings/
├── assets/
├── hooks/
├── references/
└── scripts/
```

## Scripts

### `scripts/scan-skill.sh`
Local helper that inventories a skill directory and flags suspicious patterns such as:
- credential access attempts
- network calls
- package installs
- obfuscated execution
- writes outside expected scope

### `scripts/activator.sh`
Reminder hook content for prompting a vetting pass before a skill is trusted.

### `scripts/error-detector.sh`
Reminder that suspicious outputs or failures discovered during review should be captured in the final report.

## Hook

The OpenClaw hook injects a short reminder during bootstrap:
- review the full package, not just `SKILL.md`
- classify risk before installation
- keep verdict decisions local
- optionally verify the final report

## Best use cases

- reviewing third-party skills before install
- auditing internal packaged skills
- comparing multiple skills that solve the same task
- enforcing trust boundaries in autonomous agent environments

## Design rules

- preserve local judgment
- prefer transparent dependencies
- no mandatory identity
- no required credentials
- no blind PASS-to-trust shortcut
- verification augments review; it does not replace it

## Installation

Add this repository as a Claude/OpenClaw skill, or copy the folder into your local skills directory.

## Tags

ai-agents  
security  
risk-analysis  
trust  
verification  
skill-review
