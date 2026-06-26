# Release Checklist

## Initialization
- [ ] New installation can create required folders and files
- [ ] Missing state files can be repaired
- [ ] Month history file auto-creates if absent
- [ ] Today's empty AI log files auto-create for enabled agents
- [ ] Managed logging rules can be installed into configured `AGENTS.md` files

## Sync
- [ ] AI logs with valid lines rebuild `AI DONE TODAY`
- [ ] Malformed lines are skipped without aborting sync
- [ ] Empty logs result in `AI DONE TODAY` showing only `- 暂无`
- [ ] `AI USAGE THIS WEEK` rebuilds from OpenClaw usage summary
- [ ] `Total Tokens` in the usage table uses `input + output`
- [ ] `Cache` is shown separately from fresh tokens

## Rollover
- [ ] Explicit `[x]` items in active sections move into archive
- [ ] Existing `DONE` is archived
- [ ] AI snapshot is archived
- [ ] History is grouped by clipped week sections
- [ ] The target week's `AI Usage Weekly Summary` is updated
- [ ] `FOCUS` and `TODAY` unfinished items move into new `TODAY`
- [ ] `UP NEXT` stays unchanged
- [ ] `FOCUS` resets
- [ ] Rollover is idempotent

## Validation
- [ ] `node scripts/validate_system.js` passes
- [ ] A real `sync_ai_done.js` run succeeds against a live config
