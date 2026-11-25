## Description:

Detects whether anyone has fallen within a target area using video analysis for safety monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Home safety users can submit a video for fall detection and receive a structured result, alerts, and report links. Fall alerts are for reference and should be confirmed by a person.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video upload and data-retention practices are not clear.

Mitigation: Confirm the upload destination and retention practices before sending sensitive footage.

Risk: Credential handling could expose access beyond trusted services.

Mitigation: Restrict credentials to trusted destinations and avoid exposing API keys in user-facing output.

Risk: The skill may create an account automatically and access historical reports without a clear, separate confirmation.

Mitigation: Require explicit user intent for account creation and historical report access.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-fall-detection-video-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Report links]

**Output Format:** [Structured analysis results in JSON or text; historical report lists in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fall alerts are for safety reference and require human confirmation.]

## Skill Version(s):

1.0.22 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
