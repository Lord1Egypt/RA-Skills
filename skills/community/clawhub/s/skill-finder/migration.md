# Migration Guide - Skill Finder

Read this guide when upgrading from older published versions.

## Breaking Changes in v1.1.3

### 1) Memory template now stores source-selection defaults

**Before:** `~/skill-finder/memory.md` tracked status, preferences, liked skills, passed skills, and domains.

**Now:** the memory file also tracks:
- `sources: both|clawhub|skills.sh`
- `integration: proactive|explicit`
- `## Source Policy`

**Migration steps:**
1. Back up the current memory file before editing:
   ```bash
   cp ~/skill-finder/memory.md ~/skill-finder/memory.md.bak 2>/dev/null || true
   ```
2. Preserve all existing sections and user notes.
3. Add missing status keys if they do not exist:
   ```markdown
   sources: both
   integration: proactive
   ```
4. Add a `## Source Policy` section if missing.
5. Ask the user which default source mode they want:
   - `both`
   - `clawhub`
   - `skills.sh`
6. Update `sources:` only after the user answers explicitly.

### 2) Setup now assumes dual-source search readiness

**Before:** the skill only described ClawHub search and could work with the older memory format.

**Now:** the skill can search both ClawHub and Skills.sh, and setup should explain both ecosystems before first use.

**Migration steps:**
1. If `~/skill-finder/` already exists, keep using the same folder.
2. Do not delete or rename existing files.
3. Optionally create `~/skill-finder/searches.md` if the user wants recent-query continuity.
4. If the workspace or AGENTS routing references the old one-source behavior, update it so the agent loads:
   - the `skill-finder` skill
   - `~/skill-finder/memory.md`

## Post-Migration Verification

- [ ] `~/skill-finder/memory.md` still contains all prior preferences and history
- [ ] `sources:` exists and matches the user's explicit choice
- [ ] `integration:` exists
- [ ] `## Source Policy` exists
- [ ] No existing data was deleted

## Cleanup Policy

- Never delete `memory.md.bak` without explicit user confirmation.
- Do not remove legacy notes that still provide value.
- Prefer additive migration over rewrite.
