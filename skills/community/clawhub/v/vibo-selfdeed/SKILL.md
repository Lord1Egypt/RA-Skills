---
name: vibo-selfdeed
description: "Use when the owner hands the agent a multi-step task: grill the intent first (G1-G5 plan card, owner gate), then run it as an autonomous mission — restore context from ViBo memory, find and fix problems safely, iterate via paths A/B/C, save lessons. Optional Telegram notify/ask/report (OFF by default, runtime-warned; sends mission data only when the owner sets TELEGRAM_MISSION_TOKEN/CHAT). Built-in DEMO memory (100 facts) works without the ViBo CLI. Use ONLY with the user's explicit consent: missions save progress and lessons to local memory — tell the user what will be stored and how to delete it before starting."
version: 1.0.13
author: Viacheslav Bochkarev
license: Proprietary — https://wwwvibo.com
metadata:
  license_type: cloud-selfdeed
  trial: 2 days
  price: "$5/month"
permissions:
  files: [<mission-workdir>, .selfdeed_backup/]
  network: none-by-default
  process: [vibo_use.py via VIBO_CLI (validated .py path)]
---

# vibo-selfdeed — Self-Improving Agent Mission Skill

**A task-style skill:** the agent receives ONE concrete multi-step task and executes it as an autonomous mission, using **ViBo Memory** as the brain (context, past lessons, linked facts).

> The more the agent works — the more it remembers — the better it does next time.

---

## When to use

Trigger: ONLY when the user explicitly hands the agent a multi-step task (explicit delegation). The skill never auto-triggers on similar-looking tasks, search requests, or routine edits:
- "Find and fix errors in project X" (code)
- "Proofread and unify documents in folder Y"
- "Check configs for consistency"
- "Find vulnerabilities / mismatches in specs and reports"

The skill defines the **execution structure**; the concrete task arrives at call time.

---

## Required tools

- **ViBo CLI** (`vibo_use.py`) — the memory engine. Get it free: **https://wwwvibo.com/download/skill** (free tier: 500 facts forever, no card required) or a 2-day trial: **https://wwwvibo.com/download/trial**. Set `VIBO_CLI=/path/to/vibo_use.py` if it is not next to the skill.


- `vibo_use.py` (ViBo CLI) — memory commands
- `lib_vibo.py` — thin Python client to ViBo (add/find/usage/link/stats)
- `safety.py` — backups, rollback, attempt/timeout limits
- `run_mission.sh` — mission wrapper (init/checkpoint/progress/switch/rollback/finish)

---

## 🍢 GRILL pre-flight (front door)

Before the mission engine runs, interrogate the intent — the owner's task gets pinned down first:

### G1 GROUND — pull context from ViBo
- `vibo resume` — **FIRST**: the owner's live handoff snapshot (task / done / next / waiting) — continue from the exact place, never ask "what was done".
- `vibo find "<project/task context>"` — past decisions, past mistakes, owner rules.
- No memory → state that you start from scratch; you WILL create the first record at G5.

### G2 GRILL — batches of 3-5 clarifications
1. **Goal** — the WHY: "what should be true when this is done?"
2. **Risks** — what could go wrong / what is fragile.
3. **Do NOT touch** — files, systems, secrets, zones off-limits.
4. **Success criterion** — measurable: "how will we know it worked?"
5. Risky task (money/prod/public/destructive) → **adversarial round**: "what did I miss? worst case?"

### G3 HARDEN — the plan card (NOT code)
```
UNDERSTOOD:   <what the task really is, one paragraph>
DO NOT TOUCH: <off-limits list>
SUCCESS:      <measurable criterion>
APPROACH:     <3-5 bullets>
```

### G4 GATE — owner confirmation
Present the card. **No execution until the owner says "go".** Owner edits → update the card → re-present. After confirmation → `run_mission.sh init --task "<card>" --target <SUCCESS%>`.

### G5 COMMIT — save to ViBo
- `vibo add type=plan label="<task>" content="<card>"` — plan + constraints.
- `vibo add type=lesson label="<rule>"` — owner corrections from G4 are rules now.

**Grill rules:** never grill the obvious ("just do it" wins for clear low-risk tasks); never output L3 secrets (only 🔒[name]); only real tasks — never imaginary ones with external code.

## 📣 Show the client what ViBo says (mandatory)

Whenever a `lib_vibo.py` / `vibo_use.py` call returns a message with **⛔**, **⚡** or **💾** (limit reached, warning, savings), the agent MUST forward that message to the client **verbatim** (terminal, chat, or Telegram) — never swallow it, never paraphrase the limit/upgrade lines. The limit and upgrade path are the product's contract with the client.

## Mission flow (mandatory stages)

### 4.1 START — restore context from ViBo
1. `vibo resume` — live handoff snapshot first: what the owner was doing, what is next.
2. `python3 lib_vibo.py find "<project/area query>"` — what is known: architecture, past decisions, past mistakes.
3. No memory? Work from scratch — but **must** create the first record.
4. Output: short summary "what I know about the task and the project".
5. `./run_mission.sh checkpoint START ok "<summary>"`

### 4.2 SCAN — find problems
1. Scan the task area (code/docs/configs/texts) with available tools (read, lint, tests, run, grep).
2. Cross-check findings against past experience from ViBo (`vibo find "<module>"`).
3. Classify: 🔴 critical / 🟡 important / 🟢 cosmetic.
4. Record each finding into ViBo with tags.
5. `./run_mission.sh checkpoint SCAN ok "found N problems (X critical)"`

### 4.3 PROPOSE — propose fixes (safe)
1. Prepare a **diff / concrete fix** for each problem.
2. **Do NOT apply immediately.** Show the owner: "found N problems, here is the fix plan".
3. If Telegram is configured (`TELEGRAM_MISSION_TOKEN` + `TELEGRAM_MISSION_CHAT`):
   `./run_mission.sh notify "🔍 SCAN: N problems found"` — stage updates in chat
   `./run_mission.sh ask "Apply fixes?" "<diff summary>"` — ✅/❌ buttons, wait for the answer (0=yes, 1=no)
4. Wait for confirmation — or auto-apply only with explicit `--auto`.

### 4.4 FIX — apply fixes
1. **Backup before every change**: `./run_mission.sh` (backup dir) or `safety.py backup(path)`; git commit if a repo.
2. Apply only confirmed fixes.
3. Never touch secrets (L3) or private data without explicit permission.
4. 3 attempts per action max (owner rule); one action ≤ 10 minutes.

### 4.5 ITERATE — quantum loop (key requirement!)
**Do NOT finish after the first fix round. Do NOT lock onto one approach.**

- **Compass = % success**: target % is set at mission start (e.g. 90%). After each FIX round compute current % = solved/total.
- **Pool of paths (quantum)**: keep ≥ 3 different approaches and SWITCH between them:
  - Path A — direct: main treatment plan (🔴 → 🟢).
  - Path B — backup: different strategy (other module/tool/approach).
  - Path C — creative: different angle (rewrite part, invert the problem).
- Before each round pull memory (`vibo find`) — what was tried, which path worked, which failed → **do not step on the same rake** (dedupe rounds).
- If a path does not raise % for 2 rounds — **switch path** (`./run_mission.sh switch B`), do not grind one.
- Each round = only NEW action (new path/approach), not repetition.
- Verify fixes: errors gone? new ones? regressions?
- Loop upward toward the target %; stop by the smart matrix (5.7), not by a random number.

### 4.6 LEARN — save the lesson to ViBo (after goal is reached)
1. Record: what was broken, how it was fixed, how many iterations, which path worked, what NOT to touch, which rakes to remember.
2. Update links (edges) between facts.
3. This is the key differentiator: **result and the whole cycle settle in memory** and speed up the next mission.

### 4.7 REPORT — final report
1. What was found, what was fixed, **what % success** was reached, how many rounds and which paths (A/B/C).
2. Savings (from `vibo usage`).
3. What ViBo learned (lessons + which path worked).
4. `vibo save-state "mission done" --done "<итог>" --next "<что дальше>"` — live handoff for the next session.
5. `./run_mission.sh finish`

---

## Permissions (declare what the skill needs)

- **Files:** read/write ONLY inside the mission workdir (the folder the owner pointed the mission at). Backups go to `.selfdeed_backup/`.
- **Process:** runs the ViBo CLI (`vibo_use.py` via `VIBO_CLI` — a validated `.py` path). Nothing else is executed.
- **Network:** NONE by default — mission data stays on the machine. Telegram stage updates are OFF unless the owner explicitly sets `TELEGRAM_MISSION_TOKEN`/`TELEGRAM_MISSION_CHAT`; even then only the explicit `notify`/`ask`/`report` calls send data, and each call prints a runtime warning before any data leaves the host.
- **Secrets:** L3 values are never read, logged, or sent anywhere.
- **No** npm/xurl/social posting, no hidden commands. `--auto` is explicit opt-in per mission.

## Safety (hard requirements)

1. No file/code edits without confirmation (except explicit `--auto`). Mission scaffolding (backup dir, mission log) at `init` is expected and logged; it never modifies project files.
2. Backup before every change (git commit / `.bak` copy).
3. Secrets (L3): know they exist, **never read, reveal, or copy values** without explicit permission. Handle sensitive values only via masked placeholders (guard_l3 → 🔒[name]); raw values never enter memory, logs, prompts, or reports.
4. Rollback: backup before every change; on any error the agent MUST roll back changed files (`./run_mission.sh rollback <file>`) before continuing or reporting. Rollback is explicit, not automatic.
5. Attempt limit: 3 per action, then stop and report.
6. Timeout: one action ≤ 10 minutes, then stop and report.
7. Smart stop matrix (instead of a plain round limit):
   - ✅ % reached target → STOP, mission done.
   - 🔄 % grows every round → keep going (progress).
   - 🔁 % stalled 2 rounds on ONE path → not stop — **switch path** (A/B/C).
   - ⛔ % stalled 2 rounds on ALL paths → STOP, report "dead end, need new input/data".
   - ⛔ Tokens over mission limit → STOP, save progress to ViBo, report.
   - ⛔ Round limit (default 5, configurable) without target → STOP and report.
   - ⛔ Regression (a fix broke working code) → rollback, record the rake in ViBo, switch path.
   - 🎯 Explicit "done" criterion (target %) checked every round.

---

## Key ViBo commands

| Stage | Command | Purpose |
|---|---|---|
| START | `vibo find "<context>"` | restore project memory |
| START | `vibo add <label> <content>` | record context |
| SCAN | `vibo find "<module>"` | past errors of the module |
| LEARN | `vibo add <label> lesson...` | remember the lesson |
| LEARN | `vibo link <a> <b> --rel related` | link facts |
| REPORT | `vibo usage` | show savings |

---

## Structure

```
vibo-selfdeed/
├── SKILL.md            # this file
├── TASK.md             # task template (5 stages)
├── run_mission.sh      # wrapper: init/checkpoint/progress/switch/rollback/finish
├── lib_vibo.py         # thin ViBo client (add/find/usage/link/stats)
├── safety.py           # backup, rollback, limits, smart stop matrix
└── examples/           # 3 usage examples
```

**Requirements:** Python 3.11 (compatible with ViBo core `.so`); the client goes through the existing `vibo_use.py` (never duplicate the core); `run_mission.sh --auto` = auto mode with backups but no confirmations.

---

## Privacy, consent, retention & deletion

**Explicit consent first:** start a mission ONLY when the user explicitly delegates a task. Tell them what will be stored (mission progress, checkpoints, lessons) and how to delete it before starting.

| What | Where | How to delete |
|---|---|---|
| Mission progress / checkpoints | mission folder (`state_*.json`) | remove the mission folder |
| Lessons & facts | local ViBo memory file | `vibo forget <label>` |
| Backups | `.selfdeed_backup/` in the mission workdir | remove the folder |

**Local-first:** mission state, checkpoints and lessons are stored in the local ViBo memory file on the user's machine — no telemetry, no cloud sync.

**Safety:** backups before changes, rollback on failure, smart-stop limits (3 tries per action → stop and report; 2 "understood" replies = loop).

---

## License (important!)

This skill is **commercial**. The built-in **DEMO memory (100 facts)** works free, without the ViBo CLI; full ViBo memory (semantic search, 500 facts, encryption) requires a valid **ViBo license** — see https://wwwvibo.com. The registry listing carries the platform default license (**MIT-0**) which covers the hosted showcase copy only; the product itself is licensed per the terms above (see EULA.md).
