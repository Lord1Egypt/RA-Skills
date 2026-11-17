## Description:

Automated test skill verifying skill lifecycle operations, including publish, inspect, update, and delete, via the ClawHub REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to exercise ClawHub skill lifecycle operations against the live API. It is intended for publish, inspect, update, and delete integration testing rather than general-purpose user assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to mutate a real ClawHub skill entry during publish, update, inspect, and delete lifecycle tests.

Mitigation: Install and run it only for intentional ClawHub lifecycle integration testing, and review proposed API operations before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/tosr-test-pub-update-1778050448)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance describing ClawHub REST API lifecycle operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No embedded code was present in the artifact; outputs should be reviewed before live API execution.]

## Skill Version(s):

0.2.0 (source: server release evidence and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
