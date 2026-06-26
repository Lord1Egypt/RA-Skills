---
name: Store
slug: store
version: 1.0.0
homepage: https://clawic.com/skills/store
description: Manage a physical store of any kind with opening routines, inventory control, staffing, cash discipline, merchandising, and weekly reviews.
changelog: Initial release with daily store operations, stock control, staffing routines, and weekly performance review workflows.
metadata: {"clawdbot":{"emoji":"🏬","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/store/"]}}
---

## When to Use

User runs a physical store, retail shop, showroom, kiosk, or multi-shift location and needs operational control instead of generic business advice.
Agent helps with daily store rhythm, inventory accuracy, staffing decisions, promotions, shrink control, and weekly KPI reviews.
It fits boutiques, convenience stores, specialty retail, home-goods shops, electronics stores, and other brick-and-mortar formats where floor execution matters.

## Architecture

Memory lives in `~/store/`. If `~/store/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/store/
├── memory.md          # Status, store profile, active priorities
├── routines.md        # Opening, peak-hour, and closing standards
├── inventory.md       # Stock priorities, adjustments, replenishment notes
├── staff.md           # Roles, shift habits, coaching notes
├── kpis.md            # Sales, traffic, conversion, ticket, margin
├── promotions.md      # Offer goals, timing, execution notes
└── incidents.md       # Loss, customer issues, equipment, safety events
```

## Quick Reference

Load only the smallest playbook that matches the current store problem so the operating advice stays fast and specific.

| Topic | File | Use it for |
|-------|------|------------|
| Setup and activation flow | `setup.md` | Decide how proactively the store support should jump in |
| Memory structure and starter files | `memory-template.md` | Create local store notes without storing sensitive data |
| Opening and closing routines | `opening-closing.md` | Open strong, close clean, and avoid shift-to-shift drift |
| Inventory control rules | `inventory-control.md` | Cycle counts, replenishment priorities, and stock-out diagnosis |
| Floor management during the day | `floor-ops.md` | Peak-hour priorities, queue control, and recovery timing |
| Merchandising and promo execution | `merchandising.md` | Displays, signage, promo ownership, and sell-through checks |
| Scheduling and coaching | `staffing.md` | Shift coverage, coaching focus, and labor-pressure decisions |
| Cash, shrink, and incident handling | `cash-and-loss.md` | Till variance, loss signals, incidents, and escalation discipline |
| Weekly metrics and review rhythm | `metrics.md` | KPI review, action ownership, and next-week operating focus |

## Data Storage

Local store notes live in `~/store/`.
Before the first write in a session, explain the planned files in plain language and ask for confirmation.

## Core Rules

### 1. Protect Cash, Margin, and Stock First
- Treat cash handling, stock accuracy, and shrink prevention as the store's operating truth.
- A store can look busy while quietly losing money through poor controls.

### 2. Run the Store by Rhythm, Not by Random Requests
- Separate the day into opening, trade hours, replenishment windows, and closing.
- Use the right task at the right moment so service and standards do not collide.

### 3. Make Decisions from Store-Level Numbers
- Track sales, traffic, conversion, average ticket, gross margin, stock-outs, and labor hours.
- Do not recommend staffing, purchasing, or promotions without naming the metric behind the move.

### 4. Keep Inventory Accurate Enough to Trust
- Recount fast-moving, high-value, and high-shrink items more often than the rest.
- Inventory records that drift even slightly ruin replenishment, promotions, and profit analysis.

### 5. Staff to Traffic and Mission
- Schedule around real demand peaks, delivery windows, and known task loads.
- Equal hours for everyone is not fairness if service fails during busy periods.

### 6. Promotions Must Have a Clear Job
- Every promotion needs a goal: drive traffic, clear stock, raise basket size, or defend margin.
- If the offer has no owner, expiry, and success metric, treat it as noise.

### 7. Log Repeated Friction and Close the Loop
- Capture incidents, customer complaints, equipment issues, and recurring floor bottlenecks.
- A store improves when the same problem stops happening, not when it gets handled faster each time.

## Common Traps

- Chasing total sales only -> margin, conversion, or labor productivity quietly deteriorate.
- Replenishing from memory -> empty pegs, overstock, and stock-outs compound together.
- Running promos without floor execution -> offer exists on paper but customers never see it.
- Scheduling by fixed habit -> busy hours get understaffed while quiet hours absorb payroll.
- Counting everything at month end only -> shrink and receiving errors become impossible to trace.
- Treating complaints as one-offs -> recurring service failures stay invisible.

## External Endpoints

This skill makes NO external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Nothing by default. This is an instruction-only, local-first operations workflow.

**Data stored locally:**
- Store profile, routines, KPI snapshots, staffing patterns, stock notes, promotions, and incident logs.
- Stored in `~/store/`.

**This skill does NOT:**
- request or store raw card numbers, PINs, or payment credentials.
- collect unnecessary employee personal data or private customer identifiers.
- make undeclared network calls.
- modify its own core files.

## Trust

This is an instruction-only retail operations skill.
No third-party service access is required.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `business` - strategic framing for store growth, priorities, and expansion decisions.
- `payments` - payment flow, checkout reliability, and processor-side issue handling.
- `accounting` - bookkeeping and financial statement logic behind store performance questions.
- `customer-support` - communication habits for returns, complaints, and service recovery.
- `management` - broader team leadership patterns beyond day-to-day floor control.

## Feedback

- If useful: `clawhub star store`
- Stay updated: `clawhub sync`
