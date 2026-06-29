---
name: skills-audit
description: >
  Audit all installed skills to identify duplicates, platform-mismatched skills,
  and maintenance candidates. Use when: (1) the user asks to "clean up skills",
  "check for duplicate skills", "audit installed skills", or "find skills to remove";
  (2) performing periodic skill maintenance; (3) investigating skill clutter or
  skill conflicts. Scans all SKILL.md files in ~/.workbuddy/skills/, compares
  against a golden list of approved skills, classifies each as approved / unknown /
  platform-specific, and generates a structured audit report.
---

# Skills Audit

Audit all installed WorkBuddy skills, classify them, and generate a cleanup report.

## Workflow

### 1. Run the audit script

```bash
python scripts/audit_skills.py
```

This scans `~/.workbuddy/skills/`, reads each SKILL.md, and generates a `skills-audit-YYYY-MM.md` report.

Options:
- `--dir <path>` — custom skills directory (default: `~/.workbuddy/skills/`)
- `--golden <path>` — custom golden list (default: `references/golden-list.md`)
- `--output <path>` — custom report output path

### 2. Interpret the report

The report classifies each skill into one of three categories:

| Status | Meaning | Action |
|--------|---------|--------|
| [OK] Approved | Matches the golden list | Keep |
| [!] Review | Not in golden list, not platform-specific | Manually review |
| [X] Platform: <name> | Designed for Clawdbot/Moltbot/OpenClaw | Candidate for removal |

### 3. Present findings to user

Use `present_files` to show the report. For platform-specific or unknown skills,
flag them and ask the user for confirmation before removing.

### 4. Remove redundant skills (after user confirmation)

```bash
rm -rf ~/.workbuddy/skills/<skill-dir>
```

## Classification Rules

1. **Golden list match**: If the skill name or directory matches an entry in `references/golden-list.md`, it is Approved.
2. **Platform detection**: SKILL.md is scanned for keywords (`clawdbot`, `moltbot`, `openclaw`, `clawhub`, `CodeConductor.ai`). If found and not in golden list, it is flagged as platform-specific.
3. **Otherwise**: Classified as Unknown — requires manual review.

## Bundled Resources

- `scripts/audit_skills.py` — Python script that performs the scan and generates the report
- `references/golden-list.md` — Canonical list of approved skills (edit this to add/remove approved skills)
