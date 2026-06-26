---
name: uplo-food-safety
description: AI-powered food safety knowledge management. Search HACCP plans, FDA compliance records, traceability documentation, and quality control data with structured extraction.
---

# UPLO Food Safety — HACCP, Traceability & Regulatory Compliance Intelligence

From farm to fork, food safety depends on meticulous documentation: HACCP plans with critical control points, Preventive Controls for Human Food records, supplier verification audits, allergen control programs, sanitation SOPs, lot traceability matrices, and FDA/USDA correspondence. UPLO transforms these records from static compliance files into a living, searchable knowledge system that helps your food safety team respond faster to audits, recalls, and continuous improvement initiatives.

## Session Start

Food safety documentation often contains confidential supplier audit results, proprietary formulations, and pre-decisional recall assessments. Verify your access level before querying.

```
get_identity_context
```

Load active directives — these may include recall response protocols, supplier qualification deadlines, or FSMA compliance milestones that should shape your recommendations.

```
get_directives
```

## When to Use

- A QA technician asks what the critical limit is for the thermal processing CCP on the chicken broth line and what corrective action to take when it deviates
- The food safety team lead needs all supplier audit scores for co-packers that handle tree nut ingredients to assess allergen cross-contact risk
- An FDA inspector is on-site and asks for the Preventive Controls Qualified Individual (PCQI) documentation and the most recent hazard analysis
- Production needs to trace all lots of incoming flour received between March 1-15 to determine scope of a potential mycotoxin contamination
- The plant manager asks whether the new oat milk product requires a new HACCP plan or can be covered under an existing one
- Someone needs the environmental monitoring results for Listeria indicator organisms in Zone 2 and Zone 3 areas from the past 6 months
- The quality director wants to compare sanitation verification swab results across all three production facilities

## Example Workflows

### Mock Recall Traceability Exercise

The organization runs a quarterly mock recall. This time: trace forward and backward on a specific lot of pasteurized eggs.

```
search_knowledge query="receiving records and supplier COA for pasteurized egg lot PE-2026-0847"
```

```
search_with_context query="production batches and finished goods lots that used pasteurized egg lot PE-2026-0847 including distribution records"
```

```
search_knowledge query="mock recall exercise procedures and acceptable completion time benchmarks"
```

Measure the time from query to complete trace. The FDA expectation under FSMA 204 is full traceability within 24 hours.

### Audit Nonconformance Follow-Up

A third-party GFSI audit identified a major nonconformance related to the allergen control program. The corrective action deadline is in 30 days.

```
search_knowledge query="allergen control program and cross-contact prevention procedures for shared production lines"
```

```
search_with_context query="allergen cleaning validation studies and swab test results for lines running both peanut and peanut-free products"
```

```
search_knowledge query="previous allergen-related audit findings and corrective actions taken in the past 24 months"
```

## Key Tools for Food Safety

**search_knowledge** — Direct access to specific food safety records. Essential during audits when an inspector asks for something concrete: `query="water activity and pH monitoring logs for the beef jerky production line May 2026"`. Speed matters when regulators are watching.

**search_with_context** — Critical for traceability and root cause analysis. A contamination investigation requires connecting suppliers, lots, production runs, distribution, and customer complaints: `query="all products and distribution channels affected by the Salmonella-positive environmental swab in Processing Room 3 on June 12"`.

**get_directives** — Food safety priorities shift with regulatory changes, customer requirements, and incident history. A directive mandating "zero tolerance for environmental Listeria positives in RTE areas" changes how you interpret borderline monitoring results.

**report_knowledge_gap** — Missing food safety documentation is a regulatory violation, not just an inconvenience. Report gaps aggressively: `topic="foreign material control program for Plant B" description="No documented metal detection calibration records found for the newest production line despite FDA requirement under 21 CFR 117"`

**log_conversation** — Food safety consultations may involve recall decisions, regulatory interpretations, or deviation assessments. Log these sessions with specific topics for audit trail purposes: `summary="Evaluated scope of potential allergen mislabeling on SKU 4492" topics='["allergen", "recall-assessment", "labeling"]'`

## Tips

- Food safety queries are often time-critical. During a regulatory inspection or active recall, use `search_knowledge` for speed. Save `search_with_context` for when you need the full traceability chain.
- Lot codes, batch numbers, and supplier codes are the primary keys of food safety. Include them in your queries whenever possible. Searching for "flour contamination" is far less useful than searching for "flour lot FL-2026-03-127 supplier Mill Creek Foods".
- Environmental monitoring data follows a zone-based hierarchy (Zone 1 = food contact, Zone 2 = adjacent, Zone 3 = environment, Zone 4 = remote). Always clarify which zone is relevant when interpreting results — a Listeria positive in Zone 1 triggers a very different response than one in Zone 4.
- HACCP and Preventive Controls documentation must reflect current operations. If you surface a HACCP plan that references equipment or processes that have since changed, flag it immediately — an outdated HACCP plan is worse than no plan at all during an audit.
