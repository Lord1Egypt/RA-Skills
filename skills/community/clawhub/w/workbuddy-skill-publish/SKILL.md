---
name: skill-publish
description: >
  Audit and publish agent skills to ClawHub and GitHub.
  Scans for personal data, validates frontmatter, enforces bilingual docs,
  removes internal-only content, and pushes clean distributions.
  Trigger keywords: publish skill, audit skill, 发布skill, 检查发布, skill发布, push to clawhub.
version: 1.0.1
read_when:
  - "publish skill"
  - "audit skill"
  - "发布skill"
  - "检查发布"
  - "skill发布"
  - "push to clawhub"
  - "sync to clawhub"
  - "clean publish"
---

# Skill Publish

> Audit, clean, and publish agent skills to ClawHub and GitHub.
> Complements `skill-design-guide` (design-time) with publish-time rules. Works with any SKILL.md-based skill in the OpenClaw ecosystem.

## Overview

Local skill directories often contain personal scripts, internal notes, and ticker-specific code that should never appear in public distributions. This skill standardizes the audit → cleanup → publish → verify pipeline.

**Two modes**: `audit` (scan only, no changes) or `publish` (audit + clean + push).

## Workflow

### Mode: Audit (default when user says "check" or "audit")

### Step 1: [Deterministic] Confirm Target

- Identify the skill directory to audit. If user didn't specify, ask.
- Verify SKILL.md exists at `<dir>/SKILL.md`.
- If missing, stop: "Not a skill directory — no SKILL.md found."

### Step 2: [Deterministic] Load Rules

- Read `references/publish-rules.md` for detailed validation criteria.

### Step 3: [Deterministic] Scan Files

For each file in the skill directory (recursive), check:

| Scan | What To Flag |
|------|-------------|
| **Personal data** | Ticker symbols with share counts, cost basis, account values, personal names/emails |
| **Ticker-specific code** | Scripts or configs hardcoded to single tickers (e.g. `check_tsla_entry.py`) |
| **Internal dev notes** | "审计清理版", "next N months: no new rules", personal reminders |
| **Meta-documents** | Files like `SKILL_PUBLISH_RULES.md` that aren't part of the skill itself |
| **Old version files** | `Q2_2026_交易策略.md` — outdated strategy docs |

### Step 4: [LLM] Validate SKILL.md Content

Read the full SKILL.md. Check:

| Check | Rule |
|-------|------|
| Frontmatter `name` | No version number embedded |
| Frontmatter `description` | ≤3 sentences, English, no tickers/versions/keywords |
| H1 title | No version number |
| `## 详细参考` / `## References` section | Must NOT exist |
| Version history | Only published versions, max 5 rows, no "planned" entries |
| Internal dev notes | Must be absent from body text |
| Language | Body is English (a Chinese summary paragraph at end is OK) |

### Step 5: [Deterministic] Validate Bilingual Docs

- `README.md` exists and is in English
- `README_zh.md` exists and is in Chinese
- Version numbers in both README files match
- `CONTRIBUTING.md` exists and is in English (if present)

### Step 6: [Deterministic] Generate Audit Report

Output format:

```
## Skill Publish Audit: <skill-name>

### Issues Found

| # | Severity | File | Issue |
|---|----------|------|-------|
| 1 | HIGH | SKILL.md | description 含版本号和关键词列表 |
| 2 | HIGH | SKILL.md | H1 标题带版本号 |
| 3 | MEDIUM | check_tsla_entry.py | 个股脚本，不应发布 |
| 4 | LOW | SKILL.md | 版本历史含未发布版本 |

### Clean Files (safe to publish)
- SKILL.md (after fixes above)
- README.md ✓
- README_zh.md ✓
- references/*.md (3 files) ✓
- scripts/*.py (8 files) ✓

### Action Required Before Publish
- [ ] Fix issue #1: rewrite description
- [ ] Fix issue #2: remove version from H1
- [ ] Fix issue #3: exclude check_tsla_entry.py
- [ ] Fix issue #4: trim version history
```

Stop here in audit mode. User reviews and decides next step.

### Mode: Publish (when user says "publish" or confirms audit)

### Step 7: [LLM] Fix Content Issues

Apply all fixes identified in the audit:
- Rewrite frontmatter description (≤3 English sentences)
- Strip version from H1 title
- Remove `## 详细参考/References` section
- Trim version history to 5 published versions max
- Remove internal dev notes throughout

Write fixed content to SKILL.md, README.md, README_zh.md as needed.

### Step 8: [Deterministic] Prepare Clean Directory

1. Create temp dir: `<skill-dir>-publish/`
2. Copy only whitelisted files:
   - `SKILL.md`, `README.md`, `README_zh.md`
   - `CONTRIBUTING.md`, `LICENSE` (if exist)
   - `references/` (all `.md` files)
   - `scripts/` (all `.py` files — filters out personal scripts)
   - `requirements.txt`, `_meta.json`
3. Verify: NO ticker-specific scripts, NO personal files, NO meta-documents in temp dir.

### Step 9: [Deterministic] Determine Version

- Read `_meta.json` for current published version
- If user specified a version, validate it's higher than current
- If no version specified, ask user for target version
- Generate changelog summary from audit fixes

### Step 10: [Deterministic] Push to ClawHub

```bash
clawhub publish <clean-dir> --slug <slug> --version <version> --changelog "<summary>"
```

- If "Version already exists": bump patch version and retry
- If network error: report and stop
- On success: capture new version and publish ID

### Step 11: [Deterministic] Push to GitHub

For each whitelisted file:
1. GET `https://api.github.com/repos/<owner>/<repo>/contents/<path>` → get SHA
2. PUT with base64 content + SHA (or POST if new file)

For files to delete (from audit list):
- DELETE with SHA

Use the GitHub PAT from `~/.workbuddy/connectors/<id>/tokens/github.txt`.

### Step 12: [Deterministic] Verify

```
[ ] clawhub inspect <slug> → latest version matches, English description
[ ] GitHub repo: correct files present, no personal scripts
[ ] Clean temp dir deleted
```

## Hard Rules

> These cannot be violated.

1. **Never modify local files.** All fixes go to temp publish directory. Local stays intact.
2. **Never publish without audit.** Every file must be scanned before reaching ClawHub/GitHub.
3. **Personal data is a blocking error.** Any finding of account values, share counts, cost basis → must be resolved before publish.
4. **No version in name.** `name` field and H1 title must never contain version numbers.
5. **English-first SKILL.md.** Body text must be English. Chinese summary at end is optional.
6. **Temp dir must be deleted** after successful publish.

## Failure Handling

| Scenario | Action |
|----------|--------|
| SKILL.md not found | Stop: "Not a skill directory" |
| Personal data found | Block publish; report exact file+line; user must manually remove |
| ClawHub auth missing | Guide: "Run `clawhub login --token <token>`" |
| Version already exists | Auto-bump patch version; ask user to confirm |
| GitHub PAT not found | Guide: "Ensure GitHub connector is active" |
| GitHub write fails (403) | Report: "Token lacks write permission on this repo" |
| Network timeout | Retry once; if still fails, report and stop |
| User cancels mid-publish | Clean up temp dir, report: "Publish aborted, local files untouched" |

## Output Format

### Audit Mode Output
```
## Skill Publish Audit: <name> v<version>

### Issues (N found)
[table: severity, file, issue, fix]

### Clean Files (M files, K KB)
[file list]

### Publish Target
- ClawHub: <owner>/<slug>
- GitHub: <owner>/<repo>
- Version: <current> → <target>
```

### Publish Mode Output
```
## Publish Complete: <name>@<version>

### ClawHub
- URL: https://clawhub.ai/<owner>/<slug>
- Version: <version>
- Publish ID: <id>

### GitHub
- Repo: <owner>/<repo>
- Commit: <sha>
- Files: <N> updated, <M> deleted
```
