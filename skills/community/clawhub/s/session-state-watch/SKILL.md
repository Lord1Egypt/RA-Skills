---
name: session-state-watch
version: 1.0.2
description: "Detect SESSION-STATE.md changes from cron/background tasks and notify main session. Solves the 'cron writes, main session forgets' problem in OpenClaw."
keywords: ["session state", "state monitoring", "state tracking", "cron", "background tasks", "file change detection", "mtime", "OpenClaw"]
metadata: {"openclaw": {"category": "automation", "risk": "low"}}
---

# Session State Watch

## When to Use

Use this skill when:
- You have cron tasks that write results to `SESSION-STATE.md`
- You want the main agent session to automatically detect and respond to background task outputs
- You need to sync state between isolated cron sessions and the main session

This solves the common OpenClaw pain point: **cron tasks run in isolated sessions and their outputs written to files are invisible to the main session**.

## Problem It Solves

```
Cron Task (isolated session) → writes to SESSION-STATE.md → Main session (no idea it changed!)
```

Without this skill:
- Dream learning (04:30 cron) results are written but never seen
- Post-market learning (15:05 cron) updates are missed
- Any background task output is effectively lost

## Solution Architecture

The skill implements a **lightweight file mtime tracking** mechanism:

1. **Tracker file**: `~/.openclaw/workspace/data/.session_state_tracker.json` stores last known mtime
2. **Detection script**: `scripts/check_session_state.sh` compares mtime and reports changes
3. **Integration rule**: Added to `AGENTS.md` - check before substantive answers

## Quick Start

### 1. Install the Skill

The skill files are already in `~/.openclaw/workspace/skills/session-state-watch/`.

### 2. Initialize Tracker

```bash
mkdir -p ~/.openclaw/workspace/data
cat > ~/.openclaw/workspace/data/.session_state_tracker.json << 'EOF'
{
  "last_known_mtime": 0,
  "last_known_mtime_human": "never",
  "last_check_time": "1970-01-01T00:00:00",
  "session_start_mtime": 0
}
EOF
```

### 3. Add Detection Rule to AGENTS.md

Add this section to your `~/.openclaw/workspace/AGENTS.md`:

```markdown
## 🔔 Session State Change Detection (L3 Active Awareness)

**Problem**: Cron tasks (dream learning 04:30, post-market learning 15:05) modify `SESSION-STATE.md`, 
but the main session doesn't automatically know about the changes.

**Solution**: Before substantive answers (not simple acknowledgments), check if `SESSION-STATE.md` has been modified:

\```bash
# Check if SESSION-STATE.md is newer than tracker
MTIME=$(stat -c %Y /root/.openclaw/workspace/SESSION-STATE.md 2>/dev/null || echo "0")
TRACKER_JSON="/root/.openclaw/workspace/data/.session_state_tracker.json"
TRACKER=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('last_known_mtime', 0))" < "$TRACKER_JSON" 2>/dev/null || echo "0")
if [ "$MTIME" -gt "$TRACKER" ] 2>/dev/null; then
  echo "SESSION-STATE.md has been updated!"
  # Read the file and summarize changes
fi
\```

**Implementation**:
1. **Tracker file**: `data/.session_state_tracker.json` stores last-known mtime
2. **Check on answer**: Before substantive responses, run the check above
3. **If changed**: Read `SESSION-STATE.md`, summarize new content, update tracker
4. **Update tracker**: After reading, update `last_known_mtime` in tracker to current mtime

**Cron task integration**: Cron tasks that modify `SESSION-STATE.md` do NOT need to update the tracker. 
The tracker is only updated by the main session after reading the changes. This keeps detection simple: 
cron writes → mtime changes → main session detects mismatch.

**Why this works**:
- No need to modify OpenClaw core
- File-based tracking is simple and reliable
- Works across sessions and restarts
- Puts the intelligence in the agent (not the infrastructure)
```

### 4. Use the Check Script

The skill includes `scripts/check_session_state.sh`:

```bash
# Check if SESSION-STATE.md changed (reports and updates tracker)
bash ~/.openclaw/workspace/skills/session-state-watch/scripts/check_session_state.sh

# Force re-read even if unchanged
bash ~/.openclaw/workspace/skills/session-state-watch/scripts/check_session_state.sh --force

# Update tracker without reporting
bash ~/.openclaw/workspace/skills/session-state-watch/scripts/check_session_state.sh --update
```


### 5. Optional: Real-time Event-Driven Watch (inotify)

If you have `inotify-tools` installed, the script supports event-driven detection:

```bash
# Start watching (foreground)
bash scripts/check_session_state.sh --watch

# Background daemon
nohup bash scripts/check_session_state.sh --watch --daemon > /tmp/session-state-watch.log 2>&1 &

# Stop daemon
bash scripts/check_session_state.sh --stop-daemon
```

This mode uses Linux kernel inotify to detect file changes instantly, rather than polling on check.

## Files Included

| File | Purpose |
|------|---------|
| `SKILL.md` | This documentation |
| `scripts/check_session_state.sh` | Detection script (mtime comparison + report) |
| `examples/SESSION-STATE-update.py` | Example: how cron tasks should write updates |

## How Cron Tasks Should Write Updates

When a cron task (like dream learning or post-market learning) wants to notify the main session:

```python
# Example: realtime_data_learning.py
def _write_to_session_state(self, report: str):
    """Write learning report to SESSION-STATE.md for main session detection."""
    session_state_path = "/root/.openclaw/workspace/SESSION-STATE.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(session_state_path, "a", encoding="utf-8") as f:
        f.write(f"\n## 🤖 学习更新 {timestamp}\n\n")
        f.write(report)
        f.write("\n\n---\n")
    
    # Note: Do NOT update the tracker here - let the main session detect the mtime change
```

## Comparison with Alternatives

| Solution | Pros | Cons |
|----------|------|------|
| **This skill (file mtime)** | Lightweight, no external deps, simple | Manual check before answers |
| **inotify (Linux kernel)** | Real-time event-driven, instant detection | Requires daemon process; inotifywait not installed by default; harder to restart across reboots |
| **openclaw-watchdog** | Auto-recovery of interrupted sessions | Heavy (Python, systemd), different purpose |
| **cron --announce** | Native OpenClaw feature | Only sends message, doesn't persist state |
| **agent-memory-mcp** | Full memory server | Complex setup, different use case |

## Publishing to ClawHub

To publish this skill:

1. **Sign in to ClawHub**: Visit https://clawhub.ai and sign in with GitHub
2. **Publish command** (after signing in):
   ```bash
   openclaw skills publish skills/session-state-watch
   ```
3. **Or submit via web**: https://clawhub.ai/skills/publish

## Troubleshooting

**Q: Script says "unchanged" but I know it changed!**  
A: Check if the tracker was initialized correctly. Run with `--force` to reset.

**Q: How to handle multiple cron tasks writing simultaneously?**  
A: File appends are atomic in append mode. The mtime will reflect the latest write.

**Q: Can I use this for files other than SESSION-STATE.md?**  
A: Yes! The script is generic — modify `SESSION_STATE` path at the top, or pass a custom path as argument.

**Q: Why mtime instead of inotify (kernel file events)?**  
A: Three reasons: ① Zero dependencies — works on any system without extra packages. ② No daemon process — inotify requires a persistent watcher that needs to survive reboots. ③ Agent-native — the detection is triggered by the agent itself during its response cycle, so mtime polling adds zero overhead. For a real-time event-driven approach, add `inotifywait` to your system (apt install inotify-tools) and wrap a small loop; but mtime solves the problem with far less complexity.

**Q: SESSION-STATE.md keeps growing — how do I manage it?**  
A: The script auto-truncates when the file exceeds 2000 lines, keeping the last 1000 lines with a truncation notice at top. Check the `MAX_LINES` and `KEEP_LINES` variables in `check_session_state.sh` to adjust thresholds.

**Q: Cron task wrote something, but the main session didn't pick it up?**  
A: The main session only checks mtime **before substantive answers** (not simple acknowledgments). If it replies "OK" or "NO_REPLY" from heartbeat, the check won't run. Force detection by asking it to "check SESSION-STATE.md".

## Credits

This skill was created after researching:
- `ai7eam-dev/openclaw-watchdog` (similar idea, different implementation)
- OpenClaw native cron + session isolation architecture
- The need for lightweight state sync without external daemons

---

**Innovation**: This is believed to be the first **lightweight mtime-based session state detection** skill for OpenClaw that doesn't require external daemons or heavy dependencies.
