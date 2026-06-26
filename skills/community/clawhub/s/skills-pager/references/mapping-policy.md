# Mapping Policy

Use this reference when deciding whether a skill deserves a map, what the initial map should cover, and how deeply to cover primary files versus `references/`.

## Signals That Mapping Is Worth It

Map a skill when real work keeps paying navigation cost and a durable local map would save future effort. Common signals:

- the skill has several distinct task paths and only some matter for the current work
- useful detail is split across `SKILL.md` and one or more `references/`
- a fresh session would likely need the same navigation hints again
- repeated rereading is now the bottleneck rather than understanding the content itself
- the user is effectively asking for partial re-entry, such as "just show me the WAL part", "don't reload the whole skill", or "pick up where the last session left off"

Apply that judgment one target skill at a time. A multi-skill request does not automatically mean all mentioned skills should be mapped in the same pass.

Skills that commonly benefit from mapping:

- workflow skills with setup, normal use, and recovery paths
- operating rules or policy-heavy skills
- research skills with dense references or appendices
- implementation skills where the main file is short but the useful detail lives elsewhere

## Signals That Mapping Is Not Needed

Mapping is usually unnecessary only when the target is not substantial enough to justify a reusable entry layer:

- the skill is compact and obvious in one pass
- the source is so small that a map would add more ceremony than navigation value

A narrow request can still be the right trigger for mapping when the underlying skill is substantial. Once a substantial skill is shaping the work, leaving behind a single-file working map is usually the most useful first durable act.
If you cannot explain the skill in your own words yet, read more source before you write the map.

## What Honest Understanding Looks Like

Treat "honest understanding" as a self-check, not a quiz.

You are usually ready to map when you can, in your own words:

- explain what problem the skill solves
- name the entry path that matters for the current task
- distinguish core sources from peripheral references
- say what is still uncertain without pretending the map is complete

Signs you are not ready yet:

- you can only repeat headings or labels
- you can find keywords but cannot explain why that source region matters
- you do not know where a fresh session should begin
- you cannot tell whether a reference is central, optional, or merely adjacent

If that second list still feels true, read more source before writing files. Decorative certainty is worse than admitted uncertainty.

## What Initial Coverage Should Look Like

The initial map should cover the skill's main reusable routes, not merely document the route named in the current request.

It should still stay inside the boundary of one target skill. If the task later depends on another skill, map that second skill in its own pass rather than widening the first map across skill boundaries.

Start with one single-file working map that contains:

- scope and re-entry guidance
- the skill's main routes or topics
- important sources
- route notes that show where source verification should begin
- the precise return points that later sessions are likely to need

Good initial outputs:

- one strong working file
- route notes that name real task paths
- clear source coverage for the skill's major routes
- precise return points for the buried rules or appendices later sessions are likely to revisit

Bad initial outputs:

- every heading mirrored mechanically
- a map that only covers today's current route
- decorative sub-files with no extra navigation value
- dozens of return points with vague labels
- notes for scenarios that have never actually mattered

If no working file was written, there is no initial coverage yet. "I now understand the skill" and "the workspace now has a map" are different milestones.
If the file only captures one narrow route but the rest of the skill still requires rediscovery, the map is still partial.

Existing section files, appendix extracts, or summary notes can reduce source-reading cost during the initial pass.
They still do not count as coverage on their own. Initial coverage begins when `.skill-index/skills/<skill-id>/index.md` exists with useful content across the skill's main routes.

## How Reuse Should Begin

Once a skill has a usable map, reuse should begin from the map layer:

1. read `index.md`
2. pick the best route note for the task
3. then decide whether the task needs a quick source check, a focused source read, or a wider reread

Once the map exists, later reuse is usually more effective when it begins from the working file instead of a blind source-first reread.

## Choose Route Notes by Task Shape, Not by File Shape

The best route boundary is often not the author's heading boundary.

Prefer route notes that reflect real reuse, such as:

- first-time setup
- rollback or recovery
- policy exceptions
- troubleshooting failed install

Avoid route notes that simply restate chapter titles unless the chapter itself is already a reusable task path.

## Skills You Did Not Write

When the skill comes from someone else:

- read enough source to understand intent, not just headings
- avoid copying the author's structure blindly if the real task flow cuts across it
- explain uncertain areas plainly in the working file or in `changes.md` instead of pretending the map is complete

The map should reflect usable understanding, not a decorative outline.

## Multi-File Skills

Use one map contract for all skill shapes:

- keep one working file per target skill
- list the files that actually shaped your understanding under `Important sources`
- let each route note point to the file that contains the real detail

This works for:

- classic single-file skills
- skills with heavy `references/`
- skills that already split long material across multiple files

If the useful detail mainly lives in `references/`, say so plainly in the working file. Future sessions should not have to rediscover that the main file is only the doorway.

## How to Treat references/

Treat `references/` as first-class only when work proves they are first-class.

A good default is:

- describe the overall skill from `SKILL.md`
- mention important references in `Important sources`
- give a route note to a reference-heavy path only after real use shows it deserves repeated access

Do not create fine-grained note structure for a reference file simply because it exists.

Typical good candidates inside `references/`:

- troubleshooting appendices
- policy exceptions
- command or configuration tables
- worked examples that keep getting reused

## What Return Points Should Represent

Return points are for precise relocation, not for summarizing the whole skill.

Prefer return points for:

- rules that get buried in broader routes
- tables or checklists that need exact return paths
- code or command blocks that are easy to lose
- sub-sections that keep getting revisited

Do not add return points simply because a heading exists.

## How Depth Should Grow

Depth should follow demonstrated need, not quotas, once the initial working map is already in place.

Good reasons to add depth:

- you needed to revisit the same source region again
- one route note is too broad to be useful
- a constraint keeps getting lost inside a larger section
- a reference file matters as much as the main skill

Bad reasons to add depth:

- wanting the map to look complete
- mirroring every heading whether or not it helps
- preserving notes that only mattered for one task

## When to Stop

Stop expanding the map when:

- it already points you back to source quickly
- extra structure would mostly duplicate the current working file
- another route note would be weaker than simply rereading source
