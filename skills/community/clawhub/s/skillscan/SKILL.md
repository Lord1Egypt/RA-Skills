---
name: SkillScan
metadata:
  version: "1.1.6"
description: >
  Security gate for skills. Every new skill MUST pass SkillScan before use.
  Activate on any install, load, add, evaluate, or safety question about a skill.
  On first load, run first-run to scan all existing skills.
  Blocks HIGH/CRITICAL skills. No exceptions.
---

# SkillScan v1.1.6

Security check for skill packages. Every new skill must pass this scan before use.

Implemented in `scripts/scanner.py`. Supports Windows / macOS / Linux.

Do NOT generate report files inside the skill directory.

---

## When to Activate

Run SkillScan whenever a skill is installed, loaded, added, evaluated, or questioned for safety — regardless of method or phrasing.

Trigger examples: install, load, add, use, set up, "is this safe", upload .zip/.skill, paste SKILL.md, mention unknown skill name, install from hub/store.

---

## First Load

Check `scripts/.first_run_done`:

- **Not found** → **Tell user** SkillScan is installed, ask to scan all existing skills:
  ```bash
  python <skill_scanner_dir>/scripts/scanner.py first-run
  ```
  `.first_run_done` is created automatically after completion.

- **Found** → Skip, operate normally.

---

## Commands

| Command | Usage |
|---------|-------|
| `scanner.py scan <path>` | Scan a single skill (.zip or directory) |
| `scanner.py scan-all` | Scan all installed skills |
| `scanner.py first-run` | First-time full scan |
| `scanner.py upgrade` | Manual upgrade |

---

## Scan Rules

- **.zip files** → Scan BEFORE installation. Block if fails.
- **Directory installs** (cp, mv, git clone, ln -s, any method) → Scan AFTER files land on disk.
- **Remote installs** (clawhub, skillhub, npx skills add, etc.) → Scan immediately after install.
- **Unknown skills** → If user mentions a skill you haven't seen, scan it.

---

## Exit Codes

| Code | Verdict | Action |
|------|---------|--------|
| `0` | UNKNOWN / SAFE  | Proceed |
| `1` | LOW / MEDIUM | Warn user, ask to confirm |
| `2` | HIGH / CRITICAL | Block, show details |
| `3` | Scan failed | Explain, offer retry |

---

## Auto Update

Checks for updates every day automatically. Silent, no user action needed. Manual: `scanner.py upgrade`.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SKILL_SCANNER_UPDATE_URL` | Custom update source (optional) |

---

## API

Base URL: `https://skillscan.tokauth.com`

| Step | Method | Path |
|------|--------|------|
| ① Cache lookup | GET | `/oapi/v1/skill-scan/search?dir_sha256=<dir_sha256>` |
| ② Upload | POST | `/oapi/v1/skill-scan/upload` |
| ③ Poll result | GET | `/oapi/v1/skill-scan/result?task_no=<task_no>` (poll every 20s, max 180s) |
