# HEARTBEAT.md - VexPath Heartbeat Checks

## Frequency
Every heartbeat poll (~30 minutes)

## Checklist

Run these checks on each heartbeat. Do all three in a single pass to minimize API calls.

---

### ✉️ 1. Email Triage (Every Heartbeat)

```
1. Run: himalaya envelope list --account [account] --folder INBOX --page-size 20 --output json
2. Filter for unread emails received since last check
3. Apply 10-point extraction (references/email-triage.md) for each non-spam email
4. Flag Critical and High urgency items immediately
5. For any draft replies: present for approval before sending
6. Update memory/follow-ups.json with new follow-up entries
7. Log triage summary in memory/YYYY-MM-DD.md
```

If no new emails: log "inbox checked — no new messages" and continue.

---

### 📋 2. Follow-Up Check (Every Heartbeat)

```
1. Load memory/follow-ups.json
2. Find entries where: status = "open" AND due <= today
3. For each triggered follow-up: draft the appropriate message
4. Present drafts for approval
5. Update status to "sent" after sending
6. Flag any escalations (overdue items past threshold)
```

---

### 📅 3. Calendar Check (Every 4 Hours)

Only run if last calendar check was > 4 hours ago (track in memory/heartbeat-state.json).

```
1. Check for events in next 24–48 hours
2. Flag any events within 2 hours that need prep or client communication
3. Check for scheduling requests awaiting confirmation
```

Track last check time:
```json
{
  "lastChecks": {
    "email": [unix timestamp],
    "followUps": [unix timestamp],
    "calendar": [unix timestamp]
  }
}
```

---

## When to Notify

**Always notify owner when:**
- Critical or High urgency email received
- Follow-up overdue by more than 1 day
- Calendar event within 2 hours
- Payment overdue > 14 days
- Escalation triggered

**Stay quiet when:**
- Inbox has no new emails
- No follow-ups triggered
- Nothing actionable found
- Between 23:00–08:00 local time unless Critical

---

## Output Format

When notifying:
```
⚡ VEX CHECK-IN — [time]

📧 EMAIL: [N] new, [N] require action
  → [summary of most urgent item]

📋 FOLLOW-UPS: [N] triggered
  → [most urgent follow-up]

📅 CALENDAR: [next event or "clear"]

ACTION REQUIRED: [specific ask or "none"]
```

When nothing actionable: `HEARTBEAT_OK`
