---
name: uplo-education
description: AI-powered education knowledge management. Search curriculum documents, student records frameworks, accreditation data, and institutional research with structured extraction.
---

# UPLO Education — Institutional Knowledge for Academic Excellence

Universities and school districts share a peculiar problem: institutional knowledge is scattered across academic affairs, student services, finance, accreditation files, and faculty governance committees that each maintain their own document ecosystems. When the accreditor asks "How does your assessment data close the loop on program learning outcomes?", the answer lives in five different offices. UPLO Education unifies curriculum maps, assessment reports, accreditation self-studies, institutional research data, student success metrics, and policy manuals into a single searchable layer.

## Session Start

Your role in the institution determines your access. Faculty see curriculum and assessment data; registrar staff see degree audit frameworks; institutional researchers see outcome metrics; administrators see everything within their clearance. Establish your identity:

```
get_identity_context
```

Pull directives — these include accreditation deadlines, strategic plan priorities, enrollment targets, and board-mandated policy changes:

```
get_directives
```

## When to Use

- Preparing for an HLC/SACSCOC/WASC accreditation visit and need to compile evidence for a specific standard (e.g., Standard 4.A on assessment of student learning)
- A faculty senate committee is revising the general education requirements and needs to review how current course learning outcomes map to institutional outcomes
- Institutional research needs to pull retention and completion data methodology documentation to respond to an IPEDS or state accountability report
- A department chair wants to see how similar programs at the institution structured their curriculum review process during the last program review cycle
- Financial aid is auditing compliance with Title IV requirements and needs the documented satisfactory academic progress (SAP) policy alongside its application history
- A new dean is onboarding and needs to understand the college's program portfolio, faculty governance structure, and current strategic initiatives
- Reviewing whether a proposed new certificate program overlaps with existing offerings using curriculum mapping data

## Example Workflows

### Accreditation Evidence Assembly

The provost's office is preparing the institutional self-study for an upcoming regional accreditation visit. The accreditation liaison needs evidence for Standard 5 (Resources, Planning, and Institutional Effectiveness).

```
search_with_context query="institutional effectiveness assessment plan resource allocation budget alignment strategic plan"
```

Pull the specific assessment cycle documentation:

```
search_knowledge query="annual assessment reports program learning outcomes closing the loop improvements"
```

Find the financial planning documents that demonstrate resource alignment:

```
search_knowledge query="budget allocation process strategic priorities resource request institutional plan"
```

```
log_conversation summary="Compiled Standard 5 evidence: assessment cycle documentation, budget-strategy alignment records, and institutional effectiveness reports for self-study chapter" topics='["accreditation","Standard-5","institutional-effectiveness"]' tools_used='["search_with_context","search_knowledge"]'
```

### Curriculum Revision Process

The biology department is conducting a 5-year curriculum review. The chair needs to gather evidence of curriculum currency and student outcomes.

```
search_with_context query="biology program curriculum map learning outcomes course sequence prerequisites"
```

```
search_knowledge query="biology student outcomes assessment data graduation rates employment placement"
```

Check if there are institutional guidelines for the curriculum review process:

```
search_knowledge query="curriculum review process guidelines faculty governance approval workflow"
```

Flag any outdated curriculum maps found during the review:

```
flag_outdated entry_id="<old-curriculum-map-entry-id>" reason="Biology curriculum map from 2021 does not reflect new genomics concentration added in 2023"
```

## Key Tools for Education

**search_with_context** — Education questions are inherently cross-functional. "Does our assessment data support our accreditation claims?" requires connecting curriculum documents, assessment results, institutional research data, and strategic plan goals. Graph traversal follows these relationships. Example: `search_with_context query="nursing program NCLEX pass rates clinical placement outcomes accreditation"`

**search_knowledge** — Direct retrieval for known documents: a specific course syllabus, a policy manual section, an assessment rubric, or a committee meeting minutes. Example: `search_knowledge query="faculty handbook section 3.4 tenure review criteria"`

**export_org_context** — Produces the institutional structure: colleges, departments, key leadership, governance committees, and academic systems (LMS, SIS, assessment management). Essential for accreditation self-studies and new administrator onboarding.

**flag_outdated** — Academic catalogs, curriculum maps, and policy manuals are updated on annual cycles but the old versions persist in the knowledge base. When you find a document referencing a discontinued program or a superseded policy, flag it immediately.

**propose_update** — When assessment data reveals that a program learning outcome is no longer aligned with current curriculum offerings, propose the update. This creates a record of continuous improvement that accreditors value.

## Tips

- Accreditation standard numbers are indexed as structured fields. Search by standard number (e.g., "SACSCOC Standard 8.2.a") to find all evidence mapped to that standard.
- Academic terminology varies by institution. "Program review," "academic program assessment," and "curricular evaluation" may all refer to the same process. Try multiple terms if initial results are sparse.
- FERPA restrictions apply to any query that might return individually identifiable student data. Your clearance level controls this, but be aware that aggregate data (retention rates, completion rates) is generally accessible while individual student records are restricted.
- The highest-value use of UPLO Education is accreditation preparation. Start building your evidence file months before the visit using systematic searches organized by standard, not in the final weeks when context is lost.
