# Operations

## Data Format

Use compact markdown records.

### Rule Entry Template (`rules.md`)

```markdown
- id: RULE-YYYYMMDD-XXX
  statement: <normalized rule text>
  scope: context | global
  context_key: <context-key or global>
  status: active | archived
  confirmed_by_user: yes
  occurrence_count: <n>
  first_seen: <ISO-8601>
  last_seen: <ISO-8601>
  source: <corrections file + id>
```

### Correction Entry Template (`corrections.md`)

```markdown
- id: CORR-YYYYMMDD-XXX
  raw_input: <verbatim user correction>
  normalized_key: <lowercase canonical key>
  proposed_rule: <candidate statement>
  scope_candidate: context | global
  context_key: <active context-key>
  status: pending | confirmed | rejected | promoted
  occurrence_count: <n>
  created_at: <ISO-8601>
  updated_at: <ISO-8601>
```

## Canonicalization

Build `normalized_key` by:
1. lowercase
2. trim spaces
3. collapse internal whitespace
4. remove punctuation not needed for meaning

Use this key for dedupe and recurrence counts.

## Write Flow

1. Determine `context-key`.
2. Parse correction/preference candidate.
3. Compute `normalized_key`.
4. Search active `corrections.md` and `rules.md` for same key.
5. If exists, increment `occurrence_count` and `updated_at`.
6. Else append new correction entry.
7. If user explicitly confirms, promote to `rules.md`.
8. If confirmed in 2+ contexts, propose global promotion.
9. Update `index.md` counters and timestamps.

## Query Flow

### "What did you learn?"
- Show last 10 active-context corrections.
- Show last 5 global corrections.

### "Show my rules"
- Show active context rules first.
- Then show global rules.

### "Memory stats"
Report:
- total contexts
- active/global rule counts
- pending correction counts
- last updated timestamp

## Forget Flow

### "Forget X"
1. Remove matching entries in active context.
2. Ask whether to remove global/all contexts.
3. Apply requested scope.
4. Confirm files and counts touched.

### "Forget everything"
1. Ask deletion scope first.
2. Delete only requested scope.
3. Confirm completion with counts.

Do not export automatically.

## Source Citation

When applying a learned rule, cite:
- rule id
- source file path

Example:
`Using RULE-20260303-002 from contexts/acme-api/rules.md`
