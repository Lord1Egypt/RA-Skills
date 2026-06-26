# QLD Property Research Official Sources

## Contents

- Source policy
- Statewide foundations
- Flood source order by region
- SEQ coverage guidance
- Partial-report rules

## Source policy

Use official sources only for core findings. Prefer property-specific official reports or official interactive maps over generic informational pages.

Do not use:

- real-estate listing sites
- Google Maps for core scoring evidence
- unofficial blogs, Reddit, or forum posts
- private map portals unless they are the official delivery vehicle of the relevant council or agency

## Statewide foundations

Use these pages to anchor address, roads, transport, and NBN checks.

### Queensland address and spatial context

- Queensland address guidance and Queensland Globe access:
  [Find addresses | Queensland Government](https://www.qld.gov.au/environment/land/title/addressing/finding)
- Queensland Globe access and layer workflow:
  [Using the Queensland Globe | Business Queensland](https://www.business.qld.gov.au/running-business/support-services/mapping-data-imagery/queensland-globe/using)

Use Queensland Globe to verify address placement and inspect official spatial layers for roads and land-use context.

For Brisbane addresses, it is often more reliable to query the live Brisbane ArcGIS parcel and flood services exposed by the public flood app than to rely on the consumer map interface alone.
Use `scripts/brisbane_flood_check.py` as the default Brisbane flood path. Treat the Flood Awareness browser UI as a fallback, not the primary workflow.

### Major roads

- Broader Queensland mapping tools:
  [Land use and mapping tools for agriculture | Business Queensland](https://www.business.qld.gov.au/industries/farms-fishing-forestry/agriculture/business/expand/maps)

Use Queensland Globe road layers and current Queensland Government mapping tools to decide whether a nearby corridor qualifies as a major road.

### Train network and stations

- Journey planning landing page:
  [Plan your journey | Translink](https://translink.com.au/plan-your-journey)
- Network and station maps:
  [Maps | Translink](https://translink.com.au/plan-your-journey/maps)
- Station detail pages:
  [Ferny Grove station example | Translink](https://translink.com.au/tickets-and-fares/go-card/locations/82/details)

Use Translink for nearest-station identification and station-entry coordinates. Then use openrouteservice for the walking route, as described in [openrouteservice.md](openrouteservice.md).

### NBN infrastructure

- Official public check page:
  [Check address | nbn](https://www.nbnco.com.au/check-address)

Use the NBN Co check-address service for premises technology such as FTTP, HFC, FTTN, FTTC, FTTB, Fixed Wireless, or Satellite.
For repeatable checks, prefer `scripts/nbn_infrastructure_check.py --address "<full address>"`, which queries the same public official service endpoints used by the check-address page.
When the script returns both premises and serving-area technology, treat the premises technology as the property-specific result and the serving-area technology as broader context only.

## Flood source order by region

Choose the first applicable official source in this order.

### Brisbane City Council

High-confidence coverage.

1. [FloodWise Property Report | Brisbane City Council](https://www.brisbane.qld.gov.au/building-and-planning/supporting-documents-and-online-tools/floodwise-property-report)
2. [Check your risk / Flood Awareness Map | Brisbane City Council](https://www.brisbane.qld.gov.au/community-support-and-safety/natural-disasters-and-emergencies/check-your-disaster-risk)

Use FloodWise when property-level detail is available. Use the Flood Awareness Map for the mapped finding and likelihood context.
For repeatable checks, prefer the live public ArcGIS services exposed by Flood Awareness Online, especially parcel boundaries, parcel metrics, and the flood-awareness layers.
Use `scripts/brisbane_flood_check.py --address "<full address>"` before opening FloodWise or the browser map.

### City of Moreton Bay

High-confidence coverage.

1. [Moreton Bay flood mapping | City of Moreton Bay](https://www.moretonbay.qld.gov.au/Services/Property-Ownership/Flooding/Flood-Mapping)

Use the flood check property report when accessible from the official flow. Treat it as the strongest Moreton Bay property-specific source.

### Logan City Council

High-confidence coverage.

1. [Logan PD Hub | Logan City Council](https://www.logan.qld.gov.au/planning-and-building/planning-and-development/pd-hub)
2. [Flood | Logan City Council](https://www.logan.qld.gov.au/floodimpacts)
3. [Flood maps | Logan City Council](https://www.logan.qld.gov.au/planning-and-building/Flood-maps)

Use the PD Hub property report and linked flood report first. Use the broader flood pages for policy context and portal updates.

### Sunshine Coast Council

High-confidence coverage for awareness and development-oriented flood information.

1. [Flood mapping and information including flood searches | Sunshine Coast Council](https://www.sunshinecoast.qld.gov.au/development/development-tools-and-guidelines/flood-mapping-and-information)
2. [Flood information relevant to building works | Sunshine Coast Council](https://www.sunshinecoast.qld.gov.au/building-work/flooding-and-building)
3. [Flooding questions and factsheets | Sunshine Coast Council](https://www.sunshinecoast.qld.gov.au/development/searches/flood-mapping-and-information/faq)

Use the public mapping and Development.i site-report path when available. If only a paid or manual flood search would answer the question, keep the flood section partial and say so.

### Ipswich City Council

Limited public flood support in this skill.

1. [Development.i | Ipswich City Council](https://developmenti.ipswich.qld.gov.au/)
2. [Search Fees and Information | Ipswich City Council](https://www.ipswich.qld.gov.au/Services/Searches-and-Enquiries/Property-and-Rates-Search/Search-Fees-and-Information)

Ipswich has official flood reporting, but the clearest property-specific flood report is a paid Development Flood Property Report. For unpaid public research, do best-effort map review plus clear caveats. If a reliable public flood result is unavailable, mark flood as unsupported.

### City of Gold Coast

Limited public flood support in this skill.

1. [Disaster and Emergency Dashboard | City of Gold Coast](https://dashboard.goldcoast.qld.gov.au/)
2. Official City Plan property-report flows surfaced through City systems when accessible

Gold Coast support should be treated as best-effort unless a clearly property-specific official flood result is available from the current official tools.

### Other Queensland councils

Best-effort only.

Use the council's official flood, disaster, planning, or property map tools if they are current and property-searchable. If an official property-specific result is not available, keep the report partial and omit the flood subscore.

## SEQ coverage guidance

Use these coverage labels in the `Address / Coverage` section.

| Coverage label | Meaning |
| --- | --- |
| High | Brisbane, Moreton Bay, Logan, or Sunshine Coast with current official property or map evidence for all required sections |
| Medium | Other SEQ address with partial but still usable official evidence |
| Limited | Regional Queensland address or SEQ address where one or more core sections cannot be supported from current official sources |

Apply the composite score only when the address effectively has full section support, regardless of label.

## Partial-report rules

Use a partial report when any of these conditions apply:

- the flood source is only historical or informational and not property-specific enough to score
- main-road evidence cannot be confirmed from current official mapping
- the nearest train station cannot be supported with official station evidence
- the address sits outside the strongest-supported SEQ council flows and current tools are incomplete

When partial:

- keep the `Address / Coverage`, `NBN Infrastructure`, `Flood`, `Main Road Proximity`, `Train Access`, and `Sources` sections
- keep `Composite Score` as a heading but state that it is not emitted because one or more sections are unsupported
- explain exactly which section is unsupported and why
