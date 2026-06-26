# skill-spec

> Your AI doesn't forget code. Why should it forget process?

**skill-spec** turns the invisible patterns in your Claude Code sessions into versionable, iterable, composable specs — automatically.

---

## The Insight

Every 20+ tool-call session you run is a process waiting to be captured. But you never stop to write it down because:

- You don't notice the pattern until the 3rd time
- Writing a skill from scratch is friction
- Existing skills rot because there's no change management

**skill-spec** solves all three with zero ongoing effort:

```
Session ends → hook fires → candidate logged → you review when ready → skill born (or existing skill improved)
```

**Zero tokens consumed during normal work.** The entire detection layer is pure shell.

---

## How It Works

```
                         YOUR DAILY WORKFLOW
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          │   PostToolUse      │   Stop hook        │
          │   (async, 0 tok)   │   (threshold?)     │
          │   count + log      │                    │
          │                    │   < 15 → silent    │
          │                    │   >= 15 → log it   │
          └────────────────────┼────────────────────┘
                               │
                               ▼
                    data/candidates.md
                    (accumulates silently)
                               │
                               ▼  when YOU decide
               ┌───────────────────────────────┐
               │      /skill-spec review        │
               │                               │
               │  For each candidate:          │
               │  1. Is it repeatable?         │
               │  2. Similar skill exists?     │
               │     YES → proposal            │
               │     NO  → scaffold new skill  │
               └───────────────────────────────┘
```

---

## Quick Start

```bash
# 1. Install
git clone https://github.com/ChamberZ40/skill-spec.git ~/.claude/skills/skill-spec

# 2. Add hooks to ~/.claude/settings.json (merge, don't replace)
```

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "",
      "hooks": [{"type": "command", "command": "~/.claude/skills/skill-spec/scripts/count-tool-use.sh", "timeout": 5, "async": true}]
    }],
    "Stop": [{
      "matcher": "",
      "hooks": [{"type": "command", "command": "~/.claude/skills/skill-spec/scripts/check-skill-candidate.sh", "timeout": 5}]
    }]
  }
}
```

```bash
# 3. Verify
echo '{"session_id":"test","tool_name":"Bash"}' | ~/.claude/skills/skill-spec/scripts/count-tool-use.sh
# → {"suppressOutput": true}

# 4. Done. Use Claude Code normally. Candidates accumulate silently.
```

---

## The Four Phases

### 1. Detection (automatic, 0 tokens)

Two shell hooks run on every session:
- **PostToolUse** — counts calls + logs which tools you used
- **Stop** — if count >= threshold, writes a candidate entry

You never see this. It just runs.

### 2. Scaffold (on-demand, with dedup)

When you review candidates:
1. Scans existing skills for duplicates
2. **Match found** → creates a proposal on the existing skill's CHANGE.md
3. **No match** → scaffolds a new skill from template

No duplicate skills. Ever.

### 3. Change Management (tiered)

| | Patch | Proposal |
|---|---|---|
| **What** | Typo, wording, edge case | New step, reorder, behavior change |
| **Process** | Edit + commit | CHANGE.md → user review → implement |
| **Test** | Would a user notice? No → patch | Would a user say "wait what?" → proposal |

### 4. Composition

Skills declare their downstream connections:
```
[skill-A] --{output}--> [skill-B] --{output}--> [skill-C]
```

After a skill completes, Claude checks for downstream suggestions.

---

## Token Cost

| Scenario | Cost |
|----------|------|
| Normal session (< 15 calls) | **0** |
| Complex session (>= threshold) | **~30 tokens** at session end |
| Skill loaded into context | **~700 tokens** (only when triggered) |
| Description in skill list | **~40 tokens** (same as any skill) |

The detection layer is invisible. You pay nothing until you actively review.

---

## File Structure

```
skill-spec/
├── SKILL.md              # Methodology spec (what Claude reads)
├── CHANGE.md             # This skill's own change proposals
├── README.md             # You're here
├── scripts/
│   ├── count-tool-use.sh         # PostToolUse hook
│   ├── check-skill-candidate.sh  # Stop hook
│   └── test-hooks.sh             # Schema validation
├── data/
│   ├── candidates.md    # Auto-populated log
│   └── chains.md        # Skill dependency registry
└── templates/
    └── SKILL.template.md  # New skill scaffold
```

---

## Configuration

| Variable | Default | What it does |
|----------|---------|--------------|
| `SKILL_CANDIDATE_THRESHOLD` | `15` | Min tool calls to trigger candidate logging |

Set in `~/.claude/settings.json` under `"env"`.

---

## Prerequisites

- Claude Code CLI
- `jq` (JSON parsing in hooks)
- Bash-compatible shell

---

## Philosophy

> Skills are specs. Specs need engineering.

- **Observe** — detect when a new spec is needed
- **Deduplicate** — enhance existing specs instead of creating clones
- **Govern** — light touch for patches, review gates for behavior changes
- **Compose** — specs that chain into pipelines

The goal is not more skills. It's better skills, continuously improved.

---

## License

MIT
