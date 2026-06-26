# Logging Format

Entry formats for `.learnings/` files.

## Learning Entry

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Scope**: global | domain | project

### Summary
One-line description of what was learned.

### Details
Full context: what happened, what was wrong, what is correct.

### Suggested Action
Specific fix or improvement to make.

### Metadata
- Source: conversation | error | user_feedback | self_reflection
- Domain: coding | communication | ops | writing | other
- Project: project-name (if applicable)
- Recurrence-Count: 1
- First-Seen: YYYY-MM-DD
- Last-Seen: YYYY-MM-DD
- See Also: LRN-XXXXXXXX-XXX (if related)
```

## Error Entry

Append to `.learnings/ERRORS.md`:

```markdown
## [ERR-YYYYMMDD-XXX] command_or_tool_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending

### Summary
Brief description of what failed.

### Error
Actual error message (redact secrets with [REDACTED]).

### Context
- Command attempted
- Parameters used
- Environment details if relevant

### Suggested Fix
What might resolve this.

### Metadata
- Reproducible: yes | no | unknown
- Domain: coding | ops | integration | other
- See Also: ERR-XXXXXXXX-XXX (if recurring)
```

## Feature Request Entry

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending

### Requested Capability
What the user wanted to do.

### User Context
Why they needed it, what problem they are solving.

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built.

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name
```

## HOT Memory Entry

Entries in `.self-improving/HOT.md` are short, actionable rules:

```markdown
- User prefers concise answers over long explanations.
- For task berat, spawn subagent instead of doing inline.
- Never guess config changes; read docs first, backup before editing.
- In group chats, do not respond to every message.
```

Keep each entry to one line. Maximum 80 lines total.

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`

- TYPE: `LRN` (learning), `ERR` (error), `FEAT` (feature)
- YYYYMMDD: current date
- XXX: sequential number starting from 001 per day, or 3 random alphanumeric chars

Examples: `LRN-20260405-001`, `ERR-20260405-A3F`, `FEAT-20260405-002`

## Resolving Entries

When an issue is fixed, update the entry:

```markdown
**Status**: resolved

### Resolution
- **Resolved**: ISO-8601 timestamp
- **Notes**: Brief description of what was done
```

Other status values:
- `in_progress` — actively being worked on
- `wont_fix` — decided not to address (add reason)
- `promoted` — elevated to workspace file (add `Promoted-To: <file>`)
- `archived` — moved to cold storage
