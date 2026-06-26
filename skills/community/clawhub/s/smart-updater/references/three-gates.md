# Three Gates — Detailed Reference

## Gate 1: Pre-flight (能不能升)

| Check | Rule | On Fail |
|-------|------|---------|
| Source tracked | Must be npm/clawhub/github (not `local`) | Skip, mark `untracked` |
| No name conflict | No other asset with same name but different source | Block upgrade |
| Gateway healthy | Extensions only: `openclaw gateway status` all green | Block, fix first |

## Gate 2: Isolation (不污染环境)

### Backup Paths (MUST be outside scanner paths)

| Type | Backup To | ⚠️ Never |
|------|-----------|----------|
| Skill | `~/.openclaw/skill-backups/<name>-<ver>-<ts>/` | Never in `skills/` |
| Extension | `~/.openclaw/extensions-backup/<name>-<ver>/` | Never in `extensions/` |
| Core | `~/.openclaw/plist-backup/` + `openclaw backup create` | — |

### Type-Specific Steps

**Extension** (high risk):
1. Backup → extensions-backup/
2. `rm -rf /tmp/jiti/` (mandatory — jiti caches compiled TS)
3. `npm install <pkg>@latest`
4. `find extensions/ -maxdepth 1 -name "*.bak*" -type d -exec rm -rf {} +`

**Core**:
1. Backup plist + `openclaw backup create`
2. `npm update -g openclaw`
3. `openclaw gateway install` (regenerates plist)
4. Diff old vs new plist → restore custom env vars (API keys, ports)

**Skill**: Backup → skill-backups/, then `clawhub update` or `git pull`

## Gate 3: Post-flight (验证)

| Type | Pass Criteria | Fail Action |
|------|--------------|-------------|
| Skill | SKILL.md exists + file count ≥ old version | Rollback from backup |
| Extension | `gateway restart` → log has `plugin registered`, no `duplicate plugin id` → `gateway status` all green | Rollback + clear jiti + restart |
| Core | `openclaw --version` new + `gateway status` all green + extensions loaded | `npm install openclaw@<prev>` + restore plist + restart |

Optional: If new version added executable `scripts/`, flag for `skill-vetter`.

## Rollback Commands

```bash
# Skill
cp -r ~/.openclaw/skill-backups/<name>-<ver>-<ts>/ ~/.openclaw/workspace/skills/<name>/

# Extension
cp -r ~/.openclaw/extensions-backup/<name>-<ver>/ ~/.openclaw/extensions/<name>/
rm -rf /tmp/jiti/
openclaw gateway restart

# Core
npm install -g openclaw@<previous-version>
cp ~/.openclaw/plist-backup/ai.openclaw.gateway.plist ~/Library/LaunchAgents/
openclaw gateway restart
```
