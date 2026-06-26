---
name: repo-scout
description: "Discover, evaluate, and rank GitHub repositories in any ecosystem or domain. Produces a structured ranking document with star counts, languages, issue health, and contribution friendliness scores. Use when scouting for open-source projects to contribute to, evaluating technology options, doing competitive analysis, or exploring a new ecosystem."
---

# Repo Scout — Repository Discovery & Ranking

## Overview

Systematically discover and rank GitHub repositories in a given ecosystem. Produces a structured, actionable ranking document.

**Use cases**: Open-source contribution targeting, technology landscape surveys, competitive analysis, ecosystem exploration.

## Prerequisites

Before starting, the user must have GitHub CLI authenticated:

```bash
gh auth status   # Must show "Logged in"
```

If not configured, ask the user to provide:
1. **GitHub username** — for searching and attribution
2. **GitHub token** — run `gh auth login` or set `export GH_TOKEN=<token>`

Without auth, `gh` API calls will hit rate limits quickly and private repo data won't be accessible.

## Workflow

### Step 1: Define Scope

Ask the user for (with sensible defaults):

| Parameter | Default | Example |
|-----------|---------|---------|
| Ecosystem keyword(s) | *(required)* | "AI agent", "LLM tools", "Kubernetes" |
| Target count | 15 | top 15 by stars |
| Minimum stars | 5,000 | Filter out small repos |
| Language filter | *(any)* | Python, TypeScript |
| Additional criteria | *(none)* | "must have bug label issues" |

### Step 2: Search & Collect

Use multiple search strategies to find candidates:

```
Search strategies:
1. GitHub search: "{keyword}" sorted by stars
2. "awesome-{keyword}" curated lists
3. GitHub trending in the domain
4. Web search for "{keyword} top open-source projects {year}"
```

For each candidate repository, collect:

| Data Point | How to Get |
|------------|-----------|
| Star count | GitHub API / web |
| Primary language | GitHub API |
| Last commit date | GitHub API |
| Open issue count | GitHub API |
| Bug-labeled issues | `gh issue list --label bug --state open --limit 5` |
| `good first issue` count | GitHub search |
| CONTRIBUTING.md exists? | Check repo root |
| CI configured? | Check `.github/workflows/` |
| PR template exists? | Check `.github/PULL_REQUEST_TEMPLATE.md` |
| License | GitHub API |

### Step 3: Score & Rank

Score each repository on a **contribution friendliness** scale:

| Factor | Weight | Scoring |
|--------|--------|---------|
| Actionable bug issues | 30% | 3=many clear bugs, 1=none |
| Activity (recent commits) | 20% | 3=daily, 2=weekly, 1=monthly+ |
| Contribution docs | 15% | 3=CONTRIBUTING+template, 2=partial, 1=none |
| CI/CD health | 15% | 3=green CI, 2=partial, 1=none |
| Community size (stars) | 10% | 3=>50K, 2=>10K, 1=>5K |
| Response time to PRs | 10% | 3=<3d, 2=<7d, 1=>7d |

### Step 4: Filter Out

Mark repositories to **skip** if:
- Non-code repo (awesome-lists, documentation-only, resource collections)
- Desktop/mobile UI bugs requiring hardware access
- No actionable bug issues (only feature requests or stale issues)
- Archived or unmaintained (no commits in 6+ months)
- Hostile contribution environment (PRs routinely ignored)

### Step 5: Produce Ranking Document

Write `{workspace}/ecosystem-top{N}.md`:

```markdown
# {Ecosystem} — Top {N} Repositories

> Generated: {date}
> Keywords: {keywords}
> Minimum stars: {min_stars}

## Rankings

| Rank | Repository | Stars | Language | Open Bugs | Score | Notes |
|------|-----------|-------|----------|-----------|-------|-------|
| 1 | owner/repo | 45.2K | Python | 12 | 8.5/10 | Active, good docs |
| 2 | ... | ... | ... | ... | ... | ... |

## Skipped Repositories

| Repository | Reason |
|-----------|--------|
| owner/repo | Non-code (awesome-list) |

## Detailed Profiles

### 1. owner/repo (45.2K ⭐)
- **Language**: Python
- **Last commit**: 2 days ago
- **Open issues**: 234 (12 labeled `bug`)
- **CONTRIBUTING.md**: ✅
- **CI**: ✅ GitHub Actions
- **Score breakdown**: Activity 3/3, Bugs 3/3, Docs 2/3, CI 3/3, Community 2/3, Response 2/3
- **Notes**: Very active, welcoming community
```

## Output

- `{workspace}/ecosystem-top{N}.md` — Structured ranking document ready for downstream use

## Tips

- When used as part of a contribution campaign, the output feeds directly into the **issue-hunter** skill for issue analysis.
- For technology evaluation, the ranking + detailed profiles are the final deliverable.
- Re-run periodically to catch ecosystem changes.
