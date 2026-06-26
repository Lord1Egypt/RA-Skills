---
name: meeting-notes
description: Extracts action items from meetings and tracks them to completion with owner and due date. Use when a user wants commitments from a meeting to not disappear.
license: MIT
compatibility: Requires OpenClaw. Composio Gmail optional for email context.
metadata:
  openclaw.emoji: "✏️"
  openclaw.user-invocable: "true"
  openclaw.category: communication
  openclaw.tags: "meetings,notes,actions,follow-up,accountability,tasks"
  openclaw.triggers: "meeting notes,action items,what was agreed,follow up from meeting,extract actions,meeting recap"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/meeting-notes


# Meeting Notes

Meetings generate commitments that disappear.
This skill captures them, owns them, and follows through.

---

## The problem it solves

People leave meetings with fuzzy action items.
Some get done. Most drift. Some surface three weeks later as crises.

This skill makes commitments explicit, assigns owners, and tracks them to completion.

---

## File structure

```
meeting-notes/
  SKILL.md
  actions.md         ← all open action items with owner, due date, status
  config.md          ← sources, reminder cadence, delivery
  archive/           ← completed meeting notes by date
```

---

## Input methods

**Voice memo or transcript:**
User sends recording or transcript after meeting.
Agent extracts notes.

**Manual dump:**
`/notes [meeting name]` → agent asks "what happened? what was decided? who's doing what?"
User types freely. Agent structures it.

**Calendar + email:**
If meeting-prep is installed: agent knows what the meeting was about.
Post-meeting: "How did the [meeting name] go?" — user responds, agent structures.

**Transcription service integration:**
If Otter.ai, Fathom, or Granola is connected: pull transcript automatically.

---

## Setup flow

### Step 1 — Sources

Check what's available:
- Transcription service (Otter, Fathom, Granola)
- Voice memo via mobile node
- Manual input
- Calendar + email context

### Step 2 — Reminder cadence

For action items assigned to the user:
- Default: reminder 24h before due date
- Weekly sweep: every Monday, surface all open items due that week

For items owned by others:
- Optional: gentle follow-up if item is overdue and the user wants to track it

### Step 3 — Write config.md

```md
# Meeting Notes Config

## Sources
transcription_service: [none / otter / fathom / granola]
voice_memo: true
manual: true

## My reminders
24h before due: true
weekly sweep: Monday 09:00

## Tracking others' items
track_others: true
follow_up_after_overdue: 3 days

## Delivery
channel: [CHANNEL]
to: [TARGET]
```

---

## Extraction flow

When notes arrive (any input method):

### 1. Identify the structure

Extract:
- Meeting name and date
- Attendees (if known)
- Key decisions made
- Action items: what, who, by when
- Open questions / things to resolve later
- Any commitments made to the user by others

### 2. Classify action items

For each action item:
- Owner: is it the user, or someone else?
- Due date: explicit ("by Friday") or inferred ("before next meeting")
- Priority: urgent / normal / low
- Dependencies: does this block or depend on anything?

### 3. Output the structured note

**✏️ [MEETING NAME] — [DATE]**

**Decided:**
• [Decision 1]
• [Decision 2]

**Actions — You:**
• [ ] [ACTION] — by [DATE]
• [ ] [ACTION] — by [DATE]

**Actions — Others:**
• [NAME]: [ACTION] — by [DATE]
• [NAME]: [ACTION] — by [DATE]

**Open questions:**
• [Question that needs answering before X]

**Next meeting:** [DATE if known]

### 4. Log to actions.md

Add all action items with status "open."

```md
# Open Actions

## [ACTION DESCRIPTION]
Meeting: [name] — [date]
Owner: [me / name]
Due: [date]
Status: open / in progress / done / overdue
Priority: urgent / normal / low
Notes: [any context]
```

---

## Follow-through

### Weekly sweep (Monday)

**✏️ Actions due this week:**

• [ ] [ACTION] — due [DATE] — from [MEETING]
• [ ] [ACTION] — due [DATE]

**Overdue:**
• [ACTION] — was due [DATE] — [days overdue]

### 24h reminder

"[ACTION] is due tomorrow — from the [MEETING] on [DATE]."

### Others' overdue items (if tracking enabled)

"[NAME] was supposed to [ACTION] by [DATE] — it's now [X days] overdue.
Worth a nudge?"

---

## Management commands

- `/notes [meeting name]` — start a note entry
- `/notes done [action]` — mark action complete
- `/notes extend [action] [new date]` — push deadline
- `/notes list` — show all open actions
- `/notes overdue` — show overdue items only
- `/notes meeting [name]` — show full notes for a specific meeting
- `/notes week` — show all actions due this week

---

## Integration with meeting-prep

If meeting-prep is installed:
- Pre-meeting: prep includes open actions from the last meeting with same attendees
- Post-meeting: agent prompts for notes and connects them to the prep context

The two skills form a complete meeting lifecycle:
prep → attend → notes → follow-through → prep (next meeting)

---

## What makes it good

The "others' items" tracking is underrated.
"Dmitri was supposed to send the contract by Wednesday — it's now Friday."
That's not nagging. That's information.

The weekly sweep on Monday is the right moment.
Monday morning is when people are planning. Surface open commitments then.

The connection back to the originating meeting matters.
"This action came from the product review on March 12" is more useful than an orphaned task.
