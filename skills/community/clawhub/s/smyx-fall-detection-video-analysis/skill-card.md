## Description:

Detects possible falls in a target area from video streams for safety monitoring of older adults living alone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Households and care teams can submit a monitoring clip to screen for possible falls and review prior analysis reports. Treat alerts as prompts for human confirmation, not as a substitute for checking on the person.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling and forwarding to caller-supplied destinations are not fully clarified.

Mitigation: Review and approve credential destinations before installing or connecting credentials.

Risk: Video uploads and history retrieval may expose sensitive footage or report data, and consent behavior is unclear.

Mitigation: Use only footage with appropriate consent, and clarify upload, history, and export behavior before use.

Risk: Automatic account registration and storage behavior is not fully documented.

Mitigation: Confirm what account information is created and stored before installation.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-fall-detection-video-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown]

**Output Format:** [Structured fall-detection report in text or JSON, with Markdown report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include suggestions and a report link; results need human confirmation.]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata; artifact frontmatter reports 1.0.22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
