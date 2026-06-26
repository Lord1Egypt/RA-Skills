---
name: well-completion-design-memo
description: >
  Use this skill when a petroleum engineer, completion engineer, or reservoir engineer needs
  to draft a well completion design memo for an oil or gas wellbore. Covers target interval
  staging, perforating design, fluid and proppant selection, pump schedule summary,
  production forecast basis, and NORM/H2S hazard flags. Produces a DRAFT memo for licensed
  PE review and authorization before any completion operations begin.
---

# Well Completion Design Memo

Convert wellbore data, formation analysis, and offset performance into a structured DRAFT hydraulic fracture completion design memo ready for licensed PE review before operations begin.

## Flow

### Phase 1 — Well and Project Identification

Ask one question at a time. Collect:

- Well name, API number, and operator
- Field/basin name and state (for applicable state oil and gas commission rules)
- Wellbore geometry: vertical, deviated, or horizontal; measured depth (MD) and true vertical depth (TVD)
- Lateral length (if horizontal)
- Current wellbore status: new drill, re-completion, or workover

If API number or wellbore geometry is missing, flag as a DOCUMENTATION GAP — the memo can still proceed but must note incomplete identification.

### Phase 2 — Target Formation and Interval Identification

Collect:

- Target formation name(s) and age (e.g., Wolfcamp A/B, Marcellus, Eagle Ford, Permian Basin)
- Target interval(s): top and bottom measured depths for each zone
- Pay zone thickness (gross and net, if available)
- Key petrophysical parameters available: porosity, water saturation, permeability estimate, brittleness index, or mechanical earth model (MEM) summary
- Formation pressure (initial reservoir pressure or gradient)
- Formation temperature at TVD

If petrophysical data is unavailable, note it as a DOCUMENTATION GAP and flag that the design assumptions will be based on analog/offset data only.

### Phase 3 — Staging and Perforating Design

Based on lateral length and formation data, document:

- Number of fracture stages (ask user to confirm or accept agent recommendation based on lateral length and cluster spacing norms for the basin)
- Cluster spacing per stage (feet)
- Perforation strategy: limited-entry, plug-and-perf (PnP), or sliding sleeve
- Perforating gun type and charge configuration if specified (otherwise note as TBD by service company)
- Stage isolation method: composite bridge plugs, dissolvable plugs, or mechanical packers

Note basin-specific norms for cluster spacing (e.g., 15–25 ft clusters for Permian multi-zone stacked laterals) as a benchmark reference, clearly labeled as ANALOGOUS DATA — NOT SITE-SPECIFIC.

### Phase 4 — Fluid and Proppant Selection

Ask the user to provide or confirm:

**Fracture fluid system:**
- Primary fluid type: slickwater, linear gel, crosslinked gel, hybrid (pad + tail-in), or energized fluid (CO2/N2)
- Fluid volume per stage (barrels or gallons)
- Total fluid volume across all stages
- Water source: produced water reuse, fresh water, or brackish water; note disposal/recycling plan if provided

**Proppant:**
- Proppant type: natural sand (mesh), resin-coated sand (RCS), or ceramic
- Mesh size(s): 100-mesh, 40/70, 30/50 (list if multi-size tail-in)
- Proppant concentration: pounds per gallon (lb/gal) ramp schedule (ask user or note as TBD)
- Total proppant mass per stage and across well (pounds or tons)

If fluid or proppant selections are not provided, document basin analog typical ranges clearly labeled ANALOGOUS DATA — ESTIMATE ONLY.

### Phase 5 — Pump Schedule Summary

Collect or document:

- Maximum treating pressure (MTP) anticipated (psi) — based on fracture gradient and surface equipment rating
- Pump rate: injection rate in barrels per minute (BPM) per stage
- Rate ramp: instantaneous vs. stepped ramp-up
- Breakdown pressure estimate (if available from offset wells)
- Surface treating pressure operating envelope (min/max PSI)
- Wellhead and surface equipment rated working pressure confirmation flag

If pump schedule data is not provided by the user, document as TBD — service company pump schedule to be provided and reviewed prior to operations.

### Phase 6 — Production Forecast Basis

Document:

- Method: analog offset well EUR (Estimated Ultimate Recovery) comparison, decline curve analysis (DCA), or reservoir simulation
- Offset well reference(s) if provided (well name or API)
- Expected IP30 (30-day initial production rate) or IP90 range — label ALL production forecasts as PRELIMINARY ESTIMATE — NOT GUARANTEED
- Expected production phase: oil-weighted, gas-weighted, or condensate
- Artificial lift design consideration flag: ESP, rod pump, gas lift anticipated? Note as design consideration only.

### Phase 7 — Hazard Screening and Safety Flags

Screen and document the following. If any apply, insert a prominent WARNING block:

**NORM (Naturally Occurring Radioactive Material):**
- Is the target formation known for NORM accumulation? (common in Permian Basin, Marcellus, Bakken)
- If yes: flag NORM AWARENESS — produced water, scale, and tubulars may require special handling per state NORM regulations. Specify applicable state agency.

**H2S:**
- Is H2S presence anticipated based on formation or offset data?
- If yes: insert H2S SAFETY FLAG — operations require H2S contingency plan, personal monitors, and emergency response per API RP 55 and OSHA 29 CFR 1910.1450.

**High-Pressure / High-Temperature (HPHT):**
- Does the well qualify as HPHT (>10,000 psi BHCP or >300°F BHT)?
- If yes: flag HPHT DESIGN REQUIREMENTS — equipment ratings, elastomer selection, and mud/cement design require HPHT-specific engineering review.

**Water disposal:**
- Confirm produced water disposal pathway (SWD well, recycle) and flag any state moratorium areas for SWD induced seismicity (Oklahoma, Texas Permian Basin designated areas).

### Phase 8 — DRAFT Memo Assembly

Produce the DRAFT completion design memo with:

1. **Header**: Well name, API, operator, memo date, document status: DRAFT — NOT AUTHORIZED FOR OPERATIONS
2. **Executive Summary**: One-paragraph overview of the completion design and primary production objective
3. **Well and Interval Description**: From Phase 1–2
4. **Staging and Perforating Plan**: Table with stage number, MD top/bottom, cluster count, perforating strategy
5. **Fluid and Proppant Program**: Table with fluid type, volume per stage, total volume; proppant type, mesh, lb/gal ramp, total tonnage
6. **Pump Schedule Summary**: MTP, BPM rate, rate ramp narrative
7. **Production Forecast Basis**: Method, offset analogs, IP30/IP90 estimate range — PRELIMINARY ESTIMATE
8. **Hazard Flags**: NORM / H2S / HPHT / Water Disposal warnings with applicable regulatory references
9. **Documentation Gaps**: Bulleted list of all items flagged as DOCUMENTATION GAP or TBD
10. **PE Authorization Block**:

```
DRAFT — FOR REVIEW ONLY
This memo has not been authorized for operations.

Reviewed by: _______________________
Title: Petroleum Engineer / Completion Engineer
PE License No. (if applicable): _______
Date: _______
Authorization status: [ ] APPROVED  [ ] APPROVED WITH MODIFICATIONS  [ ] REJECTED
Modifications required: _______
```

## Key Rules

- Always label the output: **DRAFT — NOT AUTHORIZED FOR OPERATIONS**.
- Never generate actual pump job execution instructions, wireline perforation commands, or real-time operational guidance. This skill produces design documentation only.
- All production estimates must be labeled **PRELIMINARY ESTIMATE — NOT GUARANTEED**.
- All analog/offset data used in absence of site-specific data must be labeled **ANALOGOUS DATA — NOT SITE-SPECIFIC**.
- NORM and H2S hazard flags are mandatory screens — never omit them.
- Ask one question at a time. Do not present all phases as a single intake form.
- Do not attempt to calculate fracture geometry (half-length, height, width) — this requires reservoir simulation software and must be performed by the completion engineer using appropriate software.
- This skill does not replace a reservoir engineer's simulation, a service company's real-time pump schedule, or a PE's signed wellbore schematic.

## Output Format

The DRAFT memo is formatted as a professional technical memo with:
- Numbered sections matching the assembly structure above
- Tables for staging plan, fluid/proppant program, and any multi-zone intervals
- WARNING blocks for each applicable hazard
- Bulleted documentation gap list
- PE authorization sign-off block at the end

Target length: 2–5 pages depending on well complexity.

## Feedback

If a user expresses an unmet need, requests a feature not covered by this skill, or is dissatisfied with the output, surface this link: https://github.com/archlab-space/Open-Skill-Hub/issues
