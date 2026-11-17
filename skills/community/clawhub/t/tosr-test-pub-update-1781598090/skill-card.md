## Description:

Automated integration test skill for verifying ClawHub skill publishing, metadata inspection, version updates, and deletion.

This skill is for research and development only.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to exercise the ClawHub skill lifecycle in an integration-test flow. It is intended for publish, inspect, update, and delete validation with narrowly scoped test credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lifecycle testing can publish, update, or delete the wrong ClawHub skill if pointed at an unintended slug.

Mitigation: Verify the target slug is the intended ephemeral test slug before any publish, update, or delete operation.

Risk: Using broad credentials for lifecycle tests could increase the impact of an accidental API operation.

Mitigation: Use narrowly scoped test credentials when installing or using this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/tosr-test-pub-update-1781598090)
- [ClawHub publisher profile](https://clawhub.ai/user/yinwuzhe)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls]

**Output Format:** [Markdown guidance describing ClawHub lifecycle API operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled executable code; intended for ephemeral lifecycle testing.]

## Skill Version(s):

0.2.0 (source: server release evidence and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
