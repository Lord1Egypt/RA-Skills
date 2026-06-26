---
name: masumi-connector
description: Manages the connection between OpenClaw and the Masumi agent network. Dispatches jobs overnight, collects results at wake-up, handles payment escrow, and presents a harvest summary. Use when a skill needs to offload compute to a cloud agent that runs while the laptop is closed.
license: MIT
compatibility: Requires Masumi network API key and ADA wallet funding.
metadata:
  openclaw.emoji: "🔗"
  openclaw.user-invocable: "true"
  openclaw.category: infrastructure
  openclaw.tags: "masumi,agents,cloud,offload,async,overnight,harvest,compute,cardano"
  openclaw.triggers: "masumi,agent pool,overnight results,what ran overnight,collect results,offload to cloud,remote agent"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/masumi-connector


# Masumi Connector

The bridge between OpenClaw and the Masumi agent network.

Dispatches jobs to cloud agents when you close the laptop.
Collects results when OpenClaw wakes up.
Handles payment escrow automatically.
Presents a morning harvest summary of everything that ran overnight.

---

## File structure

```
masumi-connector/
  SKILL.md
  config.md          ← Masumi API endpoint, wallet, agent registry
  jobs.md            ← active and completed job log
  agents.md          ← known Masumi agents with capabilities and pricing
  config-tokens.md   ← per-agent token permissions (sensitive, encrypted)
```

---

## The Harvest and Execute pattern

```
Evening / overnight:
  OpenClaw dispatches jobs → Masumi agents (funds locked in escrow)
  Masumi agents work while laptop is closed
  Results submitted on-chain with hash

Morning (OpenClaw wake-up):
  masumi-connector polls for completed jobs
  Verifies result hashes
  Collects results
  Presents harvest summary
  Triggers local authenticated actions (browser posting, email sending)
  Releases escrow payments
```

---

## Setup

### Step 1 — Masumi account

1. Create an account at masumi.network
2. Fund your purchasing wallet with ADA or supported stablecoins
3. Get your API key from the Masumi dashboard

### Step 2 — Write config.md

```md
# Masumi Connector Config

## API
endpoint: https://api.masumi.network
api_key: [stored in OpenClaw secrets, not here]
wallet: [purchasing wallet address]
network: mainnet  # or preprod for testing

## Harvest schedule
harvest_time: 07:00  # when OpenClaw collects overnight results
wake_trigger: true   # also harvest on any OpenClaw session start

## Budget
monthly_budget: [optional cap in ADA or USD equivalent]
alert_at: 80%  # alert when approaching monthly budget

## Token permissions (per agent — all off by default)
# gmail_read_only: [agent-id]  ← only enable after reviewing agent's DID
```

### Step 3 — Register known agents

Populate agents.md with the Masumi agents you want to use.
The agent registry is at explorer.masumi.network.

```md
# Known Agents

## research-agent
Masumi ID: [agent identifier from registry]
Capability: Deep multi-source research, structured briefing output
Pricing: ~0.5 ADA per job
Input schema: { query, depth, context }
Output schema: { bottom_line, established, contested, gaps, sources }
Trust level: verified (DID confirmed)
Token permissions: none

## content-generation-agent
Masumi ID: [agent identifier]
Capability: Multi-platform content generation from outline
Pricing: ~0.3 ADA per job
Input schema: { outline, voice_profile, platforms, performance_context }
Output schema: { substack, linkedin, twitter, instagram, reddit }
Trust level: verified
Token permissions: none

## monitoring-agent
Masumi ID: [agent identifier]
Capability: Continuous web monitoring with webhook delivery
Pricing: ~0.1 ADA per day
Input schema: { targets, topics, webhook_url, check_interval }
Output schema: webhook payload per event
Trust level: verified
Token permissions: none

## relationship-scoring-agent
Masumi ID: [agent identifier]
Capability: Contact scoring and opening line generation
Pricing: ~0.2 ADA per batch
Input schema: { contacts, scoring_criteria }
Output schema: { scored_contacts, opening_lines }
Trust level: verified
Token permissions: none  # gmail_read_only available as opt-in
```

### Step 4 — Register harvest cron

```json
{
  "name": "Masumi Harvest",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "<USER_TIMEZONE>" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run masumi-connector harvest. Read {baseDir}/config.md, {baseDir}/jobs.md, and {baseDir}/agents.md. Poll Masumi API for all completed jobs. Verify result hashes. Collect results. Update jobs.md. Build harvest summary. Trigger any local follow-up actions specified in job records. Release escrow for verified completed jobs.",
    "lightContext": true
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL>", "to": "<TARGET>", "bestEffort": true }
}
```

---

## Dispatching a job

Skills that support remote mode call the connector:

```
/masumi dispatch [agent-name] [input-json]
```

Or skills call it internally when `remote_mode: true` in their config.

### Dispatch flow

1. Look up agent in agents.md (ID, pricing, input schema)
2. Validate input matches agent's schema
3. Call Masumi Registry API — get `apiBaseUrl` and `sellerVkey`
4. Call agent's `POST /start_job` with input + random nonce
5. Get back `blockchainIdentifier` and timing params
6. Lock funds via Masumi Payment API `POST /purchase`
7. Poll until `FundsLocked` confirmed on-chain
8. Log job in jobs.md with status `running`

```md
# Jobs log entry (jobs.md)

## [JOB-ID]
Agent: [agent-name]
Masumi ID: [agent identifier]
Dispatched: [ISO timestamp]
Input summary: [brief — what was sent, not the full payload]
Input hash: [SHA-256 of input — for on-chain verification]
blockchainIdentifier: [from start_job response]
Status: running / completed / failed / disputed
Result: [null until harvested]
Follow-up: [local action to take on completion — e.g. "deliver via morning-briefing"]
Cost: [ADA amount]
```

---

## Harvest flow

At 07:00 daily (or on session start):

### 1. Poll for completed jobs

For each `running` job in jobs.md:
- Call Masumi Payment API `GET /purchase` with job's blockchainIdentifier
- Check `NextAction.requestedAction`

| State | Action |
|---|---|
| `FundsLocked` | Still running — check again tomorrow |
| `ResultSubmitted` | Result ready — collect it |
| `Completed` | Already settled — should have been collected earlier |
| `RefundRequested` | Something went wrong — flag for user review |
| `Disputed` | Escalate to user |

### 2. Collect results

For jobs in `ResultSubmitted` state:
- Call agent's result endpoint
- Verify result hash matches on-chain submission
- If hash mismatch: refuse result, request refund, flag to user
- If hash matches: accept result, update jobs.md

### 3. Build harvest summary

```
🔗 Overnight harvest — [DATE]

Completed (3):
• Research: "EU AI Act HR compliance" — ready for delivery
• Content drafts: "Thought on agency pricing" — 5 platforms ready for review
• Relationship scoring: 12 contacts scored — 3 worth reaching out to

Still running (1):
• Monitoring agent — continuous, checks in daily

Nothing to action today:
• [anything that doesn't need user input]

Cost this run: ~1.2 ADA (~$0.60)
Monthly spend: ~8.4 ADA / budget: 20 ADA
```

### 4. Route results to skills

Each job record in jobs.md has a `follow-up` field specifying what to do with the result:

```
research → deliver via research-brief format to user channel
content-drafts → pass to thought-leader for review gate
relationship-scoring → pass to biz-relationship-pulse for presentation
monitoring-alert → pass to content-monitor for delivery
```

The follow-up triggers the relevant skill to handle the result in its own format.
The connector doesn't know about the content — it's a delivery layer.

### 5. Trigger local authenticated actions

After user approval of any result that requires posting:

```
Content approved for LinkedIn:
  → Pass to content-publisher
  → content-publisher uses local headless browser (user's LinkedIn session)
  → Posts
  → Reports back

Content approved for email newsletter:
  → Pass to workspace-assistant
  → workspace-assistant uses Composio Gmail
  → Sends

Invoice approved for DATEV:
  → Pass to datev-uploader
  → datev-uploader uses local headless browser (DATEV session)
  → Uploads
```

The authentication split is:
- **Local browser** (LinkedIn, Reddit, Instagram, DATEV, any site with no API)
- **Composio** (Gmail, Calendar, Drive)
- **Direct API** (any service with a real API and API key)

### 6. Release escrow

For each verified result accepted:
- Call Masumi Payment API to confirm completion
- Escrow releases payment to the Masumi agent
- Log final cost in jobs.md

---

## Security

### Credentials never leave OpenClaw

Masumi agents receive **processed data**, not credentials.

When a skill needs to send user data to a Masumi agent:
1. OpenClaw collects the raw data (via Composio, local browser, or direct API)
2. OpenClaw strips and processes — removes PII not needed for the task
3. OpenClaw sends processed data to Masumi
4. Masumi never sees a password, cookie, session token, or OAuth token

**The only exception:** scoped, short-lived Composio tokens for explicitly
opted-in agents. See config-tokens.md.

### On-chain verification

Every Masumi job has an input hash committed on-chain before the agent starts.
The result must match to be accepted.

If a Masumi agent returns a result that doesn't match the committed hash:
- Result is rejected automatically
- Refund is requested
- User is alerted: "Agent [X] returned an unexpected result. Refund requested."

This is Masumi's decision logging — it provides an audit trail of what was
sent, what was returned, and that they match.

### Agent identity verification

Before dispatching a job to any agent:
- Check their DID (decentralised identity) on Masumi's registry
- Check their reputation score and transaction history
- Never dispatch to agents with no history or unverified identity

agents.md marks trust level per agent. Only `verified` agents receive jobs
by default. User can opt in to `unverified` agents explicitly.

### Budget protection

If a dispatch would exceed the monthly budget in config.md:
- Stop and alert the user
- "This job would bring monthly spend to [X], over your [Y] budget. Proceed?"
- Never auto-overspend

---

## Fallback behaviour

If Masumi is unavailable or a dispatch fails:

1. Log the failure in jobs.md
2. Fall back to local execution if the skill supports it
3. Alert user: "[Skill] fell back to local execution — Masumi unavailable"

The local skill always remains the fallback. Masumi is additive, not required.

---

## Management commands

- `/masumi dispatch [agent] [input]` — dispatch a job manually
- `/masumi harvest` — collect all pending results now
- `/masumi jobs` — show all active and recent jobs
- `/masumi jobs pending` — show jobs still running
- `/masumi status [job-id]` — check a specific job
- `/masumi agents` — list known agents from agents.md
- `/masumi budget` — show current month's spend vs budget
- `/masumi cancel [job-id]` — request refund for a running job
- `/masumi config` — show connector configuration
