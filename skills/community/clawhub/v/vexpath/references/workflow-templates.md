# Workflow Templates Reference

## Overview

Reusable workflow templates organized by business type. Each template includes trigger, steps, conditions, tools, and automation opportunities. Use as starting points — adapt to the specific client's stack.

---

## How to Use These Templates

1. Identify business type (from `onboarding.md` profiles)
2. Select the matching templates
3. For each template: confirm tools available, map to client's actual systems
4. Document the customized version in client workspace `TOOLS.md`
5. Build simple version first; add automation in phases

---

## Agency Templates

### AG-01: Client Intake → Project Kickoff

**Trigger:** New client inquiry or signed contract received

**Steps:**
1. Intake form submitted (or email received)
2. Auto-acknowledgment sent to prospect
3. Internal alert to owner for qualification
4. If qualified: send discovery call link or intake questionnaire
5. Discovery call completed
6. Proposal created and sent for approval
7. Proposal approved → send contract
8. Contract signed → create project in PM tool
9. Send kickoff email with timeline, deliverables, points of contact
10. Schedule kickoff call
11. Add client to CRM with full project details

**Conditions:**
- If prospect doesn't respond to intake ack within 24h → trigger follow-up
- If proposal not accepted within 7 days → send follow-up
- If contract not signed within 5 days → flag for owner

**Tools:** Email, Calendly, Google Docs/Notion, CRM, PM tool (Asana/Notion)

**Automation Opportunities:**
- Auto-send intake questionnaire after discovery call booked
- Auto-create project folder in Drive on contract sign
- Auto-assign team members in PM tool based on project type

---

### AG-02: Milestone Tracking + Client Updates

**Trigger:** Project created in PM tool

**Steps:**
1. Define milestones at project start (with dates)
2. 2 days before milestone: send internal reminder
3. On milestone date: if complete → send client update
4. If milestone delayed: draft delay notification for approval
5. On final delivery: send completion email with deliverables
6. 48 hours after delivery: send review request

**Conditions:**
- If milestone missed by more than 2 days → flag for owner
- If client hasn't acknowledged delivery within 3 days → send follow-up

**Tools:** PM tool, email, Google Calendar

**Automation Opportunities:**
- Auto-trigger update emails based on PM task completion
- Calendar events for all milestones at project start

---

### AG-03: Invoice Send → Payment Tracking

**Trigger:** Invoice date reached (monthly or project-based)

**Steps:**
1. Generate invoice from template
2. Send invoice with payment link for approval
3. Owner approves → invoice sent
4. Log in payment tracker
5. If unpaid after due date (+7 days): send reminder
6. If unpaid (+14 days): send formal overdue notice
7. If unpaid (+21 days): flag for owner (escalation)
8. On payment received: send receipt and update tracker

**Tools:** Invoice tool (FreshBooks/Wave/Stripe), email, Google Sheets

**Automation Opportunities:**
- Auto-generate recurring invoices on fixed schedule
- Auto-send reminders at day 7, 14, 21 overdue

---

## Service Business Templates

### SB-01: Lead Capture → Estimate → Scheduling

**Trigger:** New inquiry via contact form, email, or phone

**Steps:**
1. Lead inquiry received
2. Auto-acknowledgment: "We received your request and will be in touch within [X] hours"
3. Owner reviews and qualifies lead
4. If qualified: schedule consultation or send estimate request form
5. Estimate created based on scope
6. Estimate sent for approval → owner approves → sent to client
7. Client accepts → schedule service appointment
8. Confirmation email sent with date, time, and prep instructions
9. Reminder sent 24 hours before appointment
10. Reminder sent 1 hour before appointment

**Conditions:**
- If no response to estimate within 3 days → follow-up
- If appointment not confirmed 24h before → call/text follow-up

**Tools:** Email, Calendly or booking system, estimate tool, SMS (optional)

**Automation Opportunities:**
- Auto-send estimate request form after qualification
- Auto-send appointment reminders via calendar integration

---

### SB-02: Post-Service Follow-Up → Review Request

**Trigger:** Service appointment marked complete

**Steps:**
1. 4–6 hours after service: send thank-you email
2. Include: summary of what was done, any follow-up care instructions
3. 48 hours after service: send review request
   - Google Business or platform-specific link
4. If review left: thank-you reply (optional manual)
5. 30 days later: check-in email ("How has everything been?")
6. 30-day check-in: include referral ask or seasonal offer

**Tools:** Email, Google Business, CRM, scheduling tool

**Automation Opportunities:**
- Auto-trigger thank-you email when appointment status changes to "complete"
- Auto-queue review request on day 2

---

## E-commerce Templates

### EC-01: Order Confirmation → Shipping Update → Delivery

**Trigger:** Order placed

**Steps:**
1. Order confirmed: send order confirmation email with order details
2. Order fulfillment started: send "preparing your order" update (optional)
3. Shipped: send shipping confirmation with tracking link
4. Estimated delivery date -1 day: send "your order is almost here" email
5. Delivery confirmed: send delivery confirmation
6. 3 days after delivery: send review request
7. 30 days after delivery: send re-engagement offer

**Conditions:**
- If tracking shows delayed: send proactive delay notification
- If order not shipped within stated window: trigger internal alert

**Tools:** E-commerce platform, email marketing, shipping integration

---

### EC-02: Support Ticket Intake and Routing

**Trigger:** Customer support email or form submission

**Steps:**
1. Submission received: send acknowledgment with ticket number
2. Classify by issue type: refund, exchange, shipping, defect, account
3. Route to appropriate response template
4. Draft response for approval
5. Send approved response within defined SLA
6. If issue unresolved after 2 exchanges: escalate to human
7. On resolution: send satisfaction follow-up

**SLA targets:**
- Refund/defect: < 4 hours first response
- Shipping: < 8 hours
- General: < 24 hours

---

## Local Business Templates

### LB-01: Inquiry → Booking → Reminder → Follow-Up

**Trigger:** Inquiry via phone, email, form, or social media

**Steps:**
1. Inquiry received (any channel) → log in tracker
2. Auto-acknowledgment sent if via email/form
3. Owner or staff follows up with availability within [X] hours
4. Appointment booked → confirmation sent
5. 24 hours before: reminder sent (email or SMS)
6. 2 hours before: final reminder
7. Post-appointment: thank-you message
8. 48–72 hours after: review request
9. 30 days later: re-engagement check-in or seasonal offer

**Conditions:**
- If no-show: send rebooking offer within 2 hours
- If cancellation: offer rescheduling immediately

**Tools:** Booking system (Calendly/Acuity/Square Appointments), email, SMS

---

### LB-02: No-Show Rebooking Sequence

**Trigger:** Appointment marked as no-show

**Steps:**
1. 30 minutes after no-show: send "We missed you" message
2. Include: easy rebooking link
3. 24 hours later (if no rebooking): send second chance offer
4. 7 days later (if still no contact): send final re-engagement
5. If no response after 3 attempts: mark as inactive in CRM

**Tone:** Understanding, not accusatory. Keep the door open.

---

## Workflow Documentation Template

Use this format when documenting any custom workflow:

```
WORKFLOW: [Name]
─────────────────────────────
Business Type: [type]
Version: 1.0
Last Updated: [date]

TRIGGER:
  [What starts this workflow]

STEPS:
  1. [action]
  2. [action]
  ...

CONDITIONS:
  - If [X] → [action]
  - If [Y] → [action]

ERROR HANDLING:
  - If step [N] fails → [fallback action]
  - Notify: [who gets alerted]

HUMAN HANDOFF POINTS:
  - Step [N]: [requires approval for]

TOOLS REQUIRED:
  - [tool 1] — [what it does in this workflow]
  - [tool 2] — [what it does in this workflow]

OUTPUTS:
  - [what this workflow produces or updates]

AUTOMATION OPPORTUNITIES (Phase 2):
  - [what can be automated in a future iteration]

TIME SAVED:
  Estimated [X] hours/week once automated
```
