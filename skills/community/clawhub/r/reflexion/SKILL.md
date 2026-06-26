---
name: reflexion
description: "Closed-loop learning for AI coding agents. Auto-captures errors and corrections, recalls relevant past solutions when similar situations arise, and promotes recurring patterns to project memory. Use when: errors occur, user corrects the agent, a non-obvious solution is found, or before starting tasks in areas with past learnings."
metadata:
  version: "1.0.0"
  license: MIT
  agents: claude-code, codex, copilot, openclaw
---

# Reflexion

Closed-loop learning for AI coding agents. Inspired by [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366).

> *"Reflexion agents verbally reflect on task feedback signals, then maintain their own reflective text in an episodic memory buffer to induce better decision-making in subsequent trials."*
> — Shinn et al., 2023

**The problem**: AI agents repeat the same mistakes across sessions. They don't learn from errors, don't remember corrections, and every new conversation starts from zero.

**The solution**: A capture-recall-promote loop that closes the feedback gap.

```
Error/Correction occurs
        |
   [CAPTURE] -----> .reflexion/entries/
        |                    |
   Next similar task    [INDEX] keywords
        |                    |
   [RECALL] <--- keyword match on prompt
        |
   Inject past solution into context
        |
   [VERIFY] did it work?
        |           |
      Yes          No ---> update entry, flag for review
        |
   occurrences >= 3?
        |           |
      Yes          No ---> increment counter
        |
   [PROMOTE] append rule to CLAUDE.md
```

## Quick Reference

| Situation | What Happens |
|-----------|-------------|
| Command fails | `capture.sh` auto-logs error + context to `.reflexion/entries/` |
| User corrects agent | Agent calls `capture.sh` with correction details |
| Similar prompt later | `recall.sh` finds matching entries, injects solutions into context |
| Pattern seen 3+ times | `promote.sh` auto-appends a concise rule to `CLAUDE.md` |
| Want to see stats | Run `./scripts/status.sh` for learning dashboard |

## Install

### Claude Code (recommended)

```bash
# Clone into your project or global skills
git clone https://github.com/user/reflexion.git .claude/skills/reflexion

# Or copy into an existing skills directory
cp -r reflexion/ ~/.claude/skills/reflexion
```

Add hooks to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/skills/reflexion/scripts/capture.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/skills/reflexion/scripts/recall.sh"
          }
        ]
      }
    ]
  }
}
```

### First run

The scripts auto-initialize on first use. No setup needed. To manually initialize:

```bash
./scripts/init.sh
```

## How It Works

### 1. Capture (automatic)

The `capture.sh` hook fires after every Bash tool use. It reads the tool output from stdin (JSON), detects errors via pattern matching, and stores structured entries:

```json
{
  "id": "RFX-20260331-a7f",
  "type": "error",
  "trigger": "npm ERR! Missing script: \"build\"",
  "context": "npm run build",
  "resolution": "",
  "keywords": ["npm", "build", "missing", "script"],
  "occurrences": 1,
  "first_seen": "2026-03-31",
  "last_seen": "2026-03-31",
  "promoted": false,
  "cwd": "/home/user/project"
}
```

When the agent (or user) resolves the error, the agent should update the entry:

```
Update .reflexion/entries/RFX-20260331-a7f.json with resolution:
"Use pnpm run build - this project uses pnpm, not npm"
```

### 2. Recall (automatic)

The `recall.sh` hook fires before every user prompt. It extracts keywords from the prompt, searches the entry index, and injects relevant past learnings:

```xml
<reflexion-recall>
Past learning [RFX-20260331-a7f] (seen 2x):
  Trigger: npm ERR! Missing script: "build"
  Resolution: Use pnpm run build - this project uses pnpm, not npm
  Keywords: npm, build, missing, script
</reflexion-recall>
```

This costs ~50-80 tokens when matches exist, zero when they don't.

### 3. Promote (automatic)

When an entry hits 3+ occurrences, `promote.sh` appends a concise rule to `CLAUDE.md`:

```markdown
<!-- reflexion:auto-promoted -->
## Reflexion: Learned Rules

- This project uses pnpm, not npm. Always use `pnpm run` commands. (seen 3x, source: RFX-20260331-a7f)
```

Promoted entries are marked `"promoted": true` and stop being injected via recall (the rule is now in CLAUDE.md permanently).

### 4. Verify (agent-driven)

After the agent applies a recalled solution, it should verify and update:

- **Worked**: Increment `occurrences`, update `last_seen`
- **Failed**: Add note to entry, flag for review, decrement confidence

This step is agent-driven (via prompt instruction), not hook-automated, to avoid false positives.

## Entry Types

| Type | Trigger | Example |
|------|---------|---------|
| `error` | Command failure detected by hook | `npm ERR!`, `Permission denied`, `ModuleNotFoundError` |
| `correction` | User says "no", "actually", "wrong" | "Actually use pnpm, not npm" |
| `insight` | Non-obvious solution discovered | "Must run codegen after API changes" |
| `pattern` | Recurring approach that works | "Always check auth status before git push" |

## Data Format

Entries live in `.reflexion/entries/` as individual JSON files (one per learning). This enables:
- Fast grep-based search (no parsing a giant markdown file)
- Atomic writes (no corruption from concurrent access)
- Easy manual editing
- Git-friendly diffs

The keyword index at `.reflexion/index.txt` maps keywords to entry IDs for fast recall:

```
npm:RFX-20260331-a7f,RFX-20260401-b2c
build:RFX-20260331-a7f
pnpm:RFX-20260331-a7f,RFX-20260401-b2c
docker:RFX-20260402-c1d
```

## Promotion Rules

An entry is auto-promoted to CLAUDE.md when ALL conditions are met:

1. `occurrences >= 3`
2. `resolution` is non-empty (the fix is known)
3. `promoted` is `false` (not already promoted)
4. Entry is older than 1 day (not a flurry of the same error in one session)

Promoted rules are written as short, actionable directives. Not incident reports.

## Agent Instructions

When this skill is active, follow these behaviors:

### On Error
1. Check if `capture.sh` already logged it (it runs automatically on Bash errors)
2. If you resolve the error, update the entry's `resolution` field
3. If the error matches a recalled learning, say so and apply the known fix

### On User Correction
Log a `correction` entry manually:
```bash
cat > .reflexion/entries/RFX-$(date +%Y%m%d)-$(head -c3 /dev/urandom | xxd -p | head -c3).json << 'ENTRY'
{
  "id": "RFX-...",
  "type": "correction",
  "trigger": "user said: actually use pnpm",
  "context": "attempted npm install",
  "resolution": "this project uses pnpm, not npm",
  "keywords": ["npm", "pnpm", "install", "package-manager"],
  "occurrences": 1,
  "first_seen": "2026-03-31",
  "last_seen": "2026-03-31",
  "promoted": false
}
ENTRY
```
Then rebuild the index: `./scripts/rebuild-index.sh`

### On Recall
When `<reflexion-recall>` context appears in the prompt:
1. Read the recalled learnings
2. Apply the known resolution if relevant
3. If the resolution works, increment occurrences
4. If it doesn't apply, ignore it (no penalty)

### Before Major Tasks
Run `./scripts/status.sh` to see if there are relevant learnings for the area you're about to work in.

## Security

- Never log secrets, tokens, API keys, or credentials in entries
- The `capture.sh` script redacts common secret patterns (Bearer tokens, API keys, passwords)
- `.reflexion/` should be in `.gitignore` for private projects
- For team projects, committing `.reflexion/` creates shared learning (opt-in)

## Comparison

| Feature | self-improving-agent | OMC auto-learner | **reflexion** |
|---------|---------------------|------------------|---------------|
| Auto-capture errors | Hook reminder only | Pattern detection | **Hook + auto-parse + store** |
| Structured storage | Markdown append | Content hash dedup | **JSON entries + keyword index** |
| Cross-session recall | None | None | **Auto keyword match + inject** |
| Auto-promote to CLAUDE.md | Manual | Manual | **Auto at 3 occurrences** |
| Token overhead | ~70 tokens always | Variable | **0 tokens when no match, ~60 on match** |
| Correction capture | Reminder to log | Confidence scoring | **Structured entry with resolution** |
| Works offline | Yes | Yes | **Yes** |
| Dependencies | bash | TypeScript + npm | **bash + grep (zero deps)** |

## File Structure

```
reflexion/
├── SKILL.md                 # This file
├── scripts/
│   ├── init.sh              # Initialize .reflexion/ directory
│   ├── capture.sh           # PostToolUse hook - auto-capture errors
│   ├── recall.sh            # UserPromptSubmit hook - inject past learnings
│   ├── promote.sh           # Auto-promote recurring patterns to CLAUDE.md
│   ├── status.sh            # Learning stats dashboard
│   └── rebuild-index.sh     # Rebuild keyword index from entries
├── assets/
│   └── settings-template.json  # Claude Code settings template
└── references/
    └── integration.md       # Setup guides for different agents
```

## Citation

This skill implements the core feedback loop from:

```bibtex
@article{shinn2023reflexion,
  title   = {Reflexion: Language Agents with Verbal Reinforcement Learning},
  author  = {Noah Shinn and Federico Cassano and Edward Berman and
             Ashwin Gopinath and Karthik Narasimhan and Shunyu Yao},
  journal = {arXiv preprint arXiv:2303.11366},
  year    = {2023},
  url     = {https://arxiv.org/abs/2303.11366},
  doi     = {10.48550/arXiv.2303.11366}
}
```

The paper showed that language agents reflecting on past failures in an episodic memory buffer significantly outperform base agents — achieving 91% pass@1 on HumanEval vs GPT-4's 80%. This skill adapts that principle for AI coding agents: instead of weight updates, it stores verbal reflections (error entries with resolutions) and retrieves them when similar situations arise.
