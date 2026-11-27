# Intake — what to ask the business before you build

Send these questions to the business (owner or manager) and get written answers.
Do not start phase 0 with gaps in sections **A, B, D and E**. Section **C** may be
completed before phase 1 if A/B/D/E are already closed.
ExampleWorks answers below are **examples**; never use them as defaults for a real
customer.

Answers are kept in a short intake record (plain text or a comment on the business
object once it exists). Staff personal data never goes into chat logs or public places.

If [shift-planning](../../shift-planning/references/intake.md) was already answered
for this business, reuse those answers for the legal name, sites, people, label
language, slug, budget contact and time zone. Ask only what is new here.

## A. Business and structure

| # | Question | Why | Example answer |
|---|---|---|---|
| 1 | Name of the business (legal and short name)? Already has shift-planning scopes? | `organisation`, scope slug, reuse of `_master` | "ExampleWorks GmbH", short `exampleworks`; master already exists |
| 2 | Sites (addresses)? One or several? Is the asset list kept per site? | one `building` per site | one site |
| 3 | Which asset classes are in scope (vehicles, devices, tools, machines)? | types to activate on `_master` | two vehicles, portable devices, a ladder and fire extinguishers as `tool`, one heating plant as `machine` |
| 4 | Is there an external contractor to record as an organisation? | a second `organisation` on master, basic name only | one maintenance contractor, name only; no commercial terms on master |
| 5 | Country / region and time zone? | country module, time handling | Germany, Europe/Berlin. **Not Europe/Berlin → stop** and file `ontouser_service_request`. |
| 6 | Who maintains the asset list and the inspection duties? | phase 1 rights | the manager |

## B. People and roles

| # | Question | Why | Example answer |
|---|---|---|---|
| 7 | **Who is the manager** with full rights? Human, agent, or both? | rights matrix | owner + one agent |
| 8 | People who should appear as persons on master (name, login e-mail, site). Reuse shift-planning persons where they are the same people. | `person` | one named inspector record; manager path is the path this skill measures |
| 9 | **Visible on master:** names of people, sites and assets. Is that acceptable? | E2 on master | yes for names and identifiers; no contractor prices or private data |

## C. Rules and process

| # | Question | Why | Example answer |
|---|---|---|---|
| 10 | For each inspection kind: calendar interval in days? Also a kilometre interval on some vehicle duties? | `kind`, `intervalDays`, optional `intervalKm` | see the kinds in phase 0; oil change 365 days and 15 000 km |
| 11 | Who records an inspection, and who reports a defect? | labels and training; this skill describes the manager path | the manager records inspections and may report defects |
| 12 | After a failed inspection, should someone also file a defect order (`report_defect`)? | `record_inspection` with `result=defect` does not create a second order | yes, report the defect on the asset in a separate step |

## D. Naming and language

| # | Question | Why | Example answer |
|---|---|---|---|
| 13 | **Label language** for staff-facing texts (views, buttons)? | labels, country module | German |
| 14 | **Naming pattern** for assets and inspection orders? | readable lists | asset `VEH-<n>` / device name; order `<kind> <asset>` |
| 15 | Scope slug (lower case `a-z0-9_`; the scope name may have 30 characters and `_maintenance` takes 12, so the slug has **at most 18**)? If shift-planning already used a slug, keep it and only add `_maintenance`. | scope names | `exampleworks` → `exampleworks_master`, `exampleworks_maintenance`, `exampleworks_team` |

## E. Budget and contact for the build

| # | Question | Why |
|---|---|---|
| 16 | Credit budget for setup and test, and who tops up? | stop rule on budget |
| 17 | Who answers questions during the build, and how fast? | stop-and-ask points |
| 18 | Who logs in as the manager for the acceptance test? | browser checks on the manager path |

## Mapping to the build

| Intake | Where it is used |
|---|---|
| 1, 2, 15 | phase 0 scope names; phase 1 business/site objects (reuse if present) |
| 3, 4, 14 | phase 1 assets and names |
| 7, 8, 11 | phase 0 rights; phase 1 people |
| 10, 12 | phase 1 service orders; phase 2 forms, function, triggers and actions |
| 5 | country module (e.g. [country-de.md](country-de.md)) |
| 13, 14 | all labels and names |
| 16–18 | measurement and acceptance |

**Option values:** create **scope-specific** property definitions for any new
option list you introduce, with **English** values (`pass`, `defect`,
`scheduledInspection`, `inspectionProtocol`, `oilChange`, …). The name the business uses becomes the
option **label** in the language of question 13 (see [country-de.md](country-de.md)).
