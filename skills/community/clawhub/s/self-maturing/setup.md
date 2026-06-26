# Setup — Self-Improving Agent v3.2

## 1. Run Init (one command, zero manual steps)

```bash
python3 ./skills/self-improving/scripts/agent_memory.py init
```

This does everything automatically:
- Creates `~/self-improving/` directory structure with **seeded** memory files
- Auto-fixes persistence (symlinks ~/self-improving/ → /data/ if needed)
- **Auto-injects** hooks into SOUL.md, AGENTS.md, HEARTBEAT.md (creates them if missing)
- Creates `SESSION-STATE.md` and today's daily log

**v3.2 difference:** No manual workspace file editing needed. Init handles everything.

## 2. Daily Review Cron (auto-created)

The SOUL.md hook (auto-injected by init) includes a self-healing cron check. On the next session start after init:
1. Agent reads SOUL.md (auto-injected by OpenClaw)
2. SOUL.md hook says "verify daily review cron exists"
3. Agent checks → cron doesn't exist → creates it automatically
4. Cron runs nightly from then on

**You don't need to manually create the cron.** If you want to create it manually (or the auto-create failed), run:

```bash
python3 ./skills/self-improving/scripts/agent_memory.py cron-prompt
```

### What the cron does every night:
1. Reads all self-improving memory files
2. Reviews the day's work from SESSION-STATE.md
3. Writes new lessons to ~/self-improving/memory.md
4. **Rewrites** SOUL.md, AGENTS.md, IDENTITY.md, HEARTBEAT.md with new hardcoded rules
5. Updates index, demotes stale patterns, trims corrections to 50
6. Reports what changed

### Why a cron?
v2 relied on the agent remembering to log lessons during work. After context resets, agents skip this even though the instructions are in SOUL.md. The cron is a forcing function — even if the agent forgets all day, the nightly review catches everything.

## 3. Workspace Hooks Reference

Init auto-injects these. Listed here for reference only — you don't need to add them manually.

### SOUL.md — add before your Prime Directive / closing section:
```markdown
## Self-Improving
On EVERY new session or context reset, IMMEDIATELY:
1. Read SESSION-STATE.md and ~/self-improving/memory.md before doing anything else.
2. VERIFY the daily review cron exists: use the cron tool (action=list) and look for "Self-Improving Daily Review". If it does NOT exist, CREATE IT NOW:
   - name: "Self-Improving Daily Review + .md Rewrite"
   - schedule: cron "0 23 * * *" in user's timezone
   - sessionTarget: isolated
   - payload: agentTurn with the review prompt (run: python3 ./skills/self-improving/scripts/agent_memory.py cron-prompt)
   - Do NOT set a model — use the default
   - delivery: announce
   After creating, run: python3 ./skills/self-improving/scripts/agent_memory.py mark-cron
   This is NON-NEGOTIABLE. The skill does not work without this cron.
3. When the user corrects you or you learn something reusable, IMMEDIATELY write to ~/self-improving/corrections.md BEFORE responding (WAL protocol). The nightly cron reviews corrections.md — if nothing is written during the day, the cron has nothing to promote. WAL is what feeds the cron.
4. Prefer learned rules when relevant. Keep self-inferred rules revisable.
```

### AGENTS.md — add to Memory section:
```markdown
- **Self-improving:** ~/self-improving/ — execution-quality memory (preferences, patterns, corrections)
- Use MEMORY.md / memory/ for factual continuity. Use ~/self-improving/ for compounding execution quality.
```

### HEARTBEAT.md — add:
```markdown
## Self-Improving Check
- Read ./skills/self-improving/heartbeat-rules.md
- Use ~/self-improving/heartbeat-state.md for run markers
- If no file in ~/self-improving/ changed since last review, skip maintenance
```

## 4. Gateway Config (Recommended)

Add `~/self-improving/` to the memory search index:

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        extraPaths: ["~/self-improving"]
      }
    }
  }
}
```

## 5. Verify Installation

```bash
python3 ./skills/self-improving/scripts/agent_memory.py verify
```

This checks:
- ✅ Directory structure exists
- ✅ Core files exist and have content
- ✅ Memory is seeded (not empty)
- ✅ SESSION-STATE.md exists
- ✅ Workspace hooks in SOUL.md, AGENTS.md, HEARTBEAT.md
- ℹ️ Reminder to verify daily review cron

## 6. Test Cold-Boot Recovery

```bash
python3 ./skills/self-improving/scripts/agent_memory.py boot
```

## What Survives What

| Event | What's preserved | What's lost | Recovery |
|-------|-----------------|-------------|----------|
| Context compaction | All files on disk | Conversation details | MEMORY.md auto-loads. Read SESSION-STATE.md. |
| Gateway restart | All files on disk | In-flight conversation | Same as compaction. |
| Container restart | All files in mounted volumes (/data/) | Anything outside /data/ | ~/self-improving/ must be persistent. |
| Full wipe | Nothing | Everything | Restore from git backup. |

## ⚠️ Critical: Storage Persistence

`~` resolves to the home directory of the user running the agent. Make sure this is on persistent storage:

- **Docker**: Mount a volume at the home dir, or symlink ~/self-improving → /data/.openclaw/workspace/self-improving/
- **Bare metal**: ~/self-improving/ is fine
- **Back it up**: Include ~/self-improving/ in your workspace git repo
