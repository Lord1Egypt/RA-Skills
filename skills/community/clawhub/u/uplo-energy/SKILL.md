---
name: uplo-energy
description: AI-powered energy sector knowledge management. Search power generation records, grid management data, regulatory filings, and safety protocols with structured extraction.
---

# UPLO Energy — Generation-to-Grid Intelligence

The energy sector runs on documentation: NERC compliance evidence, generation performance reports, outage analyses, environmental permits, rate case filings, and safety management system records. These documents are produced by operations, compliance, engineering, environmental, and regulatory affairs teams that rarely share a common system. UPLO Energy indexes this sprawl so a plant manager preparing for a NERC audit and a regulatory analyst drafting a rate case filing can both find what they need without navigating six different document repositories.

## Session Start

Energy operations involve safety-critical and CEII (Critical Energy Infrastructure Information) data. Your clearance and role assignment must be verified before any queries.

```
get_identity_context
```

```
get_directives
```

Active directives in energy often include NERC compliance deadlines, planned outage schedules, emergency operations procedures during weather events, and rate case filing timelines. These are not informational — they drive daily operations.

## When to Use

- Preparing NERC CIP compliance evidence and need to locate the specific access control documentation for a cyber asset at a generating facility
- Investigating a forced outage and need to find the root cause analysis from similar equipment failures across the fleet
- A rate case is being filed and the regulatory team needs historical capital expenditure justification, O&M cost trends, and load forecast methodology documentation
- Environmental compliance requires pulling the air permit conditions, continuous emissions monitoring (CEMS) data reports, and EPA reporting documentation for an upcoming inspection
- Operations planning needs the current transmission constraint studies and generation dispatch order documentation
- A safety incident occurred and the investigation team needs the JSA (Job Safety Analysis), switching orders, and lockout/tagout procedures that were in effect
- Onboarding a new reliability coordinator who needs to understand the balancing authority area, transmission topology, and interconnection agreements

## Example Workflows

### NERC CIP Audit Preparation

A NERC audit is scheduled in 60 days. The compliance team needs to assemble evidence for CIP-007 (System Security Management).

```
search_with_context query="NERC CIP-007 system security management patch management cyber assets evidence"
```

Pull the specific documentation for security patch implementation:

```
search_knowledge query="patch management program BES cyber assets implementation records compliance"
```

Find the electronic access control documentation:

```
search_knowledge query="electronic access point monitoring BES cyber system network security CIP-005"
```

Export the organizational context to map cyber asset owners to the compliance evidence:

```
export_org_context
```

```
log_conversation summary="Assembled CIP-007 and CIP-005 evidence package for NERC audit; identified patch compliance records and EAP monitoring documentation" topics='["NERC-CIP","audit","cybersecurity","compliance"]' tools_used='["search_with_context","search_knowledge","export_org_context"]'
```

### Forced Outage Root Cause Analysis

A 500 MW combined-cycle unit tripped offline due to a combustion turbine compressor issue. The plant engineer needs to investigate.

```
search_with_context query="combustion turbine compressor trip forced outage similar events root cause fleet"
```

```
search_knowledge query="GE 7FA compressor blade inspection borescope findings maintenance records"
```

Check if there is an OEM service bulletin related to this failure mode:

```
search_knowledge query="GE service bulletin technical information letter compressor blade cracking 7FA"
```

Report a gap if the maintenance records are incomplete:

```
report_knowledge_gap query="Unit 3 combustion turbine compressor maintenance history borescope interval records"
```

## Key Tools for Energy

**search_with_context** — Energy questions span organizational boundaries. "Are we compliant with CIP-007?" touches cybersecurity, operations, maintenance, and IT documentation. Graph traversal assembles this cross-functional evidence. Example: `search_with_context query="transmission line relay settings protection coordination study 230kV"`

**search_knowledge** — Direct lookup for known documents: a specific NERC standard evidence file, a plant operating procedure, an environmental permit, or a maintenance record. Example: `search_knowledge query="air quality permit Title V Facility 004 conditions NOx limits"`

**get_directives** — Energy directives are operationally binding. A planned outage schedule, a generation curtailment order, or a NERC compliance deadline flows through here. Missing a directive can result in reliability standard violations.

**flag_outdated** — Operating procedures, relay settings, and protection coordination studies must match the current configuration. A relay setting document that does not reflect the latest short circuit study is a reliability risk. Flag immediately.

**report_knowledge_gap** — Undocumented maintenance history, missing calibration records for CEMS equipment, or absent protection coordination studies are compliance gaps. Reporting them creates accountability.

**log_conversation** — NERC standards require evidence of systematic review. Logging your compliance evidence assembly sessions creates an auditable record that demonstrates due diligence.

## Tips

- NERC standard identifiers (CIP-007-6 R2, FAC-008-3, TPL-001-5) are indexed as structured fields. Query by standard and requirement number for precise results.
- CEII data is classified at the `restricted` tier. If queries about transmission topology, generation interconnection, or critical infrastructure locations return no results, it is likely a clearance issue. Contact your CEII custodian.
- Forced outage investigations benefit from fleet-wide searches. A compressor blade issue on Unit 3 may have been seen on Unit 7 two years ago. Use `search_with_context` with equipment model identifiers to find cross-unit patterns.
- Environmental permit conditions often contain specific numerical limits (NOx lb/hr, SO2 ppm, particulate matter mg/m3). Include these units in your search terms — the extraction engine indexes them as structured fields alongside the regulatory limits.
