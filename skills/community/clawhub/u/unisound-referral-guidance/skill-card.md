## Description:

Provides primary-care referral guidance from a patient condition summary, including referral need, urgency, target department or hospital level, pre-transfer measures, and required transfer documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians in community clinics and primary-care settings use this skill to convert de-identified patient summaries into referral decision support. The output helps review referral urgency, destination, pre-transfer actions, and materials to accompany the patient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patient summaries and API credentials may be sent to configurable remote services.

Mitigation: Use only de-identified patient summaries, keep the base URL on an approved HTTPS endpoint, and use a limited, revocable API key.

Risk: Referral recommendations may be incorrect or incomplete for a specific clinical context.

Mitigation: Treat the output as clinical decision support and require qualified clinical review before acting, especially in urgent cases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-referral-guidance)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON followed by a natural-language summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print to stdout or write UTF-8 output to a file; accepts plain-text or JSON patient summaries.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
