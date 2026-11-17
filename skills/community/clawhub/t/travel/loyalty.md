# Loyalty — Programs, Points, Status, And Benefits Already Paid For

Points are a currency with no consumer protection: the issuer sets the price, changes it without notice, and can expire the balance. Treat them as a depreciating asset, not savings.

**Contents:** [The Ledger](#the-ledger) · [Expiry Beats Accumulation](#expiry-beats-accumulation) · [Valuing A Redemption](#valuing-a-redemption) · [Earning Without Distorting Decisions](#earning-without-distorting-decisions) · [Status: What It Is Actually Worth](#status-what-it-is-actually-worth) · [Alliances And Partners](#alliances-and-partners) · [Card Benefits Already Paid For](#card-benefits-already-paid-for) · [Family Pooling And Transfers](#family-pooling-and-transfers) · [Missing Credit](#missing-credit)

**Before booking anything, or before buying insurance, a lounge pass or a rental excess waiver**, read `## Loyalty` in `~/Clawic/data/travel/memory.md` — or `programs.md` if `## Boxes` points there. Half of what travellers buy at the airport is already included in a card they carry.

## The Ledger

One row per program, and the columns that matter are the expiry ones:

`program | number tail | tier | tier expires | balance | balance expires`

- The membership **number** is a working identifier and stays; the account **password or PIN** never goes in a file (`memory-template.md`, Secrets).
- Every balance expiry and every tier expiry gets a row in `## Due`, because both are silent and both are recoverable only before the date.
- Add the program number to every booking at the time of booking. Retroactive crediting is possible and it is a form and a wait.
- Past 15 programs the ledger and its `## Card Benefits` section move together to `programs.md`, headings unchanged (`memory-template.md`).

## Expiry Beats Accumulation

The two ways a balance dies:

1. **Inactivity expiry.** Many programs expire the balance after a period of no earning or spending — commonly 18 to 24 months — and a single small transaction resets the clock. Know which programs work this way and what the cheapest resetting activity is: often a shopping-portal purchase or a small points transfer.
2. **Devaluation.** An award chart repriced overnight, with no notice and no grandfathering. This is not an edge case; it is the normal life cycle of a program.

Both point the same way: **hold no more than one aspirational redemption's worth and spend the rest.** Points held for a perfect future trip are a loan to the airline at a negative interest rate.

## Valuing A Redemption

A redemption is worth taking when the value per point clears what those points would fetch on an ordinary redemption:

```
value per point = (cash price of the same ticket or room − taxes and fees paid on the award) ÷ points spent
```

Two rules that this formula makes obvious:

- **Compare against the cash price you would actually pay**, not the highest fare on the page. Redeeming 60,000 points against a business fare nobody in the household would ever buy is not value; it is a story.
- **Subtract the cash component.** Some award tickets carry surcharges large enough that the award costs most of the cash price *plus* the points.

Sweet spots exist and they are structural, not secret: long-haul premium cabins, one-way availability, and partner awards priced off a different chart. Poor value is equally structural: cheap short-haul cash fares, hotel points against a discounted rate, and anything converted into merchandise or gift cards.

## Earning Without Distorting Decisions

- **Never let earning pick the itinerary** unless the difference is small. A worse connection to preserve alliance credit is paid for in hours.
- Add the number to **every** booking, including hotels booked as part of work travel, and including partner airlines.
- **Third-party platform bookings frequently earn nothing** and do not count toward status; that is part of the direct-versus-platform comparison (`bookings.md`).
- Shopping and dining portals earn without changing behaviour, which is the only free earning that exists.
- Company-paid travel: whether the traveller keeps the points is a policy question, answered before optimising anything (`business-trips.md`).

## Status: What It Is Actually Worth

Status pays in three currencies — a free checked bag, lounge access, and priority on rebooking when things break — and the third is the one that matters and the one nobody prices. On a disrupted day, a status passenger is rebooked from the phone line while the queue is still forming (`disruption.md`).

Status is only worth chasing when the travel already exists. A mileage run to secure a tier that saves less than the run costs is a hobby, not a strategy. Soft landings, status matches with competing programs, and mid-tier benefits available through a credit card are all cheaper routes to most of the same benefits.

Tier expiry is the thing to diary: qualification periods run on the program's calendar, not yours, and the last quarter is when the decision has to be made.

## Alliances And Partners

Credit earned with one carrier usually counts in a partner's program, and the earning rate differs by program for the same flight — sometimes substantially, depending on the fare class booked. Where the traveller has a settled alliance preference, record it in `config.yaml` under `channels`, so bookings default to crediting the right program without re-litigating it.

Partner **redemptions** are frequently better value than the operating carrier's own, and they are the reason to keep a balance in a program the traveller never flies.

## Card Benefits Already Paid For

The annual fee is spent whether or not the benefits are used. Inventory them once and record them in the ledger's `## Card Benefits` section, because they are the ones bought twice:

- Travel insurance and rental-car excess cover — with the conditions: trip paid on that card, pre-existing exclusions, evacuation cap (`health.md`)
- Lounge access, and how many guests
- Free checked bags, priority boarding, seat selection
- Purchase and delay protection: reimbursement for a delayed flight or delayed baggage, which is claimed and not automatic
- No foreign transaction fee, which decides which card is the default abroad (`money.md`)
- Annual credits — a hotel credit, an airline fee credit — which expire unused on a calendar the cardholder is not watching

The annual fee itself goes in the shared `~/Clawic/data/finances/subscriptions.md` with its currency and renewal date, so it sits next to every other recurring cost and gets reviewed like one.

## Family Pooling And Transfers

Some programs pool household balances free, which turns two useless balances into one usable one; some charge to transfer, at a rate that destroys the value. Check the household's programs once and record which pool in `## Loyalty` in `memory.md` (or `programs.md` once split). Buying points is almost never worth it except to top up a specific redemption already identified and available — and then only when the arithmetic above clears.

## Missing Credit

Flights and stays fail to credit routinely: a name mismatch, a number missing at check-in, a partner booking. Claim retroactively with the boarding pass or folio, inside the program's window — commonly 6 to 12 months, and shorter for partners. This is why the boarding pass photograph from `travel-day.md` earns its keep twice.

**After any program joined, tier earned, points credited or spent, benefit discovered or fee paid**, write it in the same turn: the row in `## Loyalty` in `memory.md` (or `programs.md` once split), every expiry into `## Due`, card benefits into the ledger's `## Card Benefits` section, and the annual fee into `~/Clawic/data/finances/subscriptions.md`. Formats, split rule and shared-box protocol: `memory-template.md`.
