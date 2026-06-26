# PT Plan of Care Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Physical Therapy

## Purpose

Drafts an outpatient Physical Therapy Plan of Care (POC) aligned to **APTA Defensible Documentation** and **CMS / Medicare Part B** documentation requirements (42 CFR § 410.61, MLN 905365 — Complying with Outpatient Rehabilitation Therapy Documentation Requirements, and the 2025 Medicare Physician Fee Schedule update that established a plan-of-care signature exception allowing a signed and dated order or referral to meet certification needs, with referring-provider silence serving as ascent to the PT's submitted POC). The skill builds an ICF (International Classification of Functioning, Disability and Health) — aligned problem list, drafts measurable long-term and short-term goals with frequency / duration / intensity / type and skilled-service rationale, sets the certification period within the 90-day Medicare maximum, and lists the re-evaluation triggers — producing a DRAFT POC for licensed PT review and sign-off.

The skill is for **outpatient orthopaedic, neurological, vestibular, lymphedema, pelvic-health, geriatric, paediatric, and post-surgical** physical therapy in Medicare Part B, Medicaid, TRICARE, commercial, workers' compensation, and cash-pay settings. The skill is **not** for inpatient acute, inpatient rehab facility (IRF), skilled nursing facility (SNF), home health (under PDGM), or hospice POCs — those have different regulatory frames.

## When to Use

- Drafting a new POC after a PT initial evaluation
- Updating a POC at a Medicare 10-visit or 30-day progress report milestone
- Drafting a re-evaluation POC after a change in patient condition, surgery, or significant decline / plateau
- Aligning a POC to the 2025 Medicare PFS plan-of-care signature exception
- Pre-claim review preparation when a payer has requested medical-records review
- Onboarding a new PT, PT student, or PTA documenter to APTA Defensible Documentation discipline
- Triggering a focused payer-specific documentation flag (Medicare threshold, KX modifier, manual-medical-review threshold) when 2026 thresholds apply

## What It Does

**Phase 1: PHI-Safe Intake**
1. Captures clinician role (PT / PT student / PTA), payer, setting, referring provider, referral / order date and contents, patient demographics by initials only, ICD-10 medical diagnosis, ICD-10 treatment diagnosis where they differ, episode-of-care start date, prior PT episodes for the same condition, precautions, weight-bearing status, comorbidities, relevant medications, and surgical history with dates

**Phase 2: Examination Summary**
2. Builds the examination summary — history (chief complaint, mechanism of injury, prior and current level of function, patient-stated goals captured verbatim, social history relevant to discharge environment), systems review, tests and measures (each with measurement tool, score, reference value, and minimal-detectable-change citation where applicable), standardised outcome measures (with baseline score and minimal-clinically-important-difference citation), pain rating and aggravating / relieving factors, red-flag screen with referral disposition

**Phase 3: ICF-Aligned Problem List**
3. Maps each impairment to its corresponding activity limitation and participation restriction, prioritises by patient-stated goals and skilled-service eligibility, and flags each problem PT-amenable / refer-out / co-treat

**Phase 4: Measurable Goals**
4. Drafts long-term goals tied to participation restrictions and short-term goals tied to activity limitations or impairments — each with audience-anchored verb (patient will), measurable performance criterion with measurement tool, condition / setting, time frame, and skilled-service rationale (why a licensed PT or PTA under supervision is required to deliver care toward this goal)

**Phase 5: Interventions and Certification**
5. Lists interventions with type, frequency, duration, intensity, and progression criteria, sets the certification period within the 90-day Medicare maximum, lists re-evaluation triggers, and produces a plan-of-care certification block plus a discharge / transition-of-care plan

## Output

A DRAFT outpatient PT Plan of Care with:
- Examination summary (history, systems review, tests and measures, standardised outcome measures with citations, pain, red-flag screen)
- ICF-aligned problem list (impairment → activity limitation → participation restriction, with PT-amenable / refer-out / co-treat flag)
- Measurable long-term and short-term goals (audience, behaviour, condition, criterion, time frame, skilled-service rationale)
- Interventions with type, frequency, duration, intensity, and progression criteria
- Prognosis with explicit rehabilitation-potential statement
- Certification period (start date, end date, Medicare 90-day check)
- Plan-of-care certification block with the 2025 PFS signature-exception flag where applicable
- Payer-specific documentation flag (Medicare threshold attestation when 2026 thresholds apply, KX modifier rationale, manual-medical-review awareness)
- Re-evaluation trigger list (change in condition, plateau, new injury, payer milestone)
- Discharge / transition-of-care plan
- Open-questions / unresolved-information list

## Notes

This skill **drafts** the POC to support — never replace — the licensed PT's clinical judgement and the referring provider's certification where required. The skill does not deliver a final POC, does not sign the certification, does not submit a claim, does not opine on whether a service is "skilled" or "medically necessary" as a payer determination, does not opine on whether the patient meets KX-modifier criteria, and does not produce a payer-facing appeal letter. The skill enforces a PHI minimisation rule: patients are referred to by initials only in the working draft; the licensed PT inserts the full identifier into the final POC inside the EHR. The skill refuses to fabricate examination findings, outcome-measure scores, or measurement-tool citations. The skill flags every payer-specific element (Medicare threshold, KX, manual-medical-review, plan-of-care signature exception) and surfaces the licensed PT's required attestation. The skill is for **outpatient** Part B POCs only — inpatient acute, IRF, SNF, home health, and hospice POCs are out of scope.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
