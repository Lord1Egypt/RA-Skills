# Heartbeat Checklist

On each heartbeat that should maintain the task system:

1. Read installation config
2. Check whether `todo/NOW.md` exists; initialize if missing
3. Locate today's per-agent JSONL files
4. Parse valid lines for all enabled agents
5. Refresh `AI USAGE THIS WEEK` and `AI DONE TODAY`
6. Update sync state
7. If the date rolled over, initialize the new monthly history file if missing
8. Keep human task sections untouched unless explicitly asked to reprioritize

If nothing changed, do not rewrite the dashboard unnecessarily.
