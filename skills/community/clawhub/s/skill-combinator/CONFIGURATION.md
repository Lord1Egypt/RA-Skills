# CONFIGURATION — Skill Combinator

Complete setup guide for the Skill Combinator meta-skill.

---

## Prerequisites

### 1. OpenClaw version
Requires OpenClaw v2026.1.0 or higher.

### 2. Minimum skills installed
You need at least 2 other skills installed for combinations to be possible.
The more skills your agent has, the more powerful this meta-skill becomes.

### 3. .learnings/ directory
The skill writes logs to `.learnings/`. This directory is created automatically
by the `self-improving-agent` skill (recommended). If you don't have it:

```bash
# Create manually inside your OpenClaw container
docker exec [your-container-name] mkdir -p /data/.openclaw/workspace/.learnings
docker exec [your-container-name] touch /data/.openclaw/workspace/.learnings/LEARNINGS.md
docker exec [your-container-name] touch /data/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md
docker exec [your-container-name] touch /data/.openclaw/workspace/.learnings/ERRORS.md
```

### 4. Environment variables
Add the following to your `.env` file (located at `/docker/[your-instance]/.env`):

```
# Required — used by OpenClaw to deliver the weekly report
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Optional — if not set, falls back to last active channel
TELEGRAM_CHAT_ID=your_chat_id_here
```

> ⚠️ These values are read from the environment at runtime.
> They are **never** logged, never written to workspace files, and never
> included in COMBINATIONS.md or .learnings entries.
> Keep them in `.env` only — never hardcode them anywhere else.

### 5. Notification channel
A Telegram bot configured in OpenClaw to receive the weekly report.
Verify your bot is active and your Chat ID is correct before running the first cron job.

---

## Installation

```bash
npx clawhub@latest install skill-combinator
```

This places the skill in `/data/.openclaw/workspace/skills/skill-combinator/`.

---

## Initial Setup (first run)

### Step 1 — Create COMBINATIONS.md
Create the catalogue file in your agent's workspace:

```bash
docker exec [your-container-name] bash -c "cat > /data/.openclaw/workspace/COMBINATIONS.md << 'EOF'
# COMBINATIONS.md — Emergent Capabilities Catalogue
# Managed by skill-combinator
# Format: see SKILL.md for entry structure

## No entries yet — agent is observing and accumulating data.
EOF"
```

### Step 2 — Configure the weekly cron job
In your OpenClaw dashboard → Cron Jobs → New Job:

| Field | Value |
|---|---|
| **Name** | `skill-combinator-weekly` |
| **Schedule** | `Cron` |
| **Expression** | `0 9 * * 0` |
| **Timezone** | Your local timezone |
| **Session** | `Isolated` |
| **Wake mode** | `Now` |
| **Payload** | `Run assistant task (isolated)` |
| **Model** | `claude-sonnet-4-6` (or equivalent reasoning model) |
| **Result delivery** | `Announce summary (default)` |
| **Channel** | Your configured channel |
| **To** | Your Chat ID |

For the **Assistant Task Prompt**, paste the full content from `cron-message.md`.

### Step 3 — Verify the skill is visible to your agent
Send your agent a message:
```
List all your installed skills.
```
You should see `skill-combinator` in the response.

---

## How the Agent Uses This Skill

### Automatic — on complex missions
When your agent receives a mission involving multiple domains, it will
automatically detect which skill combinations could apply and build a
multi-skill execution plan.

You don't need to instruct it explicitly — the skill description triggers
the behavior when the situation warrants it.

### Manual trigger
You can also ask your agent directly:
```
Before executing this task, check if any of your skills can be combined
to produce better results. Use your skill-combinator.
```

### Weekly report
Every Sunday at your configured time, your agent will send a structured
report to your notification channel summarizing:
- Emergent capabilities discovered during the week
- Proven combinations promoted to COMBINATIONS.md
- New skill proposals based on detected gaps

---

## Reading COMBINATIONS.md Over Time

After a few weeks of operation, your `COMBINATIONS.md` will contain entries like:

```markdown
## [2026-03-15] News-Driven Trade Entry

**Skills involved**: news-aggregator + trading-executor
**Mission context**: daily market scan
**Emergent capability**: open positions when macro news catalysts detected
**Mechanism**: news-aggregator detects high-impact events → trading-executor
  receives signal + context → enters with wider stops for volatility
**Performance**: tested 12 times | success rate 75%
**Status**: proven
**Confidence**: high
**ROI multiplier**: 2.5x
**Logged by**: agent autonomous discovery
```

This catalogue becomes your agent's institutional memory — competitive
knowledge that compounds over time.

---

## Troubleshooting

**Agent doesn't seem to use skill combinations**
→ Verify the skill is installed: `ls /data/.openclaw/workspace/skills/`
→ Make sure you have at least 2 other skills installed
→ Try triggering manually with an explicit instruction

**COMBINATIONS.md is empty after several weeks**
→ Check `.learnings/LEARNINGS.md` for `emergent_capability` entries
→ Verify the Sunday cron job is running (check OpenClaw Cron Jobs dashboard)
→ The agent needs complex multi-domain missions to discover combinations —
  simple single-skill tasks won't trigger discovery

**Weekly report not received**
→ Verify your Chat ID in the cron job configuration
→ Check OpenClaw Logs for the Sunday job execution
→ Verify your notification channel is properly configured

**`.learnings/` directory missing**
→ See Prerequisites → Step 3 above to create it manually
→ Or install `self-improving-agent` skill which creates it automatically

---

## Compatibility

| Component | Requirement |
|---|---|
| OpenClaw | v2026.1.0+ |
| Minimum skills | 2+ other skills |
| `.learnings/` | Required (manual or via self-improving-agent) |
| Notification channel | Recommended (for weekly reports) |
| Model | Reasoning model recommended (sonnet-class or above) |

---

## File Locations

```
/data/.openclaw/workspace/
├── COMBINATIONS.md                          ← create at setup
├── skills/skill-combinator/SKILL.md         ← installed by clawhub
└── .learnings/
    ├── LEARNINGS.md                         ← combination logs
    └── FEATURE_REQUESTS.md                  ← skill gap proposals
```
