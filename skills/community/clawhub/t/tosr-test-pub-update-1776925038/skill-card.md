## Description:

Automated integration test for the full ClawHub skill lifecycle: publish, inspect, update, and delete a skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill as an automated integration-test artifact for ClawHub publish, inspect, update, and delete lifecycle checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could mistake this ephemeral integration-test artifact for a general-purpose ClawHub skill.

Mitigation: Use it only for controlled lifecycle test workflows and confirm the intended slug and version before relying on its output.

Risk: The described workflow includes publish, update, and delete operations against the live ClawHub API.

Mitigation: Review the target skill, credentials, and environment before executing lifecycle API actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/tosr-test-pub-update-1776925038)
- [Publisher profile](https://clawhub.ai/user/yinwuzhe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text lifecycle test guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled code; evidence describes lifecycle API checks only.]

## Skill Version(s):

0.2.0 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
