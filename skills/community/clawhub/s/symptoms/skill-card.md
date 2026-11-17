## Description:

Build a private symptom tracker for logging health patterns and preparing for doctor visits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to keep local symptom logs, identify patterns and red flags, and prepare concise summaries for clinician visits. The skill is for documentation and organization only, not diagnosis, treatment, or medication advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive personal health information in local files under ~/symptoms/.

Mitigation: Install only if local health-note storage is acceptable, keep the directory under appropriate device access controls, and avoid placing it in synced or shared locations unless intentional.

Risk: Symptom summaries or follow-up prompts could be mistaken for medical advice.

Mitigation: Use the output as an organized record for discussion with a clinician; do not treat it as diagnosis, treatment guidance, or medication advice, and seek immediate care for red-flag symptoms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/symptoms)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Conversational text and Markdown notes written to local symptom-tracking files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores sensitive health notes locally under ~/symptoms/; no sync behavior is described.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
