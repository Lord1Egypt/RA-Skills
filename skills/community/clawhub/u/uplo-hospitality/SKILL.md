---
name: uplo-hospitality
description: AI-powered hospitality knowledge management. Search guest service standards, property procedures, F&B operations, and event planning documentation with structured extraction.
---

# UPLO Hospitality — Guest Experience & Property Operations Intelligence

Hotels, resorts, and hospitality groups run on operational consistency across properties: brand standards manuals, front desk SOPs, housekeeping inspection checklists, F&B recipe costing sheets, banquet event orders, revenue management guidelines, and guest recovery protocols. UPLO centralizes this operational knowledge so that whether someone is at the flagship property or the newest acquisition, they can find the right procedure in seconds.

## Session Start

Hospitality organizations often manage multiple properties or brands with different operational tiers. Your identity context determines which property documentation you can access — a boutique brand's service standards differ from the convention hotel's, and both may be in the same portfolio.

```
get_identity_context
```

## When to Use

- A front desk agent encounters a guest with a confirmed reservation but no available rooms and needs the walk policy and compensation guidelines
- The banquet captain needs the setup specifications and AV requirements for a 300-person corporate gala scheduled for Saturday
- A new F&B manager asks what the target food cost percentage is for the rooftop restaurant and which menu items are below margin threshold
- Housekeeping wants to verify the deep cleaning protocol for a suite after a guest reported a bed bug sighting
- Revenue management asks what the dynamic pricing guardrails are during citywide convention dates
- The general manager needs to compile guest satisfaction scores and TripAdvisor response metrics for the quarterly owner's report
- A guest relations manager is handling an escalated complaint about a wedding reception and needs the service recovery authority matrix

## Example Workflows

### VIP Arrival Preparation

A high-profile repeat guest is arriving tomorrow. The guest relations team needs to prepare a seamless experience.

```
search_knowledge query="VIP guest arrival protocol including pre-arrival checklist and amenity placement standards"
```

```
search_with_context query="guest preference history program and loyalty tier recognition procedures"
```

```
search_knowledge query="executive suite setup specifications and turndown service enhancements for VIP stays"
```

### Food & Beverage Cost Control Review

The F&B director notices that the poolside bar's pour cost has spiked 8 points over the last two months and needs to investigate.

```
search_knowledge query="beverage inventory control procedures and pour cost calculation methodology"
```

```
search_knowledge query="poolside bar drink recipes and standard pour sizes for premium spirits"
```

```
search_with_context query="F&B purchasing agreements and approved supplier pricing for liquor and wine"
```

Compare documented standard pours and pricing against actual consumption to identify variance sources.

## Key Tools for Hospitality

**search_knowledge** — Operational SOPs are the backbone of hospitality. When a team member needs a specific procedure, this is the fastest path: `query="late checkout policy and authorization limits by front desk role level"`. Hospitality runs on procedures that need to be followed consistently, so precision matters.

**search_with_context** — Guest experience questions often cross departmental boundaries. A query about `query="managing a large group check-in for 150 rooms including luggage logistics, welcome reception setup, and billing master account procedures"` touches front office, bell services, banquets, and accounting.

**get_directives** — Brand standards and seasonal priorities flow from ownership or management company leadership. A directive to "achieve 90% TripAdvisor response rate" or "reduce F&B waste by 15% in Q3" directly shapes operational decisions.

**export_org_context** — Valuable for general manager transitions, brand conversions, or management company takeovers. The full organizational export provides a complete operational blueprint of the property.

**log_conversation** — Hospitality consultations often involve guest-facing decisions with financial implications (comping rooms, upgrading suites, waiving resort fees). Log these for audit and training purposes: `summary="Advised on service recovery for wedding group with sound system failure" topics='["service-recovery", "banquets", "guest-compensation"]'`

## Tips

- Hospitality knowledge is highly property-specific. Always include the property name or brand tier in your queries. The check-in process at a select-service hotel is fundamentally different from a luxury resort — generic queries will return irrelevant results.
- Seasonal operations change everything. Pool opening/closing procedures, holiday staffing matrices, and seasonal menu changeovers are time-dependent. Include the season or specific date range when searching for operational procedures.
- Guest service recovery has a financial dimension. When advising on how to handle a complaint, always search for the service recovery authority matrix — it defines what each role level can authorize without escalation (e.g., front desk can comp breakfast, only AGM can comp a night's stay).
- F&B operations generate some of the most granular documentation in hospitality: recipes with costing, vendor contracts, health inspection records, liquor license requirements. Search specifically within F&B document types when the question is food or beverage related.
