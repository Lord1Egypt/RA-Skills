## Description:

Helps licensed mental-health clinicians or supervised trainees convert deidentified intake notes and mental status exam data into a draft 4Ps biopsychosocial case formulation with provisional DSM-5-TR/ICD-11 diagnosis, risk-management flags, and questions for clinician review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External licensed mental-health clinicians and supervised trainees use this skill to organize deidentified intake, MSE, biopsychosocial, and risk-indicator data into a draft case formulation for review, supervision, consultation, or utilization-review preparation. The skill is not a substitute for clinical judgment, final diagnosis, treatment-plan authorship, mandated-reporting decisions, or risk assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive mental-health information.

Mitigation: Use only deidentified case details and do not provide direct identifiers such as names, dates of birth, contact details, medical record numbers, addresses, employers, schools, or photos.

Risk: Draft clinical output could be mistaken for a final diagnosis, treatment plan, or risk assessment.

Mitigation: Treat every output as draft clinical support that must be reviewed, edited, and signed by a licensed mental-health clinician or supervised trainee before use.

Risk: Acute safety, mandated-reporting, or level-of-care decisions require jurisdiction-specific professional action.

Mitigation: Follow the user's licensure jurisdiction and local safety pathways; use the skill's stop-and-confirm behavior for active suicide, homicide, abuse, psychosis, intoxication, withdrawal, or acute medical-risk signals.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown draft case formulation with headings, tables, risk flags, questions to resolve, and mandatory clinician-review banners.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires deidentified client details; output remains a draft for licensed clinician review before medical-record use, client sharing, utilization review, or care decisions.]

## Skill Version(s):

0.1.1 (source: changelog, released 2026-05-28; server release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
