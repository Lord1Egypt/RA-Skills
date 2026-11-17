# Incremental replanning

Read this before changing anything about an existing plan, and always before changing its dates.

## Why dates are the dangerous delta

Almost nothing a trip plan researches is keyed to a *date*. It is keyed to a **weekday**. Opening
hours, closure days, market days, Sunday retail law, a museum that shuts Mondays, a restaurant's
Ruhetag, a rail timetable that thins at weekends — every one of those is a fact about Tuesdays, not
about the 22nd. Move the window by a single day and all of it silently becomes a guess, while the
plan still renders, still passes every structure gate, and still reads as complete.

That is not hypothetical. [research-budget.md](research-budget.md) records a run where the dates
moved by one day, the weekday map was redone by hand, and **that manual redo introduced an
off-by-one in every ticket day index and every anchor day index**. The plan looked finished. The
lesson was written down and no tool was shipped for it, which is why this reference and
`scripts/replan_trip.py` exist.

A worked example, from the plan that prompted this. Shifting a Cologne trip from Fri 18 – Mon 21
September by **+1 day** does this:

| Day | Was | Becomes | What breaks |
| --- | --- | --- | --- |
| 2 | Saturday | Sunday | The only market day of the trip. NRW law closes retail on Sunday, and this day's whole purpose was buying allergy-safe food. |
| 3 | Sunday | Monday | Museum Ludwig closes Mondays. |
| 4 | Monday | Tuesday | The Römisch-Germanisches Museum runs Wed–Mon and closes **Tuesdays** — it was chosen precisely because it is the one major museum open on a Monday. |

Three of four days lose their anchor, and a hand edit would have caught none of it.

## Run the script; do not edit dates by hand

```bash
python scripts/replan_trip.py <plan.json> --shift-days 1 --out <new.json>
python scripts/replan_trip.py <plan.json> --start 2026-10-02 --end 2026-10-05 --out <new.json>
python scripts/replan_trip.py <plan.json> --travellers 3 --out <new.json>
python scripts/replan_trip.py <plan.json> --cap 950 --out <new.json>
```

It rewrites **only what a date shift determines**, and reports every one:

- `trip.start_date` / `trip.end_date`, every `days[].date`, and day numbering re-derived from
  position rather than re-typed — the re-typing is the off-by-one above;
- accommodation `check_in` / `check_out`. Note the checkout: it is the morning **after** the last
  night, so it is the one traveller date that legitimately sits a day outside the trip window. A
  naive "shift dates inside the window" rule skips exactly that field and quietly turns a
  three-night booking into a two-night one;
- ISO dates prefilled into booking and search URLs, including the `checkout=` parameter, for the
  same reason — a hotel button carrying last week's dates opens a search for nights the traveller
  is not there, and the defect surfaces at the payment screen;
- `attraction_tickets[].day_number` and `destination_experience_anchors[].planned_day`, re-derived
  from the dates.

It refuses, with a message and no traceback, when: the plan is not valid JSON; the shift would put
the trip in the past relative to `--today`; or a `--start`/`--end` pair has a different length than
the existing day count — that is a re-plan, not a shift, so add or remove day cards deliberately.

## What it will not do, on purpose

**It never rewrites prose.** A sentence like "Saturday is the only full shopping day of the trip"
becomes false when the dates move, and swapping the weekday token inside it would convert a stale
sentence into a *confident* one. That is strictly worse: a reader can catch a contradiction, but not
a fluent lie. Every such sentence is flagged instead.

The flagging is better than it sounds, because the plan usually refutes itself. The script scans the
plan's own text for weekday-closure claims and checks them against each day's **new** weekday. On the
+1 shift above it raised 12 of these unaided — including the plan's own sentence explaining that the
Römisch-Germanisches Museum closes on Tuesdays, on the day that had just become a Tuesday. No
research was needed to find them; the plan had already written down why the new schedule fails.

**It clears the verification.** `verification_status` goes to null and `verification_report` is
dropped, because a plan whose dates moved was never verified on those dates. A shifted plan carrying
its old verification is the single most dangerous artifact this tool could produce — it would look
checked while every weekday-keyed claim in it had gone stale.

<a id="the-gate-that-stops-it-shipping"></a>
## The gate that stops it shipping

Everything the script cannot safely recompute lands in `replan_context.must_reverify`, one entry per
invalidated fact, each with a `path` and a `reason`. `check_plan_consistency.py` fails the plan while
any entry has `resolved` other than `true`. So a replanned trip cannot be delivered until a human has
gone through each one, recorded what they found in `resolution`, and set `resolved: true`.

Entries are raised for, at minimum: every dining card whose `venue_hours` carries a weekday prefix
that no longer matches; every dining card whose `hours_status` claims `researched` or `verified`
(the claim itself is weekday-keyed); every activity carrying a `ticket_note` or an opening-time
claim; any prose naming a weekday that moved; and the plan's verification as a whole.

Two fields are deliberately **not** on that list, and the reason is worth keeping so nobody adds
them back as noise. A dining card's `rating_*` and the plan's `trip.destination_coords` are not
weekday-keyed: a restaurant's score does not change because the trip moved a day, and a city does
not move at all. What *was* weekday-keyed on that card — its opening hours, and the `hours_status`
claim about them — is already raised above. A rating goes stale with *time*, not with a shift, so
re-read it when `rating_checked_at` is old rather than because the dates slid; raising it on every
shift would train people to tick a box that was never wrong.

Resolving an entry means re-checking the fact against the **new** weekday at its original source —
not ticking the box. Where the reason begins `CLOSED ON THE NEW DAY`, do not even re-check: the plan
already carries its own refutation, so move the item to another day, take the fallback the plan
names, or drop it.

## Deltas other than dates

Restate the delta first, then trace dependencies rather than rebuilding. Most of these the script
does not touch at all — they need judgement, and the point of naming them is to stop a change
propagating further than anyone noticed:

| Change | Recompute |
| --- | --- |
| Budget or dates | Fares, number of nights, accommodation tier, paid activities, the order of the days |
| Mobility or health | Walking legs, transfers, elevation, where the accommodation sits, daily pacing |
| Weather or season | Outdoor activities, clothing, indoor alternatives, daylight-dependent timing |
| Entry or passport | Destination eligibility, transit countries, and whether `entry_context` still holds |
| Traveller count | Rooms, transport capacity, activity suitability, and every per-person budget row |

`--travellers` and `--cap` change the stated number and nothing downstream: a party that grew from
two to three does not automatically need a second room in the data, but it does in reality. Treat
those two flags as recording the decision, then work the table above by hand.

<a id="party-changes"></a>
## When the party changes

A hotel card is booked for the whole party: every `booking_options.accommodations[].guest_count`
equals `trip.traveler_count`, and `check_plan_consistency.py` refuses a card that does not. Its
`room_count`, `room_basis`, nightly cost and search link follow the same number. The rule exists
because the natural edit — typing the new number into `trip.traveler_count` — moves nothing else:
walked on 2026-09-24, a party that grew from four to five kept four hotel cards for four guests,
each linking to a search for 2 adults + 2 children, and the page shipped verified.

On a plan delivered verified, the party and `trip.traveler_constraints` also count as part of every
section that depends on them — each day, each booking option, the budget and the transport overview
(the constraints: days, booking options and the transport overview). Changing either asks for a
recheck of each of those sections, not of `trip` alone: a table, a family ticket and a car are all
bought for a number of people, and a new allergy re-opens every meal. To start over instead,
`python scripts/replan_trip.py <plan.json> --travellers N --out <new.json>` records the new party,
flags what moves with it, and clears the verification. Saved over its delivered copy with
`--overwrite` alone, a replanned plan is compared against that copy's report, so every moved part
owes a recheck; after a date shift that is nearly every part, and a fresh full verification is
usually the shorter route.

Keep what is still valid. A replan that rebuilds everything is not a replan, and it throws away
research that was correct — the script prints a `RETAINED` block naming what it deliberately left
alone so that a reviewer can see the claim and challenge it.

<a id="bookings"></a>
## When the traveller chooses or books something

Record it with `python scripts/record_booking.py <plan.json> --option <id> --chosen` (decided, not
paid) or `--booked --on <YYYY-MM-DD> --via "<where>" [--paid <amount> <CUR>]`; `--clear <id>` undoes
it. Never edit the cards to say so. One decision per group: flights and rail by `leg_group_id`,
hotels by `stay_group_id`, rental cars as one group, each ticket alone; recording another option
in a group replaces the first. A record holds the date, where, and what was paid -- never a
booking reference, a document or a payment detail.

The `bookings` block sits outside verification's fingerprints: a decision is the traveller's fact,
not research, so a verified plan stays verified. The one exception is a hotel other than the one
the days were planned around: the script re-points those days to it, and because the days really
changed, the save asks for their recheck like any edit. Re-pointing moves only the ids. The check-in
line, the route stops, the directions and the next morning's check-out still name the old hotel, so
the script prints an `EDIT:` line for each day that does. `check_bookings` refuses the plan until
none of them names a hotel of that stay that the traveller did not take. Edit them to the
recorded hotel before saving.

A purchase does not move with a replan. When `replan_trip.py` shifts the dates or changes the
party, every `booked` record becomes a `must_reverify` entry, because the ticket or room was bought
for the old dates and the old party. Change or rebook it with the provider, then record the result
again, or `--clear` it. A `chosen` record is a decision, not a purchase, and survives the replan.
