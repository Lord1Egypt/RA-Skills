---
name: small-cpa-firm
description: Practice management assistant for small CPA firms and solo bookkeepers — client onboarding, document chase, tax deadline tracking, entity compliance reminders, workflow automation, and recurring engagement management. Built for 1-5 partner firms and virtual bookkeeping shops.
---

# Small CPA Firm Assistant

Autonomous practice management for small accounting firms, solo CPAs, and bookkeeping services.

## What It Does

### Client Onboarding
- Generate customized onboarding checklists by engagement type (individual, S-Corp, C-Corp, partnership, nonprofit, trust)
- Track required documents: W-2s, 1099s, K-1s, prior returns, entity docs, bank statements
- Send automated welcome packets with engagement letters and document request lists
- Flag incomplete onboarding at 7/14/21 days with escalation reminders

### Document Chase
- Track outstanding documents per client with status (requested, reminded, received, reviewed)
- Automated reminder sequences: polite (day 7), firm (day 14), urgent (day 21), final (day 28)
- Generate document request emails customized by return type
- Dashboard view: who's complete, who's blocking, who needs a phone call

### Tax Calendar & Deadlines
- Master deadline calendar: 1040 (4/15), 1120-S (3/15), 1065 (3/15), 990 (5/15), extensions, quarterly estimates
- Per-client deadline tracking with extension status
- Alert at 30/14/7/3/1 days before each deadline
- Automatic extension reminder if documents not received by cutoff date
- State-specific deadline variations (Ohio CAT, municipal income tax)

### Entity Compliance Management
- Annual meeting minute reminders for all client entities (LLC, S-Corp, C-Corp)
- Registered agent renewal tracking
- State annual report filing deadlines by entity type and state
- S-Corp reasonable compensation review reminders (annually)
- BOI (Beneficial Ownership Information) report tracking

### Engagement & Workflow Management
- Track active engagements: tax prep, bookkeeping, advisory, payroll, entity formation
- Status pipeline per engagement: intake → in-progress → review → delivered → filed
- Reviewer assignment and review checklist generation
- Quality control: flag returns with unusual items (large deductions, missing schedules, YoY variance >20%)

### Recurring Services
- Monthly bookkeeping close checklist: bank rec, credit card rec, payroll journal, sales tax, accruals
- Quarterly estimate calculations and client notifications
- Payroll tax deposit reminders (semi-weekly, monthly, quarterly by deposit schedule)
- Year-end planning: estimated tax projection, retirement contribution deadlines, entity election deadlines (S-Corp 2553, fiscal year changes)

### Revenue & Practice Management
- Track WIP (work in progress) by client and engagement
- Time tracking summaries for billing
- Accounts receivable aging: 30/60/90 day follow-ups
- Client profitability analysis: revenue per client vs. hours spent
- Capacity planning: flag when staff utilization exceeds 85%

### KKOS-Aligned Entity Planning (Premium)
- Business entity optimization review triggers:
  - Schedule C net income >$40K → recommend LLC + S-Corp election analysis
  - Multiple entities → annual Trifecta compliance review (operating, holding, management)
  - Self-directed IRA / Solo 401(k) contribution deadline tracking
  - Asset protection structure review (annual)
- Generate entity structure diagrams from client data
- Compliance checklist by entity type (5 LLC types: operating, holding, management, land trust, statutory)

## Inputs
- Client list (name, entity type, fiscal year end, engagement types)
- Tax deadline preferences (extension default yes/no)
- Staff roster (for assignment)
- State(s) of operation per client

## Outputs
- Deadline alerts and document chase emails
- Onboarding packets and engagement letters
- Monthly/quarterly compliance reminders
- Practice dashboard: WIP, AR, capacity, deadline countdown
- Entity compliance reports

## Example Flows

### New Client Onboarding
1. User adds client: "New client: Smith Family Trust, 1041, Ohio, FYE 12/31"
2. Skill generates: onboarding checklist (trust document, K-1 beneficiary info, prior 3 years returns, EIN letter), welcome email draft, engagement letter template, deadline entry (4/15 with 9/15 extension)
3. Skill schedules: document chase sequence starting immediately, 30-day onboarding completion check

### Tax Season Workflow
1. February 1: Skill generates full season dashboard — all clients, deadlines, document status
2. Daily: flags clients with missing documents, suggests chase actions
3. Weekly: capacity report (hours booked vs. available), deadline countdown
4. March 1: urgent alerts for 3/15 S-Corp and partnership returns not yet in review
5. Post-deadline: extension tracking handoff, quarterly estimate reminders begin

### Entity Health Check
1. Triggered annually per entity client
2. Reviews: annual meeting minutes status, registered agent current, state filings up to date, S-Corp compensation reasonable, BOI report filed
3. Generates compliance report card with action items
4. Flags entities needing restructuring review (income thresholds, asset protection gaps)

## References
- `references/tax-deadline-calendar.md` — Federal + Ohio deadline master list
- `references/entity-compliance-checklist.md` — Annual requirements by entity type
- `references/document-request-templates.md` — Templates by return type

---

## Need Help Setting This Up?

This skill was built by **[ClawReady](https://clawreadynow.com)** — an OpenClaw setup and managed care service for CPA firms and small business operators.

If you want OpenClaw running properly at your firm (secure gateway, client-facing channels, skills wired up, auto-restart on updates) without the technical overhead — [book a free call](https://calendly.com/grofresh2018). Setup starts at $99.
