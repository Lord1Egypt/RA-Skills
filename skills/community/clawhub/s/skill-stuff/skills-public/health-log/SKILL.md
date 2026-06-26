---
name: health-log
description: Logs medications, symptoms, and test results and generates pre-appointment summaries. Use when a user wants to remember what to tell their doctor.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "🩺"
  openclaw.user-invocable: "true"
  openclaw.category: life-admin
  openclaw.tags: "health,medical,medications,symptoms,doctor,appointments"
  openclaw.triggers: "log my symptoms,what medications am I on,health log,before my appointment,medical history"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/health-log


# Health Log

Every doctor's appointment starts with "any changes since last time?"
And most people can't remember.

This skill remembers. Not as a medical system — as a personal log you actually use.

---

## What it is and isn't

**It is:** a personal health journal. Your record of what happened, what you were told, what you're taking.

**It is not:** medical advice. It never diagnoses, prescribes, or recommends medical decisions.

Every output that touches health decisions ends with: *Speak to your doctor.*

---

## File structure

```
health-log/
  SKILL.md
  log.md             ← the health journal
  medications.md     ← current medications and supplements
  config.md          ← medication reminders, delivery
```

---

## What to log

**Appointments:**
Date, doctor/specialist, what was discussed, what was decided, any follow-up needed.

**Symptoms:**
When something is off. Not every headache — things worth noting. Duration, severity, context.

**Test results:**
Blood tests, scans, anything with a number. Store the result and what the doctor said about it.

**Medications:**
What you're taking, dose, frequency, what it's for, when started, any side effects noticed.

**Significant health events:**
Anything that changed your health picture meaningfully.

---

## Setup flow

### Step 1 — Seed from Gmail

Scan Gmail for:
- Appointment confirmations and reminders from healthcare providers
- Any health-related receipts (pharmacy, optician)
- Any results emails if applicable

Extract what's there. Don't invent what isn't.

### Step 2 — Current medications

Ask: "Are you taking any regular medications or supplements?"
For each: name, dose, frequency, what for.

### Step 3 — Any conditions to note

Ask: "Anything significant in your health history worth having on record?"
This is voluntary and completely private. User decides what to include.

### Step 4 — Medication reminders (optional)

For medications where timing matters:
Set a daily cron reminder.
"Time for [medication]."

Simple. Optional. Off by default.

### Step 5 — Write config.md

```md
# Health Log Config

## Medication reminders
enabled: [true/false]
times: [list]

## Delivery
channel: [CHANNEL]
to: [TARGET]

## Privacy
this file is private: true
never share in group chats: true
```

---

## Logging flow

**After an appointment:**
`/health log appointment` → agent asks: who, what was discussed, what was decided, follow-up needed.

**New symptom:**
`/health log symptom [description]` → logged with date and any context.

**Test result:**
`/health log result [test] [result]` → logged with doctor's interpretation if known.

**New medication:**
`/health add medication [name] [dose] [frequency] [reason]`

**Side effect noticed:**
`/health note [medication] [observation]`

---

## Before-appointment summary

`/health prep [appointment type]`

Generates a summary of everything relevant to bring to the appointment:
- Current medications list
- Any symptoms since last visit
- Any results since last visit
- Questions worth asking
- Last time this type of appointment happened and what was said

> **Pre-appointment summary — [TYPE] — [DATE]**
>
> **Current medications:**
> • [Medication] [dose] — since [date]
>
> **Since your last [type] appointment ([date]):**
> • [Any logged symptoms or events]
> • [Any results]
>
> **Possible questions:**
> • [Based on what's been logged — e.g. "Follow up on [result from X months ago]"]
>
> *Print this or show it at the appointment.*

---

## Privacy rules

SOUL principle: "Private things stay private. Period."

Health data is the most sensitive data this skill handles.

Rules:
- log.md is never read in a group chat context
- Health data is never included in morning briefing or other shared outputs
- The agent never volunteers health information — only responds to direct `/health` commands
- If asked about health in a context where others might see the output: decline and suggest using privately
- Never include health data in shareable outputs like the recap skill

---

## Management commands

- `/health log appointment` — log an appointment
- `/health log symptom [description]` — log a symptom
- `/health log result [test] [value]` — log a test result
- `/health add medication [name] [dose] [freq] [reason]` — add medication
- `/health prep [appointment type]` — pre-appointment summary
- `/health medications` — show current medications list
- `/health history [timeframe]` — show log for a period
- `/health note [medication] [observation]` — add note on a medication

---

## What makes it good

The pre-appointment summary is the most immediately useful output.
"What medications are you on?" at the doctor's desk — answered in 10 seconds.

The medication list is the second most useful.
Emergency situations, new prescriptions, interactions — having an accurate list matters.

The privacy rules are explicit and strict.
Health data is intimate. The skill handles it accordingly.
