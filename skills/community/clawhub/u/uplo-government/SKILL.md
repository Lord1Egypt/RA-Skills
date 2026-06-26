---
name: uplo-government
description: AI-powered government knowledge management. Search policy documents, regulatory filings, public records, and inter-agency coordination data with structured extraction.
---

# UPLO Government — Policy, Regulation & Inter-Agency Intelligence

Government agencies operate under layers of statutory requirements, executive orders, rulemaking records, appropriations language, inter-agency MOUs, and internal policy memoranda. UPLO indexes this documentation so analysts, program managers, and policy staff can find authoritative answers without navigating siloed document management systems or waiting for FOIA responses from their own agency.

## Session Start

Government data carries strict classification and handling requirements. Your clearance tier determines whether you can access pre-decisional policy drafts, law enforcement sensitive materials, or budget deliberation documents. Always start here.

```
get_identity_context
```

Active directives in a government context may include administration priorities, Congressional mandates with specific deadlines, or OMB guidance that constrains how programs operate.

```
get_directives
```

## When to Use

- A program analyst asks which statutory authority authorizes the grant program and whether the current appropriations language includes any new earmarks or restrictions
- The general counsel's office needs to review all inter-agency memoranda of understanding signed in the past two years to identify overlapping jurisdiction
- A policy advisor asks how the agency's current telework policy compares to the latest OPM guidance
- Someone in the budget office needs the spending plan for a specific line item across the last three continuing resolutions
- A congressional liaison is preparing testimony and needs a briefing package on the agency's performance against its strategic plan goals
- The inspector general's office asks for all corrective action plans related to prior audit findings that remain open
- A regional office director needs the delegation of authority chain for emergency procurement above $250,000

## Example Workflows

### Rulemaking Research

The agency is drafting a proposed rule and needs to review the regulatory history and public comments from the previous rulemaking cycle.

```
search_knowledge query="notice of proposed rulemaking and Federal Register publication for the 2024 data privacy rule"
```

```
search_with_context query="public comments received on the 2024 data privacy NPRM organized by major themes and agency responses"
```

```
search_knowledge query="regulatory impact analysis and cost-benefit assessment for the data privacy rule"
```

### Audit Response Coordination

A GAO audit report recommends changes to the agency's IT procurement process. The CIO needs to develop a corrective action plan.

```
search_knowledge query="GAO report recommendations for IT procurement and acquisition reform"
```

```
search_with_context query="current IT procurement policies and delegated purchasing authority thresholds"
```

```
search_knowledge query="open corrective action plans from prior GAO and OIG audit findings related to IT spending"
```

## Key Tools for Government

**search_with_context** — Government questions frequently span organizational boundaries. A query like `query="which divisions are responsible for implementing the cybersecurity executive order requirements and what is the status of each milestone"` requires connecting organizational structure, strategic goals, and compliance tracking.

**search_knowledge** — Precise lookups for statutory citations, regulation text, and policy memoranda: `query="delegation of authority memorandum for the Administrator's emergency spending authority"`. Government staff need the exact document, not a summary.

**export_org_context** — Indispensable for Congressional testimony prep, transition briefings, and strategic planning. Exports the complete agency knowledge map: mission, structure, personnel, systems, goals, and active directives in one document.

**get_directives** — In government, directives have legal force. Executive orders, OMB circulars, and agency head memoranda all create binding obligations. Always check directives when advising on any programmatic or operational question.

**propose_update** — When you identify a policy that conflicts with newer guidance or statute, propose the correction through the formal change process rather than just noting it: `target_table="entries" target_id="..." changes={...} rationale="Agency policy references OMB Circular A-76 which was superseded by M-24-11 in March 2024"`

## Tips

- Government documentation is citation-heavy. When surfacing information, include the specific statutory section (e.g., 5 U.S.C. 552a), regulation (e.g., 48 CFR 15.404), or policy memorandum number. Government users need the authoritative reference, not just the content.
- Be aware of the distinction between pre-decisional and final documents. Draft policy memos, budget deliberation materials, and rulemaking working documents are often classified at higher tiers and may be exempt from public release. Treat them accordingly.
- Inter-agency coordination documents (MOUs, MOAs, IAAs) are some of the hardest records to find in government. If someone asks about coordination with another agency, search explicitly for these agreement types.
- Government knowledge has a fiscal year rhythm. Budget data, performance metrics, and many compliance requirements operate on an October-September cycle. Always clarify which fiscal year is relevant when answering questions about spending, staffing, or performance.
