# skillminer — User Guide

> Optional local memory scan that suggests reusable skills.

## What it is

skillminer scans recent local memory files, spots recurring work patterns, and suggests skills you may want to keep. It is local by default, does not auto-activate anything, and does not notify you unless you enable notifications. If you switch to the Claude fallback runner, that runner is external.

The nightly scan now also reports:
- A portfolio snapshot of your live skills
- Aging info for pending candidates
- Trend arrows for sub-threshold observations

## Daily cycle

```
04:00  Scan runs
       → reads recent memory files
       → finds recurring patterns
       → writes a local review file
       → optionally notifies you if enabled

       YOU decide:
       → accept, reject, defer, or silence each candidate

10:00  Write runs
       → for each accepted candidate:
         drafts a SKILL.md into skills/_pending/<slug>/
       → you promote it manually to live skills/
```

## Commands

skillminer is the product. `forge` is the command prefix.

**See what it found**
```bash
forge show
```

**Read the latest review file**
```bash
forge review
```

**Accept a candidate**
```bash
forge accept verify-bindings-post-patch
```

**Reject with cooldown**
```bash
forge reject verify-bindings-post-patch "not worth a skill"
```

**Defer for later**
```bash
forge defer verify-bindings-post-patch "maybe later"
```

**Permanently silence**
```bash
forge silence verify-bindings-post-patch "too specific to my setup"
```

**Lift a silence**
```bash
forge unsilence verify-bindings-post-patch
```

**Promote a sub-threshold observation into candidates**
```bash
forge promote verify-bindings-post-patch
```

Slug matching is fuzzy, so `verify bindings`, `verify-bindings`, and similar variants usually resolve.

Natural language examples:
```text
what skills should I have?
what patterns have I been doing?
was hat skillminer gefunden?
zeig mir skill kandidaten
ja, verify-bindings als skill
verify-bindings ablehnen
verify-bindings nochmal beobachten
verify-bindings nie wieder vorschlagen
letzten skillminer scan zeigen
```

## Installation and setup

**1. Install the skill**
```bash
git clone https://github.com/robbyczgw-cla/skillminer.git \
  "${CLAWD_DIR:-$HOME/clawd}/skills/skillminer"
```

Or:
```bash
openclaw skills install skillminer
```

**2. Bootstrap everything**
```bash
cd "${CLAWD_DIR:-$HOME/clawd}/skills/skillminer"
bash setup.sh
```

This creates the local state file if missing, copies the editable local config if missing, and prints the exact scheduler commands for your install path.

If `setup.sh` runs as root and `/usr/local/bin/skillminer` does not already exist, it also installs a convenience symlink to `scripts/skillminer`.

**3. Run one manual scan first**
```bash
CLAWD_DIR="${CLAWD_DIR:-$HOME/clawd}" bash scripts/run-nightly-scan.sh
```

Check the result locally:
```bash
ls state/review/
cat state/logs/scan-*.log | tail -n 40
```

**4. Only then add the two scheduler jobs**

Use your local timezone in the scheduler configuration, for example `<Your/Timezone>`.
Use `payload.kind: "agentTurn"` with the full dispatcher prompt inline, and let cron handle delivery via `delivery.mode: "announce"`.
The dispatcher uses the bash tool to execute the wrapper, which handles flock, backup, and atomic `.tmp` promotion.
Do not inline `prompts/nightly-scan.md` or `prompts/skill-writer.md` directly in cron.

Nightly scan example:
```json
{
  "name": "skillminer-nightly-scan",
  "schedule": { "cron": "0 4 * * *", "timezone": "<Your/Timezone>" },
  "payload": {
    "kind": "agentTurn",
    "message": "<contents of prompts/cron-dispatch-nightly.md>",
    "model": "github-copilot/claude-sonnet-4.6",
    "timeoutSeconds": 900
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "telegram:<chat-id>:topic:<topic-id>"
  }
}
```

Morning write uses the same pattern with `prompts/cron-dispatch-morning.md` as the inline `message`.
The wrapper still reads `prompts/nightly-scan.md` and `prompts/skill-writer.md` internally for the actual analysis and drafting work.

## Configuration

Edit `config/skill-miner.config.local.json`:

| Key | Default | Description |
|---|---|---|
| `scan.windowDays` | `10` | Days of memory to scan each night |
| `scan.minOccurrences` | `3` | Minimum occurrences before proposing a candidate |
| `scan.minDistinctDays` | `2` | Candidate must span at least this many days |
| `scan.cooldownDays` | `30` | Rejection/defer cooldown |
| `thresholds.low` | `3` | Low-confidence candidate band starts here |
| `thresholds.medium` | `4` | Medium-confidence candidate band starts here |
| `thresholds.high` | `6` | High-confidence candidate band starts here |
| `notifications.enabled` | `false` | Legacy setting. Scheduled notifications should come from cron `delivery.mode: "announce"` instead. |
| `notifications.channel` | `null` | Legacy setting. Leave unset for cron announce delivery. |
| `notifications.threadId` | `null` | Legacy setting. Leave unset for cron announce delivery. |
| `runner.default` | `openclaw` | `openclaw` or `claude` |
| `runner.openclaw_agent` | `main` | OpenClaw agent ID for the local runner |

## Exit codes

- `0`: success
- `2`: validation or atomic-write failure, wrapper restored the last `state.json` backup
- `3`: skipped because another skillminer instance already holds the lock

## Manual runs

Run a scan manually:
```bash
skillminer scan
```

Run the writer manually:
```bash
skillminer write
```

Run both sequentially:
```bash
skillminer full
```

See current timestamps and pending count:
```bash
skillminer status
```

Show the subcommand help:
```bash
skillminer help
```

When to use manual triggers:
- A new important memory file just landed and you do not want to wait until 02:00 UTC
- You want to test the richer scan output today
- Another agent or session wants to trigger scan or write
- You are on SSH and want a short path-style command

## Notifications

Scheduled notifications should come from cron `delivery.mode: "announce"`, not from inside the prompts.
If no announcement arrives, check the cron job delivery target first, then look at the local files:
```bash
ls state/review/
ls state/write-log/
```

## Promoting a drafted skill

After the morning write:
```bash
ls "${CLAWD_DIR:-$HOME/clawd}/skills/_pending/"
```

Review the draft, then promote manually:
```bash
mv "${CLAWD_DIR:-$HOME/clawd}/skills/_pending/my-skill" "${CLAWD_DIR:-$HOME/clawd}/skills/"
```

## Troubleshooting

**No chat notification received**
- Check cron `delivery.mode` and `delivery.to` first
- The supported scheduled target is your desired channel/topic via cron announce delivery
- Then check local review and log files

**Nothing was drafted at 10:00**
- Check that you accepted at least one candidate before 10:00
- Check `cat state/state.json | jq '.candidates'`

**Reset state**
```bash
cp state-template.json state/state.json
```
