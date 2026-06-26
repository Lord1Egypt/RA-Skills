---
name: Review Code
slug: review-code
version: 1.0.0
homepage: https://clawic.com/skills/review-code
description: Review code with risk-first analysis, reproducible evidence, and patch-ready guidance for correctness, security, performance, and maintainability.
changelog: Initial release with risk-first review workflow, severity-confidence scoring, and fix-ready output templates.
metadata: {"clawdbot":{"emoji":"🔎","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` for integration guidance and local memory initialization.

## When to Use

User asks for a code review, PR review, merge-readiness check, or bug-risk audit before shipping.
Agent delivers a risk-ranked review with explicit evidence, impact, confidence, and concrete fix direction.

## Architecture

Memory lives in `~/review-code/`. See `memory-template.md` for structure and starter templates.

```text
~/review-code/
├── memory.md             # Review preferences, stack context, and recent constraints
├── findings/             # Optional per-review finding logs
├── baselines/            # Team conventions and accepted risk baselines
└── sessions/             # Session summaries for ongoing audits
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and integration behavior | `setup.md` |
| Memory schema and templates | `memory-template.md` |
| End-to-end review execution flow | `review-workflow.md` |
| Severity and confidence calibration | `severity-and-confidence.md` |
| Language and architecture risk checks | `language-risk-checklists.md` |
| Test impact requirements by change type | `test-impact-playbook.md` |
| Comment and report templates | `comment-templates.md` |
| Patch strategy for actionable fixes | `patch-strategy.md` |

## Data Storage

Local notes stay in `~/review-code/`.
Before creating or changing local files, present the planned write and ask for user confirmation.

## Core Rules

### 1. Define the Review Contract First
Confirm target scope before reviewing: branch, files, risk tolerance, and release context.
If scope is unclear, state assumptions explicitly and keep findings tied to those assumptions.

### 2. Start With Risk Mapping, Then Deep Dive
Run a fast pass to locate high-risk zones first: auth, money, data integrity, concurrency, and migration paths.
Only then perform line-level analysis with `review-workflow.md` so major failures are surfaced early.

### 3. Every Finding Must Be Evidence-Backed
Do not report vague concerns.
Each finding must include: trigger location, concrete failure mode, user or business impact, and minimal reproduction clue.
If evidence is weak, mark low confidence or downgrade to a question.

### 4. Separate Blocking vs Advisory With Severity + Confidence
Use `severity-and-confidence.md` for consistent triage.
Blocking findings must be reproducible or highly probable with strong impact.
Advisory feedback must remain concise and never hide blockers.

### 5. Always Pair Findings With a Fix Path
For each blocking issue, provide a minimally disruptive fix strategy.
Use `patch-strategy.md` to propose rollback-safe edits, guard tests, and verification steps.

### 6. Tie Review Quality to Test Impact
Map each change to required tests using `test-impact-playbook.md`.
If tests are missing, list the exact scenarios that must be added and why they prevent regressions.

### 7. Optimize for Signal, Not Volume
Prioritize high-impact defects over style noise.
If no blockers are found, state that explicitly and list residual risks, test gaps, and monitoring advice.

## Common Traps

- Reporting opinions as facts -> review credibility drops and teams ignore real blockers.
- Mixing blocker and nit feedback without labels -> delayed merges and mis-prioritized fixes.
- Calling something “probably fine” without tests -> silent regressions in production.
- Suggesting large rewrites for local defects -> good fixes are postponed indefinitely.
- Ignoring release context (hotfix vs refactor) -> wrong trade-offs for urgency.
- Missing migration and backward-compatibility checks -> runtime failures after deploy.

## External Endpoints

This skill makes NO external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Nothing by default. This is an instruction-only review skill unless the user explicitly exports artifacts.

**Data stored locally:**
- Review preferences, project constraints, and optional findings approved by the user.
- Stored in `~/review-code/`.

**This skill does NOT:**
- auto-approve code or merge pull requests.
- make undeclared network calls.
- store credentials, tokens, or sensitive payloads.
- modify its own core instructions or auxiliary files.

## Trust

This is an instruction-only code review skill.
No credentials are required and no third-party services are contacted by default.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `code` - implementation workflow that complements review findings.
- `git` - safer branch, diff, and commit handling during remediation.
- `typescript` - stricter typing and runtime safety review for TS-heavy codebases.
- `ci-cd` - release-gate checks and deployment safeguards after fixes.
- `devops` - production risk assessment and rollback planning.

## Feedback

- If useful: `clawhub star review-code`
- Stay updated: `clawhub sync`
