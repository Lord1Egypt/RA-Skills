---
name: skill-index
description: "Auto-scan all installed skills, generate a categorized INDEX.md, and keep it in sync via git hooks. Triggers: skill index, scan skills, update index, skill catalog, manage skill list, skill inventory."
---

# Skill Index

Auto-scan every SKILL.md under `skills/`, extract metadata, categorize, and produce a single searchable INDEX.md. Git hooks keep the index fresh on every commit and pull.

## Problem It Solves

As skill count grows past 20+, finding the right one becomes painful — especially for the AI agent that must read descriptions at startup. Manual lists go stale fast.

Skill Index solves this by:

- **One command** → complete, up-to-date inventory
- **Zero maintenance** → git hooks auto-update on commit/pull
- **Instant lookup** → AI reads INDEX.md instead of crawling the whole directory

## Quick Start

### Manual scan
```bash
bash skills/skill-index/register.sh
```

### Install git hooks (one-time)
```bash
bash skills/skill-index/install-hooks.sh
```

After that, INDEX.md updates automatically whenever you commit or pull.

## How It Works

1. **Scan** — Recursively find all `SKILL.md` files under `skills/`
2. **Extract** — Parse YAML frontmatter: `name`, `description`, relative path
3. **Categorize** — Smart matching by directory structure + description keywords
4. **Generate** — Write `skills/INDEX.md` as a categorized Markdown table

## Output Format

```markdown
# Skills Index
> Auto-generated. Run `bash skills/skill-index/register.sh` to update.

## Category Name
| Skill | Path | Trigger |
|-------|------|---------|
| my-skill | path/to/SKILL.md | Description preview... |
```

## Customization

### Adding categories

Edit the `categorize()` function in `register.sh` to add your own rules:

```bash
    *your-keyword*) echo "Your Category"; return ;;
```

### Excluding skills

Add the skill's directory to the `find` exclusion list in `register.sh`:

```bash
find "$SKILLS_DIR" -name "SKILL.md" -not -path "*/skill-index/*" -not -path "*/your-private-skill/*"
```

## Requirements

- Bash 4+
- Git (for hooks)
- OpenClaw workspace with `skills/` directory

## License

MIT
