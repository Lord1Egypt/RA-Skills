## Description:

Analyzes pet sleep footage to report sleep duration, position changes, awakenings, and a sleep-quality score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and caregivers use the skill to review nighttime camera footage, monitor sleep patterns, and retrieve past reports. Its findings are not a veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pet camera footage and report history are sent to external LifeEmergence/Open API services.

Mitigation: Review the service's privacy, retention, and deletion practices before using sensitive home, clinic, or boarding footage.

Risk: The skill automatically creates or reuses a local identity and stores authentication tokens.

Mitigation: Review account and token handling before installation and restrict access to local identity data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-sleep-quality-analysis-analysis)
- [Skill API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured sleep-analysis text or JSON with report links; Markdown for report listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save results to a file and retrieve historical reports.]

## Skill Version(s):

1.0.13 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
