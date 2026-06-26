# Install Snippets — 待追加到用户文件的内容

## Append to AGENTS.md

```markdown
## Memory Management (memory-keeper)

### Session Startup — 3-Tier Load

1. Read `memory/tasks.md` (hot tier)
   - Found in-progress task → say: "Last time you were working on [task], at [status]. Next step: [next]. Continue?"
   - Multiple in-progress → list all, let user choose
   - None → skip

2. Read today's journal `memory/YYYY-MM-DD.md` + last 7 days (warm tier)
   - Not found → skip (heartbeat creates it automatically)
   - Found → read to restore recent context

3. Read `MEMORY.md` only when user mentions a specific project (cold tier)

### When to update tasks.md (trigger immediately, don't wait)

Update `memory/tasks.md` when:
1. A clear milestone is reached (version released, bug fixed, module completed)
2. User sends a pause signal: "that's it", "pause", "let's stop here", "I'll be back", etc.

> These are the only reliable triggers. Don't count turns or monitor context size.

### On project changes
When creating/deleting projects, releasing versions, or changing Git URLs:
read `skills/memory-keeper/SKILL.md` and update the project index in `MEMORY.md`.
```

## Append to HEARTBEAT.md

```markdown
## Daily Journal Check

On each heartbeat:

1. Check if today's journal `memory/YYYY-MM-DD.md` exists
   - Not found → create it using the template below (once only, never duplicate)
   - Found → skip

**Journal template:**
# YYYY-MM-DD

## Today's Work
<!-- Group by topic, skip empty sections -->

## Validated Approaches
<!-- What worked and was approved — format: Rule / Why / Trigger -->

## Key Decisions
<!-- Decisions with context and reasoning -->

## Watch List
<!-- Unresolved risks, potential regressions -->

## Lessons Learned
<!-- Format: Rule / Why / When to apply -->

2. **Dream consolidation (version-aware):**
   - Run `openclaw --version` and parse as YYYY.M.R
   - **>= 2026.4.8**: check if native Dreaming is enabled (openclaw.json → plugins.entries.memory-core.config.dreaming.enabled)
     - Enabled → skip all Dream logic below
     - Not enabled → check `memory/dream-state.json`:
       - Exists AND `lastDream != "2000-01-01"` (upgrade from old version) → notify: "检测到你升级到了 2026.4.8+，建议开启原生 Dreaming（`/dreaming on`）。开启后旧 Dream 状态文件会自动清理。"
       - Otherwise (fresh install) → notify once: "建议开启原生 Dreaming，在任意 session 中发送 /dreaming on 即可。"
       - After user enables native Dreaming → delete `memory/dream-state.json`
     - Then skip all Dream logic below
   - **< 2026.4.8**: continue with steps 2a-2d below

   2a. Update Dream state: read `memory/dream-state.json`
   - Not found → create: {"lastDream": "2000-01-01", "sessionsSinceLastDream": 0}
   - Today's journal was just created (first heartbeat of the day) → increment sessionsSinceLastDream by 1
   - Today's journal already existed → skip (no double-counting)

   2b. Check Dream trigger (both conditions required):
   - lastDream is more than 7 days ago
   - sessionsSinceLastDream >= 3
   → If triggered: run Dream consolidation (see skills/memory-keeper/SKILL.md Part 4), then reset counter

3. If nothing needs attention, reply HEARTBEAT_OK
```

## Initialize memory/tasks.md

```bash
mkdir -p ~/.openclaw/workspace/memory
cat > ~/.openclaw/workspace/memory/tasks.md << 'EOF'
# Task State

## In Progress

## Completed (archive)
EOF
```
