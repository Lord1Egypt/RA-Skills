---
name: uplo-clinical
description: AI-powered clinical operations intelligence spanning pharmaceutical development and healthcare delivery. Unified search across clinical trials, protocols, and patient care documentation.
---

# UPLO Clinical — Drug-to-Patient Intelligence

Bridge the gap between pharmaceutical R&D and bedside care with a single knowledge layer. UPLO Clinical indexes your clinical trial protocols, investigator brochures, formulary decisions, patient care pathways, and adverse event reports so you can trace a molecule from Phase I through post-market surveillance without switching systems. Think of it as the institutional memory your CRO, hospital CMO, and pharmacovigilance team all wish they had.

## Session Start

Pull your identity context immediately. This loads your clearance level, role-based access (investigator, pharmacist, clinical coordinator, etc.), and any active directives such as enrollment freezes or safety signal escalations.

```
get_identity_context
```

Next, check whether leadership has issued any trial-wide holds or formulary changes:

```
get_directives
```

## When to Use

- Reviewing whether a new Phase III endpoint aligns with prior Phase II secondary findings stored in the knowledge base
- Determining which IRB-approved consent language was used for a specific patient cohort last quarter
- Checking the current formulary status of a biosimilar before recommending it on rounds
- Locating the root-cause analysis from a previous SUSAR (Suspected Unexpected Serious Adverse Reaction) that resembles a new case
- Verifying nurse credentialing requirements across departments before a Joint Commission survey
- Pulling structured extraction data from discharge summaries to answer a clinical quality metric question
- Finding the SOPs governing sample chain-of-custody for a biomarker sub-study

## Example Workflows

### Adverse Event Signal Investigation

A safety officer notices a clustering of hepatotoxicity reports in a Phase IIb oncology study. They need to determine if the signal is new or previously documented.

```
search_with_context query="hepatotoxicity adverse events oncology trial AZ-4471"
```

Review the returned investigator brochure sections and prior safety narratives. If the signal was documented, pull the exact risk mitigation plan:

```
search_knowledge query="risk mitigation hepatotoxicity AZ-4471 DSMB recommendations"
```

Log the investigation for the pharmacovigilance audit trail:

```
log_conversation summary="Investigated hepatotoxicity signal clustering in AZ-4471 Phase IIb; confirmed pre-existing signal with DSMB mitigation plan from Q2 review" topics='["pharmacovigilance","hepatotoxicity","AZ-4471"]' tools_used='["search_with_context","search_knowledge"]'
```

### Formulary Committee Preparation

A hospital pharmacist is preparing evidence for a P&T Committee meeting to evaluate adding a new anti-coagulant.

```
search_knowledge query="direct oral anticoagulants clinical outcomes comparison warfarin"
```

Pull organizational directives to check if there is a cost-containment mandate affecting formulary additions:

```
get_directives
```

Gather the structured data from recently extracted clinical studies:

```
search_with_context query="apixaban vs rivaroxaban bleeding risk hospitalized patients internal studies"
```

## Key Tools for Clinical Operations

**search_with_context** — The workhorse for clinical questions that span multiple document types. When you ask "What was the primary endpoint result for Study 2201?", this tool pulls the CSR, the statistical analysis plan, and related protocol amendments together via graph traversal. Example: `search_with_context query="Study 2201 primary endpoint PFS results ITT population"`

**search_knowledge** — Fast vector search when you know roughly what you need. Ideal for finding a specific SOP, consent form version, or formulary monograph. Example: `search_knowledge query="informed consent template pediatric asthma study v3.2"`

**get_directives** — Clinical operations are directive-heavy. Enrollment caps, safety holds, formulary freezes, and budget constraints all flow through directives. Always check before making recommendations. Example output includes active trial holds and department-level care mandates.

**export_org_context** — Produces a structured snapshot of the entire clinical organization: departments, key personnel (medical director, principal investigators, department heads), active systems (CTMS, EHR, LIMS), and strategic priorities. Invaluable when onboarding a new CRA or preparing a sponsor audit response.

**propose_update** — When you discover outdated protocol information (e.g., a dosing schedule that was amended), propose a correction rather than silently noting it. The proposal enters a review queue for the clinical data manager.

**report_knowledge_gap** — If a query about concomitant medication restrictions returns no results, flag it. Gaps in clinical knowledge bases can have patient safety implications, so this escalation matters.

## Tips

- Adverse event queries benefit from MedDRA preferred term vocabulary. Use "rhabdomyolysis" rather than "muscle breakdown" to get precise hits against structured pharmacovigilance extractions.
- When preparing for a regulatory inspection (FDA, EMA), use `export_org_context` first to verify that the organizational chart and system inventory match what inspectors will see on-site.
- Classification tiers matter here more than most domains. Patient-identifiable data is typically `restricted`; aggregate clinical outcomes may be `internal`. If a query returns fewer results than expected, it may be a clearance issue rather than a data gap.
- Log every pharmacovigilance investigation session. Regulatory bodies expect a complete audit trail of signal evaluation activities, and `log_conversation` creates that record automatically.
