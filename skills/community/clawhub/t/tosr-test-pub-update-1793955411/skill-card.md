## Description:

Automated integration test that verifies skill creation, inspection, version updates, and deletion through the ClawHub REST API.

This skill is for research and development only.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this disposable integration test to check that an authorized ClawHub skill can be published, inspected, updated, and deleted during a test run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The lifecycle steps can create, update, and delete a live ClawHub skill, and cleanup is not verified by a bundled test runner.

Mitigation: Use only with authorization and a disposable skill; confirm the target before execution and verify deletion afterward.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/yinwuzhe/skills/tosr-test-pub-update-1793955411)

## Skill Output:

**Output Type(s):** [Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lifecycle guidance for publishing, inspecting, updating, and deleting a disposable skill.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
