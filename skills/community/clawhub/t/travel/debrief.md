# Debrief — The 48-Hour Pass That Makes The Archive Worth Having

Everything else in this skill produces value only if the trip is closed properly. A trip that is never written up costs the same as one that is, and pays nothing forward.

**Contents:** [Why 48 Hours](#why-48-hours) · [The Pass](#the-pass) · [What Gets Lifted Out Of The Dossier](#what-gets-lifted-out-of-the-dossier) · [Updating The Baselines](#updating-the-baselines) · [The Loose Ends List](#the-loose-ends-list) · [Photos And Records](#photos-and-records) · [Mining The Archive Later](#mining-the-archive-later) · [Trips That Did Not Happen](#trips-that-did-not-happen)

**Before starting a debrief**, open the trip dossier `## Trips` names, and the previous debrief for the same region. The comparison between two trips is where the useful pattern is, and it is invisible from inside either one.

## Why 48 Hours

What decays first is exactly what is worth money next time: the name of the place, the hour the queue disappeared, the transfer that worked, the item never taken out of the bag. Impressions survive for years; operational detail is gone in a week. The debrief is not a diary — the diary can wait. It is the extraction of reusable facts, and it takes about twenty minutes.

## The Pass

Six items, in this order, written into the dossier's debrief section:

1. **Actual total**, against budget, with the variance named. Which line was wrong, and by how much.
2. **Per-day rate actually spent**, per person, with what it covered — this is the row that goes to `## Spend Baselines`.
3. **Three recommendations**, specific enough to act on. "Great food" is not one; "the covered market, before 11:00, cash only" is.
4. **One would-skip**, with the reason. The reason is what stops it being re-added from a guidebook in three years.
5. **Gear never used**, and anything missing. Straight into the archetype packing template (`kit.md`).
6. **What we would do differently**, in one line: pace, duration, season, base, party.

Two optional items when they apply: what the trip cost in energy rather than money (the days lost to travel, the recovery needed), and whether the reason the place was on the wishlist was actually satisfied — because if it was not, the entry goes back on the list rather than being marked done.

## What Gets Lifted Out Of The Dossier

The dossier is a trip record; the **place file is the reusable part**. At debrief, move anything still true after the trip into `artifacts/place-<name>.md`:

- Airport or station to city: which option, how long, what it cost, what it is like late at night
- Where to stay and where not to, by area and by reason
- Local transport rule that catches visitors, and the pass worth buying
- Tipping norm, cash-versus-card reality, whether contactless works
- Two or three places to return to, with the detail that makes them work
- Anything closed, seasonal, or requiring booking ahead, with how far ahead
- Scams or safety facts specific to that place (`safety.md`)

A place file is read whenever that place comes up again, whether the next trip is in eighteen months or five years, and it is the artifact that most obviously repays writing.

## Updating The Baselines

Three writes that make future estimates accurate rather than hopeful:

- `## Spend Baselines` gains or replaces the row for that region and style, with the currency and the month. A newer actual replaces an older estimate; a long-stay rate never overwrites a holiday rate for the same city (`money.md`).
- `## How They Travel` gains anything learned about the traveller themselves, not the destination: the departure time they will not accept, the pace they actually sustained, the thing they always regret paying for. This is the section that makes the next plan feel like it was written for them.
- The wishlist entry for the place is deleted, and its row appears in `## Trips` with the actual total.

## The Loose Ends List

The debrief is also where open obligations get closed or diarised, and this is the part with money in it:

| Loose end | Action |
|---|---|
| Compensation or refund still owed | Claim now; the window is months, not weeks, but a claim not started at debrief is never started (`disruption.md`) |
| Insurance claim for a medical event or a lost item | File inside the policy's window; the receipts are still in the bag |
| Work expenses | Submit inside the policy's window, which is frequently 30 days (`business-trips.md`) |
| Points not yet credited | Retroactive credit request with the boarding pass (`loyalty.md`) |
| VAT refund submitted but not received | Diary a check; postal refunds go missing routinely (`money.md`) |
| Bookings still live for the trip that ended | Cancel anything unused and update the rows to `cancelled` |
| Documents that got used up | A visa consumed, an authorization now tied to a passport near expiry (`documents.md`) |
| Kit that broke or was confiscated | Replace before it is needed, not the night before the next trip |

Anything that cannot be closed today gets a `## Due` row with a date. An open claim with no date is a claim that expires.

## Photos And Records

Back them up before doing anything else — the trip's photographs are the only irreplaceable output of the whole exercise. Then, in the same pass: delete the obvious duplicates while it is still obvious which one was the good one, and note in the dossier where the album lives. This skill stores the pointer to the album, never the media.

Names of people met who matter afterwards go to the shared `~/Clawic/data/contacts/contacts.md` with the context of how they were met; the dossier references them by name only (`companions.md`).

## Mining The Archive Later

The archive earns its keep when a future session answers a question without research:

- "Where should we go in October?" → wishlist entries with an October window, filtered by what the baselines say is affordable (`wishlist.md`)
- "What do we usually spend?" → `## Spend Baselines`, by region and style, with dates
- "Have we been to Lisbon?" → `## Trips`, then the place file, not a generic list of sights
- "What did we say about that hotel?" → the dossier, which is why the recommendation was written specifically
- "Can we do Schengen in March?" → `## Presence`, counted backwards (`documents.md`)

If a question like these cannot be answered from the archive, that is the gap the next debrief closes.

## Trips That Did Not Happen

A cancelled trip is debriefed too, briefly and immediately: why it was cancelled, what it cost, what was recovered and what was not, and whether the destination goes back on the wishlist with an updated blocker. The dossier is kept with status `cancelled` — the entry research is still valid, and the next attempt starts from it instead of from nothing.

**Run the debrief within 48 hours of getting home and write everything in that turn**: the debrief section of `trips/<yyyy>-<place>.md`; the rate into `## Spend Baselines`; the trip row into `## Trips`; the traveller facts into `## How They Travel`; the reusable place knowledge into `artifacts/place-<name>.md` with its `## Boxes` line; the packing edits into `artifacts/packing-<archetype>.md`; the open claims into `## Due`; and the wishlist entry deleted. Destinations, formats and thresholds: `memory-template.md`.
