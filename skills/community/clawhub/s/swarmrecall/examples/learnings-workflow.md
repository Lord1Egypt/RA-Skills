# Learnings workflow — log errors, surface patterns

The learnings module turns one-off errors and corrections into recurring patterns the agent can prevent next time.

## 1. Log a learning when something breaks

```bash
swarmrecall learnings log \
  --category error \
  --summary "npm install fails with peer dep conflict" \
  --details "$(cat /tmp/npm-output.log)" \
  --priority high \
  --area build
```

Categories: `error | correction | discovery | optimization | preference`.
Priorities: `low | medium | high | critical`.

*(MCP: `learning_log`.)*

## 2. On session start, preload known patterns

```bash
swarmrecall learnings patterns
```

Returns clusters of related learnings the system has identified. Use these to anticipate problems the user is about to hit.

*(MCP: `learning_patterns`.)*

## 3. Check for promotion candidates

```bash
swarmrecall learnings promotions
```

Returns patterns that have accumulated enough supporting learnings to become first-class rules. Surface each candidate to the user for approval before promoting — never auto-promote.

*(MCP: `learning_promotions`.)*

## 4. Resolve a learning

Once you fix the root cause, close the learning with a resolution summary:

```ts
await client.learnings.resolve(learning.id, {
  resolution: 'Added --legacy-peer-deps to the install command in ci.yml',
  commit: 'abc1234',
});
```

*(MCP: `learning_resolve`.)*

## 5. Link related learnings

When you discover that two errors share a root cause:

```ts
await client.learnings.link(learningA.id, learningB.id);
```

Linking contributes to pattern detection on the next cycle.

*(MCP: `learning_link`.)*

## Tips

- Use `area` to partition learnings by subsystem (`build`, `auth`, `ingest`, `ui`, etc.). Search and list both filter by area.
- Include the raw error output in `details` — semantic search across that text is how future agents will find the pattern.
- Run `learning_search` before logging a new error so you don't duplicate an existing learning; link instead.
