---
name: uplo-hr
description: AI-powered HR knowledge management. Search employee handbooks, org charts, company policies, benefits documentation, and onboarding materials with structured extraction.
---

# UPLO HR — People Operations & Workforce Policy Intelligence

Every organization has an HR knowledge problem: policies scattered across SharePoint, benefits summaries buried in PDF packets from open enrollment two years ago, onboarding checklists that differ by department, and comp band structures that only two people in Total Rewards actually understand. UPLO indexes all of it — handbooks, policy manuals, benefits plan documents, org charts, job descriptions, performance review templates, and leave administration guides — into a single searchable layer.

## Session Start

HR data is among the most sensitive in any organization. Compensation data, disciplinary records, accommodation requests, and investigation files are typically restricted. Your identity context governs what you can see.

```
get_identity_context
```

## When to Use

- An employee asks whether they can use PTO during their first 90 days and what the accrual schedule looks like for their employment tier
- A hiring manager needs the approved job description and salary band for a Senior Data Engineer role in the Austin office
- The benefits team gets a question about whether domestic partners are eligible for dental coverage under the current plan
- A manager is drafting a performance improvement plan and needs the PIP template and the required HR sign-off process
- Someone in legal asks for the current anti-harassment training completion rates by department ahead of an EEOC inquiry
- An employee relocating from New York to Texas needs to understand what changes to expect in state tax withholding and benefits eligibility
- The CHRO wants to see attrition trends and exit interview theme summaries for the Engineering department over the past 12 months

## Example Workflows

### New Hire Onboarding Support

A manager is onboarding three new hires starting next Monday and needs to make sure everything is ready.

```
search_knowledge query="new hire onboarding checklist including IT provisioning, badge access, and required first-week training"
```

```
search_with_context query="benefits enrollment deadlines and required documentation for new employees"
```

```
search_knowledge query="department-specific onboarding orientation schedule for the Product team"
```

### Leave of Absence Administration

An employee's manager reports that the employee needs an extended medical leave. HR needs to navigate FMLA, short-term disability, and return-to-work requirements.

```
search_knowledge query="FMLA eligibility criteria and leave request procedures including required medical certification"
```

```
search_with_context query="short-term disability benefits coordination with FMLA leave and pay continuation policies"
```

```
search_knowledge query="return to work process after medical leave including fitness for duty certification and accommodation request procedures"
```

## Key Tools for HR

**search_knowledge** — The workhorse for policy questions. When an employee or manager asks about a specific policy, search directly: `query="remote work policy including eligibility criteria, equipment stipend, and in-office day requirements"`. Most HR questions have a definitive answer in a policy document somewhere.

**search_with_context** — HR questions involving organizational relationships benefit from context. A query like `query="who reports to the VP of Engineering, what are the team's open positions, and what is the approved headcount for Q3"` connects the org chart with workforce planning data.

**get_directives** — HR operates under strategic mandates: hiring freezes, diversity goals, return-to-office requirements, compensation adjustment timelines. These directives override standard procedures, so always check them before giving policy guidance.

**report_knowledge_gap** — HR documentation gaps create compliance risk and employee confusion. When someone asks a policy question and no documentation exists, report it: `topic="workplace accommodation request process for neurodivergent employees" description="No specific accommodation guidance found beyond general ADA policy; employees are asking and HR is handling ad hoc"`

**propose_update** — When you find a policy that conflicts with current law, newer company guidance, or changed practice, propose the update formally: `target_table="entries" target_id="..." changes={...} rationale="Parental leave policy still states 6 weeks; board approved extension to 12 weeks in January 2026"`

## Tips

- HR policies vary by jurisdiction, employee classification, and sometimes business unit. Always include relevant context in your queries: the employee's location, whether they are exempt or non-exempt, full-time or part-time. A query about overtime policy means nothing without knowing the classification.
- Benefits documentation has an annual cycle. Open enrollment materials, Summary Plan Descriptions, and rate sheets change each plan year. Verify that the documents you surface are from the current plan year, not a prior one.
- Some HR questions do not have a documented answer yet. If you search and find nothing, say so clearly and recommend that the person contact HR directly. Do not extrapolate from tangentially related policies — HR advice based on incorrect policy citations causes real harm.
- Performance management and disciplinary documentation is highly sensitive even within HR. If your results include specific employee names in performance contexts, note the sensitivity and confirm the requester has a legitimate need to know.
