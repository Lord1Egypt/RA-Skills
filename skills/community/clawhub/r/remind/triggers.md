# Reminder Triggers

What qualifies as remindable — and what only looks like it.

## The Test

**Only remind about things the human already knows.** Two checks:
1. Could they have written it in their own calendar? → remindable.
2. Does "just a reminder that..." read naturally in front of it? If it needs "heads up" instead → Alert, not Remind.

---

## Valid Triggers (Human Already Aware)

| Type | Example | Why it's a reminder |
|------|---------|---------------------|
| Calendar event | Meeting at 3pm | They scheduled it |
| Deadline | Report due Friday | They accepted the date |
| Promise made | "I'll call mom tomorrow" | They committed out loud |
| Recurring obligation | Quarterly taxes | Known cycle, easy to lose track of |
| Stated intention with a date | "I need to renew my license before August" | Dated intention = commitment |
| Third-party commitment | "Ana said she'd send the doc Friday" | They know about it; the follow-up is theirs to make |

---

## NOT Triggers (Use Alert Instead)

| Type | Example | Why it's NOT a reminder |
|------|---------|-------------------------|
| Breaking news | "Stock just dropped 20%" | New information |
| System event | "Server went down" | They didn't know |
| External opportunity | "Sale ends today" | They never committed to it |
| Warning | "Weather turning bad" | New situation |

---

## Explicit Requests

| Pattern | Action |
|---------|--------|
| "Remind me to X at/in Y" | Create exactly as stated — overrides all learned preferences |
| "Remind me to X" (no time) | Create with the category default from timing.md; state the time back so they can correct it |
| "Don't let me forget X" | High stakes: add an earlier stage (timing.md, Adjustment Factors) |
| "Remind me later" | Ask "when?" once; if unanswered, next natural delivery slot |

---

## Implicit Detection

Commitment verbs decide, not topics:

| Signal | Read |
|--------|------|
| "I'll / I have to / I need to ... by \<time\>" | Commitment — remindable |
| "I should / I might / someday" | Musing — not remindable until it gets a date |
| Time attached to an event ("meeting is at 4") | Calendar event |
| "I hope I don't forget" | Stakes signal: remindable, add an extra stage |

For implicit detections, first 2 in a category: offer ("Want a nudge Friday morning?") before creating. After 2 acceptances, create silently (signal ladder, SKILL.md).

---

## Skip Detection

Don't create a reminder when:
- They mentioned it in the current conversation — aware right now
- No commitment verb and no date — still a musing
- Delegated to you ("Can you handle X?") — that's your task list now, not their memory; track it, don't remind them of it
- Routine they never miss — reminding it transfers habit ownership to you (SKILL.md, When NOT to Remind)
- **Default: still unclear** → apply the default row in SKILL.md's Situation → Play (high stakes: create and say so; low stakes: skip and watch)
