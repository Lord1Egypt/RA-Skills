---
name: skill-kit
depends-on:
  - cc-plugin
  - clawhub
metadata:
  author: es6kr
  version: "0.1.2"
description: |
  Claude Code skill management. Topics — writer (create), lint (validate + fix frontmatter), merge (combine related), dedup (find duplicates), convert (agent → skill), architecture (multi-topic structure), upgrade (enhance + add topics), route (topic placement), trigger (declare + auto-register hooks), find (discover via npx skills CLI), graph (extract depends-on + topic body Skill calls into Edge Table + Mermaid + dispatched d3 force-directed render), language (per-skill language consistency enforcement), portability (public skill cross-ref + vendor isolation), publish-scope (published skill scope review before extending). Use when: "skill writer", "skill lint", "skill merge", "skill dedup", "create skill", "frontmatter fix", "multi-topic skill", "convert agent", "skill upgrade", "add topic", "topic route", "trigger compile", "hook auto register", "find skill", "discover skill", "npx skills", "skills.sh", "install skill", "skill graph", "skill dependency graph", "depends-on extract", "mermaid skill graph", "force-directed skill graph", "skill language", "description language", "portability", "publish scope".
---

# Skill-Kit

Comprehensive toolkit for creating, managing, and maintaining Claude Code skills.

## Commands

| Command | Description | Link |
| ------- | ----------- | ---- |
| architecture | Multi-topic skill structure and topics | [architecture.md](./architecture.md) |
| convert | Convert agents or scripts to skills | [convert.md](./convert.md) |
| dedup | Identify and merge duplicate skills | [dedup.md](./dedup.md) |
| find | Discover and install skills via npx skills CLI | [find.md](./find.md) |
| graph | Extract `depends-on` + topic body `Skill(...)` edges into Edge Table + Mermaid + dispatched d3 force-directed render | [graph.md](./graph.md) |
| language | Enforce per-skill language consistency (description-language rule + Edit/Write pre-check) | [language.md](./language.md) |
| lint | Validate and fix SKILL.md frontmatter | [lint.md](./lint.md) |
| merge | Combine related skills into one | [merge.md](./merge.md) |
| portability | public/published skill cross-ref + vendor-specific isolation rules | [portability.md](./portability.md) |
| publish-scope | published skill scope check before adding topics/scripts | [publish-scope.md](./publish-scope.md) |
| route | Recommend topic placement within skills (plugin-level clustering → cc-plugin/clustering) | [route.md](./route.md) |
| trigger | Register triggers and generate hooks | [trigger.md](./trigger.md) |
| upgrade | Enhance existing skills or add topics | [upgrade.md](./upgrade.md) |
| writer | Interactive skill creation wizard | [writer.md](./writer.md) |

## Core Workflows

### Creation (skill-writer)

Always use `writer` to ensure correct frontmatter and structure.

```bash
/skill-kit writer                  # Start wizard
```

### Maintenance (upgrade/lint)

Use `upgrade` to add new functionality or topics to an existing skill.

```bash
/skill-kit upgrade skill-name      # Interactive upgrade
/skill-kit lint skill-name         # Validation only
```

Improvement types:
- **Add Topic**: Add documentation for a new sub-feature
- **Add Script**: Add logic to `scripts/` and reference in SKILL.md
- **Fix Frontmatter**: Correct `triggers`, `depends-on`, or `description`

### Trigger (Auto-generate Hooks)

```bash
/skill-kit trigger compile     # Scan skills -> generate dispatcher -> register in settings.json
/skill-kit trigger list        # List registered triggers
/skill-kit trigger dry-run     # Preview only
```

Declare `triggers` in SKILL.md -> auto-generate hook scripts -> auto-register in settings.json.

[Detailed guide](./trigger.md)

### Find (Discover via npx skills)

```bash
/skill-kit find <query>        # Search the open skills ecosystem via npx skills CLI
```

Searches the [skills.sh](https://skills.sh/) leaderboard and ecosystem for installable skills. Use when looking for an existing skill rather than building one from scratch.

[Detailed guide](./find.md)

## Success Case

**Scenario (2026-03-09)**:
- Found 3 openclaw-related functions
- Proposed 3 options for merging
- Result: Implementation success, user satisfied

**Key factors**:
1. Identification of 3 functions
2. "Merge?" AskUserQuestion
3. Merging skills using skill-writer (multi-topic)

## Ralph Mode (AskUserQuestion bypass)

If `.ralph/` directory exists, operate in Ralph Mode.

**Workflow Change**:

| Step | User Interaction | Workflow |
| ---- | ---------------- | -------- |
| Step 1: Auto-detect | AskUserQuestion (multiSelect) | Summary info to `.ralph/improvements.md` |
| Step 1.5: Merge logic / Structure | - | improvements.md recording |
| Step 2: Requirements | AskUserQuestion | Trigger/scope recommendation to improvements.md |
| Step 3: Type recommendation | Recommend only | improvements.md recording |
| Step 4: Implementation | Direct action | **PROHIBITED** - Use `[NEEDS_REVIEW]` tag |
| Step 5: Validation | Validation | **Auto validation** (after changes are complete) |

## Self-Improvement

After changes are complete, **Self-improve based on conversation**:

1. Identify failure and workaround patterns
2. If candidates found, run `/skill-kit upgrade skill-kit`
