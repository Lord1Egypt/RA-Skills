# Find Skills

Discover and install skills from the open agent skills ecosystem using the Skills CLI (`npx skills`).

## When to Use

- User asks "how do I do X" where X might have an existing skill
- "find a skill for X", "is there a skill for X"
- "can you do X" where X is a specialized capability
- User wants to extend agent capabilities with new tools/workflows

## Skills CLI

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem.

**Key commands:**

```bash
npx skills find [query]              # Search for skills
npx skills add <owner/repo@skill>    # Install a skill (-g for global, -y to skip confirm)
npx skills check                     # Check for updates
npx skills update                    # Update all installed skills
```

**Browse skills at:** https://skills.sh/

### Search Source Priority

Several CLIs can search the open ecosystem. Use this order:

| Source | Command | Status | Use as |
|--------|---------|--------|--------|
| Skills CLI | `npx skills find <q>` | active | **primary** — non-interactive, parseable output, install counts |
| ClawHub | `Skill("clawhub", "find <q>")` | active | secondary — different registry; slug/publish workflow |
| context7 skills | `npx ctx7 skills search <q>` | **deprecated** | avoid — prints "Skill commands are deprecated and will stop working in the next major release"; interactive UI truncates to ~8 rows even with stdin closed |

**Default = `npx skills find`** — active, non-interactive (parseable), the canonical
Skills CLI. Use it for the `route` topic's 2b remote search. `ctx7 skills search`
exposes richer `Trust ★` + `Popularity` columns, but being deprecated + interactive
it is a one-off manual cross-check at best, never the automated default.

## Workflow

### 1. Understand the Need

Identify:
1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether a skill likely exists for this

### 2. Check the Leaderboard First

Check the [skills.sh leaderboard](https://skills.sh/) before running a CLI search. Top skills include:
- `vercel-labs/agent-skills` — React, Next.js, web design (100K+ installs)
- `anthropics/skills` — Frontend design, document processing (100K+ installs)

### 3. Search for Skills

```bash
npx skills find [query]
```

Examples:
- "how do I make my React app faster?" → `npx skills find react performance`
- "can you help me with PR reviews?" → `npx skills find pr review`
- "I need to create a changelog" → `npx skills find changelog`

### 4. Verify Quality Before Recommending

**Do not recommend based solely on search results.** Verify:

1. **Install count** — Prefer 1K+ installs. Be cautious under 100.
2. **Source reputation** — Official sources (`vercel-labs`, `anthropics`, `microsoft`) are more trustworthy.
3. **GitHub stars** — Repos with <100 stars should be treated with skepticism.

### 5. Present Options

Show the user:
1. Skill name and description
2. Install count and source
3. Install command
4. Link to learn more at skills.sh

### 6. Install

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` installs globally (user-level), `-y` skips confirmation. **Note**: global install path may collide with ClawHub-installed skills under `~/.claude/skills/`. Prefer per-project install (`npx skills add ... ` without `-g`) when a same-named skill already exists from ClawHub.

## Common Skill Categories

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## When No Skills Are Found

1. Acknowledge no existing skill was found
2. Offer to help directly with general capabilities
3. Suggest creating their own skill with `npx skills init`
