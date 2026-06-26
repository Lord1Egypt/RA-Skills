---
name: skill-install-guard
description: Guard OpenClaw skill installation with a productized five-step flow: source check, local-state check, mandatory all-files review, risk review, install execution, and post-install verification. Use this whenever installing skills from ClawHub, local folders, GitHub, or other sources and you need reliable go/no-go decisions plus verifiable outcomes.
metadata:
  short-description: 安装前审查 + 安装后验收的一体化守门流程
version: 0.4.3
---

# Skill Install Guard｜技能安装守门员

Use this skill when the user wants safer, more consistent skill installation with clear go/no-go decisions and verifiable post-install results.

## What it does

This skill enforces a fixed five-step installation guardrail:

1. **Source check**
   - Collects key source trust signals (author, activity, update freshness, public feedback when available).
   - Marks unavailable data explicitly so risk decisions stay transparent.

2. **Local-state check**
   - Detects existing local installs before action.
   - Reduces duplicate installs and path mistakes.

3. **Code review (MANDATORY)**
   - Enumerates all files in the target skill.
   - Reviews readable text files and records binary/oversize/unreadable handling with reasons.

4. **Risk review**
   - Summarizes red flags, required permissions, risk level, and final recommendation.
   - Produces human-readable conclusions and machine-readable report output.

5. **Install execution + post-install verification**
   - Runs install only when policy allows.
   - Verifies expected path and required key files after execution.

## When to use

- Before installing any unfamiliar skill from ClawHub.
- Before adopting skills from GitHub or local directories.
- When teams need consistent installation standards.
- When security-sensitive environments require auditable evidence.

## Primary command

```bash
python3 scripts/skill-install-guard.py --slug <skill-slug> [options]
```

Compatibility wrapper:

```bash
scripts/skill-install-guard.sh --slug <skill-slug> [options]
```

## Required / useful inputs

- `--slug <slug>`: required target skill slug
- `--source <source>`: optional source (`clawhub`, local path, or URL)
- `--install-cmd '<command>'`: real install command for execution phase (direct executable invocation only; no shell pipes/redirects/chaining)
- `--expected-dir <path>`: expected final install path
- `--version <version>`: optional version hint
- `--dry-run`: checks only
- `--stop-before-install`: end after review phase
- `--allow-medium-risk`: allow execution when risk is medium
- `--report-json <path>`: write machine-readable result

## Recommended operating pattern

1. Collect slug, source, intended install command, and expected final directory.
2. Run with `--stop-before-install` or `--dry-run` for non-destructive preflight.
3. Read risk summary and recommendation.
4. If blocked, stop and report why.
5. If allowed, run with actual install command.
6. Return both risk decision and post-install verification result.

## Example: non-destructive verification

```bash
python3 scripts/skill-install-guard.py \
  --slug some-skill \
  --source clawhub \
  --expected-dir skills/some-skill \
  --stop-before-install \
  --report-json tmp/skill-install-guard/some-skill-verify.json
```

## Example: real guarded install

```bash
python3 scripts/skill-install-guard.py \
  --slug some-skill \
  --source clawhub \
  --install-cmd 'clawhub install some-skill' \
  --expected-dir skills/some-skill \
  --report-json tmp/skill-install-guard/some-skill-install.json
```

## Output requirements

When using this skill, report at minimum:

- target skill name / slug
- source checked and source-data completeness
- all-files coverage summary
- red flags found (or explicit none)
- permissions needed (files / network / commands)
- risk level
- recommendation / verdict
- install command used or skipped
- final landed path check
- final go / no-go result

## Safety rules

- Do not treat command exit status as sole success criterion.
- Do not skip post-install verification.
- If slug/source/version mismatch expectations, stop before install.
- If risk recommendation is block, do not force install.
- If risk is medium without explicit operator approval, keep blocked.
- When uncertain, prefer no-go.
