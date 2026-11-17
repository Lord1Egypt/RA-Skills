---
name: weekly-content-brief
description: "Scheduled WhatsApp briefing for content founders. Runs every Monday at 8 AM. Reads your content calendar file and sends a weekly brief. Covers what is due, what shipped last week, and one suggested focus area."
---

# Weekly Content Brief
# Standalone free skill. Part of the Content Operator bundle in Claw Camp.
# For founders running TikTok, newsletters, YouTube, or any content business.

---

## Before You Load This Skill

Your agent reads a content calendar file you maintain on your server.

**Create your content calendar:**

In the browser console, run:

```
echo "# Content Calendar" > ~/content-calendar.md
```

Then open the file and add your upcoming posts. One line per post works fine. Example:

```
Week of May 12
- TikTok: AI hook video, due Tuesday
- Newsletter: Issue 14, due Wednesday
- YouTube: tool walkthrough, due Friday
```

Update this file whenever your plan changes. Your agent reads it fresh each Monday.

---

## Skill: Weekly Content Brief

**Description:**
Runs every Monday morning. Reads your content calendar and recent session logs. Sends a brief to WhatsApp covering what is due this week, what shipped last week, and one suggested focus area.

**Trigger phrase:**
"Show me this week's content brief"

**Schedule:**
Every Monday at 8:00 AM in your local timezone.

**Cron Setup**

Run this command once in the browser console as the claw user. Replace `[YOUR_TIMEZONE]` with your timezone. Common examples: `America/New_York`, `Europe/London`, `Africa/Nairobi`, `Asia/Singapore`.

Full timezone list: [https://en.wikipedia.org/wiki/List_of_tz_database_time_zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). Use the value in the TZ identifier column.

```
PATH=/home/claw/.npm-global/bin:$PATH openclaw cron add --name "Weekly Content Brief" --cron "0 8 * * 1" --message "Show me this week's content brief" --tz "[YOUR_TIMEZONE]" --announce
```

Confirm it was created:

```
PATH=/home/claw/.npm-global/bin:$PATH openclaw cron list
```

The job should appear with status `idle`. It will run automatically next Monday at 8 AM.

**To test it immediately** without waiting for Monday:

```
PATH=/home/claw/.npm-global/bin:$PATH openclaw chat "Show me this week's content brief"
```

**Tools used:**
- exec (reads ~/content-calendar.md and session log files)
- message tool (sends the brief to WhatsApp)

**What your agent reads:**
- ~/content-calendar.md (your content schedule)
- The 5 most recent session log files from ~/.openclaw/agents/main/sessions/

**What your agent does not read:**
- Email
- Direct messages
- Any social platform API
- Any file outside the workspace or home directory

**Steps:**

1. Agent reads ~/content-calendar.md for the current week's schedule
2. Agent reads the 5 most recent session log files to identify what shipped last week
3. Agent identifies what is due this week, what shipped last week, and one suggested focus area
4. Agent sends a formatted brief to WhatsApp via the message tool

**safety_constraints:**
- permissions: read-only
- writes: none
- approval_tier: 1 (autonomous) - read-only query, no approval needed
- scope: ~/content-calendar.md, ~/.openclaw/agents/main/sessions/ only
- cannot_access: email, social accounts, platform APIs, any write operation
- on_error: send WhatsApp alert, do not retry automatically

---

## What a Typical Brief Looks Like

Your agent sends a WhatsApp message each Monday morning. Format:

```
Content brief: week of [date]

Due this week:
- [item], [day]
- [item], [day]

Shipped last week:
- [item]

Focus: [one suggested priority based on what is overdue or upcoming]
```

Short. No fluff. Everything fits in one WhatsApp message.

---

## This Is One of Nine Skills

The full Content Operator bundle includes two more skills:
- Hook Performance Report (runs every Friday, ranks your best-performing hooks)
- Sunday Ops Summary (runs every Sunday, weekly close-out report)

All three bundles (Content Operator, SaaS Builder, Coach and Creator) are included in Claw Camp at $97. One payment, no subscription.
