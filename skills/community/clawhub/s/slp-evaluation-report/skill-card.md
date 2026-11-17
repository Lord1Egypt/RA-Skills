## Description:

Drafts initial speech-language pathology diagnostic evaluation reports from completed assessments, including case history, assessment results, clinical impressions, functional impact, and evidence-based recommendations for licensed SLP review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Licensed SLPs, Clinical Fellows, and clinical supervisors use this skill to turn completed speech-language assessments into structured draft diagnostic evaluation reports for review, editing, and signature. It supports documentation for clinical, educational, payer, and referral workflows without replacing licensed clinical judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical or educational users could treat draft language as a final signed evaluation.

Mitigation: Keep the draft-only label, clinician attestation placeholder, and licensed SLP review and signature requirement before any clinical, educational, payer, or third-party use.

Risk: Patient privacy exposure could occur if direct patient identifiers are entered into the assistant.

Mitigation: Use only a case ID or pseudonym, avoid names, dates of birth, addresses, SSNs, MRNs, phone numbers, and insurer IDs, and handle clinical details only in the required privacy and compliance environment.

Risk: Assessment interpretation may be incomplete when scores, bilingual considerations, interpreter use, or normative limitations are missing.

Mitigation: Flag unknown or unresolved items in the draft flags section and require licensed SLP confirmation before finalizing diagnostic impressions and recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/slp-evaluation-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown draft report with section labels and draft flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft only; requires licensed SLP review and signature before clinical, educational, or insurance use.]

## Skill Version(s):

0.1.0 (source: changelog, released 2026-05-28; server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
