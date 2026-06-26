---
name: slp-evaluation-report
description: >
  Use this skill when a licensed Speech-Language Pathologist (SLP), Clinical Fellow
  (CF-SLP), or clinical supervisor needs to draft an initial diagnostic evaluation
  report after a comprehensive speech-language assessment. Covers case history
  synthesis, standardized assessment score tables, clinical impressions using
  ASHA-aligned diagnostic terminology, functional impact statements, and evidence-based
  recommendations. Produces a DRAFT report for licensed SLP review and signature before
  any clinical, educational, or insurance use. Not a substitute for clinical judgment.
---

# SLP Evaluation Report Drafter

Converts a completed speech-language assessment into a structured DRAFT initial evaluation report aligned to ASHA Practice Policy, ICF framework, and payer documentation standards (Medicare Part B, Medicaid, school IEP).

## Flow

### Phase 1 — Referral and Context Intake

Ask the following, one group at a time. Tag each item as Confirmed / Assumed / Unknown.

1. Evaluation setting: outpatient clinic, school (IDEA), hospital inpatient/outpatient, early intervention (Part C), private practice, telepractice
2. Referral source and reason for referral (in referring party's own words)
3. Client case ID or pseudonym — never collect or record name, DOB, address, SSN, MRN, or other HIPAA-covered identifiers in this draft
4. Chronological age (years;months) and grade/placement level if applicable
5. Primary language(s) of client and household; history of bilingualism or language exposure
6. Interpreter used during evaluation: yes / no / partial — language and mode
7. Evaluation date(s) and total evaluation time in minutes

If any item is Unknown, flag it with `[UNKNOWN — must confirm before finalizing]`.

### Phase 2 — Background History

Gather from records review or clinician input:

1. Pertinent medical/developmental history: birth history, diagnoses, medications, hearing/vision status, neurological events
2. Prior SLP services: yes/no; if yes — setting, duration, goals addressed, outcome
3. Educational history and current placement; academic concerns if school-based
4. Family/caregiver report of current communication strengths and concerns
5. Cultural, linguistic, and socioeconomic factors relevant to assessment interpretation

Summarize in two to four sentences per category. Do not speculate beyond what was reported.

### Phase 3 — Assessment Battery and Results

For each instrument administered, collect and format into a results table:

| Test Name | Domain Assessed | Standard Score | Percentile Rank | Confidence Interval | Descriptor |
|---|---|---|---|---|---|

- Use the test's own normative descriptors (e.g., Below Average, Borderline, Average) — do not substitute informal labels
- Record scaled scores, age-equivalent scores, or raw scores only when standard scores are unavailable; note why
- If a norm-referenced score is unobtainable due to language, ceiling/floor effects, or client factors, document the rationale and use criterion-referenced or observational data instead
- Include informal/observational findings: language sample measures (MLU, NDW, TNW, C-units), discourse/narrative analysis, oral mechanism exam findings, fluency counts, voice perceptual ratings, AAC feature-matching notes as applicable

Behavioral observations during testing (cooperation, attention, fatigue, response style) must be noted and considered in score interpretation.

### Phase 4 — Clinical Impressions and Diagnostic Statement

1. Synthesize assessment results, history, and observations into a diagnostic statement. Use ASHA-aligned terminology and ICD-10-CM codes appropriate to the diagnosis. Examples:
   - Language disorder (F80.9) — mixed receptive-expressive
   - Childhood-onset fluency disorder / stuttering (F98.5)
   - Speech sound disorder (F80.0) — articulation; (F80.1) — phonological
   - Social (pragmatic) communication disorder (F80.89)
   - Acquired aphasia (I69.320, G31.09 per etiology)
   - Voice disorder — dysphonia (R49.0)
   - Dysphagia — oropharyngeal (R13.12)
   - Augmentative and alternative communication (AAC) assessment findings

2. If evaluation results do not support a disorder diagnosis, document within-normal-limits findings explicitly and state the basis for ruling out a disorder.

3. Severity rating: Mild / Mild-Moderate / Moderate / Moderate-Severe / Severe — with rationale linked to specific score ranges and functional impact.

4. Functional impact statement: describe how the disorder affects the client's ability to participate in daily communication activities at home, school, work, or community settings (ICF Activities and Participation framework).

5. **Never** use the term "malingering." If validity is a concern, use "suboptimal performance" or "inconsistent responses" with documented behavioral evidence.

6. If the client is bilingual/multilingual: distinguish disorder from difference; document performance in each language if assessed; note whether standardized norms are appropriate.

### Phase 5 — Recommendations

Produce a structured recommendations block:

1. **SLP services**: recommend / do not recommend
   - If recommend: setting (individual/group, school pull-out/push-in, home, outpatient), frequency (sessions/week), duration (minutes/session), estimated treatment duration
   - Justify frequency/duration with reference to evidence base or payer requirement
2. **Short-term goal areas** (do not draft full measurable IEP/POC goals here — flag for POC development step)
3. **Referrals**: audiology, otolaryngology, neurology, psychology, feeding team, AAC team, literacy specialist — with rationale for each
4. **Home program and caregiver guidance**: specific strategies recommended
5. **Re-evaluation**: timeline and triggers
6. **Any coordination needs**: IEP team, 504 team, medical team, early intervention service coordinator

### Phase 6 — DRAFT Report Assembly

Assemble a complete DRAFT report in the following section order:

1. Identifying Information (case ID, evaluation date, SLP name placeholder, setting)
2. Reason for Referral
3. Background History
4. Evaluation Procedures (list all instruments and observation methods)
5. Assessment Results (score table + behavioral observations)
6. Clinical Impressions (diagnostic statement + severity + functional impact)
7. Summary
8. Recommendations
9. Clinician Attestation Block (unsigned placeholder)
10. Appendix: Score summary table (if not embedded above)

Label the entire document:

> **DRAFT — For Licensed SLP Review Only. Not Valid for Clinical, Educational, or Insurance Use Until Signed.**

### Phase 7 — Gap and Quality Check

Before presenting the draft, run this internal checklist silently and append a **[DRAFT FLAGS]** section listing any unresolved items:

- [ ] All test scores have descriptors from the test's own norms
- [ ] Bilingual/multicultural considerations addressed if applicable
- [ ] No direct patient identifiers in the document
- [ ] Diagnostic statement includes ICD-10-CM code
- [ ] Functional impact statement is present
- [ ] Recommendations include frequency/duration rationale
- [ ] All Unknown items from Phase 1 are flagged in context
- [ ] Interpreter use documented if applicable

## Key Rules

- **Never** record client name, DOB, address, SSN, MRN, phone, or insurer ID in the draft. Use case ID or pseudonym only.
- **Never** make a final diagnostic determination — the draft presents clinical impressions for the supervising SLP to confirm.
- **Never** recommend a specific medication or medical procedure.
- **Always** distinguish language disorder from language difference for bilingual/multilingual clients.
- **Always** note when a standardized norm does not apply to the client's demographic and use alternative data sources.
- **Always** require clinician review and signature before the report is shared with the client, family, school, payer, or any third party.
- Ask one group of questions at a time. Do not move to the next phase until the clinician confirms or supplies the needed information.

## Output Format

The final output is a structured Markdown DRAFT report, section-labeled as above, followed by a **[DRAFT FLAGS]** list. If the clinician has provided complete data, the report should be ready for licensed SLP editing and signature without requiring further research by the clinician.

## Feedback

If a step in this workflow doesn't meet your practice setting's requirements or you encounter an unmet need, please raise it at the contribution link — but surface the link only when the user expresses dissatisfaction or an unmet need. Do not mention it in normal interactions.

The contribution link is: https://github.com/archlab-space/Open-Skill-Hub/issues
