# Pager Map Layout

Use this reference when you are creating or revising the `.skill-index/` directory and want a layout that a fresh session can understand quickly.

Treat the layout as a default contract, not a rigid schema. The goal is a complete working map for one target skill without turning the map into a mechanical mirror of every heading.

## Default Directory

```text
.skill-index/
  registry.json
  skills/
    <skill-id>/
      index.md
      changes.md  # optional later
```

The split is deliberate:

- `registry.json` tells the workspace which skills already have a working map
- `index.md` is the real reusable artifact for one target skill
- `changes.md` is optional history when later refreshes need a short causal trace

The initial pass should produce a single-file working map. If you eventually need more structure, grow from a strong `index.md` instead of starting with a directory full of placeholders.

Existing section files, appendix extracts, generated summaries, or prior notes may help you land the map faster.
Treat them as source inputs, not as substitutes for the `.skill-index/` files.
If creating the working file by hand is slowing progress, use `scripts/create-skills-pager-map.js` first and then replace the scaffold placeholders with real content.

## Initialization Writes Go In The Workspace Root

Write the map under the current workspace root:

- `.skill-index/registry.json`
- `.skill-index/skills/<skill-id>/index.md`

Do not place reentry files:

- inside the skill's own source directory
- inside `MEMORY.md`, `SESSION-STATE.md`, or daily memory files
- inside hidden agent home state outside the workspace unless a host explicitly requires that

The map is a workspace artifact for future task re-entry, not a modification of the source skill and not a memory transcript.

## Complete Initial Map

If you are mapping a skill for the first time, the initial map should usually include:

- `registry.json`
- `index.md`

Add `changes.md` once the map has actually evolved. Do not create extra files just to make the directory look complete.

This core set is the practical threshold for treating a skill as mapped here:

- if `index.md` does not exist, the skill is not yet mapped here
- a summary in chat does not replace files on disk
- an existing `sections/*.md`, appendix file, or note does not replace files on disk
- later sessions should treat a missing `index.md` as "no map exists yet"
- one quick existence check is enough; once absence is known, file creation should replace further auditing

If `registry.json` does not exist yet, create it as part of the same initialization pass. The registry should support that pass, not delay it.

## Workspace Registry

`registry.json` is the workspace-level directory of mapped skills.

Suggested shape:

```json
{
  "skills": {
    "deployment-pipeline": {
      "mapFile": ".skill-index/skills/deployment-pipeline/index.md",
      "lastReviewedAt": "2026-03-08T10:00:00Z",
      "notes": "Rollout and rollback routes captured in a single working map."
    }
  }
}
```

Use the registry to answer "does this workspace already have a usable map for this skill?"
Avoid turning registry inspection into a substitute for creating the skill-local file.
The registry is a workspace directory, not the map itself.

## What `index.md` Should Contain

The single-file working map should answer these questions quickly:

- what is this skill for
- when should a session start here
- what are the main reusable routes or topics
- which source files matter most
- where should source verification begin for each route
- which precise return points should later sessions not have to rediscover

One workable shape is:

```markdown
# deployment-pipeline

## What this skill is for
- ...

## When to start here
- ...

## Main routes
- `rollout`
- `rollback`
- `incident-recovery`

## Important sources
- `skills/deployment-pipeline/SKILL.md`
- `skills/deployment-pipeline/references/rollback.md`

## Route notes
### rollout
- When to start here: ...
- Start source: ...
- What to verify: ...
- Next likely checks: ...
```

Keep the file readable. It should feel like working notes that later sessions can trust, not like a schema dump.

## Route Notes

Route notes are the main reusable unit inside `index.md`. Each route note should represent a path that future sessions are likely to revisit.

Good route labels:

- `first-time-setup`
- `rollback`
- `compaction-recovery`
- `policy-exceptions`

Each route note should help a future session answer:

- when should this route be used
- where should source verification start
- which caveats or branch points matter
- what nearby route or reference may be needed next

Do not create one route note per heading. Choose route boundaries by task shape, not by source formatting.

## Precise Return Points

`index.md` should also carry the few precise return points that later sessions are most likely to need.

Prefer return points for:

- buried rules that keep getting lost
- checklists or tables that need exact return paths
- code or command blocks that are easy to lose
- appendix sections that matter more often than the main file suggests

Keep these concise. The point is fast relocation, not a second copy of the source.

## Change Log

`changes.md` explains why the map changed.
Write it for the next session that needs to judge whether a map change reflects durable reuse or a temporary detour. Human reviewers may read it too, but the primary reader is a later host deciding how much trust to place in the map.

Suggested entry:

```markdown
### 2026-03-08 — Reworked rollback route
- Trigger: incident response work needed a faster route back into rollback steps
- Changes: updated `index.md` route notes and clarified the appendix handoff
- Reason: rollback is a recurring access path, not a one-off detour
```
