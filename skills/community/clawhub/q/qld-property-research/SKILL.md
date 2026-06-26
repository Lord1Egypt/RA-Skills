---
name: qld-property-research
description: Detailed Queensland property due-diligence for a single street address using official sources only. Use when an agent needs to research a Queensland property beyond listing basics, including flood-map checks, nearest train-station access, main-road proximity, or a structured property report with cited findings and a composite suitability score.
metadata: {"openclaw":{"primaryEnv":"ORS_API_KEY"}}
---

# QLD Property Research

## Overview

Research one Queensland property at a time and return a structured Markdown report. Prioritise SEQ coverage, with strongest support in Brisbane, Moreton Bay, Logan, and Sunshine Coast, and best-effort support elsewhere in Queensland.

Read [references/methodology.md](references/methodology.md) for the scoring model, report template, and required wording. Read [references/official-sources.md](references/official-sources.md) for the source hierarchy and council coverage rules.
Read [references/openrouteservice.md](references/openrouteservice.md) before doing train routing. Use [scripts/ors_walk_route.py](scripts/ors_walk_route.py) for repeatable walking-route requests.
For Brisbane flood checks, prefer [scripts/brisbane_flood_check.py](scripts/brisbane_flood_check.py) before opening any browser-based flood UI.
For NBN infrastructure type, use [scripts/nbn_infrastructure_check.py](scripts/nbn_infrastructure_check.py) against the official NBN address-check services before opening the browser UI.

## Workflow

1. Validate the request.
   - Expect one full Queensland street address.
   - If the address is incomplete or ambiguous, ask for suburb and postcode before researching.
   - If the property is outside Queensland, stop and say this skill is out of scope.

2. Confirm coverage before scoring.
   - Check the address against the source hierarchy in [references/official-sources.md](references/official-sources.md).
   - State which council or statewide sources are being used.
   - If the address falls into a weak-coverage area, continue with a partial report and mark unsupported sections clearly.

3. Gather official evidence only.
   - Use current official council, Queensland Government, Translink, Queensland Rail, and NBN Co sources.
   - Browse current pages before relying on them because transport apps, council map tools, and flood portals change over time.
   - Do not use real-estate portals or generic map sites for core findings.
   - Third-party routing is allowed only for the train walking route. Use openrouteservice for that step.
   - Minimise browser dependency. For Brisbane flood checks, use the direct service script first and fall back to the browser only when the script cannot support the address.
   - For NBN checks, use the NBN script first and treat the public check-address browser page as the fallback.

4. Produce the informational NBN finding.
   - Run `scripts/nbn_infrastructure_check.py --address "<full address>"`.
   - Use `nbn.premises_technology` as the primary infrastructure result.
   - If `nbn.premises_technology` and `nbn.serving_area_technology` differ, mention both and treat the premises technology as the property-specific answer.
   - Keep NBN informational only. It does not change the composite score unless the user explicitly asks for a revised scoring model.

5. Produce the three section scores.
   - Flood: use the official property map or report and map the result to the flood subscore.
   - Main-road proximity: use official major-road evidence only and score distance to the closest qualifying corridor.
   - Train access: identify the nearest train station from official transport sources, then use openrouteservice walking directions plus the fixed crossing penalty from [references/methodology.md](references/methodology.md).

6. Write the report.
   - Follow the exact section order in [references/methodology.md](references/methodology.md).
   - Include links and concise cited findings in each supported section.
   - Emit the composite score only when flood, main-road proximity, and train access are all supported by official evidence.

## Operating Rules

- Prefer the most property-specific official source available for flood findings.
- Treat "not in a mapped flood area" as lower mapped risk, not a guarantee of no flood risk.
- Keep flood and main-road findings on official sources even when train routing uses openrouteservice.
- Use the openrouteservice route distance and duration as the base train-access evidence when a route is returned.
- Use the NBN `addressDetail.techType` result as the primary infrastructure type because it is the premises-level value returned by the official service.
- Penalise only crossings that materially interrupt the likely practical route to the nearest station entry.
- If one of the three scored sections is unsupported, keep the report partial and omit the composite score.
- Keep the tone factual and caveated. Do not overstate precision.

## Output Standard

Return a structured Markdown report with these headings:

```md
## Address / Coverage
## NBN Infrastructure
## Flood
## Main Road Proximity
## Train Access
## Composite Score
## Sources
```

When the report is partial, still include all headings but mark unsupported sections as `Unsupported with current official data`. The NBN section should still be included even though it does not feed the composite score.
