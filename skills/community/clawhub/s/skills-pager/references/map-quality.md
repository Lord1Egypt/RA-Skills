# Map Quality

Use this reference when you need to judge whether a pager map is genuinely useful or merely well-formatted.

## A Good Map Lets a Fresh Session Answer

- Does this skill apply to the task?
- Where should reading start?
- Which route or reference is most likely to contain the answer?
- Which parts are safe to ignore for now?

If the map cannot answer those questions quickly, improve the map before adding more detail.
A good map reduces orientation cost and blind rereading. It does not replace source verification when details matter.

## Strong Map Signals

- `index.md` explains scope in plain language instead of echoing headings
- the route notes name recurring task shapes rather than chapter titles
- the file makes important sources easy to spot
- the return points point to places people actually need to relocate precisely
- the file exists on disk, so a fresh session can reuse it
- optional `changes.md` explains why the map changed, not just that it changed

## Weak Map Signals

- the working file is a paraphrased table of contents
- the route notes simply mirror source headings
- many sub-sections exist, but none match the real way work enters the skill
- return points exist for every heading but help with none of the real lookups
- reference files are listed but their importance is unclear
- the chat answer sounds structured, but no working map file was created

Weak maps feel organized, but they do not reduce search effort.

## Misleading Map Signals

- the route title sounds right, but repeatedly starts in the wrong place
- the return point label is more specific than the source it points to
- the map still centers `SKILL.md` even though the real detail lives in `references/`
- the working file sounds current, but its route notes no longer match the source

Misleading maps are worse than thin maps because they waste confidence before they waste time.

## Before / After Example

Weak route note:

```markdown
### Configuration
- Start source: Configuration
```

Why it is weak:

- it repeats the heading
- it does not say when to use the route
- it does not tell a future session what is inside

Stronger route note:

```markdown
### Adding a New Provider
- When to start here: enabling a provider that the team has not configured before
- Start source: Provider Setup
- What to verify: provider prerequisites, authentication, verification
- Next likely checks: the verification checklist lives in the reference appendix, not the main setup section
```

Why it is stronger:

- it names a real task shape
- it gives a clear starting point
- it tells the next session where the critical detail actually lives

## Quality Check

Before you call a map "good enough", ask:

1. Would a fresh session know where to begin?
2. Would the map send it back to source fast?
3. Would the map keep it from rereading obviously irrelevant sections?
4. Would the route labels and return points still make sense a week from now?
