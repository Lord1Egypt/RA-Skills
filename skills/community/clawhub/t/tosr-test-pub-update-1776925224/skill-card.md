## Description:

Automated test skill validating creation, inspection, update, and deletion of skills via the ClawHub REST API lifecycle.

This skill is for research and development only.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to validate ClawHub skill lifecycle behavior, including publish, inspect, update, and delete operations, in a controlled test context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exercises publish, update, and delete behavior against the real ClawHub API.

Mitigation: Use only test-scoped ClawHub credentials and the intended test slug.

Risk: Running the lifecycle flow in a production or personal namespace could create, modify, or delete unintended skill releases.

Mitigation: Do not use this skill in production or personal namespaces unless deliberately validating lifecycle behavior there.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/tosr-test-pub-update-1776925224)
- [ClawHub publisher profile](https://clawhub.ai/user/yinwuzhe)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with API lifecycle steps and endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Test-scoped ClawHub credentials and the intended test slug are required for safe use.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
