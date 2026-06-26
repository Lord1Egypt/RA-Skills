# QLD Property Research Methodology

## Contents

- Report template
- Flood scoring
- Main-road proximity scoring
- Train access scoring
- Composite score
- Required caveats
- Unsupported-data handling

## Report template

Use this structure for every supported address.

```md
## Address / Coverage
- Address: <normalised address>
- Coverage: <high / medium / limited>
- Council / region: <name>
- Official sources used: <short list>
- Coverage note: <why this is full coverage or partial>

## NBN Infrastructure
- Premises technology: <FTTP / HFC / FTTN / FTTC / FTTB / Fixed Wireless / Satellite / Unsupported>
- Serving-area technology: <if different or useful>
- Service status: <available / planned / other official wording>
- Evidence: <1-2 cited findings from the official nbn source>
- Interpretation: <plain-English meaning and any caveat about premises vs serving-area values>

## Flood
- Result: <short finding>
- Evidence: <1-2 cited findings from the official source>
- Flood subscore: <0-100 or Unsupported>
- Interpretation: <plain-English meaning>

## Main Road Proximity
- Result: <short finding>
- Evidence: <major road name/type and distance band>
- Main-road proximity subscore: <0-100 or Unsupported>
- Interpretation: <plain-English meaning>

## Train Access
- Nearest station: <station name>
- Station entry coordinates: <lat/lon or address>
- Base estimated walk time: <minutes>
- Major road crossings: <count>
- Effective estimated walk time: <minutes>
- Train access subscore: <0-100 or Unsupported>
- Interpretation: <plain-English meaning>

## Composite Score
- Suitability score: <0-100 or Not emitted>
- Weighting: Flood 45%, Main road 30%, Train 25%
- Summary: <1-2 sentence synthesis>

## Sources
- <source label>: <URL>
- <source label>: <URL>
```

Use `Unsupported with current official data` when a section cannot be supported.

## NBN infrastructure

Use the official nbn address-check service for the infrastructure result.

Preferred process:

1. Run `scripts/nbn_infrastructure_check.py --address "<full address>"`.
2. Use `selected_match.formatted_address` to confirm the matched premises.
3. Use `nbn.premises_technology` as the primary result.
4. If `nbn.serving_area_technology` differs, mention it as contextual evidence only.
5. Cite the official nbn check-address page and the property-specific API result surfaced by the script.

Rules:

- Treat `nbn.premises_technology` as the authoritative property-specific technology when present.
- If the premises and serving-area technologies differ, explain that the serving-area value is broader area context.
- Do not convert the NBN section into the composite score unless the user explicitly requests a modified model.
- If the script returns `status: not_found` or no premises technology, mark the section `Unsupported with current official data`.

## Flood scoring

Use the most property-specific official flood source available. If multiple official flood products exist, score the worst supported mapped result for the property.

For Brisbane addresses, run `scripts/brisbane_flood_check.py` first. If it returns structured parcel and layer-hit data, use that result directly instead of manually driving the browser map.

Map the official result to a flood subscore:

| Condition | Flood subscore |
| --- | --- |
| Official property report or map shows no mapped flood affect on the property | 95 |
| Only rare / very low / large-event mapping touches the property, with no medium or high impact indication | 75 |
| Property is affected in a low-to-moderate way, such as lower-likelihood mapping, moderate overland-flow exposure, or a planning trigger without severe wording | 50 |
| Property is clearly affected in a high-likelihood, high-impact, or major-event way, or the report indicates strong flood planning constraints | 20 |

Rules:

- Treat "not mapped" as lower risk, not zero risk.
- If the council uses different terminology, map it to the nearest severity bucket and say that this is an interpretation of the official category.
- If a source only provides historical flood information and no current planning or awareness mapping, mention the limitation and do not convert that alone into a flood subscore.

## Main-road proximity scoring

Use official state-controlled road mapping or official council transport/planning mapping where available.

Score by the closest clear major-road edge to the property:

| Distance to major road | Main-road proximity subscore |
| --- | --- |
| More than 1000m | 95 |
| 500m to 1000m | 80 |
| 250m to 499m | 60 |
| 100m to 249m | 35 |
| Less than 100m | 15 |

Count a road as "major" when the official source clearly identifies it as a state-controlled road, motorway, highway, or obvious arterial corridor.

For Brisbane addresses, prefer the live Brisbane or Queensland ArcGIS service layers behind the public map tools rather than relying only on the rendered consumer UI.

## Train access scoring

Use the nearest train station supported by official transport sources. Then use openrouteservice walking directions to get the base route distance and duration.

Preferred process:

1. Get property coordinates from an official source.
2. Get station-entry coordinates from an official Translink or Queensland Rail source.
3. Run `scripts/ors_walk_route.py`.
4. Use the returned route duration as the base walking time.
5. If the script returns `status: not_configured`, keep the section partial and say that openrouteservice is not configured in the current environment.

Use this formula:

`effective_estimated_walk_minutes = ceil(base_route_duration_seconds / 60) + 4 * major_road_crossings`

Count only crossings that materially interrupt the likely practical route and involve a major road, motorway ramp corridor, or clear arterial road from official mapping.

Map effective estimated walk time to a train access subscore:

| Effective estimated walk minutes | Train access subscore |
| --- | --- |
| 10 minutes or less | 95 |
| 11 to 15 minutes | 80 |
| 16 to 20 minutes | 65 |
| 21 to 30 minutes | 45 |
| 31 to 45 minutes | 25 |
| More than 45 minutes, or no practical walk identified | 10 |

If official sources do not support a reliable nearest station choice or station-entry coordinates, mark train access as unsupported.

If ORS is not configured:

- set `Train access subscore` to `Unsupported with current configuration`
- say `openrouteservice is not configured in the current environment`
- do not invent a fallback walk time

If ORS is configured but does not return a route, mark train access as unsupported with the returned error context.

## Composite score

Emit the composite score only when flood, main-road proximity, and train access are all supported.

Formula:

`suitability_score = round(flood_subscore * 0.45 + main_road_proximity_subscore * 0.30 + train_access_subscore * 0.25)`

Interpretation bands:

| Suitability score | Interpretation |
| --- | --- |
| 85 to 100 | Strong fit on this screening model |
| 70 to 84 | Generally favourable with some watchpoints |
| 50 to 69 | Mixed result with notable tradeoffs |
| 0 to 49 | High caution on this screening model |

## Required caveats

Always include these ideas in the report where relevant:

- NBN technology comes from NBN Co's official address-check service. Where premises and serving-area technologies differ, the premises technology is the property-specific result.
- Flood mapping is an official planning or awareness input, not a promise of future behaviour at the lot.
- Main-road proximity is a road-adjacency screen, not a measured air-quality or CO2 reading.
- Train access is based on official property and station coordinates plus a third-party OSM-based walking route from openrouteservice, not an official government walking route, service frequency, parking availability, or personal mobility need unless the user asks for those separately.

## Unsupported-data handling

Use this decision rule:

1. If the address is outside Queensland: stop.
2. If the address cannot be matched confidently: ask for suburb/postcode.
3. If flood evidence is unavailable from current official tools: keep the report partial.
4. If main-road evidence is unavailable from current official tools: keep the report partial.
5. If train station coordinates or nearest-station evidence are unavailable from current official tools, or ORS is unavailable for the current run: keep the report partial.
6. If any scored section is unsupported: omit the composite score.
