## Description:

Analyzes pet grooming videos for visible stress behaviors such as struggling, panting, and tail tucking, then summarizes observed signals and stress levels for groomers and veterinary teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

External pet groomers, veterinary teams, and pet care providers can use the skill to review visible stress signals during grooming and consult analysis reports. Results are behavior observations, not medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious for credential and identity risks, behavior beyond video analysis, and a mode that may submit video despite saying it will not. Scanner coverage was partial because a referenced local path was missing.

Mitigation: Consider avoiding installation unless comfortable with the reported risks. If proceeding, do not provide sensitive footage or credentials until the receiving service, its privacy practices, and its account and saved-data handling have been verified.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-pet-grooming-stress-behavior-analysis)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Structured behavior analysis with observed stress signals, a stress level, and report links; available as JSON or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Behavior observation only; does not provide medical diagnosis or behavior modification plans.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
