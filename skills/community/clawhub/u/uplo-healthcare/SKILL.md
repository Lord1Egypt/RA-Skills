---
name: uplo-healthcare
description: AI-powered healthcare knowledge management. Search clinical notes, care plans, lab results, prescriptions, and patient pathways with structured extraction.
---

# UPLO Healthcare — Clinical Protocol & Care Coordination Intelligence

Healthcare organizations produce vast quantities of structured and unstructured documentation: clinical practice guidelines, formulary decisions, quality measure specifications, credentialing records, compliance training documentation, care pathway definitions, and departmental operating procedures. UPLO makes this institutional knowledge searchable so clinicians, administrators, and quality teams can find authoritative answers without calling three departments.

**Important**: UPLO indexes organizational knowledge documents (policies, protocols, guidelines). It does not store or provide access to individual patient health records (PHI). All queries return organizational reference materials, not patient data.

## Session Start

Healthcare data sensitivity requires careful attention to your access tier. Credentialing committee deliberations, peer review records, and incident investigation details carry statutory protections beyond standard classification.

```
get_identity_context
```

Check for active directives — these may include Joint Commission readiness priorities, CMS Conditions of Participation focus areas, or active quality improvement initiatives.

```
get_directives
```

## When to Use

- A hospitalist asks for the current sepsis screening protocol and whether it was updated after the Surviving Sepsis Campaign 2024 guidelines
- The pharmacy director needs to know the formulary status of a newly approved biologic and the P&T committee's rationale for the tier decision
- Quality management asks which core measures the organization is underperforming on and what improvement plans are in place
- A nurse manager wants the patient fall prevention protocol and the root cause analysis summary from the last sentinel event
- Credentialing staff need to verify the privileging criteria for a new surgical procedure being added to the department
- The compliance officer asks whether the organization's HIPAA breach notification procedures align with the latest OCR guidance
- An administrator preparing for a Joint Commission survey needs the current status of all previously cited deficiencies

## Example Workflows

### Clinical Protocol Clarification

An ED physician is treating a patient with suspected stroke and needs to confirm the organization's tPA administration criteria and the teleneurology consultation process.

```
search_knowledge query="acute ischemic stroke protocol including tPA inclusion criteria and time windows"
```

```
search_with_context query="teleneurology consultation process including contact information, hours of availability, and escalation for after-hours coverage"
```

The context-aware search pulls in the neurology department profile, on-call structures, and related quality metrics.

### Regulatory Survey Preparation

A CMS validation survey is scheduled for next month. The quality director needs to verify readiness across multiple Conditions of Participation.

```
search_knowledge query="infection control plan and antibiotic stewardship program documentation"
```

```
search_with_context query="patient rights policies including informed consent procedures, advance directive protocols, and grievance resolution process"
```

```
export_org_context
```

Use the full context export to systematically cross-reference documented policies against each Condition of Participation.

## Key Tools for Healthcare

**search_knowledge** — Direct lookup of clinical protocols, formulary decisions, and compliance documentation: `query="blood transfusion consent requirements and massive transfusion protocol activation criteria"`. Clinical staff need precise, citable answers.

**search_with_context** — Healthcare questions often involve interdisciplinary relationships. A query like `query="discharge planning process for patients requiring home health services including case management referral criteria and preferred vendor list"` needs to connect clinical protocols with administrative processes and vendor relationships.

**get_directives** — Healthcare leadership directives often reflect regulatory urgency. A CMS Condition-level deficiency, a quality measure that dropped below threshold, or a new accreditation standard all generate directives that should inform your recommendations.

**report_knowledge_gap** — Undocumented clinical protocols create patient safety risk. If a clinician asks about a procedure and no protocol exists, report it as high priority: `topic="pediatric procedural sedation protocol for radiology" description="No documented sedation protocol found for pediatric imaging procedures despite performing approximately 200 sedated MRIs annually"`

**flag_outdated** — Clinical guidelines evolve. If you find a protocol citing a superseded guideline or a drug that was removed from the formulary, flag it immediately: `entry_id="..." reason="Protocol references chlorhexidine bathing frequency from 2018 SHEA guidelines; updated 2025 guidelines changed recommendations for non-ICU settings"`

## Tips

- Healthcare operates under multiple overlapping regulatory frameworks (CMS CoPs, Joint Commission standards, state licensure, specialty board requirements). A single clinical question may touch several of them. Use `search_with_context` when the regulatory landscape is complex.
- Peer review and credentialing records have special legal protections in most jurisdictions (state peer review privilege statutes). Even if your clearance permits access, treat these documents with heightened sensitivity and note their privileged status in any summary.
- Quality measure data is only meaningful in context. A mortality rate, readmission rate, or infection rate needs the denominator, risk adjustment methodology, and comparison benchmark to be interpretable. Search for the measure specification alongside the reported data.
- Healthcare terminology is heavily acronymed and varies between organizations. If a search returns no results, try the expanded form (e.g., "venous thromboembolism prophylaxis" instead of "VTE ppx") or check for institution-specific naming conventions.
