---
name: publish-guide
description: Prepare and publish an OpenClaw AgentSkill to ClawHub. Use when a skill directory is ready and needs to be published, or when upgrading an already-published skill to a new version. Handles pre-publish checks (slug, meta, internationalization), publish execution, and post-publish verification.
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["clawhub"]
      }
    }
  }
---

# Skill Publisher

End-to-end workflow for publishing an AgentSkill directory to ClawHub.

---

## Pre-publish Checklist

### ☐ 1. Content Internationalization
- SKILL.md: use **English** (Agent can handle any language, but English description/tags improve search matching on ClawHub)
- Remove hardcoded local paths, usernames (e.g., `/mnt/e/Users/...`)
- Replace user-specific config with generic placeholders or discovery methods

### ☐ 2. Meta Verification
```bash
cat <skill-dir>/_meta.json
```

Check:
- `name` matches the `--slug` you'll publish with
- `version` is updated (semver)
- `tags` are accurate (affects ClawHub search)
- `description` is concise (this is what agents match against)

### ☐ 3. Slug Conflict Check
```bash
clawhub inspect <slug>
```
- Returns skill info → slug is taken
  - Yours → `publish` will overwrite/upgrade
  - Someone else's → rename slug, e.g. `my-skill` → `my-skill-v2`
- Errors "not found" → slug is available

### ☐ 4. Login
```bash
clawhub whoami
```
If not logged in:
```bash
clawhub login
```
Opens a browser for authorization.

---

## Publish

Prerequisites: `clawhub` CLI must be installed (`npm i -g clawhub`)

```bash
clawhub publish ~/.openclaw/skills/<skill> \
  --slug <slug> \
  --name "Display Name" \
  --version x.y.z \
  --tags "tag1,tag2" \
  --changelog "Release notes"
```

### Parameters

| Param | Description | Example |
|---|---|---|
| `path` | Skill directory | `~/.openclaw/skills/my-skill` |
| `--slug` | Unique identifier | `my-skill` |
| `--name` | Display name | `My Skill` |
| `--version` | Semver version | `1.0.0` |
| `--tags` | Comma-separated search tags | `logseq,notes` |
| `--changelog` | Release notes | `Initial release` |

---

## Post-publish Verification

```bash
# New versions may be hidden by security scan, wait ~60s
sleep 60

# Check published info
clawhub inspect <slug>

# Confirm search
clawhub search <slug>
```

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `Not logged in` | Not authenticated | `clawhub login` |
| `Slug is already taken` | Slug occupied by another skill | Rename slug or check ownership |
| `Skill is hidden` | Security scan in progress | Wait 60s and retry |
| `CTX_MAX_EXCEEDED` | Content too large | Trim SKILL.md, move details to `references/` |
