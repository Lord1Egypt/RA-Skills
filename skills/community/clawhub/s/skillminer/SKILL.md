---
name: skillminer
version: 0.5.3
emoji: ⚒️
description: "Suggest reusable skills from recurring patterns in local memory files. Human review gate, drafts only to skills/_pending/, local-first runner with optional external fallback. Triggers on \"skill forge\", \"propose a skill\", \"what skills should I have\", \"skill candidates\", \"what patterns have I been doing\", \"forge me a skill\"."
metadata:
  openclaw:
    requires:
      env: []
      bins: ["jq", "bash", "date", "git", "openclaw", "flock"]
      config: []
    primaryEnv: null
    capabilities:
      network: false
      subprocess: ["bash", "jq", "git", "openclaw", "claude"]
      writesTo: ["state/", "skills/_pending/", "skills/_rejected/"]
      readsFrom: ["memory/"]
    note: "The skill auto-detects its install location. CLAWD_DIR is an optional path config (not a credential) — defaults to ~/clawd if unset; used only for workspace memory files plus skills/_pending/ output. The default runner is openclaw (local only, no data leaves the host). FORGE_RUNNER=claude is an optional external fallback that uses Claude CLI and sends prompt data to Anthropic's API; leaving it unset keeps all data local. Never activates skills automatically."
triggers:
  - "skill forge"
  - "skill candidates"
  - "what patterns have I been doing"
  - "forge me a skill"
  - "forge show"
  - "forge accept"
  - "forge reject"
  - "forge defer"
  - "forge silence"
  - "forge unsilence"
  - "forge promote"
  - "forge review"
  - "skill candidates zeigen"
  - "was hat skillminer gefunden"
  - "annehmen als skill"
  - "ablehnen skill"
  - "letzen skillminer scan"
  - "letzten skillminer scan"
---

# skillminer ⚒️

> Your AI assistant keeps solving the same problems. skillminer notices and suggests turning them into reusable skills.

skillminer watches your local memory files, spots recurring work, and surfaces the patterns worth keeping. No auto-activation, no cloud sync, no noise by default. A morning suggestion in your inbox when something actually deserves to become a skill.

## Trust model

- Human gate first, always. Nothing ships without your explicit accept.
- Drafts go to `skills/_pending/<slug>/`, never to live skills.
- Default runner is local OpenClaw. No data leaves the host.
- `FORGE_RUNNER=claude` is an opt-in external fallback that sends prompt data to Anthropic's API.
- Notifications are off by default; review files are written locally regardless.

## Flow

```
nightly scan   reads recent memory/YYYY-MM-DD.md files
               detects recurring task patterns
               writes a review file to state/review/
               ↓
YOU DECIDE     forge accept / reject / defer / silence
               ↓
morning write  drafts a SKILL.md into skills/_pending/<slug>/
               you review it, promote it, ship it
```

Nothing goes live automatically. You stay in control at every step.

## Quick start

```bash
openclaw skills install skillminer
cd "${CLAWD_DIR:-$HOME/clawd}/skills/skillminer"
bash setup.sh
CLAWD_DIR="${CLAWD_DIR:-$HOME/clawd}" bash scripts/run-nightly-scan.sh
```

If the manual scan looks good, add the printed scheduler jobs using the dispatcher prompts.

## Environment

- `CLAWD_DIR` — optional, defaults to `~/clawd`
- `FORGE_RUNNER` — defaults to `openclaw` (local). Set to `claude` only if you accept that prompt data leaves the host.

## Commands

`forge` is the command prefix.

- `forge show` — list current candidates
- `forge review` — open the latest review file
- `forge accept <slug>` — accept a candidate for the next morning write
- `forge reject <slug> "reason"` — reject permanently
- `forge defer <slug> "reason"` — defer with cooldown
- `forge silence <slug> "reason"` — silence without cooldown
- `forge unsilence <slug>` — resurface a silenced entry
- `forge promote <slug>` — move a pending draft into live skills

## Manual triggers

When you want a one-shot run without remembering full paths:

```bash
skillminer scan     # run nightly scan now
skillminer write    # run morning write now
skillminer full     # scan + write in sequence
skillminer status   # show current ledger state
skillminer help     # show usage
```

## Security

- Slug validation gates every filesystem-path boundary (regex-enforced)
- Atomic state writes with backup rotation and JSON validation
- `flock`-based single-instance guarantee across all entry points
- Memory files are treated as untrusted data in the nightly scan prompt

See [README.md](README.md) and [USER_GUIDE.md](USER_GUIDE.md) for full docs.
