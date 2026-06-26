---
name: Texas
slug: texas
version: 1.0.0
homepage: https://clawic.com/skills/texas
description: Navigate Texas for living, moving, working, and road trips with region fit, state rules, weather risk, and daily logistics.
changelog: "Initial release with resident-first Texas guidance, regional tradeoffs, and practical state-level logistics."
metadata: {"clawdbot":{"emoji":"🤠","requires":{"bins":[],"config":["~/texas/"]},"os":["linux","darwin","win32"],"configPaths":["~/texas/"]}}
---

## When to Use

User needs Texas-specific guidance that generic U.S. advice usually gets wrong: choosing a metro, moving, driving, taxes, weather prep, family logistics, small business setup, or road trip execution.

This skill should activate for four modes: visiting, moving to Texas, living in Texas, and operating a Texas-based business.

## Architecture

This skill works statelessly for one-off Texas questions. If the user wants continuity across sessions, memory lives in `~/texas/`. If `~/texas/` does not exist, read `setup.md`, explain planned local storage in plain language, and ask for confirmation before creating files. See `memory-template.md` for structure.

```text
~/texas/
└── memory.md     # User context, region, timelines, constraints, and open loops
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Region fit and metro tradeoffs | `regions.md` |
| Move-in sequence and admin checklist | `moving-and-settling.md` |
| License, registration, tolls, and vehicles | `texas-dmv-and-vehicles.md` |
| Renting, buying, property tax, and flood risk | `housing-and-property.md` |
| Power, water, internet, and recurring bills | `utilities-and-bills.md` |
| Taxes, insurance pressure, and cost reality | `costs-and-taxes.md` |
| Heat, storms, freezes, outages, and prep | `weather-and-emergencies.md` |
| Laws, scams, and practical safety | `laws-and-safety.md` |
| Schools, childcare, and family planning | `family-and-schools.md` |
| Health insurance, urgent care, and care access | `healthcare-and-insurance.md` |
| Jobs, LLC setup, sales tax, and compliance | `work-and-business.md` |
| Road trips, visiting, and city-hopping | `road-trips-and-visiting.md` |
| Official sources map | `sources.md` |

## Core Rules

### 1. Classify the User Before Giving Advice
- Decide which Texas mode applies first: visitor, future resident, current resident, or business operator.
- Then anchor the answer to the user's region, metro, county, ZIP, and school district when those variables change the recommendation.
- If that context is missing, ask for it before pretending Texas is uniform.

### 2. Separate State Rules from Local Reality
- Texas-level rules are only the first layer. City, county, appraisal district, utility territory, school district, and flood zone often change the real answer.
- Always label which parts are statewide and which parts must be verified locally.
- For address-specific questions, prefer official portals over memory or generic summaries.

### 3. Distances and Drive Time Beat Map Intuition
- Texas plans fail when users underestimate distance, tolls, fatigue, weather, and event traffic.
- For both relocation and travel, convert geography into realistic drive-time, airport, and corridor tradeoffs.
- Never recommend same-day overstuffed plans just because destinations look close on a map.

### 4. Texas Cost Reality Is Broader Than "No State Income Tax"
- Include housing, property tax pressure, insurance, toll roads, summer power bills, car dependence, and weather-driven costs.
- For homeowners and businesses, mention appraisal, deductible, flood, hail, and outage exposure when relevant.
- Use `costs-and-taxes.md` before saying a place is "cheap."

### 5. Weather and Grid Risk Change Good Advice
- Heat, flood, hail, hurricanes, tornadoes, wildfire smoke, and winter freezes are not edge cases.
- Adjust moving plans, road trips, home choice, and seasonal recommendations around actual hazard exposure.
- When weather is part of the problem, lead with readiness and fallback plans, not brochure copy.

### 6. Deliver Checklists, Not Tourism Copy
- Texas users usually need deadlines, documents, portals, sequence, and tradeoffs.
- For administrative questions, answer in the form "do this today / this week / later" whenever possible.
- For destination questions, show why one base city or region fits better than another.
- Before creating or changing local files in `~/texas/`, explain the planned write and ask for confirmation.

### 7. Use Official Sources for Unstable Rules
- License rules, registration steps, sales tax, homestead details, district lookups, and emergency guidance can change.
- Verify current information from the official state or local source before giving precise compliance steps.
- If current verification is blocked, say so plainly and avoid false precision.

## Common Traps

- Treating Texas like one market instead of multiple different metros and risk zones.
- Recommending a neighborhood or suburb without checking commute shape, flood exposure, and school district.
- Saying "no state income tax" while ignoring property tax, insurance, tolls, and electricity spikes.
- Mixing up Texas DPS, TxDMV, county tax offices, appraisal districts, and city utilities.
- Planning a road trip by miles instead of daylight, heat, event traffic, and fuel gaps.
- Giving housing advice without mentioning HOA, wind or hail exposure, and renter or owner insurance gaps.
- Using U.S.-generic legal guidance for cannabis, DWI, landlord-tenant, or permit questions.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.texas.gov | Page requests only unless user explicitly wants form guidance | State service portal and resident tasks |
| https://www.dps.texas.gov | Page requests only unless user explicitly provides personal case details | Driver license and ID rules |
| https://www.txdmv.gov | Page requests only unless user explicitly wants vehicle workflow help | Vehicle title, registration, and county office guidance |
| https://comptroller.texas.gov | Page requests only unless user explicitly wants tax-specific guidance | Sales tax, franchise tax, property tax resources |
| https://tea.texas.gov | ZIP, city, district, or school references if the user asks for school matching | School district and education framework |
| https://www.texasready.gov | Page requests only | Emergency preparedness and hazard planning |
| https://powertochoose.org | ZIP if the user asks to compare electric plans in deregulated areas | Electricity market lookup |

No other data is sent externally.

## Security & Privacy

**Data that may leave your machine:**
- Public page requests to official Texas or utility-choice sites
- ZIP, city, county, or district data only when the user asks for location-specific guidance

**Data that stays local:**
- Region preference, move timeline, family constraints, vehicle notes, and open tasks in `~/texas/`

**This skill does NOT:**
- Submit government forms on the user's behalf without explicit instruction
- Store credentials, SSNs, or payment information in local memory
- Assume local rules when the answer depends on a city, county, or district

## Trust

By using this skill, location details such as ZIP, county, or district may be checked against official Texas or local-government websites when the user asks for precise guidance.

Only install if you trust those public services with that lookup context.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General itinerary design and travel planning structure
- `car-rental` — Rental car, pickup, and handoff decisions for Texas trips
- `booking` — Reservation workflows for flights, hotels, and schedule holds
- `business` — Broader business operations guidance beyond Texas-specific rules
- `health-insurance` — Deeper insurance-plan comparison and terminology support

## Feedback

- If useful: `clawhub star texas`
- Stay updated: `clawhub sync`
