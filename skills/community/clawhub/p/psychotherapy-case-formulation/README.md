# Psychotherapy Case Formulation

**Platforms:** Claude · Openclaw · Codex
**Domain:** Mental Health

## Purpose

Turns intake data, mental status exam, history, and risk indicators into a structured 4Ps biopsychosocial case formulation. Walks the clinician through PHI-safe intake, biological / psychological / social / cultural-spiritual factor capture, 4Ps synthesis, provisional diagnosis with differential, and treatment-direction recommendation, and produces a DRAFT case formulation with risk-management flags and a "Questions to Resolve" list — for licensed mental-health clinician review, supervision, and insurance-utilization review. Never a diagnosis, never a treatment plan, never a substitute for in-person clinical judgment.

## When to Use

- Drafting a biopsychosocial case formulation after a 90791 intake
- Preparing a case for clinical supervision, peer consultation, or staffing
- Refreshing a formulation when the client's clinical picture shifts (new stressor, relapse, new diagnosis)
- Preparing utilization-review documentation that requires a coherent formulation
- Teaching context — supervisees, psychiatry residents, doctoral practicum students learning the 4Ps / 5Ps framework
- Pre-session preparation for a complex case where the clinician wants the formulation organized before the hour

## What It Does

**Phase 1: Intake Context**
1. Confirms practitioner role and licensure jurisdiction (psychologist, LCSW, LMFT, LPC, LMHC, psychiatric NP, psychiatrist, resident, supervisee, student)
2. Captures deidentified client identifier, encounter type, session number, and presenting problem in the client's own words
3. Establishes PHI-safety rules and confirms the user has the legal basis to share information

**Phase 2: Biopsychosocial Factor Capture**
4. Biological factors — medical conditions, medications (current and historical), substance use, sleep, family psychiatric history, neurodevelopmental history
5. Psychological factors — trauma history, attachment, prior diagnoses, prior treatment response, coping style, schemas, identity, self-concept
6. Social factors — relationships, work / school, housing, finances, legal involvement, support system
7. Cultural / spiritual / contextual factors — culture, faith, language, immigration status, marginalization, gender identity, sexual orientation, community
8. Mental Status Examination summary
9. Risk indicators — suicidal ideation (with intent / plan / means / access), self-harm, homicidal ideation, abuse / neglect (mandated-reporter triggers), psychosis, intoxication

**Phase 3: 4Ps Synthesis**
10. Predisposing factors — what made this client vulnerable
11. Precipitating factors — what tipped this into presentation now
12. Perpetuating factors — what is keeping it going
13. Protective factors — what is keeping it from being worse, and what to leverage
14. Provisional diagnosis (DSM-5-TR / ICD-11) with at least two differentials and the data points distinguishing them

**Phase 4: Formulation Narrative & Treatment Direction**
15. Writes a 4–8 sentence formulation narrative that ties the 4Ps into a coherent story
16. Recommends a treatment direction (modality, frequency, level of care) with the rationale tied to the formulation
17. Surfaces risk-management flags, mandated-reporter triggers, and items requiring same-session safety planning
18. Lists "Questions to Resolve in Next Session" — the missing data the formulation depends on
19. Always labels the output **"DRAFT — LICENSED MENTAL HEALTH CLINICIAN REVIEW REQUIRED"**

## Output

A structured formulation document with identifying header (deidentified), problem list, biopsychosocial summary, MSE summary, 4Ps grid, provisional diagnosis with differential, formulation narrative, treatment-direction recommendation, risk-management flags, questions to resolve, and a mandatory review banner.

## Notes

This skill **drafts** a case formulation. It does not diagnose, does not prescribe, does not author a treatment plan, does not conduct risk assessment, and is not a substitute for clinical judgment in session. If the user shares acute risk content (active suicidal ideation with plan/intent/means, imminent harm to others, child / elder / dependent-adult abuse), the skill surfaces the appropriate clinical pathway and stops to remind the user of mandated-reporter and safety-planning obligations under their licensure jurisdiction. PHI shared during the session is treated as confidential and is never used in examples, tool calls, or external searches. The skill never asks for direct identifiers (full name, DOB, SSN, MRN, address) and refuses to record them if pasted.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
