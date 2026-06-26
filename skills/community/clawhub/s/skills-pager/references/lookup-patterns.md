# Lookup Patterns

These are example lookup patterns, not mandatory procedures. Use them when you want a quick model for how a mapped skill can be queried in real daily work without letting the map replace source judgment.

## Pattern: First Contact With a Substantial Skill

Answer first, then leave behind the index.

- Read the target `SKILL.md` (100+ lines) and answer the user's question directly from the source.
- After answering, read [initial-mapping.md](initial-mapping.md).
- Read the `references/` needed to understand the skill's main route structure, not only today's narrow request.
- If the workspace already has a section file, appendix extract, or prior note that exposes the right source region, use it as source input while landing the index.
- Identify the route notes the finished index should contain.
- Run the companion script `scripts/create-skills-pager-map.js` using the installed skill-local path to scaffold the working file.
- Replace the placeholders with real navigation content.

First contact becomes reusable once the working index is on disk. Finding the right part is a strong start, but it is more valuable when the index also covers the rest of the skill's main reusable paths.
Even when today's request is narrow, it often helps to let that request trigger the full index rather than a one-route shell.

Use this pattern when the workspace has no useful index yet and the skill is 100+ lines.
The index is a post-answer deliverable, not a prerequisite.

If multiple large skills appear in the same task, answer using the first one you actually need instead of trying to index every mentioned skill up front.

Example:

- a fresh session opens a complex skill for the first time
- a teammate hands off work and only says "the answer is in that skill somewhere"

Valid initial outcome:

- `index.md` exists
- the file names the major reusable routes
- the file lists the important sources
- the route notes point back to real source regions later sessions can verify quickly

Those notes should contain usable navigation content. A filename or placeholder heading alone is not enough.

## Pattern: The Skill Already Started Shaping The Work

If a substantial skill (100+ lines) has already influenced the task but no local index exists yet, build the index once the current answer is delivered.

- Finish answering the current question first.
- Then give the workspace a real index while the skill's structure is still fresh in context.
- Treat convenient source shortcuts as inputs, not as the index itself.
- Re-run the initial mapping scaffold if the working file on disk is missing or obviously partial.
- Initialize `.skill-index/skills/<skill-id>/index.md`.

This often happens when:

- you already read one critical section and realize you will need the skill again
- the current answer depends on one named protocol or recovery path
- the work is moving into a second turn and the same skill will clearly remain in play
- the current question looks narrow, but the skill being queried is still 100+ lines

## Pattern: Several Target Skills In One Request

Some requests name more than one skill but still do not require a combined index.

Use a single-target cycle:

1. pick the first target skill you need to answer now
2. check whether its index exists at `.skill-index/skills/<skill-id>/index.md`
3. if it exists, use the index to load only the relevant sections and answer
4. if it does not exist, read the source directly and answer
5. after answering, build the index for that target if it was 100+ lines and unmapped
6. move to the next target skill only if the request still needs it

This keeps reentry scoped and prevents a multi-skill request from turning into either:

- one oversized index that blends several skills together
- several independent raw lookups with no durable output

Example:

- "Show me research-workflow Phase architecture, then literature-research search flow, then quant-workflow stage 2."
- "Compare the rollout path in one skill with the credential policy in another."

## Pattern: Reuse Starts From The Map

Once a usable map exists, do not begin by rereading the skill from the top.

Start with:

1. `index.md`
2. the most relevant route note inside it

Then decide how much source you need:

- quick source check for one precise claim
- focused source read for one route or protocol
- wider reread only when the map shows the current task spans multiple routes or the map has gone stale

The map is the default entry point. Source depth is the variable decision that comes after the map, not before it.

## Pattern: I Know the Skill, Not the Route

Start with `index.md`.

Use the opening sections to recover scope and route choices, then pick the route note that best matches the task. Open the source directly only after the working file stops helping.

Example:

- "I know there was a warning about credentials, but I do not remember where."
- "I remember the skill covered this edge case somewhere in the appendix."

## Pattern: I Already Know the Task Shape

Start with the matching route note in `index.md`.

- If one route clearly matches the task, use it as the re-entry point.
- If the route feels close but not exact, use it as a starting guess and verify against source quickly.
- Add a more precise return point only when repeated reuse proves you need it.

Use this pattern when the task resembles something the skill has supported before.

Example:

- "I need the rollback steps again."
- "This is another first-time setup."

## Pattern: The Detail Probably Lives in a Reference

Use the working file to confirm whether the reference is central or peripheral.

- If a route note already sends you into that reference, start there.
- If not, use source directly and update the working file if the reference keeps carrying the real answer.
- If the reference keeps holding the answer, promote that path into a clearer route note instead of rediscovering the same fact every time.

Example:

- the main skill gives the route, but the exact rule lives in a companion appendix
- the worked example in a reference file has become the most reused part of the skill

## Pattern: The Task Spans More Than One Skill

Pick a primary skill first.

- Choose the skill that currently owns the task phase, decision, or protocol.
- Read the primary skill's working file before touching adjacent skills.
- Use that file to locate the handoff boundary: where the first skill stops, where the second one becomes necessary, and which constraint or route actually crosses between them.
- Query a second skill's map only if that second skill is truly part of the task, not just adjacent.
- Keep the maps separate. Cross-link them inside route notes with plain references such as "constraint lives in..." or "next skill..." instead of blending two skills into one file.

This avoids turning every multi-skill task into a broad map crawl.

Example:

- a deployment skill owns the rollout path, but a security skill owns the credential constraint
- a research workflow owns the main phase order, but a review skill owns the adversarial pass

## Pattern: The Map Feels Wrong

Trust the discomfort.

- Read the relevant source directly.
- Decide whether the problem is missing coverage, stale route notes, or a bad route boundary.
- Update only the part of the map that actually broke trust.

If the mismatch is broad, switch from querying to refreshing.

Example:

- the route note exists, but it sends you into a source region that is now too broad
- the return point sounds precise, but the source under it no longer matches
- the reference became the real source of truth, but the map still treats it as peripheral

## Pattern: Fresh Handoff

A new session should usually start with:

1. `index.md`
2. the most likely route note
3. source verification

If that still does not restore direction, the map is not yet strong enough for handoffs.
If step 1 fails because the file is missing, treat it as first contact and create the map before expecting a clean handoff.

## Pattern: The Map Was Never Landed

If a large skill has already been used in this workspace but `.skill-index/skills/<skill-id>/index.md` still does not exist, or the file only contains a thin shell, treat that skill as still unmapped here.

- Stop treating prior chat summaries as if they were the map.
- Re-open the reentry skill.
- Write the working file explicitly.
- Continue once the file exists on disk and the major routes are covered.

The value of reentry comes from durable reuse, so bring the file into existence before assuming the workspace is already mapped.
