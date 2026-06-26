---
name: skills-pager
description: >-
  Build or reuse a compact navigation index for large, multi-file, or layered
  skills so you can load only the sections you need instead of rereading the
  full source. Saves context, speeds up partial access, and gives future
  sessions a fast re-entry point.
---

# Skills Pager

Any skill over about 100 lines costs real context whether you need the whole thing or just one section. Skills Pager builds a compact `index.md` after your first deep read of a large skill, so the next time — or even two turns later in the same session — you can jump straight to the section you need without burning context on the parts you don't.

If `.skill-index/skills/<skill-id>/index.md` already exists for a skill you are about to read, start there. It is shorter than the source and tells you exactly which sections to load for the current task.

## One Job

Create or reuse a single working file at `.skill-index/skills/<skill-id>/index.md` for one target skill at a time.

This is an efficiency tool, not filing work. The source stays authoritative. The index exists so you can jump back to the right section faster, load less source, and spend more of your context on actual reasoning instead of rediscovering structure you already understood once.

## Quick Check

When a skill you need is roughly 100 lines or more:

1. Does `.skill-index/skills/<skill-id>/index.md` already exist?
2. **Yes** → read the index first, load only the source sections it points to, then answer.
3. **No** → read the source and answer the task first. After answering, build the index so the next encounter can skip the full reread.

## Current Target Skill

Paging works on one target skill at a time.

Pick the current target as the skill that owns the section, protocol, or phase you need to answer next. If several skills appear in the same request, do not widen the index to cover all of them at once. Handle the first target you actually need, then repeat for the next target only if the task still needs it.

When `.skill-index/skills/<skill-id>/index.md` is missing for the current target, that absence is not only a status check — the missing index is the next piece of work for that target once the user's question is answered.

## When It Helps

Use this skill when:

- you are about to read a SKILL.md that is 100+ lines but only need one section of it
- you just deeply read a big skill and will probably need parts of it again later
- a request names specific parts across multiple large skills
- you notice yourself rereading the same source regions across turns
- important detail is split across `SKILL.md`, `references/`, or pre-split section files
- a fresh session or handoff would likely need the same entry points again

These skill shapes often benefit from paging:

- workflow skills with distinct phases
- policy-heavy skills with buried rules
- multi-file skills where the real detail lives in `references/`
- skills whose useful content is split across many files

You usually do not need paging when:

- the skill is short or flat enough to scan directly
- the source is small enough that an index would add ceremony without improving re-entry

A narrow request can still be the right trigger for building the index when the underlying skill is substantial.

## What Mapped Means Here

A skill is treated as mapped in this workspace when `.skill-index/skills/<skill-id>/index.md` exists with useful content.

That single working file should cover:

- what the skill is for
- when a session should start there
- the main routes or topics worth re-entering
- the important sources that shaped the index
- the precise return points that later sessions should not have to rediscover

Later growth can add `changes.md`, but the first useful pass should leave one complete working file rather than several partial placeholders.

## Where It Lives

Write pager files in the workspace root, not inside the skill source and not inside memory files:

```text
.skill-index/
  registry.json
  skills/
    <skill-id>/
      index.md
      changes.md  # optional later
```

If `.skill-index/skills/<skill-id>/index.md` does not exist yet, treat the skill as unmapped in this workspace.

## Quick Start

This skill includes a companion scaffold script at `scripts/create-skills-pager-map.js`.

Resolve that path relative to the installed `skills-pager` directory. If this skill is installed under `skills/skills-pager/`, a workspace-root command typically looks like:

```bash
node skills/skills-pager/scripts/create-skills-pager-map.js \
  --skill-id <target-skill-id> \
  --source <target-skill-path> \
  --source <reference-or-section-path-if-used> \
  --page <major-route-or-topic> \
  --page <another-major-route-or-topic>
```

Use the script to draft the single-file index quickly. It is mechanical help only. Decide the route set from source first, then replace the placeholders with real content before treating the index as usable.

## Workflow

### If the Index Already Exists (Reuse Path)

1. Read `.skill-index/skills/<skill-id>/index.md`.
2. Pick the route note that matches the current task.
3. Load only the source sections it points to.
4. Verify from source as needed.
5. If the index proves weak or stale, update it and optionally add `changes.md`.

### If No Index Exists Yet (Creation Path)

1. Read the target skill's source and answer the user's question first.
2. After answering, check whether the skill was substantial enough to justify an index.
3. If yes, read `references/initial-mapping.md` for the mapping workflow.
4. Read `references/map-layout.md` for the index file structure.
5. Read enough source to understand the skill's main routes beyond today's narrow request.
6. If the workspace already has section files, appendices, or notes that expose useful source regions, use them as inputs.
7. Run the companion script `scripts/create-skills-pager-map.js` using the installed skill-local path.
8. Replace the scaffold placeholders in `index.md` so the file covers the target skill's main route set.
9. The next session or turn that needs this skill will start from the index.

A reliable mental model:

- answer the user's question using the source directly
- then ask: was that skill big enough that a future session would benefit from a shortcut?
- if yes, build the index while the understanding is fresh
- the durable output is the working file on disk, not only a chat summary

### Multi-Skill Requests

If the task names several large skills:

1. Pick the first target you need to answer now.
2. Check its index state and follow the matching path above.
3. Answer the part of the task that depends on it.
4. Move to the next target only if the request still needs it.
5. Keep each index under its own `.skill-index/skills/<skill-id>/` directory.

## Reuse

1. Read `index.md`.
2. Use that file to recover scope, route choices, and likely source jumps.
3. Decide whether the current task needs only a quick source check, a focused source read, or a wider reread.
4. Re-read the amount of source needed for the current detail level before relying on consequential instructions.
5. If the index proves weak or stale, update it and optionally record why in `changes.md`.

The index lowers re-entry cost. It does not replace source verification for consequential detail, but it often replaces blind source-first re-entry as the default starting point.

## Keep It Simple

- source is the authority
- `.skill-index/` is navigation, not memory
- first encounter: answer first, build the index after
- later encounters: check the index first, load only what you need
- later reuse starts by reading the index file
- one target skill at a time
- depth can grow later if repeated reuse proves it helpful

## Boundaries

Keep `.skill-index/` separate from:

- `MEMORY.md`
- `SESSION-STATE.md`
- `memory/YYYY-MM-DD.md`
- vector memory such as `memory_store` / `memory_recall`

A pager index stores navigation knowledge about skill sources. It should not store task outcomes, user preferences, or conversation history.

## Read These References When

- Read [references/mapping-policy.md](references/mapping-policy.md) when deciding whether a skill deserves an index and what the working file should cover.
- Read [references/initial-mapping.md](references/initial-mapping.md) when a substantial skill has started shaping the task but `.skill-index/` does not exist yet.
- Read [references/map-layout.md](references/map-layout.md) when writing or revising `index.md`.
- Read [references/lookup-patterns.md](references/lookup-patterns.md) when you want examples of daily lookup flows and handoff scenarios.
- Read [references/map-quality.md](references/map-quality.md) when judging whether an index is genuinely useful or just tidy.
- Read [references/refresh-policy.md](references/refresh-policy.md) when the source or the index has drifted.
