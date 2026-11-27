# Intake — what to ask the business before you build

Send these questions to the business (owner or manager) and get written answers.
Do not start phase 0 with gaps in sections **A, B, D and E** (phase 0 needs 1, 8, 9,
13, 19, 21 and the budget 22). Section **C** (14–18) may be completed before phase 2.
Restaurant answers below are **examples**; never use them as defaults for a real
customer.

Answers are kept in a short intake record (plain text or a comment on the business
object once it exists). Staff personal data never goes into chat logs or public places.
**Basic** person fields (name, login e-mail, stations) go into master; **protected**
fields (pay, health notes, private contacts) go into planning for managers only (E2).

## A. Business and structure

| # | Question | Why | Example answer |
|---|---|---|---|
| 1 | Name of the business (legal and short name)? | `organisation` object, scope slug | "Trattoria Example GmbH", short `trattoria` |
| 2 | Sites (addresses)? One or several? | one `building` per site | one site |
| 3 | **Stations / areas** where people work? | `space` objects and the station option of shifts | kitchen, service, bar, dishwashing, shift lead |
| 4 | Opening hours per weekday, including split days and nights after midnight? | templates, plausibility checks; shifts after midnight need the end-date prompt (phase 1 §4.3) | Tue–Sun 11:30–14:30 and 17:30–23:00, Mon closed |
| 5 | Typical shifts per station (name, start, end, break)? | `shiftTemplate` | Kitchen early 10:00–15:00, 30 min |
| 6 | Country / region and time zone? | country module, public holidays, time handling | Germany, Europe/Berlin. **Not Europe/Berlin → stop** and file `ontouser_service_request` (SKILL.md, "Stop and escalate"); without a country module for the country, ask whether the business accepts a build without the country checks. |
| 7 | Planning period: week or month? Who publishes, and how far ahead? | periods, first publication | weekly, published by Thursday for next week |

## B. People and roles

| # | Question | Why | Example answer |
|---|---|---|---|
| 8 | **Who is the manager** (operations) with full rights? Human, agent, or both? | rights matrix, stop/ask contact. The account that runs this build registers as in the platform skill, creates the three scopes and is therefore their manager; a human manager gets their own account and the same rights. | owner + one agent |
| 9 | Are there shift leads who plan but must not change master data? Note for the business: with planning write, shift leads see **and change** pay data on the staff records (phase 4 §1.2). | separate rights (planning write, master read) | one shift lead |
| 10 | **Staff list**: first name, last name, e-mail used for login, station(s) they may work at, contract type, hourly rate, year of birth (only if youth protection matters) | `person`, qualification links, payroll view | 8 people |
| 11 | **Contract types** in use? | `contractType` options; minijob warning | full-time, part-time, fixed-term, minijob, casual (one English value each, e.g. `fixedTerm`; do not use the ambiguous `contract`) |
| 12 | Which qualifications must be proven by a document (e.g. food-hygiene instruction)? | `file` attached to the person | hygiene instruction, valid until |
| 13 | Does every staff member have their own e-mail address and a device to log in? | staff accounts, notifications | yes, except two → manager clocks for them |
| 13a | **Visible to colleagues:** staff can read the master person of every colleague, including the login e-mail and — if recorded — the birth year. Is that acceptable, or must the birth year be left out (no youth-protection check) and e-mail addresses be kept private? | master person fields ([phase0.md](phase0.md) §1.4, [phase1.md](phase1.md) §4.2) | acceptable for e-mail; birth year only for the two trainees |

## C. Rules and process

| # | Question | Why | Example answer |
|---|---|---|---|
| 14 | Which requests may staff make: absence, day-off wish, shift request, swap, takeover, handover? Who decides? | phase 2 actions | all; manager decides |
| 15 | Clock in/out by staff themselves? Who may correct actual times, and is a reason required? | phase 4 | staff clock; only manager corrects, reason required |
| 16 | Notification channels: in-app only, or also e-mail/push? | notify settings | in-app + e-mail |
| 17 | Payroll office: which columns, which month cut-off, CSV separator? | phase 4 export | generic CSV, semicolon, decimal comma |
| 18 | Works council or staff representation? Data-protection contact? | country module | none / external DPO |

## D. Naming and language

| # | Question | Why | Example answer |
|---|---|---|---|
| 19 | **Label language** for staff-facing texts (views, buttons, notifications)? Second language needed? | labels, translation keys | German; English for two staff members |
| 20 | **Naming pattern** for shifts and objects? | readable lists, search | `<date> <start>-<end> <station>` e.g. `2026-11-10 17:30-23:00 service` |
| 21 | Scope slug (lower case `a-z0-9_`; the scope name may have 30 characters and `_planning` takes 9, so the slug has **at most 21**)? | scope names | `trattoria` → `trattoria_master`, `trattoria_planning`, `trattoria_team` |

## E. Budget and contact for the build

| # | Question | Why |
|---|---|---|
| 22 | Credit budget for setup and test, and who tops up? | stop rule on budget |
| 23 | Who answers questions during the build, and how fast? | stop-and-ask points |
| 24 | Who logs in as staff for the acceptance test? | browser checks |

## Mapping to the build

| Intake | Where it is used |
|---|---|
| 1, 2, 21 | phase 0 scope names; phase 1 business/site objects |
| 3, 5 | phase 0 scope-own station option values; phase 1 stations and templates |
| 8, 9, 13 | phase 0 rights matrix; phase 3 accounts |
| 13a | phase 0 master person fields; phase 1 `sp_staff_create` |
| 10, 11, 12 | phase 1 people, qualification links; phase 4 payroll view |
| 14, 15, 16 | phases 2–4 |
| 6, 18 | country module (e.g. [country-de.md](country-de.md)) |
| 19, 20 | all labels and names |

**Station and other option values:** option values are plain strings (no i18n). Create
**scope-specific** property definitions in the customer scopes with **English** values
taken from this intake (stations from question 3, contract types from 11, and the
status/kind sets in phase 0). Do not build on the platform's German defaults.
Rule for each answer: one English camelCase value (ASCII, starts lower case, no
spaces — "Front desk" → `frontDesk`); the name the business uses becomes the option
**label** in the label language of question 19. Full list of option fields:
[phase0.md](phase0.md) §1.4, "Option overrides".
