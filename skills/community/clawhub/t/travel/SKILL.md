---
name: Travel
slug: travel
version: 1.0.2
description: 'Runs a traveler''s standing system: dream list, passports and visas, Schengen day counts, bookings, points, budgets, and what broke last time. Use when someone names a destination they want to visit someday, when a passport, visa, ETA, or entry rule has to be checked before dates are fixed, when counting days already spent in a visa-limited region, when a reservation or cancellation deadline needs recording, when a flight is cancelled or delayed, a bag goes missing, a passport is stolen or a claim has to be filed, when deciding which destination to take next against a season and a budget, when travelling with children, a group, elderly parents or a pet, when a stay runs past a month or needs per-diem handling, or when points or elite status are about to expire. Not for building one trip''s day-by-day itinerary (`travel-planning`), fare search (`flight`), accommodation search (`booking`), rental cars (`car-rental`), or moving abroad for good (`expat`).'
homepage: https://clawic.com/skills/travel
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: ✈️
    os:
    - linux
    - darwin
    - win32
    displayName: Travel
    configPaths:
    - ~/Clawic/data/travel/
    - ~/Clawic/data/bookings/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/health/
    - ~/Clawic/data/pets/
    - ~/Clawic/data/vehicles/
    - ~/Clawic/data/finances/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/travel/
      - ~/Clawic/data/bookings/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/health/
      - ~/Clawic/data/pets/
      - ~/Clawic/data/vehicles/
      - ~/Clawic/data/finances/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/travel/config.yaml` (what the user declared) and `~/Clawic/data/travel/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index *is* the list of files; never work from a list of names carried in your head, because most boxes get created after this skill was written. Read `~/Clawic/data/bookings/<current year>.md` before answering anything about a date, a reservation or "what have I got booked". If none of it exists, work from defaults and say nothing about it. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens.

**Write before the session ends** whenever it produced something durable: a place the user wants to see someday; a reservation made, changed or cancelled; a document issued, renewed or nearing expiry; a border crossed where days are counted; money spent or a per-day rate learned; a claim filed and how it ended; a program joined or a status earned; a trip that finished; or something the user will want to read again — a packing template, a visa procedure that finally worked, a place file. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**Reservations go to the shared box `~/Clawic/data/bookings/<year>.md`**, not into this skill's folder: flights, stays, cars, trains and tickets from every skill land in one file, so "what do I have booked in March" answers itself whoever wrote the row. One row per reservation, identified by its **locator** — read the file first and update that row in place, never append a second one: `date | type | provider | locator | travellers | status | free change/cancel until | amount with currency | trip`. Rows you did not write belong to another source: never edit them, and if the file already exists with different columns, match its columns and never rewrite its header.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text or a scanned document the user pastes in to be kept. Store the pointer and strip the value: `1password:Travel/Passport`, `keychain:airline-login`, `file:~/Documents/insurance.pdf`. A full passport, ID or Known Traveler number, a card number and an account password are values, not identifiers: keep the issuing country, the expiry date and the last four.

Most travel questions are already answered by something the user told you on an earlier trip. Answer from the archive first, then from the live web, and say which one you used. This skill is the system of record and the adviser: it never transacts — no purchase, no booking, no cancellation is executed, only prepared with the exact page, the deadline and the amount, for the user to press the button. Work from defaults immediately; never open with questions about their passport, their budget or their taste. The two exceptions to silence are `home_airports` and `passport_countries`: while either is unset, state the assumption out loud before quoting a route or an entry rule (Rules 2, 3). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale, units) → the Configuration table default.

## When To Use

- Someone names a place they want to go someday, or asks which destination to take next against a window, a season and a budget
- An entry question before anything is booked: passport validity, visa or electronic authorization, vaccination requirement, how many days are left in a rolling allowance
- A reservation exists, changes, or has a cancellation deadline that has to be remembered
- The trip is breaking right now: cancellation, delay, missed connection, lost bag, stolen documents, illness, a raised advisory
- The traveller is not a solo adult: children, a group splitting money, elderly parents, a pet, or a stay long enough to have legal consequences
- Coming home: what was actually spent, what to recommend, what to never pack again, what to claim
- Not for one trip's day-by-day itinerary (`travel-planning`), fare search (`flight`), accommodation search (`booking`), car hire (`car-rental`) or emigrating (`expat`) — this is the layer that outlives any single trip
- Mode: **act-as** the system of record (write the archive without asking) and **advise** on decisions. Never execute a transaction.

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "I'd love to go to X someday" | Capture it decision-ready: window, cost band, duration, blocker — a wish with no window never becomes a trip | `wishlist.md` |
| "Where should we go next?" | Intersect free window × season × budget × company; the constraint that moves least decides | `wishlist.md` |
| "Is my passport OK for X?" | Expiry − 6 months, issue date, blank pages, then the authorization the nationality needs | `documents.md` |
| "How many days have I got left?" | Rolling window counted backwards from the intended entry date, not per calendar year | `documents.md` |
| Vaccines, medication across borders, insurance cover | Lead times decide the booking date; the prescription decides the clinic appointment | `health.md` |
| "What will this cost?" | Total with its date: transport, lodging, local, food, activities, insurance, fee stack | `money.md` |
| Cards, cash, FX, tipping, refunds abroad | Always pay in local currency; the fee stack is bigger than the fare difference people chase | `money.md` |
| A booking was made, changed, or has a deadline | Row in the shared `bookings/<year>.md` plus a `## Due` line for the free-cancel date | `bookings.md` |
| Travel day itself: connections, security, borders, customs | Buffers by ticket structure, what cannot cross, what must be declared | `travel-day.md` |
| Flight cancelled, bag gone, stranded, robbed | Fix the trip first, claim second; the regime is set by where you departed and who you flew | `disruption.md` |
| Scams, advisories, solo safety, devices at the border | Prevention list plus the one-page emergency card the trip should not start without | `safety.md` |
| Packing, gear, luggage rules, adapters, batteries | The standing kit, refined by what the last trip never used | `kit.md` |
| Trains, driving abroad, ferries, transfers, rail passes | Price the actual legs against the pass; reservations are what kills passes | `transport.md` |
| Kids, groups, elderly parents, a pet, solo | Whose constraint governs, and how the money gets split before departure | `companions.md` |
| A month or more in one place, or nomad life | Day counting with legal consequences, connectivity, mail, visa runs | `long-stays.md` |
| Company trip, per diem, expenses, bleisure | Policy first, receipts in the shape finance accepts, personal days separated | `business-trips.md` |
| Points, miles, elite status, card benefits | Expiry beats accumulation; the benefit already paid for beats the one being chased | `loyalty.md` |
| Just got home | The 48-hour pass: actuals, three recommendations, one would-skip, unused gear | `debrief.md` |
| Anything else travel | Answer from the archive first, name the total with its currency and date, and write down whatever this session learned | — |

Coverage map: `wishlist.md` deciding where · `documents.md` entry rules and day counts · `health.md` medical readiness · `money.md` cost and payment · `bookings.md` reservation records · `travel-day.md` moving and crossing · `disruption.md` when it breaks · `safety.md` risk and emergencies · `kit.md` what to carry · `transport.md` ground movement · `companions.md` who is travelling · `long-stays.md` a month or more · `business-trips.md` travelling for work · `loyalty.md` programs and points · `debrief.md` closing the loop.

## Core Rules

1. **Answer from the archive before the web.** Read `memory.md`, the trip dossier for that place if `## Boxes` names one, and the spend baselines, before searching anything. A traveller who already spent nine days in Lisbon does not need a list of the top ten things to do in Lisbon; they need what they did not get to, and what they said not to repeat. Say which source the answer came from.
2. **Entry permission is checked before dates, and it is two numbers.** Passport: latest safe departure = **expiry − 6 months**, because many countries refuse entry inside that window; Schengen additionally wants a passport **issued within the previous 10 years** and valid **≥3 months beyond intended departure**, so an early-renewed passport can be refused on issue date while still showing validity. Allowance: count a rolling limit **backwards from the intended day of entry**. Worked example, Schengen 90/180 — entering 10 March with 62 days already inside the previous 180 leaves 28; a 30-day trip is refused at the border, and no booking system checks this for you (`documents.md`).
3. **Every number is a total, with its currency and the date it was estimated.** total = transport + lodging + local transport + food + activities + insurance + the fee stack (visa, seat, bag, resort fee, tourist tax, FX 1-3%). Name the four largest lines. A fare is never the answer to "what will it cost", and last year's estimate is not this year's price (`money.md`).
4. **Book in order of irreversibility.** Entry permission → the scarce thing with a release date (a permit, a lottery, the one property that works) → long-haul transport → lodging → everything else. Nothing non-refundable is bought before the permission that could void it, and a refundable rate is worth paying for exactly while the trip is still conditional.
5. **Buffers are computed, not felt.** One ticket: the carrier owns the miss and the published minimum connection time is the floor. Separate tickets: you own it — budget **≥3 h international, ≥2 h domestic**, and treat the last departure of the day as a hotel night rather than a connection. Airport arrival: **2 h international / 90 min domestic**, plus whatever the place file records from last time. Scale all of it by `risk_posture` (`travel-day.md`).
6. **A reservation that is not written down does not exist.** The moment one is made, changed or cancelled, its row goes to `~/Clawic/data/bookings/<year>.md` and its free-change-or-cancel date goes to `## Due` in `memory.md`, in the property's local time. The money in travel is lost at deadlines nobody diarised, not at prices nobody negotiated.
7. **Under-plan by one thing per day.** `itinerary_density` sets the count of *anchors* — things with a fixed time or a ticket: loose 1/day, balanced 2, packed 3. Everything else is a list of candidates near that day's anchor, never a schedule. A day with three anchors has no room to absorb one queue.
8. **The debrief is part of the trip.** Within 48 hours of getting home: actual total, three recommendations, one would-skip, the gear never used, and any per-day rate learned. What decays first is exactly what is worth money next time — the name of the place, the transfer that worked, the hour the queue disappeared (`debrief.md`).

## Entry Rules That Decide The Trip

Categories are stable; specific systems, fees and dates change — verify each one on the destination government's own site before it gates a booking, and note the date you checked (`documents.md`).

| Rule | What it actually constrains |
|---|---|
| Six-month passport validity | Common requirement across Asia, the Middle East and much of Africa; enforced at check-in by the airline, which is denied boarding, not a border problem |
| Rolling day allowance | Schengen 90 days in any 180; counted backwards per entry, across all member states together, on every entry stamp you ever collected |
| Electronic travel authorization | Pre-arrival online permission separate from a visa (US, Canada, UK, Australia, New Zealand, EU): approval is usually fast, but rejection is silent until check-in — apply days ahead, not hours |
| Onward or return ticket | Airlines are fined for carrying a passenger the destination refuses; a one-way to a country that requires proof of exit is a boarding-gate problem |
| Visa tied to the passport, not to you | Renewing a passport can strip a valid visa; carry both books or get the visa transferred |
| Blank pages | Several countries require 2 blank facing pages; a full passport is refused with years of validity remaining |
| Yellow fever certificate | Required based on the countries you *transited*, not only where you started; valid from 10 days after the dose and for life under the 2016 WHO rule |
| Vaccination and medication rules | Some common prescriptions (stimulants, strong painkillers, some cold remedies) are controlled or banned in the destination; the letter has to be written before departure (`health.md`) |
| Currency declaration | €10,000 / US$10,000 equivalent triggers a mandatory declaration in the EU and the US, counted per crossing and per traveller, cash and equivalents together |
| Customs allowance on return | The limit is what you bring *in*, including gifts and things bought duty-free in transit; VAT-refund forms must be stamped before you check the bag |
| Anything else | Read the destination's own immigration page for your `passport_countries`, and record what you found with the date in the place file |

## Cost Lines People Forget

The estimate that comes in under budget is usually missing one of these, not mispriced on the big line (`money.md`).

| Line | Why it lands late |
|---|---|
| Airport ↔ city, both ends | Two transfers can outweigh the difference between the two fares that were compared for an hour |
| Seat, bag, and check-in fees | Priced after the fare comparison, and highest at the airport counter |
| Resort fee / city tourist tax | Charged at the property, in local currency, and absent from the booking total on most platforms |
| FX and DCC | 1-3% card fee; accepting the terminal's offer to bill in your home currency costs several percent more, always |
| Insurance | Pre-existing-condition and cancel-for-any-reason waivers usually expire ~14-21 days after the *first* trip payment, so buying late costs the cover, not the premium |
| Visa and authorization fees | Per traveller, non-refundable on rejection, sometimes with a service fee larger than the fee |
| Data | Roaming, or an eSIM bought calmly at home instead of at 2 a.m. in an arrivals hall |
| Deposits held | Car and hotel holds freeze real money for days on a debit card |
| The first and last day | Half-days still cost a full night, and both ends are the days people eat at the airport |
| Coming home | Restocking, a laundry pile, and the day off nobody budgeted |

## Red Flags

Observable signals that outrank every plan in this skill. Anything in this table suspends the protocols: route to a clinician or the local emergency number, and move the trip around the person.

| Signal | Suspicion | Action |
|---|---|---|
| Fever within 3 weeks of leaving a malaria area | Malaria until proven otherwise | Same-day medical care; state the country and the dates — it is missed when the travel history is not volunteered |
| Fever with rash, severe joint pain or bleeding after a tropical trip | Dengue or another arbovirus | Same-day care; avoid NSAIDs until dengue is excluded |
| Calf pain or swelling, or breathlessness, within two weeks of a flight over ~4 h | DVT or pulmonary embolism | Emergency care now, not on landing at home |
| Diarrhoea with blood, or fever past 48 h | Invasive infection | Clinician; anti-motility medication makes it worse |
| Any animal bite, scratch or bat contact where rabies exists | Rabies exposure | Wash 15 minutes with soap and water and start post-exposure prophylaxis the same day — it is not deferrable until home |
| Headache with unsteadiness, confusion, or breathlessness at rest above ~2,500 m | High-altitude cerebral or pulmonary oedema | Descend immediately; no other treatment substitutes for descent |
| Passport, visa or residence card stolen | Loss of legal status and of the ability to board | Police report first (insurers and embassies both require it), then the nearest embassy or consulate (`disruption.md`) |
| Destination advisory raised while the traveller is in country | Insurance may void on the day the advisory changes | Read the policy's advisory clause before deciding to stay; document the date (`safety.md`) |

## Output Gates

Before delivering a plan, a quote, or a recommendation:

- Did I check passport validity, authorization and the rolling day count before proposing dates (Rule 2)?
- Is my number a total with its currency and estimate date, not a fare (Rule 3)?
- Did I read the archive — past trips, place files, spend baselines — before recommending something they have already done (Rule 1)?
- Does every reservation I mentioned exist as a row in `~/Clawic/data/bookings/<year>.md`, and every deadline as a line in `## Due`?
- Am I about to execute a purchase, cancellation or change? Stop: prepare it, name the amount and the deadline, and hand it over.
- Did anything durable from this session land in the box `memory-template.md` names, with its `## Boxes` line, in this same turn?
- Did anything the user pasted — a booking email, a policy, a scan — leave a passport number, card number or password in a file instead of a pointer?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/travel/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| home_airports | list (IATA codes) | none | Origin of every route, duration and cost estimate; while unset, name the origin you are assuming before quoting |
| passport_countries | list (country) | none | Selects which entry-rule set applies in `documents.md`; while unset, say the entry rules are unverified and name exactly what to check |
| daily_budget | number + currency | none — derive from the regional band in `money.md` | The per-day spend a plan is sized to, and the bar for calling something expensive |
| trip_style | budget \| midrange \| comfort | midrange | Accommodation tier, transport class and the cost band quoted in every estimate |
| risk_posture | tight \| balanced \| padded | balanced | Connection and arrival buffers (Rule 5), refundable-versus-cheapest default, and the advisory level that changes a recommendation |
| itinerary_density | loose \| balanced \| packed | balanced | Anchors per day in anything planned (Rule 7) |
| default_party | solo \| couple \| family \| group | solo | Whose constraints apply by default: pace, room configuration, money split, `companions.md` section used |
| constraints_file | path | none | Long text at `~/Clawic/data/travel/<file>` — diet, mobility, medical, countries that are off the table — overriding generic advice wherever it conflicts |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Channels and programs** — which booking platforms, airline alliance and hotel chains they actually use, seat and room preferences, whether to quote a cash price or a points price — affects `bookings.md` and `loyalty.md`
- **Conventions** — how trips are named and archived, what a debrief must always contain, which currency estimates are quoted in — affects the trip dossier shape in `memory-template.md`
- **Platform** — home base and any second base, home currency and locale, whether prices are quoted per person or per party — affects every estimate
- **Safety posture** — refundability appetite, insurance always versus card cover, the advisory level that cancels a trip, willingness to self-transfer — affects Rules 4 and 5 and `safety.md`
- **Output format** — how much itinerary detail they want written out, whether to include maps and addresses, language of the local phrases produced — affects everything delivered
- **Restrictions** — diet, accessibility and mobility, medical constraints, countries excluded on principle, a train-instead-of-plane threshold in hours — affects destination shortlists and `transport.md`
- **Cadence** — how often the wishlist is reviewed against seasons, when documents are checked, whether expiry warnings arrive months or weeks ahead — affects the `## Due` table

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Buying the non-refundable fare before the visa is granted | The consulate does not care about your booking, and refusal rates are real | Refundable or hold-only until permission exists (Rule 4) |
| Two separate tickets treated as one connection | Nothing protects you: the second carrier owes you nothing, and the bag is not through-checked | Self-transfer buffers from Rule 5, or one ticket (`travel-day.md`) |
| A passport with five months left | It is the airline that denies boarding, before any border sees it | Diary renewal at expiry − 9 months in `## Due` (`documents.md`) |
| Accepting the terminal's offer to charge in your home currency | Dynamic currency conversion is priced by the merchant, not your bank, and always loses | Always local currency, always (`money.md`) |
| Buying insurance the week before departure | The valuable waivers close ~14-21 days after the first payment, not before departure | Buy with the first non-refundable payment (`health.md`) |
| Confirmation numbers left in the inbox | Search fails exactly when there is no data connection and a counter agent is waiting | Row in `bookings/<year>.md` at the moment of booking (Rule 6) |
| Counting Schengen days per calendar year | The window is rolling and personal; January does not reset it | Count backwards 180 days from the intended entry (Rule 2) |
| Planning around weather alone | Peak is set by school holidays and the local festival calendar; the crowd and the price move with those, not the forecast | Check both calendars before fixing dates (`wishlist.md`) |
| Chasing a cheaper fare across a whole evening | The saved amount is routinely smaller than the transfer, bag and seat lines added afterwards | Compare totals, once (Rule 3) |
| Letting points expire while saving them for the perfect trip | Most programs expire on inactivity, and devaluations are unannounced | Expiry rows in `## Due`; spend before optimizing (`loyalty.md`) |
| Photographing the passport into a notes app "just in case" | The copy outlives the trip and travels through every backup | Provider pointer only; copies in the user's own password manager (Secrets, above) |
| Coming home and getting straight back to work | The debrief costs 20 minutes and pays every subsequent trip | The 48-hour pass (Rule 8, `debrief.md`) |
| Booking a tight connection through a country requiring a transit visa | Airside transit is not visa-free everywhere, and the airline will check | Verify transit rules for `passport_countries`, not just the destination |

## Where Experts Disagree

- **Plan it or wing it.** The frontier is scarcity, not temperament: anything with finite capacity on a fixed release date (permits, a specific property, a festival, an award seat) is booked the day it opens; everything with unlimited supply is decided on the ground. The argument between the two camps is usually about trips whose scarcity profile they never compared.
- **Refundable premium versus cheapest fare.** Pay for flexibility while the trip is conditional — visa pending, dates unagreed, someone else's calendar involved. Once every condition has cleared, the premium is pure cost. The mistake is applying either policy to a whole trip.
- **Insurance always, or card cover is enough.** Card cover is real but narrow: it typically needs the trip paid on that card, excludes pre-existing conditions, and caps medical evacuation far below what an air ambulance costs. Standalone policies win the moment the destination is remote or the traveller has a condition; card cover is defensible for short trips inside good public-healthcare systems.
- **Hoard points or burn them.** Accumulators are right that redemption value scales with saving up; burners are right that programs devalue without notice and expire on inactivity. The resolution is a ceiling, not a philosophy: hold no more than one aspirational redemption's worth, spend the rest (`loyalty.md`).
- **Carry-on only, or check the bag.** Carry-on wins on connections, disruption and time; checking wins on trips with a fixed base, gear, or a party where one bag serves several people. The tie-break is how many times the bag will actually be carried.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/travel (install if the user confirms):
- `travel-planning` — building one trip's day-by-day itinerary and multi-city routing
- `flight` — fare search, price tracking and route comparison
- `booking` — accommodation search and comparison across platforms
- `car-rental` — hire pricing, comparison and lease-versus-rent analysis
- `expat` — moving abroad for good: residence visas, relocation, settling in

## Feedback

- If useful, star it: https://clawic.com/skills/travel
- Latest version: https://clawic.com/skills/travel

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/travel.
