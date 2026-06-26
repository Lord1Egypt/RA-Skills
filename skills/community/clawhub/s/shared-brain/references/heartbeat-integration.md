# Heartbeat Integration

Add this block to `HEARTBEAT.md` under the curation section (or `sb-install.sh` does it automatically):

```markdown
## Shared Brain Curation (every heartbeat)
```bash
~/clawd/skills/shared-brain/scripts/sb-curate.sh
```
- Merges shared-brain-queue.md → shared-brain.md (last-write-wins per key)
- Reports conflicts → TARS resolves manually
- Archives oldest section if brain > 8KB
```

## Conflict Resolution

When `sb-curate.sh` reports a conflict:

1. Two agents wrote different values for the same key
2. TARS reads both values, determines which is correct
3. Write the correct value to queue: `sb-write.sh SECTION "key = correct-value"`
4. Run curate again: `sb-curate.sh`

Example conflict output:
```
⚠️  CONFLICTS DETECTED:
  CONFLICT [INFRA] deploy:crimsondesert: was 'Coolify' → now 'Vercel' (by dev at 2026-03-22 10:15 UTC)
```

Resolution: Vercel is correct → no action needed (last-write-wins already applied the correct value).

## Section Load by Agent Role

| Agent | Sections to load |
|-------|-----------------|
| dev, qa | `[INFRA]` `[PROJECTS]` |
| security | `[INFRA]` `[SECURITY]` |
| growth, pm, po | `[PROJECTS]` `[DECISIONS]` `[CAMPAIGNS]` |
| seo, analytics | `[PROJECTS]` `[CAMPAIGNS]` |
| tars main | all sections |

To load only relevant sections (reduces context tokens ~60%):

```bash
# In AGENTS.md startup block:
awk '/^\[INFRA\]/{p=1} /^\[PROJECTS\]/{p=1} /^\[DECISIONS\]/{p=0} p' ~/clawd/memory/shared-brain.md
```

Or simply `cat` the full file if brain is <2KB — it's fast enough.

## Maintenance

- **Brain file grows too large** → `sb-curate.sh` auto-archives; or manually: `mv shared-brain.md shared-brain-archive-$(date +%Y-%m).md && sb-install.sh`
- **Queue has bad format entries** → `cat ~/clawd/memory/shared-brain-queue.md` to inspect; delete malformed lines manually
- **Agent writing wrong section** → check the `SB_AGENT` env var or the `AGENTS.md` write examples
