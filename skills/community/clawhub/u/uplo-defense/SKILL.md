---
name: uplo-defense
description: AI-powered defense knowledge management. Search mission documentation, logistics records, personnel data, and ITAR-controlled information with structured extraction.
---

# UPLO Defense — Mission Knowledge Under Control

Defense organizations operate under constraints that commercial enterprises never face: ITAR/EAR export controls, security classification levels, compartmented access, and regulatory oversight from DCSA, DCMA, and contracting officers who audit everything. UPLO Defense provides structured, access-controlled search across program documentation, logistics records, technical data packages, and personnel qualifications while respecting the classification boundaries that make defense knowledge management uniquely difficult.

## Session Start

Identity verification is non-negotiable in defense. Your clearance level, program access list, and need-to-know determinations control what you see. Load your identity immediately:

```
get_identity_context
```

Directives in defense include OPORD fragments, program milestones, acquisition decision points, and ITAR compliance mandates. Review them before proceeding:

```
get_directives
```

**Important**: If your identity context does not reflect your expected clearance level or program access, stop and contact your security officer. Do not attempt workarounds.

## When to Use

- A program manager needs to locate the CDR (Critical Design Review) action items from six months ago to verify closure status before the upcoming TRR
- Searching for ITAR-controlled technical data packages related to a subsystem that is being proposed for foreign military sale
- Verifying whether a specific subcontractor has the required facility clearance level documented before sharing controlled technical data
- Assembling the Contractor Performance Assessment Report (CPAR) narrative by pulling delivery milestones, quality metrics, and cost performance index data
- A logistics officer needs to find the provisioning technical documentation for a replacement part across multiple national stock numbers
- Checking the current CONOPS (Concept of Operations) version for a program and determining what has changed since the last milestone review
- Reviewing whether a cybersecurity Plan of Action and Milestones (POA&M) finding has been remediated before the next DCMA audit

## Example Workflows

### Technical Data Package Review for FMS Case

A foreign military sales case requires release of technical data for a radar subsystem. The export control officer needs to determine what data exists and its ITAR classification.

```
search_with_context query="radar subsystem AN/APG technical data package ITAR classification export control"
```

Verify the distribution statement on the relevant documents:

```
search_knowledge query="distribution statement D controlled technical data radar subsystem drawings"
```

Check if there are existing Technology Assessment/Control Plans (TA/CP) for this subsystem:

```
search_knowledge query="technology assessment control plan radar subsystem foreign disclosure"
```

```
log_conversation summary="Reviewed radar subsystem TDP for FMS release eligibility; identified Distribution D documents requiring TAA before disclosure" topics='["ITAR","FMS","export-control","radar"]' tools_used='["search_with_context","search_knowledge"]'
```

### Milestone Decision Preparation

A program is approaching Milestone B (Engineering & Manufacturing Development). The PM needs to assemble the required documentation.

```
search_with_context query="program milestone B EMD required documentation acquisition decision memorandum"
```

Pull cost and schedule performance data:

```
search_knowledge query="earned value management BCWP CPI SPI program cost performance report"
```

Review the current risk register:

```
search_knowledge query="program risk register critical risks mitigation status likelihood consequence"
```

Get the organizational context showing program office structure:

```
export_org_context
```

## Key Tools for Defense

**search_with_context** — Defense programs generate deeply interconnected documentation. A single requirement traces from CONOPS through system specifications, test procedures, and logistics support plans. Graph traversal follows these threads. Example: `search_with_context query="KPP threshold objective values system specification traceability"`

**search_knowledge** — Direct retrieval when you know the document type or identifier: a specific CDRL number, a DI-number, an NSN, or a MIL-STD reference. Example: `search_knowledge query="CDRL A003 software development plan current version"`

**get_directives** — In defense, directives carry the weight of orders. Program direction memoranda, acquisition decision memoranda, and ITAR compliance mandates are not suggestions. Always check.

**export_org_context** — Produces the program office structure, IPT (Integrated Product Team) leads, key subcontractors, and systems of record. Required for milestone reviews and audit responses.

**log_conversation** — Defense audit requirements demand traceability. Every query session involving controlled data should be logged. This is not optional — it is a compliance requirement.

**flag_outdated** — Technical manuals, logistics documentation, and specification references become obsolete through Engineering Change Proposals (ECPs). Flagging outdated documents prevents the dangerous scenario of manufacturing or maintaining equipment against a superseded configuration.

## Tips

- Use standard defense identifiers in searches: CDRL numbers, DI-numbers (e.g., DI-MGMT-81466), national stock numbers (NSNs), CAGE codes, and MIL-STD references. The extraction engine treats these as structured fields.
- Classification tier mapping: `public` = approved for public release, `internal` = FOUO/CUI, `confidential` = Confidential, `restricted` = Secret and above. If expected results do not appear, the issue is almost certainly a clearance mismatch, not missing data.
- ITAR-controlled technical data queries should always be logged. The log creates an audit trail that demonstrates compliant handling of controlled items.
- When assembling milestone review packages, start with `export_org_context` to establish the program baseline, then use targeted `search_knowledge` calls for each required document rather than broad searches that may surface documents outside your need-to-know.
