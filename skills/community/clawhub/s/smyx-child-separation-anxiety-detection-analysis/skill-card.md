## Description:

Analyzes pre-school drop-off videos for crying, clinging, and resistance behaviors, then reports a separation-anxiety level and supportive suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and preschool staff use the skill to review drop-off videos, understand observed crying or resistance, and consider supportive responses. It provides observational summaries and does not make a clinical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags account and credential handling, including broad credential sending, without enough clarity about where credentials go.

Mitigation: Avoid installation until the developer explains account creation and credential storage, and restricts the destinations that can receive credentials.

Risk: The security review says child-video upload and consent handling are not clearly disclosed.

Mitigation: Before use, confirm when footage is uploaded and how consent is obtained and handled.

Risk: The security review was partial because a referenced path was missing, so it cannot establish that reference's behavior.

Mitigation: Resolve the missing reference and review the complete skill before relying on the scan overview.

## Reference(s):

- [ClawHub release](https://clawhub.ai/18072937735/skills/smyx-child-separation-anxiety-detection-analysis)
- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis report with behavior observations, a severity level, supportive suggestions, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include observed behavior metrics, alerts, and a link to the report.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
