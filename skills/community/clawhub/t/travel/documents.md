# Documents — Passports, Visas, Authorizations, Day Counts

Categories here are stable; specific systems, fees, processing times and launch dates change every year. **Verify each requirement on the destination government's own immigration site** — not a travel blog, not an aggregator, not this file — before it gates a booking, and write down the date you checked.

**Contents:** [Passport Validity](#passport-validity) · [Which Permission Applies](#which-permission-applies) · [Counting A Rolling Allowance](#counting-a-rolling-allowance) · [Applying: The Slot Is The Constraint](#applying-the-slot-is-the-constraint) · [Airline Checks Before Border Checks](#airline-checks-before-border-checks) · [Renewals And The Expiry Ladder](#renewals-and-the-expiry-ladder) · [Copies And Custody](#copies-and-custody) · [Other Documents Worth A Row](#other-documents-worth-a-row)

**Before answering any entry question**, read `## Documents` and `## Presence` in `~/Clawic/data/travel/memory.md` — or the files `## Boxes` points to (`travel-documents.md`, `presence/`) — and `passport_countries` in `config.yaml`. Entry rules are a function of nationality: answering without knowing the passport is guessing.

## Passport Validity

Three independent tests, and a passport can pass two and fail the third:

| Test | Rule | Consequence |
|---|---|---|
| Remaining validity | Many countries require **≥6 months beyond the date of entry**; some require 3; a few only require validity through the stay | Denied at check-in by the airline, which is liable for carrying you |
| Issue date | Schengen requires the passport to have been **issued within the previous 10 years** on the day of entry, and to be valid **≥3 months beyond intended departure** | An early-renewed passport with an extended validity beyond 10 years is refused despite showing plenty of time left |
| Physical state | Blank pages — commonly 2 facing pages — plus no water damage, no detached lamination | Refused with years of validity remaining; damage is judged by the officer, not by you |

**Safe-travel date = expiry − 6 months.** Compute it once, write it in the `## Documents` row, and diary renewal at **expiry − 9 months** in `## Due`, because renewal itself takes weeks and the passport is unavailable while it happens.

A visa or authorization is usually bound to the passport book it was issued in. Renewing the passport can strip a valid multi-year visa: either carry both books where the destination allows it, or have the visa transferred before renewing.

## Which Permission Applies

Four levels, and they are not interchangeable:

1. **Visa-free** — nothing to obtain, but a duration limit and often an onward-ticket and funds requirement still apply.
2. **Electronic travel authorization** — an online pre-approval that is not a visa: the US, Canada, the UK, Australia, New Zealand and the EU each run their own, under their own name, with their own validity. Approval is usually quick and sometimes instant, but a referral for manual review takes days and the traveller finds out at the check-in desk. Apply days ahead, never hours, and never through a third-party site charging a service fee on top.
3. **Visa on arrival** — real, but it is a queue, a fee often payable only in cash or only by card, and a set of documents (photos, address, onward ticket) that must be in hand before joining it.
4. **Visa in advance** — an application, usually with biometrics in person, sometimes with the passport surrendered for weeks.

**Transit is a separate question.** Airside transit is not universally visa-free: several countries require a transit visa even without leaving the terminal, and a connection that changes terminals or requires collecting a bag is an entry. Check transit rules for the passport, not just the destination.

## Counting A Rolling Allowance

The Schengen rule — 90 days in any 180 — is the common one, and it is counted the way nobody expects:

- The window is **rolling and backwards-looking**: on any given day, look at the previous 180 days and count the days of presence inside them. It does not reset in January.
- **Day of entry and day of exit each count as a full day.** Four nights is five days.
- It is a **single shared allowance** across every member state, not per country.
- It follows **the person**, not the trip, and it includes days on someone else's trip, a work trip, and a layover where you cleared immigration.

**Worked example.** Intended entry 10 March. Sum the presence days between 12 September and 10 March: 62 used, 28 remain. A 30-day trip is refused at the border, an overstay of two days can produce a multi-year ban, and no airline or booking site checks this for you.

Hold the count in `## Presence` (`memory-template.md`) and re-sum it before booking any entry, because a trip booked in January is entered in March against a different window.

Long stays turn this into a legal question rather than an administrative one — tax residence, work rights, and health cover all key off day counts with thresholds that are not the same number (`long-stays.md`).

## Applying: The Slot Is The Constraint

For anything requiring an appointment, the processing time published by the consulate is not the lead time. The lead time is **slot wait + document gathering + processing + courier**, and the slot wait dominates and is invisible until you look.

Order of operations, once the trip is plausible and before anything non-refundable is bought (SKILL.md Rule 4):

1. Confirm the permission required for this nationality, today, on the official site. Open `artifacts/visa-<country>.md` with the URL and the date checked, and its `## Boxes` line.
2. Look at appointment availability first; that date sets everything else.
3. Assemble the documents the checklist actually names — proof of funds, itinerary, insurance meeting a stated minimum, a letter of invitation — in the format demanded. Rejections are overwhelmingly formatting, not substance.
4. Book refundable travel only if a booking is required for the application, and set its row in `~/Clawic/data/bookings/<year>.md` to `status: held for visa application` — a booking held for a consulate is cancelled the day the decision lands.
5. Finish `artifacts/visa-<country>.md` with the procedure that worked: what was asked, what was refused, how long each stage took, which office. The next application, for that country or for a family member, is a different experience with that file in hand.

## Airline Checks Before Border Checks

Most entry failures happen at a check-in desk on the departure side, hours before any officer sees the passport, because carriers are fined for bringing an inadmissible passenger:

- Passport validity against the destination's rule
- The authorization existing and matching the passport number in the booking
- An onward or return ticket where the destination requires proof of exit
- Occasionally proof of funds or an address

The practical consequence: an argument about whether the rule is really enforced is an argument you have at the airport, having already lost the flight.

## Renewals And The Expiry Ladder

Every one of these gets a `## Due` row with the warning lead time, not the expiry date:

| Document | Typical validity | Warn at |
|---|---|---|
| Passport | 5-10 years | expiry − 9 months |
| Electronic authorization | 1-5 years, and dies with the passport | expiry − 2 months, or the day the passport is renewed |
| Travel insurance, annual multi-trip | 1 year | renewal − 1 month |
| Driving licence and International Driving Permit | licence years; IDP typically 1 year | before each trip that involves driving (`transport.md`) |
| Trusted-traveller programs | commonly 5 years | expiry − 6 months; renewal queues are long |
| Vaccination certificates | varies; yellow fever is lifetime under the 2016 WHO rule | per `health.md` |
| Residence or long-stay permit | varies | expiry − 3 months, and before booking any exit |

## Copies And Custody

- Carry a **physical** photocopy of the passport page separate from the passport, plus the insurance policy number and the 24-hour line. It works with a dead phone, which is the scenario it exists for.
- Digital copies belong in the user's own password manager, never in a notes app, a chat thread, an email to themselves, or anywhere under `~/Clawic/data/`. This skill stores the pointer and the last four (`memory-template.md`, Secrets).
- Leave the itinerary and the emergency card with one person at home who is not travelling.
- When a passport is stolen, the police report comes before the embassy: both the consulate and the insurer require it (`disruption.md`).

## Other Documents Worth A Row

Each of these has stopped a trip that was otherwise fine: an International Driving Permit that must be issued in the country of licence **before departure** and cannot be obtained abroad; proof of onward travel; a vaccination certificate keyed to countries transited rather than the origin; a notarised consent letter when one parent travels with a child (`companions.md`); a pet's paperwork, whose lead time is months and not days; a student or press card that unlocks pricing; and an insurance policy whose minimum cover is itself an entry requirement in some countries.

**After any document is issued, renewed, refused, found to be expiring, or after any border crossing that counts**, write it in the same turn: the row in `## Documents`, the crossing in `## Presence`, the warning date in `## Due`, and any procedure worth repeating in `artifacts/visa-<country>.md` with its `## Boxes` line. Destinations, thresholds and the split rule: `memory-template.md`.
