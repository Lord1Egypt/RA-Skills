# Task to Skill Map (Local Map Pattern)

This file is an example of a **local shortcut map**, not a universal registry.

Use it only as a local resolution helper after:
1. capability matching
2. installed-skill inspection
3. resolution-order checks

For public or portable routing logic, the main references are:
- `capability-taxonomy.md`
- `resolution-order.md`
- `publish-safe-runtime-contract.md`

---

## What this file is for

A local environment may keep a small map like this to speed up tie-breaking when multiple installed skills are already known.

Examples:
- browser-control → prefer the locally validated browser skill
- github-workflow → prefer the locally validated GitHub skill
- skill-vetting → prefer the locally trusted vetting skill
- distillation → prefer the locally used distillation skill

These are local shortcuts, not assumptions about every user's install set.

---

## What this file is NOT for

Do not use this file to:
- assume those exact skill names exist everywhere
- skip inspection of the user's actual installed skills
- override installed reality with author preferences
- recommend discovery when a sufficient installed skill already exists

---

## Example local map shape

A local environment may define entries like:
- browser-control → [preferred browser skill]
- browser-reading → [preferred browser-reading skill]
- github-workflow → [preferred GitHub skill]
- skill-discovery → [preferred skill search skill]
- skill-vetting → [preferred skill vetting skill]
- skill-publishing → [preferred skill publishing skill]
- distillation → [preferred distillation skill]
- sop-generation → [preferred SOP skill]
- notes-vault → [preferred notes skill]
- summary-extraction → [preferred summary skill]
- weather-info → [preferred weather skill]

The exact values depend on the current user's environment.

---

## Rule

Installed reality beats local shortcut maps.
If the current environment does not contain a mapped skill, do not route as if it does.

If the local map conflicts with the actual installed environment, the local map loses.
