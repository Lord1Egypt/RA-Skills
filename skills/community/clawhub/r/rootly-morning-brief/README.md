# rootly-morning-brief

OpenClaw skill for a short daily Rootly briefing:
- active incidents
- incidents resolved in the last 24 hours
- who is on-call now
- overdue action items

The script prints the digest to stdout. OpenClaw cron `--announce` is what delivers that output to Slack.

## Phone Screenshot

This repo includes a real 8:00 AM phone delivery screenshot from the RootlyClaw app:
- `Output-screenshot.jpg`

![Rootly morning brief on phone](./Output-screenshot.jpg)

## Prerequisites

- OpenClaw is installed and running.
- Python 3 is available.
- For live Rootly data, you have a Rootly API key.
- For Slack delivery, Slack is already connected in OpenClaw.

## Install

ClawHub:
- Install the skill into your OpenClaw workspace.

Manual install:
- Copy this folder to `~/.openclaw/workspace/skills/rootly-morning-brief`
- For a named profile, use that profile's workspace instead

## Configure the Rootly API Key

You only need this for live Rootly data. Mock-data runs do not need an API key.

Recommended for OpenClaw:

```bash
mkdir -p "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/secrets"
printf '%s\n' 'YOUR_ROOTLY_API_KEY' > "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/secrets/rootly_api_key"
chmod 600 "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/secrets/rootly_api_key"
```

OpenClaw cron jobs do not inherit your shell env, so the secret file is the reliable path.

For temporary manual testing, this also works:

```bash
export ROOTLY_API_KEY="YOUR_ROOTLY_API_KEY"
```

Optional:

```bash
export ROOTLY_TIMEZONE="America/Toronto"
export ROOTLY_INCLUDE_PRIVATE="false"
```

## Step 1. Test Local Output with Real Data

This is the main path for the real daily use case.
Requires the Rootly API key from the section above. If you do not have one yet, skip to Step 2 (mock data).

```bash
python3 scripts/rootly_morning_brief.py
```

## Step 2. Test Local Output with Mock Data

Use this when you want to verify formatting without hitting the API.

```bash
python3 scripts/rootly_morning_brief.py --mock-data-dir ./mock-data
```

`./mock-data` is relative to the skill directory.

## Step 3. Test Slack Delivery Once

The script does not send to Slack by itself. OpenClaw cron `--announce` captures stdout and sends the briefing.

Start with the simplest path from the current or last chat context:

```bash
openclaw cron add \
  --name "Rootly morning brief test" \
  --at "+1m" \
  --delete-after-run \
  --session isolated \
  --light-context \
  --message "Use rootly-morning-brief. Run scripts/rootly_morning_brief.py and print the full digest." \
  --announce
```

If you want to pin a specific Slack channel instead:

```bash
openclaw cron add \
  --name "Rootly morning brief test" \
  --at "+1m" \
  --delete-after-run \
  --session isolated \
  --light-context \
  --message "Use rootly-morning-brief. Run scripts/rootly_morning_brief.py and print the full digest." \
  --announce \
  --channel slack \
  --to channel:C0123456789
```

If you want the one-time Slack test to use mock data, make the instruction explicit:

```bash
openclaw cron add \
  --name "Rootly morning brief test (mock)" \
  --at "+1m" \
  --delete-after-run \
  --session isolated \
  --light-context \
  --message 'Use the `rootly-morning-brief` skill. Run it with mock data from `./mock-data` and print the digest.' \
  --announce
```

You can wait a minute or force due jobs immediately:

```bash
openclaw cron run --due
```

## Step 4. Create the Daily Cron Job

After the one-time Slack test works, register the real daily job.

The requirements example uses `America/New_York`. This skill defaults to `America/Toronto` on purpose because that is the timezone the script and sample data were built around. Change it if your team wants a different local morning window.

Current or last chat context:

```bash
openclaw cron add \
  --name "Rootly morning brief" \
  --cron "0 8 * * *" \
  --tz "America/Toronto" \
  --session isolated \
  --light-context \
  --message "Use rootly-morning-brief. Run scripts/rootly_morning_brief.py and print the full digest." \
  --announce
```

Explicit Slack channel:

```bash
openclaw cron add \
  --name "Rootly morning brief" \
  --cron "0 8 * * *" \
  --tz "America/Toronto" \
  --session isolated \
  --light-context \
  --message "Use rootly-morning-brief. Run scripts/rootly_morning_brief.py and print the full digest." \
  --announce \
  --channel slack \
  --to channel:C0123456789
```

## Verify

List jobs:

```bash
openclaw cron list
```

Inspect runs for a job:

```bash
openclaw cron runs --id <job-id>
```

Run due jobs right now:

```bash
openclaw cron run --due
```

## Sample Output

```text
*Rootly Morning Brief* — Sun Mar 15
At a glance: 2 active (1 SEV0/SEV1) · 1 resolved in 24h · 2 on-call now · 1 overdue

*Active now*
• 🚨 <https://root.ly/gsif-3|Global sign-in failures after OIDC key rotation> — [SEV0] · [OPEN] · started Sun 6:42 AM
• 🟧 <https://root.ly/clsf-2|Checkout latency spike during us-east database failover> — [SEV2] · [OPEN] · started Sun 5:25 AM

*On-call now*
• Nicole Bu — L1 primary
• Jordan Patel — L2 secondary

*Overdue actions*
• ⚠️ <https://root.ly/gtb2es|Rotate CI deploy tokens and verify revocation in every production region.> — [P1] · due Sat 7:30 AM · Nicole Bu · SEC-742

*Resolved (24h)*
• <https://root.ly/ubaa-1|Unauthorized bastion access attempt blocked> — resolved Sun 12:02 AM
```

## Judgment Calls

- **Phone-first structure (simplified on purpose):** one top summary line + four fixed sections.  
  Why: on-call readers need fast scanability; alerting guidance emphasizes concise, actionable signal over dense context.
- **Action-first ordering:** active incidents, who is on-call now, overdue actions, then resolved(24h).  
  Why: this mirrors immediate operational questions before historical context.
- **Tight line grammar:** `title — status/severity/time` with one line per item.  
  Why: reduces cognitive load and supports sub-30-second mobile reading.
- **Severity and urgency visuals (non-flashy):** SEV-based badges (`🚨`, `🟥`, `🟧`) and priority chips (`[P1]`) on action items.  
  Why: faster triage scanning under pressure without adding long text.
- **Always render all sections:** explicit `No ...` lines instead of hiding empty groups.  
  Why: avoids ambiguity between “none” and “failed to load.”
- **Default cap = 3 items per section:** show top items, then `+N more`.  
  Why: prevents long digests from becoming pager-noise walls.
- **Only actionable metadata in the body:** assignee + due time for overdue actions; ticket key only when obvious.  
  Why: keep decision-relevant fields, skip verbose payload details.
- **Delivery abstraction:** script prints to stdout only; OpenClaw `cron --announce` handles Slack routing.  
  Why: cleaner separation of concerns and easier runtime debugging.
- **Explicit simplification vs full API coverage:** only `/v1/incidents`, `/v1/oncalls`, `/v1/action_items` are used.  
  Why: exactly matches required morning brief questions without overbuilding.

References used for formatting decisions:
- Google SRE guidance on actionable alerting and reducing noisy/non-actionable signal: https://sre.google/sre-book/practical-alerting/
- Atlassian incident communication tips (communicate early/often/precisely): https://support.atlassian.com/statuspage/docs/incident-communication-tips/
- Atlassian incident response handbook (short customer updates, explicit impact/next steps): https://www.atlassian.com/incident-management/handbook/incident-response

## What This Skill Does Not Set Up

- It does not connect OpenClaw to Slack for you.
- It does not manage its own Slack delivery. OpenClaw cron `--announce` handles that.
- It does not discover the correct Slack destination automatically.
- It does not make cron inherit shell env vars.

This skill is responsible for fetching Rootly data and formatting the briefing. OpenClaw is responsible for chat delivery and cron routing.
