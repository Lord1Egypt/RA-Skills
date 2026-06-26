# Resume Flow — Step-by-Step Decision Tree

When to resume, how to present it, and what to do if the checkpoint is stale.

---

## Session Start Sequence

```
1. Session starts (fresh or resumed)
2. Check for checkpoint files: ls memory/checkpoints/
3. If checkpoints exist:
   a. Present summary to user: "Found N checkpoint(s): [names]"
   b. Ask: "Resume any of these?"
   c. If yes → run /checkpoint resume <name>
   d. If no → continue fresh, keep checkpoints for later
4. If no checkpoints → proceed normally
```

---

## Resume Decision Tree

```
User says "continue" or "where did we stop?"
│
├─ Checkpoints exist?
│   ├─ Yes → Present checkpoint table, ask which to resume
│   └─ No → "No checkpoints found. Starting fresh."
│
User says "resume <name>"
│
├─ Checkpoint <name> exists?
│   ├─ Yes → Read checkpoint → present briefing → wait for confirm
│   └─ No → "No checkpoint named '<name>'. Run /checkpoint list to see available."
│
Detected <summary> tag or compaction signal
│
├─ Check for autosave checkpoint
│   ├─ Exists and recent (<24h) → Ask: "Unfinished work detected. Resume autosave?"
│   ├─ Exists but old (>24h) → Ask: "Autosave found but is N hours old. Resume anyway?"
│   └─ No autosave → Proceed with compaction recovery (from working-buffer.md)
```

---

## Presentation Format for Resume

When presenting a checkpoint to the user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Resume: <task name>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Saved: YYYY-MM-DD HH:MM (N hours ago)

✅ Progress:
- <completed item 1>
- <completed item 2>

🔜 Next action:
<code or command or description>

⚠️ Blockers:
- <blocker 1>
- <blocker 2>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Continue from this point? (yes/no)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## If Checkpoint is Stale

A checkpoint is stale if:
- Referenced files no longer exist
- The next action references outdated commands
- Context has fundamentally changed (e.g., new project structure)

**Stale checkpoint protocol:**

1. Present checkpoint with note: "⚠️ This checkpoint may be stale (N days old)"
2. Show what's stale (file missing, command outdated)
3. Ask: "Resume anyway (re-evaluate), or start fresh?"
4. If "resume anyway": read checkpoint, re-validate all references, proceed
5. If "start fresh": delete stale checkpoint, proceed normally

---

## Auto-Checkpoint Signals

The agent should trigger `/checkpoint auto` (save to autosave) when:

### High Context Signal
- `session_status` shows context >70%
- Agent receives "context warning" or "truncated" signal

### Close Signals
User says any of:
- "goodnight" / "晚安" / "睡觉了"
- "logout" / "退出" / "关闭"
- "明天见" / "下次继续"
- Session idle for >10 minutes with active work

### Long Operation Signal
- About to run a command that takes >30 seconds
- Multi-step workflow with >3 steps remaining

### Compaction Signal
- `<summary>` tag detected at session start
- Session restored from compaction (context was truncated)

---

## Deep Resume (Cross-Day)

For tasks spanning multiple days:

1. **Day 1:** User creates named checkpoint before close
   - `/checkpoint save project-alpha-phase2`

2. **Day 2:** Agent detects checkpoint on session start
   - Presents "Found checkpoint from yesterday: project-alpha-phase2"
   - User confirms resumption

3. **Day N:** Checkpoint may have grown (updated on subsequent sessions)
   - Same system: checkpoint is just a file, updated each session
   - Age indicator helps user decide if it's still relevant

---

## Verification Before Resume

Before executing from a checkpoint:

1. **File existence check:** Confirm referenced files still exist
2. **Git state check:** If project, confirm branch/working tree matches checkpoint
3. **Context validity:** If working on code, confirm the relevant section hasn't changed

If any check fails:
- Warn user before proceeding
- Offer to update checkpoint with new state before resuming