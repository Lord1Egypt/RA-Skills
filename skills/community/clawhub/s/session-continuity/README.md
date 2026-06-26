# Session Continuity for OpenClaw

Save your place. Resume exactly where you left off — even days later.

A skill for [OpenClaw](https://github.com/openclaw/openclaw) that treats checkpoints as first-class artifacts. When sessions end with unfinished work, the next session starts from the exact resume point — not from scratch.

---

## What It Does

```
/checkpoint save <name>      Save current task state to a named checkpoint
/checkpoint list              Show all available checkpoints
/checkpoint resume <name>     Restore session from a checkpoint
/checkpoint delete <name>     Delete a completed checkpoint
```

Checkpoints survive session death, context compaction, and crashes. They can stack for multi-day workflows.

---

## Installation

**Option 1: Via ClawHub** (recommended)
```bash
openclaw skills install session-continuity
```

**Option 2: Manual**
```bash
# Copy the skill to your OpenClaw workspace skills directory
cp -r session-continuity ~/.openclaw/workspace/skills/

# Create the checkpoints directory
mkdir -p ~/.openclaw/workspace/memory/checkpoints
```

**Verify installation:**
```bash
openclaw skills check
# session-continuity should appear in the list
```

---

## Quick Start

### Save your work before closing

When you have unfinished work and the session is about to end:

```
/checkpoint save my-task
```

The skill will write a checkpoint containing:
- Task summary
- What was completed (with file paths and line ranges)
- Exact next action (which file, which command)
- Blockers and uncertainties
- Key decisions made during the session

### Resume in a new session

```
/checkpoint list                    # see all checkpoints
/checkpoint resume my-task          # restore from checkpoint
```

The skill presents a structured briefing showing:
- Task summary and age
- What was done
- What to do next
- Any stale warnings (e.g. files that no longer exist)

---

## How It Works

### Checkpoint File

```
memory/checkpoints/<name>.md
```

Each checkpoint contains:
- **Task**: one-line summary
- **Progress**: specific completed items (file paths, line ranges)
- **Next Action**: exact next step
- **Blockers**: concrete obstacles
- **Key Decisions**: reasoning that led to current state
- **Relevant Context**: preferences, file paths, anything needed to continue

### Architecture

```
~/.openclaw/workspace/
├── SESSION-STATE.md              ← WAL: per-message decisions (proactive-agent)
├── memory/
│   ├── working-buffer.md         ← WAL: danger zone exchanges
│   └── checkpoints/
│       ├── <name>.md             ← Named checkpoints (you create)
│       └── autosave.md           ← Auto-created on close signals / high context
```

The skill builds on the WAL Protocol from [proactive-agent](https://github.com/hal-lobster/proactive-agent):
- WAL captures per-message decisions and corrections
- Checkpoints capture task-level resume state

---

## Auto-Checkpoint (Automatic Saves)

The skill automatically saves to `autosave.md` when it detects:

| Signal | Example |
|--------|---------|
| Context >70% | Running low on context tokens |
| Close signals | "goodnight", "exit", "logout" |
| Idle with work | 10+ minutes idle with active tasks |
| Long operation | About to run a command >30s |

Named checkpoints are never overwritten by autosave.

---

## Requirements

- OpenClaw (any recent version)
- Python 3.8+ (for the checkpoint script)
- `OPENCLAW_WORKSPACE` environment variable (set automatically by OpenClaw)

No external Python packages required — uses Python stdlib only.

---

## Running Tests

```bash
cd session-continuity
python3 tests/test_checkpoint.py
```

Expected output:
```
✅ Checkpoint saved: test-task
   Path: /tmp/.../memory/checkpoints/test-task.md
✅ Checkpoint saved: another-task
...
✅ All tests passed
```

---

## Directory Structure

```
session-continuity/
├── SKILL.md                                  ← Skill entry point
├── LICENSE                                   ← MIT
├── README.md                                 ← This file
├── README_zh.md                              ← 中文说明
├── setup.sh                                  ← Quick setup script
├── scripts/
│   ├── checkpoint.py                         ← Checkpoint manager CLI
│   └── requirements.txt                      ← (empty — stdlib only)
├── references/
│   ├── checkpoint-format.md                  ← Full template + examples
│   ├── resume-flow.md                        ← Resume decision tree
│   └── auto-checkpoint-signals.md            ← Auto-save trigger signals
└── tests/
    └── test_checkpoint.py                    ← Unit tests
```

---

## License

MIT — free to use, modify, distribute. No warranty.

---

## Credits

Built with the [MiniMax Skill Factory](https://github.com/MiniMax-AI/skills) workflow.
Inspired by the WAL Protocol from [proactive-agent](https://github.com/hal-lobster/proactive-agent).
