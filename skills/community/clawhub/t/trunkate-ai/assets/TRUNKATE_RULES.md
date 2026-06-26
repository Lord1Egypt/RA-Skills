# Trunkate AI: Optimization Rules

Define patterns or files that should be preserved during the proactive truncation process.

## Protected Identifiers

- `SYSTEM_INSTRUCTIONS`: Always preserve the initial system prompt.
- `PROJECT_ROOT/CLAUDE.md`: Never truncate the primary project rules.
- `PROJECT_ROOT/.env`: Do not send sensitive environment variables to the API.

## Custom Directives

- `[KEEP]`: Any block wrapped in these tags will be ignored by the pruner.
