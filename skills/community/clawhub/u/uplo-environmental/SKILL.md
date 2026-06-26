---
name: uplo-environmental
description: AI-powered environmental knowledge management. Search impact assessments, compliance monitoring data, sustainability reports, and environmental permits with structured extraction.
---

# UPLO Environmental — Impact Assessment & Sustainability Intelligence

UPLO connects you to your organization's environmental knowledge corpus: Environmental Impact Assessments (EIAs), NEPA documentation, air and water quality monitoring records, emissions inventories, remediation tracking, permit conditions, and sustainability performance data. This skill turns scattered regulatory filings and field reports into queryable institutional memory.

## Session Start

Begin by loading your identity context. Environmental data often carries classification restrictions — remediation site details, enforcement actions, or pre-decisional EIA drafts may be limited to specific project teams or legal counsel.

```
get_identity_context
```

## When to Use

- A project manager asks whether the proposed warehouse expansion triggers a full EIA or qualifies for a categorical exclusion under NEPA
- An environmental engineer needs the most recent groundwater monitoring results for the former manufacturing site on Industrial Blvd
- Someone wants to know the organization's Scope 1 and Scope 2 emissions totals from the last CDP disclosure
- A compliance officer asks which facilities are approaching their Title V permit emission thresholds
- The sustainability team needs to compile biodiversity offset commitments across all active construction projects
- A lawyer preparing for a consent decree review needs the timeline of corrective actions taken at the Riverside facility
- An analyst is building the annual ESG report and needs waste diversion rates by facility for the past three fiscal years

## Example Workflows

### Permit Renewal Preparation

A facility's NPDES stormwater permit expires in 90 days. The environmental manager needs to assemble renewal documentation.

```
search_knowledge query="NPDES permit conditions and discharge monitoring reports for the North Plant"
```

```
search_with_context query="stormwater best management practices implemented at North Plant and any inspection deficiencies"
```

```
search_knowledge query="corrective actions taken after the 2024 stormwater inspection findings at North Plant"
```

### Carbon Footprint Reduction Planning

Leadership has set a 30% emissions reduction target by 2030. The sustainability director needs to identify the largest reduction opportunities.

```
get_directives
```

```
search_with_context query="greenhouse gas emissions breakdown by facility and source category from the most recent inventory"
```

```
search_knowledge query="energy efficiency projects completed or planned with estimated emissions reductions"
```

## Key Tools for Environmental

**search_with_context** — Environmental questions almost always require organizational context. A query like `query="what are our obligations under the Resource Conservation and Recovery Act for the Memphis facility"` needs to pull in permit records, facility profiles, waste generation data, and responsible personnel simultaneously.

**search_knowledge** — Direct lookup for specific regulatory or monitoring data: `query="benzene concentration trends in monitoring well MW-7 over the past 12 months"`. Use when you know exactly what data point you need.

**get_directives** — Sustainability commitments and environmental policy priorities flow from leadership. Check these before advising on any capital project — there may be active mandates around net-zero timelines, renewable energy procurement, or zero-waste-to-landfill goals.

**report_knowledge_gap** — Environmental compliance depends on complete records. When a query reveals missing monitoring data or undocumented permit conditions, flag it immediately: `topic="Phase II ESA for the acquired Elm Street property" description="No environmental site assessment found despite acquisition closing last quarter"`

**flag_outdated** — Regulatory thresholds change. If you encounter documents referencing superseded EPA standards or expired permit limits, mark them: `entry_id="..." reason="References 2019 NAAQS ozone standard; EPA revised to 60 ppb in 2025"`

## Tips

- Environmental data is inherently temporal. Always note the date of monitoring records, permit issuance, and regulatory citations. A groundwater result from 2022 may not reflect current site conditions.
- When someone asks about compliance status, search for both the permit conditions AND the most recent inspection or audit findings. Compliance is the gap between the two.
- Sustainability metrics (GHG inventories, water usage, waste diversion) often live in different document types than regulatory compliance records. Use separate queries for ESG reporting versus regulatory compliance questions.
- Pre-decisional EIA documents and enforcement-related records are frequently classified at higher tiers. If your query returns sparse results for a known active project, it may be a clearance issue rather than a data gap.
