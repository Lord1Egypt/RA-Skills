# Repo Discovery Auditor

Repo Discovery Auditor is an OpenClaw Agent Skill for auditing unfamiliar codebases before planning, refactoring, or implementation work.

It helps an AI assistant inspect a repository systematically, map its architecture, identify user-facing features, assess maturity, surface risks, and prepare a practical handoff for coding agents such as Codex.

## What It Does

This skill guides the assistant to:

- inspect high-signal project files first;
- identify the framework, runtime, routing model, state management, data layer, authentication, and UI system;
- map user-facing features by page, module, or flow;
- evaluate maturity signals such as validation, loading states, error handling, access control, reusable abstractions, and side-effect handling;
- detect risk signals such as duplicated business logic, stale schema references, weak typing, inconsistent authorization checks, debug code, and ad-hoc branching;
- produce a concise, evidence-based repository audit.

## When to Use

Use this skill when you need to:

- inspect an unfamiliar repository;
- understand a project's architecture and structure;
- summarize implemented features;
- judge what looks mature versus rough or incomplete;
- identify technical risks before making changes;
- prepare a coding brief for another implementation agent.

## Suggested Output Structure

The skill recommends returning findings in this order:

1. Architecture summary
2. Key stack and structure
3. User-facing feature map
4. What looks mature
5. What looks rough or incomplete
6. Important risks or inconsistencies
7. Best next move

## Maturity Labels

Use simple, explainable labels:

- **Mature** — implemented with clear structure, safeguards, and reusable patterns.
- **Working but rough** — functional, but missing polish, consistency, or robustness.
- **Unclear or likely incomplete** — not enough evidence, partial implementation, or missing critical pieces.

## Evidence Rule

Every claim should be tied to actual files, code patterns, or inspected project structure.

Do not claim runtime behavior unless it has been verified. If something is inferred from static code only, say so clearly.

## Installation

Copy the skill folder into your OpenClaw workspace skills directory:

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -r repo-discovery-auditor ~/.openclaw/workspace/skills/
```

Then restart or reload OpenClaw if your setup requires it.

## Files

```text
repo-discovery-auditor/
├── README.md
└── SKILL.md
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
