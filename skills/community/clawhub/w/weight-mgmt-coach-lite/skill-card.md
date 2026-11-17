## Description:

A Chinese-language health and weight-management assistant that helps users interpret health-check reports or complete a 20-question questionnaire to generate lifestyle, nutrition, weight-management, glucose-control, and fat-loss guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1027399464-tech](https://clawhub.ai/user/1027399464-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill for informational weight-management support, health-check report explanation, BMI and calorie estimates, lifestyle suggestions, and structured health assessment reports. The skill is not intended for diagnosis, prescribing, or replacing professional medical care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate broadly on ordinary diet, weight, or health-management mentions.

Mitigation: Review activation behavior before installation and restrict use to conversations where health and weight-management assistance is intended.

Risk: Users may treat generated health, nutrition, or report explanations as medical advice.

Mitigation: Keep outputs framed as informational support, avoid diagnosis or prescriptions, and direct disease, medication, or urgent symptoms to qualified medical professionals.

Risk: Uploaded health-check reports may contain sensitive personal health information.

Mitigation: Only provide report text when comfortable sharing it with the agent environment, and avoid adding unnecessary identifiers.

Risk: The artifact includes promotional consultation guidance in generated reports and an instruction to repackage that guidance if blocked.

Mitigation: Review generated reports for unwanted promotion and remove or disable consultation-routing content before deployment where advertising or solicitation is inappropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1027399464-tech/skills/weight-mgmt-coach-lite)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report text and concise conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request user-provided health questionnaire answers or report text; generated health guidance is informational and should not be treated as medical advice.]

## Skill Version(s):

1.0.0 (source: server evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
