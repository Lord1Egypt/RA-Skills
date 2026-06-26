---
name: repo-scout
description: Use when the user wants to use Repo Scout or work on the Repo Scout project to search GitHub repos, generate project ideas and reports, compare runs, inspect history or trending data, build dashboards, manage bookmarks/watchlists, or prepare publishable scouting outputs.
---

# Repo Scout

Use Repo Scout to turn GitHub repos into research, reports, and build ideas.

## Workflow

1. Decide the target topic or topic pack.
2. Choose the smallest useful command.
3. Prefer `--format table` for quick review, `--markdown` for shareable text, and `--json` for automation.
4. Save output with `--out` when the result should be reused.

## Core commands

- Search repos: `repo-scout search ...`
- Generate ideas: `repo-scout ideas ...`
- Make a report: `repo-scout report ...`
- Produce a brief: `repo-scout brief ...`
- Inspect momentum: `repo-scout trending ...`
- Review saved runs: `repo-scout history ...`
- Compare runs: `repo-scout diff ...`
- Build the dashboard: `repo-scout dashboard ...`
- Run the local app: `repo-scout serve ...`
- Inspect the library: `repo-scout library ...`
- Manage watchlist items: `repo-scout bookmark ...`
- Generate founder outputs: `repo-scout thesis`, `memo`, `next-actions`, `openclaw-prompt`

## When to use the references

- Read `references/commands.md` for the full command map.
- Use the project’s own docs when you need the exact output shape or a publishable example.

## Good defaults

- Use `--topic-pack` when the user wants a fast starting point.
- Use `--days` when comparing fresh trends.
- Use `--limit` to keep output focused.
- Use the dashboard or HTML report when the result should feel demo-friendly.

## Skill intent

This skill is for using Repo Scout itself, not for generic GitHub browsing. If the user wants repo discovery, trend tracking, idea generation, or scouting reports, start here.
