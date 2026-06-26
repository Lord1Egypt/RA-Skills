# skillminer ⚒️

> Your AI assistant keeps solving the same problems. skillminer notices — and suggests turning them into reusable skills.

**Version:** 0.5.3 | **Runner:** OpenClaw-native | **Schema:** 0.5

You build patterns. Every day, in every conversation. skillminer watches your local memory files, spots recurring work, and surfaces the ones worth keeping. No auto-activation, no cloud sync, no noise by default. Just a morning suggestion waiting in your inbox when something actually deserves to become a skill.

---

## How it works

```
04:00 — nightly scan   reads recent memory/YYYY-MM-DD.md files
                       detects recurring task patterns
                       writes a review file to state/review/
                       cron can announce the result
                       ↓
        YOU DECIDE     forge accept / reject / defer / silence
                       ↓
10:00 — morning write  drafts a SKILL.md into skills/_pending/<slug>/
                       cron can announce the result
                       you review it, promote it, ship it
```

Nothing goes live automatically. You stay in control at every step.

By default, skillminer runs with `FORGE_RUNNER=openclaw`, which stays local to the host and does not send your data off-host.

If you explicitly set `FORGE_RUNNER=claude`, skillminer uses Claude CLI as a fallback runner. That sends prompt data to Anthropic's API. Only enable it if you understand and accept that data leaves the host.

---

## Requirements

- OpenClaw (recent version)
- `bash`, `jq`, `git` on PATH
- Claude CLI (`claude`) — only if you explicitly switch to `FORGE_RUNNER=claude`

---

## Quickstart

> `CLAWD_DIR` is optional. If unset, skillminer uses your OpenClaw workspace default at `~/clawd`.

**1. Install**

Via ClawHub:
```bash
openclaw skills install skillminer
```

Or manual:
```bash
git clone https://github.com/robbyczgw-cla/skillminer.git \
  "${CLAWD_DIR:-$HOME/clawd}/skills/skillminer"
```

**2. Bootstrap**

```bash
cd "${CLAWD_DIR:-$HOME/clawd}/skills/skillminer"
bash setup.sh
```

This creates your state file, copies the default config, and prints the exact scheduler commands for your install path, including the wrapper-dispatch cron prompts.

**3. Test it first**

```bash
CLAWD_DIR="${CLAWD_DIR:-$HOME/clawd}" bash scripts/run-nightly-scan.sh
```

Then look at what it found:
```bash
ls state/review/
cat state/logs/scan-*.log | tail -n 40
```

**4. Schedule it**

Only after the manual run looks good — `setup.sh` prints the exact commands. Nightly scan at 04:00, morning write at 10:00, your local timezone.

---

## Commands

`forge` is the command prefix. `skillminer` is the product.

```
forge show                       — what's in the ledger?
forge review                     — open pending candidates
forge accept <slug>              — queue for morning draft
forge reject <slug> "reason"     — dismiss it
forge defer <slug> "reason"      — maybe later
forge silence <slug> "reason"    — stop surfacing this one
forge unsilence <slug>           — undo silence
forge promote <slug>             — move _pending draft to live skills/
```

### Rejecting a bad candidate

When a draft skill in `_pending/` turns out to be noise or misinterpreted intent:
```
scripts/manage-ledger.sh reject <slug> "<reason>"
```
This moves the draft to `_rejected/<slug>-<timestamp>/`, marks the ledger entry
`status=rejected`, and stops the nightly scan from flagging it as open work.

---

## Configuration

Edit `config/skill-miner.config.local.json` (git-ignored, your personal values):

| Key | Default | Description |
|---|---|---|
| `notifications.enabled` | `false` | Legacy setting. Scheduled notifications should use cron `delivery.mode: "announce"` instead |
| `notifications.channel` | `null` | Legacy setting. Keep unset when using cron announce delivery |
| `notifications.threadId` | `null` | Legacy setting. Keep unset when using cron announce delivery |
| `runner.default` | `"openclaw"` | `"openclaw"` or `"claude"` |
| `runner.openclaw_agent` | `"main"` | OpenClaw agent used for the local runner |
| `scan.windowDays` | `10` | Days of memory to scan each night |
| `scan.minOccurrences` | `3` | Minimum occurrences before a pattern is a candidate |
| `scan.minDistinctDays` | `2` | Pattern must span at least this many distinct days |
| `scan.cooldownDays` | `30` | Days before rejected/deferred patterns can resurface |
| `thresholds.low` | `3` | Low-confidence band minimum |
| `thresholds.medium` | `4` | Medium-confidence band minimum |
| `thresholds.high` | `6` | High-confidence band minimum |

---

## Output

By default, skillminer is silent. It still writes everything locally:

- Scan review: `state/review/YYYY-MM-DD.md`
- Scan logs: `state/logs/scan-*.log`
- Write logs: `state/write-log/YYYY-MM-DD.md`

For scheduled runs, use cron `delivery.mode: "announce"` for chat delivery and inline `prompts/cron-dispatch-nightly.md` or `prompts/cron-dispatch-morning.md` as the payload message. The dispatcher invokes the hardened wrapper via the bash tool, then returns a human summary. Do not send notifications from inside the analysis prompts.

---

## Troubleshooting

**No notification after the scan?**
Check the cron job delivery config first. The supported scheduled pattern is cron `delivery.mode: "announce"` pointing at your channel/topic, with the dispatcher prompt inlined as the payload message.

**Nothing drafted at 10:00?**
You need to accept at least one candidate before the morning write runs:
```bash
cat state/state.json | jq '.candidates'
```

**State file corrupted?**
```bash
cp state-template.json state/state.json
```

**Wrapper exits non-zero?**
- Exit `2`: atomic validation or tmp-write promotion failed
- Exit `3`: another skillminer run already holds the lock
- Exit `4`: slug validation failed before filesystem writes

**Want to try the Claude runner?**

Default runner: `openclaw` (local only, no data leaves the host).

Optional fallback: `FORGE_RUNNER=claude`, which uses Claude CLI and sends prompt data to Anthropic's API. Only enable it if you understand that data leaves the host.

```bash
FORGE_RUNNER=claude CLAWD_DIR="${CLAWD_DIR:-$HOME/clawd}" bash scripts/run-nightly-scan.sh
```

---

## Security &amp; Privacy

skillminer reads local memory files under `$CLAWD_DIR/memory/` to detect
recurring work patterns. This is its core function.

ClawHub labels this capability as "sensitive credentials" — that label is
accurate and intended. Your memory files may contain anything you've written
to your agent; skillminer indexes them locally to surface reusable patterns.

**Off-host data flow:** the optional `FORGE_RUNNER=claude` path sends prompt
data to Anthropic's API. Off by default. Only enable if you understand that
data leaves the host.

**Secret scrubbing:** state writes pass through regex-based redaction for PEM
blocks and OpenAI / GitHub (PAT + OAuth) / AWS / JWT / Slack token shapes
before disk persistence. Patterns live in `scripts/lib/secret-patterns.tsv`
and are applied by `scripts/lib/secret-scrub.sh`. This is defense-in-depth,
not a promise — don't rely on it as your only safeguard.

**No OAuth flow, no network auth tokens, no credential storage of any kind
in skillminer itself.**

### Hardening

- Slugs are regex-validated before any filesystem path is derived from them (0.4.2)
- `flock` prevents overlapping scan and write runs from mutating shared state at the same time (0.3.2)
- State updates use atomic tmp-write promotion with backup rotation and rollback validation (0.3.2)
- Nightly scan treats memory files as untrusted data, not instructions to execute (0.3.2)
- Secret scrubbing applied to state + SKILL.md output via conservative regex patterns before atomic promotion (0.5.0); patterns externalized to `secret-patterns.tsv` (0.5.3)

---

## Full guide

See [USER_GUIDE.md](USER_GUIDE.md) for the complete walkthrough.

---

## License

MIT
