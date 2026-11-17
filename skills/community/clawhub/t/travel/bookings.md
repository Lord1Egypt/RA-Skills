# Bookings — The Record, The Deadlines, The Changes

This is the record-keeping and terms side of a reservation. Searching and comparing prices is a different job: `flight` for fares, `booking` for accommodation, `car-rental` for vehicles.

**Contents:** [What Gets Recorded, And When](#what-gets-recorded-and-when) · [Deadlines Are The Money](#deadlines-are-the-money) · [Reading The Terms Before Paying](#reading-the-terms-before-paying) · [Changing And Cancelling](#changing-and-cancelling) · [Direct Versus Platform](#direct-versus-platform) · [Names, Documents, And Rejected Check-ins](#names-documents-and-rejected-check-ins) · [Before Departure: The Reconfirm Pass](#before-departure-the-reconfirm-pass)

**Before answering anything about a date, a reservation, or "what have I got booked"**, read `~/Clawic/data/bookings/<year>.md` and the trip dossier that `## Trips` names. The inbox is not the record: search fails exactly when there is no signal and someone is waiting at a counter.

## What Gets Recorded, And When

The moment a reservation exists, changes, or is cancelled — not at the end of the session, not before departure. One row in the shared box, identified by its **locator**:

`date | type | provider | locator | travellers | status | free change/cancel until | amount with currency | trip`

Full protocol, including what to do when the file already exists with other columns, is in `memory-template.md`. Four things that make the row worth having:

- **The locator, exactly as issued.** It is the only field that survives a provider changing its website.
- **The deadline in the property's local time**, with the zone spelled out. This is the field people leave blank and the one that costs money.
- **The amount with its currency**, so a trip total can be assembled from the rows without opening emails.
- **The trip it belongs to**, so a cancelled trip is unwound in one pass.

Everything else — seat numbers, room type, the address, the check-in window — goes in the trip dossier, not in the shared box that other skills also write to.

## Deadlines Are The Money

Every deadline in a booking gets a row in `## Due` in `memory.md`, checked at the start of every session (SKILL.md Rule 6). The ones that matter:

| Deadline | What happens at it |
|---|---|
| Free cancellation ends | The booking becomes a sunk cost, usually at 23:59 **local to the property**, one to three days before arrival |
| 24-hour cancellation window | Many carriers allow a free cancel within 24 hours of purchase; it is the only unconditional escape and it expires quietly |
| Online check-in opens | Where seats or rooms are assigned, and where paying at the airport instead costs the most |
| Balance due | Tours, villas and cruises typically take a deposit and the rest 30-90 days out; missing it forfeits the deposit |
| Name-change window | Some tickets allow a correction free within a short period after issue and never again |
| Claim window | Compensation and insurance claims have limits measured in months to years by regime (`disruption.md`) |
| Points-booking cancel | Award tickets often refund the points for a fee, on a different clock from cash tickets |

A deadline row is deleted once it has passed or been used, so `## Due` stays a list of live obligations rather than a history.

## Reading The Terms Before Paying

Six questions, answered before the payment. The cancellation terms and the amount go in the row in `~/Clawic/data/bookings/<year>.md`; the rest goes in `trips/<yyyy>-<place>.md`:

1. **Refundable until when, and to what** — cash, credit with the provider, or points? A voucher is not a refund.
2. **Changeable, at what cost** — a change fee plus fare difference is the usual shape, and the fare difference is the part that hurts.
3. **What is included** — bags, seats, meals, taxes, cleaning, resort fee, tourist tax collected at the property.
4. **Who is the counterparty** — the airline, the hotel, or a third-party agency? It determines who you argue with when it goes wrong.
5. **What identity documents the booking is tied to** — passport number, name spelling, age of any child.
6. **What happens if the *provider* cancels** — the statutory floor, not the marketing promise (`disruption.md`).

Refundable rates are worth paying for exactly while the trip is conditional: visa pending, dates unagreed, someone else's calendar involved. Once every condition has cleared, the premium is pure cost (SKILL.md Rule 4).

## Changing And Cancelling

- **Cancel in writing, and keep the confirmation.** A phone cancellation with no reference number is not a cancellation, and it is the version the provider does not have.
- **Cancel the dependents in the right order**: the refundable things first, then anything whose refund depends on the trip being cancelled, then the insurance claim for the non-refundable remainder.
- **Do not cancel a flight the airline has already changed significantly** — a schedule change past a stated threshold often creates a right to a full refund that voluntarily cancelling destroys (`disruption.md`).
- **Rebooking a cheaper rate** is a real move where free cancellation exists: book the new one first, cancel the old one second, never the reverse.
- Update the row's `status` and refund amount in the same turn, and delete its `## Due` deadline.

## Direct Versus Platform

| | Booking direct | Booking through a platform |
|---|---|---|
| When it goes wrong | You deal with the operator | The operator points at the agency, the agency points at the operator; you have no contract with the operator at all |
| Changes | Handled at the desk or the counter | Frequently must go through the agency, which is closed at 3 a.m. |
| Loyalty | Stays and flights usually credit; rates often match | Third-party bookings commonly earn nothing and do not count toward status |
| Price | Frequently matched, sometimes with a member rate | The comparison view, which is the actual value |

Practical resolution: compare on the platform, book direct when the price is within a few percent, and never book through a platform for anything with a high probability of change — a connecting itinerary, a trip with a pending visa, a group. Where the platform is genuinely cheaper, record which it was in the row, because it determines who to call.

## Names, Documents, And Rejected Check-ins

- The name on the ticket must match the travel document **as printed**, including middle names on some routes and the order of surnames. A mismatch is a name change, priced as one, and occasionally not permitted at all.
- Authorizations and visas are tied to the passport number in the booking; renewing the passport after booking means updating the booking (`documents.md`).
- Children's tickets are priced by age **on the date of travel**, not on the date of booking, and infants become children mid-trip on long itineraries (`companions.md`).
- Fare rules for a "married segment" itinerary mean skipping the first leg cancels the rest. Missing an outbound cancels the return on most tickets.

## Before Departure: The Reconfirm Pass

Done once, a few days out, in one sitting:

- Every row for this trip still says confirmed at the provider's own site — schedule changes are notified by an email people miss
- Online check-in is done where it is open, and boarding passes are saved offline
- Documents match every booking's name and number
- The emergency card exists and the insurance policy is live (`artifacts/emergency-card.md`)
- Deadlines still in `## Due` are the ones that fall during the trip
- The itinerary and the locators are with one person at home who is not travelling

**Every reservation made, changed or cancelled** gets its row written or updated in `~/Clawic/data/bookings/<year>.md` in the same turn, with its free-change deadline as a `## Due` row in `memory.md` and any trip-specific detail in `trips/<yyyy>-<place>.md`. Shared-box protocol, identity key and scale cut: `memory-template.md`.
