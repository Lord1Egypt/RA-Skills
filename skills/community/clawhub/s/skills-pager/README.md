

# skills-pager

**Navigation index for large AI agent skills — load only what you need**

Answer first · Index after · Reuse forever



[English](README.md) · [中文](README.zh-CN.md)



---

## The Problem

Large AI agent skills — workflow skills, policy-heavy skills, multi-file skills — can run 200, 400, even 600+ lines. Every time the agent needs just one section, it re-reads the entire source. That wastes context window, slows down reasoning, and makes partial re-entry painful across sessions.

**What if the agent could read a large skill once, build a compact navigation index, and then load only the sections it needs from that point forward?**

## The Solution

**Skills Pager** is a standard skill that teaches the host agent to build and reuse a single-file navigation index (`index.md`) for any skill over about 100 lines.

> **First encounter** — The agent reads the full source and answers the user's question directly. After answering, it builds a compact `index.md` that maps the skill's main routes, important sources, and precise return points.
>
> **Every encounter after** — The agent reads the index first (typically 30–50 lines instead of 300–600), loads only the source sections it needs, and answers with less context burn and faster orientation.

The source stays authoritative. The index is navigation, not memory. The agent stays in control of what to map and when.

## What You Get

- **Context savings** — Stop burning hundreds of lines of context on sections you don't need. The index tells you exactly which parts to load for the current task.
- **Faster partial access** — Jump to the right section of a large skill in one read instead of scanning the whole file.
- **Durable re-entry** — Future sessions and handoffs start from a compact working file instead of blind source re-reading.
- **Answer-first workflow** — The index never blocks answering. Build it after the task is done, while understanding is fresh.
- **One file, not seven** — A single `index.md` per skill.
- **Companion scaffold script** — `create-skills-pager-map.js` removes filesystem friction so the agent can focus on writing useful route notes.

## Installation

Copy the `skills-pager` directory into your workspace skills folder:

```bash
cp -r skills-pager /path/to/workspace/skills/skills-pager
```

## How It Works

### First Encounter

```
User asks about Phase 3 of research-workflow (400-line skill)
  ↓
Agent reads skills/research/workflow/SKILL.md → answers the question
  ↓
Agent recognizes: this was a large skill, no index exists yet
  ↓
Agent runs: node skills/skills-pager/scripts/create-skills-pager-map.js \
              --skill-id research-workflow \
              --source skills/research/workflow/SKILL.md \
              --page phase-architecture \
              --page innovation-mining \
              --page adversarial-review
  ↓
Agent replaces scaffold placeholders with real route notes
  ↓
.skill-index/skills/research-workflow/index.md now exists on disk
```

### Later Encounter

```
User asks about Phase 6 of research-workflow
  ↓
Agent reads .skill-index/skills/research-workflow/index.md (40 lines)
  ↓
Finds route note: "adversarial-review" → points to SKILL.md lines 280-350
  ↓
Agent loads only that section → answers with minimal context cost
```

## File Structure

```text
.skill-index/                          # workspace root, not inside skill source
  registry.json                        # which skills are indexed
  skills/
    research-workflow/
      index.md                         # the working navigation index
      changes.md                       # optional: why the index changed
    quant-workflow/
      index.md
```

## What `index.md` Looks Like

```markdown
# research-workflow

## What this skill is for
- Multi-phase research workflow with gated transitions and iterative loops

## When to start here
- Any task involving research phases, innovation mining, or adversarial review

## Main routes
- `phase-architecture`
- `innovation-mining`
- `adversarial-review`

## Important sources
- `skills/research/workflow/SKILL.md`
- `skills/research/workflow/references/phase-order.md`

## Route notes

### phase-architecture
- When to start here: understanding the 6-phase gate structure
- Start source: `SKILL.md` "Phase Architecture" section
- What to verify: gate conditions between phases, Phase 3 internal loops
- Next likely checks: innovation-mining for Phase 3 detail

### adversarial-review
- When to start here: Phase 6 self-review or quality checks
- Start source: `SKILL.md` "Adversarial Self-Review" section
- What to verify: iterate-back conditions to Phase 3 or 4
- Next likely checks: phase-architecture for the full gate flow
```

## Companion Script

```bash
node skills/skills-pager/scripts/create-skills-pager-map.js \
  --skill-id <target-skill-id> \
  --source <path-to-SKILL.md> \
  --source <path-to-reference-if-needed> \
  --page <route-name> \
  --page <another-route-name> \
  --note "Optional note for the registry entry"
```

The script creates the directory structure, `registry.json`, and a scaffold `index.md` with placeholder route notes. Replace the placeholders with real content before treating the index as reusable.

## Design Principles


| Principle               | What it means                                                                                                          |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Answer first**        | Never let index creation block the user's question. Build the index after answering, while understanding is fresh.     |
| **Source is authority** | The index is navigation, not a replacement for source verification on consequential details.                           |
| **One skill at a time** | Each index covers one target skill. Multi-skill requests are handled as sequential single-target cycles.               |
| **One file is enough**  | A single `index.md` beats seven partial files. Depth grows from reuse, not from ceremony.                              |
| **100-line threshold**  | Skills under ~100 lines rarely need an index. Save the effort for skills where partial loading actually saves context. |


## Project Structure

```text
skills-pager/
  SKILL.md                              # main skill file (read by the host agent)
  scripts/
    create-skills-pager-map.js          # scaffold script for index creation
  references/
    initial-mapping.md                  # first-time index creation workflow
    mapping-policy.md                   # when and what to map
    map-layout.md                       # index file structure and format
    lookup-patterns.md                  # daily usage patterns and examples
    map-quality.md                      # quality signals for indexes
    refresh-policy.md                   # when and how to update stale indexes
```

## License

[MIT](LICENSE)
