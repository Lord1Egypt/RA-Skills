## Description:

Analyzes images and videos for possible strangers near minors and returns safety-oriented findings and report links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Guardians and staff at homes, schools, and childcare facilities can submit authorized images or video for a stranger-proximity analysis report and review past reports. Findings are advisory and do not replace professional security measures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Surveillance images or video involving children, bystanders, locations, or school and home footage may be uploaded to an external cloud service.

Mitigation: Upload only media you are legally allowed to share; confirm privacy, retention, and deletion controls before use.

Risk: Account tokens may be created or stored without a clear explanation to the user, and access to historical reports is not clearly scoped.

Mitigation: Review local token storage and report access controls with the publisher before connecting sensitive accounts or querying reports.

Risk: The documented real-time alerting path is unclear, so an analysis result may not provide timely protection.

Mitigation: Do not rely on the skill as a complete child-protection or emergency alert system; verify alert delivery independently and maintain human oversight.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-stranger-approach-warning-analysis)
- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured analysis text or JSON; historical reports as a Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk assessments, recommendations, and report links; results can be saved to a file.]

## Skill Version(s):

1.0.16 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
