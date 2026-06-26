# ClawHub Deployment Checklist

> Based on: community gist (adhishthite, 13-point checklist from 6 iterations)  
> + openclaw/clawhub README  
> + docs.openclaw.ai/tools/clawhub

---

## Pre-flight: SKILL.md Frontmatter

ClawHub parses the YAML frontmatter in `SKILL.md`. These fields matter:

```yaml
---
name: self-evolving-agent          # ✅ Must match folder name (lowercase, hyphens)
version: 2.0.0                     # ✅ Semver
description: "One-line description visible in search results"
homepage: https://github.com/...   # ✅ Reduces suspicion score in security scan
metadata:
  clawdbot:                        # ✅ Use clawdbot (NOT openclaw — ClawHub ignores that)
    emoji: "🧠"
    requires:
      env: []                      # List any required env vars
      files: ["scripts/*"]         # ✅ Declare scripts exist (avoids "instruction-only but has scripts" flag)
---
```

**Critical gotchas (from community research):**
- ❌ `metadata.openclaw` → ClawHub ignores this key
- ✅ `metadata.clawdbot` → This is what ClawHub actually parses
- ❌ `requires.envs` → Wrong field name
- ✅ `requires.env` → Correct (array)
- ✅ `homepage` field → Provides provenance, lowers security suspicion score

---

## Security Checklist (Clawdex Scan)

ClawHub uses Clawdex (VirusTotal partnership since 2026-02) to auto-scan submitted skills.

### Script Headers — Security Manifest Required

Every `.sh` file must include a security manifest comment:

```bash
# SECURITY MANIFEST:
# Environment variables accessed: none
# External endpoints called: none
# Local files read: ~/.openclaw/sessions/* (read-only)
# Local files written: ~/openclaw/skills/self-evolving-agent/data/
```

### Shell Injection Prevention

```bash
# ❌ Bad — RCE via $(cmd) or backticks in USER_INPUT
curl "https://api.com/${USER_INPUT}"

# ✅ Safe — sanitize before interpolation
SAFE_INPUT=$(printf '%s' "$INPUT" | python3 -c \
  'import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read().strip(), safe=""))')
curl "https://api.com/${SAFE_INPUT}"
```

### Shell Best Practices (Required for Clawdex pass)

- ✅ `set -euo pipefail` at top of every script
- ✅ Check env vars exist before using: `${VAR:?VAR is required}`
- ✅ Validate input arguments
- ✅ Proper error handling with exit codes
- ✅ No `eval` with user-supplied data

---

## SKILL.md Content Sections

ClawHub requires (or strongly recommends) these sections in the skill body:

| Section | Required? | What to Include |
|---|---|---|
| **External Endpoints** | ✅ Required | Table of every URL called + what data is sent |
| **Security & Privacy** | ✅ Required | What leaves the machine, what stays local |
| **Model Invocation Note** | ✅ Required | Explain any autonomous LLM calls; provide opt-out |
| **Trust Statement** | ✅ Required | "By using this skill, data is sent to X. Only install if..." |
| **Installation** | Recommended | Step-by-step setup |
| **Configuration** | Recommended | All config.yaml options |
| **Works Well With** | Recommended | Complementary skills |

---

## File Structure Requirements

```
self-evolving-agent/
├── SKILL.md          ✅ Required — skill definition
├── README.md         ✅ Required — shown on ClawHub page
├── LICENSE           ✅ Required — MIT recommended
├── config.yaml       Optional — user configuration
└── scripts/          Optional — declare in metadata.clawdbot.requires.files
```

**Do NOT include:**
- `node_modules/`, `__pycache__/`, `.venv/`
- `.env` files with secrets
- Large binary files (>10MB total repo limit)
- Any file that phones home without disclosure

---

## Submission Steps

### Option A: ClawHub UI (Recommended for first publish)

1. Go to https://clawhub.ai
2. Sign in with GitHub (use the account that owns the repo)
3. Click "Publish Skill"
4. Enter repo URL: `https://github.com/YOUR_USERNAME/self-evolving-agent`
5. Select version tag (create a git tag first: `git tag v2.0.0`)
6. Submit for review

**Review timeline:** ~24-48h for new publishers, faster after first approval.

### Option B: openclaw/skills PR (Community registry)

```bash
# Fork https://github.com/openclaw/skills
# Add your skill under: skills/YOUR_USERNAME/self-evolving-agent/
# Structure:
skills/YOUR_USERNAME/self-evolving-agent/
├── SKILL.md         (symlink or copy)
└── metadata.json    (ClawHub registry metadata)

# Submit PR to openclaw/skills main branch
```

### Option C: clawdhub CLI

```bash
clawdhub login
clawdhub publish --path ./self-evolving-agent --tag v2.0.0
```

---

## Pre-submission Validation

Run these checks before submitting:

```bash
# 1. ShellCheck — must pass with zero warnings
shellcheck scripts/*.sh scripts/lib/*.sh

# 2. SKILL.md frontmatter — required fields present
grep -E "^name:|^description:|^version:" SKILL.md

# 3. Security manifest in every script
for f in scripts/*.sh; do
  grep -l "SECURITY MANIFEST" "$f" || echo "⚠️ Missing manifest: $f"
done

# 4. No secrets accidentally committed
git log --all --full-history --diff-filter=D -- .env 2>/dev/null
grep -r "DISCORD_TOKEN\|OPENAI_KEY\|SECRET" . --include="*.sh" --include="*.yaml" | grep -v config.yaml

# 5. README.md has required sections
for section in "External Endpoints" "Security" "Trust"; do
  grep -q "$section" README.md || echo "⚠️ Missing section: $section"
done
```

---

## Post-publish

- [ ] Create `v2.0.0` git tag: `git tag v2.0.0 && git push --tags`
- [ ] Verify ClawHub page renders correctly at `https://clawhub.ai/YOUR_USERNAME/self-evolving-agent`
- [ ] Check that tags are searchable: search `self-improvement` on ClawHub
- [ ] Submit to `awesome-openclaw-skills` repo (separate PR)
- [ ] Post to r/OpenClaw (see GTM strategy doc)
- [ ] Reach out to complementary skill authors about cross-recommendation

---

## Version Bump Process

For future updates:
```bash
# Edit SKILL.md version field
# Commit: "chore: bump version to v2.1.0"
git tag v2.1.0
git push && git push --tags
# ClawHub auto-detects new tags (if webhook configured)
# Or: manually trigger via clawdhub publish --tag v2.1.0
```
