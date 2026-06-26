# Refresh Policy

Use this reference when the map stops matching the source or stops matching the way you actually query the skill.

## Source Is the Authority

Before trusting a map, check the source list recorded in `index.md`. If the source has changed and you do not yet understand the impact, read source before relying on the map.

If the map feels wrong even before you check the source, trust that signal and verify.
If the core working file is missing, or only a thin shell was ever written, do not call this a refresh problem. It is still an initial mapping problem.

## Patch When Understanding Still Holds

Patch the map when the old map is basically correct and only specific parts drifted. Typical cases:

- a source heading moved but the intent is unchanged
- one route note is still right in spirit but needs a clearer re-entry point
- a reference file has become important enough to deserve better coverage
- a precise return point is still relevant but needs a better source jump

Patch only the affected parts of `index.md` and record why in `changes.md` if the change is likely to matter later.

Patch when the map still helps, but not enough.

## Rebuild When the Navigation Model Misleads

Rebuild the working file when the previous navigation model no longer reflects how the source is organized or how the skill should be used. Typical cases:

- the skill changed purpose
- the major routes through the skill changed
- route boundaries are now wrong or misleading
- the current map is harder to trust than rereading source directly

If the old `index.md` still captures the high-level purpose, keep its useful parts. Rebuilding does not mean discarding all prior understanding.

## Drift Can Be Structural or Practical

Not all drift comes from source edits.

Practical drift matters too:

- a route note exists but never helps
- a return point sounded precise but was too vague in actual use
- a reference file became central even though it started as optional
- the current route set no longer matches how work actually enters the skill

Refresh the map when real work exposes these mismatches. The trigger is loss of usefulness, not a calendar.

## How Practical Drift Usually Shows Up

Practical drift is usually noticed during lookup, not discovered by comparing hashes.

Common signals:

- you keep bypassing the same route note and reading source directly
- two sessions hesitate between the same two routes
- a return point sounds precise, but still forces a broad reread
- you keep explaining a reference's importance in chat because the map does not say it

Treat repeated detours and repeated hesitation as refresh signals. They are evidence that the map's navigation model is no longer matching real work.

## Promote References Carefully

Promote a reference into clearer route coverage when:

- the reference keeps holding the real answer
- sessions repeatedly jump to the same part of that reference
- the current working file no longer explains its importance well enough

Do not promote a reference path just because the file exists.

## Delete Weak Navigation

Delete or merge navigation when:

- a route no longer points to a recurring task
- two routes overlap so heavily that they cause hesitation
- the map lists entries that look plausible but keep sending sessions to the wrong place

Two strong route notes are better than six decorative ones.

## Leave the Map Alone When It Is Doing Its Job

Do not touch the map just because you used it.

Leave it alone when:

- it got you back to source quickly
- source confirmed the map's guidance
- nothing new about task shape, reference importance, or route quality was learned

## What to Record

When you refresh, leave a short trace in `changes.md`:

- what changed
- what triggered the refresh
- whether the old entry was stale, missing, misleading, or simply too coarse

This helps future sessions decide how much confidence to place in older entries.
