## Description:

Assists drug-development teams with clinical trial method design by organizing study objectives, phase, population, endpoints, and visit schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical research and drug-development teams use this skill to convert trial inputs such as indication, intervention, phase, objectives, population, endpoints, and visits into a structured clinical-trial design review. The output is decision support and still requires clinical, statistical, ethics, and regulatory review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical or proprietary R&D data may be processed through a remote medical-model endpoint and document-processing tools.

Mitigation: Use only approved environments and endpoints, prefer JSON input for sensitive work, and confirm data-handling approval before deployment.

Risk: Credentials can be supplied on the command line as an app key.

Mitigation: Avoid passing real app keys on the command line when possible and use an approved secret-handling path.

Risk: Document inputs and the external _shared preprocessing fallback can expand the execution and data-processing surface beyond the reviewed package.

Mitigation: Sandbox untrusted documents and review or remove the external _shared fallback before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-clinical-trial-design)
- [Clinical Trial Protocol Skill reference](https://agent-skills.md/skills/anthropics/healthcare/clinical-trial-protocol-skill)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [UTF-8 JSON containing structured trial-design data and Markdown guidance text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided clinical-trial inputs and an app key for the remote medical-model endpoint.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
