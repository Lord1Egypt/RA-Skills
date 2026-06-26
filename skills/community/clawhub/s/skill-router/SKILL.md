---
name: skill-router
description: Route the current task to the most relevant installed skill, and only suggest new skills when existing ones are not enough. Use when the user asks things like "do we already have a skill for this", "which skill should we use", "did we install something for this", or when multiple installed skills could fit and the main problem is choosing the best one without wasting tokens or adding noise.
---

# Skill Router

Skill Router is a low-presence routing layer for skill-heavy environments.

Its job is not to repeat normal skill triggering. Its job is to help when **skill choice itself** becomes a meaningful decision.

For portable/public use, route by capability first, then resolve capability to installed skills. Do not assume one workspace's local skill names are universal.

## Use this skill to decide, not to announce

When active, do not dump a list of installed skills.
Do not explain the skill ecosystem unless the user explicitly wants that.
Do not interrupt simple tasks just to mention skills.

Instead, answer one question:

**Given the current task, which installed skill is most worth using right now?**

For portable use, infer likely fit from installed skill names and descriptions at runtime. Use local maps only as optional shortcut layers, not as universal truth. If no strong installed match exists, do not fake one; fall back to general guidance or discovery.

## Only intervene when routing is genuinely useful

Typical high-value situations:
- the user explicitly asks whether a relevant skill already exists
- the user asks which skill should be used
- multiple installed skills could plausibly fit
- an installed skill is easy to forget, but would clearly reduce wasted work
- the task is about installing or finding new skills, and existing skills should be checked first

Do not intervene just because a skill could theoretically apply.
If the default trigger path is already obvious and sufficient, stay out of the way.
If normal skill triggering already solved the task cleanly, Skill Router adds no value and should remain silent.

## Core routing order

Always prefer this order:
1. installed strong match
2. installed combination of skills, if one alone is not enough
3. installed general fallback
4. only then route to discovery / installation of something new

Skill Router exists to improve reuse of existing skills before expanding the skill set.
When no strong installed match exists, route to discovery rather than pretending capability already exists.
Even if the user explicitly asks to find or install a new skill, still prefer reuse first when an installed skill is already sufficient for the task.
If an installed skill can complete the task without clearly increasing failure risk or wasted work, do not trigger discovery just because another skill might be more specialized or more novel.
Follow `references/resolution-order.md` when the ranking is not obvious.

## Output rules

Keep routing advice short, concrete, and low-noise.

Default output shape:
1. current best skill choice
2. why this is the best fit
3. optional backup choice, only if actually helpful
4. immediate next step

### Compression rule
If a good routing answer fits in one or two sentences, stop there.
Do not visibly expand into framework language.
Do not expose capability-taxonomy or routing-theory language unless the user explicitly asks for design detail.

Examples of good outputs:
- "This is a browser-control task. We already have `pinchtab-browser`; use that instead of a generic browser workflow."
- "I don't see a strong installed match for this yet. Start with `find-skills`; if a candidate comes from an unfamiliar source, run `skill-vetter` before installing it."
- "For this GitHub task, `github` is the right default. Use `clawhub` only if the task is specifically about skill publishing."

Examples of bad outputs:
- long lists of every related skill
- repeating what the user already knows
- suggesting new skill installation before checking existing skills
- showing routing theory when one short recommendation would do

## References

Read `references/capability-taxonomy.md` first when you need to map a task to a capability rather than jump to a skill name.
Read `references/resolution-order.md` when multiple installed skills could fit.
Read `references/publish-safe-runtime-contract.md` to keep routing portable and grounded in the user's actual installed environment.
Read `references/task-to-skill-map.md` only as a workspace-specific shortcut map for the current environment.
Read `references/local-overrides-example.md` when thinking about local preferences versus public defaults.
Read `references/reminder-policy.md` when deciding whether to stay silent or give a light reminder.
Read `references/micro-routing-examples.md` to keep discovery-vs-reuse decisions stable.

## Final rule

Skill Router succeeds when it reduces cognitive load.
If it makes the task feel heavier, it is routing badly.
