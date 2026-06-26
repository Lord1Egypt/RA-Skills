# Email Triage Reference

## Overview

Every email that enters the inbox gets classified, extracted, and routed. No email sits without an assigned category and next action.

---

## 12 Categories

| # | Category | Definition |
|---|----------|------------|
| 1 | **New Lead** | First contact from someone not yet in the system |
| 2 | **Existing Client** | Message from a known, active client |
| 3 | **Urgent Issue** | Time-sensitive problem requiring immediate action |
| 4 | **Scheduling Request** | Request to book, change, or cancel an appointment |
| 5 | **Quote Request** | Request for pricing, proposal, or estimate |
| 6 | **Invoice/Payment** | Payment received, invoice sent, overdue notice, billing question |
| 7 | **Contract/Agreement** | Signed docs, agreements, proposals requiring review |
| 8 | **Support Request** | Technical help, troubleshooting, service issue |
| 9 | **Spam/Low Priority** | Newsletters, cold outreach, irrelevant messages |
| 10 | **Follow-Up Needed** | Thread requires a response that hasn't been sent |
| 11 | **Awaiting Response** | Message sent; waiting for reply from the other party |
| 12 | **Human Approval Required** | Cannot proceed without owner decision |

---

## 10-Point Extraction

Run this extraction for every email that is not Spam/Low Priority:

```
1. SENDER          — Full name, company, email address
2. NEED            — What they are asking for or what happened
3. URGENCY         — Low / Medium / High / Critical
4. CATEGORY        — One of the 12 categories above
5. MISSING INFO    — What information is absent that is needed to act
6. NEXT ACTION     — Specific action to take (draft reply, create event, update CRM, etc.)
7. DRAFT REPLY     — Yes / No — should a reply be drafted for approval?
8. CALENDAR EVENT  — Yes / No — does this require a calendar event?
9. CRM UPDATE      — Yes / No / Field: [what to update]
10. HUMAN APPROVAL — Yes / No — does a human need to approve before any action is taken?
```

---

## Urgency Definitions

| Level | Meaning | Response Target |
|-------|---------|-----------------|
| **Critical** | Business-stopping issue, legal matter, payment failure, angry client escalation | < 1 hour |
| **High** | Active client with a time-sensitive need, same-day deadline | < 4 hours |
| **Medium** | Standard client or lead communication | < 24 hours |
| **Low** | Informational, no action required, or no clear deadline | 48–72 hours |

---

## Routing Rules

### New Lead
- Extract: name, contact info, service interest, how they found you
- Draft intro reply for approval
- Create CRM entry
- Flag for human review before sending

### Existing Client
- Cross-reference name/email against known client list
- Determine what phase of the engagement they are in
- Route to appropriate workflow (support, scheduling, billing, etc.)
- Draft reply if action is clear; flag if ambiguous

### Urgent Issue
- Immediately flag for human
- Draft acknowledgment reply: "We received your message and are looking into it now"
- Do not send without approval
- Escalate via secondary channel if no response from owner in 30 minutes

### Scheduling Request
- Check calendar availability
- Draft reply with 2–3 available time slots
- Create calendar hold if appointment is confirmed
- Send confirmation once approved

### Quote Request
- Extract: service requested, scope details, timeline, budget if mentioned
- Flag missing scope information
- Draft quote request acknowledgment if scope is unclear
- Route to owner for pricing; draft quote for approval once pricing is provided

### Invoice/Payment
- Extract: invoice number, amount, due date, status
- Flag overdue invoices (>7 days past due) as High urgency
- Draft payment confirmation or overdue reminder for approval
- Update payment status in CRM/sheet

### Contract/Agreement
- Extract: document type, parties involved, key terms, expiration
- Flag for human review — never respond to legal/contract items without approval
- Create calendar event for expiration or deadline dates

### Support Request
- Extract: issue description, affected service, impact severity
- Draft acknowledgment and estimated resolution time for approval
- Log issue in support tracker if available
- Escalate to Critical if client is blocked

### Spam/Low Priority
- Do not extract or route
- Mark as read
- Optionally unsubscribe if newsletter
- Log domain if repeated cold outreach

### Follow-Up Needed
- Identify original thread and last message date
- Draft follow-up message for approval
- Create reminder if follow-up is time-sensitive

### Awaiting Response
- Log thread in follow-up tracker with expected response date
- If no reply after defined window (default: 3 business days), escalate to Follow-Up Needed
- Do not send another message without approval

### Human Approval Required
- Summarize the situation clearly
- Provide recommended action and drafted response
- Do nothing until owner approves
- Label clearly: "ACTION REQUIRED: [summary]"

---

## Triage Output Format

```
────────────────────────────────
[CATEGORY] Subject: [subject line]
From: [Name] <[email]>
Date: [date received]
Urgency: [level]

NEED: [what they need]
MISSING: [any missing info]
ACTION: [recommended next step]

Draft Reply: Yes / No
Calendar Event: Yes / No
CRM Update: Yes / No — [field]
Human Approval: Yes / No
────────────────────────────────
```

---

## Integration Points

### CRM (Airtable / Google Sheets / Notion)
- Create new record for every New Lead
- Update record status for Existing Client interactions
- Log all Invoice/Payment actions
- Track Follow-Up and Awaiting Response threads

### Calendar (Google Calendar)
- Create events for: Scheduling Requests (confirmed), Contract deadlines, Payment due dates
- Add reminders for Follow-Up Needed items

### Follow-Up System
- Auto-create follow-up entry from: New Lead (no reply after 24h), Awaiting Response (no reply after 3 days), Follow-Up Needed (flagged)

### Dashboard / Reporting
- Daily triage summary: total emails, by category, urgent count, actions taken
- Weekly: new leads, reply rate, open follow-ups

---

## Batch Triage Process

When processing multiple emails at once:
1. Pull all unread emails
2. Sort by date descending (newest first)
3. Quick-scan subject + sender for Critical/Urgent flags
4. Extract all non-spam emails using 10-point system
5. Group by category
6. Present summary to owner with prioritized action list
7. Execute approved actions in order of urgency
