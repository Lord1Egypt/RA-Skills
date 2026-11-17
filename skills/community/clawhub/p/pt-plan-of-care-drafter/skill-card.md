## Description:

Drafts outpatient Physical Therapy Plans of Care aligned to APTA Defensible Documentation and CMS/Medicare Part B requirements, producing draft ICF problem lists, measurable goals, interventions, and certification blocks for licensed PT review and sign-off.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Licensed PTs, PTAs under supervision, PT students, and rehab documentation specialists use this skill to draft outpatient PT plans of care for review and sign-off. It helps structure PHI-minimized intake, examination summaries, ICF problem lists, goals, interventions, payer flags, certification windows, and open questions.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Drafts may contain incorrect clinical, payer, or regulatory conclusions.

Mitigation: Require licensed PT review and sign-off before clinical use, certification, claim submission, medical-necessity conclusions, skilled-service determinations, or KX decisions.

Risk: Inputs may include PHI or payer-sensitive documentation.

Mitigation: Use only the minimum necessary patient details, avoid direct identifiers, and keep working drafts limited to initials, age, and placeholders.

Risk: Positive red-flag findings may require referral instead of a plan-of-care draft.

Mitigation: Halt drafting and surface referral disposition to the licensed PT when red flags or abuse, neglect, or trafficking concerns are present.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/pt-plan-of-care-drafter)
- [README](artifact/README.md)
- [CHANGELOG](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown draft plan of care]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft clinical documentation for licensed PT review; includes PHI-minimized placeholders, certification block, payer flags, red-flag referral disposition, and open questions.]

## Skill Version(s):

0.1.1 (source: server release metadata and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
