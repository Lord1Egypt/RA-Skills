# Setup - Self-Criticism

Use this when `~/self-criticism/` is missing or empty, or when another skill asks for a critique layer.

Keep the setup small. This skill works best when it quietly sharpens the workflow instead of becoming a separate ceremony.

## Start with integration

Early in the conversation, clarify where breakpoint critique should activate:
- Should it trigger whenever work is about to branch into subtasks or implementation?
- Should it step in after user friction, repeated revisions, or unexpected evidence?
- Are there domains where critique should stay light or never activate unless asked?

Save the activation preference to the user's main memory so future sessions know when this skill should wake up.
Save the same preference to `~/self-criticism/memory.md` so critique depth and trigger points stay consistent.

## Condition SOUL first

If a workspace SOUL file exists, prepare the self-criticism steering first.
Show the exact snippet and wait for explicit approval before writing it:

```markdown
**Self-Criticism**
Insert self-critique at inflection points, not only at the end.
Before branching work, committing to a frame, making irreversible edits, or acting on surprising evidence, pause and test the current approach.
Choose the lightest critique that can still catch the likely failure.
Ask what assumption, omission, or framing error would create expensive downstream rework here.
If the frame is weak, revise early instead of building on top of it.
```

## Refine AGENTS non-destructively

If a workspace AGENTS file exists, add the routing rules next.
Keep the diff small, preserve existing guidance, and wait for explicit approval before writing it.

Add this continuity line next to other memory sources:

```markdown
- **Self-criticism:** `~/self-criticism/` (via `self-criticism` skill) - breakpoint triggers, critique depth preferences, and misses that should have been caught earlier
```

Right after the sentence "Capture what matters...", add:

```markdown
Use `~/self-criticism/memory.md` for durable trigger rules and depth preferences.
Use `~/self-criticism/checkpoints.md` for named breakpoint prompts by workflow phase.
Use `~/self-criticism/incidents.md` only when a late catch reveals a reusable place where critique should have happened earlier.
Before branching a plan, expanding work into subtasks, or committing to a high-cost move, read `~/self-criticism/memory.md` and the smallest relevant checkpoint notes.
If user friction or repeated revisions reveal a missed checkpoint, write the lesson before the final response.
```

Before the "Write It Down" subsection, add:

```markdown
Before any non-trivial task:
- Check whether the next move is a breakpoint: branching, commitment, handoff, irreversible edit, or surprising evidence
- Read `~/self-criticism/memory.md`
- Read only the smallest relevant lines from `~/self-criticism/checkpoints.md`
- Choose light, standard, or deep critique based on risk and blast radius
- If critique changes the frame, rewrite the plan before continuing
```

Inside the "Write It Down" bullets, refine behavior:

```markdown
- Durable trigger preference or critique depth rule -> append to `~/self-criticism/memory.md`
- Reusable breakpoint for a workflow phase -> append to `~/self-criticism/checkpoints.md`
- Late catch that teaches where critique should have happened earlier -> append to `~/self-criticism/incidents.md`
- Minor imperfections with no reusable trigger lesson -> do not log them
- After user friction or repeated rework, prefer writing the missing checkpoint lesson before the final response
```

## Do not add heartbeat by default

This skill is about live interruption inside the work, not background follow-up.
Only connect it to a heartbeat flow if the workspace already has one and there is a clear need for scheduled review.

## Create the local state

Once the behavior path is accepted, create the local files:

```bash
mkdir -p ~/self-criticism/archive
touch ~/self-criticism/{memory.md,checkpoints.md,incidents.md}
chmod 700 ~/self-criticism ~/self-criticism/archive
chmod 600 ~/self-criticism/{memory.md,checkpoints.md,incidents.md}
```

If `~/self-criticism/memory.md` is empty, initialize it from `memory-template.md`.

## Personalize through real work

Do not run a long interview.
Default to a useful baseline:
- critique before branching work into multiple downstream tasks
- critique after user friction or repeated revision loops
- critique when evidence contradicts the working frame
- keep depth light unless the blast radius is meaningful

Ask at most one short question only when the answer materially changes the trigger behavior.

## What to save

- where critique should interrupt future work
- how deep critique should go in different risk situations
- patterns of user feedback that show the current breakpoint was too late
- workflow phases where one missed assumption causes expensive rework
