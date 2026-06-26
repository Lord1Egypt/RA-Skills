# SWPPP Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Civil Engineering — Construction Stormwater Compliance

## Purpose

A SWPPP drafting partner for civil engineers, Qualified SWPPP Developers (QSDs), Qualified SWPPP Practitioners (QSPs), erosion-control designers, environmental consultants, and general contractors. Turns the project's location, disturbed acreage, soils, slopes, receiving waters, sequence of construction, and planned BMP set into a DRAFT Stormwater Pollution Prevention Plan (SWPPP) aligned to the **EPA 2022 Construction General Permit (CGP)** — or equivalent state CGP when named by the user — for QSD / QSP / licensed PE review and sign-off before NOI submittal.

## When to Use

- Drafting the SWPPP for a new construction project disturbing ≥ 1 acre (or ≥ a state-CGP smaller threshold) before NOI submittal
- Updating an existing SWPPP after a major design change, sequence change, or operator change
- Producing a small-residential-lot SWPPP under a state's streamlined permit when applicable
- Producing the section-by-section narrative that pairs with site-specific drawings prepared separately by the design engineer
- Standing up the inspection-and-corrective-action recordkeeping framework the QSP will execute in the field

## What It Does

**Phase 1: Intake**
1. Captures the permitting framework (EPA 2022 CGP or the named state CGP), permit number(s), and any small-residential-lot streamlined permit applicability
2. Captures project metadata: project name, owner, operator(s), site address, county, latitude / longitude, NOI status
3. Captures site characteristics: total project area, total area to be disturbed, pre- and post-construction land cover, predominant soil types (NRCS / HSG), slope ranges, sensitive features (wetlands, riparian, karst, threatened-and-endangered species, historic properties), receiving waters with name, classification, and any impairments / TMDLs
4. Captures sequence of construction (clearing → grubbing → grading → utility → vertical → paving → final stabilization), construction start and estimated final-stabilization dates, and phasing
5. Captures planned BMPs the design engineer has already selected, and lists EPA / state-required BMP categories the user must still pick from
6. Captures pollutant sources beyond sediment: concrete-washout, fuel / oil, sanitary, paint / stucco, fertilizer / pesticide, construction debris, dewatering
7. Restates every fact with **Confirmed / Assumed / Unknown** tags before drafting

**Phase 2: BMP design narrative**
8. Builds a BMP selection matrix across **Erosion Control**, **Sediment Control**, **Pollution Prevention / Good Housekeeping**, and **Post-Construction Stormwater Management**
9. Ties each BMP to the site condition (slope, soil, drainage area, sensitive feature) that drove its selection
10. Flags numeric-effluent-limit (NEL) applicability under the 2022 CGP, dewatering-discharge controls, and any 303(d)-listed-water or TMDL-specific requirements

**Phase 3: Operations and recordkeeping**
11. Builds the inspection-and-corrective-action schedule (frequency, qualifying rain event, post-event timing, deadline to implement corrective action)
12. Builds the training plan (operator, QSP, subcontractor) and the signatory block per 40 CFR 122.22
13. Builds the recordkeeping framework (inspection forms, corrective-action log, rain gauge log, BMP installation/removal log, sampling records where required)

**Phase 4: Output**
14. Produces the DRAFT SWPPP using the structure in `SKILL.md`
15. Runs the self-check rubric and lists failures back to the user
16. Produces an "unresolved-information for engineer / QSD" list — items that must be confirmed against site survey, soils report, drawings, or the permit text before sign-off

## Output

A DRAFT SWPPP with:

- Cover page and signatory block (DRAFT — QSD / QSP / LICENSED PE MUST REVIEW)
- Permit framework and project information
- Operator and emergency-contact list
- Site assessment narrative (soils, slopes, drainage, receiving waters, sensitive features)
- Sequence-of-construction table with phasing and stabilization milestones
- BMP selection matrix (Erosion / Sediment / Pollution Prevention / Post-Construction) tied to site conditions
- Inspection-and-corrective-action schedule
- Training and certification plan
- Recordkeeping framework with form references
- Numeric-effluent-limit, dewatering-discharge, and 303(d) / TMDL flags where applicable
- Unresolved-information list (items requiring drawings, survey, soils report, or permit-text confirmation)

## Safety

This skill drafts a **plan for a QSD / QSP / licensed PE to review, modify, sign, and seal**, not a final permit-issued document. Every output is labeled **DRAFT — QSD / QSP / LICENSED PE MUST REVIEW**. The skill never submits an NOI; never signs or seals a SWPPP; never replaces site-specific drawings, calculations, or the registered design professional's seal; never opines on whether a permit will be issued; never substitutes for the operator's responsibility under the permit; never overrides the Authority Having Jurisdiction or state permitting agency. State-CGP language differs from the EPA CGP — the skill will name the framework it used and flag every item that requires the user to confirm against the permit actually in force at the project location.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
