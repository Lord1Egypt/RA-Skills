# Resolution Order

After identifying the dominant capability, resolve to installed skills in this order.

---

## 1. Installed strong match
Recommend an installed skill that is clearly specialized for the capability.

## 2. Installed combination
If one skill is not enough, suggest a small combination of installed skills.
Only do this when it materially changes the next step.

## 3. Installed general fallback
If no strongly specialized installed skill exists, suggest the best general installed fallback.

## 4. External discovery
Only after installed options are clearly insufficient, route to discovery.

Preferred discovery flow:
1. use `find-skills` to search for candidates
2. if the candidate is unfamiliar or third-party, route through `skill-vetter` before installation
3. only then proceed to install/update actions

---

## Ranking hints

When multiple installed skills could fit the same capability, prefer:
1. the more specific skill
2. the more obviously task-aligned skill
3. the user-named skill, if the user already pointed to one
4. the skill that reduces the most wasted work right now

If two skills are similar and either would work, recommend just one unless the backup changes the plan.

---

## Silence rule

If the right skill is already clearly active or obviously implied, do not add extra routing commentary.

Skill Router is for reducing selection cost, not for narrating it.

## Reuse-first rule

Even when the user explicitly asks for a new skill, prefer an installed skill first if it already covers the task well enough.
If an installed skill can complete the task without clearly increasing failure risk or wasted work, do not route to discovery just because another skill might be more specific or more novel.
Discovery is for insufficiency, not novelty.
