# Skill Dedup

Find user skills that duplicate plugin skills and offer cleanup options.

## When to Use

- After installing new plugins
- Periodic skill inventory cleanup
- Before creating new skills (check if already exists)

## Workflow

### Step 1: Get User Skill Names

```bash
ls ~/.claude/skills/ | grep -v '\.bak$'
```

Extract skill names from frontmatter:
```bash
grep -h "^name:" ~/.claude/skills/*/SKILL.md 2>/dev/null | sed 's/name: *//' | sort -u
```

### Step 2: Get Plugin Skill Names

```bash
grep -rh "^name:" ~/.claude/plugins/marketplaces/*/plugins/*/skills/*/SKILL.md 2>/dev/null | sed 's/name: *//' | sort -u
```

### Step 3: Find Duplicates

Compare the two lists. A duplicate is when user skill name matches plugin skill name.

### Step 4: Present Results

Show duplicates in a concise table:

| User Skill | Plugin | Status |
|------------|--------|--------|
| skill-name | plugin:skill-name | Backup recommended |
| other-skill | plugin:other-skill | Already backed up |

If already in `.bak`: mark as "Already backed up"

### Step 5: Offer Cleanup

Use AskUserQuestion for duplicates not yet backed up:

```
Backup these duplicate skills to .bak folder?
1. Backup All (Recommended) - Move to ~/.claude/skills/.bak/
2. Select Individually - Choose which to backup
3. Keep All - No changes
```

### Step 6: Execute Backup

```bash
mkdir -p ~/.claude/skills/.bak
mv ~/.claude/skills/{duplicate-skill} ~/.claude/skills/.bak/
```

### Step 7: Report

```
## Deduplication Complete

| Item | Count |
|------|-------|
| Skills checked | X |
| Duplicates found | Y |
| Backed up | Z |
| Unique skills | N |
```

## Additional Checks

### Similar Names

Also check for similar (not exact) matches:

| User Skill | Plugin | Similarity |
|------------|--------|------------|
| git-commit | plugin:commit-helper | Name overlap |
| k8s-debug | plugin:kubernetes-debug | Same purpose |

Recommend review or merge.

### Orphaned Backups

Check `.bak/` folder for old backups:

```bash
ls ~/.claude/skills/.bak/
```

Offer cleanup:
```
Clean up old backup folders?
1. Delete All (Recommended) - Remove ~/.claude/skills/.bak/*
2. Keep - Preserve for recovery
```

## Integration with Lint

When running `/skill-manager lint`:

If duplicates detected during scan:
```
💡 Found 3 potential duplicates with plugins.
   Run dedup? /skill-manager dedup
```

## Notes

- Backups go to `~/.claude/skills/.bak/`
- Plugin skills take precedence (maintained upstream)
- User customizations should be merged into project skills
- Review backup folder periodically
