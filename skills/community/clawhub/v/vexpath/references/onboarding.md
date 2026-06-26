# Client Onboarding Reference

## First-Run Auto-Detection

When VexPath loads and no email config exists (`~/.config/himalaya/config.toml` missing or empty), treat this as a **first run**. Automatically enter onboarding mode:

1. Introduce yourself as VEX — their new operations engine
2. Explain what VexPath does in 2-3 sentences (no jargon)
3. Ask for their **email address** and **display name**
4. Ask them to generate an app password (provide link + instructions for their provider)
5. Ask for their **business type** (agency / service / e-commerce / local / saas)
6. Run `scripts/setup-email.sh` with their credentials
7. Run `scripts/first-triage.sh` and present results using email triage categories
8. Confirm setup is complete and explain what happens next (heartbeat monitoring, follow-ups)

Keep the tone direct, professional, and calm. Make the client feel like they just hired a senior ops person.

---

## Overview

First-run setup flow for configuring a VexPath instance on a new client's OpenClaw installation. Completes in one session when all intake information is available.

---

## Step 1: Detect Email Provider

Check the email domain from intake answers:
- `@gmail.com` → Gmail
- `@outlook.com`, `@hotmail.com`, `@live.com` → Outlook / Microsoft 365
- `@[custom domain]` → Check MX records or ask; default assumption: Hostinger if client is small business

If uncertain, ask: "What email service do you use? (Gmail, Outlook, or a custom domain like Hostinger?)"

---

## Step 2: Configure himalaya

Run: `scripts/setup-email.sh [email] "[Display Name]" "[app password]"`

Provider-specific setup details: `references/gmail-setup.md`

Verify connection after setup:
```bash
himalaya envelope list --account [account-name] --folder INBOX --max-width 80
```

If connection fails → Read `references/gmail-setup.md` troubleshooting section.

---

## Step 3: Connect Calendar

Ask for calendar access method:
- **Google Calendar:** Confirm which Google account; note calendar ID
- **Outlook Calendar:** Note exchange/Office 365 credentials
- **Other:** Document manually

Store calendar connection details in workspace `TOOLS.md`.

---

## Step 4: Identify Business Type

Ask or infer from intake answers. Map to one of five profiles:

| Profile | Signals |
|---------|---------|
| **Agency** | Has clients, manages projects, delivers creative or digital services |
| **Service Business** | Provides skilled services (consulting, coaching, trades, legal, medical) |
| **E-commerce** | Sells physical or digital products, has order/fulfillment operations |
| **Local Business** | Physical location, appointment-based, community-focused |
| **SaaS** | Software product, subscription model, tech-forward operations |

---

## Business Type Profiles

### Agency

**Default triage priorities:** New Lead (High), Quote Request (High), Existing Client (Medium), Invoice (Medium)

**Default workflow templates:**
- Client intake → project kickoff
- Milestone tracking and update emails
- Invoice send → payment tracking
- Project completion → review request

**Key integrations:** Project management (Notion/Asana), Google Drive, client communication tracker

**Common bottlenecks:** Slow intake, missed follow-ups on proposals, no review/testimonial system

---

### Service Business

**Default triage priorities:** New Lead (High), Scheduling Request (High), Urgent Issue (Critical), Quote Request (Medium)

**Default workflow templates:**
- Lead capture → estimate → scheduling
- Appointment reminder (24h + 1h before)
- Post-service follow-up → review request
- Overdue invoice reminder sequence

**Key integrations:** Booking system (Calendly/Acuity), payment processor, email

**Common bottlenecks:** Manual scheduling, no-shows, no follow-up system, inconsistent intake

---

### E-commerce

**Default triage priorities:** Urgent Issue (Critical), Support Request (High), Invoice (Medium), Existing Client (Medium)

**Default workflow templates:**
- Order confirmation → shipping update → delivery confirmation
- Support ticket intake and routing
- Abandoned cart or re-engagement email
- Review request post-delivery

**Key integrations:** Shopify/WooCommerce, payment processor, shipping, email marketing

**Common bottlenecks:** Manual support responses, no post-purchase follow-up, zero review collection

---

### Local Business

**Default triage priorities:** Scheduling Request (High), New Lead (High), Urgent Issue (Critical), Follow-Up (Medium)

**Default workflow templates:**
- Inquiry → booking → reminder → follow-up
- No-show rebooking sequence
- Seasonal promotion broadcast
- Review request after visit

**Key integrations:** Booking system, Google Business, SMS/email

**Common bottlenecks:** Missed inquiries, no-shows, no review strategy, disorganized leads

---

### SaaS

**Default triage priorities:** Urgent Issue (Critical), Support Request (High), New Lead (High), Invoice (Medium)

**Default workflow templates:**
- Trial signup → onboarding sequence
- Feature request logging and routing
- Churn signal → retention outreach
- Invoice and subscription management

**Key integrations:** Help desk, CRM, payment processor, product analytics

**Common bottlenecks:** Manual support, no onboarding automation, poor churn detection

---

## Step 5: Set Preferences

Collect and record in workspace `TOOLS.md`:

```
Business Name: 
Business Type: [profile]
Owner Name:
Primary Email:
Calendar ID/System:
CRM Tool:
Project Management Tool:
Communication Channels (Slack/Discord/etc):
Preferred Reply Tone: [formal / conversational / direct]
Auto-send permitted: Yes / No (if No, all outbound requires approval)
Follow-up window: [days before follow-up triggers]
Triage frequency: [real-time / every 30 min / hourly / on-demand]
```

---

## Step 6: Run First Triage

Run: `scripts/first-triage.sh`

This pulls the last 50 emails and outputs a JSON summary.

Feed results through email triage process (`references/email-triage.md`).

Present categorized summary to client with:
- Total emails found
- Breakdown by category
- Urgent/Critical items flagged
- Recommended immediate actions
- Draft replies awaiting approval

---

## Onboarding Complete Checklist

```
[ ] Email provider identified
[ ] himalaya configured and connection verified
[ ] Calendar connected and noted
[ ] Business type profile selected
[ ] Preferences recorded in TOOLS.md
[ ] SOUL.md installed in workspace
[ ] HEARTBEAT.md installed in workspace
[ ] First triage completed
[ ] Initial action items presented to client
[ ] Workflow templates selected (reference: workflow-templates.md)
```

---

## Onboarding Output

Deliver a one-page setup summary to the client:

```
VexPath Setup Complete
─────────────────────
Business: [name]
Type: [profile]
Email: Connected — [provider]
Calendar: Connected — [system]
CRM: [tool or "not connected"]

First Triage Results:
  [N] total emails scanned
  [N] require your attention
  [N] urgent items flagged
  [N] draft replies ready for approval

Workflows configured: [list]
Next check-in: [next heartbeat or scheduled triage]
```
