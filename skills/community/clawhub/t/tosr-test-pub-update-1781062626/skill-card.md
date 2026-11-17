## Description:

Automates a ClawHub API skill lifecycle test covering creation, metadata retrieval, version update, and deletion.

This skill is for research and development only.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test operators use this skill to verify the ClawHub skill lifecycle through real API publish, inspect, update, and delete operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to create, update, and delete a test skill through the real ClawHub API.

Mitigation: Use only credentials scoped to test resources, confirm the slug before cleanup, and avoid production resources that cannot be recreated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/tosr-test-pub-update-1781062626)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with API lifecycle steps and endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Use credentials limited to test resources and verify the target slug before cleanup.]

## Skill Version(s):

0.2.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
