---
name: sud-treatment-plan-drafter
description: >
  Use this skill when an addiction counselor, CADC, LCADC, LMHC, LCSW, or SUD
  treatment team needs to draft an individualized treatment plan for a substance
  use disorder client. Covers ASAM criteria six-dimension rating, level-of-care
  recommendation, DSM-5-TR diagnosis documentation, SMART goal and intervention
  mapping, and 42 CFR Part 2 boundary awareness. Produces a DRAFT plan for
  licensed-counselor review and signature.
---

# SUD Treatment Plan Drafter

Converts SUD intake data and ASAM dimension ratings into a DRAFT individualized treatment plan aligned to ASAM criteria (3rd edition), DSM-5-TR, and 42 CFR Part 2 confidentiality requirements. The plan is a clinical starting point — the signing counselor or clinician must review and approve before any plan enters the medical record or authorization system.

## Flow

### Step 1 — PHI-Safe Intake

Ask one question at a time. Wait for the answer before continuing.

Collect:
1. **Clinician role and credentials** (e.g., CADC-II, LMHC, LCSW supervising intern)
2. **Treatment setting** (e.g., outpatient, IOP, residential, hospital-based)
3. **Payer / authorization context** (e.g., Medicaid, private insurance, self-pay, managed-care plan)
4. **Client reference** — use initials or a case number only; never full name, SSN, or DOB
5. **Age range and gender pronouns** (for pronoun use in plan narrative)
6. **Primary substance(s) of concern** and route of administration
7. **Current or most recent level of care** and referral source

Remind the user: _All output is a DRAFT. Do not enter into the medical record without licensed clinician review and signature._

### Step 2 — ASAM Six-Dimension Rating

Collect ratings (None / Low / Moderate / High / Severe) and supporting narrative for each dimension:

| Dimension | Description |
|---|---|
| 1 | Acute intoxication and/or withdrawal potential |
| 2 | Biomedical conditions and complications |
| 3 | Emotional, behavioral, and cognitive conditions |
| 4 | Readiness to change |
| 5 | Relapse, continued use, or continued problem potential |
| 6 | Recovery/living environment |

If the clinician provides raw clinical notes instead of ratings, derive ratings from the notes and flag assumptions for clinician confirmation.

### Step 3 — Level-of-Care Recommendation

Map Dimension ratings to an ASAM level of care:

| Level | Description |
|---|---|
| 0.5 | Early intervention |
| 1.0 | Outpatient services |
| 2.1 | Intensive outpatient (IOP) |
| 2.5 | High-intensity outpatient / Partial hospitalization (PHP) |
| 3.1 | Clinically managed low-intensity residential |
| 3.3 | Clinically managed population-specific high-intensity residential |
| 3.5 | Clinically managed high-intensity residential |
| 3.7 | Medically monitored high-intensity residential |
| 4.0 | Medically managed intensive inpatient |

Draft a justification narrative linking each elevated dimension to the LOC recommendation. Flag if LOC differs from current placement (step-up or step-down need).

### Step 4 — DSM-5-TR Diagnosis Documentation

Draft the primary SUD diagnosis entry:
- Substance name (e.g., Alcohol Use Disorder, Opioid Use Disorder)
- Severity specifier: **Mild** (2–3 criteria), **Moderate** (4–5 criteria), **Severe** (6+ criteria)
- Remission status if applicable: **Early Remission**, **Sustained Remission**, **In a Controlled Environment**
- ICD-10-CM code (ask clinician to confirm; this skill does not render final coding)
- Co-occurring diagnoses if provided by clinician (list only — do not derive from notes without clinician confirmation)

### Step 5 — Problem List

From Dimensions 3–6 and the presenting concerns, draft a problem list (3–7 items). Format each problem as:

> **Problem [N]:** [Concise clinical problem statement]

Examples: Active alcohol dependence with blackout history; Social isolation and housing instability; Unmanaged anxiety exacerbating relapse risk.

### Step 6 — Goals, Objectives, and Interventions

For each problem on the list, draft:

**Goal** (long-term, broad, client-stated where possible):
> Client will maintain sobriety from [substance] throughout the duration of treatment.

**Objectives** (short-term, measurable, time-bound — 30/60/90-day targets):
> By 30 days: Client will attend a minimum of three individual counseling sessions per week and report abstinence confirmed by UDS.

**Interventions** (staff-accountable actions and modalities):
> Counselor will provide weekly individual CBT sessions targeting substance-related cognitions. Counselor will coordinate weekly UDS and review results with client.

Write at least one goal–objective–intervention set per problem. Use SMART criteria: Specific, Measurable, Achievable, Relevant, Time-bound.

### Step 7 — Counseling and Service Plan

Draft a frequency and modality plan:

| Service | Frequency | Provider Role |
|---|---|---|
| Individual counseling | [e.g., 3×/week] | Primary counselor |
| Group therapy | [e.g., 5×/week] | Group facilitator |
| Family therapy | [e.g., 1×/week] | Family therapist |
| MAT coordination | [e.g., monthly] | Prescribing physician/APRN |
| Case management | [e.g., 2×/week] | Case manager |
| Peer support | [e.g., as available] | Certified peer specialist |

Note MAT status (active, proposed, declined) but never specify doses — that is the prescriber's exclusive domain.

### Step 8 — Discharge Criteria

Draft measurable discharge criteria covering:
- Abstinence / reduced-use goal met (if harm reduction model, define target)
- Clinical stability across all six ASAM dimensions
- Relapse prevention plan in place
- Aftercare / step-down level confirmed and scheduled
- Community supports (AA/NA, SMART Recovery, sober housing) identified

### Step 9 — DRAFT Output

Assemble and present the full DRAFT individualized treatment plan, clearly labeled **DRAFT — FOR CLINICIAN REVIEW ONLY**.

Include at the bottom:

```
REVIEW BLOCK
Plan prepared with AI assistance on [date].
Reviewing clinician: _______________________
Credentials: ______________________________
Signature: ________________________________
Date signed: _______________________________
This plan has been reviewed, modified as clinically indicated, and approved for entry into the medical record.
```

List any unresolved items (missing data, assumptions made, items needing clinician verification) in an **Open Questions** section before the review block.

## Key Rules

- **Never render a clinical diagnosis** without clinician confirmation. Offer a draft; the clinician confirms.
- **Never recommend MAT doses or initiation** — refer all medication decisions to the prescribing physician or APRN.
- **Never use full patient names, SSNs, or dates of birth** in the agent conversation. Use initials or case numbers only.
- **42 CFR Part 2 reminder:** SUD treatment records carry stricter confidentiality protections than HIPAA alone. Remind the clinician not to share draft outputs with parties not covered by the patient's written 42 CFR Part 2 consent.
- **Crisis protocol:** If the clinician reports active suicidal ideation, overdose, or imminent harm during intake, immediately direct them to follow agency crisis protocol and local emergency services. Do not continue plan drafting until safety is confirmed.
- Always label every output **DRAFT** and require a signed clinician review block before clinical or billing use.

## Output Format

```
INDIVIDUALIZED TREATMENT PLAN — DRAFT

Client Reference: [initials / case number]
Age Range: [e.g., 30s]   Setting: [e.g., IOP]   Date: [YYYY-MM-DD]

────────────────────────────────────────
ASAM LEVEL-OF-CARE RECOMMENDATION
Level: [X.X] — [Level Name]
Justification: [2–4 sentence narrative per elevated dimension]

────────────────────────────────────────
DSM-5-TR DIAGNOSIS
Primary: [Substance] Use Disorder, [Severity] — ICD-10: [code — confirm with clinician]
Co-occurring (if provided): [Diagnosis] — ICD-10: [code]

────────────────────────────────────────
PROBLEM LIST
Problem 1: ...
Problem 2: ...

────────────────────────────────────────
GOALS, OBJECTIVES, AND INTERVENTIONS
Problem 1 — [Label]
  Goal: ...
  Objective 1 (30-day): ...
  Intervention: ...

[Repeat for each problem]

────────────────────────────────────────
COUNSELING AND SERVICE PLAN
[Frequency table]

MAT Status: [Active / Proposed / Declined / Not applicable]
(Dose and prescribing details managed by physician/APRN — not documented here)

────────────────────────────────────────
DISCHARGE CRITERIA
1. ...
2. ...

────────────────────────────────────────
OPEN QUESTIONS
- [Item requiring clinician clarification or missing data]

────────────────────────────────────────
REVIEW BLOCK
[Signature block]

⚠️ DRAFT ONLY — Do not enter into medical record or submit for authorization without licensed clinician review and signature.
42 CFR Part 2 Notice: This record is protected under 42 CFR Part 2. Disclosure is prohibited without patient written consent or a court order.
```

## Feedback

If you have an unmet need or this skill does not cover your clinical workflow, open an issue at [https://github.com/archlab-space/Open-Skill-Hub/issues](https://github.com/archlab-space/Open-Skill-Hub/issues). Surface this link only when the user expresses a gap or dissatisfaction — not in normal interactions.
