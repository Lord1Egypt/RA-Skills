# Memory Template - Safari Browser Control

Create `~/safari/memory.md` with this structure:

```markdown
# Safari Browser Control Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Context
- Activation preference:
- Preferred control mode:
- Daily session control allowed:
- Main Safari targets:
- Risk boundaries:
- Preferred output shape:

## Notes
- Durable permission and control lessons
- Snippets and recipes worth reusing
- Recovery sequences that worked

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Keep learning modes, permission state, and failure patterns |
| `complete` | Defaults are stable | Focus on execution and maintenance |
| `paused` | User wants minimal setup | Help without pushing deeper tracking |
| `never_ask` | User wants no setup prompts | Do not ask integration questions unless requested |

## File Templates

Create `~/safari/permissions.md`:

```markdown
# Permissions

## Control Path
- Apple Events:
- Screen Recording:
- JavaScript path:
- safaridriver enabled:
- Notes:
```

Create `~/safari/sessions.md`:

```markdown
# Sessions

## Session
- Mode: real Safari | safaridriver
- Target:
- Risk level:
- Reuse allowed:
- Notes:
```

Create `~/safari/snippets.md`:

```markdown
# Snippets

## Snippet
- Goal:
- Command:
- Preconditions:
- Verification:
```

Create `~/safari/recipes.md`:

```markdown
# Recipes

## Recipe
- Goal:
- Mode:
- Steps:
- Verification:
```

Create `~/safari/incidents.md`:

```markdown
# Incidents

## YYYY-MM-DD - Incident
- Surface:
- Symptom:
- Cause found:
- Fix applied:
- Follow-up:
```

## Key Principles

- Store only durable context that improves future Safari control and recovery.
- Summarize permissions, snippets, and incidents instead of archiving raw browsing history or sensitive page content.
- Keep mode, risk, and approval boundaries explicit.
- Update `last` whenever durable defaults, snippets, or operating boundaries change.
