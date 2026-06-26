# Publish Rules for ClawHub & GitHub

> Full rule reference loaded by the `skill-publish` workflow. Do not embed this in SKILL.md.

---

## 1. Frontmatter Requirements

| Field | Rule | Why |
|-------|------|-----|
| `name` | Pure English slug, **no version number**. e.g. `invassistant` not `invassistant-v2` | ClawHub display name; version belongs in changelog |
| `description` | ≤3 sentences, English only. No version numbers, stock tickers, keyword lists, or changelogs | ClawHub card + search summary |
| `metadata.openclaw.tags` | 5-10 English tags | ClawHub category system |
| `metadata.openclaw.requires.bins` | Declare required binaries (e.g. `python3`) | ClawHub security analysis |

**Bad**:
```yaml
description: |
  个人投资组合管理框架 v2.1.1（执行简化版）。覆盖 A 股、港股、美股。
  新增 §7.4 模式 D...
  触发关键词：检查持仓, COST, LLY...
```

**Good**:
```yaml
description: >
  Multi-asset investment portfolio management framework.
  A/B/C-class differentiated rules, 7 red-line risk controls.
  Covers US, A-share, and HK stocks.
```

## 2. Content Cleanup

### Must Remove
- `## 详细参考` / `## References` section (lists internal file paths — meaningless to users)
- Unreleased versions in version history (e.g. "v3.0 planned 2027")
- Internal dev notes ("审计清理版", "next 6-12 months: no new rules")
- Ticker-specific entry scripts (e.g. `check_tsla_entry.py`) — exposes personal holdings
- Meta-documents not part of the skill (e.g. `SKILL_PUBLISH_RULES.md`)

### Version History
- Only published versions (available on ClawHub)
- One sentence per version
- Max 5 rows

## 3. Language

| File | Language |
|------|----------|
| `SKILL.md` | English body + optional Chinese intro paragraph at end |
| `README.md` | English |
| `README_zh.md` | Chinese (mirror of English README) |
| `CONTRIBUTING.md` | English |
| All `references/*.md` | English |

## 4. File Separation: Local vs Published

Files that stay **local only** (never push to GitHub or ClawHub):
- Ticker-specific scripts (`check_tsla_entry.py`, `check_detail.py`, etc.)
- Personal config files (`*-config.json` with real credentials)
- Meta-documents (`SKILL_PUBLISH_RULES.md`)
- Session-specific notes or logs
- `.git/` directory

Files that go to **both platforms**:
- `SKILL.md`, `README.md`, `README_zh.md`
- `CONTRIBUTING.md`, `LICENSE`, `requirements.txt`
- `references/` (all `.md`)
- `scripts/` (only generic, reusable engines)

Files for **ClawHub only** (not GitHub):
- `_meta.json`

## 5. Publish Mechanics

### ClawHub
```bash
clawhub publish <clean-dir> --slug <slug> --version <semver> --changelog "<one-liner>"
```
- Requires prior `clawhub login --token <token>` (persists to session)
- Version must not already exist on ClawHub
- If overriding `latest` tag, version number must be higher than current latest

### GitHub
Use GitHub API with PAT for file operations. 
- Get file SHA → PUT with base64 content + SHA
- New files: PUT without SHA
- Delete: DELETE with SHA

### Optimal strategy
1. Create clean temp directory (copy whitelisted files only)
2. Publish to ClawHub from temp dir (avoids leaking local files)
3. Push individual files to GitHub via API
4. Delete temp dir
5. Verify both platforms

## 6. Post-Publish Verification

```
[ ] clawhub inspect shows correct latest version + English description
[ ] ClawHub card description is English, ≤3 sentences
[ ] ClawHub display name has no version number
[ ] Version history shows only published versions (≤5)
[ ] SKILL.md has no "详细参考/References" section
[ ] SKILL.md has no internal dev notes
[ ] README.md + README_zh.md both exist, versions match
[ ] GitHub repo has no ticker-specific scripts
[ ] GitHub repo has no personal config files
[ ] GitHub commit message matches changelog
```
