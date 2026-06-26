# Follow-Up Tracking Reference

## Overview

Every outbound message or inbound lead that doesn't get resolved in one exchange needs a follow-up entry. This system tracks status, triggers reminders, and escalates when needed.

---

## Follow-Up Entry Fields

Every follow-up entry must include:

```
ID:           [auto-generated or sequential]
Type:         [outbound / inbound-pending]
Contact:      [name + email]
Subject:      [email subject or topic]
Thread ID:    [email thread ID if applicable]
Created:      [date created]
Due:          [date follow-up should trigger]
Status:       [open / sent / resolved / escalated / cancelled]
Priority:     [Low / Medium / High / Critical]
Last Action:  [description of last thing done]
Next Action:  [what to do when triggered]
Notes:        [any context]
Approval Req: [Yes / No]
```

---

## Trigger Rules

### Auto-Create Follow-Up From Email Triage

| Email Category | Auto-Trigger | Default Window |
|----------------|--------------|----------------|
| New Lead (no reply sent yet) | Yes | 24 hours |
| Quote Request (draft sent, awaiting reply) | Yes | 3 business days |
| Scheduling Request (sent options, no confirm) | Yes | 1 business day |
| Invoice/Payment (overdue) | Yes | 7 days post-due |
| Awaiting Response | Yes | 3 business days |
| Follow-Up Needed | Yes | Immediate (today) |
| Existing Client (unanswered) | Yes | 2 business days |
| Urgent Issue (pending resolution) | Yes | 4 hours |

### Manual Follow-Up Creation

Trigger manually when:
- Owner says "check back on this in X days"
- Contract renewal date is approaching
- Client went quiet mid-project
- Payment plan installment is due

---

## Escalation Rules

| Condition | Escalation Action |
|-----------|-------------------|
| Follow-up sent twice with no response | Upgrade to High priority; notify owner |
| Critical item unresolved > 2 hours | Flag immediately to owner |
| Quote not accepted after 7 days | Escalate: check-in call suggested |
| Invoice overdue > 14 days | Escalate: formal overdue notice, flag for owner action |
| Client silent > 14 days mid-project | Escalate: project risk flag |

---

## Status Definitions

| Status | Meaning |
|--------|---------|
| **Open** | Follow-up is active, not yet triggered |
| **Sent** | Follow-up message drafted/sent; awaiting reply |
| **Resolved** | Contact responded; follow-up closed |
| **Escalated** | Moved to higher priority or owner intervention required |
| **Cancelled** | No longer needed (resolved externally, client withdrew, etc.) |

---

## Follow-Up Message Templates

### New Lead (No Response After 24h)
```
Subject: Re: [original subject]

Hi [name],

Just following up on my message from [date]. Wanted to make sure it didn't get buried.

[brief restate of what was offered or asked]

Let me know if you have any questions or if you'd like to move forward.

[signature]
```

### Quote Pending (3 Days No Reply)
```
Subject: Re: [quote subject]

Hi [name],

Checking back on the proposal I sent over on [date]. Happy to answer any questions or adjust anything to better fit your needs.

[signature]
```

### Overdue Invoice (7 Days Past Due)
```
Subject: Invoice [#] — Past Due

Hi [name],

This is a friendly reminder that Invoice [#] for [amount] was due on [date].

Please let me know if there's an issue or if you need an alternate payment method.

[payment link or instructions]

[signature]
```

### Scheduling No Confirmation
```
Subject: Re: [scheduling subject]

Hi [name],

Just checking in — did any of the times I sent work for you? Happy to find something that fits your schedule.

[signature]
```

---

## Approval Gates

All follow-up messages require approval before sending unless:
- The client has explicitly permitted auto-send for specific message types
- The message is a pre-approved template with no variable fields remaining

**Approval format:**
```
FOLLOW-UP READY FOR APPROVAL
─────────────────────────────
To: [name] <[email]>
Re: [thread/subject]
Type: [follow-up type]
Last contact: [date]

Draft:
[message body]

Send? [Yes / No / Edit]
```

---

## Follow-Up Tracker Storage

Store follow-up state in `memory/follow-ups.json`:

```json
{
  "followUps": [
    {
      "id": "fu-001",
      "type": "outbound",
      "contact": "Jane Smith <jane@example.com>",
      "subject": "Proposal for Website Redesign",
      "created": "2026-01-10",
      "due": "2026-01-13",
      "status": "open",
      "priority": "High",
      "lastAction": "Sent proposal on 2026-01-10",
      "nextAction": "Send follow-up if no reply by 2026-01-13",
      "approvalRequired": true
    }
  ]
}
```

---

## Heartbeat Follow-Up Check

During each heartbeat:
1. Load `memory/follow-ups.json`
2. Filter for entries where `due <= today` and `status = open`
3. For each triggered entry: draft follow-up message
4. Present to owner for approval
5. Update status to `sent` after sending
6. Log in `memory/YYYY-MM-DD.md`

---

## Weekly Follow-Up Report

Produce once per week (or on request):

```
FOLLOW-UP REPORT — Week of [date]
───────────────────────────────────
Open:      [count]
Sent:      [count]
Resolved:  [count]
Escalated: [count]
Overdue:   [count]

Top Priorities:
  1. [name] — [subject] — [days overdue]
  2. [name] — [subject] — [days overdue]
  ...

Recommended Actions:
  [list of specific next steps]
```
