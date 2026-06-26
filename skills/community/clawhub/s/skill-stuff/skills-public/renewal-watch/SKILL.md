---
name: renewal-watch
description: Tracks every expiry including passport, insurance, and MOT and alerts at the right lead time. Use when a user wants to never miss a renewal or pay a late fee.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "📋"
  openclaw.user-invocable: "true"
  openclaw.category: life-admin
  openclaw.tags: "renewals,passport,insurance,MOT,licence,expiry,documents,reminders"
  openclaw.triggers: "my passport expires,renewal reminder,track my renewals,document expiry,insurance renewal,MOT"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/renewal-watch


# Renewal Watch

Passport. Driving licence. Insurance. Visa. MOT. Subscriptions.
Everything that expires quietly and costs you when you miss it.

Set it up once. Never pay a late renewal fee again.

---

## File structure

```
renewal-watch/
  SKILL.md
  renewals.md      ← everything being tracked with expiry dates and lead times
  config.md        ← alert preferences, delivery
```

Token discipline: daily cron reads only `renewals.md` + `config.md`.

---

## Categories tracked

**Documents**
Passport, driving licence, national ID, visa, residence permit, work permit

**Vehicles**
MOT, road tax, vehicle insurance, breakdown cover

**Home**
Home insurance, contents insurance, boiler service, gas safety certificate, mortgage fixed term

**Health**
Private health insurance, dental plan, prescription prepayment certificate, gym membership

**Finance**
Credit card 0% period, loan fixed term, savings account bonus rate expiry

**Professional**
Professional memberships, certifications, bar registration, medical licence, DBS check

**Subscriptions**
Any subscription the user wants to track (with price, so they can decide whether to renew)

**Custom**
Anything else the user adds

---

## Setup flow

### Step 1 — Quick scan

Ask: "What documents and subscriptions do you want to track?"

Also offer to pull from Gmail automatically:
- Search for renewal confirmation emails
- Search for "expires", "renewal", "MOT", "insurance" in sent/received
- Build initial list from what's found

### Step 2 — Build renewals.md

For each item:

```md
# Renewals

## [ITEM NAME]
Category: [document / vehicle / home / health / finance / professional / subscription / custom]
Expiry date: [DATE]
Renewal lead time: [how many days before to alert — default by category]
Cost to renew: [if known]
Where to renew: [URL or institution]
Notes: [anything useful]
Status: active / alerted / renewed / cancelled
```

**Default lead times by category:**

| Category | First alert | Reminder |
|---|---|---|
| Passport | 9 months before | 6 months, 3 months |
| Visa / permit | 3 months | 2 months, 1 month |
| Driving licence | 3 months | 1 month |
| MOT | 1 month | 2 weeks, 3 days |
| Insurance | 1 month | 2 weeks |
| Mortgage fixed term | 6 months | 3 months |
| Certifications | 3 months | 1 month |
| Subscriptions | 2 weeks | 3 days |
| Custom | 1 month | 2 weeks |

User can override any of these.

### Step 3 — Write config.md

```md
# Renewal Watch Config

## Delivery
channel: [CHANNEL]
to: [TARGET]
check time: 08:00 daily

## Alert on
- X days before (per category defaults or custom)
- Subscription price changes (if detectable)

## Silent when
Nothing coming up in the next [30] days
```

### Step 4 — Register cron job

```json
{
  "name": "Renewal Watch",
  "schedule": { "kind": "cron", "expr": "0 8 * * *", "tz": "<USER_TIMEZONE>" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run renewal-watch. Read {baseDir}/renewals.md and {baseDir}/config.md. Check if any item is within its alert window. If yes: send alert with renewal details and where to act. If no alerts due today: exit silently. Update status in renewals.md.",
    "lightContext": true
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL>", "to": "<TARGET>", "bestEffort": true }
}
```

---

## Runtime flow

### 1. Check renewals.md

For each active item, calculate days until expiry.
Compare to lead time for that category.
If within the alert window and not already alerted today: flag it.
If nothing flagged: silent exit.

### 2. Format alert

One item per alert. Clear, actionable.

**📋 [ITEM] expires in [X] days**

Expiry: [DATE]
[If cost known:] Cost to renew: [£/€/$X]
[Where to act:] [URL or institution]

[Any relevant note — "you usually need to apply 6 weeks before for passport renewal to allow processing time"]

*Mark as renewed:* reply `/renewed [item]`

### 3. Escalation

If first alert was sent and not acknowledged within 2 weeks: send a shorter reminder.
If 3 days before expiry and still not renewed: send urgent alert regardless of prior alerts.

**🚨 [ITEM] expires in 3 days. Have you renewed?**

### 4. Update renewals.md

Mark item as "alerted" with today's date.
On `/renewed` command: update expiry date to new date, reset to "active".

---

## Management commands

- `/renewed [item]` — mark as renewed, enter new expiry date
- `/renew add [item] [date]` — add new item
- `/renew remove [item]` — stop tracking
- `/renew list` — show everything being tracked with days remaining
- `/renew upcoming` — show what's coming up in the next 90 days
- `/renew snooze [item] [days]` — delay alert by X days
- `/renew scan` — re-scan Gmail for renewal emails to update dates

---

## What makes it good

The lead times are calibrated to reality, not just "30 days before".
A passport renewal with 9 months lead time exists because HMRC recommends applying 6 weeks before travel and some countries require 6 months validity.
An MOT alert 1 month out exists because garages get booked up.

The urgency escalation matters. The first alert can be ignored.
The 3-day alert cannot.

The `/renew scan` command is the recurring value — every few months, re-scan Gmail for new renewals and updates. Keeps the list current without manual entry.
