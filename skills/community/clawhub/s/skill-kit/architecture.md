# Multi-Topic Skill Architecture

Define the directory structure for skills with multiple related topics.

## When to Use

- Creating a new skill with multiple sub-topics
- Merging related skills into one
- Organizing complex skills with separate guides

## Directory Structure

```
~/.claude/skills/{skill-name}/
├── SKILL.md          # Unified frontmatter + topic references
├── {topic1}.md       # First topic content (no frontmatter)
├── {topic2}.md       # Second topic content (no frontmatter)
└── scripts/          # Shell/Python scripts called by topics (optional)
    ├── {script}.sh
    └── {script}.py
```

### File Roles

| File | Purpose |
|------|---------|
| `SKILL.md` | Entry point with frontmatter, overview, and topic index |
| `{topic}.md` | Detailed guide for specific topic (no frontmatter) |
| `scripts/` | Reusable scripts referenced from topic files |

### scripts/ Rules

- **All scripts executed by the skill must be inside `scripts/`** — no external path references
- Scripts must be permanent files (no tmp paths)
- Reference scripts from topic files using relative paths: `bash scripts/run.sh`
- If using scripts outside the skill (`~/Sync/...`, `/usr/local/...`) → copy into `scripts/` first

## SKILL.md Template

```yaml
---
name: {skill-name}
description: {unified description}. {topic1} - {desc1}, {topic2} - {desc2}. "{trigger1}", "{trigger2}" triggers
---

# {Skill Name}

{Common theme description}

## Topic Dispatch

**When this skill is invoked with a topic specifier (e.g., `/{skill-name} {topic1}` or `Skill("{skill-name}", "{topic1}")`), load and follow only the matching topic file (`{topic1}.md`). Do not echo the Topics table or summarize other topics in the response.** The Topics table below is an index for invocations without a topic specifier — it is not user-facing output when a topic is named.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| {topic1} | {description} | [{topic1}.md](./{topic1}.md) |
| {topic2} | {description} | [{topic2}.md](./{topic2}.md) |

## Quick Reference

### {Topic1}

Brief summary of topic1.

See [detailed guide](./{topic1}.md).

### {Topic2}

Brief summary of topic2.

See [detailed guide](./{topic2}.md).
```

## Topic File Template

Topic files contain only content (no frontmatter):

```markdown
# {Topic Title}

{Detailed guide content}

## When to Use

{Specific use cases for this topic}

## Instructions

{Step-by-step guidance}

## Examples

{Concrete usage examples}
```

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Skill directory | lowercase, hyphens | `argocd-helm` |
| Topic files | lowercase, hyphens, `.md` | `cleanup.md`, `oci.md` |
| SKILL.md | Uppercase | `SKILL.md` |

## Description Format

For multi-topic skills, use this description pattern (no markdown links to save tokens):

```
{Overall purpose}. {topic1} - {brief desc} [{file}], {topic2} - {brief desc} [{file}]. "{trigger1}", "{trigger2}" triggers
```

Example:
```yaml
description: ArgoCD Helm chart management. cleanup - clean Helm metadata [cleanup.md], oci - add OCI registry charts [oci.md]. "argocd helm", "helm metadata", "OCI helm" triggers
```

## Topic Dispatch Behavior

When a multi-topic skill is invoked with a topic specifier, the LLM must load the matching topic file directly and avoid echoing the SKILL.md Topics table back to the user. Exposing the full topic index is noise when the user has already named a specific topic.

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | List the full Topics table in chat when the user typed `/skill-name topic` | Read `{topic}.md` and execute its instructions; the Topics table stays internal |
| 2 | "Topic was specified, but here are the other topics for context…" preamble | No preamble. Begin executing the topic's procedure or answering directly |
| 3 | Treat the SKILL.md Topics table as part of the user-facing response | The Topics table is an index for topic-less invocations only |
| 4 | Re-read SKILL.md every turn even after the topic is resolved | After dispatching, work from the topic file contents until topic changes |

### Required SKILL.md Section

Every multi-topic SKILL.md must include a `## Topic Dispatch` section placed **immediately above the Topics table**. Copy the directive verbatim, replacing `{skill-name}` and `{topic1}` with concrete values:

```markdown
## Topic Dispatch

**When this skill is invoked with a topic specifier (e.g., `/{skill-name} {topic1}` or `Skill("{skill-name}", "{topic1}")`), load and follow only the matching topic file (`{topic1}.md`). Do not echo the Topics table or summarize other topics in the response.** The Topics table below is an index for invocations without a topic specifier — it is not user-facing output when a topic is named.
```

### When the Topics Table IS Surfaced

The Topics table remains the right answer in exactly these cases:
- The user invokes the skill without a topic (e.g., `/skill-name` alone) and needs to discover available topics
- The user explicitly asks "what topics does this skill have?"
- The user requests an overview or comparison across topics

### Integration with Other Topics

- **writer**: When generating a new multi-topic SKILL.md, insert the `## Topic Dispatch` section above the Topics table by default
- **upgrade**: When upgrading an existing multi-topic skill that lacks the section, add it as part of the upgrade procedure
- **lint**: Verify that every multi-topic SKILL.md contains the `## Topic Dispatch` heading; emit a warning if missing

## Data Store Pattern

Skills that maintain persistent state use a `data/` directory for JSON/cache files.

### Structure

```text
~/.claude/skills/{skill-name}/
├── SKILL.md
├── {topic}.md          # Read/write logic for data files
├── data/               # Persistent state (JSON, cache)
│   └── {name}.json
└── scripts/            # Optional automation scripts
```

### When to Use

- Skill needs to remember state across sessions (e.g., published versions, mappings)
- Data is too dynamic for static .md content but too small for a database
- Multiple topics share the same data source

### Rules

| Rule | Rationale |
|------|-----------|
| `data/` only stores JSON/plain text | Keep parseable, no binaries |
| Topics that modify data must update `data/` in the same step | Prevent stale cache |
| Add `data/` to `.clawhubignore` if publishing | User-specific state should not be distributed |
| Include an `updatedAt` field in JSON | Track freshness |

### Example: clawhub skill

```text
clawhub/
├── SKILL.md
├── deploy.md         # Writes to data/published.json after publish
├── status.md         # Reads from data/published.json
├── data/
│   └── published.json  # { "updatedAt": "...", "skills": [...] }
└── scripts/
    └── check-slugs.sh
```

### Example: next skill (hook locale pattern)

When a hook script needs locale-specific match patterns (Korean, Japanese, etc.) but must stay language-neutral when published, separate the patterns into `data/*.regex` files and load them at runtime:

```text
next/
├── SKILL.md
├── stall-detect.md
├── resources/
│   └── next-trigger.sh        # 100% English; loads data/*.regex at runtime
├── data/                      # git-ignored AND publish-ignored
│   ├── en.regex
│   └── ko.regex
├── .gitignore                 # data/
└── .clawhubignore             # .gitignore, data/, *.tmp
```

Hook script loader pattern:

```bash
DATA_DIR="$(dirname "$0")/../data"
if compgen -G "$DATA_DIR/*.regex" > /dev/null 2>&1; then
  PATTERN=$(cat "$DATA_DIR"/*.regex | sed 's/#.*$//' | awk 'NF' | paste -sd'|' -)
else
  PATTERN='Fix complete:|✅|all done|task complete'   # built-in English fallback
fi
echo "$LAST_TEXT" | grep -qiE "$PATTERN" && ...
```

Each `*.regex` file uses `#` for comments, one alternation entry per line. Users can add their own locale file (e.g., `ja.regex`, `zh.regex`) without forking the script. The fallback ensures the hook works on fresh installs without a `data/` directory.

| Pattern Type | When to Use |
|--------------|-------------|
| State cache (clawhub) | Persistent JSON state that scripts/topics read/write |
| Locale data (next) | Functional input data that should not be distributed but should remain extensible by end users |

### Integration with Other Topics

When creating/upgrading skills with a data store:
- **writer**: Ask if the skill needs persistent state → create `data/` directory
- **upgrade**: When adding a topic that produces state, add `data/` and a corresponding read topic
- **lint**: Verify `data/*.json` files are valid JSON

## Best Practices

1. **Keep topics focused**: Each topic file should cover one specific capability
2. **Cross-reference**: Link between related topics when relevant
3. **Consistent structure**: Use similar headings across topic files
4. **Index in SKILL.md**: Always maintain the Topics table for discoverability
