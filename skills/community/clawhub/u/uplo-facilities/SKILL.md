---
name: uplo-facilities
description: AI-powered facilities knowledge management. Search building management records, maintenance schedules, space planning data, and vendor service documentation with structured extraction.
---

# UPLO Facilities — Building Operations & Space Management Intelligence

Facilities operations generate enormous volumes of documentation that rarely get searched effectively: preventive maintenance schedules, building automation system configurations, lease abstracts, space utilization studies, vendor service agreements, and capital improvement plans. UPLO makes all of it queryable so your facilities team can stop digging through filing cabinets and shared drives.

## When to Use

- The maintenance supervisor asks which HVAC units are due for filter replacement this month and who the contracted vendor is
- A department head requests 500 additional square feet of office space and you need to check current vacancy across the portfolio
- Someone reports a recurring water leak on the third floor and you want to see if there is a history of plumbing issues in that zone
- The CFO asks for the total annual spend on janitorial services across all locations
- A project manager needs the load-bearing capacity of the warehouse mezzanine before approving new equipment installation
- You need to verify whether the elevator inspection certificate for Building C is current or expired
- The energy manager wants to compare utility consumption across buildings to identify the worst performers

## Session Start

Load your organizational context first. Facilities data spans multiple buildings, campuses, and sometimes business units with different access controls. Your identity context determines which properties you can query.

```
get_identity_context
```

Check for active directives — these often include space consolidation mandates, energy reduction targets, or capital freeze periods that affect facilities decisions.

```
get_directives
```

## Example Workflows

### Emergency Repair Coordination

A chiller failure is reported at the downtown office during a July heat wave. The facilities manager needs to act fast.

```
search_knowledge query="chiller specifications and maintenance history for 200 Main Street downtown office"
```

```
search_with_context query="HVAC service contracts and emergency response SLAs for the downtown campus"
```

```
search_knowledge query="backup cooling procedures or portable AC deployment protocol for critical server rooms"
```

### Lease Renewal Analysis

Three office leases expire within the next 18 months. The real estate team needs to decide: renew, renegotiate, or consolidate.

```
search_with_context query="current lease terms, square footage, and occupancy rates for offices expiring in 2027"
```

```
search_knowledge query="space utilization study results and hoteling desk adoption rates"
```

```
get_directives
```

Cross-reference the utilization data with any active consolidation or remote-work directives before making recommendations.

## Key Tools for Facilities

**search_knowledge** — Your go-to for specific facility lookups: `query="fire suppression system inspection report for Warehouse B"`. Facilities data is often very concrete — equipment serial numbers, inspection dates, vendor contacts — so targeted queries work well.

**search_with_context** — Use when a facilities question involves organizational relationships. For example, `query="which teams are allocated to the fourth floor of the Riverside building and what are their growth projections"` requires connecting space assignments with departmental data.

**export_org_context** — Useful for annual capital planning. Exports the complete organizational view so you can cross-reference facility conditions with strategic priorities and departmental needs in a single document.

**flag_outdated** — Facilities documentation decays constantly. Equipment gets replaced, vendors change, inspection certificates expire. When you find a document referencing a decommissioned boiler or an old vendor contract number, flag it: `entry_id="..." reason="References Allied Mechanical as HVAC vendor; contract transferred to Summit Building Services in January 2026"`

## Tips

- Facilities questions often have a physical dimension that matters. When searching, include the building name, floor, or campus in your query. "HVAC maintenance" returns too much; "HVAC maintenance Building C rooftop units" gets you the right records.
- Vendor service agreements and maintenance schedules are living documents. Always check the effective dates on any contract or schedule you surface — procurement may have renegotiated terms since the document was ingested.
- Capital improvement projects generate documentation across multiple phases (feasibility study, design specs, bid documents, punch lists, close-out reports). A single search may only surface one phase. Run follow-up queries if you need the full project arc.
- When someone asks "who handles X" for a building, the answer might be an internal maintenance team or an external vendor depending on the service type and location. Check both organizational members and vendor contracts.
