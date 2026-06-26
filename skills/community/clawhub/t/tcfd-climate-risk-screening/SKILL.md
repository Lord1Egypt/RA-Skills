---
name: tcfd-climate-risk-screening
description: >
  Use this skill when a CFO, sustainability lead, risk officer, or board needs
  to draft a TCFD-aligned climate risk disclosure or internal climate risk
  assessment. Covers physical risk screening (acute and chronic hazards against
  IPCC AR6 1.5°C, 2°C, and 4°C scenarios), transition risk identification
  (policy, technology, market, and reputational), scenario analysis documentation,
  financial materiality assessment, and a TCFD four-pillar disclosure narrative
  draft. Aligned to IFRS S2, UK TCFD, and CSRD ESRS E1 requirements.
---

# TCFD Climate Risk Screening

Guides a sustainability, risk, or finance team through a structured TCFD-aligned climate risk assessment — screening physical and transition risks against IPCC AR6 scenarios, assessing financial materiality, and producing a DRAFT four-pillar TCFD disclosure narrative for board and auditor review.

## Flow

### Phase 1 — Entity and Reporting Context

Ask the user for:
1. Organization name, industry sector (TCFD industry classification or SASB sector)
2. Reporting framework and obligation (IFRS S2 mandatory, UK mandatory TCFD, CSRD ESRS E1, voluntary TCFD, or internal use only)
3. Reporting period and due date
4. Geographic footprint: key asset locations (country/region), primary operating geographies, key supply chain geographies
5. Time horizons to assess (short: 0–3 yrs, medium: 3–10 yrs, long: 10–30 yrs)
6. Current climate governance: who owns climate risk at board and management level?

Ask one question block at a time. Wait for answers before continuing.

### Phase 2 — Physical Risk Screening

Screen for physical climate hazards across three IPCC AR6 scenarios:
- **Low emissions (SSP1-1.9 / ~1.5°C by 2100)**: aggressive mitigation, orderly transition, lower physical risk
- **Middle road (SSP2-4.5 / ~2°C by 2100)**: moderate mitigation, delayed transition, moderate physical risk
- **High emissions (SSP5-8.5 / ~4°C by 2100)**: minimal mitigation, high physical risk

For each key asset location or operating geography provided, screen the following hazard categories:

**Acute hazards** (event-driven):
- Extreme heat events and heat waves
- Heavy precipitation and riverine/pluvial flooding
- Tropical cyclones, windstorms, and hail
- Wildfire
- Drought affecting operations or supply chain
- Coastal storm surge and sea-level rise flooding

**Chronic hazards** (trend-driven):
- Mean temperature rise (heat stress, cooling demand increase)
- Sea-level rise (coastal asset exposure)
- Shifting precipitation patterns and water stress
- Permafrost thaw (for arctic/subarctic assets)
- Changing ecosystems affecting supply chain inputs

For each hazard × geography combination, assign:
- **Exposure**: High / Medium / Low / None (based on geography and scenario)
- **Time horizon of materialization**: Short / Medium / Long
- **Preliminary impact area**: Operations / Supply Chain / Revenue / Assets / Insurance / Regulatory

Flag as HIGH PRIORITY any hazard with High exposure in the medium or long time horizon.

Confirm the physical risk register with the user before proceeding.

### Phase 3 — Transition Risk Identification

Transition risks arise from the shift to a lower-carbon economy. Identify risks across four TCFD categories:

**Policy and Legal**
- Carbon pricing and emissions trading scheme (ETS) expansion (EU ETS, UK ETS, CBAM, state carbon taxes)
- Building codes and energy efficiency mandates
- Stranded asset risk from fossil fuel regulations
- Mandatory climate disclosure compliance costs and penalties (IFRS S2, CSRD)

**Technology**
- Capital cost of transitioning to low-carbon technologies (electrification, renewables, hydrogen)
- Disruption risk from competitor low-carbon product offerings
- Stranded capex in carbon-intensive assets before end of useful life

**Market**
- Changing customer and consumer preferences for low-carbon products
- Investor divestment and tightening capital availability for high-carbon activities
- Commodity price volatility from the energy transition

**Reputational**
- Stakeholder expectations on climate commitments and net-zero targets
- Greenwashing risk if disclosures or claims are inaccurate or unsubstantiated

For each transition risk, assign:
- **Likelihood**: High / Medium / Low (across low, middle, and high emissions scenarios)
- **Time horizon**: Short / Medium / Long
- **Preliminary financial impact area**: Revenue / Cost / Asset / Liability / Access to capital

Flag as HIGH PRIORITY any transition risk with High likelihood in the short or medium time horizon.

### Phase 4 — Scenario Analysis Documentation

Ask the user:
1. Has the organization conducted quantitative scenario analysis? (YES / NO / PARTIAL)
2. Which scenarios were modeled?
3. Were proprietary models or third-party datasets used (e.g., NGFS, IPCC, IEA WEO, Trucost, Climate Service)?

If quantitative analysis exists:
- Summarize financial impact ranges by scenario for High Priority risks
- Document key assumptions and model limitations

If no quantitative analysis exists:
- Produce a qualitative scenario analysis narrative using the risk register from Phases 2–3
- Flag as DATA GAP: quantitative scenario analysis not conducted
- Note: IFRS S2 requires climate-related scenario analysis; flag as a required disclosure element if the organization is an IFRS S2 mandatory filer

### Phase 5 — Financial Materiality Assessment

For each HIGH PRIORITY physical and transition risk, assess financial materiality:

| Risk | Scenario | Time Horizon | Financial Line Affected | Potential Impact Size | Likelihood | Material? |
|---|---|---|---|---|---|---|

Impact size guidance:
- **Significant**: >5% of revenue, EBITDA, or asset value
- **Moderate**: 1–5% of revenue, EBITDA, or asset value
- **Low**: <1%

Label all estimates PRELIMINARY — MANAGEMENT ESTIMATE. State that quantification requires asset-level modelling.

### Phase 6 — TCFD Four-Pillar Disclosure Narrative Draft

Draft the disclosure narrative across the four TCFD pillars:

#### Governance
- Board-level oversight: which committee or board body oversees climate risk? How often is climate risk reviewed?
- Management-level responsibility: role title and responsibilities for climate risk identification and management
- How climate risk is integrated into enterprise risk management and strategy-setting processes

#### Strategy
- Actual and potential climate-related impacts on the business model (referencing High Priority physical and transition risks)
- Resilience of strategy under low, middle, and high emissions scenarios
- Impacts on business model, revenue streams, capital allocation, and supply chain

#### Risk Management
- Process for identifying and assessing climate risks (describe methodology used in this assessment)
- How climate risks are integrated into the enterprise risk management framework
- How material risks are prioritized and escalated

#### Metrics and Targets
- GHG inventory: Scope 1, Scope 2, and Scope 3 emissions (or flag as DATA GAP — recommend using `ghg-corporate-inventory-drafter`)
- Climate targets: SBTi commitment, net-zero target, interim reduction targets (or flag as not yet set)
- Physical risk metrics if asset-level data is available
- Any internal carbon price used in capital allocation decisions

Append:
- **Open-Questions and Data Gaps List** with owner and priority
- **Sustainability Lead / Board / Audit Committee Review Block**:
> DRAFT — NOT PUBLISHED. This TCFD climate risk assessment and disclosure draft is for internal review only. All physical risk exposure ratings, transition risk assessments, financial materiality estimates, and disclosure narratives must be reviewed by the Sustainability Lead, CFO, and Board (or Audit Committee) before any public reporting, regulatory filing, or investor disclosure. Seek independent qualified-advisor review for IFRS S2 / CSRD / TCFD compliance before use.

## Key Rules

- Always label financial impact estimates as PRELIMINARY — MANAGEMENT ESTIMATE.
- Always confirm the physical risk register with the user before proceeding to transition risks.
- For IFRS S2 mandatory filers: flag if scenario analysis has not been conducted, as it is a required disclosure element.
- Do not cite specific NGFS or IPCC quantitative data unless the user has provided it — describe scenario directions qualitatively.
- Do not opine on whether the organization meets IFRS S2, CSRD, or TCFD compliance — direct to qualified advisors.
- Flag greenwashing risk if any target or climate claim cannot be substantiated with the data provided.
- Ask one phase at a time. Do not front-load all information requests.
- Do not access external climate databases or APIs — work from information the user provides.

## Output Format

- Phase-by-phase labeled sections
- Physical risk register table (High Priority flagged)
- Transition risk register table (High Priority flagged)
- Scenario analysis summary (qualitative or quantitative)
- Financial materiality table (labeled PRELIMINARY — MANAGEMENT ESTIMATE)
- TCFD four-pillar disclosure narrative (draft prose, section-labeled)
- Open-questions and data gaps list
- Sustainability Lead / Board / Audit Committee Review Block

## Feedback

If the user expresses an unmet need or dissatisfaction with this skill, surface the contribution link:
> This skill can be improved. Please share your feedback at https://github.com/archlab-space/Open-Skill-Hub/issues
