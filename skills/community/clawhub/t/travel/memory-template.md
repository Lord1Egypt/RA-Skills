# Working File Templates — Travel

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/travel/config.yaml` | Key by key, read-modify-write |
| Traveller profile, wishlist, documents, loyalty, spend baselines, trip index, due dates, box index | `~/Clawic/data/travel/memory.md` | Rewritten in place; stays small |
| Reservations of any kind — flights, stays, cars, trains, tickets, tours | `~/Clawic/data/bookings/<year>.md` (**shared**) | One row per locator, every provider and every skill in one file |
| One trip: dates, party, plan, its bookings, its money, its debrief | `~/Clawic/data/travel/trips/<yyyy>-<place>.md` | Its own file from the moment the trip is real, not when it ends |
| Places to go someday | `## Wishlist` in `memory.md` until it splits; then `~/Clawic/data/travel/destinations.md` | One row per place |
| Passports, visas, authorizations, insurance, licences — expiry ledger | `## Documents` in `memory.md` until it splits; then `~/Clawic/data/travel/travel-documents.md` | One row per document per holder |
| Loyalty programs, numbers, tiers, points | `## Loyalty` in `memory.md` until it splits; then `~/Clawic/data/travel/programs.md` | One row per program |
| Cover and perks already paid for by a card or a membership | `## Card Benefits` in `memory.md`, moving with `## Loyalty` when it splits | One row per benefit, checked before buying insurance or a lounge pass |
| Border crossings where days are counted (Schengen, tax residency) | `## Presence` in `memory.md` until it splits; then `~/Clawic/data/travel/presence/<year>.md` | Append-only, cut by year, consulted by date |
| Things produced that get re-read whole — packing templates, a visa procedure that finally worked, a place cheat-sheet, an emergency card, a claim letter and its outcome, a group money agreement | `~/Clawic/data/travel/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| A person met, hosted by, or travelling with, who matters beyond this trip | `~/Clawic/data/contacts/contacts.md` (**shared**) | Name only as a pointer from here — never a duplicate record |
| Vaccinations, allergies, medication, conditions | `~/Clawic/data/health/profile.md` (**shared**) | Travel writes the travel-relevant rows; leaves the rest alone |
| A pet's travel paperwork: microchip, rabies dates, titre, carrier size | `~/Clawic/data/pets/<name>.md` (**shared**) | Appended to the animal's own file, never copied here |
| The user's own vehicle taken abroad: cover extended, breakdown, mandatory equipment | `~/Clawic/data/vehicles/<plate>.md` (**shared**) | Appended to the vehicle's own file; referenced from a trip by plate only |
| An annual travel card fee or a subscription that exists for travel | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row, with its currency and renewal date |
| **Anything durable this table does not name** | `~/Clawic/data/travel/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials, numbers that authenticate, document scans | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A place was named as somewhere they want to go | `## Wishlist` |
| A trip became real — dates held, first payment made | `trips/<yyyy>-<place>.md`, plus its row in `## Trips` |
| Any reservation was made, changed, or cancelled | Its row in `bookings/<year>.md`, plus its free-cancel date in `## Due` |
| A document was issued, renewed, refused, or found to be expiring | `## Documents`, plus its expiry in `## Due` |
| A border was crossed and days are being counted | `## Presence` |
| Money was spent, or a per-day rate was learned | The trip's money section; the rate in `## Spend Baselines` |
| A claim, refund or compensation was filed | `artifacts/claim-<provider>-<yyyy-mm>.md`, outcome appended when it lands |
| A program was joined, a tier earned, points credited or expiring | `## Loyalty`, plus any expiry in `## Due` |
| A card or membership benefit was found, used or lapsed | `## Card Benefits` |
| A vaccination was given or a prophylaxis course prescribed | `~/Clawic/data/health/profile.md` |
| A packing template, a visa procedure, a place cheat-sheet or an emergency card was produced | `artifacts/` |
| The trip ended | The debrief section of its dossier; then update `## Spend Baselines` and `## How They Travel` |
| The user declared a preference | Its key in `config.yaml` |
| Anything recurring was scheduled or checked | `## Due` |

## Start flat, split only when it hurts

Everything except trip dossiers, artifacts and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. **Who**: whichever session is about to append the entry that crosses the line. Not later, not a cleanup pass.
2. **When**: before appending, count the section's entries. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — split first, then append to the new file.
3. **What happens to the original**: in the same turn, create the file in `~/Clawic/data/travel/`, move the whole section into it, **delete the section from `memory.md`** leaving only its `## Boxes` line, and add that line.
4. **Precedence**: never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Keep the headings identical on both sides of the move — `## Wishlist` in `memory.md` becomes the `## Wishlist` heading inside `destinations.md`, with the same columns — so the split is a copy-paste and never a rewrite that loses rows.

Trip dossiers and artifacts are the exception: a trip file and a packing template are born as their own file whatever their size, because each is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text, emails or scanned documents the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`1password:Travel/Passport` · `bitwarden:Airlines/BA` · `keychain:hotel-loyalty` · `env:TRAVEL_INSURANCE_ID` · `file:~/Documents/passport-scan.pdf` · `vault:travel/cards`

When the user pastes a booking email, an insurance policy or a photographed document to save, replace each secret value before writing and leave the pointer visible: `passport: <1password:Travel/Passport>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: booking locators and confirmation codes, airline, hotel and platform names, flight numbers, seat and room numbers, loyalty program names and membership numbers, elite tier and its expiry, insurance provider and policy number, visa type and validity dates, document expiry dates and issuing country, the last four of a passport, prices paid with currency, embassy and consulate phone numbers, IATA and station codes, addresses of places stayed.

**Secrets, strip them**: full passport, national ID and Known Traveler numbers, passport or visa scans and MRZ lines, card numbers, expiry and CVV, bank account and IBAN, airline, hotel and platform account passwords and PINs, loyalty redemption PINs, eSIM activation codes and QR images, insurance-portal logins, home alarm codes shared with a house-sitter, and any photograph of a document.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared bookings box](#shared-bookings-box) · [trips/](#trips) · [artifacts/](#artifacts) · [presence/](#presence) · [other shared boxes](#other-shared-boxes) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/travel/` if it does not exist.

```yaml
home_airports: [LHR, LGW]
passport_countries: [Ireland]
daily_budget: 140 EUR
trip_style: midrange
risk_posture: padded
itinerary_density: loose
default_party: couple
constraints_file: constraints.md

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
channels:
  alliance: oneworld
  seat: aisle, forward cabin
  stays: apartments over hotels for 4+ nights
restrictions:
  diet: coeliac
  train_over_plane_hours: 5
cadence:
  wishlist_review: quarterly
  document_warning_months: 9
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Travel Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Trip dossiers (6) → `trips/`; open the one for a place before planning or recommending anything there
- Packing template, long-haul cold → `artifacts/packing-cold-longhaul.md`; read before packing for anything under 5 °C
- Japan visa-free entry procedure, worked 2026-03 → `artifacts/visa-japan.md`; read before any Japan dates
- Lisbon place file → `artifacts/place-lisbon.md`; read whenever Lisbon comes up again
- Emergency card → `artifacts/emergency-card.md`; read before departure, and the moment anything goes wrong
- Schengen presence log (2 years) → `presence/`; read before booking any Schengen entry

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Passport expiry check (renew at expiry − 9 months) | year | 2026-01-04 | 2027-01-04 |
| Annual multi-trip insurance renewal | year | 2026-02-11 | 2027-02-11 |
| Avios expiry — any activity resets it | 18 months from last activity | 2026-05-02 | 2027-11-02 |
| Free cancellation, Kyoto ryokan (local time) | once | — | 2026-09-14 |
| Wishlist review against season windows | quarter | 2026-07-01 | 2026-10-01 |

## Traveller Profile
Two adults, Irish passports, based London. Long-haul once a year, three or four European weekends. Coeliac — see `constraints.md`.

## Documents
| Holder | Document | Issued by | Last four | Issued | Expires | Notes |
|--------|----------|-----------|-----------|--------|---------|-------|
| A | Passport | Ireland | …7741 | 2019-03-02 | 2029-03-02 | Safe travel until 2028-09-02 (expiry − 6 mo) |
| A | US ESTA | US | — | 2025-06-10 | 2027-06-10 | Tied to this passport; dies with it |
| Both | Annual multi-trip insurance | Provider name | policy 44-8812 | 2026-02-11 | 2027-02-11 | Medical evacuation 5,000,000 EUR; excludes anything above 3,000 m |

## Wishlist
| Place | Why | Best window | Rough cost | Duration | Blocker |
|-------|-----|-------------|------------|----------|---------|
| Japan | Food, temples, trains | late Mar-early Apr, or Nov | 4,000-5,000 EUR for two, 2 weeks (est. 2026-05) | 14-18 days | Sakura weeks sell out ~6 months out |
| Namibia | Self-drive, dark skies | May-Sep | 6,000 EUR for two, 12 days (est. 2026-02) | 12 days | Needs 4x4 booked a year ahead |

## Trips
| Dates | Place | Party | Status | Total | Dossier |
|-------|-------|-------|--------|-------|---------|
| 2026-09-12 → 09-26 | Japan | couple | booked | 4,380 EUR budgeted | `trips/2026-japan.md` |
| 2026-04-03 → 04-07 | Lisbon | couple | done | 812 EUR actual | `trips/2026-lisbon.md` |

## Loyalty
| Program | Number tail | Tier | Tier expires | Balance | Balance expires |
|---------|-------------|------|--------------|---------|-----------------|
| BA Executive Club | …318 | Bronze | 2027-04-30 | 61,000 Avios | on 18 months of inactivity |

## Card Benefits
| Card or membership | Benefit | Conditions | Expires |
|--------------------|---------|------------|---------|
| Travel card, annual fee 240 EUR | Trip insurance, 250,000 EUR medical | Trip must be paid on this card; pre-existing excluded | with the card |
| Same card | Two lounge visits a year, one guest each | Departure only | 2026-12-31, unused |

## Spend Baselines
| Region | Per day, per person | Covers | As of |
|--------|--------------------|--------|-------|
| Western Europe, city | 95 EUR | food, local transport, one paid sight | 2026-04 |
| Japan, mixed | 110 EUR | food, local transport, entries; excludes rail pass | 2026-09 est. |

## How They Travel
Books flexible, decides on the ground. Hates 6 a.m. departures — never propose one. Will pay for a lounge on a connection over 3 h. Never uses hotel breakfast.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next year:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Cancellation deadlines, document expiries, points expiries and review cadences all live here, and a deadline row is deleted once it has passed or been used.
- **`## Documents`**: `Last four` only, never the number. Compute and write the safe-travel date rather than making a future session redo Rule 2.
- **`## Wishlist`**: a row without a window, a cost band and a blocker is a daydream, not an entry. Costs carry their currency and the date estimated. Delete a row when the trip happens — it moves to `## Trips`.
- **`## Trips`**: an index, not a store. The dossier holds the content; this table holds one line per trip so a question about any year is answered without opening six files.
- **`## Spend Baselines`**: the reason the archive is worth keeping. One row per region and travel style, always per person per day, always with the currency and the month it was learned.
- These headings are exactly the ones the split-out files get, so the split stays a copy-paste.

| Status | Meaning |
|--------|---------|
| `ongoing` | Still learning how they travel |
| `complete` | Profile, documents and baselines are all known |

## Shared bookings box

Lives at `~/Clawic/data/bookings/<year>.md` and is shared with every other skill that touches a reservation — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Bookings — 2026

| Date | Type | Provider | Locator | Travellers | Status | Free change/cancel until | Amount | Trip |
|------|------|----------|---------|------------|--------|--------------------------|--------|------|
| 2026-09-12 | flight | BA | 4KJ2QP | A, B | confirmed | non-refundable | 1,180 EUR | 2026-japan |
| 2026-09-14 | stay | Ryokan Kyoto | R-88213 | A, B | confirmed | 2026-09-07 23:59 JST | 640 EUR | 2026-japan |
```

- **Identity is the locator.** Read the file before adding and look for it. If it is there, update the row in place — it is yours. Only its absence justifies a new row. Two rows for one locator is how a cancelled booking survives as a phantom.
- **Cancellation is part of the record.** A cancelled reservation gets `status: cancelled` and the refund amount, and is deleted at the end of the following year. A file that only grows stops being answerable.
- **Deadlines in the property's local time**, with the zone written out — `2026-09-07 23:59 JST`. A midnight deadline read in the wrong zone is the most expensive rounding error in travel. Every deadline in this column also gets a row in `## Due`.
- **Amounts carry their currency inside the value** (`640 EUR`), because rows written by other skills and other countries sit next to yours and someone will add the column up.
- **Rows you did not write are not yours.** Never edit or delete a row another source created; add your own.
- **Foreign columns win.** If the file already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- **Scale cut**: one file per year. If a single year passes ~60 rows, split by quarter into `~/Clawic/data/bookings/<year>-q<n>.md` and leave `<year>.md` as an index (`Date | Type | Locator | → file`). If you arrive and the folder already looks like that, follow it.
- The locator is a working identifier and stays. The account password behind it never does.

## trips/

One file per trip at `~/Clawic/data/travel/trips/<yyyy>-<place>.md`, created when the trip becomes real — dates held or a first payment made — not when it ends. Add its `## Trips` row and its `## Boxes` coverage in the same turn.

```markdown
# Japan — September 2026
*Read before anything about this trip, and before any future Japan question. Status: booked.*

## Dates and party
2026-09-12 → 09-26. Two adults. Anniversary.

## Entry
Irish passports, visa-free 90 days, checked 2026-05-02 on the destination's own immigration site. Passport A safe until 2028-09-02.

## Bookings
Rows live in `~/Clawic/data/bookings/2026.md`; locators 4KJ2QP, R-88213. Free cancel on the ryokan until 2026-09-07 23:59 JST.

## Money
| Line | Budget | Actual | Note |
|------|--------|--------|------|
| Transport | 1,180 EUR | — | flights, both |
| Rail | 420 EUR | — | 7-day pass, priced against 4 actual legs |
| Lodging | 1,290 EUR | — | |
| Daily (food, local, entries) | 1,540 EUR | — | 110 EUR pp/day × 14 × ... |

## Plan
Anchors only, one per day (`itinerary_density: loose`). Candidates listed per area, not scheduled.

## Debrief
Written within 48 h of getting home: actual total, three recommendations, one would-skip, gear never used, per-day rate learned.
```

- The dossier is the only place a trip's plan and money live. Nothing about a specific trip goes into `memory.md` beyond its index row.
- A trip that never happened is not deleted: set the status to `cancelled`, keep what was learned about the destination, and move the place back to `## Wishlist` with the blocker updated.
- Anything in the dossier that stays true after the trip — how to get from the airport at night, which pass was worth it, the restaurant to return to — is lifted into `artifacts/place-<name>.md` at debrief, so the next trip does not have to open a three-year-old dossier to find it.

## artifacts/

One file per thing, at `~/Clawic/data/travel/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **packing template** (`packing-<archetype>.md`), **entry procedure that worked** (`visa-<country>.md`), **place file** (`place-<name>.md`), **emergency card** (`emergency-card.md`), **claim and its outcome** (`claim-<provider>-<yyyy-mm>.md`), **group money agreement** (`group-<trip>.md`). Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Place — Lisbon
*Read whenever Lisbon comes up again. Last updated 2026-04-07.*

Airport → city: metro to Saldanha, 20 min; taxis queue badly after 22:00.
Worth returning: ... · Skip: ...
Costs seen: 95 EUR pp/day, April 2026.
```

```markdown
# Emergency card
*Read before departure, and the moment anything goes wrong. Updated 2026-07-26.*

Insurance: provider name, policy 44-8812, 24 h line +xx xxx. Login: <1password:Travel/Insurance>.
Documents: passports <1password:Travel/Passport>. Last four …7741, …2093.
Blood group, allergies, current medication: from `~/Clawic/data/health/profile.md`.
Next of kin and embassy numbers for the destination.
```

An artifact is worth a file when it will be read again by a future session that has no memory of this one. A three-line note that only makes sense inside one trip belongs in that trip's dossier instead.

## presence/

Created only when a rolling day limit or a tax-day count applies to this traveller. Until then, the count lives in `## Presence` inside `memory.md`.

```markdown
# Presence — 2026

| In | Out | Country / area | Days | Purpose | Counts toward |
|----|-----|----------------|------|---------|---------------|
| 2026-04-03 | 2026-04-07 | Portugal (Schengen) | 5 | leisure | Schengen 90/180 |
| 2026-06-11 | 2026-06-14 | France (Schengen) | 4 | work | Schengen 90/180, UK SRT |
```

- **Both the day of entry and the day of exit count as full days** in the Schengen rule; a four-night trip is five days.
- One row per crossing, never one row per country visited on the same continuous stay — the stamp is what an officer counts.
- Answering "how many days do I have left" means summing the rows whose dates fall inside the 180 days *before the intended entry date*, not inside a calendar year.
- Tax-day thresholds are jurisdiction-specific and are not all a simple 183-day count. Record the days; say what they add up to; route the conclusion to a tax professional.

## Other shared boxes

Each of these is owned by a different skill the user may not have installed, so the minimum protocol travels here. In all of them: read before adding, match on the identity key, update in place, never rewrite a header you did not write, and leave amounts with their currency.

**Retirement is part of every one of these boxes.** When something this skill wrote stops being true — a policy lapsed, a vaccination out of validity, a card cancelled, a vehicle sold, a person who was a one-trip contact — delete the row or block you wrote and note what you deleted, from which box, with the date, in `memory.md`. A shared box that only grows stops being answerable, and the deletion note is what stops a future session re-adding it. Rows another source wrote are never yours to delete.

- **`~/Clawic/data/contacts/contacts.md`** — identity is email or handle. Columns `name | role | preferred channel | context`. A host, guide, driver or friend met on a trip who matters afterwards goes here once; the trip dossier references them by name only. Past 15 people the box becomes one file per person and `contacts.md` the index.
- **`~/Clawic/data/health/profile.md`** — identity is the metric plus its date. Travel writes only travel-relevant rows: vaccinations with dates and validity, prophylaxis courses, allergies, current medication with its generic name (the brand does not exist in most countries), and any condition an insurer or a clinic abroad would need. Never overwrite rows another skill wrote; append with a date. `profile.md` holds what is stable; a metric measured as a series moves to `~/Clawic/data/health/<metric>.md` once it passes ~15 entries, and `profile.md` keeps its index line. A vaccination whose validity has run out is deleted, not left as history — the certificate is the history.
- **`~/Clawic/data/pets/<name>.md`** — identity is the animal's name. Travel appends the paperwork block only: microchip presence, rabies vaccination date, titre test date if the route needs one, carrier dimensions accepted, and the date each requirement was verified with the destination authority. The animal's medical history is not this skill's to write. One file per animal at any size; a requirement no longer valid is replaced by the current one, never stacked underneath it.
- **`~/Clawic/data/vehicles/<plate>.md`** — identity is the registration plate. Travel appends only what a trip abroad establishes: insurance extended to which countries and until when, breakdown cover valid abroad, the mandatory equipment that country requires, and any toll or zone registration. The vehicle's servicing and ownership history belongs to whichever skill owns it. If the folder holds a single `vehicles.md` table instead of one file per plate, follow what is there. Cover that has expired comes out of the file: an extension that ended is the most dangerous thing to leave looking current.
- **`~/Clawic/data/finances/subscriptions.md`** — identity is the subscription name. A travel credit card's annual fee or a lounge membership goes here with its amount, currency and renewal date, so it is visible next to every other recurring cost. The card's number never does. The file is a single table and is not split by year or count — it stays small because a cancelled subscription's row is deleted on cancellation, with the date noted in `memory.md`.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings and columns it had inside `memory.md`.

`destinations.md` — `## Wishlist`. Once it exists, add a `Last reviewed` line at the top: a wishlist nobody reviews against its season windows is a list of regrets.

`travel-documents.md` — `## Documents`. Crosses the threshold fastest for a family: four people times passport, authorization, insurance and licence is sixteen rows before anyone has travelled.

`programs.md` — `## Loyalty` and `## Card Benefits`, moved together and under the same headings. The benefits section is what makes the file worth opening before buying insurance or a lounge pass.

`presence/<year>.md` — `## Presence`, cut by year because it is a log consulted by date and it never stops growing.
