## Description:

Retrieves Bilibili's current trending searches through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to check what is currently trending on Bilibili and receive a concise summary of the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A simple trend lookup may trigger installation of qhkit or Node and changes to local shell settings.

Mitigation: Review the setup first; preinstall and pin trusted versions, and require approval before changing shell settings.

Risk: Setup may handle an API token or replace existing qhkit site and token settings.

Mitigation: Configure the token securely and require explicit approval before overwriting existing settings.

Risk: Trend queries may incur Qinghu credit charges.

Mitigation: Estimate the charge and obtain user consent before paid calls; report actual usage afterward.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-bilibili-hot-search)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise summary with key results; table file for 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid queries use Qinghu credits; report the credits consumed.]

## Skill Version(s):

0.1.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
