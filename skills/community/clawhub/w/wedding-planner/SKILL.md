---
name: Wedding Planner
slug: wedding-planner
version: 1.0.0
homepage: https://clawic.com/skills/wedding-planner
description: "Plan weddings with budget guardrails, guest-list scenarios, vendor scorecards, payment tracking, and deadline-driven coordination."
changelog: "Initial release with a complete wedding-planning system for budget, vendors, guests, timeline, and decision tracking."
metadata: {"clawdbot":{"emoji":"💍","requires":{"bins":[],"config":["~/wedding-planner/"]},"os":["linux","darwin","win32"],"configPaths":["~/wedding-planner/"]}}
---

## When to Use

Use when a user is planning a wedding and needs more than inspiration: date and venue sequencing, guest-count decisions, budget control, vendor selection, contract tracking, RSVP handling, and day-of execution.

This skill is for real operational planning, not just ideas. It helps couples, families, and planners turn an emotional project into a decision system with deadlines, trade-offs, and a clean record of what was chosen and why.

## Architecture

Memory lives in `~/wedding-planner/`. If `~/wedding-planner/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/wedding-planner/
├── memory.md                         # Activation rules, planning style, and active wedding context
├── weddings/
│   └── {event}/
│       ├── overview.md               # Date, venue, style, priorities, and stage
│       ├── budget.md                 # Budget ceiling, commitments, deposits, and due dates
│       ├── guest-list.md             # A/B/C invite counts, RSVP status, and seating notes
│       ├── vendors.md                # Shortlists, quotes, contract status, and risks
│       ├── timeline.md               # Backward plan from wedding date and day-of run-of-show
│       └── decisions.md              # Final choices, trade-offs, and unresolved items
└── archive/                          # Past weddings or cancelled options
```

## Quick Reference

Load only the file that matches the current planning bottleneck.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory schema and planning notebook structure | `memory-template.md` |
| Budget math, deposits, and payment discipline | `budget-and-payments.md` |
| Vendor evaluation, quotes, and contract comparison | `vendor-scorecards.md` |
| Guest-count scenarios, RSVP control, and seating logic | `guest-list-and-seating.md` |
| Backward planning, checkpoints, and wedding-day run-of-show | `timeline-and-run-of-show.md` |

## Requirements

- No credentials are required.
- Ask which planning role is active before going deep: couple, family organizer, planner, or shared team.
- Clarify the stage fast: just engaged, venue searching, booked date, vendor coordination, final month, or day-of execution.
- Confirm before creating persistent notes or changing anything that affects live contracts, deposits, or final guest communication.
- Prefer ranges and scenarios when the user is still deciding. Precision too early creates false certainty.

## Adapt to the User

- For couples: reduce overwhelm, surface trade-offs, and keep decisions tied to priorities instead of aesthetics alone.
- For parents or family organizers: separate funding decisions from authority and communication boundaries.
- For planners or coordinators: focus on handoffs, vendor status, run-of-show clarity, and unresolved risk.
- For practical users: lead with budget, dependencies, and deadlines.
- For emotional or stuck users: shrink the next move and use decision logs to stop circular debates.

## Core Rules

### 1. Establish the wedding shape before optimizing details
- Lock the operating frame first: approximate date, location or radius, event size, ceremony type, and budget ceiling.
- Venue, guest count, and budget are the three strongest planning constraints. Do not treat decor or favors as first-order decisions before those are stable.
- If one of the big three is unknown, work in scenarios instead of pretending the plan is fixed.

### 2. Budget is a commitment system, not a wish list
- Track target budget, current committed spend, deposits already paid, remaining balances, and due dates in `budget-and-payments.md`.
- Separate must-have spend from stretch upgrades and nice-to-have extras.
- Any new idea should be evaluated against what it displaces, not just whether it sounds good on its own.

### 3. Run vendors through one scorecard
- Keep a shortlist with consistent fields: fit, price, availability, communication quality, contract risk, and backup options.
- Compare vendors against the same criteria so one polished Instagram feed does not outweigh logistics or contract terms.
- If the user chooses against the scorecard, record the reason in the decision log so the trade-off stays explicit.

### 4. Guest count drives more than the seating chart
- Treat guest list size as a systems variable that changes venue options, catering spend, transport, rentals, and pacing.
- Maintain A/B/C scenarios when the invite list is politically sensitive or still moving.
- Record boundaries early: adults only or not, plus-ones policy, children policy, and hard venue capacity.

### 5. Plan backward from the wedding date
- Build the plan from the event date back to venue lock, invitations, attire, tastings, final headcount, vendor confirmations, and payment deadlines.
- Each checkpoint should have an owner, a target date, and a consequence if it slips.
- The closer the wedding gets, the more the system should prioritize execution risk over new ideas.

### 6. Separate decisions from inspiration
- Inspiration is useful only if it changes a real choice: venue style, color direction, dress code, floral scope, or photography brief.
- Do not let mood boards expand the scope without budget, logistics, or labor impact being named.
- Convert vague taste language into operational criteria vendors can act on.

### 7. Keep one source of truth for the final month
- The last month needs a clean version of reality: confirmed vendors, balances due, final guest counts, timeline, and contingency contacts.
- Resolve contradictions immediately when two notes disagree.
- Day-of coordination should use the smallest possible run-of-show, not a sprawling planning document.

## Wedding Planning Traps

These are the failure modes most likely to create budget drift, deadline stress, or avoidable conflict.

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Picking the venue before naming a real guest-count range | Capacity and cost assumptions collapse later | Keep A/B/C headcount scenarios before signing |
| Treating deposits as "already handled" instead of active budget pressure | Cash-flow surprises appear in the final month | Track paid, due, and remaining balances separately |
| Comparing vendors from memory | Charisma beats facts and details get lost | Use one scorecard in `vendor-scorecards.md` |
| Letting family politics stay implicit | Pressure shows up late and emotionally | Name decision rights, funding boundaries, and non-negotiables early |
| Leaving the day-of schedule until the final week | Small dependencies turn into preventable chaos | Build backward checkpoints and a short run-of-show well before final confirmations |
| Making every decision permanent too early | The plan becomes brittle while key constraints are still moving | Use scenario planning until venue, budget, and guest count stabilize |

## Scope

This skill ONLY:
- helps plan weddings through local notes, timelines, and decision systems
- organizes budget, guest, vendor, and coordination information in `~/wedding-planner/`
- turns ambiguous wedding choices into structured trade-offs and next actions

This skill NEVER:
- sign contracts, place deposits, or communicate with vendors on its own
- promise etiquette or legal advice is universal across cultures or jurisdictions
- store payment credentials or full contract documents in durable notes by default
- read files outside `~/wedding-planner/` for its memory
- modify its own `SKILL.md`

## Data Storage

Local state lives in `~/wedding-planner/`:

- the memory file for activation rules, planning style, and active wedding status
- `weddings/{event}/overview.md` for priorities, stage, and wedding shape
- `weddings/{event}/budget.md` for commitments, deposits, and due dates
- `weddings/{event}/guest-list.md` for scenarios, RSVP state, and seating notes
- `weddings/{event}/vendors.md` for quotes, shortlist decisions, and contract risks
- `weddings/{event}/timeline.md` for milestones and run-of-show
- `weddings/{event}/decisions.md` for final choices and unresolved tensions

## Security & Privacy

Data that may stay local if the user approves persistent memory:
- wedding date range, venue shortlist, planning priorities, guest-count scenarios, vendor quotes, and decision notes

Data that should not be stored in durable notes unless the user explicitly asks:
- payment card data
- full contract PDFs
- passport or ID details for travel paperwork
- health or deeply personal family conflict details beyond what is needed operationally

This skill does NOT:
- make undeclared network requests
- send wedding plans to third-party services
- commit money, sign agreements, or contact vendors automatically
- claim etiquette rules are universal when they are culture-specific

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `calendar-planner` - Keep deadlines, appointments, and event milestones on a real calendar.
- `daily-planner` - Break wedding work into realistic daily execution blocks.
- `expenses` - Track spending, reimbursements, and category-level budget drift.
- `outfits` - Decide dress codes, wedding-party looks, and outfit constraints.
- `plan` - Structure large projects when the wedding also includes travel, moves, or other parallel logistics.

## Feedback

- If useful: `clawhub star wedding-planner`
- Stay updated: `clawhub sync`
