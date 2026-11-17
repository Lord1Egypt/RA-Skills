---
name: skillminer
version: 0.6.0
emoji: "\u2692\ufe0f"
description: "Suggest reusable skills from recurring patterns in local memory files. Human review gate, drafts only to skills/_pending/, local-first runner with optional external fallback. Triggers on \"skill forge\", \"propose a skill\", \"what skills should I have\", \"skill candidates\", \"what patterns have I been doing\", \"forge me a skill\", \"forge show\", \"forge accept\", \"forge reject\", \"forge promote\"."
metadata:
  openclaw:
    requires:
      bins: ["jq", "bash", "date", "git", "openclaw"]
    note: "jq is required by the scan scripts; install it if the skill reports missing binaries. CLAWD_DIR is an optional path (not a credential) and defaults to the OpenClaw workspace. The default runner is openclaw and keeps all data on the host; FORGE_RUNNER=claude is an optional external fallback that sends prompt data to Anthropic. The skill never activates a generated skill on its own."
    envVars:
      - name: CLAWD_DIR
        required: false
        description: "Workspace path to scan. Defaults to the OpenClaw workspace."
      - name: FORGE_RUNNER
        required: false
        description: "Optional external runner. Unset keeps everything local."
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

## Relationship to the built-in Skill Workshop

OpenClaw 2.0 ships automatic self-learning and a system-owned skill review job:

```
skill-collection-review   every 7d   main
```

It proposes skills too. skillminer differs in three ways: it reads your memory files
rather than session behaviour, it writes drafts to `skills/_pending/` instead of creating
anything live, and every candidate passes an explicit accept/reject ledger. Running both
is fine - they draw on different signals - but expect overlapping suggestions. Check what
is scheduled with `openclaw automations list`.

## Quick start

```bash
openclaw skills install skillminer
cd ~/.openclaw/workspace/skills/skillminer     # or "$CLAWD_DIR/skills/skillminer"
bash setup.sh
bash scripts/run-nightly-scan.sh
```

If the manual scan looks good, add the printed scheduler jobs with
`openclaw automations add`.

`jq` must be on PATH. Without it OpenClaw marks the skill as needing setup, which also
means the model cannot see it and the slash command does not exist - the skill is simply
absent with no message in the chat. `openclaw skills info skillminer` shows which binary
is missing.

## Environment

- `CLAWD_DIR` - optional. Defaults to the OpenClaw workspace, which is
  `~/.openclaw/workspace` on OpenClaw 2.0. Older installs used `~/clawd`; set this
  explicitly if your memory files live somewhere else.
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
