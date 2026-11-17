# Business Trips — Policy, Per Diem, Expenses, Bleisure

A work trip is optimised for a different thing than a holiday: arriving functional, being reimbursed without friction, and not creating a problem for the employer. The traveller is not the payer, which changes every default in this skill.

**Contents:** [Policy First](#policy-first) · [Booking Under A Policy](#booking-under-a-policy) · [Per Diem Versus Actuals](#per-diem-versus-actuals) · [Receipts In The Shape Finance Accepts](#receipts-in-the-shape-finance-accepts) · [Arriving Functional](#arriving-functional) · [Adding Personal Days](#adding-personal-days) · [Cross-Border Work Exposure](#cross-border-work-exposure) · [Points Earned On Company Money](#points-earned-on-company-money) · [Conferences And Client Visits](#conferences-and-client-visits)

**Before booking or expensing anything for work**, read `## Trips` for the last trip of this kind and the policy notes recorded on it. Reimbursement rules do not change often, and re-deriving them each quarter is the waste this archive removes.

## Policy First

Six questions, answered once and recorded, that determine everything else:

| Question | Why it decides |
|---|---|
| Booking channel | Many employers only reimburse through a corporate tool or agency; a cheaper direct booking is simply not reimbursed |
| Cabin and fare rules | Class by flight duration, refundable versus cheapest, advance-booking requirement |
| Lodging cap | Per night, by city, and whether it is inclusive of tax |
| Per diem or actuals | Two entirely different expense processes (below) |
| Ground transport | Ride apps, taxis, mileage rate for a personal car, whether a hire car needs approval |
| What is never reimbursed | Alcohol, in-flight Wi-Fi, seat selection, laundry under a stated trip length, personal days |

Record the answers in `artifacts/policy-work-travel.md` with the date and the employer, and read it before the next trip. A policy is stable and rediscovering it is unpaid work.

## Booking Under A Policy

- Book inside the channel the policy names, even where it is more expensive: the reimbursement is the product, not the price.
- Refundable is usually correct for work travel, because the meeting moves and the traveller does not control the calendar (SKILL.md Rule 4).
- Keep the itinerary and the approval in the same place; approval-before-booking is a common requirement and an approval reconstructed afterwards is not one.
- Where the traveller pays first and claims later, note the cash-flow gap: a long-haul fare on a personal card, reimbursed in six weeks, is a real cost worth raising rather than absorbing.
- Everything still gets its row in `~/Clawic/data/bookings/<year>.md`, marked with the trip, because a work booking has the same deadlines as any other (`bookings.md`).

## Per Diem Versus Actuals

- **Per diem** pays a fixed daily amount regardless of spend. Receipts are usually not required for the covered categories, which makes the process trivial and makes the daily rate the traveller's to manage. Partial days at each end are usually paid at a reduced fraction, and a provided meal — a conference lunch, a hotel breakfast — usually reduces the rate for that day. That deduction rule is the part people get wrong.
- **Actuals** reimburse what was spent, with a receipt for everything above a threshold, inside category caps. Slower, and it requires the discipline in the next section.

Never mix them within a trip unless the policy explicitly allows it, and never claim a per diem for a day whose meals were paid on the company card.

## Receipts In The Shape Finance Accepts

The reason expense claims bounce is almost never the amount:

- **Photograph each receipt the day it happens**, not at the end of the trip. Thermal receipts fade, and the ones that matter are the ones in a pocket in another currency.
- **The itemised bill, not the card slip.** Finance frequently needs the tax breakdown, which the card slip does not have.
- **Currency and rate**: claim in the currency the policy requires, and use the rate the policy names — the card statement rate, a published daily rate, or the amount actually charged. Picking your own rate is a query every time.
- **Business purpose, attendees, and the reason** for anything involving hospitality. A dinner with no named attendees is the most commonly rejected line in expenses.
- **Split personal from business at the point of payment**, not at the point of claiming. Ask for separate bills.
- File within the policy's window, which is frequently 30 days and is enforced.

## Arriving Functional

The optimisation is performance on the day of the meeting, not the price of the ticket:

- Arrive the evening before for anything that starts in the morning. A same-morning arrival with a delay is a missed meeting, and the saved night costs more than it saves (`travel-day.md`).
- Eastward flights are the harder direction: for a short trip crossing few zones, staying on home time deliberately beats a partial adjustment (`health.md`).
- Book the accommodation for proximity to the meeting, not to the nightlife. The commute at 08:00 in an unfamiliar city is the variable that goes wrong.
- Redeye flights straight into a working day are a false economy for anything requiring judgement, and the policy usually permits the alternative if asked.
- Confirm the meeting address, the building entry process and the contact's phone number before departure; a locked lobby with no answer is a real failure mode.

## Adding Personal Days

Extending a work trip is usually allowed and usually governed by a rule:

- The employer typically pays the fare it **would have paid** for the work-only itinerary; the traveller pays any difference, and the comparison quote must be captured at booking time — reconstructing it later is impossible.
- Lodging, meals and transport on personal days are personal, and the split is recorded per day, not averaged.
- Insurance may differ: corporate travel cover often stops when the business purpose ends, leaving personal days uninsured. Check, and buy cover for the gap.
- Personal days do not stop counting for immigration or tax day counts (`long-stays.md`).

Keep the whole trip in one dossier with a clear line down the middle: work days and personal days, with their own money rows.

## Cross-Border Work Exposure

Attending meetings, signing, or performing work in another country can trigger obligations regardless of the length of stay: business-visa requirements distinct from tourist entry, withholding or payroll consequences, and permanent-establishment risk for the employer. Frequent short trips to the same country accumulate into thresholds nobody is tracking. Record the days in `## Presence` with `Purpose: work`, state what they add up to, and route the conclusion to the employer's tax or mobility function — not to a guess (`documents.md`).

## Points Earned On Company Money

Whether the traveller keeps the miles and hotel points from company-paid travel is a **policy question with three common answers**: keep them, surrender them, or use them for company travel only. Establish which before optimising anything, because the whole strategy in `loyalty.md` depends on it. Where they are kept, the loyalty number goes into every booking made through the corporate channel too, which is the step most often skipped.

## Conferences And Client Visits

Conferences: register before the early rate expires and note the deadline in `## Due`; the room block usually beats public rates and sells out first; the sessions worth attending are decided in advance, because the schedule is designed to fill the day.

Client visits: the client is a person and belongs in the shared `~/Clawic/data/contacts/contacts.md` — identity is email or handle, columns `name | role | preferred channel | context` — referenced from the trip dossier by name only, never duplicated. The work itself — objectives, outcomes, decisions — is not this skill's to record; only the travel around it is.

**After any work trip**, write in the same turn: the policy answers into `artifacts/policy-work-travel.md`; the work/personal day split and the reimbursed total into the trip dossier; the crossing with `Purpose: work` into `## Presence`; people met into `~/Clawic/data/contacts/contacts.md`; the claim deadline into `## Due` while it is open. Destinations, formats and shared-box protocol: `memory-template.md`.
