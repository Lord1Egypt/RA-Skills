---
name: skill-audit
description: >-
  Runs a deterministic static safety audit for third-party AI skill or plugin
  repositories before install or execution. Use when asked to scan a skill repo,
  assess whether a repo is safe to install, run a skill safety assessment, or
  produce evidence-backed findings for pre-install security screening.
version: 0.1.0
metadata:
  clawdbot:
    homepage: https://github.com/mode-io/mode-io-skills/tree/main/skill-audit
    requires:
      bins:
        - python3
---

# Run pre-install repository safety audits

Use this skill to evaluate a skill, plugin, or repository before you install it, trust it, or recommend it.

This skill is for static evidence-backed auditing only. It does not execute code, install dependencies, or run hooks in the target repository.

Maintainer-only validation and benchmark assets are excluded from ClawHub uploads.

## Scope

- Included:
  - deterministic repository audit through `evaluate` / `scan`
  - prompt payload generation through `prompt`
  - evidence-linkage checks through `validate`
  - context-aware merge flow through `adjudicate`
- Not included:
  - code execution inside the target repository
  - dependency installation or hook execution in the target repository
  - benchmark helper workflows as the normal published runtime path

## Working directory

Run these commands from inside the `skill-audit` folder.

## Requirements

- Hard requirement: `python3`
- Optional enhancement: `git` for commit metadata and GitHub-origin discovery
- Optional enhancement: `GITHUB_TOKEN` for higher GitHub API rate limits

## Core commands

Installed entrypoint:

```bash
skill-audit evaluate --target-repo /path/to/repo --json > /tmp/skill_scan.json
skill-audit prompt --target-repo /path/to/repo --scan-file /tmp/skill_scan.json --include-full-findings
skill-audit validate --scan-file /tmp/skill_scan.json --assessment-file /tmp/assessment.md --json
skill-audit adjudicate --scan-file /tmp/skill_scan.json --assessment-file /tmp/adjudication.json --json
```

Repo-local wrapper:

```bash
python3 scripts/skill_safety_assessment.py evaluate --target-repo /path/to/repo --json > /tmp/skill_scan.json
python3 scripts/skill_safety_assessment.py prompt --target-repo /path/to/repo --scan-file /tmp/skill_scan.json --include-full-findings
python3 scripts/skill_safety_assessment.py validate --scan-file /tmp/skill_scan.json --assessment-file /tmp/assessment.md --json
python3 scripts/skill_safety_assessment.py adjudicate --scan-file /tmp/skill_scan.json --assessment-file /tmp/adjudication.json --json
```

Compatibility alias:

```bash
python3 scripts/skill_safety_assessment.py scan --target-repo /path/to/repo --json > /tmp/skill_scan.json
```

## Runtime notes

- `evaluate` always attempts the GitHub OSINT precheck first when the target repository has a GitHub `origin`
- `evaluate` intentionally skips target-repo `tests/` and fixture paths so the result stays focused on installable runtime surfaces
- `prompt` should follow a deterministic scan; `validate` checks model-written output against scan evidence; `adjudicate` handles context-sensitive merge decisions
- `scripts/run_repo_set.py` is a maintainer benchmark helper and is not part of the normal ClawHub runtime flow
- Use `--json` whenever you want the full deterministic report with integrity, scoring, highlights, and findings

## References

- `references/architecture.md` — package layout and scan pipeline.
- `references/prompt-contract.md` — strict prompt contract for model-assisted review.
- `references/output-contract.md` — JSON/report contract and compatibility expectations.

## When not to use

- Live execution-time safety checks for commands or operations
- Content transformation tasks that need to mask, rewrite, or restore sensitive data
- Local routing or middleware scenarios where requests must flow through a gateway
