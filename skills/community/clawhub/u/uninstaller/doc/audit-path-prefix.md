# Path Prefix Audit — Wander & openclaw-uninstall

Systematic audit of path/namespace/prefix issues across both repos.

---

## 1. openclaw-uninstall: skr/ghcr.io

### Symptom

```
Push failure: invalid reference ghcr.io/ERerGB/uninstaller:latest: invalid repository "ERerGB/uninstaller"
Push failure: invalid reference ghcr.io/ERerGB/.:latest: invalid repository "ERerGB/."
```

### Root cause

- **path: .** — skr scans repo root and finds multiple skills:
  1. Root (`.` has SKILL.md) → skill name `"."` → `ghcr.io/ERerGB/.`
  2. `.github/skills/uninstaller/` → skill name `"uninstaller"` → `ghcr.io/ERerGB/uninstaller`
- **namespace: github.repository_owner** → `ERerGB`
- ghcr.io format: `ghcr.io/OWNER/REPO:tag`. REPO must be valid (lowercase, no dots, etc.)
- `ERerGB/.` is invalid (`.`)
- `ERerGB/uninstaller` — may fail if ghcr.io expects repo name `openclaw-uninstall` for this repo

### Fix (implemented)

- **path: ./skill-dist** — Single skill at `skill-dist/openclaw-uninstall/SKILL.md` (symlink to root)
- skr publishes `ghcr.io/ERerGB/openclaw-uninstall` (dir name = image name)
- **SSOT**: Root `SKILL.md` is canonical. `.github/skills/uninstaller/SKILL.md` and `skill-dist/openclaw-uninstall/SKILL.md` are symlinks. No sync script.
- Personal: `./scripts/install-personal.sh` creates `~/.cursor/skills/uninstaller` → repo

---

## 2. Wander: path resolution

### Current resolution order

| Source | Logic | Example |
|--------|-------|---------|
| WANDER_HOME | Env var | `~/code/wander` |
| WANDER_DIR | Env var | Override |
| Sibling | `$(dirname $REPO_ROOT)/wander` | openclaw-uninstall at `~/code/openclaw-uninstall` → `~/code/wander` |

### Potential issues

| Scenario | REPO_ROOT | WANDER_DIR (sibling) | Works? |
|----------|-----------|---------------------|--------|
| Standard | `~/code/openclaw-uninstall` | `~/code/wander` | ✓ |
| Nested | `~/projects/x/openclaw-uninstall` | `~/projects/x/wander` | ✗ if wander not there |
| Worktree | `~/code/fulmail/.worktrees/openclaw-uninstall` | `~/code/fulmail/.worktrees/wander` | ✗ |

### Skill doc vs implementation

- Skill: "Default: ~/code/wander" — but project wrappers use **sibling**, not `~/code/wander`
- When WANDER_HOME is set (e.g. by install-personal.sh), sibling is ignored ✓
- When not set: sibling is used. If user has wander at `~/code/wander` and repo elsewhere, fails.

### Recommendation

- Document: "WANDER_HOME overrides sibling. Set WANDER_HOME for personal install."
- No code change needed; resolution order is correct.

---

## 3. openclaw-uninstall: .gitignore skills/

### Issue

- `.gitignore` has `skills/` → ignores any `skills/` dir
- `.github/skills/` was ignored until we added `!.github/skills/`
- Root cause: `skills/` is too broad (matches `.github/skills/`)

### Fix

- Use `/skills` to only ignore root-level `skills/` (ClawHub local installs)
- Remove `!.github/skills/` — `.github/skills/` would no longer match

```gitignore
# ClawHub installs (root-level only)
/skills/
```

---

## 4. Summary

| Repo | Issue | Severity | Status |
|------|-------|----------|--------|
| openclaw-uninstall | skr path finds 2 skills, invalid ghcr refs | P0 | ✅ Fixed: path: ./skill-dist |
| openclaw-uninstall | .gitignore skills/ too broad | P1 | ✅ Fixed: /skills/ |
| openclaw-uninstall | Doc: ghcr install path wrong | P2 | ✅ Aligned: ghcr.io/ERerGB/openclaw-uninstall |
| Wander | Sibling path fails when wander elsewhere | P2 | Doc: set WANDER_HOME |

---

## 5. Next steps

1. ~~**skr fix**~~ — Done: `skill-dist/openclaw-uninstall/` + `path: ./skill-dist`
2. ~~**.gitignore**~~ — Done: `/skills/`
3. **Wander skill**: Add note about WANDER_HOME for non-sibling layouts
