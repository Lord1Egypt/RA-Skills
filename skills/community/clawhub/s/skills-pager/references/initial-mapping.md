# Initial Mapping

Use this reference when `.skill-index/skills/<skill-id>/index.md` is missing and the current task already depends on a substantial skill.

Initial mapping is the first working index for one target skill. The goal is to leave behind a reusable single-file index for that skill alone, not only a placeholder for today's question.

Answer the user's question first using the source directly. Then, while you still understand the skill's structure, use that understanding to write the index. For any skill over about 100 lines, the first deep contact is usually the right time to create the index that later sessions can reuse.

## Single-Target Cycle

Treat initial mapping as a single-target cycle:

1. choose the current target skill
2. answer the user's question using the source directly
3. after answering, build the index for that target skill while understanding is fresh
4. only then move to the next target skill if the task still needs it

This keeps multi-skill requests from turning into broad preloading. A missing index for the current target does not block answering — it means the index is the natural follow-up once the answer is delivered.

## Sequence

1. Identify the first substantial skill (100+ lines) that is actually driving the task.
2. Read that skill's `SKILL.md` and answer the user's question.
3. After answering, read enough of the skill's `references/` to understand its main routes, important references, and likely handoff points.
4. Read [map-layout.md](map-layout.md).
5. List the route or topic notes the working file should contain.
6. Run the companion scaffold script using the installed skill-local path.

If the skill is installed under `skills/skills-pager/`, a workspace-root command looks like this:

```bash
node skills/skills-pager/scripts/create-skills-pager-map.js \
  --skill-id <target-skill-id> \
  --source <target-skill-path> \
  --source <reference-or-section-path-if-used> \
  --page <major-route-or-topic-label> \
  --page <another-major-route-or-topic-label>
```

7. Replace the generated placeholders in `index.md` with real route notes, source coverage, and return points.
8. Keep the file focused on the target skill's main reusable routes, not just today's narrow request.

If the task later turns to a second substantial skill, start a new cycle for that second skill. Keep each index under its own `.skill-index/skills/<skill-id>/` directory.

Argument notes:

- `--skill-id` names the skill being mapped, not `skills-pager`
- `--source` points at the real source files that shaped the current task
- `--page` can be repeated; use it for the major routes or topics the finished map should include, not only the route named in the current request

## What The Script Is For

The script is mechanical help only.

- It creates the directory, registry entry, and `index.md` scaffold in `.skill-index/`.
- It does not decide which routes matter.
- It does not replace source reading.
- It does not make the map reusable until the placeholders are replaced with real navigation content.

Use it to remove filesystem friction so your attention can stay on source judgment.

## What a Complete Initial Map Should Cover

After the scaffold pass, make sure all of these are true:

- `index.md` explains what the skill is for
- `index.md` tells a fresh session when it should start here
- the file names the skill's main routes or topics, not only today's request
- the file lists the important sources that shaped the map
- the route notes point back to real source regions later sessions should not have to rediscover
- the map makes a fresh session capable of choosing the right route before it has to reread source broadly

If those conditions are not true yet, the workspace has source notes but not yet a complete reusable map.
