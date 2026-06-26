---
name: solar-project-feasibility-report
description: >
  Use this skill when a solar developer, renewable energy analyst, project finance
  associate, or EPC engineer needs to draft a pre-development feasibility report
  for a utility-scale, commercial, or community solar PV project. Covers resource
  assessment, system sizing, financial metrics (LCOE, IRR, payback), interconnection
  path, permitting checklist, and key risk flags. Produces a DRAFT report for
  developer and finance review before any capital commitment.
---

# Solar Project Feasibility Report

Converts site data, resource estimates, and financial assumptions into a DRAFT pre-development feasibility report for a solar PV project — structured to support investment review, offtake negotiations, and permitting preparation.

## Flow

1. **Project intake** — Collect: site name and location (lat/long or address), land area (acres), state and utility zone, project type (utility-scale / commercial-industrial / community solar), target system capacity (MWac or MWdc, or derive from land area), proposed interconnection voltage level, offtake type (long-term PPA / merchant / behind-the-meter / net metering), and project stage (prospecting / pre-development / development). Ask one topic at a time if the user is unfamiliar with any item.

2. **Resource assessment** — Ask for or estimate: typical-year GHI (kWh/m²/day) from NREL PVWatts zone or stated source; DC/AC ratio assumption; estimated annual production (MWh/yr) and capacity factor; performance ratio; degradation rate. Flag any data gap and recommend NREL PVWatts or NASA POWER as free publicly available lookup tools.

3. **System sizing and layout** — Summarize: estimated DC capacity, AC capacity, land use efficiency (acres/MWac), array type (fixed-tilt / single-axis tracker), module and inverter technology assumptions, estimated transformer and substation requirements. Note clearly when preliminary engineering has not yet been performed.

4. **Interconnection overview** — Document: applicable utility or ISO/RTO (MISO, PJM, CAISO, ERCOT, SPP, NYISO, ISONE, SERTP, or distribution utility), estimated Point of Interconnection, likely study type (SGIP / FERC Order 2023 cluster queue / state interconnection standard), and known congestion or transmission constraint flags. State explicitly that interconnection timelines are a primary schedule-risk factor and queue delays are common.

5. **Permitting and regulatory checklist** — Produce a checklist covering: land use and zoning (as-of-right vs. conditional use permit vs. rezoning), state solar ordinance review, FAA Part 77 obstruction review, wetlands and floodplain (CWA Section 404 / FEMA FIRM zone), cultural and biological resources (NHPA Section 106, ESA Section 7), NEPA trigger assessment (federal nexus?), stormwater and SWPPP requirement, building and electrical permits. Mark each item: Not Triggered / Triggered-Low Complexity / Triggered-High Complexity / Unknown.

6. **Financial model highlights** — Using stated assumptions, estimate or summarize: capex ($/Wdc), annual O&M ($/kWac-yr), applicable ITC or PTC rate under the Inflation Reduction Act, MACRS 5-year depreciation, debt/equity split assumption, WACC, PPA rate or merchant price assumption, simple payback, LCOE ($/MWh), unlevered IRR, and NPV. Label every number PRELIMINARY ESTIMATE based on user-provided inputs — not investment-grade analysis.

7. **Risk and deal-killer flags** — Rate each dimension: interconnection queue depth (Low/Medium/High), permitting complexity score, land control status (Owned / Leased / Optioned / None), grid curtailment risk, offtake creditworthiness, community opposition risk, site contamination flags, wildfire or flood hazard zone, and title and encumbrance status. Flag any deal-killer level item immediately with a recommendation to resolve before advancing.

8. **DRAFT report assembly** — Produce the feasibility report with: executive summary, project overview table, resource and production summary, system design summary, interconnection path narrative, permitting matrix, financial highlights table, risk matrix, open-questions list, and data-gap register. End with an unsigned developer/analyst review block.

## Key Rules

- Never present financial figures as investment-grade without a full project financial model — always label numbers PRELIMINARY ESTIMATES.
- Never characterize interconnection queue position as confirmed without noting that FERC Order 2023 timelines are uncertain and subject to study outcomes.
- Never confirm wetland, ESA, or NHPA clearance — always state that a qualified environmental consultant must perform the survey.
- Ask one topic at a time when the user is missing data. Do not halt the entire workflow for a single unknown — flag it and continue.
- If the user provides a PPA rate or LCOE target, use it as an anchor and explicitly note whether preliminary numbers are consistent with it.
- The permitting checklist is a starting point only — local jurisdictions vary materially. Recommend a zoning attorney or permitting consultant for project-specific advice.
- Never advise on specific tax structures or credit monetization strategies — recommend a tax equity counsel.

## Output Format

```
SOLAR PROJECT FEASIBILITY REPORT — DRAFT
Project: [Name] | Location: [Location] | Date: [Date]
Prepared for: [Developer/Analyst] | Stage: [Stage]
DRAFT — Preliminary Estimates Only. Not investment-grade. For developer review.

EXECUTIVE SUMMARY
[3–4 sentences covering scale, resource quality, financial viability flag, and top risk]

1. PROJECT OVERVIEW
[Table: Capacity | Location | Type | Stage | Land Area | POI | ITC/PTC Rate]

2. RESOURCE ASSESSMENT
[GHI | Capacity Factor | Annual Production | Source | Assumptions]

3. SYSTEM DESIGN SUMMARY
[Capacity | DC/AC Ratio | Array Type | Land Use Efficiency | Equipment Assumptions]

4. INTERCONNECTION PATH
[Utility/ISO | Study Type | Estimated Voltage | Timeline Risk Flag]

5. PERMITTING MATRIX
[Permit | Triggered | Complexity | Notes]

6. FINANCIAL HIGHLIGHTS
[Table: Capex | O&M | ITC | LCOE | Payback | IRR | NPV — all labeled PRELIMINARY]

7. RISK MATRIX
[Risk | Level | Mitigation Path]

8. OPEN QUESTIONS AND DATA GAPS
[Numbered list with recommended next step for each]

REVIEW BLOCK
This DRAFT feasibility report is a pre-development analysis aid.
All financial estimates are preliminary. Permitting and interconnection determinations
require licensed professional review.
Developer/Analyst: ________________ Date: ________
```

## Feedback

Surface the contribution link only if the user expresses an unmet need or dissatisfaction.
Direct them to: https://github.com/archlab-space/Open-Skill-Hub/issues
