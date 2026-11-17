## Description:

Queries patient details by patient number or ID through an external endpoint that requires no authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lc-nian](https://clawhub.ai/user/lc-nian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or support agents use this skill to retrieve patient records when a user supplies a patient ID or number. It should only be used where the organization is authorized to access those records and has privacy controls outside the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retrieve sensitive patient information from an external endpoint using only a patient ID.

Mitigation: Use it only with explicit authorization to access those records and only after the service owner confirms authentication, authorization, logging, and privacy controls outside the skill.

Risk: Use with real patient data may create medical privacy or compliance exposure.

Mitigation: Do not use it with real patient data unless the deployment complies with applicable medical and privacy rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lc-nian/skills/tyxh-lc)
- [Patient lookup API endpoint](https://kjcrmcs.tianyuxh.com:8107/task/agent_test/getPatientInfo)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a patient_id query parameter; endpoint responses may contain sensitive patient information.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
