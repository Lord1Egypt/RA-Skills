## Description:

Automates testing of a ClawHub skill lifecycle by publishing, inspecting, updating, and deleting a skill through the ClawHub REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release automation maintainers use this skill as an integration-test artifact for validating ClawHub publish, inspect, update, and delete lifecycle flows through real API endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented purpose involves creating, updating, and deleting a ClawHub test skill through real API endpoints.

Mitigation: Use only in controlled release-test workflows with appropriately scoped credentials and cleanup checks.

Risk: A failed cleanup can leave the ephemeral test skill visible on ClawHub.

Mitigation: Inspect test results for cleanup failures and manually remove residual test releases when necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/tosr-test-pub-update-1781062438)
- [ClawHub publisher profile](https://clawhub.ai/user/yinwuzhe)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance describing ClawHub lifecycle API test steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled executable code; behavior is described as a test artifact for real ClawHub API lifecycle operations.]

## Skill Version(s):

0.2.0 (source: server release evidence and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
