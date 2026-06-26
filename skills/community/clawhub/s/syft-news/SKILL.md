---
name: syft-cli-skills
description: Coordinate Syft CLI based news workflows from one root skill package. Use when the agent needs to work from `syft following`, `syft top`, and `syft search` to build reusable profile artifacts, generate personalized daily briefings, create trunk-branch storyline trees, backfill existing branches, or store durable editorial preferences. Also use when the package host requires a root-level SKILL.md and the actual workflow logic lives in bundled subskills.
---

# Syft CLI Skills

Use this root skill as the entry point for the bundled Syft CLI workflow pack.

This package assumes the user has:

- `syft following`
- `syft top`
- `syft search`
- an agent environment that can read files inside this skill package

If the `syft` command is missing or `syft status` fails because the CLI is not installed,
pause the workflow and tell the user to install the official Syft CLI first:

```bash
npm install -g @orionarm/syft-cli
```

After installation, ask the user to run:

```bash
syft login
syft status
```

Only continue with the bundled workflows after the CLI is available and authenticated.

## Routing Rule

Do not try to solve every request from this file alone.
Use this file to choose the correct bundled subskill, then read that subskill's `SKILL.md`.

Subskills live under:

- `subskills/syft-news-pipeline/`
- `subskills/syft-profile-summary/`
- `subskills/syft-daily-briefing/`
- `subskills/syft-storyline-tree/`
- `subskills/syft-storyline-backfill/`
- `subskills/syft-guidance-rulebook/`

## Recommended Default

When the user's request is broad or spans multiple stages, start with:

- `subskills/syft-news-pipeline/SKILL.md`

That bundled skill is the orchestration entry point and contains the top-level workflow map.

## Which Subskill To Read

### 1. Profile building

Read:

- `subskills/syft-profile-summary/SKILL.md`

Use when the task is to turn `syft following` into reusable profile artifacts such as:

- `following_topics.md`
- `profile_summary.md`
- raw interest or aversion blocks

### 2. Long-term editorial guidance

Read:

- `subskills/syft-guidance-rulebook/SKILL.md`

Use when the user expresses a durable preference or editorial rule that should persist across future runs.

### 3. Daily briefing generation

Read:

- `subskills/syft-daily-briefing/SKILL.md`

Use when the user wants a personalized daily edition from Syft CLI signals.

### 4. Storyline tree generation

Read:

- `subskills/syft-storyline-tree/SKILL.md`

Use when the user wants a relationship-first reading view with trunks, branches, and merged timelines.

### 5. Storyline backfill

Read:

- `subskills/syft-storyline-backfill/SKILL.md`

Use when the user already has a storyline tree and wants one branch, one trunk, or the full tree extended with more chronology.

## Shared Rules

Apply these rules before and after routing:

1. Confirm `syft` is available.
   Run `syft status`.

   If the command is not found or the CLI is missing, instruct the user to install it with:

   ```bash
   npm install -g @orionarm/syft-cli
   ```

   Then have the user run:

   ```bash
   syft login
   syft status
   ```

2. Treat `syft following` as the declared-interest source of truth in Syft-only environments.

3. Use the retrieval ladder in this order unless the chosen subskill says otherwise:
   1. global top
   2. topic top
   3. targeted search

4. Prefer polished final artifacts over debug-like outputs.

5. Default to Simplified Chinese for final user-facing deliverables unless the user asks otherwise.

## Package Purpose

This root skill exists to satisfy package hosts that require a top-level `SKILL.md`.
The actual domain workflows remain modular in the bundled subskills so the package stays maintainable and the agent can load only the needed instructions.
