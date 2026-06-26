# Memory Template — Skill Finder

Create `~/skill-finder/memory.md` with this structure:

```markdown
# Skill Finder Memory

## Status
status: ongoing
last: YYYY-MM-DD
sources: both
integration: proactive

## Preferences
<!-- Explicit quality values stated by user -->
<!-- Examples: "prefers minimal", "wants well-maintained", "okay with experimental" -->

## Source Policy
<!-- Default source mode: both, clawhub, or skills.sh -->
<!-- Example: both -->
<!-- Install scope for `npx skills add`: ask, project, or global -->

## Liked
<!-- Skills user explicitly praised, with their reason -->
<!-- Format: source:identifier — "what they said they liked" -->
<!-- Examples: clawhub:skill-manager — "clear and safe" -->
<!--           skills.sh:vercel-labs/agent-skills@frontend-design — "great for UI work" -->

## Passed
<!-- Skills user explicitly declined, with their reason -->
<!-- Format: source:identifier — "what they said was wrong" -->

## Domains
<!-- Areas user works in (helps narrow searches) -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning preferences |
| `established` | Has enough preference data |

## What to Store

### Source Policy (from explicit statements)
- "Search both" → `sources: both`
- "Only use ClawHub" → `sources: clawhub`
- "Only use Skills.sh" → `sources: skills.sh`
- "Prefer project installs" → add under `## Source Policy`
- "Prefer global installs" → add under `## Source Policy`

### Preferences (from explicit statements)
- "I prefer minimal skills" → add verbatim
- "I want well-maintained only" → add verbatim
- "I don't mind experimental" → add verbatim

### Liked (from explicit praise)
- User says "this skill is great because X" → `source:identifier — "X"`
- User expresses satisfaction → `source:identifier — "reason"`

### Passed (from explicit rejection)
- User declines with reason → `source:identifier — "reason"`
- User uninstalls and explains → `source:identifier — "reason"`

## What NOT to Store

- Silent installations (no comment = no data)
- Inferred preferences from behavior patterns
- Anything not explicitly stated by user

## Using Memory

When multiple skills match a search:
1. **Check source mode** — Search `both`, `clawhub`, or `skills.sh` accordingly
2. **Check Passed** — exclude similar
3. **Check Liked** — favor similar qualities
4. **Apply Preferences** — filter accordingly

## Maintenance

Keep under 50 lines. When exceeded:
- Archive old Liked/Passed entries
- Keep most recent Preferences
