# Auto-Checkpoint Signals

Internal trigger reference for `/checkpoint auto` mode. Not invoked by the user — the agent scans for these signals and acts autonomously.

---

## Signal Categories

### 🔴 High Priority — Context Risk

These signals mean "checkpoint immediately or lose work":

| Signal | Description | Response |
|--------|-------------|----------|
| Context >75% | `session_status` shows high usage | Save autosave immediately |
| `<summary>` tag in session start | Context was truncated | Save autosave, read working-buffer |
| "context limit" in message | Context approaching limit | Save autosave before continuing |
| "truncated" in message | Message was cut off | Save autosave, read working-buffer |
| Compaction triggered | Automatic context compression | Save autosave post-compaction |

### 🟡 Medium Priority — Close Signals

These signals mean "session is ending, save your place":

| Signal | Keywords | Response |
|--------|----------|----------|
| Sleep / logout | "goodnight", "晚安", "睡觉了", "休息了" | Save autosave |
| Exit intent | "logout", "退出", "关闭", "exit", "bye" | Save autosave |
| Tomorrow intent | "明天见", "下次继续", "later", "tomorrow" | Save autosave |
| Session idle | >10 min idle with active work (SESSION-STATE not empty) | Save autosave |

### 🟢 Low Priority — Long Operation

These signals mean "a lot of work is about to happen, protect it":

| Signal | Description | Response |
|--------|-------------|----------|
| Multi-step workflow | >3 steps remaining in known plan | Save autosave before start |
| Build/compile command | `npm run build`, `make`, `dotnet build`, etc. | Save autosave before start |
| Data processing | Script expected to run >30s | Save autosave before start |
| Deployment | Any deploy script | Save autosave before start |

---

## Signal Combination Logic

Multiple signals together increase urgency:

```
Context >75% + close signal = CRITICAL → immediate autosave
Context >60% + long op signal = HIGH → save before running command
Close signal alone = MEDIUM → save autosave
Long op signal alone = LOW → consider saving, not mandatory
```

---

## What to Check Before Autosaving

Before writing `autosave.md`, verify:

1. **SESSION-STATE.md has actual content** — don't save empty checkpoint
2. **Task is incomplete** — if task is done, no need to autosave
3. **Autosave doesn't already exist** — if one was just saved (<5 min ago), don't overwrite

---

## Autosave File Location

```
memory/checkpoints/autosave.md
```

**Important:** Named checkpoints (`/checkpoint save <name>`) are never overwritten by autosave. Autosave only ever writes to `autosave.md`.

---

## Quiet Confirmation

When autosave fires, write a minimal log entry — do NOT produce verbose user output:

```
# Autosave log
- [2026-05-12 15:50] autosave written (context 78%)
- [2026-05-12 16:30] autosave written (close signal: goodnight)
```

Store this log at `memory/checkpoints/autosave-log.md` so it can be reviewed if needed.