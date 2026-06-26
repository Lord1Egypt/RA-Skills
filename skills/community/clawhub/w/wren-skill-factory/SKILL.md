---
name: skill-factory
description: "Build and publish OpenClaw skills from recurring pain points. Scans .learnings/ for errors that hit 3+ recurrences, scaffolds skills from them, and publishes to ClawHub. Use when: (1) you want to create a new skill from a pain point, (2) you want to check if any recurring errors are ready for extraction, (3) you want to package and publish a skill in one step, (4) you want to automate the pain-to-skill pipeline. The thing that builds the thing."
---

# Skill Factory

Turn recurring pain points into published skills. Automatically.

## Why This Exists

Building skills manually takes 30 minutes: write SKILL.md, write the script, test, package, publish. The factory cuts this to 10 minutes by structuring the workflow and automating the boring parts.

More importantly: it connects to your `.learnings/` error log. When a problem recurs 3+ times, the factory flags it as a skill candidate. Your mistakes become products.

## Prerequisites

- `.learnings/ERRORS.md` and/or `.learnings/LEARNINGS.md` in your workspace (see `self-improving-agent` skill or create manually)
- ClawHub CLI authenticated (`npx clawhub@latest login`)
- Python 3 (for packaging via skill-creator)

## Commands

### Scan for skill candidates

```bash
node scripts/factory.js scan
```

Reads `.learnings/` and finds entries with 3+ recurrences and a known fix. These are ready for extraction into skills.

### Build from a pain point description

```bash
node scripts/factory.js build "agents keep double-replying to the same post"
```

Creates a skill scaffold at `skills/public/<slug>/` with a `.factory-prompt.md` describing what to build. Then you (the LLM) write the SKILL.md and script.

### Build from a .learnings/ entry

```bash
node scripts/factory.js from-error ERR-20260316-001
```

Same as `build`, but pulls the description and fix from an existing error entry.

### Publish

```bash
node scripts/factory.js publish skills/public/my-skill
```

Packages and publishes to ClawHub in one step. Cleans up factory files first.

## The Pipeline

```
Mistake → .learnings/ERRORS.md → scan (3+ recurrences) → from-error → write skill → publish
```

### Learnings Format

The factory expects entries in this format:

```markdown
## [ERR-20260316-001] Short description
**Recurrences:** 3 | **Last:** 2026-03-16
**What failed:** what went wrong
**Fix:** what actually solved it
```

Or for learnings:

```markdown
## [LRN-20260316-001] Short description
**Category:** best_practice
**Recurrences:** 3 | **Last:** 2026-03-16
**What happened:** context
**The lesson:** what's correct
```

## Integrating With Heartbeats

Add to your heartbeat config to surface new candidates:

```yaml
collectors:
  - name: skill-candidates
    command: "node tools/skill-factory/factory.js scan --count"
    format: text
    alert: "> 0"
    summary: "{{output}} skill candidates ready for extraction"
```

## CLI Reference

```
node scripts/factory.js <command>

  scan                    Find extractable patterns in .learnings/
  scan --count            Just print the count (for heartbeat integration)
  build "description"     Scaffold a skill from a pain point
  from-error <id>         Scaffold from a .learnings/ entry
  publish <dir>           Package + publish to ClawHub
```
